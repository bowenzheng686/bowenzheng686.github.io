---
layout: default
title: "Docker 容器技术 · 基于CRIU实现容器热迁移（了解）"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 07 基于CRIU实现容器热迁移（了解）
### 1.7 基于CRIU实现容器热迁移（了解）

## 1.7 CRIU 检查点与容器恢复

[Docker checkpoint 文档](https://docs.docker.com/reference/cli/docker/checkpoint/)和 [CRIU 项目](https://criu.org/Main_Page)介绍了把运行中进程状态保存为检查点、之后恢复执行的机制。它与“完全不中断的热迁移”不是同一概念：创建检查点通常会使容器停止，复制与恢复期间也有停机时间。是否能迁移跨主机网络连接、卷和外部依赖，取决于环境兼容性，不能仅靠复制一个目录保证业务无感。

### 检查点保存什么、没保存什么

CRIU（Checkpoint/Restore In Userspace）记录进程内存、文件描述符及部分命名空间状态等。Docker 提供 `docker checkpoint create`、`ls`、`rm`，并用 `docker start --checkpoint` 恢复。容器的镜像、创建参数、持久卷及外部数据库并不会因为有检查点就自动复制到另一台主机。

创建检查点前，需要在目标系统上安装与内核兼容的 CRIU，执行 `criu check`，并确认 Docker Engine 支持 checkpoint。某些版本要求 Docker 守护进程开启 `experimental`；如果需要在 `/etc/docker/daemon.json` 中加入 `"experimental": true`，应与原有 JSON 配置合并，不要直接覆盖文件或在末尾追加第二个 JSON 对象。修改守护进程配置后先检查语法，再按维护窗口重启 Docker。

### 同主机演示：保存与恢复计数进程

这个无外部依赖的 BusyBox 容器便于观察进程状态。请在测试主机执行，镜像标签和路径按本机情况调整：

```bash
docker run -d --name cr-test busybox:1.36 sh -c \
  'i=0; while true; do echo "$i"; i=$((i+1)); sleep 1; done'
docker logs --tail=3 cr-test

mkdir -p /srv/cr-checkpoints
docker checkpoint create --checkpoint-dir /srv/cr-checkpoints cr-test checkpoint1
docker checkpoint ls --checkpoint-dir /srv/cr-checkpoints cr-test
docker ps -a --filter name=cr-test

docker start --checkpoint checkpoint1 \
  --checkpoint-dir /srv/cr-checkpoints cr-test
docker logs --tail=5 cr-test
```

`create` 默认停止容器，恢复后计数应接着检查点附近的值继续，而不是从零重新运行。`--leave-running` 能让原容器在生成检查点后继续运行，但若又恢复出第二个具有相同外部身份的实例，可能造成重复写入；不能将它当作无风险高可用方案。

### 跨主机迁移前必须核对

1. 目标主机的内核、CPU 架构、CRIU 与 Docker 版本能否恢复该检查点；先用最小容器做兼容性验证。
2. 目标容器由相同镜像与兼容的创建参数构建，相关卷、文件、密钥和外部服务已准备好。不要直接修改 Docker 内部 `/var/lib/docker/containers/`，其布局不是稳定的迁移 API。
3. 检查点文件通过受控渠道复制到目标主机；其中可能包含进程内存里的凭据，应限制访问并在完成后清理。
4. 预先设计 IP、端口和服务发现切换，以及停机、回滚、数据一致性方案。保持打开的网络连接并不保证可以在新主机继续工作。

因此，这一节应理解为 CRIU 原理与实验，而不是无需停机的生产迁移操作手册。大多数无状态服务更适合通过编排系统在新主机重新启动，再由负载均衡完成流量切换。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/06-docker-run-parameters.html' | relative_url }}">← 上一篇：查看 docker run 启动参数命令</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/08-docker-image-fundamentals.html' | relative_url }}">下一篇：Docker 镜像说明 →</a>
</nav>
