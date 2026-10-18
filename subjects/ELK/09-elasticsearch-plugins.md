---
layout: default
title: "ELK 日志分析 · Elasticsearch 插件"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 09 Elasticsearch 插件
### 2.5 Elasticsearch 插件

通过使用各种插件可以实现对 ES 集群的状态监控, 数据访问, 管理配置等功能

ES集群状态:

green 绿色状态:表示集群各节点运行正常，而且没有丢失任何数据，各主分片和副本分片都运行正常 yellow 黄色状态:表示由于某个节点宕机或者其他情况引起的，node节点无法连接、所有主分片都正常分配,有副本分片丢失，但是还没有丢失任何数据 red 红色状态:表示由于某个节点宕机或者其他情况引起的主分片丢失及数据丢失,但仍可读取数据和存储

监控下面两个条件都满足才是正常的状态

集群状态为 green 所有节点都启动

### Head 插件

### Head 介绍

Head 是一个 ES 在生产较为常用的插件，目前此插件更新较慢，还是2018年4月的版本

git地址：https://github.com/mobz/elasticsearch-head

![ELK 日志分析第 84 页插图](assets/img-2469bb5ef41e63ed.png)

三种安装方法

编译安装 Docker 浏览器插件

### 编译安装

2.5.1.2.1 安装 Head 插件前准备

注意: 如果使用浏览器插件,则无需此步

修改elasticsearch节点的服务配置文件，开启跨域访问支持，然后重启elasticsearch服务

官方文档:

<https://www.elastic.co/guide/en/elasticsearch/reference/6.8/modules-http.html>

范例:

```bash
[root@es-node1 ~]# vim /etc/elasticsearch/elasticsearch.yml
#在文件最后添加下面两行
http.cors.enabled: true      #开启支持跨域访问
http.cors.allow-origin: "*"   #指定允许访问范围
[root@es-node1 ~]# systemctl restart elasticsearch
```

2.5.1.2.2 服务方式启动

在elasticsearch 5.x版本以后不再支持直接安装head插件，而是通过服务启动

此安装方式通过 npm 工具实现

npm(Node Package Manager)是和NodeJS一起安装的包管理和分发工具，使用npm 可以很方便让 JavaScript开发者下载、安装、上传以及管理已经安装的相关包。

范例: CentOS 7 安装 Head 插件

```bash
[root@es-node1 ~]# yum install -y npm git
#因为使用了nodejs,建议用下面方式加速
[root@es-node1 ~]#apt install npm
[root@es-node1 ~]#npm config get registry
https://registry.npmjs.org/
[root@es-node1 ~]#npm config set registry  https://registry.npm.taobao.org
[root@es-node1 ~]#npm config get registry
https://registry.npm.taobao.org/
[root@es-node1 ~]# cd /usr/local/src/
[root@es-node1 src]#git clone git://github.com/mobz/elasticsearch-head.git
[root@es-node1 src]# cd elasticsearch-head/
[root@es-node1 elasticsearch-head]# npm install grunt -save
[root@es-node2 elasticsearch-head]# ll node_modules/grunt #确认生成文件
[root@es-node1 elasticsearch-head]# npm install #执行安装
[root@es-node1 elasticsearch-head]# npm run start  & #后台启动服务
```

范例: Ubuntu 安装 Head 插件

```bash
[root@es-node1 ~]#apt -y install npm
#因为使用了nodejs,建议用下面方式加速
[root@es-node1 ~]#npm config get registry
https://registry.npmjs.org/
[root@es-node1 ~]#npm config set registry  https://registry.npm.taobao.org
[root@es-node1 ~]#npm config get registry
https://registry.npm.taobao.org/
[root@es-node1 ~]# git clone git://github.com/mobz/elasticsearch-head.git
[root@es-node1 ~]# cd elasticsearch-head/
[root@es-node1 elasticsearch-head]# npm install #执行安装
[root@es-node1 elasticsearch-head]# npm run start  & #后台启动服务
```

### Docker 方式启动 Head 插件

```bash
[root@es-node1 ~]#docker run -d -p 9100:9100 --name head  mobz/elasticsearch-
head:5
#安装完毕后,访问:http://localhost:9100
```

![ELK 日志分析第 86 页插图](assets/img-87d3133664fb4698.png)

### 浏览器安装插件

2.5.1.4.1 在线安装

从谷歌应用商店下载安装插件,支持chrome和edge浏览器

注意: 需要科学上网

谷歌应用商店，搜索 elasticsearch-head，进行安装

<https://chrome.google.com/webstore/category/extensions?hl=en-US>

<https://chrome.google.com/webstore/detail/multi-elasticsearch-head/cpmmilfkofbeimbmgiclohpodggeheim?hl=en-US>

<https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm/related>

![ELK 日志分析第 87 页插图](assets/img-f0a027496cfe5a9e.png)

![ELK 日志分析第 87 页插图](assets/img-3084b3c33c5ddfbd.png)

![ELK 日志分析第 88 页插图](assets/img-90cbcb3b97248ae1.png)

![ELK 日志分析第 88 页插图](assets/img-36b814a1f2e9eba3.png)

安装完插件,点击图标就可以打开插件

![ELK 日志分析第 89 页插图](assets/img-ea90ca645e9e2535.png)

2.5.1.4.2 离线安装

先下载Head插件文件,再离线安装，支持Chrome 内核的各种浏览器，比如：edge

注意：要打开开发者模式

![ELK 日志分析第 89 页插图](assets/img-4eef921a7628415f.png)

![ELK 日志分析第 89 页插图](assets/img-349b05ba27245b3c.png)

![ELK 日志分析第 90 页插图](assets/img-39e24dc7097fc4dc.png)

![ELK 日志分析第 90 页插图](assets/img-946b2423379116f1.png)

![ELK 日志分析第 90 页插图](assets/img-2f55b2ba0b3bb5ce.png)

![ELK 日志分析第 90 页插图](assets/img-9be08d1c628b70dd.png)

### 利用 Head 插件观察状态

head 插件中集群状态说明

状态颜色说明:

绿色:索引数据完整,副本满足,所有条件都满足黄色:索引数据完整,副本不满足,即数据没有丢失,但副本丢失,可能会影响容错功能红色:有索引数据不完整的情况,即数据丢失紫色:有数据分片正在同步过程中

0 表示分片的片shard编号

粗体线框为主分片,细体线框为副本分片

星表示主master节点,圆点表示slave工作节点

![ELK 日志分析第 91 页插图](assets/img-608abbfcc49e9a68.png)

添加索引后,可以观察到下面显示

![ELK 日志分析第 91 页插图](assets/img-863e07c20f50e13b.png)

![ELK 日志分析第 91 页插图](assets/img-c94f706a6012c592.png)

![ELK 日志分析第 92 页插图](assets/img-4cae311f84dce1f0.png)

![ELK 日志分析第 92 页插图](assets/img-9616cc2bf39464b5.png)

![ELK 日志分析第 92 页插图](assets/img-e115e01f8b2dc129.png)

![ELK 日志分析第 93 页插图](assets/img-b86db6d6966fd6d3.png)

```bash
[root@node3 ~]#systemctl stop  elasticsearch.service
```

![ELK 日志分析第 93 页插图](assets/img-a93650aad66fd9bf.png)

```bash
[root@node3 ~]#systemctl start  elasticsearch.service
```

![ELK 日志分析第 93 页插图](assets/img-da31e6ae81cdb345.png)

有时出现紫色的同步状态

![ELK 日志分析第 94 页插图](assets/img-94358e4718777b2d.png)

index2数据库是2分片3副本

![ELK 日志分析第 94 页插图](assets/img-89d5cf7d7babe318.png)

### Cerebro 插件

### Cerebro 介绍

![ELK 日志分析第 94 页插图](assets/img-e2ee5fd51f192732.png)

Cerebro 是开源的 elasticsearch 集群 Web 管理程序，此工具应用也很广泛，此项目升级比 Head 频繁

当前最新版本为Apr 10, 2021发布的 v0.9.4

Cerebro v0.9.3 版本之前需要 java1.8 或者更高版本

Cerebro v0.9.4 版本更高版本需要 Java11

github链接：

<https://github.com/lmenezes/cerebro>

![ELK 日志分析第 95 页插图](assets/img-a6caee2590807819.png)

### 包安装

注意：安装cerebro内存建议大于3G以上

```bash
#依赖JDK，JRE-21不支持
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-11-jre
[root@ubuntu2004 ~]#apt update && apt -y install openjdk-11-jdk
#Java8实际也支持
[root@ubuntu2004 ~]#apt -y install openjdk-8-jdk
#下载包,官方提供了DEB和RPM包
[root@ubuntu2004 ~]#wget
https://github.com/lmenezes/cerebro/releases/download/v0.9.4/cerebro_0.9.4_all.d
eb
#安装
[root@ubuntu2004 ~]#dpkg -i cerebro_0.9.4_all.deb
#启动
[root@ubuntu2004 ~]#systemctl start cerebro.service
#默认服务无法启动，端口无法打开
[root@ubuntu2004 ~]#ss -ntlp|grep 9000
#默认无法启动,查看日志,可以看到以下提示,原因是默认cerebro.db文件所有目录没有权限导致
[root@ubuntu2004 ~]#journalctl  -u cerebro
Caused by: java.sql.SQLException: opening db: './cerebro.db': 权限不够
#修改配置文件
[root@ubuntu2004 ~]#vim /etc/cerebro/application.conf
data.path: "/var/lib/cerebro/cerebro.db" #取消此行注释
#data.path = "./cerebro.db"  #注释此行，默认路径是/usr/share/cerebro/cerebro.db
#此目录自动生成
[root@ubuntu2204 ~]#ll -d /var/lib/cerebro
drwxr-xr-x 2 cerebro cerebro 4096  4月 10  2021 /var/lib/cerebro/
[root@ubuntu2004 ~]#systemctl restart  cerebro.service
active
#默认监听9000端口
[root@ubuntu2004 ~]#ss -ntlp|grep 9000
LISTEN   0   100   *:9000         *:*        users:(("java",pid=26333,fd=155))
#访问下面链接地址
http://cerebro.bowen.org:9000
#在Node address输入框中输入任意ES集群节点的地址
http://127.0.0.1:9200
```

![ELK 日志分析第 96 页插图](assets/img-4af0c49dbc990049.png)

单节点ES显示如下

![ELK 日志分析第 97 页插图](assets/img-2242213160d0f100.png)

显示特殊索引

![ELK 日志分析第 97 页插图](assets/img-a040bbbb5c6f8da7.png)

![ELK 日志分析第 97 页插图](assets/img-95de6799bcd5fda2.png)

三节点集群显示如下，实心的五角星表示Master节点

![ELK 日志分析第 98 页插图](assets/img-6e03b16a5aafa37a.png)

如果数据丢失，会显示红色

![ELK 日志分析第 98 页插图](assets/img-8b85ffe0f052cced.png)

### 二进制安装

注意：内存建议大于3G以上

```json
#先安装jdk
[root@es-node1 ~]#apt update && apt -y install  openjdk-8-jdk
[root@es-node1 ~]#apt update && apt -y install  openjdk-11-jdk
#下载文件
[root@es-node1 ~]#wget
https://github.com/lmenezes/cerebro/releases/download/v0.9.4/cerebro-0.9.4.tgz
[root@es-node1 ~]#wget
https://github.com/lmenezes/cerebro/releases/download/v0.9.3/cerebro-0.9.3.tgz
[root@es-node1 ~]#tar xvf cerebro-0.9.3.tgz -C /usr/local/
[root@es-node1 ~]#ln -s /usr/local/cerebro-0.9.3/ /usr/local/cerebro
#修改配置
[root@es-node1 ~]#vim /usr/local/cerebro/conf/application.conf
hosts = [
{
host = "http://10.0.0.101:9200" #修改此行,指向ES的地址
name = "es-cluster"             #修改此行
#  headers-whitelist = [ "x-proxy-user", "x-proxy-roles", "X-Forwarded-For" ]
#}
# Example of host with authentication
#{
#  host = "http://some-authenticated-host:9200"
#  name = "Secured Cluster"
#  auth = {
#    username = "username"
#    password = "secret-password"
#  }
}
]
#启动插件
[root@es-node1 ~]#/usr/local/cerebro/bin/cerebro &
[info] play.api.Play - Application started (Prod) (no global state)
[info] p.c.s.AkkaHttpServer - Listening for HTTP on /0:0:0:0:0:0:0:0:9000
......
#打开浏览器访问http://10.0.0.101:9000 可看到下面提示
```

![ELK 日志分析第 99 页插图](assets/img-8a848ba502b78359.png)

点击集群名es-cluster 就可以进入下面界面

![ELK 日志分析第 100 页插图](assets/img-fe5f55856c1291e8.png)

![ELK 日志分析第 100 页插图](assets/img-284dcc8e266a0747.png)

### Docker 运行

<https://hub.docker.com/r/lmenezes/cerebro>

范例:

```text
docker run -p 9000:9000 lmenezes/cerebro
docker run -p 9000:9000 lmenezes/cerebro:0.8.3
docker run -p 9000:9000 --env-file env-ldap  lmenezes/cerebro
#configure a custom port for cerebro by using the CEREBRO_PORT environment
variable. This defaults to 9000.
docker run -e CEREBRO_PORT=8080 -p 8080:8080 lmenezes/cerebro
```

### 其它插件

Edge 浏览器应用中还有其它ES插件,可以使用

![ELK 日志分析第 100 页插图](assets/img-cf9e2abb23fe0dab.png)

### 利用插件管理索引

### 利用 cerebro 插件创建索引

![ELK 日志分析第 101 页插图](assets/img-605ed4f426e2a638.png)

建议shard分片数配置为ELK服务器的数量,副本为1表示对数据有一个备份

![ELK 日志分析第 101 页插图](assets/img-10eca26d77c1dd7a.png)

![ELK 日志分析第 102 页插图](assets/img-108c9dcb7ca36039.png)

![ELK 日志分析第 102 页插图](assets/img-220f63d730d44384.png)

再创建一个索引，不指定分片信息

![ELK 日志分析第 103 页插图](assets/img-3ac7ff4764389cf7.png)

### 利用 cerebro 插件验证分片

ES7.0版本默认分片为1个，并且只有1个副本

ES6.X版本前默认分片为5个副本1个

![ELK 日志分析第 103 页插图](assets/img-4154972fec4cc561.png)

![ELK 日志分析第 104 页插图](assets/img-e05205cfa6e3147c.png)

### 利用 head 插件验证

![ELK 日志分析第 104 页插图](assets/img-05554b04485bb372.png)

观察下面2外面的框比较粗，即为primary分片

![ELK 日志分析第 105 页插图](assets/img-0e4aa5338a38d973.png)

### 利用 head 插件删除索引

![ELK 日志分析第 105 页插图](assets/img-0075423c6851a361.png)

### 在各个节点主机自动生成下面目录

```bash
[root@es-node1 ~]#ll /data/es-data/nodes/0/indices/
total 16
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39
32A1_WR4QEKmTfKFe61JjA/
drwxr-xr-x 6 elasticsearch elasticsearch 4096 Jan 26 13:31
TPUrqHNdRT2lCNVPMPF2eg/
[root@es-node2 ~]#ll /data/es-data/nodes/0/indices/
total 12
drwxr-xr-x 3 elasticsearch elasticsearch 4096 Jan 26 13:31 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 7 elasticsearch elasticsearch 4096 Jan 26 13:32
TPUrqHNdRT2lCNVPMPF2eg/
[root@es-node3 ~]#ll /data/es-data/nodes/0/indices/
total 16
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39
32A1_WR4QEKmTfKFe61JjA/
drwxr-xr-x 6 elasticsearch elasticsearch 4096 Jan 26 13:31
TPUrqHNdRT2lCNVPMPF2eg/
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/08-accessing-elasticsearch.html' | relative_url }}">← Previous: Accessing Elasticsearch</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/10-how-elasticsearch-clusters-work.html' | relative_url }}">Next: How Elasticsearch Clusters Work →</a>
</nav>
