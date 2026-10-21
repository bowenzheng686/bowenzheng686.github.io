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

## 一个从定位到验收的闭环

假设员工检索接口按姓名前缀过滤，按 `name, id` 稳定排序，返回 20 行；业务约束是结果不能漏行、不能换序，写入吞吐不能明显回退。先记录表行数、前缀选择性、当前索引、SQL digest 的调用频率及接口尾延迟。若慢点集中在扫描和回表，就提出两个相互独立的候选：收窄投影列，或新增更合适的索引。一次实验只改一个变量，避免无法归因。

~~~sql
SHOW CREATE TABLE employees;
SHOW INDEX FROM employees;

EXPLAIN ANALYZE
SELECT id, name, age, position
FROM employees
WHERE name LIKE 'Li%'
ORDER BY name, id
LIMIT 20;
~~~

如果查询必须返回 `hire_time`，现有 `(name, age, position)` 索引未必覆盖；新增索引是否值得，要把写入维护、索引大小和 Buffer Pool 压力算进去。若排序列包含主键，InnoDB 二级索引条目通常附带主键，但具体能否避免额外排序仍以目标版本计划为准。`EXPLAIN ANALYZE` 关注实际扫描与循环次数，接口监控关注连接等待及网络时间；两个视角要能相互解释。

## 结果一致性比“跑得快”优先

深度分页案例中，`LIMIT 90000,5` 与 `id > 90000 LIMIT 5` 只有在非常严格的数据连续性和排序条件下才可能对应；主键删除、有过滤条件或并发插入都会改变结果。若产品允许“下一页”而不是任意页码，可改用最后一个 `(name,id)` 作为游标，保证排序确定性；这属于接口契约变更，不能静默替换原分页语义。

事务和锁同样可能主导耗时。如果 `EXPLAIN ANALYZE` 在隔离测试库很快，而线上 p99 很高，应转向锁等待链、长事务、连接池与存储 I/O，不能继续给同一 SELECT 盲目加索引。一次完整记录应至少包含：

| 阶段 | 记录内容 | 通过条件 |
| --- | --- | --- |
| 基线 | SQL、参数分布、表大小、索引、p95/p99、扫描/返回行数 | 可复现且结果集已保存 |
| 单变量实验 | 新 SQL 或索引、计划、冷热缓存及并发测量 | 结果和顺序一致 |
| 灰度 | 小流量业务指标、写入成本、锁等待与错误率 | 达到预设收益且无新故障 |
| 回滚 | 原 SQL、原索引/参数、切换步骤 | 可在约定时间恢复 |

索引回滚还要考虑建删索引的 DDL 时间、复制延迟及线上负载，不能把 `DROP INDEX` 当成瞬时操作。验收结束保留前后两组证据，并在不同流量周期复核，避免把一次缓存命中或低峰时段误判为稳定收益。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/24-mysql-8-features.html' | relative_url }}">← 上一篇：MySQL 8.0 中与调优相关的能力</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
</nav>
