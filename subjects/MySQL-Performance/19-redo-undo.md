---
layout: default
title: "MySQL 性能调优 · redo、undo 与提交耐久性"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 19 redo、undo 与提交耐久性

## 两种日志解决不同问题

redo log 记录 InnoDB 页变更的恢复信息，使提交后的修改可在崩溃后重放；undo log 保存回滚所需的信息并支撑一致性读。它们不是互相替代的“前镜像/后镜像文件”。写数据页之前先持久化必要的 redo，属于 WAL 思路；实际耐久性还受 `innodb_flush_log_at_trx_commit`、操作系统和存储设备影响。

```sql
SHOW VARIABLES LIKE 'innodb_flush_log_at_trx_commit';
SHOW VARIABLES LIKE 'innodb_redo_log_capacity';
SHOW GLOBAL STATUS LIKE 'Innodb_os_log%';
```

`innodb_flush_log_at_trx_commit` 的 `0/1/2` 取值应结合故障模型理解：`1` 通常是更强的提交刷盘要求，但不能绝对保证所有硬件故障零丢失；放松刷盘可提高吞吐，也会扩大故障窗口。MySQL 8.0.30 起 redo 容量主要由 `innodb_redo_log_capacity` 控制，不要照搬只适用于旧版本的日志文件数/大小配置。[官方参考：redo log](https://dev.mysql.com/doc/refman/8.0/en/innodb-redo-log.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/18-pages-buffer-pool.html' | relative_url }}">← 上一篇：数据页、Buffer Pool 与读写路径</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/20-binlog-commit.html' | relative_url }}">下一篇：binlog 与提交一致性 →</a>
</nav>
