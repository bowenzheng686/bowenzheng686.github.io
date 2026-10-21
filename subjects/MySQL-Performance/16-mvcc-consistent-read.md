---
layout: default
title: "MySQL 性能调优 · MVCC、undo 与一致性读"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 16 MVCC、undo 与一致性读

## 快照如何看到旧版本

InnoDB 记录包含事务标识及指向旧版本的回滚信息；更新形成可供回滚和一致性读追溯的 undo 版本链。Read View 决定某个版本对当前一致性读是否可见。RC 通常每次一致性读生成新快照；RR 通常在事务中首次一致性读建立快照并复用。自己的写入仍可被自己看到，因此“事务内所有 SELECT 永远看到完全相同的数据”也不准确。

```sql
-- 会话 A
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;
-- 会话 B 更新并提交后，A 再做普通 SELECT 与 FOR UPDATE，比较结果。
SELECT balance FROM accounts WHERE id = 1;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
COMMIT;
```

普通一致性读通常不等待记录写锁，锁定读需要读当前可加锁的记录；MVCC 并不是“所有读取都无锁”。长期持有快照会拖慢旧版本清理，因此与长事务治理直接相关。[官方参考：一致性读](https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/15-gap-next-key-locks.html' | relative_url }}">← 上一篇：记录锁、间隙锁与 next-key 锁</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/17-lock-waits-deadlocks.html' | relative_url }}">下一篇：锁等待、死锁与排障 →</a>
</nav>
