---
layout: default
title: "Docker 容器技术 · 查看 docker run 启动参数命令"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 06 查看 docker run 启动参数命令
### 1.6 查看 docker run 启动参数命令

如果忘记容器启动时使用的 `docker run` 参数，可以用 `docker inspect` 查看当前配置，也可以用第三方工具 `runlike` 将配置整理成一条便于参考的命令。**还原结果不一定与原始命令逐字相同**，例如默认值和运行时生成的主机名也可能被列出；重新部署前应逐项检查端口、卷、环境变量和镜像标签。

<https://github.com/lavie/runlike>

### 安装 runlike

```bash
# 方式一：通过 pip 安装
sudo apt install -y python3-pip
pip3 install runlike

# 方式二：通过容器运行，无需在主机上安装 Python 包
alias runlike='docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike'
```

挂载 Docker socket 等同于授予工具管理 Docker 守护进程的权限，仅在可信环境中使用。

范例：

```bash
docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD='<密码>' \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD='<密码>' \
  -v /data/mysql:/var/lib/mysql \
  --restart=always \
  mysql:8.0.29-oracle

runlike -p mysql
```

示例输出（实际值取决于该容器的配置）：

```bash
docker run --name=mysql \
--hostname=7c0f6ba11f5a \
--mac-address=02:42:ac:11:00:02 \
--env=MYSQL_ROOT_PASSWORD='<密码>' \
--env=MYSQL_DATABASE=wordpress \
--env=MYSQL_USER=wordpress \
--env=MYSQL_PASSWORD='<密码>' \
--volume=/data/mysql:/var/lib/mysql \
--expose=3306 \
--expose=33060 \
--restart=always \
--runtime=runc \
--detach=true \
mysql:8.0.29-oracle \
mysqld
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/05-practical-examples.html' | relative_url }}">← 上一篇：实践示例</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/07-container-live-migration-with-criu.html' | relative_url }}">下一篇：使用 CRIU 迁移容器 →</a>
</nav>
