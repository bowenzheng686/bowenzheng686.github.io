---
layout: default
title: "Docker Container Technology · Deploying the RuoYi Microservices Project"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Docker Container Technology Index]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 25 Deploying the RuoYi Microservices Project
### 5.8 实战案例：RuoYI 微服务项目

```yaml
#https://gitee.com/y_project/RuoYi-Cloud/blob/master/docker/docker-compose.yml
version : '3.8'
services:
ruoyi-nacos:
container_name: ruoyi-nacos
image: nacos/nacos-server
build:
context: ./nacos
environment:
- MODE=standalone
volumes:
- ./nacos/logs/:/home/nacos/logs
-
./nacos/conf/application.properties:/home/nacos/conf/application.properties
ports:
- "8848:8848"
- "9848:9848"
- "9849:9849"
depends_on:
- ruoyi-mysql
ruoyi-mysql:
container_name: ruoyi-mysql
image: mysql:5.7
build:
context: ./mysql
ports:
- "3306:3306"
volumes:
- ./mysql/conf:/etc/mysql/conf.d
- ./mysql/logs:/logs
- ./mysql/data:/var/lib/mysql
command: [
'mysqld',
'--innodb-buffer-pool-size=80M',
'--character-set-server=utf8mb4',
'--collation-server=utf8mb4_unicode_ci',
'--default-time-zone=+8:00',
'--lower-case-table-names=1'
]
environment:
MYSQL_DATABASE: 'ry-cloud'
MYSQL_ROOT_PASSWORD: password
ruoyi-redis:
container_name: ruoyi-redis
image: redis
build:
context: ./redis
ports:
- "6379:6379"
volumes:
- ./redis/conf/redis.conf:/home/ruoyi/redis/redis.conf
- ./redis/data:/data
command: redis-server /home/ruoyi/redis/redis.conf
ruoyi-nginx:
container_name: ruoyi-nginx
image: nginx
build:
context: ./nginx
ports:
- "80:80"
volumes:
- ./nginx/html/dist:/home/ruoyi/projects/ruoyi-ui
- ./nginx/conf/nginx.conf:/etc/nginx/nginx.conf
- ./nginx/logs:/var/log/nginx
- ./nginx/conf.d:/etc/nginx/conf.d
depends_on:
- ruoyi-gateway
links:
- ruoyi-gateway
ruoyi-gateway:
container_name: ruoyi-gateway
build:
context: ./ruoyi/gateway
dockerfile: dockerfile
ports:
- "8080:8080"
depends_on:
- ruoyi-redis
links:
- ruoyi-redis
ruoyi-auth:
container_name: ruoyi-auth
build:
context: ./ruoyi/auth
dockerfile: dockerfile
ports:
- "9200:9200"
depends_on:
- ruoyi-redis
links:
- ruoyi-redis
ruoyi-modules-system:
container_name: ruoyi-modules-system
build:
context: ./ruoyi/modules/system
dockerfile: dockerfile
ports:
- "9201:9201"
depends_on:
- ruoyi-redis
- ruoyi-mysql
links:
- ruoyi-redis
- ruoyi-mysql
ruoyi-modules-gen:
container_name: ruoyi-modules-gen
build:
context: ./ruoyi/modules/gen
dockerfile: dockerfile
ports:
- "9202:9202"
depends_on:
- ruoyi-mysql
links:
- ruoyi-mysql
ruoyi-modules-job:
container_name: ruoyi-modules-job
build:
context: ./ruoyi/modules/job
dockerfile: dockerfile
ports:
- "9203:9203"
depends_on:
- ruoyi-mysql
links:
- ruoyi-mysql
ruoyi-modules-file:
container_name: ruoyi-modules-file
build:
context: ./ruoyi/modules/file
dockerfile: dockerfile
ports:
- "9300:9300"
volumes:
- ./ruoyi/uploadPath:/home/ruoyi/uploadPath
ruoyi-visual-monitor:
container_name: ruoyi-visual-monitor
build:
context: ./ruoyi/visual/monitor
dockerfile: dockerfile
ports:
- "9100:9100"
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/24-building-and-deploying-tomcat.html' | relative_url }}">← Previous: Practical Examples: 构建和部署 Tomcat</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/26-converting-between-docker-run-and-compose.html' | relative_url }}">Next: Practical Examples: docker run 和 Docker Compose 文件相互转换 →</a>
</nav>
