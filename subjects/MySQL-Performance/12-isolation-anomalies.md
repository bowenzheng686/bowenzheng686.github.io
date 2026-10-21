---
layout: default
title: "MySQL 性能调优 · 隔离级别与并发异常"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 12 隔离级别与并发异常

## 将读现象与锁定读分开

常见并发异常包括脏读、不可重复读、幻读和丢失更新。MySQL/InnoDB 支持 `READ UNCOMMITTED`、`READ COMMITTED`（RC）、`REPEATABLE READ`（RR）及 `SERIALIZABLE`；默认隔离级别通常是 RR，但应用要以当前实例配置为准。RC 的一致性读通常每条语句取新快照，RR 通常在事务中首次一致性读建立快照。`SELECT ... FOR UPDATE` 是当前读/锁定读，不能拿它的结果与普通快照读混为一谈。

```sql
SELECT @@transaction_isolation;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;
COMMIT;
```

隔离级别不是“越高越好”：要结合并发量、锁冲突、复制设置和业务不变量选择。所谓“RR 完全杜绝一切幻读”也不严谨，特别是在同一事务混用快照读与当前读时，观察结果与加锁行为会不同。丢失更新应通过原子更新、条件更新或锁定读设计避免。[官方参考：InnoDB 隔离级别](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)。



## 并发异常与四种隔离级别实验

### 并发事务处理带来的问题

丢失更新与脏写是不同问题：前者可能由读改写竞争造成，后者是覆盖其他事务尚未提交的写入。InnoDB 写锁通常阻止同一行的脏写。

两个事务读取同一旧值后分别计算并覆盖，可能造成丢失更新；可用原子更新、条件更新或锁定读防护。

脏读（Dirty Reads）

事务A读取到了事务B已经修改但尚未提交的数据

不可重读（Non-Repeatable Reads）

事务A内部的相同查询语句在不同时刻读出的结果不一致

幻读（Phantom Reads）

幻读指同一事务内相同谓词查询前后看到的行集合发生变化；普通快照读和锁定读在 InnoDB RR 下需分开讨论。

### 事务隔离级别

“脏读”、“不可重复读”和“幻读”,其实都是数据库读一致性问题,必须由数据库提供一定的事务隔离机制来解决。

| 隔离级别 | 脏读 | 不可重复读 | 幻读与锁定读 |
| --- | --- | --- | --- |
| READ UNCOMMITTED | 可能 | 可能 | 需结合具体语句 |
| READ COMMITTED | 避免 | 可能 | 语句级快照 |
| REPEATABLE READ | 避免 | 一致性读通常避免 | 快照读与当前读不同 |
| SERIALIZABLE | 避免 | 避免 | 通过更强锁定约束并发 |

隔离级别越强通常约束越多，但代价不是统一的“串行化”；应结合快照读、锁冲突、正确性与吞吐实测选择。

同时,不同的应用对读一致性和事务隔离程度的要求也是不同的,比如许多应用对“不可重复读"和“幻读”并不敏感,可能更关心数据并发访问的能力。

查看当前隔离级别：SHOW VARIABLES LIKE 'transaction_isolation';

设置当前会话隔离级别：SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;

InnoDB 默认隔离级别通常为 REPEATABLE READ；应用框架可能覆盖，生产判断以会话实际值为准。

### 事务隔离级别案例分析

```sql
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `balance` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
INSERT INTO `test`.`account` (`name`, `balance`) VALUES ('lilei', '450');
INSERT INTO `test`.`account` (`name`, `balance`) VALUES ('hanmei', '16000');
INSERT INTO `test`.`account` (`name`, `balance`) VALUES ('lucy', '2400');
```

读未提交：

（1）打开一个客户端A，并设置当前事务模式为read uncommitted（未提交读），查询表account的初始值：

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
```

![隔离级别与并发异常配图](assets/transaction-001-63d7656acbda.webp)

（2）在客户端A的事务提交之前，打开另一个客户端B，更新表account：

![隔离级别与并发异常配图](assets/transaction-002-8378b8002460.webp)

（3）这时，虽然客户端B的事务还没提交，但是客户端A就可以查询到B已经更新的数据：

![隔离级别与并发异常配图](assets/transaction-003-cb22fa5ead61.webp)

（4）一旦客户端B的事务因为某种原因回滚，所有的操作都将会被撤销，那客户端A查询到的数据其实就是脏数据：

![隔离级别与并发异常配图](assets/transaction-004-b2e0d1d8afee.webp)

在 READ UNCOMMITTED 下，普通读取可见未提交数据；UPDATE 是当前读并受行锁约束，不能用此前的脏读快照直接推断更新计算结果。

![隔离级别与并发异常配图](assets/transaction-005-5802e3a8982b.webp)

3、读已提交

（1）会话 A 设置 READ COMMITTED，读取 account 初始值：

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

![隔离级别与并发异常配图](assets/transaction-006-0af119f00c23.webp)

（2）在客户端A的事务提交之前，打开另一个客户端B，更新表account：

![隔离级别与并发异常配图](assets/transaction-007-7ab32401fcf0.webp)

（3）这时，客户端B的事务还没提交，客户端A不能查询到B已经更新的数据，解决了脏读问题：

![隔离级别与并发异常配图](assets/transaction-008-d498331607aa.webp)

（4）客户端B的事务提交

![隔离级别与并发异常配图](assets/transaction-009-231bd446630e.webp)

（5）客户端A执行与上一步相同的查询，结果 与上一步不一致，即产生了不可重复读的问题

![隔离级别与并发异常配图](assets/transaction-010-286cd37d4f8f.webp)

4、可重复读

REPEATABLE READ 的普通一致性读通常在事务内第一次一致性读取时建立 Read View，并复用该视图；不是事务刚开启就立即复制全库快照。锁定读与 UPDATE 使用当前读。

（1）打开一个客户端A，并设置当前事务模式为repeatable read，查询表account的所有记录

```sql
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

![隔离级别与并发异常配图](assets/transaction-011-6e498dd182b3.webp)

（2）在客户端A的事务提交之前，打开另一个客户端B，更新表account并提交

![隔离级别与并发异常配图](assets/transaction-012-c6d6fdb2ddb8.webp)

（3）在客户端A查询表account的所有记录，与步骤（1）查询结果一致，没有出现不可重复读的问题

![隔离级别与并发异常配图](assets/transaction-013-a0930e78ff80.webp)

（4）会话 A 执行 UPDATE 时读取并锁定当前版本，不沿用之前普通 SELECT 的快照值；随后再做一致性读时要结合自身写入和可见性规则分析。

![隔离级别与并发异常配图](assets/transaction-014-422ca5f3913e.webp)

（5）重新打开客户端B，插入一条新数据后提交

![隔离级别与并发异常配图](assets/transaction-015-4b6d1a89d8c1.webp)

（6）普通一致性读仍基于原 Read View，因此此处看不到会话 B 的新增行；这不代表 RR 下所有读法都绝对看不到新行。

![隔离级别与并发异常配图](assets/transaction-016-ab7a77aa0ce7.webp)

（7)验证幻读

会话 A 对 B 插入的 id 执行 UPDATE 属于当前读；更新后本事务的写入对自己可见，因此后续 SELECT 可能看到该行。

![隔离级别与并发异常配图](assets/transaction-017-7105fee01a5c.webp)

5、串行化

（1）打开一个客户端A，并设置当前事务模式为serializable，查询表account的初始值：

```sql
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

![隔离级别与并发异常配图](assets/transaction-018-6995cfc42913.webp)

SERIALIZABLE 下的普通 SELECT 在显式事务中可能转为加锁读，从而阻塞冲突写入；具体锁范围与查询谓词、索引和执行计划有关。

范围读取可能阻塞范围内的插入，但应通过实际锁信息确认记录锁、间隙锁和 next-key 锁，不应假定所有语句锁定同一范围。

这种隔离级别并发性极低，开发中很少会用。

![隔离级别与并发异常配图](assets/transaction-019-06e8b0fe2378.webp)



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/11-transactions-acid.html' | relative_url }}">← 上一篇：事务、ACID 与提交边界</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/13-transaction-optimization.html' | relative_url }}">下一篇：事务边界与长事务优化 →</a>
</nav>
