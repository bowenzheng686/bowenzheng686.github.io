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

`type` 显示访问方法，例如 `const`、`ref`、`range`、`index`、`ALL`；它不是跨所有 SQL 通用的性能分数。扫描少量行的 `ALL` 可能比大量回表的 `range` 更快。看计划时把表大小、预估扫描行数、过滤比例、回表、排序和实际耗时一起考虑。第 04 章的范围扫描案例展示了优化器如何在候选复合索引与全表扫描之间选择。

下一篇用实测核对估算。[官方参考：EXPLAIN](https://dev.mysql.com/doc/refman/8.0/en/explain.html)。

## 逐列阅读传统 EXPLAIN

| 列 | 应读出的信息 | 容易误判的地方 |
| --- | --- | --- |
| `id`、`select_type` | 查询块和子查询类型 | `id` 不是步骤耗时排序 |
| `table`、`partitions` | 当前访问对象与分区 | 派生表可能显示为临时编号 |
| `type` | `const`、`ref`、`range`、`index`、`ALL` 等访问方法 | 访问方法不是单独的性能评分 |
| `possible_keys` | 优化器认为可能使用的索引 | 非空不表示最后会选它 |
| `key`、`key_len` | 选用索引与计划中的最大键长 | `key_len` 不是“实际逐行使用的字节数”，也不直接代表过滤效果 |
| `ref` | 与索引列比较的常量或列 | 要结合 JOIN 顺序理解 |
| `rows`、`filtered` | 估计扫描行数与条件通过比例 | 不是实际执行计数；数据倾斜时偏差可能很大 |
| `Extra` | 覆盖、ICP、排序、临时表等补充信息 | 一个标签不能替代总成本与实测 |

同一 SQL 若涉及多张表，需要按查询块和连接顺序逐行阅读：先确认哪张表提供候选行，再看被探测侧是否有可用关联索引、每次探测预计取回多少行，最后考虑排序与结果输出。`rows` 的含义是每次访问的估算量，不能把各行的 `rows` 简单相加当成最终读取行数。

## 四个常见 Extra 标签

- `Using where`：有谓词在取行过程中被检查；它不等于没有用索引。
- `Using index`：所需列由索引覆盖，通常减少回表；它不是“使用索引完成 ORDER BY”的专用提示。
- `Using index condition`：启用了索引条件下推（ICP），可在二级索引条目上先过滤部分条件；剩余条件仍可能需要回表检查。
- `Using filesort` / `Using temporary`：分别表示额外排序或内部临时表路径；是否落盘、处理多少行及是否成为瓶颈，要看实际执行和系统指标。

例如索引为 `(name, age, position)`，查询仅返回这三列时可能覆盖；改成 `SELECT *` 后，`hire_time` 等未覆盖列会引入回表。两个查询即使 WHERE 相同，最优计划也可能不同。下一章用 `EXPLAIN ANALYZE` 和统计信息验证这种差异，而不是只比较 `type` 的字面顺序。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/01-slow-sql-baseline.html' | relative_url }}">← 上一篇：慢 SQL 的定位与测试基线</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/03-plan-validation.html' | relative_url }}">下一篇：执行计划验证与优化器判断 →</a>
</nav>
