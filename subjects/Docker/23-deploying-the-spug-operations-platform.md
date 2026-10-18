---
layout: default
title: "Docker 容器技术 · 实战案例: 搭建运维平台 Spug"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 23 实战案例: 搭建运维平台 Spug
### 5.6 实战案例: 搭建运维平台 Spug

Spug是面向中小型企业设计的轻量级无Agent的自动化运维平台，整合了主机管理、主机批量执行、主机在线终端、文件在线上传下载、应用发布部署、在线任务计划、配置中心、监控、报警等一系列功能。

Spug是上海时巴克科技有限公司旗下的开源运维项目，公司旗下现有产品「Spug开源运维平台」 「Spug推送助手」，公司专注为中小企业服务。

参考链接

<https://spug.cc/docs/install-docker>

范例: 基于docker-compose 部署 Spug

```yaml
#安装docker和docker-compse
略
#创建docker-compse.yml文件
#vi docker-compose.yml
version: "3.9"
services:
db:
image: mysql:5.7.30
container_name: spug-db
restart: always
command: --character-set-server=utf8mb4 --collation-
server=utf8mb4_unicode_ci
volumes:
- /data/spug/mysql:/var/lib/mysql
environment:
- MYSQL_DATABASE=spug
- MYSQL_USER=spug
- MYSQL_PASSWORD=spug.cc
- MYSQL_ROOT_PASSWORD=spug.cc
spug:
#image: registry.aliyuncs.com/openspug/spug
image: openspug/spug-service
container_name: spug
privileged: true
restart: always
volumes:
- /data/spug/service:/data/spug
- /data/spug/repos:/data/repos
ports:
# 如果80端口被占用可替换为其他端口，例如: - "8000:80"
- "80:80"
environment:
- SPUG_DOCKER_VERSION=v3.2.1
- MYSQL_DATABASE=spug
- MYSQL_USER=spug
- MYSQL_PASSWORD=spug.cc
- MYSQL_HOST=db
- MYSQL_PORT=3306
depends_on:
- db
#启动项目
#docker compose up -d
#初始化:以下操作会创建一个用户名为 admin 密码为 123456 的管理员账户，可自行替换管理员账户/密
码。
docker exec spug init_spug admin 123456
#访问测试:在浏览器中输入 http://localhost:80 访问（默认账户密码在上面一步初始化时设置）。
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/22-deploying-wordpress.html' | relative_url }}">← Previous: Practical Examples: 实现 Wordpress 应用</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/24-building-and-deploying-tomcat.html' | relative_url }}">Next: Practical Examples: 构建和部署 Tomcat →</a>
</nav>
