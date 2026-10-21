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

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/16-mvcc-consistent-read.html' | relative_url }}">← 上一篇：MVCC、undo 与一致性读</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/18-pages-buffer-pool.html' | relative_url }}">下一篇：数据页、Buffer Pool 与读写路径 →</a>
</nav>
