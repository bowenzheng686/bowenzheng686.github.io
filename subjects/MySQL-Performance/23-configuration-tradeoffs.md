---
layout: default
title: "MySQL 性能调优 · 关键配置与资源预算"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 23 关键配置与资源预算

## 连接、内存、日志不能分别拍脑袋

`max_connections` 决定允许的并发连接上限，但上调它不能解决慢查询导致的连接堆积；应用连接池、活跃线程数、CPU、每连接内存和操作系统文件描述符要一起评估。`innodb_buffer_pool_size` 应按实例是否独占、工作集和其他内存消耗定；排序/连接缓冲及临时表可能按会话或执行路径增加，不能简单把各缓冲值乘以连接数当作精确占用，也不能忽略极端并发风险。

```sql
SHOW VARIABLES WHERE Variable_name IN (
  'max_connections','innodb_buffer_pool_size',
  'innodb_redo_log_capacity','tmp_table_size','sort_buffer_size'
);
SHOW GLOBAL STATUS LIKE 'Max_used_connections';
```

固定内存比例、连接数公式和默认值可能随版本变化；应按“查看当前值 → 找到瓶颈 → 估算资源 → 单变量试验 → 回滚”。参数变更需注明作用域、动态生效性、重启需求和持久化方式。[官方参考：系统变量](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/22-instance-observability.html' | relative_url }}">← 上一篇：实例级观测与调优顺序</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/24-mysql-8-features.html' | relative_url }}">下一篇：MySQL 8.0 中与调优相关的能力 →</a>
</nav>
