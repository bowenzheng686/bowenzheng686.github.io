---
layout: default
title: "Docker 容器技术 · 使用 Dockerfile 构建镜像"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Docker 目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 10 使用 Dockerfile 构建镜像

与 `docker commit` 把交互操作固化为镜像相比，Dockerfile 把构建过程写成可审查、可复现的文本。本章先说明构建上下文、缓存与常用指令，再用 Web、Go、前端和 Java 场景展示单阶段与多阶段构建。原笔记的 Alpine 源码编译 Nginx、Oracle JDK 8 和旧版 Apollo 案例依赖过时版本或第三方下载源，下面保留其构建思想，不把历史命令伪装成当前可直接用于生产的配方。

![Dockerfile 构建镜像、镜像运行容器以及推送或导出镜像的关系示意](assets/img-f0674de899ccbeca.webp)

图中的 `build`、`run`、`push` 和 `save` 面向不同对象：`build` 生成镜像，`run` 由镜像创建容器，`push` 推送到仓库，`save` 导出镜像归档；容器可写层和业务卷并不随镜像归档一起保存。

## 10.1 构建上下文与层

```bash
docker build -t demo-app:1.0 -f Dockerfile .
docker image history demo-app:1.0
```

末尾的 `.` 是**构建上下文目录**，不是 Dockerfile 路径。`COPY` 默认只能引用上下文里的文件；`-f` 可选择另一个 Dockerfile。构建器按指令生成可复用的构建结果，缓存是否命中取决于指令及其输入；把变化少的依赖步骤放前面、经常变化的应用代码放后面，可减少无谓重建。并非“每行都一定新增一个有文件内容的层”，也不应为了追求最少行数把所有逻辑堆进一个不可读的 `RUN`。`RUN cd /tmp` 的工作目录不会延续到下一条指令，持久切换目录用 `WORKDIR`。

`.dockerignore` 排除不需要传入的内容，既减少构建上下文，也避免意外把本地密钥打进镜像：

```text
.git
node_modules
target
*.log
.env
*.pem
```

排除规则应与项目实际文件核对，避免把构建必需的内容也忽略。已经进入历史层的密钥不能靠后续 `RUN rm` 真正抹去；构建密钥应使用 BuildKit secret 等机制，而不是 `ARG`/`ENV` 明文传递。

## 10.2 常用指令：构建时与运行时

| 指令 | 作用与容易混淆的地方 |
| --- | --- |
| `FROM` | 指定基础镜像或新构建阶段；用经过测试的版本，必要时固定 digest |
| `RUN` | 构建期间执行命令，如安装依赖；一个 `RUN` 的 shell 状态不自动延续到下一个 |
| `COPY` | 从构建上下文或其他阶段复制文件；普通复制优先用它 |
| `ADD` | 还可处理 URL 和本地 tar 自动解包；只有确实需要附加行为时使用 |
| `WORKDIR` | 指定后续命令及容器默认工作目录，不存在时会创建 |
| `ARG` | 构建参数，不自动成为运行时环境；**不适合放密钥** |
| `ENV` | 设置镜像运行时环境；可由容器启动参数覆盖 |
| `LABEL` | 添加维护者、版本等元数据；旧 `MAINTAINER` 已过时 |
| `USER` | 指定后续构建指令和运行时的用户；须保证文件及目录权限 |
| `EXPOSE` | 声明应用预期监听端口，不会自动执行宿主机端口映射 |
| `VOLUME` | 声明匿名卷挂载点；具名卷/宿主机路径宜在运行时或 Compose 中配置 |
| `HEALTHCHECK` | 用容器内部命令报告健康状态，不代替应用监控 |
| `STOPSIGNAL` | 配置停止时发给主进程的信号，须与应用优雅退出机制匹配 |
| `SHELL`、`ONBUILD` | 更换 shell 或让子镜像构建时触发指令，属于有明确需求再使用的高级功能 |

`RUN` 在**构建时**运行，`CMD`、`ENTRYPOINT` 在**容器启动时**决定进程。两者的 exec 形式使用 JSON 数组，如 `CMD ["nginx", "-g", "daemon off;"]`；shell 形式经 `/bin/sh -c` 解释，可使用重定向/变量展开，但进程与信号行为不同。运行时主进程应保持前台运行并能正确接收停止信号。

若只有 `CMD`，`docker run IMAGE extra-command` 会替换它。exec 形式的 `ENTRYPOINT` 设定固定可执行程序，而 `CMD` 可提供默认参数；`docker run IMAGE other-args` 替换这些默认参数，并附加到入口点。需要临时替换入口点时用 `--entrypoint`。不要把 shell 与 exec 形式的组合行为混为一谈，可用一个小镜像实测启动参数。

## 10.3 一个可检查的 Web 镜像

静态网站无须从零编译 Nginx。把页面放在 `site/` 后：

```dockerfile
FROM nginx:1.27-alpine
LABEL org.opencontainers.image.title="example-static-site"
COPY site/ /usr/share/nginx/html/
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
```

```bash
docker build -t example-static-site:1.0 .
docker run --rm -p 127.0.0.1:8080:80 example-static-site:1.0
curl -I http://127.0.0.1:8080/
```

如果确实需要自编译 Nginx 模块，应把编译工具、源码校验和运行时依赖放在不同构建阶段，最终阶段仅保留二进制、配置及其动态库；源码版本与依赖需同步维护。用 Alpine 构建的二进制不一定能直接复制到 glibc 基础镜像，反之亦然。

## 10.4 多阶段构建

多阶段构建让构建工具留在 builder 阶段，最终镜像只包含运行所需文件。后续删除 builder 中的文件并不会缩小已生成的旧层，所以直接复制必要产物更清晰。

### Go：编译与运行分离

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -trimpath -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

`./cmd/app` 须替换成项目真实入口，`CGO_ENABLED=0` 适用于不依赖 C 库的应用。若需要 CGO，应为最终镜像准备匹配的动态库。distroless 镜像通常没有 shell，排障方式要提前设计。

### Vue 等前端：Node 构建，Web 服务器交付

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist/ /usr/share/nginx/html/
EXPOSE 80
```

确认项目使用 `npm`、锁文件及产物目录确实为 `dist/`；若用 pnpm/yarn 或 SPA history 路由，需相应调整构建命令和 Nginx 配置。`node_modules` 留在构建阶段，避免将大量开发依赖送入最终镜像。

### Java：构建 JAR，运行 JRE

```dockerfile
FROM eclipse-temurin:21-jdk AS builder
WORKDIR /src
COPY . .
RUN ./mvnw -B -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /src/target/app.jar /app/app.jar
USER 10001:10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

示例假设 Maven Wrapper 和最终文件名 `app.jar`，需根据项目构建结果改写。`-DskipTests` 仅用于演示构建速度，正式流水线要在独立阶段运行测试。Apollo 等微服务还要提供配置中心地址、网络访问与运行时参数，不是一个通用 Dockerfile 就能完成部署。旧版 Oracle JDK 8 与第三方 Alpine-glibc 镜像的许可、维护和 ABI 风险应单独评估；优先使用维护中的 OpenJDK 发行版。

## 10.5 验证与维护

```bash
docker build --pull -t example:1.0 .
docker image inspect example:1.0
docker image history example:1.0
docker run --rm example:1.0
```

`--pull` 会尝试获取基础镜像更新，但发布环境仍应记录最终 digest；必要时用 `--no-cache` 排除缓存问题，而不是每次构建都无条件禁用缓存。`docker image history` 只能查看镜像层的部分构建信息，**不能可靠还原原始 Dockerfile**，更无法恢复被忽略的文件或构建时秘密。第三方“从镜像导出 Dockerfile”的工具得到的是推测结果，应回到源码仓库核对。

对每个案例，最终验收不是“build 成功”，还包括：镜像能启动、主进程保持运行、健康检查有效、端口与卷匹配、文件权限正确、没有明文秘密、依赖版本可追溯。这样 Dockerfile 才成为可维护的交付说明，而非一份只在作者机器上成功过的终端记录。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/09-building-images-with-docker-commit.html' | relative_url }}">← 上一章：使用 Docker Commit 构建镜像</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 目录</a>
  <a href="{{ '/subjects/Docker/11-container-data-management.html' | relative_url }}">下一章：容器数据管理 →</a>
</nav>
