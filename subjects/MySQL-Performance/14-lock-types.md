---
layout: default
title: "MySQL 性能调优 · InnoDB 锁的类型与兼容性"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 14 InnoDB 锁的类型与兼容性

## 从行、表到元数据

共享锁（S）允许兼容的共享访问，排他锁（X）与相同记录上的冲突锁互斥。InnoDB 行锁落在索引记录上；表级意向锁（IS/IX）表明事务将持有相应行锁，便于表锁冲突判断，不能简单理解为“给整张表加排他锁”。普通一致性读通常不设置行锁；锁定读与 DML 则需按隔离级别和访问路径分析。

```sql
START TRANSACTION;
SELECT * FROM employees WHERE id = 1 FOR SHARE;
-- 另一事务对同一行请求不兼容的锁可能等待。
COMMIT;
```

MySQL 8.0 推荐 `FOR SHARE`（旧写法 `LOCK IN SHARE MODE` 仍用于兼容）。元数据锁（MDL）保护表结构与正在使用它的语句，长事务可能阻塞 DDL；它与行锁、显式 `LOCK TABLES` 不是一回事。讨论“乐观/悲观、表/页/行、读/写”分类时，要区分应用层版本号乐观并发控制与 InnoDB 实际锁类型。[官方参考：InnoDB 锁](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html)。

## 先分清锁的作用域

InnoDB 的记录锁作用于**索引记录**。即使 SQL 写的是普通列谓词，实际锁范围也由优化器采用的索引和扫描路径决定；缺少合适索引时，大量记录可能被扫描并锁定，但这不等于自动变成一个传统意义的表 X 锁。表级意向锁 IS、IX 是事务将取得或已持有行级 S、X 锁的声明，使表锁兼容性检查无需遍历所有行锁。

| 已持有 / 新请求 | S | X | IS | IX |
| --- | --- | --- | --- | --- |
| S | 兼容 | 冲突 | 兼容 | 冲突 |
| X | 冲突 | 冲突 | 冲突 | 冲突 |
| IS | 兼容 | 冲突 | 兼容 | 兼容 |
| IX | 冲突 | 冲突 | 兼容 | 兼容 |

上表是**表级意向锁与表锁**的兼容性关系；具体记录上的 S/X 还要分别判断。普通 `SELECT` 在常见 RC/RR 一致性读下通常通过 MVCC 读取可见版本，不取得记录 S 锁；`FOR SHARE`、`FOR UPDATE` 和更新、删除则可能取得记录锁及间隙相关锁。自动提交模式下单条锁定语句的锁持有边界，与显式事务不同。

## 锁定读与 DML 的边界

~~~sql
-- 会话 A
START TRANSACTION;
SELECT id, name FROM employees WHERE id = 1 FOR UPDATE;
-- 保持事务未提交，观察会话 B 的锁等待。

-- 会话 B
START TRANSACTION;
UPDATE employees SET position = 'lead' WHERE id = 1;
-- 此处可能等待 A 释放同一记录上的冲突锁。
~~~

实验结束要在两个会话分别 `ROLLBACK` 或 `COMMIT`，并记录隔离级别和索引。若把谓词从主键等值改为非唯一索引范围，锁集合可能扩大；如果只看 SQL 文本而不看 `data_locks`，容易误以为 InnoDB “锁的是 WHERE 条件”。

元数据锁保护正在使用的表结构。例如事务中读取一张表后长时间不提交，另一会话的 `ALTER TABLE` 可能等待 MDL；随后到来的新查询还可能在 DDL 后排队，形成看似突然的雪崩。排查时先找最早未提交事务，再看 DDL 与后续等待链，不要把所有阻塞归咎于行锁。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/13-transaction-optimization.html' | relative_url }}">← 上一篇：事务边界与长事务优化</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/15-gap-next-key-locks.html' | relative_url }}">下一篇：记录锁、间隙锁与 next-key 锁 →</a>
</nav>
