---
layout: default
title: "Docker 容器技术 · 常见面试题"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 37 常见面试题
## 8 常见面试题

这一节按“镜像与构建、运行与网络、排障与安全”整理常见问题。回答时最好结合本专题前面的实例，不要只背命令名称。

### 镜像与构建

1. **常用 Docker 命令有哪些？** 用 `docker image ls` 查看镜像，`docker ps -a` 查看容器，`docker run` 创建并启动容器，`docker logs` 查看标准输出，`docker exec` 进入运行中的容器，`docker inspect` 查看详细配置。
2. **Dockerfile 中 `RUN`、`CMD`、`ENTRYPOINT` 有什么区别？** `RUN` 在构建镜像时执行；`CMD` 提供容器启动时的默认命令或参数；`ENTRYPOINT` 指定主要可执行程序。`docker run IMAGE ...` 可以覆盖 `CMD`，但通常会作为 exec 形式 `ENTRYPOINT` 的参数。
3. **`COPY` 与 `ADD` 如何选择？** 普通文件复制优先使用含义更清晰的 `COPY`。`ADD` 还支持远程 URL 和本地 tar 自动解包，只有确实需要这些特性时再使用。
4. **如何优化镜像？** 选用适合的基础镜像、使用 `.dockerignore` 排除无关文件、合理利用构建缓存，并用多阶段构建移除构建依赖。优化应以可维护性、安全性和镜像体积共同衡量。
5. **构建镜像时能否修改“容器内内核参数”？** 容器共享宿主机内核；不能把一个独立内核打进普通 Docker 镜像。运行时允许调整的参数取决于宿主机和容器运行权限，宿主机级参数应在宿主机上管理。

### 容器运行与网络

6. **如何查看 Docker 版本？** `docker version` 分别显示客户端与服务端版本；`docker info` 显示运行环境信息。
7. **常见网络模式有哪些？** 默认 `bridge` 提供容器网络；`host` 直接使用宿主机网络命名空间；`none` 不配置网络。用户自定义 bridge 通常支持容器名解析，跨主机通信还需要路由、端口发布或覆盖网络等额外方案。
8. **不同宿主机上的容器如何通信？** 可以发布端口并经宿主机地址访问；也可以使用具备跨主机网络能力的编排或网络方案。单机默认 bridge 不会自动把两个宿主机上的容器连成同一网络。
9. **`EXPOSE` 与 `-p` 有何区别？** `EXPOSE` 是镜像中的端口元数据，不会自行在宿主机开放端口；`docker run -p 宿主机端口:容器端口` 才创建端口发布规则。
10. **容器创建后能直接修改 `-p` 映射吗？** 普通 Docker 命令不支持在已有容器上直接修改端口发布。应先根据 `docker inspect` 或 Compose 配置确认卷和环境变量，再按新端口重建容器；持久数据应放在卷中。

### 排障与安全

11. **如何查看容器日志？** 优先使用 `docker logs CONTAINER` 或集中式日志系统。日志在宿主机上的具体路径取决于日志驱动，不能假定都位于某个固定目录；可用 `docker inspect` 查询 `LogPath` 和日志配置。
12. **Docker 如何管理和隔离容器？** Docker Engine 通过 API 管理镜像与容器，底层利用 Linux 命名空间、cgroups、联合文件系统及容器运行时等机制。隔离并不等同于虚拟机的独立内核。
13. **Docker 守护进程如何通信？** Docker 客户端与 Engine 使用 Docker API；本机通常经 Unix socket，远程连接可使用 SSH 或配置了 TLS 的 TCP。不要无保护地暴露 Docker API。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/36-container-gpu-limits.html' | relative_url }}">← 上一篇：容器 GPU 资源限制</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
</nav>
