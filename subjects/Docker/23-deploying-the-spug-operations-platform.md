---
layout: default
title: "Docker 容器技术 · 实战案例: 搭建运维平台 Spug"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 23 实战案例: 搭建运维平台 Spug
### 5.6 实战案例: 搭建运维平台 Spug

Spug 是面向中小团队的运维平台，提供主机管理、批量执行、应用发布、任务计划和告警等功能。下面用 Docker Compose 展示数据库与应用服务的依赖关系；具体镜像标签、初始化命令及环境变量应与所用 Spug 版本的官方文档核对。

官方安装文档：

<https://spug.cc/docs/install-docker>

### 使用 Compose 部署

先在部署目录创建 `.env`，设置 `SPUG_DB_PASSWORD` 与 `SPUG_DB_ROOT_PASSWORD`，并确保数据目录可写。不要将实际密码提交到仓库。

```yaml
services:
  db:
    image: mysql:5.7.30
    container_name: spug-db
    restart: unless-stopped
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
    volumes:
      - /data/spug/mysql:/var/lib/mysql
    environment:
      MYSQL_DATABASE: spug
      MYSQL_USER: spug
      MYSQL_PASSWORD: ${SPUG_DB_PASSWORD:?请设置数据库密码}
      MYSQL_ROOT_PASSWORD: ${SPUG_DB_ROOT_PASSWORD:?请设置数据库管理员密码}

  spug:
    image: openspug/spug-service
    container_name: spug
    restart: unless-stopped
    volumes:
      - /data/spug/service:/data/spug
      - /data/spug/repos:/data/repos
    ports:
      - "8000:80"
    environment:
      SPUG_DOCKER_VERSION: v3.2.1
      MYSQL_DATABASE: spug
      MYSQL_USER: spug
      MYSQL_PASSWORD: ${SPUG_DB_PASSWORD:?请设置数据库密码}
      MYSQL_HOST: db
      MYSQL_PORT: "3306"
    depends_on:
      - db
```

保存为 `compose.yaml` 后，先执行 `docker compose config` 检查插值与语法，再执行 `docker compose up -d`。`depends_on` 仅控制启动顺序，不保证数据库已可接受连接；若应用首次启动失败，先检查 `docker compose logs db spug`。

应用启动后，按所用版本文档初始化管理员账号，例如 `docker exec spug init_spug admin '<强密码>'`，然后访问 `http://localhost:8000`。生产部署还需考虑 HTTPS、访问控制、备份和镜像版本升级。若所用版本明确要求额外容器权限，再针对该功能评估，而非默认启用 `privileged: true`。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/22-deploying-wordpress.html' | relative_url }}">← 上一篇：部署 WordPress</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/24-building-and-deploying-tomcat.html' | relative_url }}">下一篇：构建与部署 Tomcat →</a>
</nav>
