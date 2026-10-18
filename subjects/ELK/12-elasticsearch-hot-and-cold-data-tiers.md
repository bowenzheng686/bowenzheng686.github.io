---
layout: default
title: "ELK 日志分析 · Elasticsearch 数据冷热分离"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 12 Elasticsearch 数据冷热分离
### 2.8 Elasticsearch 数据冷热分离

### 为什么按数据温度分层

近期写入、频繁查询的日志适合放在性能较高的热层；查询较少但仍需保留的数据可以迁往成本较低的温层或冷层。分层目标是平衡检索性能、存储成本和保留时间，而不是仅凭磁盘类型把节点分组。具体的磁盘选择仍应按写入量、查询负载与副本需求测试。

| 层级 | 典型用途 | 规划重点 |
| --- | --- | --- |
| 热层 | 持续写入和高频查询 | 写入吞吐、低延迟、足够的副本空间。 |
| 温层 | 写入减少、偶尔查询 | 成本与查询性能的平衡。 |
| 冷层 | 很少查询的历史数据 | 较长保留期、恢复时间与存储成本。 |

例如三台热节点和两台冷节点可以采用不同的 CPU、内存和磁盘规格，但必须确认每层都能容纳目标分片及其副本。只有一台冷节点时，要求两个副本分布到冷层可能无法满足。

### 当前版本：数据层与生命周期策略

较新的 Elasticsearch 版本提供 `data_hot`、`data_warm`、`data_cold` 等数据层角色，并通常由索引生命周期管理（ILM）把索引从热层迁往后续层级。先为各节点设置对应角色，再定义索引模板和 ILM 策略；迁移前应验证目标层容量、索引是否仍在写入及所用版本的功能支持情况。分片分配偏好可通过 `_tier_preference` 查看：

```http
GET /my-index/_settings/index.routing.allocation.include._tier_preference
GET /_cat/shards/my-index?v&h=index,shard,prirep,node
```

此处 `my-index` 是实际索引名占位符。新版本优先采用数据层和 ILM，不要把下面的手工属性过滤与 `_tier_preference` 混用而产生相互矛盾的分配约束。

### 旧版方案：自定义节点属性与索引过滤

在仍使用自定义属性的版本中，可给节点设置 `node.attr.temperature: hot` 或 `node.attr.temperature: cold`，然后按索引要求分片落在对应节点。例如：

```yaml
# 热节点的 elasticsearch.yml
node.attr.temperature: hot
```

```yaml
# 冷节点的 elasticsearch.yml
node.attr.temperature: cold
```

在 Dev Tools 中查看节点属性，并把已有索引限制在热节点：

```http
GET /_cat/nodeattrs?v&h=node,attr,value

PUT /my-index/_settings
{
  "index.routing.allocation.require.temperature": "hot"
}

GET /_cat/shards/my-index?v&h=index,shard,prirep,node
```

需要迁往冷节点时，将 `hot` 改为 `cold`，并在变更后持续观察分片恢复与磁盘水位。`include` 表示可落在匹配节点，`require` 表示必须满足属性条件，`exclude` 表示排除匹配节点；具体多个值的匹配语义以当前版本文档为准。原资料把 `warm`、`cold` 混称，并把 HTTP 请求与 JSON 混在同一代码块，容易导致读者复制后执行失败。

如果分片迟迟没有迁移，先用分配解释 API 检查原因，不要继续叠加过滤条件：

```http
GET /_cluster/allocation/explain
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/11-scaling-elasticsearch-clusters.html' | relative_url }}">← 上一篇：Elasticsearch 集群扩容和缩容</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/13-monitoring-performance-with-metricbeat.html' | relative_url }}">下一篇：利用 Metricbeat 监控性能相关指标 →</a>
</nav>
