---
layout: default
title: "微服务架构 · Kafka 介绍"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 14 Kafka 介绍
### 3.2 Kafka 介绍

![微服务技术第 40 页插图](assets/img-21dc56f8886243dc.webp)

Apache Kafka 是分布式事件流平台。生产者将记录写入主题（Topic）的分区；Broker 按配置保存数据并通过副本提供故障容忍；消费者组跟踪消费位点，既可处理新事件，也可在保留期内按位点重放。与“取走就从队列删除”的模型不同，消息是否仍可读取由保留策略决定。

典型用途包括业务事件分发、日志与变更数据采集，以及接入流处理应用。Kafka 的吞吐和延迟取决于分区数、消息大小、批量、压缩、磁盘和网络条件，不能只用“快”来描述。下一篇比较不同产品时，应先明确是否需要重放、复杂路由、严格顺序范围与运维成本。

官方文档：<https://kafka.apache.org/documentation/>。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/13-introduction-to-message-queues.html' | relative_url }}">← 上一篇：消息队列简介</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/15-comparing-message-queues.html' | relative_url }}">下一篇：常用消息队列对比 →</a>
</nav>
