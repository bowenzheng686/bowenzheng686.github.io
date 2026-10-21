---
layout: default
title: "MySQL 性能调优 · 事务、ACID 与提交边界"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 11 事务、ACID 与提交边界

## 原子性不等于“写一条反向 SQL”

事务把一组操作定义成提交或回滚的工作单元。ACID 的实现机制需要区分：undo 记录用于回滚与一致性读，并非简单保存“完全相反的一句 SQL”；redo 支撑崩溃恢复，耐久性还受刷盘配置与硬件故障模型影响；隔离由锁与 MVCC 等共同实现；一致性还依赖约束和应用业务规则。

下面用余额表说明事务边界。演示库先执行：

```sql
CREATE TABLE accounts (
  id BIGINT PRIMARY KEY,
  balance DECIMAL(12,2) NOT NULL
) ENGINE=InnoDB;
INSERT INTO accounts VALUES (1, 1000.00), (2, 1000.00);

START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- 任一步失败，应由应用显式 ROLLBACK，并处理重试与幂等。
```

`autocommit=1` 下每条独立 DML 默认各自成为事务；显式事务需明确异常路径，不要在持锁期间做外部 RPC 或等待人工输入。DDL 的提交行为与普通 DML 不同，不应混入这个转账事务。下一篇讨论并发下“看见什么”。[官方参考：事务](https://dev.mysql.com/doc/refman/8.0/en/commit.html)。
示例仅用于观察原子提交；真实转账还需余额不足检查、请求幂等和失败重试策略。



## 事务语义与 ACID

### 概述

我们的数据库一般都会并发执行多个事务，多个事务可能会并发的对相同的一批数据进行增删改查操作，可能就会导致我们说的脏写、脏读、不可重复读、幻读这些问题。

这些现象属于多事务并发下的一致性问题。隔离级别、锁、MVCC 与日志分别约束可见性、写入冲突和持久性；下一章先比较四种隔离级别，再进入锁与版本链。

### 事务及其ACID属性

事务是一组操作要么全部成功，要么全部失败，目的是为了保证数据最终的一致性。

事务具有以下4个属性,通常简称为事务的ACID属性。

- 原子性：事务作为工作单元提交或回滚。undo 支持回滚，崩溃恢复还依赖 redo 等机制。

- 一致性：事务前后满足约束与业务不变量；数据库机制不能代替正确的应用逻辑。

- 隔离性：锁、MVCC 与隔离级别共同控制并发事务之间的可见性及冲突。

- 持久性：已提交变更在约定故障模型下可恢复，取决于 redo、刷盘配置及存储系统。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/10-joins-subqueries-count.html' | relative_url }}">← 上一篇：关联、子查询与计数</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/12-isolation-anomalies.html' | relative_url }}">下一篇：隔离级别与并发异常 →</a>
</nav>
