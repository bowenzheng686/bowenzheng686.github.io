---
layout: default
title: "Docker 容器技术 · 安装和准备"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 19 安装和准备
### 5.2 安装和准备

### 安装 Docker Compose

### 方法1：通过 Compose plugin 形式安装

即通过docker 内置子命令实现, 此方式无需专门安装独立的 docker-compose 工具

注意：此方式需要配置官方仓库才支持，Ubuntu内置仓库没有此插件包

```text
#https://docs.docker.com/compose/install/linux/
Set up Docker's repository on your Linux system.
Install Compose manually.
Note
These instructions assume you already have Docker Engine and Docker CLI installed
and now want to install the Compose plugin.
For Compose standalone, see Install Compose Standalone.
Install using the repository
For Ubuntu and Debian, run:
sudo apt-get update
sudo apt-get install docker-compose-plugin
For RPM-based distros, run:
sudo yum update
sudo yum install docker-compose-plugin
Verify that Docker Compose is installed correctly by checking the version.
content_copy
docker compose version
```

在配置官方仓库后，进行安装docker时

在新版docker-23.0.0以上开始内置了compose的子命令 docker-20.10.24以前版本没有内置，需要单独安装docker-compose

范例：在Ubuntu22.04 安装docker-compose插件

```bash
[root@ubuntu2204 ~]#curl -fsSL https://mirrors.aliyun.com/docker-
ce/linux/ubuntu/gpg | sudo apt-key add -
[root@ubuntu2204 ~]#add-apt-repository "deb [arch=amd64]
https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
[root@ubuntu2204 ~]#apt update
[root@ubuntu2204 ~]#apt-get install docker-compose-plugin
[root@ubuntu2204 ~]#docker version
Client: Docker Engine - Community
Version:           23.0.0
API version:       1.42
Go version:        go1.19.5
Git commit:        e92dd87
Built:             Wed Feb  1 17:47:51 2023
OS/Arch:           linux/amd64
Context:           default
Server: Docker Engine - Community
Engine:
Version:          23.0.0
API version:      1.42 (minimum version 1.12)
Go version:       go1.19.5
Git commit:       d7573ab
Built:            Wed Feb  1 17:47:51 2023
OS/Arch:          linux/amd64
Experimental:     false
containerd:
Version:          1.6.24
GitCommit:        61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
runc:
Version:          1.1.9
GitCommit:        v1.1.9-0-gccaecfc
docker-init:
Version:          0.19.0
GitCommit:        de40ad0
[root@ubuntu2204 ~]#docker <两次TAB>
attach     config     diff       history    inspect    logs       plugin
rename     save       start      tag        version
build      container  events     image      kill       manifest   port
restart    search     stats      top        volume
builder    context    exec       images     load       network    ps         rm
secret     stop       trust      wait
commit     cp         export     import     login      node       pull       rmi
service    swarm      unpause
compose    create     help       info       logout     pause      push       run
stack      system     update
[root@ubuntu2204 ~]#docker compose version
Docker Compose version v2.21.0
```

```bash
[root@ubuntu2204 ~]#docker version
Client: Docker Engine - Community
Version:           24.0.7
API version:       1.43
Go version:        go1.20.10
Git commit:        afdd53b
Built:             Thu Oct 26 09:07:41 2023
OS/Arch:           linux/amd64
Context:           default
Server: Docker Engine - Community
Engine:
Version:          24.0.7
API version:      1.43 (minimum version 1.12)
Go version:       go1.20.10
Git commit:       311b9ff
Built:            Thu Oct 26 09:07:41 2023
OS/Arch:          linux/amd64
Experimental:     false
containerd:
Version:          1.6.24
GitCommit:        61f9fd88f79f081d64d6fa3bb1a0dc71ec870523
runc:
Version:          1.1.9
GitCommit:        v1.1.9-0-gccaecfc
docker-init:
Version:          0.19.0
GitCommit:        de40ad0
[root@ubuntu2204 ~]#docker <两次TAB>
attach     commit     context    events     history    info       login
network    port       rename     run        service    stop       top
version
build      compose    cp         exec       image      inspect    logout
node       ps         restart    save       stack      swarm      trust
volume
builder    config     create     export     images     kill       logs
pause      pull       rm         search     start      system     unpause
wait
buildx     container  diff       help       import     load       manifest
plugin     push       rmi        secret     stats      tag        update
[root@ubuntu2204 ~]#docker compose version
Docker Compose version v2.21.0
```

### 方法2: 在线直接从包仓库安装

此方法安装的版本较旧，不推荐使用

范例：Ubuntu24.04内置仓库安装docker-compose

```bash
#Ubuntu24.04默认需要安装python3-pip，否则无法启动
[root@ubuntu2404 ~]#apt update && apt  install -y  python3-pip
[root@ubuntu2404 ~]#apt update && apt install -y  docker.io docker-compose
[root@ubuntu2404 ~]#docker-compose version
docker-compose version 1.29.2, build unknown
docker-py version: 5.0.3
CPython version: 3.12.3
OpenSSL version: OpenSSL 3.0.13 30 Jan 2024
```

范例：Ubuntu22.04内置仓库安装docker-compose

```bash
#ubuntu安装,此为默认版本
[root@ubuntu2204 ~]#apt list  docker-compose
正在列表... 完成
docker-compose/jammy 1.29.2-1 all
[root@ubuntu1804 ~]#apt -y install docker-compose
[root@ubuntu1804 ~]#docker-compose --version
docker-compose version 1.17.1, build unknown
#CentOS7安装，依赖EPEL源
[root@centos7 ~]#yum -y install docker-compose
[root@centos7 ~]#docker-compose --version
docker-compose version 1.18.0, buil 8dd22a9
```

### 方法3: 离线安装，直接从github或国内镜像站下载安装对应版本

参看说明:  https://github.com/docker/compose/releases

此方法安装版本可方便指定，推荐方法，但网络下载较慢

```bash
[root@ubuntu1804 ~]#curl -L
https://github.com/docker/compose/releases/download/1.25.3/docker-compose-`uname
-s`-`uname -m` -o /usr/local/bin/docker-compose
#从国内镜像站下载
[root@ubuntu1804 ~]#curl -L
https://get.daocloud.io/docker/compose/releases/download/1.25.3/docker-
compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
[root@ubuntu1804 ~]#chmod +x /usr/local/bin/docker-compose
[root@ubuntu1804 ~]#ldd /usr/local/bin/docker-compose
不是动态可执行文件
```

### 方法4: 在线通过 pip安装

python-pip 包将安装一个 pip 的命令，pip 命令是一个python 安装包的安装工具，其类似于ubuntu 的 apt 或者 redhat 的yum，但是pip 只安装 python 相关的安装包，可以在多种操作系统安装和使用pip

此方式当前安装的版本较新，为docker_compose-1.25.3，推荐使用

```bash
Ubuntu:
# apt  update
# apt  install -y  python-pip
CentOS:
# yum install epel-release
# yum install -y python-pip
# pip install --upgrade pip
```

范例:  基于python3 安装 docker-compose

```bash
#配置加速
#方法1
[root@ubuntu2004 ~]#python3 -m pip config set global.index-url
https://pypi.tuna.tsinghua.edu.cn/simple
[root@ubuntu2404 ~]#cat /root/.config/pip/pip.conf
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
#方法2
[root@ubuntu2004 ~]#mkdir ~/.pip
[root@ubuntu2004 ~]#cat > ~/.pip/pip.conf <<-EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
EOF
[root@ubuntu2004 ~]#apt -y install python3-pip
[root@ubuntu2004 ~]#pip3 install --upgrade pip
[root@ubuntu2004 ~]#pip3 install docker-compose
[root@ubuntu2004 ~]#docker-compose --version
docker-compose version 1.27.4, build unknown
#基于python2安装docker-compose
[root@ubuntu1804 ~]#apt -y install python-pip
[root@ubuntu1804 ~]#pip install docker-compose
[root@ubuntu1804 ~]#docker-compose --version
docker-compose version 1.25.3, build unknown
```

### 查看命令格式

官方文档:  https://docs.docker.com/compose/reference/

```text
docker-compose --help
Define and run multi-container applications with Docker.
Usage:
docker-compose [-f <arg>...] [options] [COMMAND] [ARGS...]
docker-compose -h|--help
#选项说明:
-f，–file FILE #指定Compose 模板文件，默认为docker-compose.yml|yaml
-p，–project-name NAME #指定项目名称，默认将使用当前所在目录名称作为项目名。
--verbose   #显示更多输出信息
--log-level LEVEL    #定义日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
--no-ansi #不显示ANSI 控制字符
-v, --version #显示版本
#以下为命令选项，需要在docker-compose.yml|yaml 文件所在在目录里执行
config  -q #查看当前配置，没有错误不输出任何信息
up #创建并启动容器
build  #构建镜像
bundle #从当前docker compose 文件生成一个以<当前目录>为名称的json格式的Docker Bundle 备
份文件
create #创建服务
down #停止和删除所有容器、网络、镜像和卷
events #从容器接收实时事件，可以指定json 日志格式
exec #进入指定容器进行操作
help #显示帮助细信息
images #显示镜像信息
kill #强制终止运行中的容器
logs #查看容器的日志
pause #暂停服务
port #查看端口
ps #列出容器
pull #重新拉取镜像，镜像发生变化后，需要重新拉取镜像
push #上传镜像
restart #重启服务
rm #删除已经停止的服务
run #一次性运行容器
scale  #设置指定服务运行的容器个数，新版已废弃
start #启动服务
stop #停止服务
top #显示容器运行状态
unpause #取消暂定
```

范例:

```bash
[root@ubuntu1804 ~]#docker-compose --version
docker-compose version 1.25.3, build d4d1b42b
```

范例：

```bash
#默认查找的文件 docker-compose.yml, docker-compose.yaml, compose.yml, compose.yaml
[root@ubuntu2204 ~]#docker-compose  ps
ERROR:
Can't find a suitable configuration file in this directory or any
parent. Are you in the right directory?
Supported filenames: docker-compose.yml, docker-compose.yaml,
compose.yml, compose.yaml
```

范例：

```bash
[root@ubuntu2204 ~]#docker compose  ls
NAME                STATUS              CONFIG FILES
nginx               running(1)          /data/docker-compose/nginx/docker-
compose.yaml
wordpress           running(2)          /data/docker-compose/wordpress/docker-
compose.yml
[root@ubuntu2204 wordpress]#docker-compose ps
NAME        IMAGE                     COMMAND
SERVICE     CREATED         STATUS         PORTS
mysql       registry.cn-beijing.aliyuncs.com/bowenxiaochun/mysql:8.0.29-oracle
"docker-entrypoint.sh mysqld"               mysql       7 minutes ago   Up 4
seconds   3306/tcp, 33060/tcp
wordpress   registry.cn-beijing.aliyuncs.com/bowenxiaochun/wordpress:php8.2-apache
"docker-entrypoint.sh apache2-foreground"   wordpress   7 minutes ago   Up 4
seconds   0.0.0.0:8080->80/tcp, :::8080->80/tcp
```

### docker compose 文件格式

官方文档:  https://docs.docker.com/compose/compose-file/

docker compose 文件是一个yaml格式的文件，所以注意行首的缩进很严格

注意: docker compose 其实也支持json文件格式, 比如: docker compose -f docker-compose.json up

<https://docs.docker.com/compose/faq/#can-i-use-json-instead-of-yaml-for-my-compose-file>

默认docker-compose命令会调用当前目录下的docker-compose.yml的文件，因此一般执行dockercompose命令前先进入docker-compose.yml文件所在目录

docker compose文件的格式很不同版本，版本不同，语法和格式有所不同，参看以下列表

Compose file format Docker Engine release

3.7 18.06.0+

3.6 18.02.0+

3.5 17.12.0+

3.4 17.09.0+

3.3 17.06.0+

3.2 17.04.0+

3.1 1.13.1+

3.0 1.13.0+

2.4 17.12.0+

2.3 17.06.0+

2.2 1.13.0+

2.1 1.12.0+

2.0 1.10.0+

1.0 1.9.1.+

docker compose版本众多，以下通过具体示例说明docker compose的使用方法

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/18-introduction-to-docker-compose.html' | relative_url }}">← Previous: Introduction to Docker Compose</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/20-starting-a-single-container-with-docker-compose.html' | relative_url }}">Next: Starting a Single Container with Docker Compose →</a>
</nav>
