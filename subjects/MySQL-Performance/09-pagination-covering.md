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

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/08-optimizer-index-choice.html' | relative_url }}">← 上一篇：优化器选索引与统计信息</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/10-joins-subqueries-count.html' | relative_url }}">下一篇：关联、子查询与计数 →</a>
</nav>
