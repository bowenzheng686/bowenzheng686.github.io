---
layout: default
title: "JumpServer 堡垒机 · Docker Compose 部署"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 09 Docker Compose 部署

上一篇用 docker run 分别说明网络、环境变量和数据卷。本篇用 Compose 把这些关系放进一份 YAML 文件。原资料的两段 Compose 示例失去了 YAML 缩进，且把 v4.1.0 与 v4.10.7、不同数据库与镜像来源混在一起；照抄会导致解析错误或组件版本不一致。因此先选定一个 JumpServer 版本，再以该版本的[官方 Compose 文件](https://github.com/jumpserver/Dockerfile/tree/master/allinone)为准。本页着重说明配置结构与检查方法。

## 服务如何配合

示例包含三个服务：MariaDB 保存平台数据库，Redis 提供缓存或任务状态，JumpServer 提供 Web 与 SSH 接入。它们处于同一 Compose 网络，JumpServer 在配置中使用 db、redis 这两个**服务名**，不依赖容器临时 IP。三个数据卷分别对应数据库、Redis 和 JumpServer 数据，容器重建时不能随意删除。

下面是整理后的结构示例；使用前把镜像和卷内路径与选定版本文档核对，并在本地准备不提交到 Git 的 .env 文件：

~~~dotenv
VERSION=v4.1.0
DB_ROOT_PASSWORD=REPLACE_WITH_RANDOM_ROOT_PASSWORD
DB_PASSWORD=REPLACE_WITH_RANDOM_DB_PASSWORD
REDIS_PASSWORD=REPLACE_WITH_RANDOM_REDIS_PASSWORD
SECRET_KEY=REPLACE_WITH_UNIQUE_RANDOM_SECRET
BOOTSTRAP_TOKEN=REPLACE_WITH_ANOTHER_RANDOM_TOKEN
~~~

~~~yaml
services:
  db:
    image: mariadb:10.6
    restart: unless-stopped
    environment:
      MARIADB_ROOT_PASSWORD: $DB_ROOT_PASSWORD
      MARIADB_DATABASE: jumpserver
      MARIADB_USER: jumpserver
      MARIADB_PASSWORD: $DB_PASSWORD
    volumes:
      - dbdata:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mariadb-admin ping -h 127.0.0.1 -u root -p$$MARIADB_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.0
    restart: unless-stopped
    command: ["redis-server", "--requirepass", "$REDIS_PASSWORD", "--appendonly", "yes"]
    environment:
      REDIS_PASSWORD: $REDIS_PASSWORD
    volumes:
      - redisdata:/data
    healthcheck:
      test: ["CMD-SHELL", "REDISCLI_AUTH=$$REDIS_PASSWORD redis-cli ping | grep PONG"]
      interval: 10s
      timeout: 5s
      retries: 5

  jumpserver:
    image: jumpserver/jms_all:$VERSION
    restart: unless-stopped
    environment:
      SECRET_KEY: $SECRET_KEY
      BOOTSTRAP_TOKEN: $BOOTSTRAP_TOKEN
      DB_ENGINE: mysql
      DB_HOST: db
      DB_PORT: "3306"
      DB_USER: jumpserver
      DB_PASSWORD: $DB_PASSWORD
      DB_NAME: jumpserver
      REDIS_HOST: redis
      REDIS_PORT: "6379"
      REDIS_PASSWORD: $REDIS_PASSWORD
    ports:
      - "8080:80"
      - "2222:2222"
    volumes:
      - jsdata:/opt/data
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  dbdata:
  redisdata:
  jsdata:
~~~

这不是声称所有 JumpServer 版本都能直接使用的生产配置。特别是 MariaDB／Redis 版本、DB_ENGINE 是否必填、镜像内数据目录及健康检查接口，均应跟所选版本逐项核对。Compose 文件中的环境变量也可能通过容器检查接口被看到；生产环境有密钥管理平台时，应采用其 Secret 机制。

## 启动前检查

先校验 YAML 展开结果，再启动和观察状态：

~~~bash
docker compose config --quiet
docker compose up -d
docker compose ps
docker compose logs --tail 100 jumpserver
~~~

如果 config 命令失败，先检查缩进、空变量和拼错的服务名；若 db 或 redis 始终不健康，先检查各自日志，不要直接排查 Web 页面。depends_on 的健康条件只表示依赖服务通过其健康检查，不代表数据库初始化或 JumpServer 迁移一定成功。

浏览器访问宿主机 8080 端口时，还要完成登录、资产连接与审计录像验证。停止服务可用 docker compose down；**不要随手加 --volumes**，否则上面三个命名卷可能一起删除。升级前备份数据库和审计数据，再按目标版本迁移说明调整镜像和配置，而不是盲目使用 latest。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/08-docker-deployment.html' | relative_url }}">← 上一篇：Docker 部署</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">返回 JumpServer 专题目录</a>
  <a href="{{ '/subjects/JumpServer/10-installing-with-the-official-script.html' | relative_url }}">下一篇：官方脚本安装 →</a>
</nav>