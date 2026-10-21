---
layout: default
title: "MySQL 性能调优 · 数据页、Buffer Pool 与读写路径"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 18 数据页、Buffer Pool 与读写路径

## 先理解缓存，再讨论内存参数

MySQL Server 层解析与优化 SQL，InnoDB 存储引擎管理索引页、行记录和事务。原资料的总体架构图可帮助建立层次，但其中“查询缓存”属于旧版本：MySQL 8.0 已移除 query cache。Buffer Pool 缓存数据页与索引页，修改后的页成为脏页；刷盘由后台机制协调，而不是每条更新都立即随机写回数据文件。

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_dirty';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
```

缓存命中率要结合工作集、扫描模式和 I/O 延迟看，不能单凭一个高百分比断言没有瓶颈。原图保留于[原资料图像归档](source-figures.html)，但图中固定“内存占比 60–70%”不是普适配置建议。[官方参考：Buffer Pool](https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html)。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=f030268c54f18d2116837f8f3ef045bf&sub=4D84722956BB4A4BBB6C42A1D337BCAA)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/17-lock-waits-deadlocks.html' | relative_url }}">← 上一篇：锁等待、死锁与排障</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/19-redo-undo.html' | relative_url }}">下一篇：redo、undo 与提交耐久性 →</a>
</nav>
