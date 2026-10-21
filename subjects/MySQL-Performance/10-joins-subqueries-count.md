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

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/09-pagination-covering.html' | relative_url }}">← 上一篇：深度分页与覆盖扫描</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/11-transactions-acid.html' | relative_url }}">下一篇：事务、ACID 与提交边界 →</a>
</nav>
