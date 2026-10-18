---
layout: default
title: "Docker 容器技术 · 默认网桥与容器通信"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 14 默认网桥与容器通信

容器网络要回答三个问题：**容器如何获得自己的网卡和地址、同一主机的容器如何互通、流量怎样到达主机外部**。本篇以 Linux 上 Docker Engine 的默认 `bridge` 网络为例；Docker Desktop、rootless 模式和其他网络驱动的实现细节可能不同。后续章节再介绍按服务组织的自定义网络与跨主机通信。

![Docker 容器网络连接示意](assets/img-cace5f8f392e04e4.webp)

## 默认网桥、网络命名空间与 veth

在常见 Linux 安装中，Docker 创建名为 `docker0` 的 Linux 网桥，默认桥接网络通常使用 `172.17.0.0/16`，网桥地址例如 `172.17.0.1`。**这些是常见默认值，不是所有主机都固定不变的地址**：实际网段取决于 daemon 配置及既有网络。用命令观察本机，而不是照抄旧教程的大段 `ip a` 输出。

```bash
docker network ls
docker network inspect bridge
ip -br addr show docker0
```

桥接模式下，容器拥有独立网络命名空间，里面通常看到 `lo` 和 `eth0`。容器 `eth0` 与宿主机上的一个 `veth` 端点成对出现，宿主机端连接到 `docker0`。把 veth 想成穿越命名空间的一根虚拟网线：容器发出的包从一端进入，在另一端到达网桥。网桥负责本机同一二层网络内的转发；容器访问外部网络时，Docker 还会配置转发与地址转换规则。

```bash
docker run -d --name net-a alpine:3.20 sleep 3600
docker exec net-a ip -br addr
ip -br link show master docker0
docker inspect net-a --format '{{json .NetworkSettings.Networks}}'
```

容器内 `eth0@ifN` 的 `N` 可用于追踪宿主机侧的对应接口编号；`ip -br link show master docker0` 则列出接到网桥的接口。veth 名称和容器 IP 均会随创建、重建而变化，不适合作为长期配置项。

## 两个容器如何通信

再创建第二个容器，观察它也得到一个地址和一端 veth。在**默认 bridge 网络**上，两个容器通常能用 IP 互通，但不会像自定义 bridge 那样自动按容器名做 DNS 解析。因此原资料中“能 ping 对方 IP，却不能解析对方名称”并不矛盾。

```bash
docker run -d --name net-b alpine:3.20 sleep 3600
docker inspect net-a --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker inspect net-b --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
NET_B_IP=$(docker inspect net-b --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
docker exec net-a ping -c 1 "$NET_B_IP"
docker exec net-a ping -c 1 net-b
```

最后一条在默认 bridge 上可能得到 `bad address`。如果应用需要稳定的服务名，创建用户自定义 bridge，把两个容器加入同一网络：

```bash
docker network create app-net
docker network connect app-net net-a
docker network connect app-net net-b
docker exec net-a ping -c 1 net-b
```

连接自定义网络后，Docker 的内置 DNS 才能按服务或容器名解析该网络中的成员。一个容器可能同时连到多个网络，因此排查时需看它所在的**具体网络**，不能只看全局容器列表。

## 主机端口、跨主机与隔离

`-p 8080:80` 是把宿主机端口发布到容器端口，不等于把容器私有 IP 暴露给另一台主机。两台宿主机可能都用 `172.17.0.2` 分配给本地容器，所以跨主机不能直接依赖这些默认 bridge IP；通常通过宿主机地址加发布端口访问，或采用专门的跨主机网络方案。

默认 bridge 中的容器一般允许相互访问。原教程通过在 Docker 的系统 service 文件里加 `--icc=false` 演示全局禁止容器间通信，但该做法影响范围广，也容易与发行版升级及现有 daemon 参数冲突。更可控的做法是**按应用创建独立网络，只让需要互通的容器加入同一网络**，再结合应用鉴权和主机防火墙。网络隔离不应被当成唯一访问控制；若服务发布了主机端口，其他网络中的客户端仍可能通过主机地址访问它。

```bash
docker network create app-a
docker network create app-b
docker run -d --name service-a --network app-a alpine:3.20 sleep 3600
docker run -d --name service-b --network app-b alpine:3.20 sleep 3600
docker network inspect app-a
docker network inspect app-b
```

## 地址冲突与自定义网段

当默认 `docker0` 网段与企业 VPN 或局域网重叠时，路由可能把流量送往错误方向。先检查实际路由和其他 Docker 网络的网段；只改 `docker0` 并不能自动修复所有已存在的用户自定义网络。

如确需修改默认网桥地址，可在 `/etc/docker/daemon.json` 的**现有 JSON 中合并** `bip` 字段，例如：

```json
{
  "bip": "192.168.100.1/24"
}
```

修改前确认 `192.168.100.0/24` 与宿主机、VPN 和其他容器网络都不冲突，安排维护窗口并记录原配置。重启 Docker 可能中断现有工作负载；重启后用 `docker network inspect bridge` 和 `ip -br addr show docker0` 验证。不要同时在命令行参数和 `daemon.json` 中重复设置同一选项。

对于**新应用网络**，通常无须手工创建 Linux 网桥并改写 `docker.service`；直接由 Docker 管理更清晰：

```bash
docker network create --driver bridge --subnet 172.30.10.0/24 project-net
docker run -d --name project-a --network project-net alpine:3.20 sleep 3600
docker network inspect project-net
```

完成练习后删除示例容器和网络，避免留下名称冲突：`docker rm -f net-a net-b service-a service-b project-a`，再分别删除本篇创建的网络。不要删除其他项目仍在使用的网络。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/13-data-volume-containers.html' | relative_url }}">← 上一篇：数据卷容器</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/15-container-name-networking.html' | relative_url }}">下一篇：容器名称与网络访问 →</a>
</nav>
