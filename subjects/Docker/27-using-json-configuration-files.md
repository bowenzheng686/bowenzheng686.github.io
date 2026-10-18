---
layout: default
title: "Docker 容器技术 · 使用 Json 格式文件"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 27 使用 Json 格式文件
### 5.10 使用 Json 格式文件

```yaml
[root@ubuntu2204 data]#cat  docker-compose.yaml
version: "3.9"
services:
redis:
#image: redis:alpine
image: registry.cn-beijing.aliyuncs.com/bowenxiaochun/redis:7.2.5
[root@ubuntu2204 data]#docker-compose up -d
Creating network "data_default" with the default driver
Creating data_redis_1 ... done
[root@ubuntu2204 data]#docker-compose ps
Name                  Command               State    Ports
----------------------------------------------------------------
data_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
[root@ubuntu2204 data]#docker-compose down
Stopping data_redis_1 ... done
Removing data_redis_1 ... done
Removing network data_default
#使用Json格式文件
[root@ubuntu2404 data]#apt update && apt -y install libghc-yaml-dev jq
reserialize
[root@ubuntu2204 data]#apt update && apt -y install libghc-yaml-dev jq
[root@ubuntu2204 data]#yaml2json docker-compose.yaml > docker-compose.json
[root@ubuntu2204 data]#cat docker-compose.json
{"version":"3.9","services":{"redis":{"image":"redis:alpine"}}}
[root@ubuntu2204 data]#cat docker-compose.json |jq
{
"version": "3.9",
"services": {
"redis": {
"image": "redis:alpine"
}
}
}
[root@ubuntu2204 data]#docker-compose -f docker-compose.json up -d
[root@ubuntu2204 data]#docker-compose -f docker-compose.json ps
Name                  Command               State    Ports
----------------------------------------------------------------
data_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
```

```bash
[root@ubuntu2204 data]#docker-compose -f docker-compose.json down
Stopping data_redis_1 ... done
Removing data_redis_1 ... done
Removing network data_default
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/26-converting-between-docker-run-and-compose.html' | relative_url }}">← Previous: Practical Examples: docker run 和 Docker Compose 文件相互转换</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/28-official-docker-hub.html' | relative_url }}">Next: Official Docker Hub →</a>
</nav>
