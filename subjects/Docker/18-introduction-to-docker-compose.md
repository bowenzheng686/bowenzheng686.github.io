---
layout: default
title: "Docker 容器技术 · Docker Compose 介绍"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 18 Docker Compose 介绍

Docker Compose 用一个 YAML 文件描述由多个容器组成的应用，并用 `docker compose` 命令统一创建、启动、查看和停止这些服务。它适合本地开发、测试和单机部署；如果需要跨多台主机调度容器，则要评估其他编排方案。

![Docker 容器技术第 343 页插图](assets/img-aaad6bb5b7425758.webp)

假设一个应用包含 Nginx、应用服务和 MySQL。逐条执行 `docker run` 时，维护人员要反复指定网络、端口、卷和环境变量，配置稍有不一致就可能无法互通。Compose 则把这些设置写在同一份配置里，让服务一起启动，并让同一项目中的容器通过服务名互相访问。

不过，`depends_on` 主要描述启动依赖；**容器已启动不等于服务已准备好**。如果应用必须等数据库可接受连接后才启动，应为数据库设置健康检查，并让依赖条件或应用自身的重试机制处理就绪问题。Compose 也不会替应用解决数据库初始化和数据迁移。

可把 Compose 文件理解为“声明应用由哪些服务组成”，而不是一段依次执行 `docker run` 的 Shell 脚本。日常流程通常是修改配置后运行 `docker compose up -d`，用 `docker compose ps` 检查状态，并通过 `docker compose logs` 定位问题。旧资料中的独立命令 `docker-compose` 对应早期版本；当前 Docker Compose 插件使用带空格的 `docker compose`。

- 项目地址：<https://github.com/docker/compose>
- 官方文档：<https://docs.docker.com/compose/>

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/17-cross-host-container-networking.html' | relative_url }}">← 上一篇：跨主机容器网络</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术专题目录</a>
  <a href="{{ '/subjects/Docker/19-installation-and-preparation.html' | relative_url }}">下一篇：安装与准备 →</a>
</nav>
