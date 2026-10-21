---
layout: default
title: "MySQL 性能调优 · 锁等待、死锁与排障"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 17 锁等待、死锁与排障

## 找到阻塞链再处理

锁等待是事务请求的锁尚未可用；死锁是循环等待。InnoDB 通常检测死锁并回滚其中一个事务，应用应处理相应错误并在幂等前提下有限重试。不要只提高 `innodb_lock_wait_timeout`，那会放大排队时间。先保存问题时段的 SQL、事务年龄、对象和阻塞关系。

```sql
SELECT * FROM performance_schema.data_lock_waits;
SELECT ENGINE_TRANSACTION_ID, OBJECT_SCHEMA, OBJECT_NAME,
       INDEX_NAME, LOCK_TYPE, LOCK_MODE, LOCK_STATUS
FROM performance_schema.data_locks;
SHOW ENGINE INNODB STATUS\G
```

MySQL 8.0 应优先看 Performance Schema 的 `data_locks`/`data_lock_waits`；旧 `INFORMATION_SCHEMA.INNODB_LOCKS` 教程不可原样照搬。优化路径通常是：给过滤条件合适索引、缩小更新范围、统一访问顺序、缩短事务，再回归验证等待分布和正确性。[官方参考：锁等待信息](https://dev.mysql.com/doc/refman/8.0/en/innodb-information-schema-understanding-innodb-locking.html)。

## 把等待关系还原成事务链

`data_locks` 展示锁请求与状态，`data_lock_waits` 连接“正在等待的锁”和“阻塞它的锁”。排查时先找等待事务，再回溯阻塞事务及其最近 SQL、事务开始时间和应用请求；阻塞者当前可能处于空闲状态，单看“正在执行的慢 SQL”会漏掉它。锁对象还包含 schema、表、索引及锁模式，可与查询计划核对是否因缺少索引扫描了过多记录。

~~~sql
SELECT w.REQUESTING_ENGINE_TRANSACTION_ID AS waiting_trx,
       w.BLOCKING_ENGINE_TRANSACTION_ID AS blocking_trx,
       rl.OBJECT_SCHEMA, rl.OBJECT_NAME, rl.INDEX_NAME,
       rl.LOCK_TYPE, rl.LOCK_MODE AS waiting_mode,
       bl.LOCK_MODE AS blocking_mode
FROM performance_schema.data_lock_waits AS w
JOIN performance_schema.data_locks AS rl
  ON rl.ENGINE_LOCK_ID = w.REQUESTING_ENGINE_LOCK_ID
JOIN performance_schema.data_locks AS bl
  ON bl.ENGINE_LOCK_ID = w.BLOCKING_ENGINE_LOCK_ID;
~~~

监控采样可能错过短暂等待，因此还要结合应用错误码、等待时长分布和 `SHOW ENGINE INNODB STATUS` 中最近一次死锁信息。MySQL 错误 1213 常对应死锁，错误 1205 常对应锁等待超时；处理方式不同，日志里应保留事务标识、业务幂等键与重试次数。

## 死锁示例与重试边界

假设会话 A 先更新 id=1 再更新 id=2，会话 B 先更新 id=2 再更新 id=1：两者各持有对方所需的记录锁，就形成循环等待。InnoDB 检测到死锁后通常选择一个事务回滚；应用应重新执行**整个事务**，而不是从失败 SQL 的下一句继续。重试要有限次数、带退避，并确保外部调用或消息发送不会因重试重复生效。

解决问题时优先统一访问顺序、缩短持锁时间、拆小批次，并用合适索引避免无关记录进入锁定范围。`innodb_lock_wait_timeout` 仅规定等待上限，不会消除死锁根因。改动后要同时比较 p95/p99、死锁次数、锁等待总时间和业务正确性，必要时回滚索引或事务改写。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/16-mvcc-consistent-read.html' | relative_url }}">← 上一篇：MVCC、undo 与一致性读</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/18-pages-buffer-pool.html' | relative_url }}">下一篇：数据页、Buffer Pool 与读写路径 →</a>
</nav>
