---
layout: default
title: "ELK 日志分析 · Elasticsearch 集群扩容和缩容"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 11 Elasticsearch 集群扩容和缩容
### 2.7 Elasticsearch 集群扩容和缩容

### 集群扩容

新加入两个节点node4和node5，变为Data节点

在两个新节点安装 ES，并配置文件如下

```text
vim /etc/elasticsearch/elasticsearch.yml
cluster.name: ELK-Cluster #和原集群名称相同
#当前节点在集群内的节点名称，同一集群中每个节点要确保此名称唯一
node.name: es-node4 #第二个新节点为es-node5
#集群监听端口对应的IP，默认是127.0.0.1:9300
network.host: 0.0.0.0
#指定任意集群节点即可
discovery.seed_hosts: ["10.0.0.101","10.0.0.102","10.0.0.103"]
#集群初始化时指定希望哪些节点可以被选举为 master,只在初始化时使用,新加节点到已有集群时此项可不
配置
#cluster.initial_master_nodes: ["10.0.0.101","10.0.0.102","10.0.0.103"]
#cluster.initial_master_nodes: ["ubuntu2204.bowen.org"]
```

```text
#如果不参与主节点选举设为false,默认值为true
node.master: false
#存储数据,默认值为true,此值为false则不存储数据而成为一个路由节点
#如果将原有的true改为false,需要先执行/usr/share/elasticsearch/bin/elasticsearch-node
repurpose 清理数据
node.data: true
systemctl restart elasticsearch
```

### 集群缩容

从集群中删除两个节点node4和node5，在两个节点按一定的顺序逐个停止服务，即可自动退出集群

注意：停止服务前，要观察索引的情况，按一定顺序关机，即先关闭一台主机，等数据同步完成后，再关闭第二台主机，防止数据丢失

```text
systemctl stop elasticsearch
```

### Data 节点变为Coordinating 节点

将一个节点node3变为Coordinating 节点

在node3执行下面操作

```text
vim /etc/elasticsearch/elasticsearch.yml
node.master: false
#存储数据,默认值为true,此值为false则不存储数据而成为一个路由节点,如果将原有的true改为false,
需要先执行 清理数据
node.data: false
#无法启动
systemctl restart elasticsearch
#清理数据
/usr/share/elasticsearch/bin/elasticsearch-node repurpose
#重启
systemctl start elasticsearch
#注意：Coordinating 节点在 Cerebro 等插件中前端数据页面不显示，在nodes页才会显示出来
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/10-how-elasticsearch-clusters-work.html' | relative_url }}">← Previous: How Elasticsearch Clusters Work</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/12-elasticsearch-hot-and-cold-data-tiers.html' | relative_url }}">Next: Elasticsearch Hot and Cold Data Tiers →</a>
</nav>
