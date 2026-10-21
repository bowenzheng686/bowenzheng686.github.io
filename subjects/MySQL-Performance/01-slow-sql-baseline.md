---
layout: default
title: "MySQL 性能调优 · 慢 SQL 的定位与测试基线"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 01 慢 SQL 的定位与测试基线

## 从症状到可验证的问题

调优不是先建索引或修改参数。先记录业务目标：接口的 p95/p99 延迟、吞吐、错误率、涉及的 SQL、返回行数、数据量和数据分布。把“偶发慢”区分为锁等待、磁盘 I/O、网络传输、连接池排队与 SQL 执行慢；慢查询日志只覆盖达到阈值的已执行语句，不等于端到端耗时。

```sql
SELECT VERSION();
SHOW VARIABLES LIKE 'slow_query_log%';
SHOW VARIABLES LIKE 'long_query_time';
SHOW GLOBAL STATUS LIKE 'Threads_running';
```

在可控环境用与生产相近的数据量、索引、统计信息和参数复现，再按 SQL digest 聚合调用次数、总耗时与最大耗时。比较同一查询的冷/热缓存结果，固定过滤条件和返回列；单次客户端计时不作为结论。高流量系统启用或下调慢日志阈值前要评估日志量、I/O 与敏感字段。

后续索引实验使用 `employees(id, name, age, position, hire_time)` 和复合索引 `(name, age, position)`；需要复现时先建表，再只在测试库造数：

```sql
CREATE TABLE employees (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(24) NOT NULL,
  age INT NOT NULL,
  position VARCHAR(20) NOT NULL,
  hire_time DATETIME NOT NULL,
  KEY idx_name_age_position (name, age, position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

下一篇先读执行计划，再决定是否需要 SQL 或索引变更。[官方参考：慢查询日志](https://dev.mysql.com/doc/refman/8.0/en/slow-query-log.html)。

## 建立可对比的性能基线

先固定“慢”的定义：同一接口的请求量、成功率、p50/p95/p99、返回行数及服务端 SQL 时间应分别记录。客户端等待时间还包含连接池排队、网络传输、对象反序列化等环节；如果只看到 SQL 耗时下降，却没有看到接口尾延迟改善，就需要继续拆分链路。一次优化至少要留下变更前后相同时间窗口、相似流量与相同结果集的对照。

慢查询日志适合捕获超过阈值的语句；Performance Schema 的 digest 汇总更适合寻找“单次不算慢、调用次数极高”的 SQL。下面的计时列以皮秒为单位，换算成秒后再比较：

~~~sql
SELECT SCHEMA_NAME, DIGEST_TEXT, COUNT_STAR,
       ROUND(SUM_TIMER_WAIT / 1000000000000, 3) AS total_seconds,
       ROUND(AVG_TIMER_WAIT / 1000000000000, 6) AS avg_seconds,
       SUM_ROWS_EXAMINED, SUM_ROWS_SENT
FROM performance_schema.events_statements_summary_by_digest
WHERE SCHEMA_NAME = DATABASE()
ORDER BY SUM_TIMER_WAIT DESC
LIMIT 20;
~~~

`SUM_ROWS_EXAMINED / SUM_ROWS_SENT` 可提示扫描放大，但返回零行时不能直接做除法；高频写入和排序语句也需要结合自己的指标分析。digest 把不同常量归为相似语句，适合排序优先级，却可能掩盖数据倾斜：同一模板传入“热门值”和“冷门值”时，最优访问路径与耗时可能完全不同。选样时保留参数分布，而不是仅用一条碰巧很快的语句。

## 可复现实验的四个控制量

1. **数据规模与分布**：记录总行数、目标谓词的命中比例、是否有大量重复值以及最近是否批量写入。十行测试表与千万行生产表的计划不能直接类比。
2. **表结构与版本**：保存 `SHOW CREATE TABLE`、`SHOW INDEX`、`SELECT VERSION()` 和隔离级别；尤其要核对索引列序、字符集与排序规则。
3. **缓存与并发**：分别记录热缓存和冷缓存的结果，并在接近实际的并发下复测。单次客户端时间容易被磁盘预读、Buffer Pool 命中及网络抖动影响。
4. **语义与资源**：优化前后比较结果集、排序稳定性、事务边界、锁等待、CPU/I/O 与写放大；只提升一条 SELECT 但使更新明显变慢，不算完整验收。

实验记录建议包含假设、原 SQL、候选改写、计划、三次以上稳定期测量、业务指标及回滚条件。`EXPLAIN` 是诊断入口，下一章再逐字段解释它提供和未提供的信息。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/02-explain-fields.html' | relative_url }}">下一篇：EXPLAIN 字段与访问路径 →</a>
</nav>
