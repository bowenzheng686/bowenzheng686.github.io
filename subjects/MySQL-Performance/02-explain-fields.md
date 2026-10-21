---
layout: default
title: "MySQL 性能调优 · EXPLAIN 字段与访问路径"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 02 EXPLAIN 字段与访问路径

## 读计划时先看证据链

`EXPLAIN` 描述优化器拟采用的计划。`table`/`id`/`select_type` 标识访问对象和查询块；`possible_keys` 是候选索引，`key` 是实际所选索引，`key_len` 是计划使用的索引长度；`rows` 与 `filtered` 是估算，不是精确执行计数。`Extra` 中的 `Using index` 通常表示覆盖索引，`Using index condition` 表示索引条件下推；`Using temporary` 和 `Using filesort` 是应分析的信号，不能仅凭出现就判定慢。

```sql
EXPLAIN SELECT name, age, position
FROM employees
WHERE name LIKE 'LiLei%' AND age = 22;
```

`type` 显示访问方法，例如 `const`、`ref`、`range`、`index`、`ALL`；它不是跨所有 SQL 通用的性能分数。扫描少量行的 `ALL` 可能比大量回表的 `range` 更快。看计划时把表大小、预估扫描行数、过滤比例、回表、排序和实际耗时一起考虑。下图中优化器选择 `ALL` 而非候选复合索引，说明在该数据分布和版本下，全表扫描的估算成本可能更低。

![候选索引存在但选择全表扫描的执行计划](assets/index-1-001-c619f9d36f14.webp)

下一篇用实测核对估算。[官方参考：EXPLAIN](https://dev.mysql.com/doc/refman/8.0/en/explain.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/01-slow-sql-baseline.html' | relative_url }}">← 上一篇：慢 SQL 的定位与测试基线</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/03-plan-validation.html' | relative_url }}">下一篇：执行计划验证与优化器判断 →</a>
</nav>
