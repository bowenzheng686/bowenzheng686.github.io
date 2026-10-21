---
layout: default
title: "MySQL 性能调优 · 联合索引设计与最左前缀"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 05 联合索引设计与最左前缀

## 用查询形态决定列顺序

联合索引 `(name, age, position)` 可支持从 `name` 开始的查找；等值列后接范围列时，后续列通常难以继续缩小连续扫描区间，但仍可能用于覆盖或索引条件下推。排序能否利用索引要单独核对计划。不能把“范围后面的列完全没有作用”写成绝对规则，也不能为了凑最左前缀而注入无意义的 `IN` 条件。

```sql
EXPLAIN SELECT id FROM employees
WHERE name = 'LiLei' AND age = 22;
EXPLAIN SELECT id FROM employees
WHERE name LIKE 'Li%' AND age = 22 AND position = 'manager';
```

优先盘点高频 SQL，再评估等值过滤、范围、`ORDER BY`、返回列与更新成本。原资料的社交搜索案例可归纳为：`(province, city, sex, age)` 与 `(sex, score)` 服务不同查询路径；是否保留两个索引要看查询比例和写入代价。为“最近七天活跃”增设派生布尔列会引入持续维护和时间边界问题，不能只凭索引命中率决定。对于长字符串前缀索引，还要验证区分度，且完整排序通常不能仅靠截断前缀完成。[官方参考：多列索引](https://dev.mysql.com/doc/refman/8.0/en/multiple-column-indexes.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=d2e8a0ae8c9dc2a45c799b771a5899f6&sub=C1831C9ABBE84A29829DE1891B06EF5A)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/04-index-structure-cost.html' | relative_url }}">← 上一篇：索引结构与访问成本</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/06-predicate-index-usage.html' | relative_url }}">下一篇：过滤谓词与索引使用 →</a>
</nav>
