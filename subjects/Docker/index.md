---
layout: default
title: Docker 容器技术
subject_page: true
pdf_notes: true
---

# Docker 容器技术

本专题共 37 章，可按顺序阅读，也可直接查看所需主题。

## Docker 入门与基础管理

<ol start="1">
  <li><a href="{{ '/subjects/Docker/01-introduction-to-docker.html' | relative_url }}">Docker 介绍</a></li>
  <li><a href="{{ '/subjects/Docker/02-installing-docker-and-basic-commands.html' | relative_url }}">Docker 安装及基础命令介绍</a></li>
  <li><a href="{{ '/subjects/Docker/03-managing-container-images.html' | relative_url }}">容器镜像管理</a></li>
  <li><a href="{{ '/subjects/Docker/04-basic-container-commands.html' | relative_url }}">容器操作基础命令</a></li>
  <li><a href="{{ '/subjects/Docker/05-practical-examples.html' | relative_url }}">实战案例</a></li>
  <li><a href="{{ '/subjects/Docker/06-docker-run-parameters.html' | relative_url }}">查看 docker run 启动参数命令</a></li>
  <li><a href="{{ '/subjects/Docker/07-container-live-migration-with-criu.html' | relative_url }}">基于CRIU实现容器热迁移（了解）</a></li>
</ol>

## Docker 镜像构建

<ol start="8">
  <li><a href="{{ '/subjects/Docker/08-docker-image-fundamentals.html' | relative_url }}">Docker 镜像说明</a></li>
  <li><a href="{{ '/subjects/Docker/09-building-images-with-docker-commit.html' | relative_url }}">将现有容器通过 docker commit 手动构建镜像</a></li>
  <li><a href="{{ '/subjects/Docker/10-building-images-with-dockerfile.html' | relative_url }}">利用 DockerFile 文件执行 docker build 自动构建镜像</a></li>
</ol>

## Docker 数据管理

<ol start="11">
  <li><a href="{{ '/subjects/Docker/11-container-data-management.html' | relative_url }}">容器的数据管理介绍</a></li>
  <li><a href="{{ '/subjects/Docker/12-data-volumes.html' | relative_url }}">数据卷(data volume)</a></li>
  <li><a href="{{ '/subjects/Docker/13-data-volume-containers.html' | relative_url }}">数据卷容器（了解）</a></li>
</ol>

## Docker 网络

<ol start="14">
  <li><a href="{{ '/subjects/Docker/14-default-docker-networking.html' | relative_url }}">Docker的默认的网络通信（学习）</a></li>
  <li><a href="{{ '/subjects/Docker/15-container-name-networking.html' | relative_url }}">容器名称互联（了解）</a></li>
  <li><a href="{{ '/subjects/Docker/16-docker-network-modes.html' | relative_url }}">Docker 网络连接模式(重点)</a></li>
  <li><a href="{{ '/subjects/Docker/17-cross-host-container-networking.html' | relative_url }}">实现跨宿主机的容器之间网络互联（了解）</a></li>
</ol>

## Docker Compose 编排

<ol start="18">
  <li><a href="{{ '/subjects/Docker/18-introduction-to-docker-compose.html' | relative_url }}">Docker Compose 介绍</a></li>
  <li><a href="{{ '/subjects/Docker/19-installation-and-preparation.html' | relative_url }}">安装和准备</a></li>
  <li><a href="{{ '/subjects/Docker/20-starting-a-single-container-with-docker-compose.html' | relative_url }}">从 docker compose 启动单个容器</a></li>
  <li><a href="{{ '/subjects/Docker/21-starting-multiple-containers-with-docker-compose.html' | relative_url }}">从 docker compose 启动多个容器</a></li>
  <li><a href="{{ '/subjects/Docker/22-deploying-wordpress.html' | relative_url }}">实战案例: 实现 Wordpress 应用</a></li>
  <li><a href="{{ '/subjects/Docker/23-deploying-the-spug-operations-platform.html' | relative_url }}">实战案例: 搭建运维平台 Spug</a></li>
  <li><a href="{{ '/subjects/Docker/24-building-and-deploying-tomcat.html' | relative_url }}">实战案例: 构建和部署 Tomcat</a></li>
  <li><a href="{{ '/subjects/Docker/25-deploying-the-ruoyi-microservices-project.html' | relative_url }}">实战案例：RuoYI 微服务项目</a></li>
  <li><a href="{{ '/subjects/Docker/26-converting-between-docker-run-and-compose.html' | relative_url }}">实战案例: docker run 和 Docker Compose 文件相互转换</a></li>
  <li><a href="{{ '/subjects/Docker/27-using-json-configuration-files.html' | relative_url }}">使用 Json 格式文件</a></li>
</ol>

## Docker 仓库管理

<ol start="28">
  <li><a href="{{ '/subjects/Docker/28-official-docker-hub.html' | relative_url }}">官方 Docker 仓库</a></li>
  <li><a href="{{ '/subjects/Docker/29-alibaba-cloud-docker-registry.html' | relative_url }}">阿里云Docker仓库</a></li>
  <li><a href="{{ '/subjects/Docker/30-private-docker-registry.html' | relative_url }}">私有云单机仓库 Docker Registry （了解）</a></li>
  <li><a href="{{ '/subjects/Docker/31-distributed-harbor-registry.html' | relative_url }}">Docker 之分布式仓库 Harbor （重点）</a></li>
</ol>

## Docker 资源限制

<ol start="32">
  <li><a href="{{ '/subjects/Docker/32-docker-resource-limits.html' | relative_url }}">Docker 资源限制</a></li>
  <li><a href="{{ '/subjects/Docker/33-load-testing-with-stress-ng.html' | relative_url }}">Stress-ng 压力测试工具</a></li>
  <li><a href="{{ '/subjects/Docker/34-container-memory-limits.html' | relative_url }}">容器的内存限制</a></li>
  <li><a href="{{ '/subjects/Docker/35-container-cpu-limits.html' | relative_url }}">容器的 CPU 限制</a></li>
  <li><a href="{{ '/subjects/Docker/36-container-gpu-limits.html' | relative_url }}">容器的 GPU 限制 （了解）</a></li>
</ol>

## 常见面试题

<ol start="37">
  <li><a href="{{ '/subjects/Docker/37-common-interview-questions.html' | relative_url }}">常见面试题</a></li>
</ol>
