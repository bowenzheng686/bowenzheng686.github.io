---
layout: default
title: "MySQL 性能调优 · 过滤谓词与索引使用"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 06 过滤谓词与索引使用

## 避免把语法写成“失效清单”

范围、`IN`、`OR`、前缀 `LIKE` 在大表与小表上可能产生不同计划。正确解释是优化器按代价选路径，语法形式本身不保证或禁止索引。`LIKE 'Li%'` 可能产生可用范围；`LIKE '%Li'` 通常不能利用普通 B+ 树的有序前缀定位。列上的函数、不同类型的隐式转换也可能削弱可搜索性，但生成列/函数索引和查询改写有适用条件。

```sql
EXPLAIN SELECT * FROM employees WHERE name LIKE 'Li%';
EXPLAIN SELECT * FROM employees WHERE name IN ('LiLei','Lucy');
EXPLAIN SELECT * FROM employees WHERE name > 'LiLei';
```

索引条件下推（ICP）允许存储引擎在二级索引条目上先检验可用谓词，减少回表；它不等于把范围后的每一列都用作精确定位。`IS NULL`、`OR` 及不等式都需结合选择性、覆盖与实际计划判断。分析执行计划时，应同时核对 SQL、数据量和 MySQL 版本。[官方参考：ICP](https://dev.mysql.com/doc/refman/8.0/en/index-condition-pushdown-optimization.html)。



## IN、OR、LIKE 与索引条件下推

4、IN 和 OR 能否利用索引由谓词选择性、表规模、统计信息与回表成本共同决定。

```sql
EXPLAIN SELECT * FROM employees WHERE name in ('LiLei','HanMeimei','Lucy') AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-004-cd0bfe14e0a1.webp)

```sql
EXPLAIN SELECT * FROM employees WHERE (name = 'LiLei' or name = 'HanMeimei') AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-005-40194c2625fc.webp)

做一个小实验，将employees 表复制一张employees_copy的表，里面保留两三条记录

```sql
EXPLAIN SELECT * FROM employees_copy WHERE name in ('LiLei','HanMeimei','Lucy') AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-006-c9585e37701a.webp)

```sql
EXPLAIN SELECT * FROM employees_copy WHERE (name = 'LiLei' or name = 'HanMeimei') AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-007-3dd3a45c7f0a.webp)

5、LIKE '前缀%' 可以形成索引范围；最终计划仍由成本决定。

```sql
EXPLAIN SELECT * FROM employees WHERE name like 'LiLei%' AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-008-1d1e7f9e276f.webp)

```sql
EXPLAIN SELECT * FROM employees_copy WHERE name like 'LiLei%' AND age = 22 AND position ='manager';
```

![过滤谓词与索引使用配图](assets/index-1-009-5fc826f9e9ed.webp)

索引条件下推（ICP）可在扫描二级索引时先检查索引列上的剩余条件，从而减少不必要的回表。

什么是索引下推了？

对于联合索引 (name, age, position)，name LIKE 'LiLei%' 可形成前缀范围。范围后的 age 和 position 不一定继续缩小索引定位范围，但可由 ICP 在索引条目上先行过滤；具体以执行计划和版本为准。

没有 ICP 时，存储引擎取得候选二级索引条目后，需要回到聚簇索引读取整行，再判断尚未在索引层完成的谓词，回表可能较多。

MySQL 5.6 引入 ICP。满足条件时，存储引擎可在二级索引条目上检查 age、position 等索引列，只有通过检查的条目才回表读取完整记录。

索引下推会减少回表次数，对于innodb引擎的表索引下推只能用于二级索引，innodb的主键索引（聚簇索引）树叶子节点上保存的是全行数据，所以这个时候索引下推并不会起到减少查询全行数据的效果。

范围扫描与 ICP 为什么不能画等号？

范围条件决定候选索引条目，ICP 检查条目上的其他谓词。是否启用 ICP 与存储引擎、访问方法、覆盖情况及优化器成本判断有关；不能仅凭范围大小或 LIKE 语法作绝对判断。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/05-composite-index.html' | relative_url }}">← 上一篇：联合索引设计与最左前缀</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/07-order-group.html' | relative_url }}">下一篇：排序与分组的优化边界 →</a>
</nav>
