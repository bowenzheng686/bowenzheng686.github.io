---
layout: default
title: "MinIO 对象存储 · 缩容"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 15 缩容

缩容比扩容更容易误删数据。MinIO 的对象分片属于特定服务器池和纠删码集合，**不能直接从 `MINIO_VOLUMES` 删除一组端点、停掉节点并重启剩余服务**。原案例在“缩容成功”后显示 `0 Objects`，而缩容前有 `6 Objects`；这恰恰说明对象不可见或已经丢失，不能将“进程启动且节点数变少”视为成功。

## 先判断要缩减什么

- **释放一整个服务器池**：确认当前版本支持该池的退役／decommission，且剩余池有足够可用容量与写入余量；按官方流程迁移、验证，再移除端点。
- **减少单个池内的节点或磁盘**：通常不能直接删除端点来缩小现有纠删码集合，应评估新建目标集群并迁移对象。
- **缩小 LVM 或文件系统**：与 MinIO 集群缩容不是一回事，文件系统未必支持在线缩小；容量占用、纠删码开销和底层文件系统都需要单独评估。

不论采用哪条路线，都先记录存储桶、对象数、版本、生命周期策略、对象锁、复制配置、用户和访问密钥，以及备份的可恢复性。访问密钥等管理配置未必会随着对象复制自动迁移。

## 可退役服务器池的处理思路

在支持服务器池退役的版本中，先用 `mc admin info` 查看池和容量，再通过当前版本 `mc admin decommission --help` 确认命令语法与限制。退役过程中要保留原池的服务与数据盘可用，让对象迁移到其他池；持续观察状态与错误，不能提前停掉节点。

```bash
mc admin info minio-cluster
mc admin decommission --help
mc admin heal minio-cluster --dry-run
```

只有退役状态明确完成，且对象清单、抽样下载、版本与元数据核验通过后，才按该版本文档更新集群端点和负载均衡后端。退役是否支持、对象锁等特性的限制、以及需要多少空余空间，都要以实际版本为准。任何失败应先保留原池，排查并重试，不要用直接删除配置“完成”流程。

## 不支持原地缩容时

建立容量与冗余设计合理的新集群，使用受支持的对象复制或迁移工具转移对象，再核对桶配置、版本、权限和应用访问。切换客户端入口前，应验证新集群的读写和回滚路径；保留旧集群一段观察期，确认无遗漏后再下线。第 16、17 章介绍备份与恢复，但备份和迁移仍需分别设计。

缩容验收至少包括：缩容前后对象与版本清单可对照、抽样校验一致、应用无读写错误、所有预期驱动器在线、监控与备份重新覆盖目标拓扑。仅看到 `mc admin info` 中节点数下降，不构成数据完整性证明。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/14-scaling-out.html' | relative_url }}">← 上一篇：扩容</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/16-backup-and-restore-overview.html' | relative_url }}">下一篇：备份与恢复概述 →</a>
</nav>
