---
layout: default
title: "JumpServer Bastion Host · Docker Compose Deployment"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to JumpServer Bastion Host Index]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 09 Docker Compose Deployment
### 2.4 Docker-Compose 部署

<https://github.com/jumpserver/Dockerfile/blob/v4.1.0/allinone/docker-compose.yml>

<https://github.com/jumpserver/Dockerfile/blob/master/allinone/docker-compose.yml>

范例：官方docker-compose.yml文件

```yaml
#https://github.com/jumpserver/Dockerfile/blob/v4.1.0/allinone/docker-
compose.yml
services:
mysql:
image: mariadb:10.6
container_name: jms_mysql
restart: always
environment:
TZ: ${TZ:-Asia/Shanghai}
MARIADB_ROOT_PASSWORD: ${DB_PASSWORD:-Np2qgqtiUayA857GpuVI0Wtg}
MARIADB_DATABASE: ${DB_NAME:-jumpserver}
healthcheck:
test: "mysql -h127.0.0.1 -uroot -p$$MARIADB_ROOT_PASSWORD -e 'SHOW
DATABASES;'"
interval: 10s
timeout: 5s
retries: 3
start_period: 30s
volumes:
- ${VOLUME_DIR:-./data}/mariadb/data:/var/lib/mysql
networks:
- net
redis:
image: redis:7.0
container_name: jms_redis
restart: always
command: redis-server --requirepass ${REDIS_PASSWORD:-
KoJqlTDu1d5HwfXgJ4QTbZQt}
environment:
TZ: ${TZ:-Asia/Shanghai}
REDIS_PASSWORD: ${REDIS_PASSWORD:-KoJqlTDu1d5HwfXgJ4QTbZQt}
healthcheck:
test: "redis-cli -h 127.0.0.1 -a $$REDIS_PASSWORD info Replication"
interval: 10s
timeout: 5s
retries: 3
start_period: 10s
volumes:
- ${VOLUME_DIR:-./data}/redis/data:/data
networks:
- net
jumpserver:
image: jumpserver/jms_all:${VERSION:-latest}
build:
context: .
dockerfile: Dockerfile
container_name: jms_all
privileged: true
restart: always
environment:
TIME_ZONE: ${TZ:-Asia/Shanghai}
TZ: ${TZ:-Asia/Shanghai}
SECRET_KEY: ${SECRET_KEY:-
vYneAbsXUhe4BghEeedNL7nfWLwaTTmhnwQMvjYOIG25Ofzghk}
BOOTSTRAP_TOKEN: ${BOOTSTRAP_TOKEN:-K1ffDfLSIK8SV2PZj6VaxOiv8KuawlJK}
LOG_LEVEL: ${LOG_LEVEL:-ERROR}
DB_HOST: ${DB_HOST:-mysql}
DB_PORT: ${DB_PORT:-3306}
DB_USER: ${DB_USER:-root}
DB_PASSWORD: ${DB_PASSWORD:-Np2qgqtiUayA857GpuVI0Wtg}
DB_NAME: ${DB_NAME:-jumpserver}
REDIS_HOST: ${REDIS_HOST:-redis}
REDIS_PORT: ${REDIS_PORT:-6379}
REDIS_PASSWORD: ${REDIS_PASSWORD:-KoJqlTDu1d5HwfXgJ4QTbZQt}
DOMAINS: ${DOMAINS:-}
ports:
- ${HTTP_PORT:-80}:80/tcp
- ${SSH_PORT:-2222}:2222/tcp
depends_on:
mysql:
condition: service_healthy
redis:
condition: service_healthy
healthcheck:
test: "curl -fsL http://localhost/api/health/ > /dev/null"
interval: 10s
timeout: 5s
retries: 3
start_period: 90s
volumes:
- ${VOLUME_DIR:-./data}/core/data:/opt/jumpserver/data
- ${VOLUME_DIR:-./data}/koko/data:/opt/koko/data
- ${VOLUME_DIR:-./data}/lion/data:/opt/lion/data
- ${VOLUME_DIR:-./data}/chen/data:/opt/chen/data
- ${VOLUME_DIR:-./data}/web/data/logs:/var/log/nginx
- ${VOLUME_DIR:-./data}/web/data/download:/opt/download
networks:
- net
networks:
net:
```

范例：基于Jumpserver-v4.10.7 修改官方的docker-compose.yaml （练习）

```json
[root@ubuntu2404 ~]#apt update && apt  -y install docker-compose python3-pip
[root@ubuntu2404 ~]#cat > /etc/docker/daemon.json
{
"registry-mirrors": [
"https://docker.m.daocloud.io",
"https://docker.1panel.live"
]
}
[root@ubuntu2404 ~]#systemctl restart docker
[root@ubuntu2404 ~]#docker-compose version
docker-compose version 1.29.2, build unknown
docker-py version: 5.0.3
CPython version: 3.12.3
OpenSSL version: OpenSSL 3.0.13 30 Jan 2024
[root@ubuntu2404 ~]#cat docker-compose.yaml
services:
mysql:
#image: mariadb:10.6
image: registry.cn-beijing.aliyuncs.com/bowenxiaochun/mariadb:10.6
container_name: jms_mysql
restart: always
environment:
MARIADB_ROOT_PASSWORD: ${DB_PASSWORD:-123456}
MARIADB_DATABASE: ${DB_NAME:-jumpserver}
healthcheck:
test: "mysql -h127.0.0.1 -uroot -p$$MARIADB_ROOT_PASSWORD -e 'SHOW
DATABASES;'"
interval: 10s
timeout: 5s
retries: 3
start_period: 30s
volumes:
- ${VOLUME_DIR:-./data}/mariadb/data:/var/lib/mysql
networks:
- net
redis:
#image: redis:7.0
image: registry.cn-beijing.aliyuncs.com/bowenxiaochun/redis:7.2.5
container_name: jms_redis
restart: always
command: redis-server --requirepass ${REDIS_PASSWORD:-123456}
environment:
REDIS_PASSWORD: ${REDIS_PASSWORD:-123456}
healthcheck:
test: "redis-cli -h 127.0.0.1 -a $$REDIS_PASSWORD info Replication"
interval: 10s
timeout: 5s
retries: 3
start_period: 10s
volumes:
- ${VOLUME_DIR:-./data}/redis/data:/data
networks:
- net
jumpserver:
image: jumpserver/jms_all:v4.10.7
#image: jumpserver/jms_all:v4.10.2
#image: registry.cn-beijing.aliyuncs.com/bowenxiaochun/jms_all:v4.6.0
#build:
#  context: .
#  dockerfile: Dockerfile
container_name: jms_all
privileged: true
restart: always
environment:
SECRET_KEY: ${SECRET_KEY:-
LfFL6zB2mt4fMVq1D3hGKxxW0hopV1tlNicUHvsKJMQxsFPhBM}
BOOTSTRAP_TOKEN: ${BOOTSTRAP_TOKEN:-OVxLWFfTmXRd2f0e}
LOG_LEVEL: ${LOG_LEVEL:-ERROR}
DB_ENGINE: ${DB_HOST:-mysql} #新版要求
DB_HOST: ${DB_HOST:-mysql}
DB_PORT: ${DB_PORT:-3306}
DB_USER: ${DB_USER:-root}
DB_PASSWORD: ${DB_PASSWORD:-123456}
DB_NAME: ${DB_NAME:-jumpserver}
REDIS_HOST: ${REDIS_HOST:-redis}
REDIS_PORT: ${REDIS_PORT:-6379}
REDIS_PASSWORD: ${REDIS_PASSWORD:-123456}
DOMAINS: ${DOMAINS:-}
ports:
- ${HTTP_PORT:-80}:80/tcp
- ${SSH_PORT:-2222}:2222/tcp
depends_on:
mysql:
condition: service_healthy
redis:
condition: service_healthy
healthcheck:
test: "curl -fsL http://localhost/api/health/ > /dev/null"
interval: 10s
timeout: 5s
retries: 3
start_period: 90s
volumes:
- ${VOLUME_DIR:-./data}/core/data:/opt/jumpserver/core/data
- ${VOLUME_DIR:-./data}/koko/data:/opt/jumpserver/koko/data
- ${VOLUME_DIR:-./data}/lion/data:/opt/jumpserver/lion/data
- ${VOLUME_DIR:-./data}/chen/data:/opt/jumpserver/chen/data
- ${VOLUME_DIR:-./data}/kael/data:/opt/jumpserver/kael/data
- ${VOLUME_DIR:-./data}/web/log:/var/log/nginx
networks:
- net
networks:
net:
ipam:
driver: default
config:
- subnet: 172.27.0.0/16
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/08-docker-deployment.html' | relative_url }}">← Previous: Docker Deployment</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">Back to JumpServer Bastion Host Index</a>
  <a href="{{ '/subjects/JumpServer/10-installing-with-the-official-script.html' | relative_url }}">Next: Installing with the Official Script →</a>
</nav>
