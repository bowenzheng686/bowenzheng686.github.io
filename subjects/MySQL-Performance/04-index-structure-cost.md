---
layout: default
title: "MySQL 性能调优 · 索引结构与访问成本"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 04 索引结构与访问成本

## 从 B+ 树到回表

InnoDB 聚簇索引的叶页承载行记录；二级索引的叶页记录索引列及主键值。用二级索引检索未覆盖的列，通常还要按主键回到聚簇索引，这就是回表。索引覆盖所需列时可以避免相应回表，但更宽的索引增加存储、写入、页分裂和缓存压力。

```sql
-- 同一过滤条件，比较是否需要取回整行
EXPLAIN SELECT * FROM employees WHERE name > 'LiLei';
EXPLAIN SELECT name, age, position FROM employees WHERE name > 'LiLei';
```

原资料的覆盖索引案例值得保留，结论应改为：是否采用索引取决于成本，投影列变化可能改变计划；不保证覆盖索引在每个数据集上都更快。低基数字段也不是“一律不建索引”：它可与其他条件或排序组合，或成为高频查询的一部分。设计时以真实查询、选择性、写入比例和维护成本共同决定。[官方参考：InnoDB 索引类型](https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html)。

原资料对照：强制索引时可能出现 `Using index condition`；仅取索引覆盖的列时出现 `Using index`。两图是该实验的计划，不是新版实例的固定结果。

![原资料强制索引的执行计划](assets/index-1-002-e746417dbdcb.webp)

![原资料覆盖索引的执行计划](assets/index-1-003-a4d707431671.webp)

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=d2e8a0ae8c9dc2a45c799b771a5899f6&sub=C1831C9ABBE84A29829DE1891B06EF5A)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/03-plan-validation.html' | relative_url }}">← 上一篇：执行计划验证与优化器判断</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/05-composite-index.html' | relative_url }}">下一篇：联合索引设计与最左前缀 →</a>
</nav>
