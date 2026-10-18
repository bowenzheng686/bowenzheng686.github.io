---
layout: default
title: "Docker 容器技术 · 从 docker compose 启动单个容器"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 20 从 docker compose 启动单个容器
### 5.3 从 docker compose 启动单个容器

注意:  使用Docker compose之前，先要安装docker

### 创建 docker compose文件

docker compose 文件可在任意目录，创建文件名为docker-compose.yml 配置文件，要注意前后的缩进

```bash
[root@ubuntu1804 ~]#docker-compose --version
docker-compose version 1.25.4, build unknown
[root@ubuntu1804 ~]#mkdir /data/docker-compose
[root@ubuntu1804 ~]#cd /data/docker-compose
[root@ubuntu1804 docker-compose]#vim  docker-compose.yml
[root@ubuntu1804 docker-compose]#cat docker-compose.yml
service-nginx-web:
image: harbor.bowen.org/example/nginx-centos7-base:1.6.1
container_name: nginx-web
expose:
- 80
- 443
ports:
- "80:80"
- "443:443"
```

### 查看配置和格式检查

```yaml
[root@ubuntu1804 docker-compose]#docker-compose  config
services:
service-nginx-web:
container_name: nginx-web
expose:
- 80
- 443
image: harbor.bowen.org/example/nginx-centos7-base:1.6.1
network_mode: bridge
ports:
- 80:80/tcp
- 443:443/tcp
version: '2.1'
[root@ubuntu1804 docker-compose]#docker-compose  config -q
#改错ocker-compose文件格式
[root@ubuntu1804 docker-compose]#vim docker-compose.yml
service-nginx-web   #改此行，最后的”:"删除
image: harbor.bowen.org/example/nginx-centos7-base:1.6.1
container_name: nginx-web
expose:
- 80
- 443
ports:
- "80:80"
- "443:443"
[root@ubuntu1804 docker-compose]#docker-compose  config -q
ERROR: yaml.scanner.ScannerError: mapping values are not allowed here
in "./docker-compose.yml", line 2, column 8
[root@ubuntu1804 docker-compose]#
```

### 启动容器

注意:  必须要在docker compose文件所在的目录执行

```bash
#前台启动
[root@ubuntu1804 docker-compose]#docker-compose up
Pulling service-nginx-web (harbor.bowen.org/example/nginx-centos7-base:1.6.1)...
ERROR: Get https://harbor.bowen.org/v2/: dial tcp 10.0.0.102:443: connect:
connection refused
[root@ubuntu1804 docker-compose]#vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
--insecure-registry harbor.bowen.org
[root@ubuntu1804 docker-compose]#systemctl daemon-reload
[root@ubuntu1804 docker-compose]#systemctl restart docker
[root@ubuntu1804 docker-compose]#docker-compose up
Pulling service-nginx-web (10.0.0.102/example/nginx-centos7-base:1.6.1)...
1.6.1: Pulling from example/nginx-centos7-base
f34b00c7da20: Pull complete
544476d462f7: Pull complete
39345915aa1b: Pull complete
d5376f2bbd9e: Pull complete
4596aecee927: Pull complete
1617b995c379: Pull complete
d00df95be654: Pull complete
Digest: sha256:82e9e7d8bf65e160ba79a92bb25ae42cbbf791092d1e09fb7de25f91b31a21ff
Status: Downloaded newer image for 10.0.0.102/example/nginx-centos7-base:1.6.1
Creating nginx-web ... done
Attaching to nginx-web
#以上是前台执行不退出
```

### 验证docker compose执行结果

```bash
#上面命令是前台执行，所以要查看结果，可以再开一个终端窗口进行观察
[root@ubuntu1804 ~]#docker ps
CONTAINER ID        IMAGE                                         COMMAND
CREATED             STATUS              PORTS
NAMES
d71030504f6a        harbor.bowen.org/example/nginx-centos7-base:1.6.1
"/apps/nginx/sbin/ng…"   15 seconds ago      Up 13 seconds       0.0.0.0:80-
>80/tcp, 0.0.0.0:443->443/tcp   nginx-web
[root@ubuntu1804 ~]#docker-compose ps
ERROR:
Can't find a suitable configuration file in this directory or any
parent. Are you in the right directory?
Supported filenames: docker-compose.yml, docker-compose.yaml
[root@ubuntu1804 ~]#cd /data/docker-compose/
[root@ubuntu1804 docker-compose]#docker-compose ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
[root@ubuntu1804 docker-compose]#curl 127.0.0.1/app/
Test Page in app
[root@ubuntu1804 docker-compose]#docker-compose images
Container                Repository                  Tag      Image Id       Size
---------------------------------------------------------------------------------
--
nginx-web   harbor.bowen.org/example/nginx-centos7-base   1.6.1   ea3840c349e5
413.4 MB
[root@ubuntu1804 docker-compose]#docker-compose exec service-nginx-web bash
[root@17c17ad30193 /]#
[root@17c17ad30193 /]#
[root@17c17ad30193 /]#
[root@17c17ad30193 /]# tail -f /apps/nginx/logs/access.log
172.17.0.1 - - [04/Feb/2020:16:01:42 +0800] "GET /app/ HTTP/1.1" 200 17 "-"
"curl/7.58.0"
10.0.0.101 - - [04/Feb/2020:16:06:29 +0800] "GET /app/ HTTP/1.1" 200 17 "-"
"curl/7.58.0"
10.0.0.102 - - [04/Feb/2020:16:08:22 +0800] "GET /app/ HTTP/1.1" 200 17 "-"
"curl/7.58.0"
```

### 结束前台执行

```bash
[root@ubuntu1804 docker-compose]#docker-compose up
Pulling service-nginx-web (10.0.0.102/example/nginx-centos7-base:1.6.1)...
1.6.1: Pulling from example/nginx-centos7-base
f34b00c7da20: Pull complete
544476d462f7: Pull complete
39345915aa1b: Pull complete
d5376f2bbd9e: Pull complete
4596aecee927: Pull complete
1617b995c379: Pull complete
d00df95be654: Pull complete
Digest: sha256:82e9e7d8bf65e160ba79a92bb25ae42cbbf791092d1e09fb7de25f91b31a21ff
Status: Downloaded newer image for 10.0.0.102/example/nginx-centos7-base:1.6.1
Creating nginx-web ... done
Attaching to nginx-web
^CGracefully stopping... (press Ctrl+C again to force)  #ctrl+c键，结束容器
Stopping nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose ps
Name             Command           State    Ports
---------------------------------------------------
nginx-web   /apps/nginx/sbin/nginx   Exit 0
[root@ubuntu1804 docker-compose]#docker ps -a
CONTAINER ID        IMAGE                                         COMMAND
CREATED             STATUS                          PORTS
NAMES
d71030504f6a       harbor.bowen.org/example/nginx-centos7-base:1.6.1
"/apps/nginx/sbin/ng…"   5 minutes ago       Exited (0) About a minute ago
nginx-web
[root@ubuntu1804 docker-compose]#docker-compose start
Starting service-nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
#关闭容器
[root@ubuntu1804 docker-compose]#docker-compose kill
Killing nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose ps
Name             Command            State     Ports
-----------------------------------------------------
nginx-web   /apps/nginx/sbin/nginx   Exit 137
```

### 删除容器

```bash
[root@ubuntu1804 docker-compose]#docker-compose ps
Name             Command           State    Ports
---------------------------------------------------
nginx-web   /apps/nginx/sbin/nginx   Exit 0
#只删除停止的容器
[root@ubuntu1804 docker-compose]#docker-compose rm
Going to remove nginx-web
Are you sure? [yN] y
Removing nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose up -d
Creating nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose rm
No stopped containers
#停止并删除容器及镜像
[root@ubuntu1804 docker-compose]#docker-compose down
Stopping nginx-web ... done
Removing nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose ps
Name   Command   State   Ports
------------------------------
[root@ubuntu1804 docker-compose]#docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED
STATUS              PORTS               NAMES
#也会自动删除镜像
[root@ubuntu1804 docker-compose]#docker-compose  images
Container   Repository   Tag   Image Id   Size
----------------------------------------------
```

### 后台执行

```bash
[root@ubuntu1804 docker-compose]#docker-compose  up -d
Creating nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
[root@ubuntu1804 docker-compose]#curl 127.0.0.1/app/
Test Page in app
[root@ubuntu1804 docker-compose]#curl http://127.0.0.1/app/
Test Page in app
```

### 停止和启动与日志查看

```bash
[root@ubuntu1804 docker-compose]#docker-compose stop
Stopping nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State    Ports
---------------------------------------------------
nginx-web   /apps/nginx/sbin/nginx   Exit 0
[root@ubuntu1804 docker-compose]#docker-compose start
Starting service-nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
[root@ubuntu1804 docker-compose]#docker-compose  restart
Restarting nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
#执行上面操作时，可以同时开一个终端，观察日事件
[root@ubuntu1804 docker-compose]#docker-compose events
2020-02-04 15:38:13.253822 container kill
5d92e4da8679a973145e5b4db364ae8cf8596a03c4fd0b3b6a28213a2f155be6
(image=harbor.bowen.org/example/nginx-centos7-base:1.6.1, name=nginx-web)
2020-02-04 15:38:13.531208 container die
5d92e4da8679a973145e5b4db364ae8cf8596a03c4fd0b3b6a28213a2f155be6
(image=harbor.bowen.org/example/nginx-centos7-base:1.6.1, name=nginx-web)
2020-02-04 15:38:13.631137 container stop
5d92e4da8679a973145e5b4db364ae8cf8596a03c4fd0b3b6a28213a2f155be6
(image=harbor.bowen.org/example/nginx-centos7-base:1.6.1, name=nginx-web)
2020-02-04 15:38:15.137495 container start
5d92e4da8679a973145e5b4db364ae8cf8596a03c4fd0b3b6a28213a2f155be6
(image=harbor.bowen.org/example/nginx-centos7-base:1.6.1, name=nginx-web)
2020-02-04 15:38:15.137546 container restart
5d92e4da8679a973145e5b4db364ae8cf8596a03c4fd0b3b6a28213a2f155be6
(image=10.0.0.102/example/nginx-centos7-base:1.6.1, name=nginx-web)
#以json格式显示日志
[root@ubuntu1804 docker-compose]#docker-compose events --json
{"time": "2020-02-04T15:48:22.423539", "type": "container", "action": "kill",
"id": "19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b",
"service": "service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
{"time": "2020-02-04T15:48:22.537200", "type": "container", "action":
"exec_die", "id":
"19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b", "service":
"service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
{"time": "2020-02-04T15:48:22.745670", "type": "container", "action": "die",
"id": "19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b",
"service": "service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
{"time": "2020-02-04T15:48:22.863375", "type": "container", "action": "stop",
"id": "19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b",
"service": "service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
{"time": "2020-02-04T15:48:23.979421", "type": "container", "action": "start",
"id": "19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b",
"service": "service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
{"time": "2020-02-04T15:48:23.979468", "type": "container", "action": "restart",
"id": "19d72e9bc85842d8879d7dcf2a3d2defd79a5a0c3c3d974ddfbbbc6e95bf910b",
"service": "service-nginx-web", "attributes": {"name": "nginx-web", "image":
"10.0.0.102/example/nginx-centos7-base:1.6.1"}}
```

### 暂停和恢复

```bash
[root@ubuntu1804 docker-compose]#docker-compose  pause
Pausing nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State                     Ports
---------------------------------------------------------------------------------
-----
nginx-web   /apps/nginx/sbin/nginx   Paused   0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
[root@ubuntu1804 docker-compose]#curl -m 1  http://127.0.0.1/app/
curl: (28) Operation timed out after 1002 milliseconds with 0 bytes received
[root@ubuntu1804 docker-compose]#docker-compose  unpause
Unpausing nginx-web ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name             Command           State                    Ports
---------------------------------------------------------------------------------
----
nginx-web   /apps/nginx/sbin/nginx   Up      0.0.0.0:443->443/tcp, 0.0.0.0:80-
>80/tcp
[root@ubuntu1804 docker-compose]#curl -m 1  http://127.0.0.1/app/
Test Page in app
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/19-installation-and-preparation.html' | relative_url }}">← Previous: Installation and Preparation</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/21-starting-multiple-containers-with-docker-compose.html' | relative_url }}">Next: Starting Multiple Containers with Docker Compose →</a>
</nav>
