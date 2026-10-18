---
layout: default
title: "Docker 容器技术 · 从 docker compose 启动单个容器"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 20 从 docker compose 启动单个容器
### 5.3 从 docker compose 启动单个容器

本例沿用上一章的 Compose V2 插件，用一个 Nginx 容器演示配置、启动、验证与清理。先确认 `docker compose version` 正常，且宿主机 8080 端口未被占用。

### 1. 编写配置

在空目录中创建 `compose.yaml`：

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    restart: unless-stopped
```

`web` 是服务名；`8080:80` 把宿主机 8080 端口发布到容器 80 端口。镜像标签仅用于示例，正式部署应选择经过验证的具体版本。单个服务在其默认网络内无需额外声明 `expose` 才能被同项目的其他服务访问。

### 2. 检查并启动

```bash
cd ~/compose-demo
docker compose config
docker compose up -d
docker compose ps
curl -I http://127.0.0.1:8080/
```

`config` 若报告 YAML 格式错误，先检查 `services:`、`web:` 的冒号及缩进。`up -d` 在后台运行；不带 `-d` 时命令会附着到日志输出，按 `Ctrl+C` 会停止本次前台启动的容器。若拉取镜像失败，先检查网络、镜像名与镜像仓库访问权限，不要把连接失败直接归因于 Docker 的 TLS 设置。

### 3. 查看状态与排障

```bash
docker compose ps
docker compose logs --tail=50 web
docker compose exec web nginx -t
docker compose images
```

`docker compose` 默认在项目目录寻找配置文件；从其他目录操作时可加 `-f /完整路径/compose.yaml`。`docker compose exec` 使用**服务名** `web`，不是随机生成的容器名。需要交互 shell 时可用 `docker compose exec web sh`。

### 4. 停止、重启与清理

| 操作 | 命令 | 结果 |
| --- | --- | --- |
| 临时停止 | `docker compose stop` | 保留容器，之后可 `start`。 |
| 再次启动 | `docker compose start` | 启动已创建的容器。 |
| 重启服务 | `docker compose restart web` | 重新启动现有容器；修改配置后通常应使用 `up -d` 以重建。 |
| 删除项目容器 | `docker compose down` | 删除容器及项目网络；默认保留镜像和命名卷。 |

`docker compose kill` 会强制终止进程，正常关闭应优先使用 `stop` 或 `down`。如需同时删除命名卷，必须明确执行 `docker compose down -v`，执行前确认卷内数据可丢弃。前面的原始示例把 `down` 说成“也会自动删除镜像”，这一点不正确。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/19-installation-and-preparation.html' | relative_url }}">← 上一篇：安装和准备</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/21-starting-multiple-containers-with-docker-compose.html' | relative_url }}">下一篇：从 docker compose 启动多个容器 →</a>
</nav>
