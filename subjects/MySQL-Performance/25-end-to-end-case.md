---
layout: default
title: "MySQL 性能调优 · 端到端案例、验收与回滚"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 25 端到端案例、验收与回滚

## 把一次优化写成可复查的实验

以员工检索为例：接口按 `name` 前缀筛选并返回 `age/position`。先保留原 SQL、索引定义、目标版本、行数分布和基线；提出“减少回表”的假设，再比较仅改变投影列或索引设计后的计划与多次实测。若改动了语义（例如用 `id > 10000` 替代偏移分页），即使更快也不能视为等价优化。

```sql
EXPLAIN ANALYZE SELECT * FROM employees
WHERE name LIKE 'Li%' ORDER BY name, id LIMIT 20;
EXPLAIN ANALYZE SELECT id, name, age, position FROM employees
WHERE name LIKE 'Li%' ORDER BY name, id LIMIT 20;
```

验收记录至少包含：结果集一致性、p95/p99、扫描行数、锁等待、CPU/I/O、写入开销、索引体积和回归时段。单变量灰度后按预先约定的阈值决定保留或回滚；回滚须包含 SQL、索引和参数，不删证据。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/24-mysql-8-features.html' | relative_url }}">← 上一篇：MySQL 8.0 中与调优相关的能力</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
</nav>
