---
layout: default
title: "Docker Container Technology · Starting Multiple Containers with Docker Compose"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Docker Container Technology Index]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 21 Starting Multiple Containers with Docker Compose
### 5.4 从 docker compose 启动多个容器

### 编辑 docker-compose 文件并使用数据卷

注意:  同一个文件 ，数据卷的优先级比镜像内的文件优先级高

```bash
[root@ubuntu1804 docker-compose]#vim docker-compose.yml
[root@ubuntu1804 docker-compose]#cat  docker-compose.yml
service-nginx-web:
image: 10.0.0.102/example/nginx-centos7-base:1.6.1
container_name: nginx-web
volumes:
- /data/nginx:/apps/nginx/html/#指定数据卷，将宿主机/data/nginx挂载到容
器/apps/nginx/html
expose:
- 80
- 443
ports:
- "80:80"
- "443:443"
service-tomcat-app1:
image: 10.0.0.102/example/tomcat-web:app1
container_name: tomcat-app1
expose:
- 8080
ports:
- "8081:8080"
```

```bash
service-tomcat-app2:
image: 10.0.0.102/example/tomcat-web:app2
container_name: tomcat-app2
expose:
- 8080
ports:
- "8082:8080"
#在宿主机准备nginx测试页面文件
[root@ubuntu1804 docker-compose]#mkdir /data/nginx
[root@ubuntu1804 docker-compose]#echo Docker compose test page >
/data/nginx/index.html
```

### 启动容器并验证结果

```bash
[root@ubuntu1804 docker-compose]#docker-compose up -d
Pulling service-tomcat-app1 (10.0.0.102/example/tomcat-web:app1)...
app1: Pulling from example/tomcat-web
f34b00c7da20: Already exists
544476d462f7: Already exists
39345915aa1b: Already exists
4b792f2bae38: Already exists
4439447a3522: Already exists
fe34d2ec1dd0: Already exists
b8487ca03126: Already exists
5a475b7d8b1a: Already exists
df8703d3d2dd: Already exists
f0da1ffa7aa7: Pull complete
80fd4c70e670: Pull complete
c2a0247d7bfa: Pull complete
b0977ed809cd: Pull complete
Digest: sha256:e0aba904df6095ea04c594d6906101f8e5f4a6ceb0a8f9b24432c47698d0caa8
Status: Downloaded newer image for 10.0.0.102/example/tomcat-web:app1
Pulling service-tomcat-app2 (10.0.0.102/example/tomcat-web:app2)...
app2: Pulling from example/tomcat-web
f34b00c7da20: Already exists
544476d462f7: Already exists
39345915aa1b: Already exists
4b792f2bae38: Already exists
4439447a3522: Already exists
fe34d2ec1dd0: Already exists
b8487ca03126: Already exists
5a475b7d8b1a: Already exists
df8703d3d2dd: Already exists
f0da1ffa7aa7: Already exists
80fd4c70e670: Already exists
1a55cb76a801: Pull complete
565ab795f82a: Pull complete
Digest: sha256:c4d6f166c3933f6c1ba59c84ea0518ed653af25f28b87981c242b0deff4209bb
Status: Downloaded newer image for 10.0.0.102/example/tomcat-web:app2
Creating tomcat-app1 ... done
Creating tomcat-app2 ... done
Creating nginx-web   ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name                  Command               State                    Ports
---------------------------------------------------------------------------------
--------------
nginx-web     /apps/nginx/sbin/nginx           Up      0.0.0.0:443->443/tcp,
0.0.0.0:80->80/tcp
tomcat-app1   /apps/tomcat/bin/run_tomcat.sh   Up      8009/tcp, 0.0.0.0:8081-
>8080/tcp
tomcat-app2   /apps/tomcat/bin/run_tomcat.sh   Up      8009/tcp, 0.0.0.0:8082-
>8080/tcp
[root@ubuntu1804 docker-compose]#curl http://127.0.0.1/
Docker compose test page
[root@ubuntu1804 docker-compose]#curl http://127.0.0.1:8081/app/
Tomcat Page in app1
[root@ubuntu1804 docker-compose]#curl http://127.0.0.1:8082/app/
Tomcat Page in app2
```

### 指定同时启动容器的数量

```bash
[root@ubuntu1804 docker-compose]#vim docker-compose.yml
[root@ubuntu1804 docker-compose]#cat docker-compose.yml
service-nginx-web:
image: 10.0.0.102/example/nginx-centos7-base:1.6.1
#  container_name: nginx-web #同时启动多个同一镜像的容器，不要指定容器名称，否则会冲突
expose:
- 80
- 443
#  ports:                    #同时启动多个同一镜像的容器，不要指定端口号，否则会冲突
#    - "80:80"
#    - "443:443"
#再加一个service
service-tomcat:
image: 10.0.0.102/example/tomcat-base:v8.5.50
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name   Command   State   Ports
------------------------------
[root@ubuntu1804 docker-compose]#docker-compose  up -d --scale service-nginx-
web=2
Creating docker-compose_service-tomcat_1    ... done
Creating docker-compose_service-nginx-web_1 ... done
Creating docker-compose_service-nginx-web_2 ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name                         Command           State         Ports
---------------------------------------------------------------------------------
-----
docker-compose_service-nginx-web_1   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-nginx-web_2   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-tomcat_1      /bin/bash                Exit 0
[root@ubuntu1804 docker-compose]#docker-compose  up -d --scale service-nginx-
web=3 --scale service-tomcat=2
Starting docker-compose_service-tomcat_1    ... done
Starting docker-compose_service-nginx-web_1 ... done
Starting docker-compose_service-nginx-web_2 ... done
Creating docker-compose_service-nginx-web_3 ... done
Creating docker-compose_service-tomcat_2    ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name                         Command           State         Ports
---------------------------------------------------------------------------------
-----
docker-compose_service-nginx-web_1   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-nginx-web_2   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-nginx-web_3   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-tomcat_1      /bin/bash                Exit 0
docker-compose_service-tomcat_2      /bin/bash                Exit 0
[root@ubuntu1804 docker-compose]#docker-compose  up -d
Stopping and removing docker-compose_service-nginx-web_2 ... done
Stopping and removing docker-compose_service-nginx-web_3 ... done
Stopping and removing docker-compose_service-tomcat_2    ... done
Starting docker-compose_service-tomcat_1                 ... done
Starting docker-compose_service-nginx-web_1              ... done
[root@ubuntu1804 docker-compose]#docker-compose  ps
Name                         Command           State         Ports
---------------------------------------------------------------------------------
-----
docker-compose_service-nginx-web_1   /apps/nginx/sbin/nginx   Up       443/tcp,
80/tcp
docker-compose_service-tomcat_1      /bin/bash                Exit 0
```

### 扩容和缩容

注意: 新版中scale 命令已废弃

```bash
#扩容
[root@ubuntu1804 docker-compose]#docker-compose scale service-nginx-web=3
#缩容为0，即删除容器
[root@ubuntu1804 docker-compose]#docker-compose scale service-nginx-web=0
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/20-starting-a-single-container-with-docker-compose.html' | relative_url }}">← Previous: Starting a Single Container with Docker Compose</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/22-deploying-wordpress.html' | relative_url }}">Next: Practical Examples: 实现 Wordpress 应用 →</a>
</nav>
