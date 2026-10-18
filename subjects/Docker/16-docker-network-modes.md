---
layout: default
title: "Docker 容器技术 · Docker 网络连接模式"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Docker 目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 16 Docker 网络连接模式

容器通常拥有自己的网络命名空间，Docker 用网络驱动把容器连接起来。本章先比较 `bridge`、`host`、`none` 和 `container` 共享网络，再解释自定义 bridge、DNS 名称、网络隔离以及跨网络连接。原笔记把“自定义网络”列作与这些模式并列的第五种模式；更准确地说，它通常是**用户创建的 bridge 网络**，也可以由其他网络驱动实现。

## 16.1 先看网络和接口

```bash
docker network ls
docker network inspect bridge
docker info --format '{{json .DriverStatus}}'
```

运行容器时可用 `--network NAME` 选择网络，省略时通常接入默认 bridge。不要假定默认网段永远是 `172.17.0.0/16`，应查看当前网络配置，并避免与宿主机、VPN、云 VPC 网段冲突。容器是否能访问外部网络还受主机转发、防火墙、NAT、代理和 DNS 影响；不能只凭 `docker network inspect` 判断所有链路都通。

| 模式 | 网络命名空间 | 常见用途 | 关键约束 |
| --- | --- | --- | --- |
| 默认/自定义 `bridge` | 每个容器独立 | 单机服务网络 | 对外访问服务需发布端口；自定义网络有容器名 DNS |
| `host` | 与宿主机共享 | 需要直接使用宿主网络的 Linux 服务 | 端口可能冲突，`-p` 发布规则不生效 |
| `none` | 独立但无 Docker 配置的外部接口 | 强隔离或自行配置网络 | 默认不能访问外部；仍有回环接口 |
| `container:NAME` | 与指定容器共享 | sidecar 式网络共享 | 两容器共享 IP、端口空间和 localhost |

## 16.2 Bridge：默认网络与自定义网络

默认 bridge 为容器分配内部地址，容器访问外部通常经主机转发/NAT；外部访问容器服务需 `-p` 发布端口。自定义 bridge 在此基础上提供更方便的容器名/别名解析和网络分组，应优先用于同一应用的多容器通信。**默认 bridge 上不要依赖旧式 `--link` 做服务发现**。

```bash
docker network create --driver bridge --subnet 172.28.10.0/24 app-net
docker run -d --name web --network app-net -p 127.0.0.1:8080:80 nginx:1.27
docker run --rm --network app-net alpine:3.20 nslookup web
docker network inspect app-net
```

自定义网段必须避开已有路由；只需要名称解析时可省略 `--subnet` 让 Docker 分配。第二个容器可以通过 `web:80` 访问服务，**不需要**经宿主机的 `8080` 端口。`-p 127.0.0.1:8080:80` 是给宿主本机提供的入口，不等于容器间通信配置。需要名称别名可在创建时用 `--network-alias`；一个容器可加入多个用户定义网络。

```bash
docker network create backend
docker network connect backend web
docker network inspect backend
docker network disconnect backend web
```

`network connect` 是解决单机不同用户网络之间特定容器通信的清晰方式：让容器同时接入两个网络，再由应用按可解析名称连接。原笔记中直接修改 Docker 管理的 iptables 规则不仅脆弱，还会绕过网络隔离设计；重启 Docker 后规则也可能变化，不宜作为应用连接方案。默认 bridge 与用户定义网络的隔离、可达性应以当前 daemon、防火墙规则及实际连通测试为准，不能概括成“所有不同网络一定互不通信”。

修改默认 bridge 网段可在维护窗口调整 daemon 配置，例如：

```json
{
  "bip": "172.29.0.1/24"
}
```

不要同时让 `bip` 与另一套相冲突的 bridge 选项控制同一网桥；先确认现有容器、网络和路由的影响，备份 `/etc/docker/daemon.json`，验证 JSON 后重启 daemon，并再次检查 `docker network inspect bridge`。生产系统改网段可能影响正在运行的容器通信，应规划回滚。

## 16.3 Host、None 与共享容器网络

```bash
docker run --rm --network host nginx:1.27
docker run --rm --network none alpine:3.20 ip addr
docker run -d --name net-base --network app-net alpine:3.20 sleep 3600
docker run --rm --network container:net-base alpine:3.20 ip addr
```

`host` 在 Linux 上直接使用宿主机网络命名空间，容器服务监听的端口就是主机端口；此时 `-p`/`-P` 不会产生额外映射。它不意味着文件系统和 PID 命名空间也共享。不同平台的 Docker Desktop 对 host 网络的支持与 Linux 原生主机可能不同，应核对当前版本。

`none` 不给容器配置可对外通信的网络接口，仍可见回环接口；适合不需要网络的批处理或需要自行配置网络的场景。`container:net-base` 让两个容器共享网络命名空间，`127.0.0.1` 可用于它们之间通信，但两个进程不能占用相同监听端口。共享网络不代表共享文件系统；运行时参数的端口发布应放在拥有该网络命名空间的基础容器上。基础容器停止或重建时，依赖它的容器网络也要重新检查。

## 16.4 用例：WordPress 与 Redis Cluster

WordPress + MySQL 在一个自定义网络中，WordPress 的数据库主机名可写成 MySQL 容器的服务名，而不必依赖固定 IP 或旧式 `--link`。数据库端口不需要发布到宿主机；只发布 Web 入口。业务数据要单独挂载卷，密码等配置不要写在可公开的命令记录里。多服务长期运行更适合使用下一部分的 Compose：网络、卷和服务名可一起声明。

Redis Cluster 的六节点实验更复杂：除了容器间数据端口，还要考虑 cluster bus 端口、节点对外通告地址和客户端连接路径。单机自定义 bridge 能演示分片与故障转移流程，但**不能证明跨主机可达性或真正的故障域高可用**。先确认每个节点地址与通告地址、容器名解析及防火墙，再创建集群并测试 `CLUSTER NODES`；切忌把旧脚本中的固定地址、密码直接复制到生产部署。跨主机通信另见下一章。

## 16.5 排查顺序

1. `docker network inspect NETWORK`：确认容器是否在预期网络，地址、网关是否冲突。
2. 在容器内测试名称解析与目标端口；DNS 成功不代表应用正在监听。
3. 区分“容器到容器地址”与“宿主机发布端口”，检查应用监听地址是否为 `127.0.0.1` 或 `0.0.0.0`。
4. 再检查主机路由、firewall/nftables/iptables、`ip_forward` 与云安全组；不要第一步就手改 Docker 创建的规则。

这样可以从命名空间、名称解析、端口监听、主机转发逐层定位，而不是把所有连接失败都归咎于 Docker bridge。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/15-container-name-networking.html' | relative_url }}">← 上一章：容器名称通信</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 目录</a>
  <a href="{{ '/subjects/Docker/17-cross-host-container-networking.html' | relative_url }}">下一章：跨宿主机容器网络 →</a>
</nav>
