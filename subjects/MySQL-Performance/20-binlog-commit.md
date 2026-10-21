---
layout: default
title: "MySQL 性能调优 · binlog 与提交一致性"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 20 binlog 与提交一致性

## Server 层日志与引擎日志的衔接

binlog 是 MySQL Server 层的二进制变更日志，用于复制和时间点恢复；redo 是 InnoDB 引擎的崩溃恢复机制。为避免“引擎已提交但 binlog 缺失”或相反的持久化不一致，MySQL 将事务提交与 binlog 写入协调起来，常称两阶段提交。不能把 binlog 当作唯一备份，也不能用手工删除当前日志文件来释放空间。

```sql
SHOW VARIABLES LIKE 'log_bin';
SHOW VARIABLES LIKE 'binlog_format';
SHOW VARIABLES LIKE 'sync_binlog';
SHOW BINARY LOGS;
```

原资料的 `mysqlbinlog` 查看与误删恢复演示可以作为**隔离测试环境**案例；真实恢复须从经过校验的全量备份加 binlog 重放，并明确停止位置、GTID/事务边界和复制拓扑。清理日志前确认备份和所有副本的需求。[官方参考：binlog](https://dev.mysql.com/doc/refman/8.0/en/binary-log.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=f030268c54f18d2116837f8f3ef045bf&sub=4D84722956BB4A4BBB6C42A1D337BCAA)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/19-redo-undo.html' | relative_url }}">← 上一篇：redo、undo 与提交耐久性</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/21-checkpoint-crash-recovery.html' | relative_url }}">下一篇：checkpoint、刷盘与崩溃恢复 →</a>
</nav>
