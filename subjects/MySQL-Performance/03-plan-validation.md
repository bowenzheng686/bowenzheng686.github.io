---
layout: default
title: "MySQL 性能调优 · 执行计划验证与优化器判断"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 03 执行计划验证与优化器判断

## 估算、实测、原因

MySQL 8.0.18 起可用 `EXPLAIN ANALYZE` 查看迭代器的实际耗时与行数；**它会执行语句**，所以先在隔离环境对 `SELECT` 使用，避免在业务高峰跑昂贵查询。普通 `EXPLAIN` 不等于真实执行时间。`FORMAT=JSON` 可查看成本与条件下推等细节，`optimizer_trace` 用于解释候选路径为何被接受或放弃，短时开启后关闭。

```sql
EXPLAIN FORMAT=JSON
SELECT * FROM employees WHERE name > 'LiLei';
EXPLAIN ANALYZE
SELECT * FROM employees WHERE name > 'LiLei';

SET SESSION optimizer_trace='enabled=on';
SELECT * FROM employees WHERE name > 'LiLei';
SELECT TRACE FROM information_schema.OPTIMIZER_TRACE\G
SET SESSION optimizer_trace='enabled=off';
```

原资料比较了 `name > 'a'` 与 `name > 'zzz'`：前者可能命中大部分表，后者可能很少，回表代价使最优路径不同。保留这个案例，但不把某个执行计划截图推广为“范围条件必然不用索引”。若估算和实测差异大，先检查统计信息、数据倾斜与参数，再考虑 `ANALYZE TABLE`，并记录它对线上负载的影响。[官方参考：优化器统计信息](https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/s/YoQZCEjl)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/02-explain-fields.html' | relative_url }}">← 上一篇：EXPLAIN 字段与访问路径</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/04-index-structure-cost.html' | relative_url }}">下一篇：索引结构与访问成本 →</a>
</nav>
