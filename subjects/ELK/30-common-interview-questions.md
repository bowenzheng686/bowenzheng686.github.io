---
layout: default
title: "ELK 日志分析 · 常见面试题"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 30 常见面试题
## 7 常见面试题

这些问题更适合用一个真实项目串起来回答：先交代数据量、保留周期和查询目标，再说明架构选择及自己负责的部分。没有固定的“正确机器数”；需要根据负载和可用性要求估算。

### 架构与数据流

1. **日志平台的完整数据流是什么？** 常见路径是应用日志 → Filebeat → Logstash（可选）→ Elasticsearch → Kibana。Filebeat 采集并转发，Logstash 解析和转换，Elasticsearch 建索引供检索，Kibana 查询并展示。
2. **Logstash 与 Filebeat 有何区别？** Filebeat 是轻量采集器，适合部署在日志源；Logstash 功能更丰富，适合集中进行复杂过滤和路由，但资源消耗更高。根据日志格式决定是否需要 Logstash。
3. **Logstash 常用哪些插件？** 输入可选 `beats`、`file`、`kafka`，过滤可选 `grok`、`date`、`mutate`、`geoip`，输出通常为 `elasticsearch`。应说明每个插件解决了什么问题，而非只报名称。

### Elasticsearch 设计与运维

4. **集群需要多少节点、各是什么角色？** 说明数据节点、主节点等角色和副本策略，再结合日写入量、保留天数、查询并发及故障容忍目标给出规模。不要把测试环境的节点数当成通用方案。
5. **如何实现冷热数据分层？** 按访问频率与保留期限制定索引生命周期策略，配置相应数据层及迁移规则；要核对所用 Elasticsearch 版本支持的具体机制。
6. **磁盘如何选型？** 热数据层关注随机读写与延迟，常采用 SSD；冷数据层可在容量与成本之间取舍。还需预留副本、段合并、水位线和增长空间。
7. **如何设计索引？** 明确时间范围、字段类型、模板、分片与生命周期。高基数字段及不必要的动态映射会增加存储和查询成本。
8. **如何优化 ELK？** 从采集端背压、解析规则、批量写入、分片数量、保留周期、查询过滤及监控入手，依据实际瓶颈调整，而非套用单一配置。

### 项目经验

9. **采集了哪些日志、自己负责什么？** 说清应用日志、访问日志或审计日志的来源，举一个字段解析和故障排查实例，并区分自己负责的部署、配置、运维和协作范围。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/29-writing-collected-logs-to-mysql-with-logstash.html' | relative_url }}">← 上一篇：使用 Logstash 将日志写入 MySQL</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
</nav>
