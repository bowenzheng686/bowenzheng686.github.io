---
layout: default
title: "JumpServer 堡垒机 · 安装方法介绍"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 07 安装方法介绍

安装方式决定了后续的升级、备份和排障方法。原资料把四种方式挤在同一行，实际应分别理解：

| 方式 | 适用情况 | 需要承担的工作 |
| --- | --- | --- |
| 手动按组件部署 | 需要理解各组件或有特殊集成要求 | 自行管理依赖版本、服务配置、证书与升级顺序 |
| 官方快速安装脚本 | 短期体验或受支持的标准环境 | 先核对脚本对应版本及其将修改的主机配置；后续仍需处理备份和更新 |
| 容器／Compose 部署 | 单机或少量节点，期望隔离组件依赖 | 管理镜像版本、持久化卷、环境变量与日志；Compose 不等于跨主机高可用 |
| 分布式部署 | 会话并发、可用性或地域隔离有明确要求 | 为入口、Core、连接组件、数据库、Redis 和录像存储分别设计扩容与故障恢复 |

后续章节展示若干具体部署示例。它们使用的镜像和命令可能对应不同的历史版本，动手前先确认目标版本和兼容性，不要把几种方案的配置拼在一起使用。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/06-installation-requirements.html' | relative_url }}">← 上一篇：安装要求</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">返回 JumpServer 专题目录</a>
  <a href="{{ '/subjects/JumpServer/08-docker-deployment.html' | relative_url }}">下一篇：Docker 部署 →</a>
</nav>
