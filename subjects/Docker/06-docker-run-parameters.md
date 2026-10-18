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

忘记之前启动一个容器的启动命令是什么，现在需要找回来 docker run 的运行参数，可以使用  runlike 工具实现

<https://github.com/lavie/runlike>

安装 runlike

```text
#安装方式1: pip
apt  install -y python3-pip
pip3 install runlike
#安装方法2: by docker
alias runlike="docker run --rm -v /var/run/docker.sock:/var/run/docker.sock
assaflavie/runlike"
```

范例：

```bash
#包安装
[root@ubuntu2404 ~]#apt  install -y python3-pip
[root@ubuntu2404 ~]#pip3 install runlike --break-system-packages
[root@ubuntu2204 ~]#apt  install -y python3-pip
[root@ubuntu2204 ~]#pip3 install runlike
#启动一个测试容器
[root@ubuntu2204 ~]#docker run -e MYSQL_ROOT_PASSWORD=123456 -e
MYSQL_DATABASE=wordpress -e MYSQL_USER=wordpress -e MYSQL_PASSWORD=123456 --name
mysql -d  -v /data/mysql:/var/lib/mysql --restart=always registry.cn-
beijing.aliyuncs.com/bowenxiaochun/mysql:8.0.29-oracle
#查看容器运行命令
[root@ubuntu2204 ~]#runlike -p mysql
docker run --name=mysql \
--hostname=7c0f6ba11f5a \
--mac-address=02:42:ac:11:00:02 \
--env=MYSQL_ROOT_PASSWORD=123456 \
--env=MYSQL_DATABASE=wordpress \
--env=MYSQL_USER=wordpress \
--env=MYSQL_PASSWORD=123456 \
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
  <a href="{{ '/subjects/Docker/05-practical-examples.html' | relative_url }}">← Previous: Practical Examples</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/07-container-live-migration-with-criu.html' | relative_url }}">Next: Container Live Migration with CRIU →</a>
</nav>
