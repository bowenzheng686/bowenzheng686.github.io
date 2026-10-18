---
layout: default
title: "ELK 日志分析 · ELK 应用场景"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 02 ELK 应用场景
### 1.2 ELK 应用场景

ELK（以及加入 Beats 等组件后的 Elastic Stack）适合把分散的数据汇集起来，再进行检索、分析和可视化。先区分数据来源与目标，才能决定是否需要 Logstash 处理、如何设计索引以及保留多久。

### 日志排障与运维

- **集中收集**：从不同主机、容器和应用采集日志，统一时间戳、字段与环境标识。
- **快速定位故障**：按服务、实例、请求 ID 和时间范围检索日志，关联同一次请求的异常信息。
- **可视化与告警**：统计错误率、异常类型和访问趋势，以仪表板展示，并根据明确的阈值或查询规则告警。

### 业务与安全分析

- **用户行为与性能分析**：对访问日志中的页面、来源、耗时等字段聚合，观察流量与延迟变化。
- **安全事件排查**：结合身份、来源 IP 与操作记录检索可疑行为。需要注意日志脱敏、访问权限及留存策略。
- **容量规划**：按时间序列观察日志量和业务指标，辅助扩容决策。自动故障恢复需要另接编排或自动化系统，并不是 ELK 自带的结果。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/01-introduction-to-elk.html' | relative_url }}">← 上一篇：ELK 介绍</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/03-elk-architecture.html' | relative_url }}">下一篇：ELK 应用架构 →</a>
</nav>
