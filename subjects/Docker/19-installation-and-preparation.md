---
layout: default
title: "Docker 容器技术 · 安装和准备"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 19 安装和准备
### 5.2 安装和准备

### 先确认 Docker Engine 与 Compose 插件

当前主要使用 **Compose V2 插件**，命令形式是 `docker compose`（中间有空格）。旧版独立工具 `docker-compose`（带连字符）属于不同的安装与发布线；原资料将二者及多个年代的输出混排，容易导致读者照抄失效命令。本专题后续示例统一使用 V2。

```bash
docker version
docker compose version
```

如果第二条命令提示没有 `compose` 子命令，应先按[Docker 官方 Linux 安装文档](https://docs.docker.com/compose/install/linux/)为当前系统安装 Compose 插件。已配置 Docker 官方软件源的 Debian/Ubuntu 系统通常可执行：

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
docker compose version
```

RPM 系发行版的软件包管理器和包名需以对应发行版文档为准。不要仅凭 Docker Engine 版本号推断插件一定存在；Engine、CLI 和 Compose 插件可以分别安装或升级。过时的 `apt-key`、Python 2 `pip` 及下载旧版 `docker-compose` 二进制文件的流程不再作为本教程推荐路径。

### 命令与项目目录

Compose 在一个项目目录中读取配置文件。当前常用文件名为 `compose.yaml`；也可通过 `-f` 明确指定其他文件。先进入项目目录，再执行以下命令：

| 命令 | 用途 |
| --- | --- |
| `docker compose config` | 解析变量并检查配置，输出规范化结果。 |
| `docker compose up -d` | 创建并在后台启动服务。 |
| `docker compose ps` | 查看本项目的容器状态。 |
| `docker compose logs -f` | 持续查看服务日志。 |
| `docker compose exec 服务名 命令` | 在运行中的服务容器内执行命令。 |
| `docker compose down` | 停止并删除本项目的容器和网络；**默认不删除镜像或命名卷**。 |

项目名通常由目录名推导，可用 `-p` 指定。`docker compose ls` 可列出 Compose 项目；`docker compose --help` 和 `docker compose COMMAND --help` 可查看当前安装版本的准确参数。

### 最小配置与格式检查

创建目录和 `compose.yaml`：

```bash
mkdir -p ~/compose-demo
cd ~/compose-demo
```

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

YAML 缩进决定层级：`web` 属于 `services`，`image` 和 `ports` 属于 `web`。先运行 `docker compose config`，再运行 `docker compose up -d`。如果出现配置文件不存在的错误，检查当前目录和文件名，而不是直接改 Docker 服务配置。

Compose V2 依照当前 [Compose Specification](https://docs.docker.com/compose/compose-file/) 解析文件，通常无需顶层 `version` 字段。旧资料的“Compose 文件格式 2.x/3.x 对应 Engine 版本”表格主要适用于历史兼容场景，不能用于判断现代 Compose V2 的可用功能。JSON 配置另见本专题第 27 篇。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/18-introduction-to-docker-compose.html' | relative_url }}">← 上一篇：Docker Compose 介绍</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/20-starting-a-single-container-with-docker-compose.html' | relative_url }}">下一篇：从 docker compose 启动单个容器 →</a>
</nav>
