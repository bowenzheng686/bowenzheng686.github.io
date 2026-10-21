---
layout: default
title: "MySQL 性能调优 · checkpoint、刷盘与崩溃恢复"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 21 checkpoint、刷盘与崩溃恢复

## “已提交”不等于数据页已落盘

脏页可以晚于事务提交写入数据文件；崩溃后 InnoDB 根据持久化 redo 恢复应保留的更改，并利用 undo 处理未完成事务。checkpoint 推进后，较早的 redo 空间才可安全复用。doublewrite buffer 用于降低数据页部分写入造成的损坏风险，与 redo/undo 职责不同。

排查写入抖动时观察 redo 空间、脏页比例、刷盘速率、磁盘延迟和检查点推进，不应只把 `innodb_io_capacity` 调大。更改 `innodb_flush_log_at_trx_commit` 或 `sync_binlog` 前先确定可接受的数据丢失窗口。恢复演练应包括：备份可读、实例能启动、关键表计数和抽样校验、应用查询正确以及复制追平。

redo、binlog、undo 分别承担崩溃恢复、复制与时间点恢复、回滚与一致性读等职责；精确提交和恢复顺序需结合目标版本验证。[官方参考：InnoDB 恢复](https://dev.mysql.com/doc/refman/8.0/en/innodb-recovery.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/20-binlog-commit.html' | relative_url }}">← 上一篇：binlog 与提交一致性</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/22-instance-observability.html' | relative_url }}">下一篇：实例级观测与调优顺序 →</a>
</nav>
