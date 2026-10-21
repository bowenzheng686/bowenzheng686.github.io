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



## redo 写入、检查点与刷盘策略

### Innodb底层原理与Mysql日志机制

![redo、undo 与提交耐久性配图](assets/innodb-logs-004-9e5c100bae7c.webp)

### redo log重做日志关键参数

innodb_log_buffer_size 控制 redo log buffer 大小，应结合事务大小与写入压力观测，不使用固定值作为通用建议。

```sql
show variables like '%innodb_log_buffer_size%';
```

旧版本常以 innodb_log_group_home_dir 指定 redo 路径；MySQL 8.0.30+ 的 redo 文件组织和容量参数已调整，配置前要核对实际版本。

```sql
show variables like '%innodb_log_group_home_dir%';
```

![redo、undo 与提交耐久性配图](assets/innodb-logs-005-1aba15ed97a1.webp)

旧版本通过 innodb_log_files_in_group 控制文件数；MySQL 8.0.30+ 应重点检查 innodb_redo_log_capacity。

```sql
show variables like '%innodb_log_files_in_group%';
```

旧版本使用 innodb_log_file_size 规划单文件大小；MySQL 8.0.30+ 主要通过 innodb_redo_log_capacity 管理总容量。

```sql
show variables like '%innodb_log_file_size%';
```

redo log 写入磁盘过程分析：

redo 记录循环复用，容量不足会推动刷盘与检查点；文件布局随 MySQL 版本改变，下面的环形图只表达日志复用与 checkpoint 的关系。

![redo、undo 与提交耐久性配图](assets/innodb-logs-006-ee44827869cd.webp)

write position 表示新 redo 写入进度；checkpoint 表示已可安全回收的进度。实现中的日志序号与物理文件布局需按版本理解。

推进 checkpoint 的前提是相关脏页已持久化；这不是简单“擦除记录”。

当可用 redo 空间逼近下限时，InnoDB 会加强刷盘，写入可能受阻；应观察 redo 容量、脏页和 I/O，而非仅调整单个参数。

innodb_flush_log_at_trx_commit：这个参数控制 redo log 的写入策略，它有三种可能取值：

- 设置为0：表示每次事务提交时都只是把 redo log 留在 redo log buffer 中，数据库宕机可能会丢失数据。

- 设为 1 时每次提交要求将 redo 刷到持久存储，通常提供较强的提交耐久性；仍需考虑操作系统、控制器缓存与硬件故障模型。

- 设为 2 时提交将 redo 写入操作系统缓存，后续再刷盘；mysqld 进程故障与整机故障的数据丢失风险不同。

后台刷盘存在周期性行为，但调度受负载与实现影响，不应把“每隔 1 秒”视为严格的持久化保证。

redo log写入策略参看下图：

![redo、undo 与提交耐久性配图](assets/innodb-logs-007-878f76ccde3f.webp)

```sql
# 查看innodb_flush_log_at_trx_commit参数值：
show variables like 'innodb_flush_log_at_trx_commit';
# 设置innodb_flush_log_at_trx_commit参数值(也可以在my.ini或my.cnf文件里配置)：
set global innodb_flush_log_at_trx_commit=1;
```



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/18-pages-buffer-pool.html' | relative_url }}">← 上一篇：数据页、Buffer Pool 与读写路径</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/20-binlog-commit.html' | relative_url }}">下一篇：binlog 与提交一致性 →</a>
</nav>
