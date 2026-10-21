---
layout: default
title: "MySQL 性能调优 · 事务边界与长事务优化"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 13 事务边界与长事务优化

## 缩短持锁时间而不破坏业务原子性

事务优化优先识别长时间处于活动状态的事务及其等待对象。常见原因包括事务内大量逐行更新、客户端“空闲但未提交”、跨服务调用、过大批次和缺少索引导致的宽范围锁定。可将非事务性计算前移，缩小批次，在满足业务正确性的前提下统一访问顺序并及时提交。

```sql
SELECT trx_id, trx_started, trx_state, trx_query
FROM information_schema.innodb_trx
ORDER BY trx_started;
```

将更新放到事务靠后位置，有时可减少持锁时间，但不能机械执行：外键、唯一约束、并发竞争和业务依赖可能要求不同顺序。对于冲突后的重试，应设置次数上限、退避和幂等键；不要把死锁或超时吞掉当成成功。下一组进入锁机制。[官方参考：死锁处理](https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html)。



## 长事务定位与边界优化

事务问题定位

```sql
-- 查询已运行超过 1 秒的事务；结合线程与锁等待信息判断原因。
SELECT
	*
FROM
	information_schema.innodb_trx
WHERE
	TIME_TO_SEC( timediff( now( ), trx_started ) ) > 1;

-- 确认会话归属、事务影响和回滚成本后，才考虑终止对应连接：
-- KILL CONNECTION <trx_mysql_thread_id>;
```

大事务的影响

- 并发情况下，数据库连接池容易被撑爆

- 锁定太多的数据，造成大量的阻塞和锁超时

- 执行时间长，容易造成主从延迟

- 回滚所需要的时间比较长

- undo log膨胀

- 容易导致死锁

### 事务优化

- 将查询等数据准备操作放到事务外

- 事务中避免远程调用，远程调用要设置超时，防止事务等待时间太久

- 事务中避免一次性处理太多数据，可以拆分成多个事务分次处理

- 更新等涉及加锁的操作尽可能放在事务靠后的位置

- 能异步处理的尽量异步处理

- 应用侧(业务代码)保证数据一致性，非事务执行



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/12-isolation-anomalies.html' | relative_url }}">← 上一篇：隔离级别与并发异常</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/14-lock-types.html' | relative_url }}">下一篇：InnoDB 锁的类型与兼容性 →</a>
</nav>
