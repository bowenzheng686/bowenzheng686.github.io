---
layout: default
title: "JumpServer 堡垒机 · 安装要求"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 06 安装要求

安装前先固定 JumpServer 的目标版本与部署方式。单机体验、容器部署、分布式部署所需的计算资源和外部依赖不同；尤其要核对数据库、Redis 与组件镜像的版本兼容性。

官方安装说明：

<https://docs.jumpserver.org/zh/master/install/setup_by_fast/>

原资料中的“2 核、4 GiB 内存、50 GiB 磁盘”可视为旧版实验环境的起点，不能作为生产容量保证。实际容量还受并发会话数、录像保留期、数据库大小和高可用副本数影响。规划时至少分别列出：

1. **计算与系统**：CPU 架构、操作系统版本、可用内存和磁盘空间是否满足当前发行版要求。
2. **数据库与缓存**：MySQL／MariaDB 与 Redis 的受支持版本、字符集、连接数和备份方式。原资料把 `utf8` 错写成 `uft8`，且列出的 Python 3.6、MySQL 5.6 等版本已经过时，不应照抄部署。
3. **网络与证书**：用户到入口、接入组件到目标资产、服务到数据库／Redis 的连通性，以及 HTTPS 证书与域名。
4. **审计存储**：按会话录像增长量估算保留空间，并测试归档与恢复。安装成功不代表审计数据已具备容灾能力。

下篇比较安装方式；选定方式后，再用对应版本的官方要求表核对具体数值。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/05-jumpserver-components.html' | relative_url }}">← 上一篇：JumpServer 组件</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">返回 JumpServer 专题目录</a>
  <a href="{{ '/subjects/JumpServer/07-installation-methods.html' | relative_url }}">下一篇：安装方法 →</a>
</nav>
