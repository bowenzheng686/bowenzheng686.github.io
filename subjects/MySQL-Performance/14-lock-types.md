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

MySQL 8.0 推荐 `FOR SHARE`（旧写法 `LOCK IN SHARE MODE` 仍用于兼容）。元数据锁（MDL）保护表结构与正在使用它的语句，长事务可能阻塞 DDL；它与行锁、显式 `LOCK TABLES` 不是一回事。原资料按“乐观/悲观、表/页/行、读/写”分类时，要区分应用层版本号乐观并发控制与 InnoDB 实际锁类型。[官方参考：InnoDB 锁](https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html)。

---

本章依据 MySQL 官方手册与前后章节内容整合；用户所给锁/MVCC 链接与事务篇重复。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/13-transaction-optimization.html' | relative_url }}">← 上一篇：事务边界与长事务优化</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/15-gap-next-key-locks.html' | relative_url }}">下一篇：记录锁、间隙锁与 next-key 锁 →</a>
</nav>
