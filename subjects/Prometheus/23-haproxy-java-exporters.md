---
layout: default
title: "Prometheus · HAProxy 与 Java 监控"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 23 HAProxy 与 Java 监控

## 7.3 Haproxy 监控

Haproxy的监控有两种实现方式

借助于专用的haproxy_exporter组件来采集 haproxy的csv数据
haproxy_exporter 可以和 haproxy 处于不同的环境，不同主机等  
借助于 haproxy本身的机制，暴露metrics指标  
/metrics 和 /haproxy-status 是同时配置的  

相当于 zookeeper 的 /metrics

### 7.3.1 Haproxy_exporter 监控

#### 7.3.1.1 Haproxy_exporter 介绍

对于负载均衡软件来说，prometheus提供了专用的监控组件haproxy-exporter来实现对于haproxy负载均衡软件的代理工作。

haproxy-exporter 本质上，它是根据对haproxy的状态页面uri地址获取到的csv内容进行了解析，从而获取我们需要监控到的数据
下载链接:https://prometheus.io/download/
官网地址：https://github.com/prometheus/haproxy_exporter

![原 PDF 第 298 页插图](assets/img-267af1685a44474a.png)

#### 7.3.1.2 实战案例

7.3.1.2.1 准备 Haproxy 环境
```bash
#安装haproxy软件
apt -y install haproxy
#设定haproxy配置文件
cat /etc/haproxy/haproxy.cfg
global
......
    stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
......
listen stats
    mode http
    bind 0.0.0.0:9999
    stats enable
    log global
    stats uri     /haproxy-status
    stats auth    admin:123456
#重启haproxy服务
systemctl restart haproxy.service
#浏览器访问 10.0.0.106:9999/haproxy-status 页面
```

![原 PDF 第 299 页插图](assets/img-412c08d012892de7.png)

![原 PDF 第 299 页插图](assets/img-06b6a761107b2032.png)
```text
#浏览器访问 10.0.0.106:9999/haproxy-status;csv 页面
```

![原 PDF 第 299 页插图](assets/img-b535f928366445ff.png)

7.3.1.2.2 安装 Haproxy Exporter 组件
https://github.com/prometheus/haproxy_exporter

haproxy_exporter 支持通过两种方式监控: stats状态和socket文件

![原 PDF 第 300 页插图](assets/img-57aedf2dd8b2c8f6.png)
```ini
#获取软件
wget
https://github.com/prometheus/haproxy_exporter/releases/download/v0.13.0/haproxy_exporter-0.13.0.linux-amd64.tar.gz
#解压软件
tar xf haproxy_exporter-0.13.0.linux-amd64.tar.gz -C /usr/local/
ln -s /usr/local/haproxy_exporter-0.13.0.linux-amd64 /usr/local/haproxy_exporter
cd /usr/local/haproxy_exporter/
mkdir bin
mv haproxy_exporter bin/
#修改haproxy_exporter的服务启动文件
vim /lib/systemd/system/haproxy_exporter.service
[Unit]
Description=haproxy exporter project
After=network.target
[Service]
Type=simple
ExecStart=/usr/local/haproxy_exporter/bin/haproxy_exporter --haproxy.scrape-
uri="http://admin:123456@10.0.0.106:9999/haproxy-status;csv"
#也支持通过socket文件实现
#ExecStart=/usr/local/haproxy_exporter/bin/haproxy_exporter --haproxy.scrape-
uri=unix:/run/haproxy/admin.sock
Restart=on-failure
[Install]
WantedBy=multi-user.target
#配置解析：在原来的配置文件基础上，添加了 --haproxy.scrape-uri属性来指定haproxy状态值的获取
#重载并重启服务
systemctl daemon-reload
systemctl enable --now haproxy_exporter.service
systemctl status haproxy_exporter.service
#检查是否监听9101/tcp端口
ss -ntlp|grep haproxy
LISTEN    0 492  0.0.0.0:9999 0.0.0.0:*        users:(("haproxy",pid=124021,fd=7))
LISTEN    0 4096         *:9101       *:*        users:
(("haproxy_exporte",pid=126538,fd=3))
```

7.3.1.2.3 修改 Prometheus 配置
```yaml
#修改prometheus的配置文件，让它自动过滤文件中的节点信息
vim /usr/local/prometheus/conf/prometheus.yml
...
  - job_name: "haproxy_exporter"
    static_configs:
      - targets: ["10.0.0.104:9101"]
#重启服务
systemctl reload prometheus.service
#稍等几秒钟，到浏览器中查看监控目标
```

![原 PDF 第 301 页插图](assets/img-88d26e4992210192.png)

![原 PDF 第 301 页插图](assets/img-8a181e16c374823c.png)

7.3.1.2.4 Grafana 图形展示
```text
导入grafana的镜像模板文件 https://grafana.com/grafana/dashboards/2428 ,查看效果
```

![原 PDF 第 302 页插图](assets/img-bb9b5f98ae123e50.png)

![原 PDF 第 302 页插图](assets/img-37edb1c4cf8fd3ec.png)

![原 PDF 第 302 页插图](assets/img-bb8824f1ee8d62f9.png)

### 7.3.2 Haproxy 内置功能实现监控

haproxy自从2.X 版本开始，就提供了专用的暴露数据的功能，只需要在编译安装haproxy的时候，开启该功能即可，然后，就可以按照传统的prometheus监控目标的方式来进行监控了。

#### 7.3.2.1 安装 Haproxy 开启内置的监控 Exporter 功能

7.3.2.1.1 包安装 haproxy

Ubuntu 22.04 包安装默认内置了 /metrics 的接口，无需编译安装
```bash
[root@ubuntu2204 ~]#apt update && apt install haproxy -y
[root@ubuntu2204 ~]#haproxy  -vv
HAProxy version 2.4.18-0ubuntu1.2 2023/02/13 - https://haproxy.org/
Status: long-term supported branch - will stop receiving fixes around Q2 2026.
Known bugs: http://www.haproxy.org/bugs/bugs-2.4.18.html
Running on: Linux 5.15.0-52-generic #58-Ubuntu SMP Thu Oct 13 08:03:55 UTC 2022
x86_64
Build options :
  TARGET  = linux-glibc
  CPU     = generic
  CC      = cc
  CFLAGS  = -O2 -g -O2 -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -
fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -
D_FORTIFY_SOURCE=2 -Wall -Wextra -Wdeclaration-after-statement -fwrapv -Wno-address-
of-packed-member -Wno-unused-label -Wno-sign-compare -Wno-unused-parameter -Wno-
clobbered -Wno-missing-field-initializers -Wno-cast-function-type -Wtype-limits -
Wshift-negative-value -Wshift-overflow=2 -Wduplicated-cond -Wnull-dereference
  OPTIONS = USE_PCRE2=1 USE_PCRE2_JIT=1 USE_OPENSSL=1 USE_LUA=1 USE_SLZ=1
USE_SYSTEMD=1 USE_PROMEX=1
  DEBUG   =
```

7.3.2.1.2 编译安装 haproxy
```bash
#安装依赖软件
apt update
apt -y install  gcc make libssl-dev libpcre3 libpcre3-dev zlib1g-dev libreadline-dev
libsystemd-dev
#获取lua软件
wget http://www.lua.org/ftp/lua-5.4.3.tar.gz
tar zxf lua-5.4.3.tar.gz -C /usr/local/
cd /usr/local/lua-5.4.3
make all test
cd
#获取软件
wget https://www.haproxy.org/download/2.5/src/haproxy-2.5.0.tar.gz
tar xf haproxy-2.5.0.tar.gz -C /usr/local/src
cd /usr/local/src/haproxy-2.5.0/
#定制编译变量
make -j $(nproc) ARCH=x86_64 TARGET=linux-glibc USE_PCRE=1 USE_OPENSSL=1 USE_ZLIB=1
USE_SYSTEMD=1 USE_CPU_AFFINITY=1 USE_PROMEX=1 USE_LUA=1 LUA_INC=/usr/local/lua-
5.4.3/src/ LUA_LIB=/usr/local/lua-5.4.3/src/
#解析：
-j $(nproc) 指的是cpu的核数
#在 HAProxy 2.0.x - 2.3.x ，使用 EXTRA_OBJS 参数来进行 make 构建
EXTRA_OBJS="contrib/prometheus-exporter/service-prometheus.o"
#在 HAProxy 2.4.x 版本 ，使用 USE_PROMEX 参数来进行 make 构建：
make TARGET=linux-glibc USE_PROMEX=1
#编译安装
make install PREFIX=/usr/local/haproxy
#定制命令软连接
ln -s /usr/local/haproxy/sbin/haproxy /usr/local/sbin/
/usr/local/sbin/haproxy -v
```

#### 7.3.2.2 定制 Haproxy 服务功能
```ini
#创建相关的配置文件目录
mkdir -p /etc/haproxy/ /var/lib/haproxy
#准备错误文件
cp -r /usr/local/src/haproxy-2.5.0/examples/errorfiles /usr/local/haproxy/
ln -s /usr/local/haproxy/errorfiles /etc/haproxy/errorfiles
#准备配置文件
vim /etc/haproxy/haproxy.cfg
global
    maxconn 100000
    chroot /usr/local/haproxy
    stats socket /var/lib/haproxy/haproxy.sock mode 600 level admin
    daemon
    pidfile /var/lib/haproxy/haproxy.pid
    log 127.0.0.1 local7 debug
defaults
    option http-keep-alive
    option  forwardfor
    maxconn 100000
    mode http
    timeout connect 300000ms
    timeout client  300000ms
    timeout server  300000ms
frontend stats
    bind *:9999
    stats enable
    stats uri /haproxy-status
    stats refresh 10s
    http-request use-service prometheus-exporter if { path /metrics }  #添加此行实
现/metrics暴露
#配置解析：http-request 属性表明，开启了一个专属的metrics的url地址
#准备service服务启动文件
vim /lib/systemd/system/haproxy.service
[Unit]
Description=HAProxy Load Balancer
After=syslog.target network.target
[Service]
ExecStartPre=/usr/local/haproxy/sbin/haproxy -f /etc/haproxy/haproxy.cfg  -c -q
ExecStart=/usr/local/haproxy/sbin/haproxy -Ws -f /etc/haproxy/haproxy.cfg -p
/var/lib/haproxy/haproxy.pid
ExecReload=/bin/kill -USR2 $MAINPID
[Install]
WantedBy=multi-user.target
#属性解析：
-Ws 代表haproxy启动的模式是 Master/Workers 的进程模式
-USR2 是 haproxy的master-worker模式下自定义的软stop信号，可以通过 man haproxy 方式查看
#启动服务
systemctl daemon-reload
systemctl enable --now haproxy
systemctl status haproxy
#查看服务状态
pstree -p |grep haproxy
           |-haproxy(15128)---haproxy(15130)---{haproxy}(15132)
s -tnulp | grep haproxy
tcp     LISTEN   0  4096  0.0.0.0:9999           0.0.0.0:*
users:(("haproxy",pid=30582,fd=6))
#浏览器访问 http://10.0.0.106:9999/haproxy-status 页面
```

![原 PDF 第 305 页插图](assets/img-50163f5d583a7deb.png)
```text
浏览器访问:http://10.0.0.106:9999/metrics 页面
```

![原 PDF 第 305 页插图](assets/img-8872212d37031767.png)

#### 7.3.2.3 修改 Prometheus 配置
```yaml
#修改prometheus的配置文件，让它自动过滤文件中的节点信息
vim /usr/local/prometheus/conf/prometheus.yml
...
  - job_name: "mertics_from_haproxy"
    static_configs:
      - targets: ["10.0.0.106:9999"]
#重启服务
systemctl reload prometheus.service
#稍等几秒钟，到浏览器中查看监控目标
```

![原 PDF 第 306 页插图](assets/img-7c12f9404fcbb40e.png)

![原 PDF 第 306 页插图](assets/img-0c247762edec11a4.png)

#### 7.3.2.4 Grafana 图形展示
```text
#导入grafana的镜像模板文件 https://grafana.com/grafana/dashboards/12693 ,查看效果
#注意：两种方式的haproxy的grafana的模板不一样，使用的底层机制不太一样
```

![原 PDF 第 306 页插图](assets/img-835a6a1bdc2eafc6.png)

![原 PDF 第 307 页插图](assets/img-a8b2bf84ca014b31.png)

![原 PDF 第 307 页插图](assets/img-06278194a919bd02.png)

## 7.4 Java 应用监控

对于 Java 应用， 可以借助于专门的 jmx exporter方式来暴露相关的指标数据
```text
#下载链接:
https://prometheus.io/download/
#官方地址：
https://github.com/prometheus/jmx_exporter
```

### 7.4.1 准备 Java 环境
```bash
#方法1：包安装 Tomcat
[root@ubuntu2404 ~]#apt update && apt -y install tomcat10
[root@ubuntu2204 ~]#apt update && apt -y install tomcat9
[root@ubuntu2004 ~]#apt update && apt -y install tomcat9
#方法2：二进制安装 Tomcat
#下载java,最新java8下载地址：
https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html
#安装java
tar xf jdk-8u121-linux-x64.tar.gz -C /usr/local
cd /usr/local/
ln -s jdk1.8.0_121 java
#配置java环境变量
echo 'export JAVA_HOME=/usr/local/java' >> /etc/profile.d/java.sh
echo 'export JRE_HOME=$JAVA_HOME/jre' >> /etc/profile.d/java.sh
echo 'export CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar' >>
/etc/profile.d/java.sh
echo 'export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH' >> /etc/profile.d/java.sh
source /etc/profile.d/java.sh
#检查效果
java -version
#获取java软件,此处以tomcat为例
wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.56/bin/apache-tomcat-9.0.56.tar.gz
#解压软件
tar xf apache-tomcat-9.0.56.tar.gz -C /usr/local/
ln -s /usr/local/apache-tomcat-9.0.56 /usr/local/tomcat
#定制环境变量
echo 'PATH=$PATH:/usr/local/tomcat/bin' >> /etc/profile
source /etc/profile
#尝试启动tomcat
catalina.sh start
#检查效果
netstat -tnulp | grep java
tcp6       0  0 127.0.0.1:8005          :::*                    LISTEN
 29447/java
tcp6       0  0 :::8080                 :::*                    LISTEN
 29447/java
```

### 7.4.2 准备 Jmx Exporter
```bash
#获取软件
#新版本
wget
https://github.com/prometheus/jmx_exporter/releases/download/1.3.0/jmx_prometheus_javaagent-1.3.0.jar
wget
https://github.com/prometheus/jmx_exporter/releases/download/1.2.0/jmx_prometheus_javaagent-1.2.0.jar
wget
https://github.com/prometheus/jmx_exporter/releases/download/1.1.0/jmx_prometheus_javaagent-1.1.0.jar
wget
https://repo.maven.apache.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/1.0.1/jmx_prometheus_javaagent-1.0.1.jar
#旧版本
wget
https://repo.maven.apache.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar
wget
https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.19.0/jmx_prometheus_javaagent-0.19.0.jar
wget
https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.17.2/jmx_prometheus_javaagent-0.17.2.jar
wget
https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.16.1/jmx_prometheus_javaagent-0.16.1.jar
#下载配置文件，可能需要科学上网
wget https://github.com/prometheus/jmx_exporter/blob/main/example_configs/tomcat.yml
wget
https://raw.githubusercontent.com/prometheus/jmx_exporter/master/example_configs/tomcat.yml
#准备配置文件内容
cat tomcat.yml
---
lowercaseOutputLabelNames: true
lowercaseOutputName: true
rules:
- pattern: 'Catalina<type=GlobalRequestProcessor, name=\"(\w+-\w+)-(\d+)\"><>(\w+):'
  name: tomcat_$3_total
  labels:
    port: "$2"
    protocol: "$1"
  help: Tomcat global $3
  type: COUNTER
- pattern: 'Catalina<j2eeType=Servlet, WebModule=//([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-
zA-Z0-9+&@#/%=~_|]), name=([-a-zA-Z0-9+/$%~_-|!.]*), J2EEApplication=none,
J2EEServer=none><>(requestCount|maxTime|processingTime|errorCount):'
  name: tomcat_servlet_$3_total
  labels:
    module: "$1"
    servlet: "$2"
  help: Tomcat servlet $3 total
  type: COUNTER
- pattern: 'Catalina<type=ThreadPool, name="(\w+-\w+)-(\d+)"><>
(currentThreadCount|currentThreadsBusy|keepAliveCount|pollerThreadCount|connectionCou
nt):'
  name: tomcat_threadpool_$3
  labels:
    port: "$2"
    protocol: "$1"
  help: Tomcat threadpool $3
  type: GAUGE
- pattern: 'Catalina<type=Manager, host=([-a-zA-Z0-9+&@#/%?=~_|!:.,;]*[-a-zA-Z0-
9+&@#/%=~_|]), context=([-a-zA-Z0-9+/$%~_-|!.]*)><>
(processingTime|sessionCounter|rejectedSessions|expiredSessions):'
  name: tomcat_session_$3_total
  labels:
    context: "$2"
    host: "$1"
  help: Tomcat session $3 total
  type: COUNTER
#准备相关文件
#1：包安装tomcat
#Ubuntu24.04版本
[root@ubuntu2404 ~]#mv jmx_prometheus_javaagent-1.1.0.jar /usr/share/tomcat10/lib/
[root@ubuntu2404 ~]#mv tomcat.yml /usr/share/tomcat10/etc/
#Ubuntu22.04之前版本
mv jmx_prometheus_javaagent-0.16.1.jar  /usr/share/tomcat9/lib/
mv tomcat.yml /usr/share/tomcat9/etc/
#方式2：二进制安装tomcat
cp jmx_prometheus_javaagent-0.16.1.jar /usr/local/tomcat/bin/
cp tomcat.yml /usr/local/tomcat/bin/
#修改tomcat的启动脚本 catalina.sh
#方式1：包安装tomcat，9527为监听的端口号
#Ubuntu24.04版本
[root@ubuntu2404 ~]#vim /usr/share/tomcat10/bin/catalina.sh
JAVA_OPTS="-javaagent:/usr/share/tomcat10/lib/jmx_prometheus_javaagent-
1.1.0.jar=9527:/usr/share/tomcat10/etc/tomcat.yml"
[root@ubuntu2404 ~]#systemctl restart tomcat10.service
[root@ubuntu2404 ~]#ps aux|grep jmx
tomcat      5313 25.8  8.2 3122088 162636 ?      Ssl  14:43   0:04
/usr/lib/jvm/default-java/bin/java -
Djava.util.logging.config.file=/var/lib/tomcat10/conf/logging.properties -
Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -
javaagent:/usr/share/tomcat10/lib/jmx_prometheus_javaagent-
1.1.0.jar=9527:/usr/share/tomcat10/etc/tomcat.yml -Djdk.tls.ephemeralDHKeySize=2048 -
Djava.protocol.handler.pkgs=org.apache.catalina.webresources -
Dorg.apache.catalina.security.SecurityListener.UMASK=0027 --add-
opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --
add-opens=java.base/java.util=ALL-UNNAMED --add-
opens=java.base/java.util.concurrent=ALL-UNNAMED --add-
opens=java.rmi/sun.rmi.transport=ALL-UNNAMED -classpath
/usr/share/tomcat10/bin/bootstrap.jar:/usr/share/tomcat10/bin/tomcat-juli.jar -
Dcatalina.base=/var/lib/tomcat10 -Dcatalina.home=/usr/share/tomcat10 -
Djava.io.tmpdir=/tmp org.apache.catalina.startup.Bootstrap start
#Ubuntu22.04之前版本
vim /usr/share/tomcat9/bin/catalina.sh
.......
JAVA_OPTS="-javaagent:/usr/share/tomcat9/lib/jmx_prometheus_javaagent-
0.16.1.jar=9527:/usr/share/tomcat9/etc/tomcat.yml"
# OS specific support.  $var _must_ be set to either true or false.
......
[root@ubuntu2204 ~]#systemctl restart tomcat9.service
#2：二进制安装tomcat
vim /usr/local/tomcat/bin/catalina.sh
......
# OS specific support.  $var _must_ be set to either true or false.
JAVA_OPTS="$JAVA_OPTS $JSSE_OPTS"
JAVA_OPTS="-javaagent:/usr/local/tomcat/bin/jmx_prometheus_javaagent-
0.16.1.jar=9527:/usr/local/tomcat/bin/tomcat.yml"
#重启tomcat
catalina.sh stop
catalina.sh start
#查看效果
ss -tnulp | grep java
tcp    LISTEN  0 1   [::ffff:127.0.0.1]:8005    *:*      users:
(("java",pid=59676,fd=66))
tcp    LISTEN  0 50                   *:2181    *:*      users:
(("java",pid=928,fd=60))
tcp    LISTEN  0 3                    *:9527    *:*      users:
(("java",pid=59676,fd=13))
tcp    LISTEN  0 50                   *:40651   *:*      users:
(("java",pid=928,fd=45))
tcp    LISTEN  0 50                   *:8080    *:*      users:
(("java",pid=928,fd=52))
tcp    LISTEN  0 50                   *:7000    *:*      users:
(("java",pid=928,fd=47))
#浏览器访问:
http://10.0.0.106:9527/metrics
```

![原 PDF 第 311 页插图](assets/img-32a1bcd48afb965a.png)

### 7.4.3 修改 Prometheus 配置
```yaml
#修改prometheus的配置文件，让它自动过滤文件中的节点信息
vim /usr/local/prometheus/conf/prometheus.yml
...
  - job_name: "mertics_from_tomcat"
    static_configs:
      - targets: ["10.0.0.106:9527"]
#重启服务
systemctl reload prometheus.service
#稍等几秒钟，到浏览器中查看监控目标
```

![原 PDF 第 312 页插图](assets/img-dfaeb9f2474f54e9.png)

![原 PDF 第 312 页插图](assets/img-9deeae7362a2f364.png)

### 7.4.4 Grafana 图形展示
```text
#导入grafana的镜像模板文件 https://grafana.com/grafana/dashboards/8704|14845,查看效果
#需要手动指定job名和target信息
```

![原 PDF 第 312 页插图](assets/img-d62b6db57434c767.png)

注意：默认job为java , 需要修改job名称为前面prometheus中配置的job名称 mertics_from_tomcat

![原 PDF 第 313 页插图](assets/img-b2cfacb456b2803c.png)

![原 PDF 第 313 页插图](assets/img-e819edce34b4c5e2.png)

### 7.4.5 基于 docker compose 实现监控 tomcat
https://github.com/nlighten/tomcat_exporter

范例
```bash
[root@ubuntu2204 tomcat-metrics]#tree
.
├── docker-compose.yml
└── tomcat
    ├── context.xml
    ├── Dockerfile
    ├── sources.list
    └── tomcat-users.xml
1 directory, 5 files
[root@ubuntu2204 tomcat-metrics]#cat docker-compose.yml
version: '3.6'
volumes:
    tomcat_webapps: {}
networks:
  monitoring:
    driver: bridge
    ipam:
      config:
         - subnet: 172.31.0.0/24
services:
  tomcat:
    #image: tomcat:jdk11
    build:
      context: tomcat
      dockerfile: Dockerfile
    hostname: tomcat.bowen.org
    expose:
      - 8080
    ports:
      - 8080:8080
    volumes:
      - tomcat_webapps:/usr/local/tomcat/webapps
      - ./tomcat/tomcat-users.xml:/usr/local/tomcat/conf/tomcat-users.xml
    networks:
      - monitoring
    environment:
      TZ: Asia/Shanghai
[root@ubuntu2204 tomcat-metrics]#cat tomcat/context.xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<Context antiResourceLocking="false" privileged="true" >
  <CookieProcessor className="org.apache.tomcat.util.http.Rfc6265CookieProcessor"
                     sameSiteCookies="strict" />
<!--
  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
          allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />
-->
  <Manager sessionAttributeValueClassNameFilter="java\.lang\.
(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.CsrfPrevention
Filter\$LruCache(?:\$1)?|java\.util\.(?:Linked)?HashMap"/>
</Context>
[root@ubuntu2204 tomcat-metrics]#cat tomcat/Dockerfile
FROM tomcat:9.0-jdk17-openjdk-slim
ADD ./sources.list /etc/apt/sources.list
ENV TOMCAT_SIMPLECLIENT_VERSION=0.12.0
ENV TOMCAT_EXPORTER_VERSION=0.0.15
RUN apt-get update && apt-get install -y curl && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=io/prometheus/simpleclient/${TOMCAT_SIMPLECLIENT_VERSION}/simpleclient-${TOM
CAT_SIMPLECLIENT_VERSION}.jar --output
/usr/local/tomcat/lib/simpleclient-${TOMCAT_SIMPLECLIENT_VERSION}.jar && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=io/prometheus/simpleclient_common/${TOMCAT_SIMPLECLIENT_VERSION}/simpleclien
t_common-${TOMCAT_SIMPLECLIENT_VERSION}.jar --output
/usr/local/tomcat/lib/simpleclient_common-${TOMCAT_SIMPLECLIENT_VERSION}.jar && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=io/prometheus/simpleclient_hotspot/${TOMCAT_SIMPLECLIENT_VERSION}/simpleclie
nt_hotspot-${TOMCAT_SIMPLECLIENT_VERSION}.jar --output
/usr/local/tomcat/lib/simpleclient_hotspot-${TOMCAT_SIMPLECLIENT_VERSION}.jar && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=io/prometheus/simpleclient_servlet/${TOMCAT_SIMPLECLIENT_VERSION}/simpleclie
nt_servlet-${TOMCAT_SIMPLECLIENT_VERSION}.jar --output
/usr/local/tomcat/lib/simpleclient_servlet-${TOMCAT_SIMPLECLIENT_VERSION}.jar && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=io/prometheus/simpleclient_servlet_common/${TOMCAT_SIMPLECLIENT_VERSION}/sim
pleclient_servlet_common-${TOMCAT_SIMPLECLIENT_VERSION}.jar --output
/usr/local/tomcat/lib/simpleclient_servlet_common-${TOMCAT_SIMPLECLIENT_VERSION}.jar
&& \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=nl/nlighten/tomcat_exporter_client/${TOMCAT_EXPORTER_VERSION}/tomcat_exporte
r_client-${TOMCAT_EXPORTER_VERSION}.jar --output
/usr/local/tomcat/lib/tomcat_exporter_client-${TOMCAT_EXPORTER_VERSION}.jar && \
    curl -v --fail --location https://search.maven.org/remotecontent?
filepath=nl/nlighten/tomcat_exporter_servlet/${TOMCAT_EXPORTER_VERSION}/tomcat_export
er_servlet-${TOMCAT_EXPORTER_VERSION}.war --output
/usr/local/tomcat/webapps/metrics.war
RUN mv /usr/local/tomcat/webapps.dist/* /usr/local/tomcat/webapps/
ADD ./context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml
[root@ubuntu2204 tomcat-metrics]#cat tomcat/sources.list
deb https://repo.huaweicloud.com/debian/ bullseye main non-free contrib
deb-src https://repo.huaweicloud.com/debian/ bullseye main non-free contrib
deb https://repo.huaweicloud.com/debian-security/ bullseye-security main
deb-src https://repo.huaweicloud.com/debian-security/ bullseye-security main
deb https://repo.huaweicloud.com/debian/ bullseye-updates main non-free contrib
deb-src https://repo.huaweicloud.com/debian/ bullseye-updates main non-free contrib
deb https://repo.huaweicloud.com/debian/ bullseye-backports main non-free contrib
deb-src https://repo.huaweicloud.com/debian/ bullseye-backports main non-free contrib
[root@ubuntu2204 tomcat-metrics]#cat tomcat/tomcat-users.xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at
      http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
               version="1.0">
<!--
  By default, no user is included in the "manager-gui" role required
  to operate the "/manager/html" web application.  If you wish to use this app,
  you must define such a user - the username and password are arbitrary.
  Built-in Tomcat manager roles:
    - manager-gui    - allows access to the HTML GUI and the status pages
    - manager-script - allows access to the HTTP API and the status pages
    - manager-jmx    - allows access to the JMX proxy and the status pages
    - manager-status - allows access to the status pages only
  The users below are wrapped in a comment and are therefore ignored. If you
  wish to configure one or more of these users for use with the manager web
  application, do not forget to remove the <!.. ..> that surrounds them. You
  will also need to set the passwords to something appropriate.
-->
<!--
  <user username="admin" password="<must-be-changed>" roles="manager-gui"/>
  <user username="robot" password="<must-be-changed>" roles="manager-script"/>
-->
<!--
  The sample user and role entries below are intended for use with the
  examples web application. They are wrapped in a comment and thus are ignored
  when reading this file. If you wish to configure these users for use with the
  examples web application, do not forget to remove the <!.. ..> that surrounds
  them. You will also need to set the passwords to something appropriate.
-->
<!--
  <role rolename="tomcat"/>
  <role rolename="role1"/>
  <user username="tomcat" password="<must-be-changed>" roles="tomcat"/>
  <user username="both" password="<must-be-changed>" roles="tomcat,role1"/>
  <user username="role1" password="<must-be-changed>" roles="role1"/>
-->
  <role rolename="manager-gui"/>
  <role rolename="manager-script"/>
  <user username="tomcat" password="123456" roles="manager-gui,manager-script"/>
</tomcat-users>
[root@ubuntu2204 tomcat-metrics]#docker-compose build
[root@ubuntu2204 tomcat-metrics]#docker-compose up -d
#修改prometheus的配置文件，让它自动过滤文件中的节点信息
[root@ubuntu2204 ~]#vim /usr/local/prometheus/conf/prometheus.yml
...
  - job_name: "mertics_from_tomcat"
    static_configs:
      - targets: ["tomcat.bowen.org:8080"]
#生效服务
[root@ubuntu2204 ~]#systemctl reload prometheus.service
```

![原 PDF 第 317 页插图](assets/img-cacb00c8f9c9c6e0.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/22-node-mysql-exporters.html' | relative_url }}">← 上一章：Node Exporter 与 MySQL 监控</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/24-redis-nginx-exporters.html' | relative_url }}">下一章：Redis 与 Nginx 监控 →</a>
</nav>
