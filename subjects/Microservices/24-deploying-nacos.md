---
layout: default
title: "微服务架构 · Nacos 部署"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 24 Nacos 部署
### 4.2 Nacos 部署

### Nacos 部署说明

<https://nacos.io/zh-cn/docs/v2/quickstart/quick-start.html>

版本选择

当前推荐的稳定版本为 2.X

<https://github.com/alibaba/nacos/releases>

Nacos 支持三种部署模式

单机模式 - 用于测试和单机试用集群模式 - 用于生产环境，确保高可用多集群模式 - 用于多数据中心场景

环境准备

安装好 JDK，需要 1.8 及其以上版本建议: 2核 CPU / 4G 内存 及其以上建议: 生产环境 3 个节点 及其以上

### Nacos 单机部署

<https://nacos.io/zh-cn/docs/quick-start.html>

### 预备环境准备

Nacos 依赖 Java 环境来运行。如果您是从代码开始构建并运行Nacos，还需要为此配置 Maven环境，请确保是在以下版本环境中安装使用:

1. 64 bit OS，支持 Linux/Unix/Mac/Windows，推荐选用 Linux/Unix/Mac。

2. 64 bit JDK 1.8+；下载 & 配置。

3. Maven 3.2.x+；下载 & 配置。

### 下载源码或者二进制安装包

你可以通过源码和发行包两种方式来获取 Nacos。

4.2.2.2.1 从 Github 上下载源码编译安装方式

```text
git clone https://github.com/alibaba/nacos.git
cd nacos/
mvn -Prelease-nacos -Dmaven.test.skip=true clean install -U
ls -al distribution/target/
// change the $version to your actual path
cd distribution/target/nacos-server-$version/nacos/bin
```

4.2.2.2.2 下载编译后二进制压缩包方式

您可以从 最新稳定版本 下载 nacos-server-$version.zip 包。

```text
unzip nacos-server-$version.zip 或者 tar -xvf nacos-server-$version.tar.gz
cd nacos/bin
```

范例: 二进制安装

```bash
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-21-jdk
[root@ubuntu2404 ~]#java -version
openjdk version "21.0.6" 2025-01-21
OpenJDK Runtime Environment (build 21.0.6+7-Ubuntu-124.04.1)
OpenJDK 64-Bit Server VM (build 21.0.6+7-Ubuntu-124.04.1, mixed mode, sharing)
[root@ubuntu2204 ~]#apt update && apt -y install openjdk-17-jdk
[root@ubuntu2204 ~]#apt update && apt -y install openjdk-11-jdk
#或者
[root@ubuntu2204 ~]#apt update && apt -y install openjdk-8-jdk
[root@ubuntu2204 ~]#wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.tar.gz
[root@ubuntu2204 ~]#tar xf nacos-server-2.2.3.tar.gz -C /usr/local/
[root@ubuntu2204 ~]#ls /usr/local/nacos/
bin  conf  data  LICENSE  logs  NOTICE  target
[root@ubuntu2204 ~]#ls /usr/local/nacos/bin/
shutdown.cmd  shutdown.sh  startup.cmd  startup.sh
[root@ubuntu2204 ~]#ls /usr/local/nacos/target/
nacos-server.jar
[root@ubuntu2204 ~]#ls /usr/local/nacos/conf/
1.4.0-ipv6_support-update.sql  application.properties          cluster.conf.example  mysql-schema.sql
announcement.conf              application.properties.example  derby-schema.sql      nacos-logback.xml
#修改配置，可选
[root@ubuntu2204 ~]#vi /usr/local/nacos/conf/application.properties
#修改默认的访问URL路径
#server.servlet.contextPath=/nacos
server.servlet.contextPath=/
#***********Expose prometheus and health **************************#
#取消下面行注释开启prometheus监控，指标路径：http://127.0.0.1:8848/nacos/actuator/prometheus
management.endpoints.web.exposure.include=prometheus,health
#添加PATH变量中，可选
[root@ubuntu2204 ~]#echo 'PATH=/usr/local/nacos/bin:$PATH' >> /etc/profile
[root@ubuntu2204 ~]#. /etc/profile
```

### 启动和关闭服务器

注：Nacos的运行建议至少在2C4G 60G的机器配置下运行。

4.2.2.3.1 启动服务

Linux/Unix/Mac

启动命令(standalone代表着单机模式运行，非集群模式):

```text
sh startup.sh -m standalone
```

如果您使用的是ubuntu系统，或者运行脚本报错提示[[符号找不到，可尝试如下运行：

```text
bash startup.sh -m standalone
```

Windows

启动命令(standalone代表着单机模式运行，非集群模式):

```text
startup.cmd -m standalone
```

范例:  Nacos 2.X 之前版本启动

```bash
#启动
[root@ubuntu2204 ~]#/usr/local/nacos/bin/startup.sh -m standalone
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-
amd64/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/lib/ext  -Xms512m -Xmx512m -Xmn256m -
Dnacos.standalone=true -Dnacos.member.list= -Xloggc:/usr/local/nacos/logs/nacos_gc.log -verbose:gc -
XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -
XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-header-size=524288
nacos is starting with standalone
nacos is starting，you can check the /usr/local/nacos/logs/start.out
[root@ubuntu2204 ~]#tail -f /usr/local/nacos/logs/start.out
'   : |  ; .' ," .--.; |'   ; :__|   :    |  `----.   \
|   | '`--'  /  /  ,.  |'   | '.'|\   \  /  /  /`--'  /
'   : |     ;  :   .'   \   :    : `----'  '--'.     /
;   |.'     |  ,     .-./\   \  /            `--'---'
'---'        `--`---'     `----'
2023-06-04 17:12:25,379 INFO Tomcat initialized with port(s): 8848 (http)
2023-06-04 17:12:25,468 INFO Root WebApplicationContext: initialization completed in 3089 ms
2023-06-04 17:12:30,773 INFO Adding welcome page: class path resource [static/index.html]
2023-06-04 17:12:31,344 WARN You are asking Spring Security to ignore Ant [pattern='/**']. This is not
recommended -- please use permitAll via HttpSecurity#authorizeHttpRequests instead.
2023-06-04 17:12:31,345 INFO Will not secure Ant [pattern='/**']
2023-06-04 17:12:31,378 INFO Will secure any request with
[org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@754777cd,
org.springframework.security.web.context.SecurityContextPersistenceFilter@4b6166aa,
org.springframework.security.web.header.HeaderWriterFilter@4089713,
org.springframework.security.web.csrf.CsrfFilter@7cbee484,
org.springframework.security.web.authentication.logout.LogoutFilter@791cbf87,
org.springframework.security.web.savedrequest.RequestCacheAwareFilter@4fd4cae3,
org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@a1217f9,
org.springframework.security.web.authentication.AnonymousAuthenticationFilter@2b52c0d6,
org.springframework.security.web.session.SessionManagementFilter@7807ac2c,
org.springframework.security.web.access.ExceptionTranslationFilter@62923ee6]
2023-06-04 17:12:31,448 INFO Exposing 1 endpoint(s) beneath base path '/actuator'
2023-06-04 17:12:31,511 INFO Tomcat started on port(s): 8848 (http) with context path '/nacos'
2023-06-04 17:12:31,549 INFO Nacos started successfully in stand alone mode. use embedded storage
2023-06-04 17:12:53,942 INFO Initializing Servlet 'dispatcherServlet'
2023-06-04 17:12:53,947 INFO Completed initialization in 5 ms
#查看端口
[root@ubuntu2204 ~]#ss -ntlp|grep java
LISTEN 0      4096               *:7848            *:*    users:(("java",pid=4336,fd=188))
LISTEN 0      100                *:8848            *:*    users:(("java",pid=4336,fd=230))
LISTEN 0      4096               *:9848            *:*    users:(("java",pid=4336,fd=185))
LISTEN 0      4096               *:9849            *:*    users:(("java",pid=4336,fd=186))
```

范例: Nacos 3.X 以后版本默认要求必须开启鉴权才能启动

```bash
#Nacos 3.0.0 首次启动时需要输入鉴权的相关信息
[root@ubuntu2404 ~]#/usr/local/nacos/bin/startup.sh -m standalone
`nacos.core.auth.server.identity.key` is missing, please set: VGhpc0lzTXlDdXN0b21TZWNyZXRLZXkwMTIzNDU2Nzg=
`nacos.core.auth.server.identity.key` is missing, please set: bowen
`nacos.core.auth.server.identity.key` Updated:
nacos.core.auth.server.identity.key=bowen
----------------------------------
`nacos.core.auth.server.identity.value` is missing, please set: bowen
`nacos.core.auth.server.identity.value` Updated:
nacos.core.auth.server.identity.value=bowen
----------------------------------
/usr/lib/jvm/java-21-openjdk-amd64/bin/java    -Xms512m -Xmx512m -Xmn256m -Dnacos.standalone=true -
Dnacos.member.list= -Xlog:gc*:file=/usr/local/nacos/logs/nacos_gc.log:time,tags:filecount=10,filesize=100m -
Dnacos.deployment.type=merged -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-request-header-size=524288
nacos is starting with standalone
nacos is starting. you can check the /usr/local/nacos/logs/startup.log
#查看文件中添加鉴权信息
[root@ubuntu2404 ~]#vim /usr/local/nacos/conf/application.properties
nacos.core.auth.server.identity.key=bowen
nacos.core.auth.server.identity.value=bowen
...........
nacos.core.auth.plugin.nacos.token.secret.key=VGhpc0lzTXlDdXN0b21TZWNyZXRLZXkwMTIzNDU2Nzg=
.......
#Nacos 3.0.0默认控制台使用8080端口,而8848端口用于API访问
[root@ubuntu2404 ~]#ss -ntlp|grep java
LISTEN 0      100                *:8080            *:*    users:(("java",pid=57765,fd=227))
LISTEN 0      4096               *:9848            *:*    users:(("java",pid=57765,fd=165))
LISTEN 0      4096               *:9849            *:*    users:(("java",pid=57765,fd=166))
LISTEN 0      4096               *:7848            *:*    users:(("java",pid=57765,fd=167))
LISTEN 0      100                *:8848            *:*    users:(("java",pid=57765,fd=222))
```

4.2.2.3.2 关闭服务

Linux/Unix/Mac

```text
sh shutdown.sh
```

Windows

```text
shutdown.cmd
```

或者双击shutdown.cmd运行文件。

4.2.2.3.3 准备Sevice文件

```bash
[root@ubuntu2404 ~]#id nacos &> /dev/null || useradd -r -s /sbin/nologin nacos
[root@ubuntu2404 ~]#chown -R nacos: /usr/local/nacos/
[root@ubuntu2404 ~]#cat >  /lib/systemd/system/nacos.service
[Unit]
Description=nacos.service
After=network.target
[Service]
Type=forking
ExecStart=/usr/local/nacos/bin/startup.sh -m standalone
ExecStop=/usr/local/nacos/bin/shutdown.sh
User=nacos
Group=nacos
[Install]
WantedBy=multi-user.target
[root@ubuntu2404 ~]#systemctl daemon-reload
[root@ubuntu2404 ~]#systemctl enable --now  nacos.service
```

### 服务注册&发现和配置管理

注意：启用验证后，将无法直接用下面的curl命令访问

服务注册

```text
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?
serviceName=nacos.bowen.serviceName&ip=1.2.3.4&port=8080'
```

服务发现

```text
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.bowen.serviceName'
```

发布配置

```text
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=HelloWorld"
```

获取配置

```text
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

范例：将配置文件上传生成配置信息

```bash
curl --location --request POST 'http://127.0.0.1:8848/nacos/v1/cs/configs?import=true&namespace=public' \
--form 'policy=OVERWRITE' --form 'file=@"/PATH/ZIP_FILE"'
#示例：将配置文件nacos_config.zip上传到dev名称空间
[root@ubuntu2204 ~]#curl --location --request POST 'http://127.0.0.1:8848/nacos/v1/cs/configs?
import=true&namespace=dev'        --form 'policy=OVERWRITE' --form 'file=@"./nacos_config.zip"'
```

### Web 访问

```text
#从3.0开始
http://nacos.bowen.org:8080
```

首次登录时需要初始化设置密码

![微服务技术第 89 页插图](assets/img-5f40ca594a16e3c0.png)

![微服务技术第 90 页插图](assets/img-5110b07d13de13ed.png)

![微服务技术第 90 页插图](assets/img-1b379e9ae2c98ff3.png)

```text
#2.X之前
http://nacos.bowen.org:8848/nacos/
```

![微服务技术第 91 页插图](assets/img-119ea7f9c1c5a845.png)

![微服务技术第 91 页插图](assets/img-5f3262705348ccf1.png)

### 单机模式支持 MySQL

<https://nacos.io/zh-cn/docs/deployment.html#MySQL的表结构>

<https://gitee.com/lbtooth/RuoYi-Cloud/blob/master/docker/mysql/db/ry_config_20231204.sql>

在0.7版本之前，在单机模式时nacos使用嵌入式数据库实现数据的存储，不方便观察数据存储的基本情况。

0.7版本增加了支持MySQL数据源能力，具体的操作步骤：

安装数据库，版本要求：5.6.5+ 创建数据库nacos和用户nacos，并授权执行数据库初始化脚本 mysql-schema.sql 修改conf/application.properties文件，增加支持MySQL数据源配置（目前只支持mysql），添加mysql数据源的url、用户名和密码。

```text
spring.datasource.platform=mysql
db.num=1
db.url.0=jdbc:mysql://127.0.0.1:3306/nacos?
characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true
db.user=nacos
db.password=123456
```

再以单机模式启动nacos，nacos所有写嵌入式数据库的数据都写到了mysql

范例: 单机模式支持 MySQL,内存至少3G

```bash
[root@ubuntu2204 ~]#apt update && apt -y install mysql-server
[root@ubuntu2204 ~]#sed -i '/127.0.0.1/s/^/#/' /etc/mysql/mysql.conf.d/mysqld.cnf
[root@ubuntu2204 ~]#systemctl restart mysql
[root@ubuntu2204 ~]#ss -tnlp|grep mysql
LISTEN 0      151                *:3306             *:*    users:(("mysqld",pid=5875,fd=33))
LISTEN 0      70                 *:33060            *:*    users:(("mysqld",pid=5875,fd=21))
[root@ubuntu2204 ~]#mysql
Server version: 8.0.33-0ubuntu0.22.04.4 (Ubuntu)
mysql> create database nacos;
#需要指定验证插件，不支持默认插件caching_sha2_password
mysql> create user nacos@'127.0.0.1' identified with  mysql_native_password by '123456';
mysql> grant all on nacos.* to nacos@'127.0.0.1';
#生成表结构
[root@ubuntu2204 ~]#mysql -unacos -p123456 -h127.0.0.1  nacos  < /usr/local/nacos/conf/mysql-schema.sql
[root@ubuntu2204 ~]#vim /usr/local/nacos/conf/application.properties
#*************** Config Module Related Configurations ***************#
### If use MySQL as datasource:
### Deprecated configuration property, it is recommended to use `spring.sql.init.platform` replaced.
# spring.datasource.platform=mysql
# spring.sql.init.platform=mysql
spring.sql.init.platform=mysql #加此行
### Count of DB:
# db.num=1
db.num=1                       #加此行
### Connect URL of DB:
# db.url.0=jdbc:mysql://127.0.0.1:3306/nacos?
characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=true&useSSL=false&
serverTimezone=UTC
# db.user.0=nacos
# db.password.0=nacos
#加下面三行
db.url.0=jdbc:mysql://127.0.0.1:3306/nacos?
characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode
=true&useSSL=false&serverTimezone=UTC
db.user.0=nacos
db.password.0=123456
#如果启动,先关闭服务，重新启动服务
[root@ubuntu2204 ~]#/usr/local/nacos/bin/shutdown.sh
The nacosServer(4336) is running...
Send shutdown request to nacosServer(4336) OK
[root@ubuntu2204 ~]#/usr/local/nacos/bin/startup.sh -m standalone
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-
amd64/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/lib/ext  -Xms512m -Xmx512m -Xmn256m -
Dnacos.standalone=true -Dnacos.member.list= -Xloggc:/usr/local/nacos/logs/nacos_gc.log -verbose:gc -
XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -
XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-header-size=524288
nacos is starting with standalone
nacos is starting，you can check the /usr/local/nacos/logs/start.out
#查看日志
[root@ubuntu2204 ~]#tail -f /usr/local/nacos/logs/start.out
,--.
,--.'|
,--,:  : |                                           Nacos 2.2.3
,`--.'`|  ' :                       ,---.               Running in stand alone mode, All function modules
|   :  :  | |                      '   ,'\   .--.--.    Port: 8848
:   |   \ | :  ,--.--.     ,---.  /   /   | /  /    '   Pid: 6587
|   : '  '; | /       \   /     \.   ; ,. :|  :  /`./   Console: http://10.0.0.200:8848/nacos/index.html
'   ' ;.    ;.--.  .-. | /    / ''   | |: :|  :  ;_
|   | | \   | \__\/: . ..    ' / '   | .; : \  \    `.      https://nacos.io
'   : |  ; .' ," .--.; |'   ; :__|   :    |  `----.   \
|   | '`--'  /  /  ,.  |'   | '.'|\   \  /  /  /`--'  /
'   : |     ;  :   .'   \   :    : `----'  '--'.     /
;   |.'     |  ,     .-./\   \  /            `--'---'
'---'        `--`---'     `----'
2023-06-04 17:30:59,801 INFO Tomcat initialized with port(s): 8848 (http)
2023-06-04 17:30:59,884 INFO Root WebApplicationContext: initialization completed in 3317 ms
2023-06-04 17:31:04,055 INFO Adding welcome page: class path resource [static/index.html]
2023-06-04 17:31:04,804 WARN You are asking Spring Security to ignore Ant [pattern='/**']. This is not
recommended -- please use permitAll via HttpSecurity#authorizeHttpRequests instead.
2023-06-04 17:31:04,805 INFO Will not secure Ant [pattern='/**']
2023-06-04 17:31:04,838 INFO Will secure any request with
[org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@ec0c838,
org.springframework.security.web.context.SecurityContextPersistenceFilter@f9b7332,
org.springframework.security.web.header.HeaderWriterFilter@2c177f9e,
org.springframework.security.web.csrf.CsrfFilter@290b1b2e,
org.springframework.security.web.authentication.logout.LogoutFilter@b672aa8,
org.springframework.security.web.savedrequest.RequestCacheAwareFilter@6fefce9e,
org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@1bdf8190,
org.springframework.security.web.authentication.AnonymousAuthenticationFilter@6e46d9f4,
org.springframework.security.web.session.SessionManagementFilter@209775a9,
org.springframework.security.web.access.ExceptionTranslationFilter@33617539]
2023-06-04 17:31:04,875 INFO Exposing 1 endpoint(s) beneath base path '/actuator'
2023-06-04 17:31:04,940 INFO Tomcat started on port(s): 8848 (http) with context path '/nacos'
2023-06-04 17:31:04,981 INFO Nacos started successfully in stand alone mode. use external storage
```

测试访问,可看到下面页面

<http://nacos.bowen.org:8848/nacos>

![微服务技术第 93 页插图](assets/img-83cd8a7b5ea718d1.png)

### 开启鉴权

注意：3.X 版本默认开启，2.X版本默认不开启

<https://nacos.io/zh-cn/docs/auth.html>

Nacos是一个内部微服务组件，需要在可信的内部网络中运行，不可暴露在公网环境，防止带来安全风险。

Nacos提供简单的鉴权实现，为防止业务错用的弱鉴权体系，不是防止恶意攻击的强鉴权体系。

如果运行在不可信的网络环境或者有强鉴权诉求，请参考官方简单实现做替换增强。

默认无需登录就可管理nacos,基于安全可以启用登录验证功能

非Docker环境

按照官方文档配置启动,默认是不需要登录的，这样会导致配置中心对外直接暴露。而启用鉴权之后，需要在使用用户名和密码登录之后，才能正常使用nacos。

开启鉴权之前，application.properties中的配置信息为：

```text
### If turn on auth system:
nacos.core.auth.enabled=false
```

开启鉴权之后，application.properties中的配置信息为：

```text
### If turn on auth system:
nacos.core.auth.system.type=nacos
nacos.core.auth.enabled=true
```

Docker环境

如果使用官方镜像，请在启动docker容器时，添加如下环境变量

```text
NACOS_AUTH_ENABLE=true
```

例如，可以通过如下命令运行开启了鉴权的容器:

```text
docker run --env PREFER_HOST_MODE=hostname --env MODE=standalone --env NACOS_AUTH_ENABLE=true -p 8848:8848
nacos/nacos-server
```

注意：启用验证后，将无法直接用curl命令访问,需要先获取Token才能访问

范例: Nacos 2.X 开启鉴权

```bash
#生成toke的值，至少32位，否则无法启动
[root@ubuntu2204 ~]#openssl rand -base64 33
YfmvRi6Kx8tuI+k0lRBr5nm2WNi1I5h0SFBREpPFZ36R
#修改配置文件,共四行内容
[root@ubuntu2204 ~]#vim /usr/local/nacos/conf/application.properties
#*************** Access Control Related Configurations ***************#
......
nacos.core.auth.system.type=nacos
#nacos.core.auth.enabled=false
nacos.core.auth.enabled=true  #修改此行为true
nacos.core.auth.server.identity.key=bowen    #指定值,否则无法启动
nacos.core.auth.server.identity.value=bowen  #指定值,否则无法启动
nacos.core.auth.plugin.nacos.token.secret.key=YfmvRi6Kx8tuI+k0lRBr5nm2WNi1I5h0SFBREpPFZ36R #添加前面生成的token的
值
#重启服务生效
[root@ubuntu2204 ~]#/usr/local/nacos/bin/shutdown.sh
[root@ubuntu2204 ~]#/usr/local/nacos/bin/startup.sh -m standalone
```

测试访问第一次登录需要指定nacos的新密码，默认用户名和密码都是nacos

<http://nacos.bowen.org:8848/nacos>

![微服务技术第 94 页插图](assets/img-f42e883946116ffd.png)

![微服务技术第 95 页插图](assets/img-514347d66b1a70b8.png)

修改密码

![微服务技术第 95 页插图](assets/img-65dc69857383a96b.png)

密码保存在nacos库中的users表中

```bash
[root@ubuntu2204 ~]#mysql -unacos -pnacos -h127.0.0.1  nacos -e 'select * from users'
mysql: [Warning] Using a password on the command line interface can be insecure.
+----------+--------------------------------------------------------------+---------+
| username | password                                                     | enabled |
+----------+--------------------------------------------------------------+---------+
| nacos    | $2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu |       1 |
+----------+--------------------------------------------------------------+---------+
```

后续访问需要经过鉴权后才能访问

```bash
#直接访问失败
[root@ubuntu2204 ~]#curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?
serviceName=nacos.bowen.serviceName&ip=1.2.3.4&port=8080'
#返回失败提示如下
{"timestamp":"2023-12-07T11:57:20.434+08:00","status":403,"error":"Forbidden","message":"user not
found!","path":"/nacos/v1/ns/instance"}
#登录验证,获取Token
[root@ubuntu2204 ~]#curl -X POST 'http://127.0.0.1:8848/nacos/v1/auth/login' -d
'username=nacos&password=nacos'
{"accessToken":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTcwMTkzOTA5M30.Bd1tCAxPXHDp_yxDYUfcDKmm0eWI2
6b0_gAyaN9i8mM","tokenTtl":18000,"globalAdmin":true,"username":"nacos"}
#利用Token访问
[root@ubuntu2204
~]#TOKEN=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTcwMTkzOTA5M30.Bd1tCAxPXHDp_yxDYUfcDKmm0eWI26b0_gAy
aN9i8mM
#服务注册
[root@ubuntu2204 ~]#curl -X POST "http://127.0.0.1:8848/nacos/v1/ns/instance?
accessToken=$TOKEN&serviceName=nacos.bowen.serviceName&ip=1.2.3.4&port=8080"
#后续服务访问需要在原URL后添加
&accessToken=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuYWNvcyIsImV4cCI6MTcwMTkzOTA5M30.Bd1tCAxPXHDp_yxDYUfcDKmm0eWI26b0
_gAyaN9i8mM
#服务发现
[root@ubuntu2204 ~]#curl -X GET "http://127.0.0.1:8848/nacos/v1/ns/instance/list?
accessToken=$TOKEN&serviceName=nacos.bowen.serviceName"
{"name":"DEFAULT_GROUP@@nacos.bowen.serviceName","groupName":"DEFAULT_GROUP","clusters":"","cacheMillis":10000,
"hosts":
[{"instanceId":"1.2.3.4#8080#DEFAULT#DEFAULT_GROUP@@nacos.bowen.serviceName","ip":"1.2.3.4","port":8080,"weight
":1.0,"healthy":true,"enabled":true,"ephemeral":true,"clusterName":"DEFAULT","serviceName":"DEFAULT_GROUP@@nac
os.bowen.serviceName","metadata":
{},"instanceHeartBeatInterval":5000,"instanceHeartBeatTimeOut":15000,"ipDeleteTimeout":30000,"instanceIdGenera
tor":"simple"}],"lastRefTime":1701921969338,"checksum":"","allIPs":false,"reachProtectionThreshold":false,"val
id":true}
#发布配置
[root@ubuntu2204 ~]#curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?
accessToken=$TOKEN&dataId=nacos.cfg.dataId&group=test&content=HelloWorld"
true
#获取配置
[root@ubuntu2204 ~]#curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?
accessToken=$TOKEN&dataId=nacos.cfg.dataId&group=test"
HelloWorld
#登录nacos控制台验证访问成功
```

![微服务技术第 96 页插图](assets/img-c14e328edf4ced1d.png)

![微服务技术第 96 页插图](assets/img-ed45a50b573e2ad6.png)

### Nacos 单机部署脚本

```bash
#!/bin/bash
#
#FileName:          install_nacos_single_node.sh
#Description:       The test script
#支持在线和离线安装,建议离线安装,在线可能下载很慢
NACOS_VERSION=2.4.3
#NACOS_VERSION=2.4.0.1
#NACOS_VERSION=2.3.2
#NACOS_VERSION=2.3.0
#NACOS_VERSION=2.2.3
NACOS_FILE=nacos-server-${NACOS_VERSION}.tar.gz
GITHUB_PROXY=https://mirror.ghproxy.com/
NACOS_URL=https://github.com/alibaba/nacos/releases/download/${NACOS_VERSION}/${NACOS_FILE}
INSTALL_DIR=/usr/local/nacos
HOST=`hostname -I|awk '{print $1}'`
.  /etc/os-release
color () {
RES_COL=60
MOVE_TO_COL="echo -en \\033[${RES_COL}G"
SETCOLOR_SUCCESS="echo -en \\033[1;32m"
SETCOLOR_FAILURE="echo -en \\033[1;31m"
SETCOLOR_WARNING="echo -en \\033[1;33m"
SETCOLOR_NORMAL="echo -en \E[0m"
echo -n "$1" && $MOVE_TO_COL
echo -n "["
if [ $2 = "success" -o $2 = "0" ] ;then
${SETCOLOR_SUCCESS}
echo -n $"  OK  "
elif [ $2 = "failure" -o $2 = "1"  ] ;then
${SETCOLOR_FAILURE}
echo -n $"FAILED"
else
${SETCOLOR_WARNING}
echo -n $"WARNING"
fi
${SETCOLOR_NORMAL}
echo -n "]"
echo
}
install_jdk() {
java -version &>/dev/null && { color "JDK 已安装!" 1 ; return;  }
if command -v yum &>/dev/null ; then
yum -y install java-1.8.0-openjdk-devel || { color "安装JDK失败!" 1; exit 1; }
elif command -v apt &>/dev/null ; then
apt update
apt install openjdk-17-jdk -y || { color "安装JDK失败!" 1; exit 1; }
#apt install openjdk-11-jdk -y || { color "安装JDK失败!" 1; exit 1; }
#apt install openjdk-8-jdk -y || { color "安装JDK失败!" 1; exit 1; }
else
color "不支持当前操作系统!" 1
exit 1
fi
java -version && { color "安装 JDK 完成!" 0 ; } || { color "安装JDK失败!" 1; exit 1; }
}
install_nacos() {
if [ -f ${NACOS_FILE} ] ;then
cp ${NACOS_FILE} /usr/local/src/
else
wget -P /usr/local/src/ --no-check-certificate ${GITHUB_PROXY}$NACOS_URL || { color  "下载失败!" 1
;exit ; }
fi
tar xf /usr/local/src/${NACOS_FILE} -C /usr/local
id nacos &> /dev/null || useradd -r -s /sbin/nologin nacos
chown -R nacos:nacos ${INSTALL_DIR}
echo "PATH=${INSTALL_DIR}/bin:$PATH" >>  /etc/profile
.  /etc/profile
start_nacos () {
cat > /lib/systemd/system/nacos.service <<EOF
[Unit]
Description=nacos.service
After=network.target
[Service]
Type=forking
#Environment=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/bin/startup.sh -m standalone
ExecStop=${INSTALL_DIR}/bin/shutdown.sh
User=nacos
Group=nacos
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now  nacos.service
systemctl is-active nacos.service
if [ $? -eq 0 ] ;then
color "nacos 安装成功!" 0
echo "-------------------------------------------------------------------"
echo -e "请访问链接: \E[32;1mhttp://$HOST:8848/nacos/\E[0m"
else
color "nacos 安装失败!" 1
exit 1
fi
}
}
```

```text
install_jdk
install_nacos
start_nacos
```

### Nacos 集群部署

### 集群部署说明

<https://nacos.io/zh-cn/docs/cluster-mode-quick-start.html>

集群部署架构

http://ip1:port/openAPI  直连ip模式，机器挂则需要修改ip才可以使用。 http://SLB:port/openAPI  挂载SLB模式(内网SLB，不可暴露到公网，以免带来安全风险)，直连SLB即可，下面挂server真实ip，可读性不好。 http://nacos.com:port/openAPI  域名 + SLB模式(内网SLB，不可暴露到公网，以免带来安全风险)，可读性好，而且换ip方便，推荐模式

deployDnsVipMode.jpg

DNS

domain (x.nacos.com) -> VIPs / SLBs

VIP / SLBVIP / SLBVIP / SLB

Internal VIPs or SLBs

IP 1 IP 2 IP 3

![微服务技术第 99 页插图](assets/img-11f68f76b363f4c2.png)

![微服务技术第 99 页插图](assets/img-11f68f76b363f4c2.png)

![微服务技术第 99 页插图](assets/img-11f68f76b363f4c2.png)

Nacos Server Cluster

![微服务技术第 99 页插图](assets/img-92cc51ebfc684107.jpeg)

以上三种模式，推荐使用第三种，即用户把所有服务列表放到一个vip下面，然后挂到一个域名下面

端口情况

端口与主端口的偏移量描述

8848 0 主端口，客户端、控制台及OpenAPI所使用的HTTP端口

9848 1000 客户端gRPC请求服务端端口，用于客户端向服务端发起连接和请求

9849 1001 服务端gRPC请求服务端端口，用于服务间同步等

7848 -1000 raft请求服务端端口，用于处理服务端间的Raft相关请求

注意：

使用VIP/nginx请求时，需要配置成TCP转发，不能配置http2转发，否则连接会被nginx断开 9849和7848端口为服务端之间的通信端口，请勿暴露到外部网络环境和客户端测。

### 部署案例

![微服务技术第 100 页插图](assets/img-fb384890261cceb2.png)

角色地址

VIP 10.0.0.100

haproxy1+keepalived 10.0.0.101

haproxy2+keepalived 10.0.0.102

nacos1 10.0.0.201

nacos2 10.0.0.202

nacos3 10.0.0.203

MySQL 10.0.0.200

4.2.3.2.1 预备环境准备

请确保是在环境中安装使用:

64 bit OS  Linux/Unix/Mac，推荐使用Linux系统 64 bit JDK 1.8+；下载. 配置 Maven 3.2.x+；下载 & 配置 3个或3个以上Nacos节点才能构成集群

4.2.3.2.2 下载源码或者安装包

你可以通过两种方式来获取 Nacos。

从 Github 上下载源码方式

```text
apt update && apt -y install git openjdk-8-jdk maven
git clone https://github.com/alibaba/nacos.git
unzip nacos-develop.zip
cd nacos-develop
mvn -Prelease-nacos clean install -U
cd distribution/target/nacos-server-2.3.0-SNAPSHOT/nacos/
```

下载编译后压缩包方式

```text
apt update && apt -y install openjdk-17-jdk
apt update && apt -y install openjdk-8-jdk
apt update && apt -y install openjdk-11-jdk
wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.tar.gz
tar xf nacos-server-2.2.3.tar.gz  -C /usr/local/
```

范例：二进制安装 Nacos

```bash
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-21-jdk
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-17-jdk
[root@ubuntu2204 ~]#apt update && apt -y install openjdk-11-jdk
[root@ubuntu2204 ~]#wget https://github.com/alibaba/nacos/releases/download/2.2.3/nacos-server-2.2.3.tar.gz
[root@ubuntu2204 ~]#tar xf nacos-server-2.2.3.tar.gz  -C /usr/local/
```

4.2.3.2.3 确定数据源

如果使用内置数据源

无需进行任何配置使用外置数据源

生产使用建议至少主备模式，或者采用高可用数据库。 初始化 MySQL 数据库 sql语句源文件

范例:  部署MySQL做为数据源

```bash
[root@ubuntu2204 ~]#apt update && apt -y install mysql-server
[root@ubuntu2204 ~]#sed -i '/127.0.0.1/s/^/#/' /etc/mysql/mysql.conf.d/mysqld.cnf
[root@ubuntu2204 ~]#systemctl restart mysql
[root@ubuntu2204 ~]#mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 25
Server version: 8.0.33-0ubuntu0.22.04.4 (Ubuntu)
mysql> create database nacos;
mysql> create user nacos@'10.0.0.%' identified with  mysql_native_password by '123456';
mysql> grant all on nacos.* to nacos@'10.0.0.%' ;
[root@node01 ~]#apt update && apt -y install mysql-client
[root@node01 ~]#mysql -unacos -p123456 -h10.0.0.200 nacos  < /usr/local/nacos/conf/mysql-schema.sql
```

4.2.3.2.4 配置集群配置文件

在nacos的解压目录nacos/的conf目录下，有配置文件cluster.conf，请每行配置成ip:port。

在所有集群节点修改下面文件

```bash
[root@node1 ~]#vim /usr/local/nacos/conf/cluster.conf
# ip:port
10.0.0.201:8848
10.0.0.202:8848
10.0.0.203:8848
#所有节点同步配置
[root@node1 ~]#scp /usr/local/nacos/conf/cluster.conf node2:/usr/local/nacos/conf/cluster.conf
[root@node1 ~]#scp /usr/local/nacos/conf/cluster.conf node3:/usr/local/nacos/conf/cluster.conf
```

4.2.3.2.5 修改 Nacos 配置文件 application.properties

如果使用内置数据源无需修改配置

如果使用MySQL数据源，在所有集群节点上需要执行下面操作

```bash
[root@node1 ~]#vi /usr/local/nacos/conf/application.properties
#*************** Config Module Related Configurations ***************#
### If use MySQL as datasource:
### Deprecated configuration property, it is recommended to use `spring.sql.init.platform` replaced.
# spring.datasource.platform=mysql
spring.sql.init.platform=mysql #取消注释
### Count of DB:
db.num=1             #取消注释
### Connect URL of DB:
#修改下面行
db.url.0=jdbc:mysql://10.0.0.200:3306/nacos?
characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useUnicode=tru
e&useSSL=false&serverTimezone=UTC
db.user.0=nacos
db.password.0=123456
[root@node1 ~]#cd /usr/local/nacos/conf/
[root@node1 conf]#ls
1.4.0-ipv6_support-update.sql  application.properties          cluster.conf          derby-schema.sql  nacos-
logback.xml
announcement.conf              application.properties.example  cluster.conf.example  mysql-schema.sql
#将配置同步到其它的节点
[root@node1 conf]#scp application.properties cluster.conf 10.0.0.202:/usr/local/nacos/conf
[root@node1 conf]#scp application.properties cluster.conf 10.0.0.203:/usr/local/nacos/conf
```

4.2.3.2.6 启动和关闭服务

Linux/Unix/Mac

集群模式启动

使用内置数据源

```text
/usr/local/nacos/bin/startup.sh -p embedded
```

使用外置数据源

```bash
#在所有集群节点执行启动
[root@node1 ~]#/usr/local/nacos/bin/startup.sh
[root@node1 ~]#cat /usr/local/nacos/logs/start.out
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-
amd64/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/lib/ext  -server -Xms2g -Xmx2g -Xmn1g -
XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=320m -XX:-OmitStackTraceInFastThrow -XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/usr/local/nacos/logs/java_heapdump.hprof -XX:-UseLargePages -Dnacos.member.list= -
Xloggc:/usr/local/nacos/logs/nacos_gc.log -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -
XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-header-size=524288
,--.
,--.'|
,--,:  : |                                           Nacos 2.2.3
,`--.'`|  ' :                       ,---.               Running in cluster mode, All function modules
|   :  :  | |                      '   ,'\   .--.--.    Port: 8848
:   |   \ | :  ,--.--.     ,---.  /   /   | /  /    '   Pid: 82453
|   : '  '; | /       \   /     \.   ; ,. :|  :  /`./   Console: http://10.0.0.201:8848/nacos/index.html
'   ' ;.    ;.--.  .-. | /    / ''   | |: :|  :  ;_
|   | | \   | \__\/: . ..    ' / '   | .; : \  \    `.      https://nacos.io
'   : |  ; .' ," .--.; |'   ; :__|   :    |  `----.   \
|   | '`--'  /  /  ,.  |'   | '.'|\   \  /  /  /`--'  /
'   : |     ;  :   .'   \   :    : `----'  '--'.     /
;   |.'     |  ,     .-./\   \  /            `--'---'
'---'        `--`---'     `----'
2023-06-03 22:32:23,223 INFO The server IP list of Nacos is [10.0.0.201:8848, 10.0.0.202:8848,
10.0.0.203:8848]
2023-06-03 22:32:24,228 INFO Nacos is starting...
2023-06-03 22:32:31,150 INFO Nacos started successfully in cluster mode. use external storage
[root@node2 ~]#/usr/local/nacos/bin/startup.sh
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-
amd64/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/lib/ext  -server -Xms2g -Xmx2g -Xmn1g -
XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=320m -XX:-OmitStackTraceInFastThrow -XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/usr/local/nacos/logs/java_heapdump.hprof -XX:-UseLargePages -Dnacos.member.list= -
Xloggc:/usr/local/nacos/logs/nacos_gc.log -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -
XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-header-size=524288
nacos is starting with cluster
nacos is starting，you can check the /usr/local/nacos/logs/start.out
[root@node2 ~]#tail -f /usr/local/nacos/logs/start.out
2023-06-03 21:57:55,128 INFO Nacos is starting...
2023-06-03 21:58:01,105 INFO Nacos started successfully in cluster mode. use external storage
[root@node3 ~]#/usr/local/nacos/bin/startup.sh
/usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.ext.dirs=/usr/lib/jvm/java-8-openjdk-
amd64/jre/lib/ext:/usr/lib/jvm/java-8-openjdk-amd64/lib/ext  -server -Xms2g -Xmx2g -Xmn1g -
XX:MetaspaceSize=128m -XX:MaxMetaspaceSize=320m -XX:-OmitStackTraceInFastThrow -XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/usr/local/nacos/logs/java_heapdump.hprof -XX:-UseLargePages -Dnacos.member.list= -
Xloggc:/usr/local/nacos/logs/nacos_gc.log -verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -
XX:+PrintGCTimeStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M -
Dloader.path=/usr/local/nacos/plugins,/usr/local/nacos/plugins/health,/usr/local/nacos/plugins/cmdb,/usr/local
/nacos/plugins/selector -Dnacos.home=/usr/local/nacos -jar /usr/local/nacos/target/nacos-server.jar  --
spring.config.additional-location=file:/usr/local/nacos/conf/ --logging.config=/usr/local/nacos/conf/nacos-
logback.xml --server.max-http-header-size=524288
nacos is starting with cluster
nacos is starting，you can check the /usr/local/nacos/logs/start.out
[root@node3 ~]#tail -f /usr/local/nacos/logs/start.out
2023-06-03 21:57:58,660 INFO Nacos is starting...
2023-06-03 21:58:03,513 INFO Nacos started successfully in cluster mode. use external storage
```

关闭服务

Linux/Unix/Mac

```bash
[root@node1 ~]#/usr/local/nacos/bin/shutdown.sh
```

4.2.3.3.7 服务注册&发现和配置管理

服务注册

```text
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?
serviceName=nacos.bowen.serviceName&ip=1.2.3.4&port=8080'
```

注意：如果开启默认鉴权插件，需要在Header中带上用户名密码。

服务发现

```text
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.bowen.serviceName'
```

注意：如果开启默认鉴权插件，需要在Header中带上用户名密码。

发布配置

```text
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test&content=helloWorld"
```

注意：如果开启默认鉴权插件，需要在Header中带上用户名密码。

获取配置

```text
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

注意：如果开启默认鉴权插件，需要在Header中带上用户名密码。

4.2.3.3.8 配置 haproxy 和 keepalived 实现负载均衡和高可用

4.2.3.3.8.1 配置 haproxy 实现负载均衡

```bash
#修改内核参数
[root@ubuntu2204 ~]#echo net.ipv4.ip_nonlocal_bind = 1 >> /etc/sysctl.conf
[root@ubuntu2204 ~]#sysctl -p
#在两台服务器上安装配置haproxy实现负载均衡反向代理和高可用
[root@ubuntu2204 ~]#apt update && apt -y install haproxy
[root@ubuntu2204 ~]#vim /etc/haproxy/haproxy.cfg
#添加下面行
listen stats
mode http
bind 0.0.0.0:9999
stats enable
log global
stats uri     /haproxy-status
stats auth    admin:123456
listen nacos-8848
#mode tcp
bind 10.0.0.100:8848
server nacos01 10.0.0.201:8848 check
server nacos02 10.0.0.202:8848 check
server nacos03 10.0.0.203:8848 check
listen nacos-9848
mode tcp
bind 10.0.0.100:9848
server nacos01 10.0.0.201:9848 check
server nacos02 10.0.0.202:9848 check
server nacos03 10.0.0.203:9848 check
[root@ubuntu2204 ~]#systemctl reload haproxy
```

4.2.3.3.8.2 配置keepalived实现高可用

```bash
#在两台服务器上安装配置keepalived实现高可用
[root@ubuntu2204 ~]#apt update && apt -y install keepalived
#/usr/share/doc/keepalived/samples/keepalived.conf.sample
#/usr/share/doc/keepalived/samples/keepalived.conf.vrrp.localcheck
#参考上面文件修改配置文件
[root@ubuntu2204 ~]#vim /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
router_id ka1           #另一台主机上为ka2
}
vrrp_script chk_haproxy {
script "killall -0 haproxy"     # cheaper than pidof
interval 1
weight -30
}
vrrp_instance VI_1 {
interface eth0
virtual_router_id 66
state MASTER              #另一台主机上为BACKUP
priority 100              #另一台主机上为80
advert_int 1
authentication {
auth_type PASS
auth_pass 123456
}
virtual_ipaddress {
10.0.0.100/24 dev eth0 label eth0:1
}
track_script {
chk_haproxy
}
}
[root@ubuntu2204 ~]#systemctl restart keepalived
#浏览器访问haproxy的管理页,用户名/密码:admin/123456
http://10.0.0.100:9999/haproxy-status
```

![微服务技术第 104 页插图](assets/img-48e855d770affb1c.png)

4.2.3.3.9 访问集群创建配置

```bash
#创建配置，10.0.0.100的LB的VIP地址
[root@ubuntu2204 ~]#curl -X POST "http://10.0.0.100:8848/nacos/v1/cs/configs?
dataId=nacos.cfg.dataId&group=test&content=HelloWorld"
```

4.2.3.3.10 Web 页面访问

<http://nacos.bowen.org/nacos>

![微服务技术第 105 页插图](assets/img-9139a35d188407be.png)

![微服务技术第 105 页插图](assets/img-3cf8e61b0f67ffc8.png)

### Nacos 基于 Docker 部署

<https://nacos.io/zh-cn/docs/quick-start-docker.html>

### Docker 部署启动

```text
#当前最新精简版
docker run --name nacos -e MODE=standalone --network host -d --restart always registry.cn-
beijing.aliyuncs.com/bowenxiaochun/nacos-server:v2.4.3-slim
docker run --name nacos -e MODE=standalone --network host -d --restart always registry.cn-
beijing.aliyuncs.com/bowenxiaochun/nacos-server:v2.2.3-slim
docker run --name nacos -e MODE=standalone --network host -d --restart always nacos/nacos-server:v2.2.3-slim
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d --restart always nacos/nacos-
server:v2.2.3-slim
#当前最新版
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d --restart always nacos/nacos-
server:v2.2.3
#旧版
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d nacos/nacos-server:v2.2.0
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d nacos/nacos-server:v2.2.0-slim
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d nacos/nacos-server:2.0.3
docker run --name nacos -e MODE=standalone -p 8848:8848 -p 9848:9848 -d nacos/nacos-server:2.0.3-slim
```

### docker compose 部署启动

<https://github.com/nacos-group/nacos-docker>

注意：内存需要4G

Clone 项目

```text
git clone https://github.com/nacos-group/nacos-docker.git
cd nacos-docker
```

单机模式 Derby 德比

```yaml
#example/standalone-derby.yaml 内容
version: "2"
services:
nacos:
image: nacos/nacos-server:${NACOS_VERSION}
container_name: nacos-standalone
environment:
- PREFER_HOST_MODE=hostname
- MODE=standalone
- NACOS_AUTH_IDENTITY_KEY=serverIdentity
- NACOS_AUTH_IDENTITY_VALUE=security
- NACOS_AUTH_TOKEN=SecretKey012345678901234567890123456789012345678901234567890123456789
volumes:
- ./standalone-logs/:/home/nacos/logs
ports:
- "8848:8848"
- "9848:9848"
prometheus:
container_name: prometheus
image: prom/prometheus:latest
volumes:
- ./prometheus/prometheus-standalone.yaml:/etc/prometheus/prometheus.yml
ports:
- "9090:9090"
depends_on:
- nacos
restart: on-failure
grafana:
container_name: grafana
image: grafana/grafana:latest
ports:
- 3000:3000
restart: on-failure
docker-compose -f example/standalone-derby.yaml up
```

单机模式 MySQL 如果希望使用MySQL5.7

```yaml
#example/standalone-mysql-5.7.yaml
version: "3.8"
services:
nacos:
image: nacos/nacos-server:${NACOS_VERSION}
container_name: nacos-standalone-mysql
env_file:
- ../env/custom-application-config.env
volumes:
- ./standalone-logs/:/home/nacos/logs
- ./init.d/application.properties:/home/nacos/conf/application.properties
ports:
- "8848:8848"
- "9848:9848"
depends_on:
mysql:
condition: service_healthy
restart: on-failure
mysql:
container_name: mysql
build:
context: .
dockerfile: ./image/mysql/5.7/Dockerfile
image: example/mysql:5.7
env_file:
- ../env/mysql.env
volumes:
- ./mysql:/var/lib/mysql
ports:
- "3306:3306"
healthcheck:
test: [ "CMD", "mysqladmin" ,"ping", "-h", "localhost" ]
interval: 5s
timeout: 10s
retries: 10
#../env/mysql.env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=nacos_devtest
MYSQL_USER=nacos
MYSQL_PASSWORD=nacos
LANG=C.UTF-8
docker-compose -f example/standalone-mysql-5.7.yaml up
```

如果希望使用MySQL8

```yaml
#example/standalone-mysql-8.yaml
version: "3.8"
services:
nacos:
image: nacos/nacos-server:${NACOS_VERSION}
container_name: nacos-standalone-mysql
env_file:
- ../env/nacos-standlone-mysql.env
volumes:
- ./standalone-logs/:/home/nacos/logs
ports:
- "8848:8848"
- "9848:9848"
depends_on:
mysql:
condition: service_healthy
restart: always
mysql:
container_name: mysql
build:
context: .
dockerfile: ./image/mysql/8/Dockerfile
image: example/mysql:8.0.30
env_file:
- ../env/mysql.env
volumes:
- ./mysql:/var/lib/mysql
ports:
- "3306:3306"
healthcheck:
test: [ "CMD", "mysqladmin" ,"ping", "-h", "localhost" ]
interval: 5s
timeout: 10s
retries: 10
#../env/nacos-standlone-mysql.env
PREFER_HOST_MODE=hostname
MODE=standalone
SPRING_DATASOURCE_PLATFORM=mysql
MYSQL_SERVICE_HOST=mysql
MYSQL_SERVICE_DB_NAME=nacos_devtest
MYSQL_SERVICE_PORT=3306
MYSQL_SERVICE_USER=nacos
MYSQL_SERVICE_PASSWORD=nacos
MYSQL_SERVICE_DB_PARAM=characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&us
eSSL=false&allowPublicKeyRetrieval=true
NACOS_AUTH_IDENTITY_KEY=2222
NACOS_AUTH_IDENTITY_VALUE=2xxx
NACOS_AUTH_TOKEN=SecretKey012345678901234567890123456789012345678901234567890123456789
docker-compose -f example/standalone-mysql-8.yaml up
```

集群模式

```yaml
#example/cluster-hostname.yaml 内容
version: "3.8"
services:
nacos1:
hostname: nacos1
container_name: nacos1
image: nacos/nacos-server:${NACOS_VERSION}
volumes:
- ./cluster-logs/nacos1:/home/nacos/logs
ports:
- "7848:7848"
- "8848:8848"
- "9868:9848"
- "9850:9849"
env_file:
- ../env/nacos-hostname.env
restart: always
depends_on:
mysql:
condition: service_healthy
nacos2:
hostname: nacos2
image: nacos/nacos-server:${NACOS_VERSION}
container_name: nacos2
volumes:
- ./cluster-logs/nacos2:/home/nacos/logs
ports:
- "7849:7848"
- "8849:8848"
- "9869:9848"
- "9851:9849"
env_file:
- ../env/nacos-hostname.env
restart: always
depends_on:
mysql:
condition: service_healthy
nacos3:
hostname: nacos3
image: nacos/nacos-server:${NACOS_VERSION}
container_name: nacos3
volumes:
- ./cluster-logs/nacos3:/home/nacos/logs
ports:
- "7850:7848"
- "8850:8848"
- "9870:9848"
- "9852:9849"
env_file:
- ../env/nacos-hostname.env
restart: always
depends_on:
mysql:
condition: service_healthy
mysql:
container_name: mysql
build:
context: .
dockerfile: ./image/mysql/5.7/Dockerfile
image: example/mysql:5.7
env_file:
- ../env/mysql.env
volumes:
- ./mysql:/var/lib/mysql
ports:
- "3306:3306"
healthcheck:
test: [ "CMD", "mysqladmin" ,"-uroot","-proot","ping", "-h", "localhost" ]  #修改此行，指定用户名和密码
都是root
interval: 5s
timeout: 10s
retries: 10
#../env/nacos-hostname.env 内容
PREFER_HOST_MODE=hostname
NACOS_SERVERS=nacos1:8848 nacos2:8849 nacos3:8850
SPRING_DATASOURCE_PLATFORM=mysql
MYSQL_SERVICE_HOST=mysql
MYSQL_SERVICE_DB_NAME=nacos_devtest
MYSQL_SERVICE_PORT=3306
MYSQL_SERVICE_USER=nacos
MYSQL_SERVICE_PASSWORD=nacos
MYSQL_SERVICE_DB_PARAM=characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&us
eSSL=false&allowPublicKeyRetrieval=true
NACOS_AUTH_IDENTITY_KEY=2222
NACOS_AUTH_IDENTITY_VALUE=2xxx
NACOS_AUTH_TOKEN=SecretKey012345678901234567890123456789012345678901234567890123456789
docker-compose -f example/cluster-hostname.yaml up
nacos3    | 2023-09-18 10:30:43,276 INFO Nacos started successfully in cluster mode. use external storage
nacos3    |
nacos2    | 2023-09-18 10:30:43,658 INFO Nacos started successfully in cluster mode. use external storage
[root@ubuntu2204 nacos-docker-master]#docker-compose -f example/cluster-hostname.yaml ps
Name               Command                  State
Ports
----------------------------------------------------------------------------------------------------------
------------------------------------------------------------------
mysql    docker-entrypoint.sh mysql ...   Up (healthy)   0.0.0.0:3306->3306/tcp,:::3306->3306/tcp,
33060/tcp
nacos1   bin/docker-startup.sh            Up             0.0.0.0:7848->7848/tcp,:::7848->7848/tcp,
0.0.0.0:8848->8848/tcp,:::8848->8848/tcp,
0.0.0.0:9868->9848/tcp,:::9868->9848/tcp,
0.0.0.0:9850->9849/tcp,:::9850->9849/tcp
nacos2   bin/docker-startup.sh            Up             0.0.0.0:7849->7848/tcp,:::7849->7848/tcp,
0.0.0.0:8849->8848/tcp,:::8849->8848/tcp,
0.0.0.0:9869->9848/tcp,:::9869->9848/tcp,
0.0.0.0:9851->9849/tcp,:::9851->9849/tcp
nacos3   bin/docker-startup.sh            Up             0.0.0.0:7850->7848/tcp,:::7850->7848/tcp,
0.0.0.0:8850->8848/tcp,:::8850->8848/tcp,
0.0.0.0:9870->9848/tcp,:::9870->9848/tcp,
0.0.0.0:9852->9849/tcp,:::9852->9849/tcp
```

### 服务访问

服务注册

```text
curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?
serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'
```

服务发现

```text
curl -X GET 'http://127.0.0.1:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'
```

发布配置

```text
curl -X POST "http://127.0.0.1:8848/nacos/v1/cs/configs?
dataId=nacos.cfg.dataId&group=test&content=helloWorld"
```

获取配置

```text
curl -X GET "http://127.0.0.1:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

Nacos 控制台 link：http://127.0.0.1:8848/nacos/

Common property configuration 属性名称描述选项 MODE 系统启动方式: 集群/单机 cluster/standalone默认 cluster NACOS_SERVERS 集群地址 p1:port1空格ip2:port2 空格ip3:port3 PREFER_HOST_MODE 支持IP还是域名模式 hostname/ip 默认 ip NACOS_SERVER_PORT Nacos 运行端口默认 8848 NACOS_SERVER_IP 多网卡模式下可以指定IP SPRING_DATASOURCE_PLATFORM 单机模式下支持MYSQL数据库 mysql / 空 默认:空 MYSQL_SERVICE_HOST 数据库 连接地址 MYSQL_SERVICE_PORT 数据库端口默认 : 3306 MYSQL_SERVICE_DB_NAME 数据库库名 MYSQL_SERVICE_USER 数据库用户名 MYSQL_SERVICE_PASSWORD 数据库用户密码 MYSQL_SERVICE_DB_PARAM 数据库连接参数 default : characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false MYSQL_DATABASE_NUM 数据库编号默认 :1 JVM_XMS -Xms 默认 :1g JVM_XMX -Xmx 默认 :1g JVM_XMN -Xmn 默认 :512m JVM_MS -XX:MetaspaceSize 默认 :128m JVM_MMS -XX:MaxMetaspaceSize 默认 :320m NACOS_DEBUG 是否开启远程DEBUG y/n 默认 :n TOMCAT_ACCESSLOG_ENABLED server.tomcat.accesslog.enabled 默认 :false NACOS_AUTH_SYSTEM_TYPE 权限系统类型选择,目前只支持nacos类型默认 :nacos NACOS_AUTH_ENABLE 是否开启权限系统默认 :false NACOS_AUTH_TOKEN_EXPIRE_SECONDS token 失效时间默认 :18000 NACOS_AUTH_TOKEN token 默认 :SecretKey012345678901234567890123456789012345678901234567890123456789 NACOS_AUTH_CACHE_ENABLE 权限缓存开关 ,开启后权限缓存的更新默认有15

默认 : false

秒的延迟

MEMBER_LIST 通过环境变量的方式设置集群地址例子:192.168.16.101:8847?raft_port=8807,192.168.16.101?raft_port=8808,192.168.16.101:8849?raft_port=8809 EMBEDDED_STORAGE 是否开启集群嵌入式存储模式 embedded 默认 : none NACOS_AUTH_CACHE_ENABLE nacos.core.auth.caching.enabled default : false NACOS_AUTH_USER_AGENT_AUTH_WHITE_ENABLE nacos.core.auth.enable.userAgentAuthWhite default : false NACOS_AUTH_IDENTITY_KEY nacos.core.auth.server.identity.key default : serverIdentity NACOS_AUTH_IDENTITY_VALUE nacos.core.auth.server.identity.value default : security NACOS_SECURITY_IGNORE_URLS nacos.security.ignore.urls default : /,/error,/**/*.css,/**/*.js,/**/*.html,/**/*.map,/**/*.svg,/**/*.png,/**/*.ico,/console-

```text
fe/public/**,/v1/auth/**,/v1/console/health/**,/actuator/**,/v1/console/server/**
```

### Nacos 基于 Kubernetes 的YAML方式部署

<https://nacos.io/zh-cn/docs/use-nacos-with-kubernetes.html>

本项目包含一个可构建的Nacos Docker Image，旨在利用StatefulSets在Kubernetes上部署Nacos

推荐使用Nacos Operator在Kubernetes部署Nacos Server

例子部署环境

机器配置

内网IP 主机名配置

10.0.0.200 k8s-master Ubuntu22.04 Single-core processor Mem 4G disk 40G

10.0.0.201 node01 Ubuntu22.04 Single-core processor Mem 4G disk 40G

10.0.0.202 node02 Ubuntu22.04 Single-core processor Mem 4G disk 40G

Kubernetes NFS 版本：在k8s-master进行安装Server端，并且指定共享目录，本项目指定的/data/nfs-share Git

### 基本功能实现

Clone 项目

```text
git clone https://github.com/nacos-group/nacos-k8s.git
```

简单例子

如果你使用简单方式快速启动,请注意这是没有使用持久化卷的,可能存在数据丢失风险

```yaml
cd nacos-k8s
chmod +x quick-startup.sh
./quick-startup.sh
cat ./quick-startup.sh
#!/usr/bin/env bash
echo "mysql mysql startup"
kubectl create -f ./deploy/mysql/mysql-local.yaml
echo "nacos quick startup"
kubectl create -f ./deploy/nacos/nacos-start.yaml
#单机MySQL
cat ./deploy/mysql/mysql-local.yaml
apiVersion: v1
kind: ReplicationController
metadata:
name: mysql
labels:
name: mysql
spec:
replicas: 1
selector:
name: mysql
template:
metadata:
labels:
name: mysql
spec:
containers:
- name: mysql
image: nacos/nacos-mysql:5.7
ports:
- containerPort: 3306
volumeMounts:
- name: mysql-data
mountPath: /var/lib/mysql
env:
- name: MYSQL_ROOT_PASSWORD
value: "root"
- name: MYSQL_DATABASE
value: "nacos_devtest"
- name: MYSQL_USER
value: "nacos"
- name: MYSQL_PASSWORD
value: "nacos"
volumes:
- name: mysql-data
hostPath:
path: /var/lib/mysql
---
apiVersion: v1
kind: Service
metadata:
name: mysql
labels:
name: mysql
spec:
ports:
- port: 3306
targetPort: 3306
selector:
name: mysql
#cat ./deploy/nacos/nacos-start.yaml
---
apiVersion: v1
kind: Service
metadata:
name: nacos-headless
labels:
app: nacos-headless
spec:
type: ClusterIP
clusterIP: None
ports:
- port: 8848
name: server
targetPort: 8848
- port: 9848
name: client-rpc
targetPort: 9848
- port: 9849
name: raft-rpc
targetPort: 9849
## 兼容1.4.x版本的选举端口
- port: 7848
name: old-raft-rpc
targetPort: 7848
selector:
app: nacos
---
apiVersion: v1
kind: ConfigMap
metadata:
name: nacos-cm
data:
mysql.host: "mysql"
mysql.db.name: "nacos_devtest"
mysql.port: "3306"
mysql.user: "nacos"
mysql.password: "nacos"
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
name: nacos
spec:
serviceName: nacos-headless
replicas: 3
template:
metadata:
labels:
app: nacos
annotations:
pod.alpha.kubernetes.io/initialized: "true"
spec:
affinity:
podAntiAffinity:
requiredDuringSchedulingIgnoredDuringExecution:
- labelSelector:
matchExpressions:
- key: "app"
operator: In
values:
- nacos
topologyKey: "kubernetes.io/hostname"
containers:
- name: nacos
imagePullPolicy: Always
image: nacos/nacos-server:latest
resources:
requests:
memory: "2Gi"
cpu: "500m"
ports:
- containerPort: 8848
name: client
- containerPort: 9848
name: client-rpc
- containerPort: 9849
name: raft-rpc
- containerPort: 7848
name: old-raft-rpc
env:
- name: NACOS_REPLICAS
value: "3"
- name: MYSQL_SERVICE_HOST
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.host
- name: MYSQL_SERVICE_DB_NAME
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.db.name
- name: MYSQL_SERVICE_PORT
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.port
- name: MYSQL_SERVICE_USER
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.user
- name: MYSQL_SERVICE_PASSWORD
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.password
- name: SPRING_DATASOURCE_PLATFORM
value: "mysql"
- name: NACOS_SERVER_PORT
value: "8848"
- name: NACOS_APPLICATION_PORT
value: "8848"
- name: PREFER_HOST_MODE
value: "hostname"
- name: NACOS_SERVERS
value: "nacos-0.nacos-headless.default.svc.cluster.local:8848 nacos-1.nacos-
headless.default.svc.cluster.local:8848 nacos-2.nacos-headless.default.svc.cluster.local:8848"
selector:
matchLabels:
app: nacos
```

测试

服务注册

```text
curl -X POST 'http://cluster-ip:8848/nacos/v1/ns/instance?
serviceName=nacos.naming.serviceName&ip=20.18.7.10&port=8080'
```

服务发现

```text
curl -X GET 'http://cluster-ip:8848/nacos/v1/ns/instance/list?serviceName=nacos.naming.serviceName'
```

发布配置

```text
curl -X POST "http://cluster-ip:8848/nacos/v1/cs/configs?
dataId=nacos.cfg.dataId&group=test&content=helloWorld"
```

获取配置

```text
curl -X GET "http://cluster-ip:8848/nacos/v1/cs/configs?dataId=nacos.cfg.dataId&group=test"
```

### 高级功能实现

在高级使用中,Nacos在K8S拥有自动扩容缩容和数据持久特性

请注意如果需要使用这部分功能请使用PVC持久卷,Nacos的自动扩容缩容需要依赖持久卷,以及数据持久化也是一样

本例中使用的是NFS来使用PVC.

4.2.5.2.1 部署 NFS

创建角色

```yaml
~#kubectl create -f deploy/nfs/rbac.yaml
~#cat deploy/nfs/rbac.yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: nfs-client-provisioner-runner
rules:
- apiGroups: [""]
resources: ["persistentvolumes"]
verbs: ["get", "list", "watch", "create", "delete"]
- apiGroups: [""]
resources: ["persistentvolumeclaims"]
verbs: ["get", "list", "watch", "update"]
- apiGroups: [""]
resources: ["endpoints"]
verbs: ["get", "list", "watch", "create", "update", "patch"]
- apiGroups: ["storage.k8s.io"]
resources: ["storageclasses"]
verbs: ["get", "list", "watch"]
- apiGroups: [""]
resources: ["events"]
verbs: ["create", "update", "patch"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: run-nfs-client-provisioner
subjects:
- kind: ServiceAccount
name: nfs-client-provisioner
namespace: default
roleRef:
kind: ClusterRole
name: nfs-client-provisioner-runner
apiGroup: rbac.authorization.k8s.io
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: leader-locking-nfs-client-provisioner
rules:
- apiGroups: [""]
resources: ["endpoints"]
verbs: ["get", "list", "watch", "create", "update", "patch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: leader-locking-nfs-client-provisioner
subjects:
- kind: ServiceAccount
name: nfs-client-provisioner
# replace with namespace where provisioner is deployed
namespace: default
roleRef:
kind: Role
name: leader-locking-nfs-client-provisioner
apiGroup: rbac.authorization.k8s.io
```

如果的K8S命名空间不是default，请在部署RBAC之前执行以下脚本:

```text
# Set the subject of the RBAC objects to the current namespace where the provisioner is being deployed
$ NS=$(kubectl config get-contexts|grep -e "^\*" |awk '{print $5}')
$ NAMESPACE=${NS:-default}
$ sed -i'' "s/namespace:.*/namespace: $NAMESPACE/g" ./deploy/nfs/rbac.yaml
```

创建 ServiceAccount 和部署 NFS-Client Provisioner

```yaml
~#kubectl create -f deploy/nfs/deployment.yaml
~#cat deploy/nfs/deployment.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: nfs-client-provisioner
---
kind: Deployment
apiVersion: apps/v1
metadata:
name: nfs-client-provisioner
spec:
replicas: 1
strategy:
type: Recreate
selector:
matchLabels:
app: nfs-client-provisioner
template:
metadata:
labels:
app: nfs-client-provisioner
spec:
serviceAccount: nfs-client-provisioner
containers:
- name: nfs-client-provisioner
image: quay.io/external_storage/nfs-client-provisioner:latest
volumeMounts:
- name: nfs-client-root
mountPath: /persistentvolumes
env:
- name: PROVISIONER_NAME
value: fuseim.pri/ifs
- name: NFS_SERVER
value: 172.17.79.3
- name: NFS_PATH
value: /data/nfs-share
volumes:
- name: nfs-client-root
nfs:
server: 172.17.79.3
path: /data/nfs-share
```

创建 NFS StorageClass

```yaml
~#kubectl create -f deploy/nfs/class.yaml
~#cat deploy/nfs/class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
name: managed-nfs-storage
provisioner: fuseim.pri/ifs
parameters:
archiveOnDelete: "false"
```

验证NFS部署成功

```text
~#kubectl get pod -l app=nfs-client-provisioner
```

4.2.5.2.2 部署数据库

```yaml
~#cd nacos-k8s
~#kubectl create -f deploy/mysql/mysql-nfs.yaml
~#cat deploy/mysql/mysql-nfs.yaml
apiVersion: v1
kind: ReplicationController
metadata:
name: mysql
labels:
name: mysql
spec:
replicas: 1
selector:
name: mysql
template:
metadata:
labels:
name: mysql
spec:
containers:
- name: mysql
image: nacos/nacos-mysql:5.7
ports:
- containerPort: 3306
volumeMounts:
- name: mysql-data
mountPath: /var/lib/mysql
env:
- name: MYSQL_ROOT_PASSWORD
value: "root"
- name: MYSQL_DATABASE
value: "nacos_devtest"
- name: MYSQL_USER
value: "nacos"
- name: MYSQL_PASSWORD
value: "nacos"
volumes:
- name: mysql-data
nfs:
server: 172.17.79.3
path: /data/mysql
---
apiVersion: v1
kind: Service
metadata:
name: mysql
labels:
name: mysql
spec:
ports:
- port: 3306
targetPort: 3306
selector:
name: mysql
```

验证数据库是否正常工作

```text
kubectl get pod
NAME                         READY   STATUS    RESTARTS   AGE
mysql-gf2vd                        1/1     Running   0          111m
```

执行数据库初始化语句

数据库初始化语句位置 https://github.com/alibaba/nacos/blob/develop/distribution/conf/nacos-mysql.sql

4.2.5.2.3 部署Nacos

修改 deploy/nacos/nacos-pvc-nfs.yaml

```text
data:
mysql.host: "数据库地址"
mysql.db.name: "数据库名称"
mysql.port: "端口"
mysql.user: "用户名"
mysql.password: "密码"
```

创建 Nacos

```yaml
~#kubectl create -f nacos-k8s/deploy/nacos/nacos-pvc-nfs.yaml
~#cat ./deploy/nacos/nacos-pvc-nfs.yaml
# 请阅读Wiki文章
# https://github.com/nacos-group/nacos-
k8s/wiki/%E4%BD%BF%E7%94%A8peerfinder%E6%89%A9%E5%AE%B9%E6%8F%92%E4%BB%B6
---
apiVersion: v1
kind: Service
metadata:
name: nacos-headless
labels:
app: nacos
spec:
publishNotReadyAddresses: true
ports:
- port: 8848
name: server
targetPort: 8848
- port: 9848
name: client-rpc
targetPort: 9848
- port: 9849
name: raft-rpc
targetPort: 9849
## 兼容1.4.x版本的选举端口
- port: 7848
name: old-raft-rpc
targetPort: 7848
clusterIP: None
selector:
app: nacos
---
apiVersion: v1
kind: ConfigMap
metadata:
name: nacos-cm
data:
mysql.host: "mysql"
mysql.db.name: "nacos_devtest"
mysql.port: "3306"
mysql.user: "nacos"
mysql.password: "nacos"
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
name: nacos
spec:
podManagementPolicy: Parallel
serviceName: nacos-headless
replicas: 3
template:
metadata:
labels:
app: nacos
annotations:
pod.alpha.kubernetes.io/initialized: "true"
spec:
affinity:
podAntiAffinity:
requiredDuringSchedulingIgnoredDuringExecution:
- labelSelector:
matchExpressions:
- key: "app"
operator: In
values:
- nacos
topologyKey: "kubernetes.io/hostname"
serviceAccountName: nfs-client-provisioner
initContainers:
- name: peer-finder-plugin-install
image: nacos/nacos-peer-finder-plugin:1.1
imagePullPolicy: Always
volumeMounts:
- mountPath: /home/nacos/plugins/peer-finder
name: data
subPath: peer-finder
containers:
- name: nacos
imagePullPolicy: Always
image: nacos/nacos-server:latest
resources:
requests:
memory: "2Gi"
cpu: "500m"
ports:
- containerPort: 8848
name: client-port
- containerPort: 9848
name: client-rpc
- containerPort: 9849
name: raft-rpc
- containerPort: 7848
name: old-raft-rpc
env:
- name: NACOS_REPLICAS
value: "3"
- name: SERVICE_NAME
value: "nacos-headless"
- name: DOMAIN_NAME
value: "cluster.local"
- name: POD_NAMESPACE
valueFrom:
fieldRef:
apiVersion: v1
fieldPath: metadata.namespace
- name: MYSQL_SERVICE_HOST
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.host
- name: MYSQL_SERVICE_DB_NAME
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.db.name
- name: MYSQL_SERVICE_PORT
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.port
- name: MYSQL_SERVICE_USER
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.user
- name: MYSQL_SERVICE_PASSWORD
valueFrom:
configMapKeyRef:
name: nacos-cm
key: mysql.password
- name: SPRING_DATASOURCE_PLATFORM
value: "mysql"
- name: NACOS_SERVER_PORT
value: "8848"
- name: NACOS_APPLICATION_PORT
value: "8848"
- name: PREFER_HOST_MODE
value: "hostname"
volumeMounts:
- name: data
mountPath: /home/nacos/plugins/peer-finder
subPath: peer-finder
- name: data
mountPath: /home/nacos/data
subPath: data
- name: data
mountPath: /home/nacos/logs
subPath: logs
volumeClaimTemplates:
- metadata:
name: data
annotations:
volume.beta.kubernetes.io/storage-class: "managed-nfs-storage"
spec:
accessModes: [ "ReadWriteMany" ]
resources:
requests:
storage: 20Gi
selector:
matchLabels:
app: nacos
```

验证Nacos节点启动成功

```text
kubectl get pod -l app=nacos
NAME      READY   STATUS    RESTARTS   AGE
nacos-0   1/1     Running   0          19h
nacos-1   1/1     Running   0          19h
nacos-2   1/1     Running   0          19h
```

4.2.5.2.4 扩容测试

在扩容前，使用 kubectl exec 获取在pod中的Nacos集群配置文件信息

```text
for i in 0 1; do echo nacos-$i; kubectl exec nacos-$i cat conf/cluster.conf; done
```

StatefulSet控制器根据其序数索引为每个Pod提供唯一的主机名。 主机名采用 - 的形式。 因为nacos StatefulSet的副本字段设置为2，所以当前集群文件中只有两个Nacos节点地址

![微服务技术第 118 页插图](assets/img-d56b8b3d8d98e22b.png)

使用kubectl scale 对Nacos动态扩容

```text
kubectl scale sts nacos --replicas=3
```

![微服务技术第 118 页插图](assets/img-8f071eb35cd6b605.png)

在扩容后，使用 kubectl exec 获取在pod中的Nacos集群配置文件信息

```text
for i in 0 1 2; do echo nacos-$i; kubectl exec nacos-$i cat conf/cluster.conf; done
```

![微服务技术第 118 页插图](assets/img-2398d65f39ea332e.png)

使用 kubectl exec 执行Nacos API 在每台节点上获取当前Leader是否一致

```text
for i in 0 1 2; do echo nacos-$i; kubectl exec nacos-$i curl -X GET
"http://localhost:8848/nacos/v1/ns/raft/state"; done
```

到这里你可以发现新节点已经正常加入Nacos集群当中

4.2.5.2.5 持久化

必须要使用持久卷，否则会出现数据丢失的情况

项目目录

目录描述

plugin 帮助Nacos集群进行动态扩容的插件Docker镜像源码

deploy K8s 部署文件

配置属性

nacos-pvc-nfs.yaml or nacos-start.yaml

名称必

要描述

mysql.host Y 自建数据库地址,使用外部数据库时必须指定

mysql.db.name Y 数据库名称

mysql.port N 数据库端口

mysql.user Y 数据库用户名(请不要含有符号, )

mysql.password Y 数据库密码(请不要含有符号, )

SPRING_DATASOURCE_PLATFORM Y 数据库类型,默认为embedded嵌入式数据库,参数只支持mysql或embedded

NACOS_REPLICAS N 确定执行Nacos启动节点数量,如果不适用动态扩容插件,就必须配置这个属性，否则使用

扩容插件后不会生效

NACOS_SERVER_PORT N Nacos 端口 为peer_finder插件提供端口

NACOS_APPLICATION_PORT N Nacos 端口

PREFER_HOST_MODE Y 启动Nacos集群按域名解析

nfs deployment.yaml

名称必要描述

NFS_SERVER Y NFS 服务端地址

NFS_PATH Y NFS 共享目录

server Y NFS 服务端地址

path Y NFS 共享目录

mysql

名称必要描述

MYSQL_ROOT_PASSWORD N ROOT 密码

MYSQL_DATABASE Y 数据库名称

MYSQL_USER Y 数据库用户名

MYSQL_PASSWORD Y 数据库密码

MYSQL_REPLICATION_USER Y 数据库复制用户

MYSQL_REPLICATION_PASSWORD Y 数据库复制用户密码

Nfs:server N NFS 服务端地址，如果使用本地部署不需要配置

Nfs:path N NFS 共享目录，如果使用本地部署不需要配置

### Nacos 基于 Kubernetes 的nacos-operator方式部署

<https://github.com/nacos-group/nacos-k8s/blob/master/operator/README-CN.md>

nacos-operator项目，快速在K8s上面部署构建nacos。

### 与nacos-k8s的项目区别

优点

通过operator快速构建nacos集群，指定简单的cr.yaml文件，既可以实现各种类型的nacos集群(数据库选型、standalone/cluster模式等) 增加一定的运维能力，在status中增加对nacos集群状态的检查、自动化运维等(后续扩展更多功能)

### 快速开始

```text
# 直接使用helm方式安装operator
helm install nacos-operator ./chart/nacos-operator
# 如果没有helm, 使用kubectl进行安装, 默认安装在default下面
kubectl apply -f chart/nacos-operator/nacos-operator-all.yaml
```

### 启动单实例，standalone模式

查看crd文件

```yaml
cat config/samples/nacos.yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
type: standalone
image: nacos/nacos-server:1.4.1
replicas: 1
# 安装demo standalone模式
kubectl apply -f config/samples/nacos.yaml
```

查看nacos实例

```yaml
kubectl get nacos
NAME    REPLICAS   READY     TYPE         DBTYPE   VERSION   CREATETIME
nacos   1          Running   standalone            1.4.1     2021-03-14T09:21:49Z
kubectl get pod  -o wide
NAME                 READY   STATUS    RESTARTS   AGE    IP               NODE        NOMINATED NODE
READINESS GATES
nacos-0   1/1     Running   0          84s    10.168.247.38    slave-100   <none>           <none>
kubectl get nacos nacos -o yaml
...
status
conditions:
- instance: 10.168.247.38
nodeName: slave-100
podName: nacos-0
status: "true"
type: leader
phase: Running
version: 1.4.1
```

清除

```text
make demo clear=true
```

### 启动集群模式

```yaml
cat config/samples/nacos_cluster.yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
type: cluster
image: nacos/nacos-server:1.4.1
replicas: 3
# 创建nacos集群
kubectl apply -f config/samples/nacos_cluster.yaml
kubectl get po -o wide
NAME             READY   STATUS    RESTARTS   AGE    IP               NODE         NOMINATED NODE   READINESS
GATES
nacos-0          1/1     Running   0          111s   10.168.247.39    slave-100    <none>           <none>
nacos-1          1/1     Running   0          109s   10.168.152.186   master-212   <none>           <none>
nacos-2          1/1     Running   0          108s   10.168.207.209   slave-214    <none>           <none>
kubectl get nacos
NAME    REPLICAS   READY     TYPE      DBTYPE   VERSION   CREATETIME
nacos   3          Running   cluster            1.4.1     2021-03-14T09:33:09Z
kubectl get nacos nacos -o yaml -w
...
status:
conditions:
- instance: 10.168.247.39
nodeName: slave-100
podName: nacos-0
status: "true"
type: leader
- instance: 10.168.152.186
nodeName: master-212
podName: nacos-1
status: "true"
type: Followers
- instance: 10.168.207.209
nodeName: slave-214
podName: nacos-2
status: "true"
type: Followers
event:
- code: -1
firstAppearTime: "2021-03-05T08:35:03Z"
lastTransitionTime: "2021-03-05T08:35:06Z"
message: The number of ready pods is too small[]
status: false
- code: 200
firstAppearTime: "2021-03-05T08:36:09Z"
lastTransitionTime: "2021-03-05T08:36:48Z"
status: true
phase: Running
version: 1.4.1
```

清除

```text
make demo clear=true
```

### 设置模式

目前支持standalone和cluster模式

通过配置spec.type 为 standalone/cluster

### 数据库配置

embedded数据库

```yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
type: standalone
image: nacos/nacos-server:1.4.1
replicas: 1
database:
type: embedded
# 启动数据卷，不然重启后数据丢失
volume:
enabled: true
requests:
storage: 1Gi
storageClass: default
```

mysql数据库

该模式下需要提供外部mysql连接信息，会自动创建创建nacos数据库，并执行初始化sql

```yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
type: standalone
image: nacos/nacos-server:1.4.1
replicas: 1
database:
type: mysql
mysqlHost: mysql
mysqlDb: nacos
mysqlUser: root
mysqlPort: "3306"
mysqlPassword: "123456"
```

### 自定义配置

1. 通过环境变量配置 兼容nacos-docker项目， https://github.com/nacos-group/nacos-docker

```yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
type: standalone
env:
- key: JVM_XMS
value: 2g
```

2. 通过properties文件配置

https://github.com/nacos-group/nacos-docker/blob/master/build/bin/docker-startup.sh

```text
export CUSTOM_SEARCH_NAMES="application,custom"
export CUSTOM_SEARCH_LOCATIONS=${BASE_DIR}/init.d/,file:${BASE_DIR}/conf/
```

支持自定义配置文件，spec.config 会直接映射成custom.properties文件

```yaml
apiVersion: nacos.io/v1alpha1
kind: Nacos
metadata:
name: nacos
spec:
...
config:|
management.endpoints.web.exposure.include=*
```

### Prometheus 监控

默认没有开启Prometheus监控，

### 配置打开Promethues 监控功能

```bash
#修改配置
[root@ubuntu2204 ~]#vi /usr/local/nacos/conf/application.properties
#***********Expose prometheus and health **************************#
#取消下面行注释开启prometheus监控，指标路径：http://127.0.0.1:8848/nacos/actuator/prometheus
management.endpoints.web.exposure.include=prometheus,health
[root@ubuntu2204 ~]#systemctl restart nacos
#验证访问
[root@ubuntu2404 ~]#curl -s  http://127.0.0.1:8848/nacos/actuator/prometheus |grep -v '^#'|grep nacos
nacos_naming_publisher{version="v1",} 0.0
nacos_naming_publisher{version="v2",} 0.0
nacos_naming_subscriber{version="v1",} 0.0
nacos_naming_subscriber{version="v2",} 0.0
nacos_monitor_seconds_max{module="core",name="raft_apply_log_timer",} 0.0
nacos_monitor_seconds_max{module="core",name="raft_apply_read_timer",} 0.0
nacos_monitor_seconds_count{module="core",name="raft_apply_log_timer",} 0.0
nacos_monitor_seconds_sum{module="core",name="raft_apply_log_timer",} 0.0
nacos_monitor_seconds_count{module="core",name="raft_apply_read_timer",} 0.0
nacos_monitor_seconds_sum{module="core",name="raft_apply_read_timer",} 0.0
application_ready_time_seconds{main_application_class="com.alibaba.nacos.Nacos",} 12.294
application_started_time_seconds{main_application_class="com.alibaba.nacos.Nacos",} 12.265
nacos_monitor{module="naming",name="mysqlHealthCheck",} 0.0
nacos_monitor{module="naming",name="emptyPush",} 0.0
nacos_monitor{module="config",name="configCount",} 1.0
nacos_monitor_count{module="core",name="raft_read_from_leader",} 0.0
nacos_monitor_sum{module="core",name="raft_read_from_leader",} 0.0
```

### 配置 Prometheus 监控 Nacos

```text
https://github.com/nacos-group/nacos-docker/tree/master/example/prometheus
#https://github.com/nacos-group/nacos-docker/blob/master/example/prometheus/prometheus-cluster.yaml
#集群模式
# my global config
global:
scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
# scrape_timeout is set to the global default (10s).
# Alertmanager configuration
alerting:
alertmanagers:
- static_configs:
- targets:
# - alertmanager:9093
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
# - "first_rules.yml"
# - "second_rules.yml"
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
# The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
- job_name: 'prometheus'
# metrics_path defaults to '/metrics'
# scheme defaults to 'http'.
static_configs:
- targets: ['localhost:9090']
- job_name: 'nacos'
metrics_path: '/nacos/actuator/prometheus'
static_configs:
- targets: ["nacos1:8848","nacos2:8848","nacos3:8848"]
#https://github.com/nacos-group/nacos-docker/blob/master/example/prometheus/prometheus-standalone.yaml
#单机模式
# my global config
global:
scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
# scrape_timeout is set to the global default (10s).
# Alertmanager configuration
alerting:
alertmanagers:
- static_configs:
- targets:
# - alertmanager:9093
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
# - "first_rules.yml"
# - "second_rules.yml"
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
# The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
- job_name: 'prometheus'
# metrics_path defaults to '/metrics'
# scheme defaults to 'http'.
static_configs:
- targets: ['localhost:9090']
- job_name: 'nacos'
metrics_path: '/nacos/actuator/prometheus'
static_configs:
- targets: ['nacos:8848']
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/23-nacos-architecture-and-overview.html' | relative_url }}">← Previous: Nacos Architecture and Overview</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/25-nacos-examples.html' | relative_url }}">Next: Nacos Examples →</a>
</nav>
