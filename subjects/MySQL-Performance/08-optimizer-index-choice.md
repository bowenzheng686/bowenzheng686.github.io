---
layout: default
title: "MySQL 性能调优 · 优化器选索引与统计信息"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 08 优化器选索引与统计信息

## 不把 FORCE INDEX 当作默认答案

优化器比较表扫描、范围扫描、回表、排序和连接等路径的估计成本。数据倾斜或过期统计信息会造成估算偏差；先用 `EXPLAIN ANALYZE` 对照实际行数，再检查索引基数、直方图与 `ANALYZE TABLE`。直方图主要补充非索引列值分布，不是所有估算问题的万能修复。

```sql
SHOW INDEX FROM employees;
EXPLAIN ANALYZE SELECT * FROM employees WHERE name > 'zzz';
-- 仅在可控环境验证统计信息刷新效果
ANALYZE TABLE employees;
```

原资料用 `FORCE INDEX` 对比全表扫描与索引回表，核心价值是证明“强制索引不必然更快”。提示可用于诊断或极少数稳定场景，但会与数据分布、版本升级和新索引相互影响；上线前应做回归，并准备移除提示。MySQL 8.0 的不可见索引可用于评估删除索引的影响，但要先确认查询是否依赖它。[官方参考：不可见索引](https://dev.mysql.com/doc/refman/8.0/en/invisible-indexes.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=d2e8a0ae8c9dc2a45c799b771a5899f6&sub=C1831C9ABBE84A29829DE1891B06EF5A)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/07-order-group.html' | relative_url }}">← 上一篇：排序与分组的优化边界</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/09-pagination-covering.html' | relative_url }}">下一篇：深度分页与覆盖扫描 →</a>
</nav>
