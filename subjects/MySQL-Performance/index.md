---
layout: default
title: MySQL 性能调优
subject_page: true
pdf_notes: true
---

# MySQL 性能调优

本专题共 25 章，按“定位问题 → 读执行计划 → 索引与 SQL → 事务 → 锁/MVCC → 存储与日志 → 实例调优 → 验收”阅读。示例应结合实际 MySQL 版本、表结构与测试数据验证。

[查看配图汇总]({{ '/subjects/MySQL-Performance/source-figures.html' | relative_url }})。

## 执行计划与诊断
<ol start="1">
  <li><a href="{{ '/subjects/MySQL-Performance/01-slow-sql-baseline.html' | relative_url }}">慢 SQL 的定位与测试基线</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/02-explain-fields.html' | relative_url }}">EXPLAIN 字段与访问路径</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/03-plan-validation.html' | relative_url }}">执行计划验证与优化器判断</a></li>
</ol>

## 索引优化实战
<ol start="4">
  <li><a href="{{ '/subjects/MySQL-Performance/04-index-structure-cost.html' | relative_url }}">索引结构与访问成本</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/05-composite-index.html' | relative_url }}">联合索引设计与最左前缀</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/06-predicate-index-usage.html' | relative_url }}">过滤谓词与索引使用</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/07-order-group.html' | relative_url }}">排序与分组的优化边界</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/08-optimizer-index-choice.html' | relative_url }}">优化器选索引与统计信息</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/09-pagination-covering.html' | relative_url }}">深度分页与覆盖扫描</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/10-joins-subqueries-count.html' | relative_url }}">关联、子查询与计数</a></li>
</ol>

## 事务语义与优化
<ol start="11">
  <li><a href="{{ '/subjects/MySQL-Performance/11-transactions-acid.html' | relative_url }}">事务、ACID 与提交边界</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/12-isolation-anomalies.html' | relative_url }}">隔离级别与并发异常</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/13-transaction-optimization.html' | relative_url }}">事务边界与长事务优化</a></li>
</ol>

## 锁、死锁与 MVCC
<ol start="14">
  <li><a href="{{ '/subjects/MySQL-Performance/14-lock-types.html' | relative_url }}">InnoDB 锁的类型与兼容性</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/15-gap-next-key-locks.html' | relative_url }}">记录锁、间隙锁与 next-key 锁</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/16-mvcc-consistent-read.html' | relative_url }}">MVCC、undo 与一致性读</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/17-lock-waits-deadlocks.html' | relative_url }}">锁等待、死锁与排障</a></li>
</ol>

## InnoDB 与日志
<ol start="18">
  <li><a href="{{ '/subjects/MySQL-Performance/18-pages-buffer-pool.html' | relative_url }}">数据页、Buffer Pool 与读写路径</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/19-redo-undo.html' | relative_url }}">redo、undo 与提交耐久性</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/20-binlog-commit.html' | relative_url }}">binlog 与提交一致性</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/21-checkpoint-crash-recovery.html' | relative_url }}">checkpoint、刷盘与崩溃恢复</a></li>
</ol>

## 全局调优与 MySQL 8.0
<ol start="22">
  <li><a href="{{ '/subjects/MySQL-Performance/22-instance-observability.html' | relative_url }}">实例级观测与调优顺序</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/23-configuration-tradeoffs.html' | relative_url }}">关键配置与资源预算</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/24-mysql-8-features.html' | relative_url }}">MySQL 8.0 中与调优相关的能力</a></li>
  <li><a href="{{ '/subjects/MySQL-Performance/25-end-to-end-case.html' | relative_url }}">端到端案例、验收与回滚</a></li>
</ol>
