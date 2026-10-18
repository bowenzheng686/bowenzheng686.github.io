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

扩缩容不是简单地增删服务器：Elasticsearch 会重新分配分片，节点角色、磁盘水位、网络连通性和副本数都会影响结果。以下以已有三节点集群扩充数据节点为例；命令和配置应与实际 Elasticsearch 大版本核对。

### 扩容：加入数据节点

在新主机上安装与现有集群兼容的 Elasticsearch，配置相同的 `cluster.name`、唯一的 `node.name`，并确保传输端口可达。现代版本使用 `node.roles` 指定角色：

```yaml
cluster.name: ELK-Cluster
node.name: es-node4
network.host: 10.0.0.104
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102", "10.0.0.103"]
node.roles: [data]
```

第二台新主机将名称与监听地址换成 `es-node5`、`10.0.0.105`。`cluster.initial_master_nodes` 仅用于**首次引导全新集群**，加入现有集群时不要重新设置。启动服务前还需确认安全配置、证书、JVM 内存及数据目录权限与现有节点匹配。

启动后查看节点与分片迁移：

```bash
sudo systemctl start elasticsearch
curl -s 'http://10.0.0.101:9200/_cat/nodes?v'
curl -s 'http://10.0.0.101:9200/_cluster/health?pretty'
curl -s 'http://10.0.0.101:9200/_cat/shards?v'
```

示例 URL 假定集群使用无认证的 HTTP；开启安全功能后应使用 HTTPS 与相应凭据。新节点出现不意味着扩容完成，仍需检查分片是否分配完毕、磁盘水位和查询/写入负载是否恢复稳定。

### 缩容：先迁出分片，再停止节点

计划移除 `es-node4` 时，可先暂时排除该节点的分片分配，并观察迁移结果。变更前确认其余节点有足够空间与满足索引副本的节点数量：

```http
PUT /_cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._name": "es-node4"
  }
}
```

待 `_cat/shards` 中不再有分片位于 `es-node4` 且集群状态稳定后，停止该节点。再以同样步骤处理 `es-node5`，不要同时停止两个仍持有副本的节点。结束后清理排除设置，避免影响未来同名节点：

```http
PUT /_cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._name": null
  }
}
```

### 将数据节点改为仅协调节点

所有 Elasticsearch 节点都能协调请求；只做协调、不存储数据的节点可设置 `node.roles: []`。**不能直接在仍保存分片的节点上改角色并重启**。先按上面的缩容方法迁出分片、停止服务，再按当前版本文档检查数据目录是否需要执行离线 `elasticsearch-node repurpose`；该工具可能删除与新角色不符的数据，务必先确认迁移与备份。修改角色后再启动并验证节点状态。

旧版资料中的 `node.master: false`、`node.data: false` 属旧版本配置，不适用于所有当前版本；以对应版本的节点角色文档为准。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/10-how-elasticsearch-clusters-work.html' | relative_url }}">← 上一篇：Elasticsearch 集群工作原理</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/12-elasticsearch-hot-and-cold-data-tiers.html' | relative_url }}">下一篇：Elasticsearch 数据冷热分离 →</a>
</nav>
