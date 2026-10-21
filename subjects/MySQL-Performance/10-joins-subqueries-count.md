---
layout: default
title: "MySQL 性能调优 · 关联、子查询与计数"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 10 关联、子查询与计数

## 先确认结果语义，再谈算法

用 `t1`/`t2` 对比有索引与无索引的关联、`IN`/`EXISTS` 和 `COUNT(*)`，同时注意版本差异：MySQL 8.0.20 起 Block Nested Loop 已被移除，可用时改由 hash join；不能仅凭 `Extra` 没有 `Using join buffer` 就断言使用某个连接算法。内连接的驱动顺序通常由优化器决定，外连接还受语义限制。

以下是可复现实验的最小表结构；先按业务比例造数，再比较两条连接计划：

```sql
CREATE TABLE t1 (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  a INT, b INT, KEY idx_a (a)
) ENGINE=InnoDB;
CREATE TABLE t2 LIKE t1;

EXPLAIN FORMAT=TREE
SELECT t1.id, t2.id FROM t1 JOIN t2 ON t1.a = t2.a;
EXPLAIN FORMAT=TREE
SELECT t1.id, t2.id FROM t1 JOIN t2 ON t1.b = t2.b;
```

高频连接先检查过滤后的行数、连接列类型/字符集、被查找侧索引和返回列。`IN` 与 `EXISTS` 可能被改写为半连接，谁更快取决于计划，不宜套固定口诀。`COUNT(*)` 统计符合条件的行；InnoDB 不保存可立即返回的全表精确行数，缓存计数或汇总表要定义一致性要求。[官方参考：Hash Join](https://dev.mysql.com/doc/refman/8.0/en/hash-joins.html)。



## 关联算法、子查询与 COUNT 实验

### Join关联查询优化

```sql
-- 示例表：
CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_a` (`a`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table t2 like t1;

-- 插入一些示例数据
-- 往t1表插入1万行记录
drop procedure if exists insert_t1;
delimiter ;;
create procedure insert_t1()
begin
  declare i int;
  set i=1;
  while(i<=10000)do
    insert into t1(a,b) values(i,i);
    set i=i+1;
  end while;
end;;
delimiter ;
call insert_t1();

-- 往t2表插入100行记录
drop procedure if exists insert_t2;
delimiter ;;
create procedure insert_t2()
begin
  declare i int;
  set i=1;
  while(i<=100)do
    insert into t2(a,b) values(i,i);
    set i=i+1;
  end while;
end;;
delimiter ;
call insert_t2();
```

### mysql的表关联常见有两种算法

- Indexed Nested-Loop Join（有可用关联索引）

- 无可用关联索引时的历史 BNL 与 MySQL 8.0.20+ hash join

1、 嵌套循环连接 Nested-Loop Join(NLJ) 算法

一次一行循环地从第一张表（称为驱动表）中读取行，在这行数据中取到关联字段，根据关联字段在另一张表（被驱动表）里取出满足条件的行，然后取出两张表的结果合集。

```sql
EXPLAIN select * from t1 inner join t2 on t1.a= t2.a;
```

![关联、子查询与计数配图](assets/index-2-011-004067c77ba3.webp)

从执行计划中可以看到这些信息：

- 本例计划以过滤后的 t2 为外侧、用 t1.a 的索引做内侧查找。`EXPLAIN` 行顺序可作为线索，但复杂计划应查看 `FORMAT=TREE` 或 `EXPLAIN ANALYZE` 的实际执行树；`INNER JOIN` 的 SQL 书写顺序不固定驱动顺序。

- 外连接通常受保留行语义约束；若过滤条件使外连接可被改写为内连接，优化器仍可能重排。内连接也不是永远由物理行数较少的表驱动，而是比较过滤后行数、索引探测、输出行数和连接算法的成本。

- 若被查找侧关联列有合适索引，常见路径是索引嵌套循环；是否使用其他算法应查看 EXPLAIN FORMAT=TREE 或 EXPLAIN ANALYZE，不能只靠 Extra 中某个字符串判断。

上面sql的大致流程如下：

- 从表 t2 中读取一行数据（如果t2表有查询过滤条件的，用先用条件过滤完，再从过滤结果里取出一行数据）；

- 从第 1 步的数据中，取出关联字段 a，到表 t1 中查找；

- 取出表 t1 中满足条件的行，跟 t2 中获取到的结果合并，作为结果返回给客户端；

- 重复上面 3 步。

在示例数据中，t2 有 100 行，t1.a 每个匹配值也只有一行，因此可把工作量直观理解为读取约 100 个外侧行、进行约 100 次索引探测并取得约 100 个匹配行。但“扫描 200 行”不是通用成本公式：索引树访问、缓存命中、重复键和投影列都会改变实际 I/O 与耗时。

如果被查找侧缺少可用关联索引，逐行全表扫描成本可能较高；现代 MySQL 版本可能选择 hash join。

2、无索引关联：历史 BNL 与现代 hash join

旧版本 BNL 将驱动侧行缓存在 join buffer 中，再扫描另一侧进行匹配；MySQL 8.0.20 起 BNL 实现已移除，无索引等值连接应结合 hash join 计划分析。

```sql
EXPLAIN select * from t1 inner join t2 on t1.b= t2.b;
```

![关联、子查询与计数配图](assets/index-2-012-c7d3deef1990.webp)

图中 Using join buffer (Block Nested Loop) 是旧版本的计划输出；MySQL 8.0.20+ 不应照此判断连接算法。

上面sql的大致流程如下：

- 把 t2 的所有数据放入到 join_buffer 中

- 把表 t1 中每一行取出来，跟 join_buffer 中的数据做对比

- 返回满足 join 条件的数据

历史 BNL 示例中，扫描行数和内存比较次数取决于两表规模及缓冲区批次。现代版本的 hash join 还要考虑哈希表构建、内存预算与溢写。

若构建侧数据不能全部放入内存，连接执行可能分批或溢写；应观测目标版本的实际算法，而不是固定套用旧版 BNL 公式。

join_buffer_size 是连接类操作的资源预算参数之一；默认值及行为以实例版本为准。

旧版 BNL 可能分批缓存并反复扫描另一侧；在新版本应以 EXPLAIN ANALYZE 的行数和耗时判断是否需要补关联索引或改写查询。

为什么关联列索引通常重要？

有可用索引时，被查找侧可按键快速定位；无索引时，可能需要扫描或构建哈希表，成本随行数、行宽和内存预算变化。

不能仅以“磁盘扫描次数”比较算法，缓存命中、构建成本、输出行数和溢写也会影响结果。

优先检查过滤后的参与行数及关联列索引，再用实测计划决定优化方向。

### 对于关联sql的优化

- 高频等值关联先评估被查找侧连接列索引，再检查两侧过滤条件、联合索引列序与返回列；建索引有写入和空间成本，全表扫描或 hash join 在某些数据分布下也可能更优。

- 先让优化器选择驱动顺序；只有证据表明计划持续不佳，才考虑 STRAIGHT_JOIN，并为数据分布变化准备回滚。

straight_join解释：straight_join功能同join类似，但能让左边的表来驱动右边的表，能改表优化器对于联表查询的执行顺序。

比如：select * from t2 straight_join t1 on t2.a = t1.a; 代表指定mysql选着 t2 表作为驱动表。

- `STRAIGHT_JOIN` 用于固定所写表的连接顺序，但不应把它当作外连接语义转换工具。外连接是否能重排还受过滤条件与优化器改写影响。

- 尽可能让优化器去判断，因为大部分情况下mysql优化器是比人要聪明的。使用straight_join一定要慎重，因为部分情况下人为指定的执行顺序并不一定会比优化引擎要靠谱。

对于小表定义的明确

“小表”应看过滤后的参与行数、行宽和可用访问路径，而不只是原始表大小。索引嵌套循环往往希望外侧行数较少且内侧探测便宜；hash join 则会比较构建侧大小、内存预算和输出基数。最终以实际计划和耗时判断。

### in和exsits优化

IN 与 EXISTS 可能被优化器改写为半连接，不能用“小表驱动大表”作为固定快慢规则。

IN：比较子查询是否可去重、是否相关、连接列索引与实际计划。

```sql
SELECT * FROM A WHERE id IN (SELECT id FROM B);
```

直观上可把它理解为判断 `A.id` 是否存在于 B 的结果集合，但实际执行可能采用半连接、物化或索引探测，不等同于固定的逐行双层循环；还要考虑 `NULL` 语义。

EXISTS：关注相关条件、每轮探测成本及优化器是否消除了逐行执行。

将主查询A的数据，放到子查询B中做条件验证，根据验证结果（true或false）来决定主查询的数据是否保留

```sql
SELECT * FROM A WHERE EXISTS (SELECT 1 FROM B WHERE B.id = A.id);
```

可以把 `EXISTS` 理解为对每个 A 行检查是否存在匹配的 B 行，但优化器可能去相关或改写为半连接。是否需要 B.id 索引，应结合 B 的大小、过滤条件与执行计划判断。

1、EXISTS (subquery)只返回TRUE或FALSE,因此子查询中的SELECT * 也可以用SELECT 1替换,官方说法是实际执行时会忽略SELECT清单,因此没有区别

2、EXISTS子查询的实际执行过程可能经过了优化而不是我们理解上的逐条对比

3、EXISTS子查询往往也可以用JOIN来代替，何种最优需要具体问题具体分析

### count(*)查询优化

```sql
SELECT COUNT(*) FROM employees;
SELECT COUNT(1) FROM employees;
SELECT COUNT(id) FROM employees;
SELECT COUNT(name) FROM employees;
-- 对比 EXPLAIN ANALYZE 与结果语义；COUNT(name) 不统计 NULL。
```

注意：`COUNT(列)` 只统计该列非 `NULL` 的行；`COUNT(*)` 和 `COUNT(1)` 统计符合条件的行。本例主键 `id` 非空，`COUNT(id)` 才与前两者结果相同。

![关联、子查询与计数配图](assets/index-2-013-5e1e6b9f7c78.webp)

执行计划相似不代表耗时完全相同；比较前还要确认统计对象是否允许 NULL。

有索引时 COUNT(*)、COUNT(1)、COUNT(id) 的实际路径由优化器选定；COUNT(可空列) 必须检查非 NULL 值，不能套固定速度排名。

无索引时也不宜给 COUNT 形式固定排名；索引宽度、缓存与谓词选择性更重要。

COUNT(1) 与 COUNT(*) 在 MySQL 中通常可由优化器采用类似计数路径，不能凭字面形式推断明显性能差异。

COUNT(*) 统计符合条件的行，不会把全部列取出；COUNT(列) 只统计非 NULL 值，二者语义不同。

InnoDB 可选择较窄的二级索引完成无条件计数，但没有可立即返回的全表精确行数；实际路径需查看计划。

### 常见优化方法

1、查询mysql自己维护的总行数

对于myisam存储引擎的表做不带where条件的count查询性能是很高的，因为myisam存储引擎的表的总行数会被mysql存储在磁盘上，查询不需要计算

![关联、子查询与计数配图](assets/index-2-014-851b35193f16.webp)

对于innodb存储引擎的表mysql不会存储表的总记录行数(因为有MVCC机制，后面会讲)，查询count需要实时计算

2、show table status

如果只需要知道表总行数的估计值可以用如下sql查询，性能很高

![关联、子查询与计数配图](assets/index-2-015-7370a7fc3319.webp)

3、将总数维护到Redis里

插入或删除表数据行的时候同时维护redis里的表总行数key的计数值(用incr或decr命令)，但是这种方式可能不准，很难保证表操作和redis操作的事务一致性

4、增加数据库计数表

插入或删除表数据行的时候同时维护计数表，让他们在同一个事务里操作



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/09-pagination-covering.html' | relative_url }}">← 上一篇：深度分页与覆盖扫描</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/11-transactions-acid.html' | relative_url }}">下一篇：事务、ACID 与提交边界 →</a>
</nav>
