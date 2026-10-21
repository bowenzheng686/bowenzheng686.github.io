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

本专题的索引实验沿用原资料的 `employees(id, name, age, position, hire_time)` 和复合索引 `(name, age, position)`；需要复现时先建表，再只在测试库造数：

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

---

原始资料：[有道云笔记](https://note.youdao.com/s/YoQZCEjl)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/02-explain-fields.html' | relative_url }}">下一篇：EXPLAIN 字段与访问路径 →</a>
</nav>
