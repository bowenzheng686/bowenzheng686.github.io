---
layout: default
title: "MySQL 性能调优 · 记录锁、间隙锁与 next-key 锁"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 15 记录锁、间隙锁与 next-key 锁

## 锁范围取决于实际扫描路径

记录锁保护索引记录；间隙锁保护记录之间的间隔；next-key 锁可视为记录锁加其前间隙。RR 下范围扫描常使用 next-key 锁以限制插入造成的幻行；但精确唯一索引等值命中已有记录等场景可能只需要记录锁。RC 下普通搜索/扫描的间隙锁行为不同，外键和重复键检查仍有例外。

```sql
-- 在测试库两会话观察；实际锁范围随索引与版本变化。
START TRANSACTION;
SELECT id FROM employees
WHERE name BETWEEN 'Li' AND 'Lu' FOR UPDATE;
-- 会话 B 尝试在该范围插入，再查看 data_locks/data_lock_waits。
```

RR 下的锁定范围不能套用“锁住所有扫过的记录和间隙”的固定公式：谓词、索引、优化器计划、唯一性、隔离级别均会改变锁定范围。无索引的更新尤其应先用计划审查实际扫描量，不要笼统称为“自动升级为表锁”。[官方参考：锁定语句所加锁](https://dev.mysql.com/doc/refman/8.0/en/innodb-locks-set.html)。

## 用索引区间理解三类锁

假设索引键依次是 10、20、30。记录锁针对某个现有索引条目；间隙锁针对条目之间的区间，如 (10,20)；next-key 锁可理解为一个记录锁加上其前方间隙，例如 (10,20]。还要考虑最小值前与最大值后的边界区间。间隙锁主要阻止向区间插入，并不等同于“锁住区间里每个尚不存在的值”；不同事务的间隙锁本身也可能兼容。

精确命中**已存在**记录的唯一索引等值锁定，通常只需锁住该记录；查询一个不存在的唯一键、使用非唯一索引等值条件或范围条件时，锁范围可能不同。二级索引扫描后回表更新，还可能在聚簇索引上取得锁。要判断一条 `UPDATE` 实际影响的并发，先核对 `EXPLAIN` 的访问路径，再在可复现事务中查看 `performance_schema.data_locks`。

## 两会话复现实验

~~~sql
CREATE TABLE lock_demo (
  id INT PRIMARY KEY,
  score INT NOT NULL,
  KEY idx_score (score)
) ENGINE=InnoDB;
INSERT INTO lock_demo VALUES (1,10),(2,20),(3,30);

-- 会话 A：设置 RR 并锁定一个非唯一索引范围
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM lock_demo
WHERE score BETWEEN 10 AND 20 FOR UPDATE;

-- 会话 B：在独立连接中尝试插入 score=15，观察是否等待
INSERT INTO lock_demo VALUES (4,15);
~~~

实际等待结果要结合唯一性、谓词边界及执行计划解释。完成实验后释放会话 A 的事务，并清理测试表。若会话 A 改用 RC，同一范围搜索通常不会按 RR 的方式保留普通 gap 锁，但外键检查和重复键检查仍存在例外；不能把 RC 解释成“完全没有间隙相关锁”。

业务上减少锁冲突的首选通常是缩短事务、增加合适索引并缩小扫描范围，而不是盲目降低隔离级别。降低隔离级别会改变读一致性和并发语义，必须与业务不变量一起评估。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/14-lock-types.html' | relative_url }}">← 上一篇：InnoDB 锁的类型与兼容性</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/16-mvcc-consistent-read.html' | relative_url }}">下一篇：MVCC、undo 与一致性读 →</a>
</nav>
