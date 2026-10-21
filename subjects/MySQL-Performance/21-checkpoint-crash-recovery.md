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



## undo、刷盘与其他日志

### undo log回滚日志

undo 信息按回滚段管理，支持事务回滚与一致性读；具体表空间布局和清理机制随版本变化。

旧版回滚段数量限制不能直接推算现代 MySQL 的最大并发事务数；应以目标版本文档及实例观测为准。

```sql
SHOW VARIABLES LIKE 'innodb_undo%';
-- 核对当前版本的 undo tablespace、截断与清理配置。
```

undo log日志什么时候删除

插入类 undo 在相关回滚需求结束后可回收；回收时机由事务和 purge 机制决定。

更新、删除类 undo 可能仍被旧 Read View 需要，必须等不再被可见性判断引用后才能清理。

为什么Mysql不能直接更新磁盘上的数据而设置这么一套复杂的机制来执行SQL了？

因为来一个请求就直接对磁盘文件进行随机读写，然后更新磁盘文件里的数据性能可能相当差。

因为磁盘随机读写的性能是非常差的，所以直接更新磁盘文件是不能让数据库抗住很高并发的。

写入先作用于 Buffer Pool 中的页，并记录 redo；脏页之后刷回数据文件。该路径把提交持久性与随机数据页写入解耦。

更新内存的性能是极高的，然后顺序写磁盘上的日志文件的性能也是非常高的，要远高于随机读写磁盘文件。

实际吞吐取决于工作集、索引数量、锁竞争、日志与存储系统，不能按机器配置给出固定 QPS 承诺。

### 错误日志

错误日志记录服务器启动、关闭和运行中的诊断信息；实例异常时，可先查看最近的错误日志并结合系统日志分析。

错误日志的输出位置、格式与详细程度取决于版本和配置，不应假定它固定写入某个文件，或记录了所有 SQL 错误。

```sql
# 查看错误日志存放位置
show variables like '%log_error%';
```

### 通用查询日志

通用查询日志主要记录客户端连接、断开及服务器收到的语句，可用于还原部分请求过程；它不是审计系统，也不记录服务器启动、关闭的全部细节。

通用查询日志用来还原操作时的具体场景，可以帮助我们准确定位一些疑难问题，比如重复支付等问题。

general_log：是否开启日志参数，默认为OFF，处于关闭状态，因为开启会消耗系统资源并且占用磁盘空间。一般不建议开启，只在需要调试查询问题时开启。

general_log_file：通用查询日志记录的位置参数。

```sql
show variables like '%general_log%';
# 打开通用查询日志
SET GLOBAL general_log=on;
```



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/20-binlog-commit.html' | relative_url }}">← 上一篇：binlog 与提交一致性</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/22-instance-observability.html' | relative_url }}">下一篇：实例级观测与调优顺序 →</a>
</nav>
