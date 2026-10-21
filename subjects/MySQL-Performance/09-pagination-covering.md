---
layout: default
title: "MySQL 性能调优 · 深度分页与覆盖扫描"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 09 深度分页与覆盖扫描

## 区分页码跳转与游标翻页

`LIMIT 10000, 10` 仍需处理前面的结果；有过滤、排序、回表时成本更高。“先取主键再回表”适合宽行且排序索引可覆盖内层查询的场景，但仍要扫描或跳过偏移量。能使用上一页边界值时，seek/keyset 分页通常更稳定：排序列不唯一时把主键作为决胜列。

```sql
CREATE INDEX idx_hire_id ON employees(hire_time, id);
SELECT id, name, hire_time FROM employees
WHERE hire_time > :last_time
   OR (hire_time = :last_time AND id > :last_id)
ORDER BY hire_time, id LIMIT 10;
```

上面的占位符由应用参数绑定；首次分页应有明确起点。它适合顺序翻页，不等价于任意页码跳转，也不能在并发写入下保证“第 N 页”永远不变。不要把“`id > 10000`”当作“跳过 10000 行”的通用改写：主键有缺口、过滤条件或不同排序时，语义不同。[官方参考：LIMIT 优化](https://dev.mysql.com/doc/refman/8.0/en/limit-optimization.html)。



## 深度分页的两类查询

### 分页查询优化

```sql
-- 示例表
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) NOT NULL DEFAULT '' COMMENT '姓名',
  `age` int(11) NOT NULL DEFAULT '0' COMMENT '年龄',
  `position` varchar(20) NOT NULL DEFAULT '' COMMENT '职位',
  `hire_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间',
  PRIMARY KEY (`id`),
  KEY `idx_name_age_position` (`name`,`age`,`position`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='员工记录表';
```

很多时候我们业务系统实现分页功能可能会用如下sql实现

```sql
select * from employees limit 10000,10;
```

LIMIT 10000,10 需要跳过前 10000 个候选结果；若没有 ORDER BY，返回顺序本身不保证稳定。深度分页的代价还取决于过滤、排序和回表。

常见的分页场景与优化前提：

1、根据自增且连续的主键排序的分页查询

首先来看一个根据自增且连续主键排序的分页查询的例子：

```sql
select * from employees limit 90000,5;
```

![深度分页与覆盖扫描配图](assets/index-2-001-d29f88aa1ada.webp)

该示例只有在结果明确按 id 排序、主键连续且已知上一页边界时，才能比较两种写法；没有 ORDER BY 的原 SQL 不保证等价。

```sql
select * from employees where id > 90000 limit 5;
```

![深度分页与覆盖扫描配图](assets/index-2-002-cde334d2a6b0.webp)

先确认结果顺序与边界语义，再比较执行计划：

```sql
EXPLAIN select * from employees limit 90000,5;
```

![深度分页与覆盖扫描配图](assets/index-2-003-e26862a93237.webp)

```sql
EXPLAIN select * from employees where id > 90000 limit 5;
```

![深度分页与覆盖扫描配图](assets/index-2-004-358d0047744d.webp)

按主键边界定位通常减少扫描；但直接以 90000 代替“跳过 90000 行”仅在严格前提下成立。

但是，这条改写的SQL 在很多场景并不实用，因为表中可能某些记录被删后，主键空缺，导致结果不一致，如下图试验所示（先删除一条前面的记录，然后再测试原 SQL 和优化后的 SQL）：

![深度分页与覆盖扫描配图](assets/index-2-005-9b4c651bcb43.webp)

![深度分页与覆盖扫描配图](assets/index-2-006-36c2dd95a3a0.webp)

删除前面的记录后，偏移量与主键值不再对应。主键有缺口或附加过滤条件时，两条 SQL 的结果不同。

另外如果原 SQL 是 order by 非主键的字段，按照上面说的方法改写会导致两条 SQL 的结果不一致。所以这种改写得满足以下两个条件：

- 主键值与行序号连续对应；或应用直接保存上一页的最后一个主键。

- 排序必须明确为 id，并考虑并发写入造成的页边界变化。

2、根据非主键字段排序的分页查询

再看一个根据非主键字段排序的分页查询，SQL 如下：

```sql
select * from employees ORDER BY name limit 90000,5;
```

![深度分页与覆盖扫描配图](assets/index-2-007-8d06bcb39029.webp)

```sql
EXPLAIN select * from employees ORDER BY name limit 90000,5;
```

![深度分页与覆盖扫描配图](assets/index-2-008-8fbf183e84f7.webp)

若排序读取大量宽行并产生回表或额外排序，优化器可能放弃 name 索引。应通过 EXPLAIN ANALYZE 核对扫描量、回表次数和实际耗时。

知道不走索引的原因，那么怎么优化呢？

可先用覆盖排序索引的内层查询取出 id，再按主键回表取宽行；仍要处理 OFFSET 的扫描成本，并以实际计划确认收益。

```sql
select * from employees e inner join (select id from employees order by name limit 90000,5) ed on e.id = ed.id;
```

![深度分页与覆盖扫描配图](assets/index-2-009-143d33bca385.webp)

此实验的耗时差异不能作为普适倍数；应在相同数据量、缓存状态和并发下多次测量。

![深度分页与覆盖扫描配图](assets/index-2-010-0a2aea47dbd0.webp)

若内层查询利用排序索引且仅返回 id，可减少宽行读取；最终是否出现 filesort 仍以目标版本执行计划为准。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/08-optimizer-index-choice.html' | relative_url }}">← 上一篇：优化器选索引与统计信息</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/10-joins-subqueries-count.html' | relative_url }}">下一篇：关联、子查询与计数 →</a>
</nav>
