---
layout: default
title: "MySQL 性能调优 · 实例级观测与调优顺序"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 22 实例级观测与调优顺序

## 从工作负载到资源瓶颈

原资料将 SQL/索引优化放在全局调优之前，这一顺序合理，但“不调参数就能解决大多数问题”同样不能保证。先按业务接口与 SQL digest 看 p95/p99、QPS、扫描/返回行比和锁等待，再看 CPU、内存、磁盘 I/O、连接排队、临时表与复制延迟。把变更窗口内的指标和同类历史时段对比，避免被流量变化误导。

![原资料的优化手段层次示意](assets/global-8-001-ca70823a7ba1.webp)

```sql
SHOW GLOBAL STATUS LIKE 'Threads_connected';
SHOW GLOBAL STATUS LIKE 'Threads_running';
SHOW GLOBAL STATUS LIKE 'Created_tmp_disk_tables';
SELECT * FROM sys.statement_analysis LIMIT 10;
```

`sys` 视图基于 Performance Schema，若采集未启用或实例版本不同，结果可能缺失。读取统计指标要看单位、时间窗口和重置时点。下一篇只讨论可通过证据驱动的关键参数。[官方参考：Performance Schema](https://dev.mysql.com/doc/refman/8.0/en/performance-schema.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=c0b91c9b60a787a2293a780ca5d3c151&sub=A8EEC383AEEB4D7C883228E7CAF37B17)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/21-checkpoint-crash-recovery.html' | relative_url }}">← 上一篇：checkpoint、刷盘与崩溃恢复</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/23-configuration-tradeoffs.html' | relative_url }}">下一篇：关键配置与资源预算 →</a>
</nav>
