---
layout: default
title: "MinIO 对象存储 · 部署模式和方法"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 05 部署模式和方法

部署时要分开考虑两个问题：**数据分布在多少个磁盘和节点上**，以及**用什么方式启动和管理 MinIO 进程**。包、二进制、容器和 Kubernetes 是运行方式；单盘、多盘、多节点才是数据布局，不能混成一张清单。

| 数据布局 | 适合用途 | 需要注意 |
| --- | --- | --- |
| 单机单盘 | 本地学习或功能验证 | 没有跨盘冗余，磁盘或主机故障可能直接影响数据 |
| 单机多盘 | 在一台机器上学习多盘数据分布 | 可应对部分磁盘故障，但整机仍是故障点 |
| 多机多盘 | 有明确容量和可用性要求的集群 | 需要规划节点、磁盘、网络、纠删集与恢复时间 |

运行方式可选系统包、独立二进制、Docker 容器或 Kubernetes。容器化方便交付，但不会自动带来跨节点高可用；Kubernetes 也需要持久卷、节点故障域和负载入口设计。下一篇先实践单机部署，再进入多节点集群。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/04-how-minio-works.html' | relative_url }}">← 上一篇：MinIO 工作机制</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 专题目录</a>
  <a href="{{ '/subjects/MinIO/06-standalone-deployment.html' | relative_url }}">下一篇：单机部署 →</a>
</nav>
