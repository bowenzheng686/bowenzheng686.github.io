---
layout: default
title: "MySQL 性能调优 · MySQL 8.0 中与调优相关的能力"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 24 MySQL 8.0 中与调优相关的能力

## 新特性只在合适场景有收益

8.0 提供 `EXPLAIN ANALYZE`、降序索引、不可见索引、直方图、窗口函数、CTE、原子 DDL 等能力；具体起始小版本和限制需按部署版本核对。窗口函数和 CTE 可提升表达能力与可读性，但未必比原查询快，仍需比较计划与中间结果。不可见索引用于评估移除风险，不能代替完整的查询回归。

```sql
SELECT VERSION();
EXPLAIN ANALYZE SELECT * FROM employees WHERE name = 'LiLei';
CREATE INDEX idx_hire_desc_id ON employees(hire_time DESC, id DESC);
ALTER TABLE employees ALTER INDEX idx_hire_desc_id INVISIBLE;
-- 验证后可改回 VISIBLE；不要在尚有依赖时直接删除。
```

旧资料中 MySQL 5.7 的 query cache 配置在 8.0 已不适用；同样，8.0.20 起无索引关联不能继续笼统解释为 Block Nested Loop。新能力的章节以官方版本说明和实验结果为准。[官方参考：MySQL 8.0 新特性](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=c0b91c9b60a787a2293a780ca5d3c151&sub=A8EEC383AEEB4D7C883228E7CAF37B17)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/23-configuration-tradeoffs.html' | relative_url }}">← 上一篇：关键配置与资源预算</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/25-end-to-end-case.html' | relative_url }}">下一篇：端到端案例、验收与回滚 →</a>
</nav>
