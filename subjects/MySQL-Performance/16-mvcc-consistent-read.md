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
SELECT balance FROM account WHERE id = 1;
-- 会话 B 更新并提交后，A 再做普通 SELECT 与 FOR UPDATE，比较结果。
SELECT balance FROM account WHERE id = 1;
SELECT balance FROM account WHERE id = 1 FOR UPDATE;
COMMIT;
```

普通一致性读通常不等待记录写锁，锁定读需要读当前可加锁的记录；MVCC 并不是“所有读取都无锁”。长期持有快照会拖慢旧版本清理，因此与长事务治理直接相关。[官方参考：一致性读](https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html)。

## 版本链、Read View 与可见性

InnoDB 聚簇索引记录有用于事务可见性判断的隐藏字段，包括最近修改该行的事务标识和指向 undo 版本的回滚指针。一次更新会形成新版本，旧版本信息通过 undo 记录供回滚或一致性读追溯。Read View 记录创建时活跃事务的范围和标识；读取某个版本时，InnoDB 判断该版本的创建事务是否已在快照前提交、是否属于当前事务，以及是否仍活跃。若当前版本不可见，就沿版本链查找更旧的可见版本。

这解释了“普通 SELECT 不必等待正在修改的行”：它可以读取符合快照的旧版本。但如果访问路径需要锁定当前行，例如 `SELECT ... FOR UPDATE`、`UPDATE`、`DELETE`，就要按当前版本及锁兼容性执行，可能等待或发生死锁。MVCC 提供的是特定读法下的多版本可见性，不是对所有 SQL 的无锁承诺。

## RC 与 RR 的快照时间

- **READ COMMITTED**：普通一致性读通常每条语句建立新的 Read View；事务内两次相同查询可能看到其他事务期间提交的变化。
- **REPEATABLE READ**：普通一致性读通常在本事务第一次一致性读取时建立 Read View，并在后续一致性读中复用。`START TRANSACTION` 本身通常不等于立刻建立快照；`START TRANSACTION WITH CONSISTENT SNAPSHOT` 有专门语义。
- **本事务写入**：自己的更新对自己可见；把“RR 内所有 SELECT 返回完全相同的值”当作固定规则，会忽略本事务写入和当前读。

例如会话 A 在 RR 下第一次普通 `SELECT` 读到余额 400，会话 B 更新为 350 并提交后，A 的普通 `SELECT` 仍可能读到 400；A 再用 `FOR UPDATE` 读取则面向当前可锁定版本，可能读到 350。若 B 尚未提交，锁定读可能等待。分析现象时必须同时标注会话、事务边界、读法和提交顺序。

旧 Read View 长时间存活会使仍被引用的 undo 版本难以及时清理，增加历史链长度和存储压力。定位长事务时可结合 `information_schema.innodb_trx`、会话状态和业务调用链；不要只调大 undo 空间，而忽略持有快照的根因。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/15-gap-next-key-locks.html' | relative_url }}">← 上一篇：记录锁、间隙锁与 next-key 锁</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/17-lock-waits-deadlocks.html' | relative_url }}">下一篇：锁等待、死锁与排障 →</a>
</nav>
