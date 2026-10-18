---
layout: default
title: "ELK 日志分析 · Kibana 介绍"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 20 Kibana 介绍
## 5 Kibana 图形显示

### 5.1 Kibana 介绍

Kibana 是 Elastic Stack 的浏览器端分析与可视化界面，主要与 Elasticsearch 配合使用。它可以通过数据视图检索索引中的数据，创建图表、表格、地图和仪表板，便于观察日志量、错误趋势及业务指标。

Kibana 负责查询和展示，**不负责代替采集器收集日志**。部署时应先确认 Elasticsearch 中已有可用数据，再配置 Kibana 与集群的连接，并让两者版本保持兼容。Kibana 的前端及相关代码主要使用 TypeScript。

### 下载与参考链接

官方当前版本及历史版本：

<https://www.elastic.co/cn/downloads/kibana>

<https://www.elastic.co/cn/downloads/past-releases#kibana>

镜像站（版本覆盖情况以站点实际提供为准）：

<https://mirrors.tuna.tsinghua.edu.cn/elasticstack/>

官方演示：

<https://demo.elastic.co/>

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/19-logstash-practical-examples.html' | relative_url }}">← 上一篇：Logstash 实践示例</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/21-installing-and-configuring-kibana.html' | relative_url }}">下一篇：安装和配置 Kibana →</a>
</nav>
