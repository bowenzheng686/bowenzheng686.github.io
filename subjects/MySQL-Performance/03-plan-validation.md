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

比较 `name > 'a'` 与 `name > 'zzz'`：前者可能命中大部分表，后者可能很少，回表代价使最优路径不同。不能把某个执行计划推广为“范围条件必然不用索引”。若估算和实测差异大，先检查统计信息、数据倾斜与参数，再考虑 `ANALYZE TABLE`，并记录它对线上负载的影响。[官方参考：优化器统计信息](https://dev.mysql.com/doc/refman/8.0/en/optimizer-statistics.html)。

## 估算行数与实际行数

传统 `EXPLAIN` 主要给出优化器在执行前的估计。`EXPLAIN ANALYZE` 会真正执行查询，输出迭代器的实际耗时、返回行数和循环次数。读这些数据时应先辨认迭代器是“每次循环”还是“总计”：嵌套循环右侧若执行了许多次，即使单次只取一行，总访问量也可能很大。实际执行环境中的锁等待、缓存命中与并发会影响计时，所以单次结果只用于定位，不应作为上线收益承诺。

以下两个谓词共享 SQL 形状，却可能有完全不同的选择性。先确认 `name` 的值分布，再对比估计、实测与返回行数：

~~~sql
EXPLAIN ANALYZE
SELECT id, name, age, position
FROM employees WHERE name > 'a';

EXPLAIN ANALYZE
SELECT id, name, age, position
FROM employees WHERE name > 'zzz';

SHOW INDEX FROM employees;
~~~

如果估计与实际差异很大，排查顺序可以是：统计信息是否陈旧；谓词是否有相关列或严重数据倾斜；列类型、字符集和隐式转换是否改变了比较；是否存在 LIMIT、排序和回表成本；当前版本是否支持相应直方图或优化器特性。`ANALYZE TABLE employees` 可以刷新索引统计信息，但可能带来额外 I/O 或计划改变，应先在测试环境复现，再安排可观察的变更窗口。

## 从候选路径到最终决策

优化器不只比较“索引还是全表扫描”。它还估计索引范围内要读取的条目数、回表次数、过滤后的行数、是否需要额外排序，以及多个表的连接顺序。索引扫描返回大比例记录时，随机回表可能比顺序扫描昂贵；改成覆盖投影后，回表消失，最优路径可能随之改变。`FORCE INDEX` 可作为诊断对照，但若数据分布变化，强制路径可能变差，不宜只因为一次截图更快就长期固定。

`optimizer_trace` 的 `range_analysis` 可查看候选范围索引和成本估算；`considered_execution_plans` 可看最终访问路径。它的内容随版本变化，分析时抓住“候选—估计行数—成本—选择理由”四项，不把某个 JSON 字段顺序当成稳定接口。完成分析后关闭 trace，并保存目标版本、表结构、统计信息及实验 SQL，这样同一结论才可复查。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/02-explain-fields.html' | relative_url }}">← 上一篇：EXPLAIN 字段与访问路径</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/04-index-structure-cost.html' | relative_url }}">下一篇：索引结构与访问成本 →</a>
</nav>
