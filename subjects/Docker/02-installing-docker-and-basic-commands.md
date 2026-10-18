---
layout: default
title: "Docker 容器技术 · Docker 安装及基础命令介绍"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Docker 目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 02 Docker 安装及基础命令介绍

安装 Docker 的目标不仅是让 `docker --version` 有输出，还要确认守护进程正常、镜像能拉取、容器能启动，且理解镜像与容器数据保存在哪儿。下文按“选版本 → 安装 → 验证 → 配置 → 排障”的顺序展开。原笔记保留了 Docker 17.x、CentOS 7/8 和早期静态安装的大量终端记录；它们有历史参考价值，但不应当作当前发行版的一键安装命令。

## 2.1 版本与安装方式

Docker Engine 由 `dockerd` 守护进程、`docker` CLI、`containerd` 及相关组件组成。Docker CE、EE 与 Moby 的名称沿革用于理解旧文档即可；选择版本时应看当前发行版是否受支持，以及 [Docker 官方安装文档](https://docs.docker.com/engine/install/) 中该发行版的包名和依赖。**Kubernetes 1.24 起不再内置 dockershim**，新集群通常选 containerd 或 CRI-O 作为 CRI 运行时，不能仅按旧的“Kubernetes 对 Docker 版本要求”安装 Docker Engine。

优先通过发行版对应的官方 Docker 软件仓库安装，便于更新。仅在离线或受限环境下使用静态二进制包；不要把官方便利脚本直接用于需要版本锁定和审计的生产主机。旧版 CentOS 7/8 已结束常规维护，新增部署优先选择仍受支持的发行版。

## 2.2 Ubuntu/Debian：软件包安装

以下是 Ubuntu 的官方仓库流程；Debian 应改用其对应的发行版路径和仓库。安装前如有冲突的发行版自带 `docker.io`、`podman-docker` 等包，先按官方文档检查与移除；**卸载包并不等于删除 `/var/lib/docker` 中的数据**。

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
printf 'Types: deb\nURIs: https://download.docker.com/linux/ubuntu\nSuites: %s\nComponents: stable\nSigned-By: /etc/apt/keyrings/docker.asc\n' \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" | \
  sudo tee /etc/apt/sources.list.d/docker.sources >/dev/null
sudo apt-get update
apt-cache policy docker-ce
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

若要固定特定版本，先用 `apt-cache madison docker-ce` 查可用版本，再同时指定 `docker-ce` 与 `docker-ce-cli` 的对应版本；不要混装旧文档中的 `17.03` 与当前插件包。不同发行版或版本的仓库 URL、包名可能不同，执行前以官方页面核对。

## 2.3 RHEL 系：仓库安装

在当前受支持的 RHEL 兼容发行版上，先确认 Docker 官方支持矩阵，再加入对应仓库。以 CentOS 系命令形式说明：

```bash
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf list docker-ce --showduplicates
sudo dnf install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

RHEL、Rocky Linux、AlmaLinux 与 CentOS Stream 的仓库适用性并非完全相同，应按实际系统确认。Podman 是另一套容器工具，`podman-docker` 只是 CLI 兼容入口，不表示安装了 Docker daemon。不要因为 CentOS 8 曾推广 Podman，就推断所有 `docker` 命令均完全兼容。

## 2.4 离线二进制安装与自动化边界

离线环境可以从 [官方静态包目录](https://download.docker.com/linux/static/stable/) 下载匹配架构与版本的包，**同时核对校验值**，再在目标机器解压安装 `dockerd`、`docker` 等文件。相比包安装，还要自行维护 `containerd`、systemd unit、升级和卸载步骤，不能只复制一个 `docker` 可执行文件。离线包安装前先检查内核、cgroups、iptables/nftables、存储驱动与目录空间。

旧文档中跨 Ubuntu/CentOS 的“一键脚本”包含固定版本、替换镜像源和环境假设，不宜跨系统直接执行。若要自动化，应把仓库、版本、服务启动、验证和回滚分别写成可检查步骤，在同版测试机验证后部署。

## 2.5 验证安装和常用命令

```bash
docker version              # CLI 与 Server 两部分都应返回版本
docker info                 # 查看运行时、存储驱动、数据目录等
docker run --rm hello-world # 验证拉取、创建与运行链路
docker --help
docker image --help
docker container --help
systemctl status docker
```

只有 Client 而没有 Server 信息，通常说明 `dockerd` 未运行、当前用户无权访问 socket，或 CLI 指向了错误的 Docker context。`docker version` 与 `docker info` 比单看 `docker --version` 更能证明安装完整。命令的对象形式如 `docker image ls`、`docker container ls` 更便于理解；下一章分别展开镜像和容器操作。

默认 Docker socket 的访问权限等同于很高的宿主机操作权限。需要免 `sudo` 时可以把可信用户加入 `docker` 组，但这不是普通的“只读便利权限”，应按主机安全要求管理。

## 2.6 文件位置、网络与存储驱动

包安装通常将 daemon 配置放在 `/etc/docker/daemon.json`，数据根目录默认在 `/var/lib/docker`。systemd unit 可用 `systemctl cat docker` 查看；修改启动选项宜用 drop-in，而不是直接编辑包管理器提供的 unit。`docker info` 中的 `Docker Root Dir`、`Storage Driver` 比猜测目录更可靠。

默认 bridge 网络通常创建 `docker0`，但其地址不保证总是 `172.17.0.1`；可用 `docker network inspect bridge` 查看实际网段。镜像只读层与容器可写层由存储驱动管理，常见 Linux 环境使用 `overlay2`，依赖底层文件系统特性。AUFS、devicemapper 属于旧环境背景，不能把旧版迁移命令直接用于新主机。**改动存储驱动或 `data-root` 可能让原镜像/容器在新配置下不可见**，先备份、停服务，再按官方迁移步骤操作。容器内需要持久保存的业务数据优先放卷，而不是依赖可写层。

配置示例 `/etc/docker/daemon.json`：

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

先用 `dockerd --validate --config-file=/etc/docker/daemon.json`（若当前版本支持）验证，再 `sudo systemctl restart docker`、`docker info` 确认。日志选项主要影响**新建容器**；已有容器需重建才会采用新的日志配置。`daemon.json` 的键值不要与 systemd 启动参数重复定义，否则 daemon 可能无法启动。

## 2.7 代理与远程访问

拉取镜像需要代理时，给 `docker.service` 配置 systemd drop-in 的 `HTTP_PROXY`、`HTTPS_PROXY`、`NO_PROXY`，然后 `daemon-reload` 并重启。容器内应用的网络代理是另一层配置，不能与 daemon 拉取镜像的代理混为一谈。若使用私有仓库，优先正确配置可信 CA；不要将其一概加入不安全仓库列表。

**不要直接开放未加密、无认证的 Docker TCP 端口**，它几乎相当于向远端提供宿主机控制权。临时跨机操作可使用 `docker context create` 的 `ssh://USER@HOST` 端点；需要长期 API 访问时，应配置双向 TLS、网络限制与访问审计。修改远程配置前保留本地 socket 和回滚方式。

安装后的排查顺序：先看 `systemctl status docker` 和 `journalctl -u docker`，再核对 `docker version` 的 Server、`docker info` 的存储/代理配置，最后运行一次 `hello-world`。这样比看到镜像拉取失败就重装 Docker 更容易定位原因。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/01-introduction-to-docker.html' | relative_url }}">← 上一章：Docker 简介</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 目录</a>
  <a href="{{ '/subjects/Docker/03-managing-container-images.html' | relative_url }}">下一章：容器镜像管理 →</a>
</nav>
