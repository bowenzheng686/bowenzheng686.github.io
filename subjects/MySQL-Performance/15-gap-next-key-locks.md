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

原资料“RR 会锁住所有扫过的记录和间隙”可作为直观引入，但不应当成精确锁集合公式：谓词、索引、优化器计划、唯一性、隔离级别均会改变锁定范围。无索引的更新尤其应先用计划审查实际扫描量，不要笼统称为“自动升级为表锁”。[官方参考：锁定语句所加锁](https://dev.mysql.com/doc/refman/8.0/en/innodb-locks-set.html)。

---

本章依据 MySQL 官方手册与前后章节内容整合；用户所给锁/MVCC 链接与事务篇重复。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/14-lock-types.html' | relative_url }}">← 上一篇：InnoDB 锁的类型与兼容性</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/16-mvcc-consistent-read.html' | relative_url }}">下一篇：MVCC、undo 与一致性读 →</a>
</nav>
