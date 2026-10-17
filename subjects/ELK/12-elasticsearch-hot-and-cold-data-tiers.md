---
layout: default
title: "ELK Log Analytics · Elasticsearch Hot and Cold Data Tiers"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 12 Elasticsearch Hot and Cold Data Tiers
### 2.8 Elasticsearch 数据冷热分离

### 冷热分离原理

为了保证Elasticsearch的读写性能，官方建议磁盘使用SSD固态硬盘。然而Elasticsearch要解决的是海量数据的存储和检索问题，海量的数据就意味需要大量的存储空间，如果都使用SSD固态硬盘成本将成为一个很大的问题，这也是制约许多企业和个人使用Elasticsearch的因素之一。为了解决这个问题， Elasticsearch冷热分离架构应运而生。 传统的Elasticsearch集群中所有节点均采用相同的配置，然而Elasticsearch并没有对节点的规格一致性做要求，换而言之就是每个节点可以是任意规格，当然这样做会导致集群各节点性能不一致，影响集群稳定性。但是如果有规则的将集群的节点分成不同类型，部分是高性能的节点用于存储热点数据，部分是性能相对差些的大容量节点用于存储冷数据，却可以一方面保证热数据的性能，另一方面保证冷数据的存储，降低存储成本，这也是Elasticsearch冷热分离架构的基本思想

### 配置方法

### 准备硬件配置不同的多个节点

如下图为一个3热节点，2冷节点的冷热分离Elasticsearch集群

节点 CPU 内存存储

Node1 16C 64G 1TB SSD

Node2 16C 64G 1TB SSD

Node3 16C 64G 1TB SSD

Node4 8C 32G 5TB HDD

Node5 8C 32G 5TB HDD

### 指定节点的冷热属性

仅仅将不同的节点设置为不同的规格还不够，为了能明确区分出哪些节点是热节点，哪些节点是冷节点，需要为对应节点打标签

Elasticsearch支持给节点打标签，具体方式是在elasticsearch.yml文件中增加

```text
node.attr.{attribute}: {value}
#其中attribute为用户自定义的任意标签名，value为该节点对应的该标签的值
```

例如对于冷热分离，可以使用如下设置

```text
#示例
vim elasticsearch.yml
node.attr.temperature: hot //热节点
node.attr.temperature: warm  //冷节点
```

```text
#验证
GET _cat/nodeattrs?v&h=node,attr,value&s=attr:desc
node        attr        value
node1   temperature     hot
node2   temperature     hot
node3   temperature     warm
node4   temperature     hot
node5   temperature     warm
```

```bash
[root@ubuntu2404 ~]#curl 'http://10.0.0.101:9200/_cat/nodeattrs?
v&h=node,attr,value&s=attr:desc'
node   attr                           value
node-1 xpack.installed                true
node-3 xpack.installed                true
node-2 xpack.installed                true
node-1 transform.config_version       10.0.0
node-3 transform.config_version       10.0.0
node-2 transform.config_version       10.0.0
node-1 temperature                    hot
node-3 temperature                    cold
node-2 temperature                    hot
node-1 ml.max_jvm_size                2030043136
node-3 ml.max_jvm_size                2030043136
node-2 ml.max_jvm_size                2030043136
node-1 ml.machine_memory              4056039424
node-3 ml.machine_memory              4056064000
node-2 ml.machine_memory              4056064000
node-1 ml.config_version              12.0.0
node-3 ml.config_version              12.0.0
node-2 ml.config_version              12.0.0
node-1 ml.allocated_processors_double 2.0
node-3 ml.allocated_processors_double 2.0
node-2 ml.allocated_processors_double 2.0
node-1 ml.allocated_processors        2
node-3 ml.allocated_processors        2
node-2 ml.allocated_processors        2
```

### 指定索引冷热属性

指定数据的冷热属性，来设置和调整数据分布。冷热分离方案中数据冷热分布的基本单位是索引，即指定某个索引为热索引，另一个索引为冷索引。通过索引的分布来实现控制数据分布的目的。

Elasticsearch提供了index shard filtering功能(2.x开始)，该功能在索引配置中提供了如下几个配置

用户可以在创建索引，或后续的任意时刻设置这些配置来控制索引在不同标签节点上的分配动作。

```text
index.routing.allocation.include.{attribute} #表示索引可以分配在包含多个逗号分隔的值中其
中一个的节点上。
index.routing.allocation.require.{attribute} #表示索引要分配在包含索引指定多个逗号分隔的
值的节点上,并且多个值都要匹配
index.routing.allocation.exclude.{attribute} #表示索引只能分配在不包含指定多个逗号分隔的
值值的节点上。
```

业务方可以根据实际情况决定索引的冷热属性

范例:

```json
#对于热数据，索引设置如下
PUT hot_warm_test_index/_settings
{
"index.routing.allocation.require.temperature": "hot"
}
#示例:将index1索引设亩hot的属性
curl -XPUT http://10.0.0.101:9200/index1/_settings -H 'Content-Type:
application/json'  -d '
{
"index.routing.allocation.require.temperature": "hot"
}'
```

```bash
#查看分片分配,发现分片均分配在热节点上
GET _cat/shards/hot_warm_test_index?v&h=index,shard,prirep,node&s=node
#查看index1的数据只存放在hot节点node-1和node-2节点上
[root@ubuntu2404 ~]#curl 'http://10.0.0.101:9200/_cat/shards/index1?
v&h=index,shard,prirep,node&s=node'
index  shard prirep node
index1 0     r      node-1
index1 1     p      node-1
index1 0     p      node-2
index1 1     r      node-2
```

```json
#对于冷数据，索引设置
PUT hot_warm_test_index/_settings
{
"index.routing.allocation.require.temperature": "warm"
}
#查看分片分配，发现分片均分配到冷节点上
GET _cat/shards/hot_warm_test_index?v&h=index,shard,prirep,node&s=node
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/11-scaling-elasticsearch-clusters.html' | relative_url }}">← Previous: Scaling Elasticsearch Clusters</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/13-monitoring-performance-with-metricbeat.html' | relative_url }}">Next: Monitoring Performance with Metricbeat →</a>
</nav>
