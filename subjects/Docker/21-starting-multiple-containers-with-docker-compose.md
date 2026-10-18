---
layout: default
title: "Docker 容器技术 · 从 docker compose 启动多个容器"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 21 从 docker compose 启动多个容器
### 5.4 从 docker compose 启动多个容器

本例在一个 Compose 项目中启动 Nginx 和两个 Apache HTTP Server 服务，分别验证卷挂载和端口发布。和单容器示例相比，关键变化是 `services` 下有多个同级服务，而不是把几个服务名连续写在文件顶层。

### 1. 准备页面与配置

```bash
mkdir -p ~/compose-multi/site
printf 'Compose 多服务示例\n' > ~/compose-multi/site/index.html
cd ~/compose-multi
```

将下面内容保存为 `compose.yaml`：

```yaml
services:
  web:
    image: nginx:alpine
    volumes:
      - ./site:/usr/share/nginx/html:ro
    ports:
      - "8080:80"

  app1:
    image: httpd:alpine
    ports:
      - "8081:80"

  app2:
    image: httpd:alpine
    ports:
      - "8082:80"
```

宿主机的 `./site` 覆盖了 Nginx 镜像内相应目录的可见内容，因此访问首页会看到本地创建的文字。`:ro` 让容器只读挂载该目录。`8081:80` 与 `8082:80` 分别发布两个服务；同一项目的服务也可通过服务名在默认网络内互相访问，无需旧式 `links`。

### 2. 启动并检查

```bash
docker compose config
docker compose up -d
docker compose ps
curl http://127.0.0.1:8080/
curl -I http://127.0.0.1:8081/
curl -I http://127.0.0.1:8082/
```

第一条请求应返回本地页面；后两条请求应返回 HTTP 响应头。若有端口占用，修改左侧的宿主机端口后重新执行 `docker compose up -d`。完成演示后执行 `docker compose down`；`./site` 是宿主机目录，不会因此被删除。

### 3. 同一服务扩容

前面的 `web`、`app1`、`app2` 都绑定了固定宿主机端口；直接把它们扩成多个副本会发生端口冲突。另建一个不指定 `container_name`、不发布固定宿主机端口的 `compose.scale.yaml`：

```yaml
services:
  worker:
    image: nginx:alpine
```

```bash
docker compose -p compose-scale-demo -f compose.scale.yaml up -d --scale worker=3
docker compose -p compose-scale-demo -f compose.scale.yaml ps
docker compose -p compose-scale-demo -f compose.scale.yaml up -d --scale worker=1
docker compose -p compose-scale-demo -f compose.scale.yaml down
```

这样演示的是创建三个同类容器，而不是自动获得负载均衡入口。若需要从宿主机对多个副本提供统一访问，还须配置反向代理、负载均衡器或其他发布机制。旧版 `docker-compose scale` 命令已被 `up --scale` 取代，不应与固定端口映射一起照抄。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/20-starting-a-single-container-with-docker-compose.html' | relative_url }}">← 上一篇：从 docker compose 启动单个容器</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/22-deploying-wordpress.html' | relative_url }}">下一篇：使用 Compose 部署 WordPress →</a>
</nav>
