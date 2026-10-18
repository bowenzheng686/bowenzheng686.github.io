---
layout: default
title: "Docker 容器技术 · 容器操作基础命令"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Docker 目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 04 容器操作基础命令

镜像是模板，容器是由模板创建的运行实例。本章沿一个容器的生命周期介绍创建、观察、交互、停止、删除，再说明端口、环境变量、DNS 与文件复制。命令中的 `web` 是示例容器名，执行时可按实际名称替换。

## 4.1 创建与运行

`docker run` 会在需要时拉取镜像、创建容器并启动其主进程；再次执行 `run` 是**新建另一个容器**，不是启动已存在的容器。先用一次性命令确认运行链路：

```bash
docker run --rm hello-world
docker run --rm -it alpine:3.20 sh
docker run -d --name web --restart unless-stopped -p 127.0.0.1:8080:80 nginx:1.27
```

`-it` 提供交互终端，`-d` 在后台运行，`--name` 指定名称，`--rm` 在主进程结束后删除容器。`--rm` 不适合需要保留停止状态用于排查的服务容器，且不能与重启策略同时使用。容器的生命周期由其主进程（PID 1）决定：主进程退出，容器就停止；`-d` 并不会让一个立即退出的命令“常驻”。不要靠 `tail -f /dev/null` 掩盖真实服务启动失败。

常见重启策略：`no` 不自动重启；`on-failure[:N]` 只在失败退出时尝试重启；`always` 在 daemon 恢复时也会重启，手动停止则在 daemon 重启后仍可能恢复；`unless-stopped` 会尊重手动停止状态。具体边界应以当前 Docker 版本验证，不能简单说“除 always 外重启主机都不会启动”。

## 4.2 查看状态与日志

```bash
docker container ls              # 运行中的容器
docker container ls -a           # 包括已停止的容器
docker container ls --filter status=exited
docker container inspect web     # 配置、网络、挂载及状态
docker container top web         # 容器中的进程
docker container stats web       # 实时资源用量，Ctrl+C 退出
docker container logs --tail 100 -f web
docker container port web
```

`logs` 读取容器主进程输出到 stdout/stderr 的内容，是否能读取和保存多久取决于日志驱动配置，不能假定日志总在 `/var/lib/docker/containers/<id>/*-json.log`。服务没有日志时，要先确认应用是否真的向标准输出写入，而不是直接查某个固定路径。`inspect` 中的 IP、挂载与状态字段比从终端输出猜测可靠。

## 4.3 停止、恢复、暂停与信号

```bash
docker stop web       # 发停止信号，等待宽限期后才强制结束
docker start web      # 启动已有容器
docker restart web    # 停止后再启动
docker pause web      # 暂停进程
docker unpause web
docker kill --signal=HUP web    # 给主进程发送指定信号
```

`docker kill` 默认发送 SIGKILL，不等同于可优雅退出的 `stop`；仅在需要立即结束或发送特定信号时使用。批量操作前用 `docker container ls` 确认对象，避免把“停止所有容器”的命令作为日常操作。停止容器不会删除它的可写层；删除容器才会删除其可写层，挂载卷则按卷生命周期管理。

## 4.4 进入容器与执行命令

```bash
docker exec -it web sh
docker exec web nginx -t
docker exec -u 0 web id
```

`exec` 在运行中的容器里启动一个**新进程**，退出该 shell 不会让原服务退出。镜像可能没有 `bash`，先用 `sh`。`attach` 接到主进程的标准流，退出交互时可能影响主进程；需要排障通常优先 `exec`。最小化镜像也可能没有 shell，此时应使用应用自身的诊断接口或专门的调试容器，而非假定可以 `exec bash`。

`--privileged` 会大幅扩大容器对宿主机设备与内核能力的访问范围，不是“让容器内 root 变成 root”的普通开关；排障和生产部署应先评估具体需要的 capability、设备映射或安全配置。`--sysctl`、`--ulimit` 也应针对具体内核参数或进程限制设置，并核对当前网络命名空间和 daemon 的支持范围。

## 4.5 环境变量与启动命令

```bash
docker run --rm -e APP_MODE=demo alpine:3.20 env
docker run --rm --env-file ./app.env alpine:3.20 env
docker run --rm alpine:3.20 echo hello
```

运行命令可覆盖镜像的 `CMD`；`ENTRYPOINT` 与 `CMD` 的组合规则见 Dockerfile 章节。环境变量适合普通配置，不适合直接在命令行明文传递数据库密码：命令记录和容器检查结果可能暴露它。密钥应根据编排环境使用专门的 Secret 管理方式。MySQL、WordPress 等镜像各自要求的变量应以对应镜像当前版本文档为准。

## 4.6 端口映射

容器处于 bridge 网络时，宿主机以外能否访问服务取决于端口发布、监听地址和防火墙。`EXPOSE` 只是镜像元数据，不会自动发布端口；`-P` 把镜像声明的端口发布到宿主机随机端口，`-p` 明确指定映射。

```bash
docker run -d --name web2 -p 8081:80 nginx:1.27
docker run -d --name local-web -p 127.0.0.1:8082:80 nginx:1.27
docker container port web2
```

第一条通常在宿主机所有接口发布 TCP 8081；第二条仅绑定回环地址，更适合本机调试。可用 `-p HOST_IP:HOST_PORT:CONTAINER_PORT/udp` 指定 UDP。多个容器可以监听相同的容器端口，但同一宿主机地址与端口不能被重复占用。端口发布通常通过防火墙/NAT 规则实现，不能直接修改容器内部配置就期待宿主机映射随之改变；已有容器需要新的发布规则时，应以新参数重建容器并迁移数据。

## 4.7 名称解析与文件复制

Docker 会生成容器内的 `/etc/hosts` 与 `/etc/resolv.conf`，具体 DNS 来源取决于网络模式和 daemon 配置。自定义 bridge 网络上的容器可通过名称互相解析；默认 bridge 与 host 网络行为不同，详见网络章节。临时映射名称可用 `--add-host name:IP`，指定 DNS 可用 `--dns IP`，但应先排查宿主机 DNS 和网络连通性。

```bash
docker run --rm --add-host api.example:192.0.2.10 alpine:3.20 cat /etc/hosts
docker cp web:/etc/nginx/nginx.conf ./nginx.conf
docker cp ./nginx.conf web:/tmp/nginx.conf
```

`docker cp` 可在容器运行或停止时复制普通文件；它不是卷备份工具。需要持续共享或持久保存数据时使用 bind mount/命名卷，复制后还要确认文件属主、权限及应用是否重新加载配置。

## 4.8 删除、清理与导出

```bash
docker stop web2 local-web
docker rm web2 local-web
docker container prune      # 先确认提示，仅清理已停止容器
docker system df
```

`docker rm -f` 会强制停止并删除运行中的容器，慎用于有状态服务。`docker system prune` 的范围更广，可能清理未使用的网络、镜像和构建缓存；先查看占用和依赖，避免误删回滚所需资源。

`docker container export CONTAINER -o rootfs.tar` 只导出容器可见的文件系统快照，不含挂载卷内容，也不保留原镜像全部层、默认启动命令等元数据；`docker image import rootfs.tar` 生成一个新镜像。迁移完整镜像用 `docker image save` / `docker image load`，迁移业务数据还须单独备份卷。原文“docker export 操作的源是镜像”属于笔误：`export` 的源是**容器**。

学习这些命令时，建议每次记录容器名、镜像 tag、端口与卷，再按“创建 → 查看 → 日志 → 交互 → 停止 → 删除”走完一次生命周期，避免后续章节的网络、卷和 Compose 配置失去上下文。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/03-managing-container-images.html' | relative_url }}">← 上一章：容器镜像管理</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 目录</a>
  <a href="{{ '/subjects/Docker/05-practical-examples.html' | relative_url }}">下一章：实战案例 →</a>
</nav>
