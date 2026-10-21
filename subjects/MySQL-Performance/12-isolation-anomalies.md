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

原资料列举脏读、不可重复读、幻读和丢失更新。MySQL/InnoDB 支持 `READ UNCOMMITTED`、`READ COMMITTED`（RC）、`REPEATABLE READ`（RR）及 `SERIALIZABLE`；默认隔离级别通常是 RR，但应用要以当前实例配置为准。RC 的一致性读通常每条语句取新快照，RR 通常在事务中首次一致性读建立快照。`SELECT ... FOR UPDATE` 是当前读/锁定读，不能拿它的结果与普通快照读混为一谈。

```sql
SELECT @@transaction_isolation;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
SELECT balance FROM accounts WHERE id = 1;
COMMIT;
```

隔离级别不是“越高越好”：要结合并发量、锁冲突、复制设置和业务不变量选择。所谓“RR 完全杜绝一切幻读”也不严谨，特别是在同一事务混用快照读与当前读时，观察结果与加锁行为会不同。丢失更新应通过原子更新、条件更新或锁定读设计避免。[官方参考：InnoDB 隔离级别](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=9cdb35f4b463f3db296c57f5120bcf5d&sub=DA9C05A19FCE4B4EA56272006036698F)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/11-transactions-acid.html' | relative_url }}">← 上一篇：事务、ACID 与提交边界</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/13-transaction-optimization.html' | relative_url }}">下一篇：事务边界与长事务优化 →</a>
</nav>
