---
layout: default
title: "Docker 容器技术 · 实战案例：RuoYI 微服务项目"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 25 实战案例：RuoYI 微服务项目
### 5.8 实战案例：RuoYI 微服务项目

下面的 Compose 配置沿用 RuoYI-Cloud 项目示例的服务拆分：MySQL、Redis、Nacos、网关、认证、业务模块及 Nginx。原始资料中的 YAML 缩进和跨行卷路径已损坏，不能直接执行；以下按服务层级重排。它仍依赖相应的 `./nacos`、`./mysql`、`./ruoyi` 等构建目录，使用前应以[上游项目的 Compose 文件](https://gitee.com/y_project/RuoYi-Cloud/blob/master/docker/docker-compose.yml)和实际版本为准。

先将 `RUOYI_MYSQL_ROOT_PASSWORD` 写入本地 `.env`，并检查映射目录、端口占用及数据库初始化文件。示例中 Nacos 采用单机模式，仅用于演示；对外开放 MySQL、Redis 和管理端口时应另行设置访问控制。

```yaml
services:
  ruoyi-mysql:
    container_name: ruoyi-mysql
    build: ./mysql
    image: mysql:5.7
    ports:
      - "3306:3306"
    volumes:
      - ./mysql/conf:/etc/mysql/conf.d
      - ./mysql/logs:/logs
      - ./mysql/data:/var/lib/mysql
    command:
      - mysqld
      - --innodb-buffer-pool-size=80M
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --default-time-zone=+8:00
      - --lower-case-table-names=1
    environment:
      MYSQL_DATABASE: ry-cloud
      MYSQL_ROOT_PASSWORD: ${RUOYI_MYSQL_ROOT_PASSWORD:?请设置数据库密码}

  ruoyi-redis:
    container_name: ruoyi-redis
    build: ./redis
    image: redis
    ports:
      - "6379:6379"
    volumes:
      - ./redis/conf/redis.conf:/home/ruoyi/redis/redis.conf
      - ./redis/data:/data
    command: redis-server /home/ruoyi/redis/redis.conf

  ruoyi-nacos:
    container_name: ruoyi-nacos
    build: ./nacos
    image: nacos/nacos-server
    environment:
      MODE: standalone
    volumes:
      - ./nacos/logs:/home/nacos/logs
      - ./nacos/conf/application.properties:/home/nacos/conf/application.properties
    ports:
      - "8848:8848"
      - "9848:9848"
      - "9849:9849"
    depends_on:
      - ruoyi-mysql

  ruoyi-gateway:
    container_name: ruoyi-gateway
    build:
      context: ./ruoyi/gateway
      dockerfile: dockerfile
    ports:
      - "8080:8080"
    depends_on:
      - ruoyi-redis
      - ruoyi-nacos

  ruoyi-auth:
    container_name: ruoyi-auth
    build:
      context: ./ruoyi/auth
      dockerfile: dockerfile
    ports:
      - "9200:9200"
    depends_on:
      - ruoyi-redis
      - ruoyi-nacos

  ruoyi-modules-system:
    container_name: ruoyi-modules-system
    build:
      context: ./ruoyi/modules/system
      dockerfile: dockerfile
    ports:
      - "9201:9201"
    depends_on:
      - ruoyi-redis
      - ruoyi-mysql

  ruoyi-modules-gen:
    container_name: ruoyi-modules-gen
    build:
      context: ./ruoyi/modules/gen
      dockerfile: dockerfile
    ports:
      - "9202:9202"
    depends_on:
      - ruoyi-mysql

  ruoyi-modules-job:
    container_name: ruoyi-modules-job
    build:
      context: ./ruoyi/modules/job
      dockerfile: dockerfile
    ports:
      - "9203:9203"
    depends_on:
      - ruoyi-mysql

  ruoyi-modules-file:
    container_name: ruoyi-modules-file
    build:
      context: ./ruoyi/modules/file
      dockerfile: dockerfile
    ports:
      - "9300:9300"
    volumes:
      - ./ruoyi/uploadPath:/home/ruoyi/uploadPath

  ruoyi-visual-monitor:
    container_name: ruoyi-visual-monitor
    build:
      context: ./ruoyi/visual/monitor
      dockerfile: dockerfile
    ports:
      - "9100:9100"

  ruoyi-nginx:
    container_name: ruoyi-nginx
    build: ./nginx
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/html/dist:/home/ruoyi/projects/ruoyi-ui
      - ./nginx/conf/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/logs:/var/log/nginx
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - ruoyi-gateway
```

保存为 `compose.yaml` 后，先执行 `docker compose config` 校验，再执行 `docker compose build` 和 `docker compose up -d`。`depends_on` 仅保证启动顺序，不保证 MySQL、Redis 或 Nacos 已就绪；若业务服务启动失败，应查看相应服务日志及上游项目的初始化要求。这里保留了示例项目的 MySQL 5.7 约束，升级数据库前须验证应用兼容性。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/24-building-and-deploying-tomcat.html' | relative_url }}">← 上一篇：构建与部署 Tomcat</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/26-converting-between-docker-run-and-compose.html' | relative_url }}">下一篇：docker run 与 Compose 转换 →</a>
</nav>
