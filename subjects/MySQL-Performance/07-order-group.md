---
layout: default
title: "MySQL 性能调优 · 排序与分组的优化边界"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 07 排序与分组的优化边界

## 先看是否能借用索引顺序

`ORDER BY`/`GROUP BY` 能否利用索引顺序，取决于过滤条件、排序列顺序、方向、连接路径和优化器选择。`Using filesort` 是额外排序算法名称，**不代表一定落盘**；排序缓冲不足时才可能产生临时文件。`Using temporary` 也不是固定的性能故障，需要看参与行数、内存/磁盘临时表和总延迟。

```sql
EXPLAIN SELECT name, age FROM employees
WHERE name = 'LiLei' ORDER BY age;
EXPLAIN SELECT name, age FROM employees
WHERE name > 'LiLei' ORDER BY position;
```

排序可采用 `<sort_key, additional_fields>` 或 `<sort_key, rowid>` 两类模式。不应仅凭旧版本的 `max_length_for_sort_data` 阈值调整新版本配置；应以目标版本的 trace、实际行宽和内存使用验证。若过滤后只剩几十行，先过滤再排序可能优于为排序新增宽索引。减少 `SELECT *` 和过大的返回集往往同样重要。[官方参考：ORDER BY 优化](https://dev.mysql.com/doc/refman/8.0/en/order-by-optimization.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/06-predicate-index-usage.html' | relative_url }}">← 上一篇：过滤谓词与索引使用</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/08-optimizer-index-choice.html' | relative_url }}">下一篇：优化器选索引与统计信息 →</a>
</nav>
