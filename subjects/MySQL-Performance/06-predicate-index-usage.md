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

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/05-composite-index.html' | relative_url }}">← 上一篇：联合索引设计与最左前缀</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/07-order-group.html' | relative_url }}">下一篇：排序与分组的优化边界 →</a>
</nav>
