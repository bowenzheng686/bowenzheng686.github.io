---
layout: default
title: "ELK Log Analytics · Installing Elasticsearch"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 07 Installing Elasticsearch
### 2.3 Elasticsearch 安装

### 包安装 Elasticsearch

### 安装 Elasticsearch 包

下载链接

<https://www.elastic.co/cn/downloads/elasticsearch>

<https://mirrors.tuna.tsinghua.edu.cn/elasticstack/>

范例：安装 elasticsearch-9

```bash
[root@ubuntu2404 ~]#wget
https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.4-
amd64.deb
dpkg -i elasticsearch-9.0.4-amd64.deb
systemctl enable --now  elasticsearch.service
......
--------------------------- Security autoconfiguration information -------------
-----------------
Authentication and authorization are enabled.
TLS for the transport and HTTP layers is enabled and configured.
The generated password for the elastic built-in superuser is :
cz+1XmXs9lPgOYWockJq #密码
If this node should join an existing cluster, you can reconfigure this with
'/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token
<token-here>'
after creating an enrollment token on your existing cluster.
You can complete the following actions at any time:
Reset the password of the elastic built-in superuser with
'/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.
Generate an enrollment token for Kibana instances with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.
Generate an enrollment token for Elasticsearch nodes with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.
---------------------------------------------------------------------------------
----------------
### NOT starting on installation, please execute the following statements to
configure elasticsearch service to start automatically using systemd
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
sudo systemctl start elasticsearch.service
```

```json
#默认9.X开启xpack安全，导致无法直接访问
[root@ubuntu2204 ~]#curl http://127.0.0.1:9200/
curl: (52) Empty reply from server
[root@ubuntu2404 ~]#PASSWORD=cz+1XmXs9lPgOYWockJq
curl -u"elastic:$PASSWORD" -k  https://127.0.0.1:9200
{
"name" : "ubuntu2404.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "jGW_RCOsQDCeZwdGAEO2eA",
"version" : {
"number" : "9.0.4",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "e03b6699309ed1458e07dbcd94918b36f5ffee9e",
"build_date" : "2025-07-16T22:08:05.257395109Z",
"build_snapshot" : false,
"lucene_version" : "10.1.0",
"minimum_wire_compatibility_version" : "8.18.0",
"minimum_index_compatibility_version" : "8.0.0"
},
"tagline" : "You Know, for Search"
}
#关闭XPACK功能
[root@ubuntu2404 ~]#vim /etc/elasticsearch/elasticsearch.yml
.....
xpack.security.enabled: false #修改为false
```

```bash
[root@ubuntu2404 ~]#systemctl restart elasticsearch.service
```

```json
[root@ubuntu2404 ~]#curl   http://127.0.0.1:9200
{
"name" : "ubuntu2404.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "jGW_RCOsQDCeZwdGAEO2eA",
"version" : {
"number" : "9.0.4",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "e03b6699309ed1458e07dbcd94918b36f5ffee9e",
"build_date" : "2025-07-16T22:08:05.257395109Z",
"build_snapshot" : false,
"lucene_version" : "10.1.0",
"minimum_wire_compatibility_version" : "8.18.0",
"minimum_index_compatibility_version" : "8.0.0"
},
"tagline" : "You Know, for Search"
}
```

范例：安装 elasticsearch-8

```bash
#注意：是elasticsearch目录，不是enterprise-search目录
[root@ubuntu2204 ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/elasticstack/8.x/apt/pool/main/e/elasticsea
rch/elasticsearch-8.6.1-amd64.deb
[root@ubuntu2204 ~]#dpkg -i elasticsearch-8.6.1-amd64.deb
正在选中未选择的软件包 elasticsearch。
(正在读取数据库 ... 系统当前共安装有 73714 个文件和目录。)
准备解压 elasticsearch-8.6.1-amd64.deb  ...
Creating elasticsearch group... OK
Creating elasticsearch user... OK
正在解压 elasticsearch (8.6.1) ...
正在设置 elasticsearch (8.6.1) ...
--------------------------- Security autoconfiguration information -------------
-----------------
Authentication and authorization are enabled.
TLS for the transport and HTTP layers is enabled and configured.
The generated password for the elastic built-in superuser is :
35uYxBSsBS9g_Q2eSJ__
If this node should join an existing cluster, you can reconfigure this with
'/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token
<token-here>'
after creating an enrollment token on your existing cluster.
You can complete the following actions at any time:
Reset the password of the elastic built-in superuser with
'/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.
Generate an enrollment token for Kibana instances with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.
Generate an enrollment token for Elasticsearch nodes with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.
---------------------------------------------------------------------------------
----------------
### NOT starting on installation, please execute the following statements to
configure elasticsearch service to start automatically using systemd
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
sudo systemctl start elasticsearch.service
#内置JAVA
[root@ubuntu2204 ~]#/usr/share/elasticsearch/jdk/bin/java -version
openjdk version "19.0.1" 2022-10-18
OpenJDK Runtime Environment (build 19.0.1+10-21)
OpenJDK 64-Bit Server VM (build 19.0.1+10-21, mixed mode, sharing)
#JVM优化
[root@ubuntu2204 ~]#vim /etc/elasticsearch/jvm.options
## -Xms4g
-Xms128m
## -Xmx4g
-Xmx128m
[root@ubuntu2204 ~]#systemctl enable --now elasticsearch.service
#默认8.X开启xpack安全，导致无法直接访问
[root@ubuntu2204 ~]#curl http://127.0.0.1:9200/
curl: (52) Empty reply from server
#方法1：基于XPACK安全功能的密码直接访问
[root@ubuntu2204 ~]#PASSWORD=35uYxBSsBS9g_Q2eSJ__
[root@ubuntu2204 ~]#curl -u"elastic:$PASSWORD" -k  https://127.0.0.1:9200
[root@ubuntu2204 ~]#curl   https://”elastic:$PASSWORD“@10.0.0.100:9200 -k
{
"name" : "ubuntu2204.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "0cOiGg3SSGeOnO1AF0a61w",
"version" : {
"number" : "8.15.3",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "f97532e680b555c3a05e73a74c28afb666923018",
"build_date" : "2024-10-09T22:08:00.328917561Z",
"build_snapshot" : false,
"lucene_version" : "9.11.1",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
```

```json
#方法2：关闭xpack安全功能
[root@ubuntu2204 ~]#vim /etc/elasticsearch/elasticsearch.yml
xpack.security.enabled: false  #默认值为true
[root@ubuntu2204 ~]#systemctl restart elasticsearch.service
[root@ubuntu2204 ~]#curl http://127.0.0.1:9200/
{
"name" : "node-1",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "fz_huZn7SAW51VlvmdlX-A",
"version" : {
"number" : "8.6.1",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "180c9830da956993e59e2cd70eb32b5e383ea42c",
"build_date" : "2023-01-24T21:35:11.506992272Z",
"build_snapshot" : false,
"lucene_version" : "9.4.2",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
#ES8.8.2的JAVA版本
[root@ubuntu2204 ~]#/usr/share/elasticsearch/jdk/bin/java -version
openjdk version "20.0.1" 2023-04-18
OpenJDK Runtime Environment (build 20.0.1+9-29)
OpenJDK 64-Bit Server VM (build 20.0.1+9-29, mixed mode, sharing)
```

范例: Ubuntu 安装包含JDK的elasticsearch-7 包

```bash
[root@node1 ~]#dpkg -i elasticsearch-7.14.0-amd64.deb
[root@node1 ~]#systemctl daemon-reload
[root@node1 ~]#systemctl enable --now elasticsearch.service
[root@node1 ~]#pstree -p |grep java
|-java(1341)-+-controller(1538)-+-{controller}(1540)
|            |-{java}(1519)
|            |-{java}(1520)
|            |-{java}(1521)
|            |-{java}(1522)
[root@node1 ~]#ss -ntl
State  Recv-Q  Send-Q       Local Address:Port   Peer Address:Port
LISTEN 0       128          127.0.0.53%lo:53          0.0.0.0:*
LISTEN 0       128                0.0.0.0:22          0.0.0.0:*
LISTEN 0       128              127.0.0.1:6010        0.0.0.0:*
LISTEN 0       128              127.0.0.1:6011        0.0.0.0:*
LISTEN 0       128     [::ffff:127.0.0.1]:9200              *:*
LISTEN 0       128                  [::1]:9200           [::]:*
LISTEN 0       128     [::ffff:127.0.0.1]:9300              *:*
LISTEN 0       128                  [::1]:9300           [::]:*
LISTEN 0       128                   [::]:22             [::]:*
LISTEN 0       128                  [::1]:6010           [::]:*
LISTEN 0       128                  [::1]:6011           [::]:*
[root@node1 ~]#ss -ntlp|grep java
LISTEN  0  128  [::ffff:127.0.0.1]:9200     *:*       users:
(("java",pid=1341,fd=287))
LISTEN  0  128               [::1]:9200  [::]:*       users:
(("java",pid=1341,fd=286))
LISTEN  0  128  [::ffff:127.0.0.1]:9300     *:*       users:
(("java",pid=1341,fd=284))
LISTEN  0  128               [::1]:9300  [::]:*       users:
(("java",pid=1341,fd=283))
[root@node1 ~]#curl 127.0.0.1:9200
{
"name" : "node1.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "vvp4iBkkTfOJPf_rtcE0Og",
"version" : {
"number" : "7.14.0",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "dd5a0a2acaa2045ff9624f3729fc8a6f40835aa1",
"build_date" : "2021-07-29T20:49:32.864135063Z",
"build_snapshot" : false,
"lucene_version" : "8.9.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
[root@node1 ~]#curl 127.0.0.1:9300
This is not an HTTP port
```

范例: Ubuntu 安装不包含 JDK 的elasticsearch 包

```sql
[root@ubuntu1804 ~]#apt update
[root@ubuntu1804 ~]#apt -y install openjdk-8-jdk
#默认无法找到Java,安装失败
[root@ubuntu1804 ~]#dpkg -i elasticsearch-7.14.0-no-jdk-amd64.deb
update-alternatives: using /usr/lib/jvm/java-8-openjdk-amd64/bin/appletviewer to
provide /usr/bin/appletviewer (appletviewer) in auto mode
update-alternatives: using /usr/lib/jvm/java-8-openjdk-amd64/bin/jconsole to
provide /usr/bin/jconsole (jconsole) in auto mode
Processing triggers for libgdk-pixbuf2.0-0:amd64 (2.36.11-2) ...
Processing triggers for libc-bin (2.27-3ubuntu1.2) ...
Errors were encountered while processing:
elasticsearch
E: Sub-process /usr/bin/dpkg returned an error code (1)
(Reading database ... 88094 files and directories currently installed.)
Preparing to unpack elasticsearch-7.14.0-no-jdk-amd64.deb ...
Unpacking elasticsearch (7.14.0) over (7.14.0) ...
Setting up elasticsearch (7.14.0) ...
### NOT starting on installation, please execute the following statements to
configure elasticsearch service to start automatically using systemd
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
sudo systemctl start elasticsearch.service
could not find java in bundled JDK at /usr/share/elasticsearch/jdk/bin/java
dpkg: error processing package elasticsearch (--install):
installed elasticsearch package post-installation script subprocess returned
error exit status 1
Processing triggers for ureadahead (0.100.0-21) ...
Processing triggers for systemd (237-3ubuntu10.42) ...
Errors were encountered while processing:
elasticsearch
[root@ubuntu1804 ~]#java -version
openjdk version "1.8.0_292"
OpenJDK Runtime Environment (build 1.8.0_292-8u292-b10-0ubuntu1~18.04-b10)
OpenJDK 64-Bit Server VM (build 25.292-b10, mixed mode)
[root@ubuntu1804 ~]#which java
/usr/bin/java
#配置JAVA环境
[root@ubuntu1804 ~]#mkdir /usr/share/elasticsearch/jdk/bin/ -p
[root@ubuntu1804 ~]#ln -s /usr/bin/java /usr/share/elasticsearch/jdk/bin/java
#提示非no-jdk的发行版将被淘汰,建议使用包含JDK的包
[root@ubuntu1804 ~]#dpkg -i elasticsearch-7.14.0-no-jdk-amd64.deb
(Reading database ... 88094 files and directories currently installed.)
Preparing to unpack elasticsearch-7.14.0-no-jdk-amd64.deb ...
Unpacking elasticsearch (7.14.0) over (7.14.0) ...
Setting up elasticsearch (7.14.0) ...
### NOT starting on installation, please execute the following statements to
configure elasticsearch service to start automatically using systemd
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
sudo systemctl start elasticsearch.service
Future versions of Elasticsearch will require Java 11; your Java version from
[/usr/lib/jvm/java-8-openjdk-amd64/jre] does not meet this requirement. Consider
switching to a distribution of Elasticsearch with a bundled JDK. If you are
already using a distribution with a bundled JDK, ensure the JAVA_HOME environment
variable is not set.
warning: no-jdk distributions that do not bundle a JDK are deprecated and will
be removed in a future release
Created elasticsearch keystore in /etc/elasticsearch/elasticsearch.keystore
Processing triggers for ureadahead (0.100.0-21) ...
Processing triggers for systemd (237-3ubuntu10.42) ...
[root@ubuntu1804 ~]#systemctl daemon-reload
[root@ubuntu1804 ~]#systemctl enable --now elasticsearch.service
Synchronizing state of elasticsearch.service with SysV service script with
/lib/systemd/systemd-sysv-install.
Executing: /lib/systemd/systemd-sysv-install enable elasticsearch
Created symlink /etc/systemd/system/multi-user.target.wants/elasticsearch.service
→ /usr/lib/systemd/system/elasticsearch.service.
[root@ubuntu1804 ~]#curl 127.0.0.1:9200
{
"name" : "node2.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "hNlDtBjMTyerjIBt2dNjKg",
"version" : {
"number" : "7.14.0",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "dd5a0a2acaa2045ff9624f3729fc8a6f40835aa1",
"build_date" : "2021-07-29T20:49:32.864135063Z",
"build_snapshot" : false,
"lucene_version" : "8.9.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
```

CentOS 7 安装 Elasticsearch

```bash
[root@centos7 ~]#yum -y install elasticsearch-7.6.2-x86_64.rpm
```

Ubuntu18.04 安装 Elasticsearch

```bash
[root@ubuntu1804 ~]#dpkg -i elasticsearch-7.6.2-amd64.deb
```

### 编辑服务配置文件

参考文档：

<https://www.ibm.com/support/knowledgecenter/zh/SSFPJS_8.5.6/com.ibm.wbpm.main.doc/topics/rfps_esearch_configoptions.html>

<https://www.elastic.co/guide/en/elasticsearch/reference/index.html>

<https://www.elastic.co/guide/en/elasticsearch/reference/master/settings.html>

<https://www.elastic.co/guide/en/elasticsearch/reference/master/important-settings.html>

2.3.1.2.1 配置文件说明

```bash
[root@es-node1 ~]# grep "^[a-Z]"  /etc/elasticsearch/elasticsearch.yml
#ELK集群名称，单节点无需配置，同一个集群内每个节点的此项必须相同,新加集群的节点此项和其它节点相
同即可加入集群,而无需再验证
cluster.name: ELK-Cluster
#当前节点在集群内的节点名称，同一集群中每个节点要确保此名称唯一
node.name: es-node1
#ES 数据保存目录，包安装默认路径：/var/lib/elasticsearch/，生产建议修改
path.data: /data/es-data
#ES 日志保存目录，包安装默认路径：/var/log/elasticsearch/，生产建议修改
path.logs: /data/es-logs
#服务启动的时候立即分配(锁定)足够的内存，防止数据写入swap,提高启动速度,但是true可以会导致启动
失败，需要优化
bootstrap.memory_lock: true
#指定该节点用于集群的监听IP，默认监听在127.0.0.1:9300，集群模式必须修改此行，单机默认即可
network.host: 0.0.0.0
#指定HTTP的9200/TCP的监听地址，默认127.0.0.1
http.host: 0.0.0.0
#监听端口
http.port: 9200
#发现集群的node节点列表，可以添加部分或全部节点IP
#在新增节点到已有集群时,此处需指定至少一个已经在集群中的节点地址，给予可用性，一般添加所有节点地
址
discovery.seed_hosts: ["10.0.0.101","10.0.0.102","10.0.0.103"]
#集群初始化时指定希望哪些节点可以被选举为 master,只在初始化时使用,新加节点到已有集群时此项可不
配置
cluster.initial_master_nodes: ["10.0.0.101","10.0.0.102","10.0.0.103"]
#一个集群中的 N 个节点启动后,才允许进行数据恢复处理，默认是1,一般设为所有节点的一半以上,防止出
现脑裂现象
#当集群无法启动时,可以将之修改为1,或者将下面行注释掉,实现快速恢复启动
gateway.recover_after_nodes: 2
#设置是否可以通过正则表达式或者_all匹配索引库进行删除或者关闭索引库，默认true表示必须需要明确指
定索引库名称，不能使用正则表达式和_all，生产环境建议设置为 true，防止误删索引库。
action.destructive_requires_name: true
#如果不参与主节点选举设为false,默认值为true
#新版：8.X https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-
node.html
node.roles: [ master ]
node.roles: [ data, master, voting_only ]
#旧版7,X
node.master: false
#存储数据,默认值为true,此值为false则不存储数据而成为一个路由节点
#如果将原有的true改为false,需要先执行/usr/share/elasticsearch/bin/elasticsearch-node
repurpose 清理数据
node.data: true
#7.x以后版本下面指令已废弃，在2.x 5.x 6.x 版本中用于配置节点发现列表
discovery.zen.ping.unicast.hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
#8.X版后默认即开启Xpack功能，可以修改为false禁用
xpack.security.enabled: true
#开启跨域访问支持，默认为false
http.cors.enabled: true
# 跨域访问允许的域名地址，(允许所有域名)以上使用正则
http.cors.allow-origin: "*"
```

2.3.1.2.2 单机配置

范例: 8.X 单机使用默认的配置开启xpack.security功能

```bash
[root@ubuntu2204 ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/elasticstack/8.x/apt/pool/main/e/elasticsea
rch/elasticsearch-8.14.3-amd64.deb
[root@ubuntu2204 ~]#dpkg -i elasticsearch-8.14.3-amd64.deb
Selecting previously unselected package elasticsearch.
(Reading database ... 74275 files and directories currently installed.)
Preparing to unpack elasticsearch-8.14.3-amd64.deb ...
Creating elasticsearch group... OK
Creating elasticsearch user... OK
Unpacking elasticsearch (8.14.3) ...
Setting up elasticsearch (8.14.3) ...
--------------------------- Security autoconfiguration information -------------
-----------------
Authentication and authorization are enabled.
TLS for the transport and HTTP layers is enabled and configured.
The generated password for the elastic built-in superuser is :
XQ6=3KT6uatlFYk5bHi+
If this node should join an existing cluster, you can reconfigure this with
'/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token
<token-here>'
after creating an enrollment token on your existing cluster.
You can complete the following actions at any time:
Reset the password of the elastic built-in superuser with
'/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.
Generate an enrollment token for Kibana instances with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.
Generate an enrollment token for Elasticsearch nodes with
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.
---------------------------------------------------------------------------------
----------------
### NOT starting on installation, please execute the following statements to
configure elasticsearch service to start automatically using systemd
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
sudo systemctl start elasticsearch.service
```

```bash
#8.X默认开启xpack.security功能,配置文件默认不做修改
[root@ubuntu2204 ~]#grep -Ev "#|^$" /etc/elasticsearch/elasticsearch.yml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
xpack.security.enabled: true
xpack.security.enrollment.enabled: true
xpack.security.http.ssl:
enabled: true
keystore.path: certs/http.p12
xpack.security.transport.ssl:
enabled: true
verification_mode: certificate
keystore.path: certs/transport.p12
truststore.path: certs/transport.p12
cluster.initial_master_nodes: ["ubuntu2204"]
http.host: 0.0.0.0
#启动
[root@ubuntu2204 ~]#systemctl enable --now  elasticsearch.service
[root@ubuntu2204 ~]#ss -ntlp|grep java
LISTEN 0      4096                    *:9200            *:*    users:
(("java",pid=1910,fd=449))
LISTEN 0      4096   [::ffff:127.0.0.1]:9300            *:*    users:
(("java",pid=1910,fd=444))
LISTEN 0      4096                [::1]:9300         [::]:*    users:
(("java",pid=1910,fd=443))
#8.X默认开启xpack.security功能,无法直接通过http匿名访问
[root@ubuntu2204 ~]#curl  http://127.0.0.1:9200/
curl: (52) Empty reply from server
[root@ubuntu2204 ~]#curl   https://127.0.0.1:9200/
curl: (60) SSL certificate problem: self-signed certificate in certificate chain
More details here: https://curl.se/docs/sslcerts.html
curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
[root@ubuntu2204 ~]#apt -y install jq
#没有验证无法匿名访问
[root@ubuntu2204 ~]#curl -ks  https://127.0.0.1:9200/|jq
{
"error": {
"root_cause": [
{
"type": "security_exception",
"reason": "missing authentication credentials for REST request [/]",
"header": {
"WWW-Authenticate": [
"Basic realm=\"security\" charset=\"UTF-8\"",
"Bearer realm=\"security\"",
"ApiKey"
]
}
}
],
"type": "security_exception",
"reason": "missing authentication credentials for REST request [/]",
"header": {
"WWW-Authenticate": [
"Basic realm=\"security\" charset=\"UTF-8\"",
"Bearer realm=\"security\"",
"ApiKey"
]
}
},
"status": 401
}
#根据提示,用初始密码访问,执行下面
[root@ubuntu2204 ~]#PASSWORD="XQ6=3KT6uatlFYk5bHi+"; curl -u"elastic:$PASSWORD"
-k  https://127.0.0.1:9200
{
"name" : "ubuntu2204",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "cqu99gddRf2-p01evofhSA",
"version" : {
"number" : "8.14.3",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "d55f984299e0e88dee72ebd8255f7ff130859ad0",
"build_date" : "2024-07-07T22:04:49.882652950Z",
"build_snapshot" : false,
"lucene_version" : "9.10.0",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
```

```bash
#如果忘记密码,可以重置生成新密码
#方法1:生成随机密码
[root@ubuntu2204 ~]#/usr/share/elasticsearch/bin/elasticsearch-reset-password -u
elastic
This tool will reset the password of the [elastic] user to an autogenerated
value.
The password will be printed in the console.
Please confirm that you would like to continue [y/N]y
Password for the [elastic] user successfully reset.
New value: gdzk_Y*acHkKViOWUQO9
#方法2:生成指定密码
[root@ubuntu2204 ~]#/usr/share/elasticsearch/bin/elasticsearch-reset-password --
username elastic -i
This tool will reset the password of the [elastic] user.
You will be prompted to enter the password.
Please confirm that you would like to continue [y/N]y
Enter password for [elastic]:
Re-enter password for [elastic]:
Password for the [elastic] user successfully reset.
#用新密码访问
[root@ubuntu2204 ~]#PASSWORD="gdzk_Y*acHkKViOWUQO9"; curl -u"elastic:$PASSWORD"
-k  https://127.0.0.1:9200
{
"name" : "ubuntu2204",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "cqu99gddRf2-p01evofhSA",
"version" : {
"number" : "8.14.3",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "d55f984299e0e88dee72ebd8255f7ff130859ad0",
"build_date" : "2024-07-07T22:04:49.882652950Z",
"build_snapshot" : false,
"lucene_version" : "9.10.0",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
```

范例：8.X 单机配置关闭xpack.security功能

```bash
#8.X版,修改配置文件一行即可
[root@ubuntu2204 ~]#vim /etc/elasticsearch/elasticsearch.yml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
#network.host: 0.0.0.0         #保留注释此行
xpack.security.enabled: false  #只需要修改此行true为false即可,其它行默认即可
xpack.security.enrollment.enabled: true
xpack.security.http.ssl:
enabled: true
keystore.path: certs/http.p12
xpack.security.transport.ssl:
enabled: true
verification_mode: certificate
keystore.path: certs/transport.p12
truststore.path: certs/transport.p12
cluster.initial_master_nodes: ["ubuntu2204.bowen.org"]  #默认此行不做修改
http.host: 0.0.0.0
[root@ubuntu2204 ~]#systemctl enable --now elasticsearch.service
#查看9200和9300端口
[root@ubuntu2204 ~]#ss -ntlp |grep -E '9200|9300'
LISTEN 0      4096                    *:9200            *:*    users:
(("java",pid=1594,fd=417))
LISTEN 0      4096   [::ffff:127.0.0.1]:9300            *:*    users:
(("java",pid=1594,fd=412))
LISTEN 0      4096                [::1]:9300         [::]:*    users:
(("java",pid=1594,fd=411))
[root@ubuntu2204 ~]#curl  http://127.0.0.1:9200/
{
"name" : "ubuntu2204.bowen.org",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "HBd5Y7IyTle648VDvCXsjw",
"version" : {
"number" : "8.6.1",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "180c9830da956993e59e2cd70eb32b5e383ea42c",
"build_date" : "2023-01-24T21:35:11.506992272Z",
"build_snapshot" : false,
"lucene_version" : "9.4.2",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
[root@ubuntu2204 ~]#curl  http://127.0.0.1:9200/_cluster/health?pretty=true
{
"cluster_name" : "elasticsearch",
"status" : "green",
"timed_out" : false,
"number_of_nodes" : 1,
"number_of_data_nodes" : 1,
"active_primary_shards" : 1,
"active_shards" : 1,
"relocating_shards" : 0,
"initializing_shards" : 0,
"unassigned_shards" : 0,
"delayed_unassigned_shards" : 0,
"number_of_pending_tasks" : 0,
"number_of_in_flight_fetch" : 0,
"task_max_waiting_in_queue_millis" : 0,
"active_shards_percent_as_number" : 100.0
}
[root@ubuntu2204 ~]#curl 'http://127.0.0.1:9200/_cat/nodes?v'
ip        heap.percent ram.percent cpu load_1m load_5m load_15m node.role
master name
127.0.0.1           20          96   6    0.24    0.21     0.09 cdfhilmrstw *
ubuntu2204.bowen.org
```

范例: 7.X 单节点配置

```bash
#7.X版之前
[root@ubuntu2004 ~]#grep -v '#'  /etc/elasticsearch/elasticsearch.yml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
node.name: node-1
network.host: 0.0.0.0 #修改此行
discovery.seed_hosts: ["10.0.0.100"]
cluster.initial_master_nodes: ["node-1"]
```

2.3.1.2.3 集群配置

范例：8.X 以上版本集群配置

```bash
#默认配置文件需要以下六行
[root@ubuntu2204 ~]#vim /etc/elasticsearch/elasticsearch.yml
cluster.name: my-application #指定集群名称，同一个集群内的所有节点相同
node.name: node-1 #修改此行，每个节点不同
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 0.0.0.0       #集群模式必须修改此行，默认是127.0.0.1:9300,否则集群节点无法
通过9300端口通信，每个节点相同
discovery.seed_hosts: ["10.0.0.201", "10.0.0.202","10.0.0.203"] #修改此行，每个节点
相同
cluster.initial_master_nodes: ["10.0.0.201", "10.0.0.202","10.0.0.203"] #修改此
行，每个节点相同
xpack.security.enabled: false                                   #修改此行，每个节点
相同
xpack.security.enrollment.enabled: true
xpack.security.http.ssl:
enabled: true
keystore.path: certs/http.p12
xpack.security.transport.ssl:
enabled: true
verification_mode: certificate
keystore.path: certs/transport.p12
truststore.path: certs/transport.p12
# cluster.initial_master_nodes: ["ubuntu2204.bowen.org"]     #将此行注释
http.host: 0.0.0.0
[root@ubuntu2204 ~]#systemctl enable --now elasticsearch
#打开9200和9300端口
[root@ubuntu2204 ~]#ss -ntlp |grep -E '9200|9300'
LISTEN 0      4096               *:9200            *:*    users:
(("java",pid=1406,fd=426))
LISTEN 0      4096               *:9300            *:*    users:
(("java",pid=1406,fd=411))
[root@ubuntu2204 ~]#curl  http://127.0.0.1:9200/_cluster/health?pretty=true
{
"cluster_name" : "elasticsearch",
"status" : "green",
"timed_out" : false,
"number_of_nodes" : 3,
"number_of_data_nodes" : 3,
"active_primary_shards" : 1,
"active_shards" : 2,
"relocating_shards" : 0,
"initializing_shards" : 0,
"unassigned_shards" : 0,
"delayed_unassigned_shards" : 0,
"number_of_pending_tasks" : 0,
"number_of_in_flight_fetch" : 0,
"task_max_waiting_in_queue_millis" : 0,
"active_shards_percent_as_number" : 100.0
}
[root@ubuntu2204 ~]#curl 'http://127.0.0.1:9200/_cat/nodes?v'
ip         heap.percent ram.percent cpu load_1m load_5m load_15m node.role
master name
10.0.0.203           45          97   0    0.12    0.08     0.07 cdfhilmrstw -
node-3
10.0.0.201           57          96   1    0.00    0.06     0.08 cdfhilmrstw -
node-1
10.0.0.202           61          95   1    0.08    0.08     0.07 cdfhilmrstw *
node-2
```

范例: 7.X 集群配置

```bash
[root@es-node1 ~]#grep -Ev '^$|#' /etc/elasticsearch/elasticsearch.yml
cluster.name: es-cluster
node.name: es-node1
path.data: /data/es-data
path.logs: /data/es-logs
bootstrap.memory_lock: true
network.host: 0.0.0.0
discovery.seed_hosts: ["10.0.0.101","10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101","10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
action.destructive_requires_name: true
[root@es-node1 ~]#scp /etc/elasticsearch/elasticsearch.yml es-
node2:/etc/elasticsearch/
[root@es-node1 ~]#scp /etc/elasticsearch/elasticsearch.yml es-
node3:/etc/elasticsearch/
[root@es-node2 ~]#grep -v "#" /etc/elasticsearch/elasticsearch.yml
cluster.name: es-cluster
node.name: es-node2          #只需要修改此行，每个节点都不能相同
path.data: /data/es-data
path.logs: /data/es-logs
network.host: 0.0.0.0
http.port: 9200
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
[root@es-node3 ~]#grep -v "#" /etc/elasticsearch/elasticsearch.yml
cluster.name: es-cluster     #与es-node1相同
node.name: es-node3          #修改此行，与es-node2不能相同
path.data: /data/es-data
path.logs: /data/es-logs
network.host: 0.0.0.0
http.port: 9200
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
```

### 优化 ELK 资源配置

2.3.1.3.1 开启 bootstrap.memory_lock 优化

开启bootstrap.memory_lock: true 可以优化性能，但会导致无法启动的错误解决方法

注意：开启bootstrap.memory_lock: true 需要足够的内存，建议4G以上，否则内存不足，启动会很失败或很慢

官方文档:

<https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html#bootstrap-memory_lock>

<https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-system-settings.html#systemd>

![ELK 日志分析第 36 页插图](assets/img-98aaedc47115587b.png)

![ELK 日志分析第 36 页插图](assets/img-9e13ce67c66e91e4.png)

```bash
[root@node1 ~]#vim /etc/elasticsearch/elasticsearch.yml
#开启此功能导8.X致集群模式无法启动,但单机模式可以启动
bootstrap.memory_lock: true
[root@node1 ~]#systemctl restart elasticsearch.service
Job for elasticsearch.service failed because the control process exited with
error code.
See "systemctl status elasticsearch.service" and "journalctl -xe" for details.
```

```bash
[root@node1 ~]#tail /data/es-logs/es-cluster.log
[2021-08-15T22:21:13,600][INFO ][o.e.t.TransportService   ] [node-1]
publish_address {10.0.0.101:9300}, bound_addresses {[::]:9300}
[2021-08-15T22:21:13,911][INFO ][o.e.b.BootstrapChecks    ] [node-1] bound or
publishing to a non-loopback address, enforcing bootstrap checks
[2021-08-15T22:21:13,934][ERROR][o.e.b.Bootstrap          ] [node-1] node
validation exception
[1] bootstrap checks failed. You must address the points described in the
following [1] lines before starting Elasticsearch.
bootstrap check failure [1] of [1]: memory locking requested for elasticsearch
process but memory is not locked
[2021-08-15T22:21:13,941][INFO ][o.e.n.Node               ] [node-1] stopping
...
[2021-08-15T22:21:13,955][INFO ][o.e.n.Node               ] [node-1] stopped
[2021-08-15T22:21:13,955][INFO ][o.e.n.Node               ] [node-1] closing ...
[2021-08-15T22:21:13,970][INFO ][o.e.n.Node               ] [node-1] closed
[2021-08-15T22:21:13,971][INFO ][o.e.x.m.p.NativeController] [node-1] Native
controller process has stopped - no new native processes can be started
#8.X致集群模式需要修改如下配置
#方法1：直接修改elasticsearch.service
[root@node1 ~]#vim /lib/systemd/system/elasticsearch.service
[Service]
#加下面一行
LimitMEMLOCK=infinity
#方法2：新建文件
[root@node1 ~]#systemctl edit elasticsearch
### Anything between here and the comment below will become the new contents of
the file
#加下面两行，注意加在中间位置
[Service]
LimitMEMLOCK=infinity
### Lines below this comment will be discarded
[root@node1 ~]#cat /etc/systemd/system/elasticsearch.service.d/override.conf
[Service]
LimitMEMLOCK=infinity
```

```bash
[root@node1 ~]#systemctl daemon-reload
[root@node1 ~]#systemctl restart elasticsearch.service
[root@node1 ~]#systemctl is-active elasticsearch.service
active
#测试访问是否成功
[root@node1 ~]#curl http://node1.bowen.com:9200
[root@node1 ~]#curl http://node2.bowen.com:9200
[root@node1 ~]#curl http://node3.bowen.com:9200
```

2.3.1.3.2 内存优化

官方文档：

<https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html#heap-size-settings>

<https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#set-jvm-heap-size>

推荐使用宿主机物理内存的一半，ES的heap内存最大不超过30G,26G是比较安全的

官方文档:

```text
https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-
configuration.html#set-jvm-heap-size
https://www.elastic.co/guide/en/elasticsearch/reference/current/important-
settings.html#heap-size-settings
https://www.elastic.co/guide/en/elasticsearch/reference/master/advanced-
configuration.html#set-jvm-heap-size
The heap size should be based on the available RAM:
Set Xms and Xmx to no more than 50% of your total memory. Elasticsearch requires
memory for purposes other than the JVM heap. For example, Elasticsearch uses off-
heap buffers for efficient network communication and relies on the operating
system’s filesystem cache for efficient access to files. The JVM itself also
requires some memory. It’s normal for Elasticsearch to use more memory than the
limit configured with the Xmx setting.
When running in a container, such as Docker, total memory is defined as the
amount of memory visible to the container, not the total system memory on the
host.
Set Xms and Xmx to no more than the threshold for compressed ordinary object
pointers (oops). The exact threshold varies but 26GB is safe on most systems and
can be as large as 30GB on some systems. To verify you are under the threshold,
check the Elasticsearch log for an entry like this:
堆大小应基于可用 RAM：
将 Xms 和 Xmx 设置为不超过总内存的 50%。 Elasticsearch 需要内存用于 JVM 堆以外的用途。 例
如，Elasticsearch 使用堆外缓冲区来实现高效的网络通信，并依靠操作系统的文件系统缓存来高效地访问
文件。 JVM 本身也需要一些内存。 Elasticsearch 使用比 Xmx 设置配置的限制更多的内存是正常的。
在容器（例如 Docker）中运行时，总内存定义为容器可见的内存量，而不是主机上的总系统内存。
将 Xms 和 Xmx 设置为不超过压缩普通对象指针 (oops) 的阈值。 确切的阈值会有所不同，但在大多数系
统上 26GB 是安全的，在某些系统上可能高达 30GB。 要验证您是否低于阈值，请检查 Elasticsearch
日志中的条目，如下所示：
```

关于OOPS的说明

```text
Managed pointers in the Java heap point to objects which are aligned on 8-byte
address boundaries. Compressed oops represent managed pointers (in many but not
all places in the JVM software) as 32-bit object offsets from the 64-bit Java
heap base address.
Because they're object offsets rather than byte offsets, they can be used to
address up to four billion objects (not bytes), or a heap size of up to about 32
gigabytes.
To use them, they must be scaled by a factor of 8 and added to the Java heap base
address to find the object to which they refer. Object sizes using compressed
oops are comparable to those in ILP32 mode.
Java 堆中的托管指针指向在 8 字节地址边界上对齐的对象。 压缩 oop 将托管指针（在 JVM 软件中的许
多但不是所有地方）表示为相对于 64 位 Java 堆基地址的 32 位对象偏移量。
因为它们是对象偏移量而不是字节偏移量，所以它们可用于处理多达 40 亿个对象（不是字节），或高达约
32 GB 的堆大小。
要使用它们，必须将它们缩放 8 倍并添加到 Java 堆基地址以找到它们所引用的对象。 使用压缩 oop 的
对象大小与 ILP32 模式中的对象大小相当。
```

关于 Heap 内存大小

```text
虽然JVM可以处理大量的堆内存，但是将堆内存设置为过大的值可能导致以下问题：
堆内存分配的效率低。Java语言本身就是一种高级语言，这意味着需要更多的堆内存来存储对象。但是，当堆
内存过大时，分配对象所需的时间也会相应增加，这可能会导致应用程序出现性能问题。
操作系统内存管理的限制。操作系统必须以页为单位进行内存管理。如果Java堆内存过大，则需要更多的页来
管理堆内存。这可能会导致操作系统出现性能问题。
垃圾回收(Garbage Collection, GC)：JVM内存的一部分被用于存储对象，这些对象随着时间的推移可能
不再需要。这些不再需要的对象被视为“垃圾”，需要由垃圾收集器清除，以释放内存空间。然而，执行GC会暂
停所有的应用线程，这被称为 "Stop-the-World"（暂停世界）。这种暂停可能会影响应用的性能和响应时
间。一般来说，如果堆内存非常庞大，GC需要检查和清理的对象数量会变得非常庞大，这会导致GC操作的时间
变得非常漫长。
对象指针的大小：在某些JVM实现（例如Oracle的HotSpot），在堆（Heap）大小超过32GB之后，对象指针
的表示将从32位压缩oops（Ordinary Object Pointers普通对象指针）转变为64位非压缩指针，这导致
了内存使用的增加。如果内存设置接近或略超过32GB，实际上可能会因为此原因造成更多的内存消耗。因此，
通常在32GB以下时，我们会使用32位压缩指针，而超过这个阈值时，除非有明确的需要，否则通常会选择保持
在30GB左右以避免转为64位指针。
因此，建议将Java堆内存设置为合适的大小，以便在GC操作的同时与应用程序的性能之间进行平衡。通常情况
下，堆内存应该设置为操作系统的物理内存的一半或三分之一。虽然这个数字可能会因系统配置和工作负载而
有所变化，但是在32G的机器上，32G的堆空间已经超出了大部分Java应用程序的需求，因此更大的堆内存并
不是必要的。
当然，根据具体的应用场景和需求，以及你使用的具体的JVM版本和垃圾收集器类型，这个30GB的规则并非绝
对。比如ZGC和Shenandoah这类的低延迟垃圾回收器就可以处理大于30GB的堆内存，同时还能保持低停顿时
间。
```

内存优化建议:

为了保证性能，每个ES节点的JVM内存设置具体要根据 node 要存储的数据量来估算,建议符合下面约定

在内存和数据量有一个建议的比例：对于一般日志类文件，1G 内存能存储48G~96GB数据 JVM 堆内存最大不要超过30GB 单个分片控制在30-50GB，太大查询会比较慢，索引恢复和更新时间越长；分片太小，会导致索引碎片化越严重，性能也会下降

范例:

```text
#假设总数据量为1TB，3个node节点，1个副本；那么实际要存储的大小为2TB
每个节点需要存储的数据量为:2TB / 3 = 700GB，每个节点还需要预留20%的空间，所以每个node要存储
大约 700*100/80=875GB 的数据；每个节点按照内存与存储数据的比率计算：875GB/48GB=18，即需要
JVM内存为18GB,小于30GB
因为要尽量控制分片的大小为30GB；875GB/30GB=30个分片,即最多每个节点有30个分片
#思考：假设总数据量为2TB，3个node节点，1个副本呢？
```

范例：指定heap内存最小和最大内存限制

```bash
#建议将heap内存设置为物理内存的一半且最小和最大设置一样大,但最大不能超过30G
[root@es-node1 ~]# vim /etc/elasticsearch/jvm.options
-Xms30g
-Xmx30g
#每天产生1TB左右的数据量的建议服务器配置，还需要定期清理磁盘
16C 64G 6T硬盘 共3台服务器
```

范例： 修改service文件，做优化配置

```bash
[root@es-node1 ~]# vim /usr/lib/systemd/system/elasticsearch.service #修改内存限制
LimitNOFILE=1000000  #修改最大打开的文件数，默认值为65535
LimitNPROC=65535   #修改打开最大的进程数，默认值为4096
LimitMEMLOCK=infinity #无限制使用内存，以前旧版需要修改，否则无法启动服务，8.X当前版本无需修
改
```

内存锁定的配置参数：

<https://discuss.elastic.co/t/memory-lock-not-working/70576>

### 目录权限更改

在各个ES服务器创建数据和日志目录并修改目录权限为elasticsearch

```bash
#此步可选,可以不用创建下面目录es-data和es-logs，系统可以自动创建
[root@es-node1 ~]# mkdir -p /data/es-{data,logs}
[root@es-node1 ~]# ll /data/
total 0
drwxr-xr-x 2 root root 6 Apr 18 18:44 es-data
drwxr-xr-x 2 root root 6 Apr 18 18:44 es-logs
#必须分配权限，否则服务无法启动
[root@es-node1 ~]# chown  -R elasticsearch.elasticsearch /data/
[root@es-node1 ~]# ll /data/
total 0
drwxr-xr-x 2 elasticsearch elasticsearch 6 Apr 18 18:44 es-data
drwxr-xr-x 2 elasticsearch elasticsearch 6 Apr 18 18:44 es-logs
```

### 启动 Elasticsearch 服务并验证

```bash
[root@ubuntu-node1 ~]#grep -Ev '^$|#'
/usr/lib/systemd/system/elasticsearch.service
[Unit]
Description=Elasticsearch
Documentation=https://www.elastic.co
Wants=network-online.target
After=network-online.target
[Service]
Type=notify
RuntimeDirectory=elasticsearch
PrivateTmp=true
Environment=ES_HOME=/usr/share/elasticsearch
Environment=ES_PATH_CONF=/etc/elasticsearch
Environment=PID_DIR=/var/run/elasticsearch
Environment=ES_SD_NOTIFY=true
EnvironmentFile=-/etc/default/elasticsearch
WorkingDirectory=/usr/share/elasticsearch
User=elasticsearch
Group=elasticsearch
ExecStart=/usr/share/elasticsearch/bin/systemd-entrypoint -p
${PID_DIR}/elasticsearch.pid --quiet
StandardOutput=journal
StandardError=inherit
LimitNOFILE=65535
LimitNPROC=4096
LimitAS=infinity
LimitFSIZE=infinity
TimeoutStopSec=0
KillSignal=SIGTERM
KillMode=process
SendSIGKILL=no
SuccessExitStatus=143
TimeoutStartSec=75
[Install]
WantedBy=multi-user.target
[root@es-node1 ~]#systemctl enable --now  elasticsearch
#默认以elasticsearch 用户启动
[root@es-node1 ~]#id elasticsearch
用户id=113(elasticsearch) 组id=118(elasticsearch) 组=118(elasticsearch)
[root@es-node1 ~]#ps aux|grep elasticsearch
elastic+    1300  2.5  3.1 2605340 63508 ?       Ssl  12:22   0:02
/usr/share/elasticsearch/jdk/bin/java -Xms4m -Xmx64m -XX:+UseSerialGC -
Dcli.name=server -Dcli.script=/usr/share/elasticsearch/bin/elasticsearch -
Dcli.libs=lib/tools/server-cli -Des.path.home=/usr/share/elasticsearch -
Des.path.conf=/etc/elasticsearch -Des.distribution.type=deb -cp
/usr/share/elasticsearch/lib/*:/usr/share/elasticsearch/lib/cli-launcher/*
org.elasticsearch.launcher.CliToolLauncher -p
/var/run/elasticsearch/elasticsearch.pid --quiet
elastic+    1416 38.2 68.4 3776636 1360480 ?     Sl   12:22   0:33
/usr/share/elasticsearch/jdk/bin/java -Des.networkaddress.cache.ttl=60 -
Des.networkaddress.cache.negative.ttl=10 -Djava.security.manager=allow -
XX:+AlwaysPreTouch -Xss1m -Djava.awt.headless=true -Dfile.encoding=UTF-8 -
Djna.nosys=true -XX:-OmitStackTraceInFastThrow -Dio.netty.noUnsafe=true -
Dio.netty.noKeySetOptimization=true -Dio.netty.recycler.maxCapacityPerThread=0 -
Dlog4j.shutdownHookEnabled=false -Dlog4j2.disable.jmx=true -
Dlog4j2.formatMsgNoLookups=true -Djava.locale.providers=SPI,COMPAT --add-
opens=java.base/java.io=ALL-UNNAMED -XX:+UseG1GC -
Djava.io.tmpdir=/tmp/elasticsearch-10867261048884827118 -
XX:+HeapDumpOnOutOfMemoryError -XX:+ExitOnOutOfMemoryError -
XX:HeapDumpPath=/var/lib/elasticsearch -
XX:ErrorFile=/var/log/elasticsearch/hs_err_pid%p.log -
Xlog:gc*,gc+age=trace,safepoint:file=/var/log/elasticsearch/gc.log:utctime,pid,t
ags:filecount=32,filesize=64m -Xms970m -Xmx970m -
XX:MaxDirectMemorySize=508559360 -XX:G1HeapRegionSize=4m -
XX:InitiatingHeapOccupancyPercent=30 -XX:G1ReservePercent=15 -
Des.distribution.type=deb --module-path /usr/share/elasticsearch/lib --add-
modules=jdk.net -m
org.elasticsearch.server/org.elasticsearch.bootstrap.Elasticsearch
elastic+    1460  0.0  0.1 107900  3364 ?        Sl   12:22   0:00
/usr/share/elasticsearch/modules/x-pack-ml/platform/linux-x86_64/bin/controller
[root@es-node1 ~]#tail -f /data/es-logs/es-cluster.log
```

### 验证端口监听成功

```bash
#9200端口集群访问端口,9300集群同步端口
[root@es-node1 ~]#ss -ntlp|grep java
LISTEN   0         128                       *:9200                   *:*
users:(("java",pid=2372,fd=225))
LISTEN   0         128                       *:9300                   *:*
users:(("java",pid=2372,fd=211))
```

### 通过浏览器访问 Elasticsearch 服务端口

```json
#显示如下信息，表示服务启动，但不意味着集群是健康的
[root@es-node1 ~]#curl 127.0.0.1:9200
{
"name" : "es-node1",
"cluster_name" : "es-cluster",
"cluster_uuid" : "_na_",
"version" : {
"number" : "7.6.2",
"build_flavor" : "default",
"build_type" : "deb",
"build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
"build_date" : "2020-03-26T06:34:37.794943Z",
"build_snapshot" : false,
"lucene_version" : "8.4.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
#显示如下信息表示集群是健康的
[root@node1 ~]#curl http://127.0.0.1:9200/_cat/health?v
1682481515 03:58:35 my-application green 3 3 0 0 0 0 0 0 - 100.0%
```

### 二进制安装 Elasticsearch

官方文档

<https://www.elastic.co/guide/en/elasticsearch/reference/master/targz.html>

### 下载二进制文件

下载二进制文件

<https://www.elastic.co/cn/downloads/elasticsearch>

![ELK 日志分析第 43 页插图](assets/img-ce61375bdd8b52d8.png)

范例： 基于二进制包含JDK文件安装

```bash
[root@ubuntu1804 ~]#wget
https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.8.2-linux-
x86_64.tar.gz
[root@ubuntu1804 ~]#ls
elasticsearch-7.6.2-linux-x86_64.tar.gz
[root@ubuntu1804 ~]#tar xf elasticsearch-7.6.2-linux-x86_64.tar.gz  -C
/usr/local/
[root@ubuntu1804 ~]#ls /usr/local/
bin  elasticsearch-7.6.2  etc  games  include  lib  man  sbin  share  src
[root@ubuntu1804 ~]#ln -s /usr/local/elasticsearch-7.6.2/
/usr/local/elasticsearch
[root@ubuntu1804 ~]#ls /usr/local/elasticsearch
bin  config  jdk  lib  LICENSE.txt  logs  modules  NOTICE.txt  plugins
README.asciidoc
```

### 编辑服务配置文件

```bash
[root@es-node1 ~]#vim /usr/local/elasticsearch/config/elasticsearch.yml
[root@es-node1 ~]#grep -v "#" /usr/local/elasticsearch/config/elasticsearch.yml
cluster.name: es-clusterx
node.name: es-node1             #在其它节点改为唯一的标识,如es-node2,es-node3
path.data: /data/es-data
path.logs: /data/es-logs
network.host: 10.0.0.101
http.port: 9200
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
xpack.security.enabled: false #默认开启Xpack功能，可以设为false关闭此功能
#如果是集群,还需要复制配置文件到其它节点
[root@es-node1 ~]#scp /usr/local/elasticsearch/config/elasticsearch.yml  es-
node2:/usr/local/elasticsearch/config/
[root@es-node1 ~]#scp /usr/local/elasticsearch/config/elasticsearch.yml  es-
node3:/usr/local/elasticsearch/config/
#在其它节点也修改配置文件
[root@es-node2 ~]#vim /usr/local/elasticsearch/config/elasticsearch.yml
[root@es-node2 ~]#grep -v "#" /usr/local/elasticsearch/config/elasticsearch.yml
cluster.name: es-cluster
node.name: es-node2           #只修改此行即可
path.data: /data/es-data
path.logs: /data/es-logs
network.host: 10.0.0.102
http.port: 9200
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
[root@es-node3 ~]#vim /usr/local/elasticsearch/config/elasticsearch.yml
[root@es-node1 ~]#grep -v "#" /usr/local/elasticsearch/config/elasticsearch.yml
cluster.name: es-cluster
node.name: es-node3         #只修改此行即可
path.data: /data/es-data
path.logs: /data/es-logs
network.host: 10.0.0.103
http.port: 9200
discovery.seed_hosts: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
cluster.initial_master_nodes: ["10.0.0.101", "10.0.0.102","10.0.0.103"]
gateway.recover_after_nodes: 2
```

### 修改 ELK 内存配置

修改ELK内存配置，推荐使用宿主机物理内存的一半，最大不超过30G

官方文档：

<https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html#heap-size-settings>

范例：

```bash
#包安装
[root@es-node1 ~]#vim /etc/elasticsearch/jvm.options
#二进制
[root@es-node1 ~]#vim /usr/local/elasticsearch/config/jvm.options
22 -Xms2g
23 -Xmx2g
```

### 创建用户

从ES7.X以后版不允许以root启动服务，需要委创建专用的用户

在所有节点上创建用户

```bash
[root@es-node1 ~]#useradd -r elasticsearch
```

### 目录权限更改

在所有节点上创建数据和日志目录并修改目录权限为elasticsearch

```bash
#可以不用创建下面目录es-data和es-logs，系统可以自动创建
[root@es-node1 ~]# mkdir -p /data/es-{data,logs}
[root@es-node1 ~]# ll /data/
total 0
drwxr-xr-x 2 root root 6 Apr 18 18:44 es-data
drwxr-xr-x 2 root root 6 Apr 18 18:44 es-logs
#必须分配权限，否则服务无法启动
[root@es-node1 ~]# chown  -R elasticsearch:elasticsearch /data/es-{data,logs}
[root@es-node1 ~]# ll /data/
total 0
drwxr-xr-x 2 elasticsearch elasticsearch 6 Apr 18 18:44 es-data
drwxr-xr-x 2 elasticsearch elasticsearch 6 Apr 18 18:44 es-logs
#修改elasticsearch安装目录权限
[root@es-node1 ~]#chown -R elasticsearch.elasticsearch /usr/local/elasticsearch/
```

### 启动 Elasticsearch服务

在所有节点上配置并启动

```bash
[root@es-node1 ~]#echo 'PATH=/usr/local/elasticsearch/bin:$PATH' >
/etc/profile.d/elasticsearch.sh
[root@es-node1 ~]#. /etc/profile.d/elasticsearch.sh
[root@es-node1 ~]#tail -f /data/es-logs/es-cluster.log
#不能以root用户运行，切换用户
[root@es-node1 ~]#su - elasticsearch
No directory, logging in with HOME=/
$ elasticsearch
OpenJDK 64-Bit Server VM warning: Option UseConcMarkSweepGC was deprecated in
version 9.0 and will likely be removed in a future release.
[2021-01-21T13:26:40,017][INFO ][o.e.e.NodeEnvironment    ] [es-node1] using [1]
data paths, mounts [[/data (/dev/sda5)]], net usable_space [43.1gb], net
total_space [45.5gb], types [ext4]
[2021-01-21T13:26:40,031][INFO ][o.e.e.NodeEnvironment    ] [es-node1] heap size
[1007.3mb], compressed ordinary object pointers [true]
[2021-01-21T13:26:40,182][INFO ][o.e.n.Node               ] [es-node1] node name
[es-node1], node ID [m__LGOZgTCCK010g6_VcJQ], cluster name
```

### 验证端口监听成功

在所有节点上验证端口

```bash
[root@es-node1 ~]#ss -ntlp|grep java
LISTEN   0         128                       *:9200                   *:*
users:(("java",pid=2372,fd=225))
LISTEN   0         128                       *:9300                   *:*
users:(("java",pid=2372,fd=211))
```

### 通过浏览器访问 Elasticsearch 服务端口

在所有节点上验证访问9200/tcp端口

```bash
#8.X 默认开启XPACK功能，需要验证才能访问
[root@ubuntu2204 ~]#su - elasticsearch
su: warning: cannot change directory to /home/elasticsearch: No such file or
directory
$ elasticsearch
......
```

✅ Elasticsearch security features have been automatically configured! ✅ Authentication is enabled and cluster connections are encrypted.

ℹ  Password for the elastic user (reset with `bin/elasticsearch-reset-password

```text
-u elastic`):
r+pXBoArctXJuKbL3_H2
```

ℹ  HTTP CA certificate SHA-256 fingerprint:

```text
dba974705b42645c082522e7829de3f8c52af6af5ef014619fd6be7feac56820
```

ℹ  Configure Kibana to use this cluster:

```text
• Run Kibana and click the configuration link in the terminal when Kibana
starts.
• Copy the following enrollment token and paste it into Kibana in your browser
(valid for the next 30 minutes):
eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTAuMC4wLjEwMDo5MjAwIl0sImZnciI6ImRiYTk3NDcwNW
I0MjY0NWMwODI1MjJlNzgyOWRlM2Y4YzUyYWY2YWY1ZWYwMTQ2MTlmZDZiZTdmZWFjNTY4MjAiLCJrZX
kiOiJTMHREd1pJQkdUOG9JbHBNWlFQWDo3Q3pPVUlWUlNvdXQ0MnFLdzhZdVNBIn0=
```

ℹ  Configure other nodes to join this cluster:

```text
• On this node:
```

⁃ Create an enrollment token with `bin/elasticsearch-create-enrollment-token -s

```text
node`.
```

⁃ Uncomment the transport.host setting at the end of config/elasticsearch.yml. ⁃ Restart Elasticsearch.

```text
• On other nodes:
```

⁃ Start Elasticsearch with `bin/elasticsearch --enrollment-token <token>`,

```json
using the enrollment token that you generated.
[root@ubuntu2204 ~]#TOKEN=r+pXBoArctXJuKbL3_H2
[root@ubuntu2204 ~]#curl -u"elastic:$TOKEN" -k  https://127.0.0.1:9200
{
"name" : "ubuntu2204",
"cluster_name" : "elasticsearch",
"cluster_uuid" : "OeX5UtoOQfS9B3cdUshTqw",
"version" : {
"number" : "8.15.3",
"build_flavor" : "default",
"build_type" : "tar",
"build_hash" : "f97532e680b555c3a05e73a74c28afb666923018",
"build_date" : "2024-10-09T22:08:00.328917561Z",
"build_snapshot" : false,
"lucene_version" : "9.11.1",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
#7.X版本以前版本直接访问
[root@es-node1 ~]#curl 10.0.0.101:9200
{
"name" : "es-node1",
"cluster_name" : "es-cluster",
"cluster_uuid" : "vzp2MIpeQSGtCPzd29C2PA",
"version" : {
"number" : "7.6.2",
"build_flavor" : "default",
"build_type" : "tar",
"build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
"build_date" : "2020-03-26T06:34:37.794943Z",
"build_snapshot" : false,
"lucene_version" : "8.4.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
[root@es-node1 ~]#curl -sXGET http://10.0.0.101:9200/_cluster/health?pretty=true
{
"cluster_name" : "es-cluster",
"status" : "green",
"timed_out" : false,
"number_of_nodes" : 3,
"number_of_data_nodes" : 3,
"active_primary_shards" : 0,
"active_shards" : 0,
"relocating_shards" : 0,
"initializing_shards" : 0,
"unassigned_shards" : 0,
"delayed_unassigned_shards" : 0,
"number_of_pending_tasks" : 0,
"number_of_in_flight_fetch" : 0,
"task_max_waiting_in_queue_millis" : 0,
"active_shards_percent_as_number" : 100.0
}
```

### 创建 service 文件

```bash
[root@es-node1 ~]#cat /lib/systemd/system/elasticsearch.service
[Unit]
Description=Elasticsearch
Documentation=http://www.elastic.co
Wants=network-online.target
After=network-online.target
[Service]
RuntimeDirectory=elasticsearch
PrivateTmp=true
Environment=PID_DIR=/var/run/elasticsearch
WorkingDirectory=/usr/local/elasticsearch
User=elasticsearch
Group=elasticsearch
ExecStart=/usr/local/elasticsearch/bin/elasticsearch -p
${PID_DIR}/elasticsearch.pid --quiet
# StandardOutput is configured to redirect to journalctl since
# some error messages may be logged in standard output before
# elasticsearch logging system is initialized. Elasticsearch
# stores its logs in /var/log/elasticsearch and does not use
# journalctl by default. If you also want to enable journalctl
# logging, you can simply remove the "quiet" option from ExecStart.
# Specifies the maximum file descriptor number that can be opened by this
process
LimitNOFILE=65535
# Specifies the maximum number of processes
LimitNPROC=4096
# Specifies the maximum size of virtual memory
LimitAS=infinity
# Specifies the maximum file size
LimitFSIZE=infinity
# Disable timeout logic and wait until process is stopped
TimeoutStopSec=0
# SIGTERM signal is used to stop the Java process
KillSignal=SIGTERM
# Send the signal only to the JVM rather than its control group
KillMode=process
# Java process is never killed
SendSIGKILL=no
# When a JVM receives a SIGTERM signal it exits with code 143
SuccessExitStatus=143
[Install]
WantedBy=multi-user.target
# Built for packages-7.6.2 (packages)
[root@es-node1 ~]#systemctl daemon-reload
[root@es-node1 ~]#systemctl enable --now elasticsearch.service
```

### 基于 Docker 部署

官方文档

<https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html>

<https://www.elastic.co/guide/en/elasticsearch/reference/7.5/docker.html>

### 单节点部署

```json
[root@ubuntu1804 ~]#docker run --name es-single-node -d -p 9200:9200 -p
9300:9300 -e "discovery.type=single-node"
docker.elastic.co/elasticsearch/elasticsearch:7.6.2
[root@ubuntu1804 ~]#curl 10.0.0.100:9200
{
"name" : "2d46279f23e3",
"cluster_name" : "docker-cluster",
"cluster_uuid" : "NnmXvLMcS9-fxTsPe0bSMw",
"version" : {
"number" : "7.6.2",
"build_flavor" : "default",
"build_type" : "docker",
"build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
"build_date" : "2020-03-26T06:34:37.794943Z",
"build_snapshot" : false,
"lucene_version" : "8.4.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
```

### 多节点集群部署

2.3.3.2.1 部署前准备

注意：此方式需要3G以上内存，否则会出现OOM下面的信息

![ELK 日志分析第 50 页插图](assets/img-b7b0fc6164b373c5.png)

修改内核参数，默认无法启动，会出现下面错误提示

![ELK 日志分析第 50 页插图](assets/img-5a7deca2bfee796c.png)

```bash
[root@ubuntu1804 ~]#echo vm.max_map_count=262144 >>  /etc/sysctl.conf
[root@ubuntu1804 ~]#sysctl -p
```

2.3.3.2.2 创建docker-compose.yml文件

范例：

```yaml
#https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
version: "2.2"
services:
setup:
image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
volumes:
- certs:/usr/share/elasticsearch/config/certs
user: "0"
command: >
bash -c '
if [ x${ELASTIC_PASSWORD} == x ]; then
echo "Set the ELASTIC_PASSWORD environment variable in the .env file";
exit 1;
elif [ x${KIBANA_PASSWORD} == x ]; then
echo "Set the KIBANA_PASSWORD environment variable in the .env file";
exit 1;
fi;
if [ ! -f config/certs/ca.zip ]; then
echo "Creating CA";
bin/elasticsearch-certutil ca --silent --pem -out config/certs/ca.zip;
unzip config/certs/ca.zip -d config/certs;
fi;
if [ ! -f config/certs/certs.zip ]; then
echo "Creating certs";
echo -ne \
"instances:\n"\
"  - name: es01\n"\
"    dns:\n"\
"      - es01\n"\
"      - localhost\n"\
"    ip:\n"\
"      - 127.0.0.1\n"\
"  - name: es02\n"\
"    dns:\n"\
"      - es02\n"\
"      - localhost\n"\
"    ip:\n"\
"      - 127.0.0.1\n"\
"  - name: es03\n"\
"    dns:\n"\
"      - es03\n"\
"      - localhost\n"\
"    ip:\n"\
"      - 127.0.0.1\n"\
> config/certs/instances.yml;
bin/elasticsearch-certutil cert --silent --pem -out
config/certs/certs.zip --in config/certs/instances.yml --ca-cert
config/certs/ca/ca.crt --ca-key config/certs/ca/ca.key;
unzip config/certs/certs.zip -d config/certs;
fi;
echo "Setting file permissions"
chown -R root:root config/certs;
find . -type d -exec chmod 750 \{\} \;;
find . -type f -exec chmod 640 \{\} \;;
echo "Waiting for Elasticsearch availability";
until curl -s --cacert config/certs/ca/ca.crt https://es01:9200 | grep -
q "missing authentication credentials"; do sleep 30; done;
echo "Setting kibana_system password";
until curl -s -X POST --cacert config/certs/ca/ca.crt -u
"elastic:${ELASTIC_PASSWORD}" -H "Content-Type: application/json"
https://es01:9200/_security/user/kibana_system/_password -d "
{\"password\":\"${KIBANA_PASSWORD}\"}" | grep -q "^{}"; do sleep 10; done;
echo "All done!";
'
healthcheck:
test: ["CMD-SHELL", "[ -f config/certs/es01/es01.crt ]"]
interval: 1s
timeout: 5s
retries: 120
es01:
depends_on:
setup:
condition: service_healthy
image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
volumes:
- certs:/usr/share/elasticsearch/config/certs
- esdata01:/usr/share/elasticsearch/data
ports:
- ${ES_PORT}:9200
environment:
- node.name=es01
- cluster.name=${CLUSTER_NAME}
- cluster.initial_master_nodes=es01,es02,es03
- discovery.seed_hosts=es02,es03
- ELASTIC_PASSWORD=${ELASTIC_PASSWORD}
- bootstrap.memory_lock=true
- xpack.security.enabled=true
- xpack.security.http.ssl.enabled=true
- xpack.security.http.ssl.key=certs/es01/es01.key
- xpack.security.http.ssl.certificate=certs/es01/es01.crt
- xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.enabled=true
- xpack.security.transport.ssl.key=certs/es01/es01.key
- xpack.security.transport.ssl.certificate=certs/es01/es01.crt
- xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.verification_mode=certificate
- xpack.license.self_generated.type=${LICENSE}
mem_limit: ${MEM_LIMIT}
ulimits:
memlock:
soft: -1
hard: -1
healthcheck:
test:
[
"CMD-SHELL",
"curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep
-q 'missing authentication credentials'",
]
interval: 10s
timeout: 10s
retries: 120
es02:
depends_on:
- es01
image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
volumes:
- certs:/usr/share/elasticsearch/config/certs
- esdata02:/usr/share/elasticsearch/data
environment:
- node.name=es02
- cluster.name=${CLUSTER_NAME}
- cluster.initial_master_nodes=es01,es02,es03
- discovery.seed_hosts=es01,es03
- bootstrap.memory_lock=true
- xpack.security.enabled=true
- xpack.security.http.ssl.enabled=true
- xpack.security.http.ssl.key=certs/es02/es02.key
- xpack.security.http.ssl.certificate=certs/es02/es02.crt
- xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.enabled=true
- xpack.security.transport.ssl.key=certs/es02/es02.key
- xpack.security.transport.ssl.certificate=certs/es02/es02.crt
- xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.verification_mode=certificate
- xpack.license.self_generated.type=${LICENSE}
mem_limit: ${MEM_LIMIT}
ulimits:
memlock:
soft: -1
hard: -1
healthcheck:
test:
[
"CMD-SHELL",
"curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep
-q 'missing authentication credentials'",
]
interval: 10s
timeout: 10s
retries: 120
es03:
depends_on:
- es02
image: docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}
volumes:
- certs:/usr/share/elasticsearch/config/certs
- esdata03:/usr/share/elasticsearch/data
environment:
- node.name=es03
- cluster.name=${CLUSTER_NAME}
- cluster.initial_master_nodes=es01,es02,es03
- discovery.seed_hosts=es01,es02
- bootstrap.memory_lock=true
- xpack.security.enabled=true
- xpack.security.http.ssl.enabled=true
- xpack.security.http.ssl.key=certs/es03/es03.key
- xpack.security.http.ssl.certificate=certs/es03/es03.crt
- xpack.security.http.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.enabled=true
- xpack.security.transport.ssl.key=certs/es03/es03.key
- xpack.security.transport.ssl.certificate=certs/es03/es03.crt
- xpack.security.transport.ssl.certificate_authorities=certs/ca/ca.crt
- xpack.security.transport.ssl.verification_mode=certificate
- xpack.license.self_generated.type=${LICENSE}
mem_limit: ${MEM_LIMIT}
ulimits:
memlock:
soft: -1
hard: -1
healthcheck:
test:
[
"CMD-SHELL",
"curl -s --cacert config/certs/ca/ca.crt https://localhost:9200 | grep
-q 'missing authentication credentials'",
]
interval: 10s
timeout: 10s
retries: 120
kibana:
depends_on:
es01:
condition: service_healthy
es02:
condition: service_healthy
es03:
condition: service_healthy
image: docker.elastic.co/kibana/kibana:${STACK_VERSION}
volumes:
- certs:/usr/share/kibana/config/certs
- kibanadata:/usr/share/kibana/data
ports:
- ${KIBANA_PORT}:5601
environment:
- SERVERNAME=kibana
- ELASTICSEARCH_HOSTS=https://es01:9200
- ELASTICSEARCH_USERNAME=kibana_system
- ELASTICSEARCH_PASSWORD=${KIBANA_PASSWORD}
- ELASTICSEARCH_SSL_CERTIFICATEAUTHORITIES=config/certs/ca/ca.crt
mem_limit: ${MEM_LIMIT}
healthcheck:
test:
[
"CMD-SHELL",
"curl -s -I http://localhost:5601 | grep -q 'HTTP/1.1 302 Found'",
]
interval: 10s
timeout: 10s
retries: 120
volumes:
certs:
driver: local
esdata01:
driver: local
esdata02:
driver: local
esdata03:
driver: local
kibanadata:
driver: local
```

范例

```yaml
[root@ubuntu1804 ~]#cat docker-compose.yml
version: '2.2'
services:
es01:
image: docker.elastic.co/elasticsearch/elasticsearch:7.5.2
container_name: es01
environment:
- node.name=es01
- cluster.name=es-docker-cluster
- discovery.seed_hosts=es02,es03
- cluster.initial_master_nodes=es01,es02,es03
- bootstrap.memory_lock=true
- "ES_JAVA_OPTS=-Xms512m -Xmx512m"
ulimits:
memlock:
soft: -1
hard: -1
volumes:
- data01:/usr/share/elasticsearch/data
ports:
- 9200:9200
networks:
- elastic
es02:
image: docker.elastic.co/elasticsearch/elasticsearch:7.5.2
container_name: es02
environment:
- node.name=es02
- cluster.name=es-docker-cluster
- discovery.seed_hosts=es01,es03
- cluster.initial_master_nodes=es01,es02,es03
- bootstrap.memory_lock=true
- "ES_JAVA_OPTS=-Xms512m -Xmx512m"
ulimits:
memlock:
soft: -1
hard: -1
volumes:
- data02:/usr/share/elasticsearch/data
networks:
- elastic
es03:
image: docker.elastic.co/elasticsearch/elasticsearch:7.5.2
container_name: es03
environment:
- node.name=es03
- cluster.name=es-docker-cluster
- discovery.seed_hosts=es01,es02
- cluster.initial_master_nodes=es01,es02,es03
- bootstrap.memory_lock=true
- "ES_JAVA_OPTS=-Xms512m -Xmx512m"
ulimits:
memlock:
soft: -1
hard: -1
volumes:
- data03:/usr/share/elasticsearch/data
networks:
- elastic
volumes:
data01:
driver: local
data02:
driver: local
data03:
driver: local
networks:
elastic:
driver: bridge
```

2.3.3.2.3 启动集群

```bash
[root@ubuntu1804 ~]#docker-compose up -d
```

2.3.3.2.4 验证

```json
[root@ubuntu1804 ~]#curl -sXGET http://10.0.0.100:9200
{
"name" : "es01",
"cluster_name" : "es-docker-cluster",
"cluster_uuid" : "Q0d0L9rCSuyuJyTEo8EE3w",
"version" : {
"number" : "7.6.2",
"build_flavor" : "default",
"build_type" : "docker",
"build_hash" : "ef48eb35cf30adf4db14086e8aabd07ef6fb113f",
"build_date" : "2020-03-26T06:34:37.794943Z",
"build_snapshot" : false,
"lucene_version" : "8.4.0",
"minimum_wire_compatibility_version" : "6.8.0",
"minimum_index_compatibility_version" : "6.0.0-beta1"
},
"tagline" : "You Know, for Search"
}
[root@ubuntu1804 ~]#curl -sXGET http://10.0.0.100:9200/_cluster/health?
pretty=true
{
"cluster_name" : "es-docker-cluster",
"status" : "green",
"timed_out" : false,
"number_of_nodes" : 3,
"number_of_data_nodes" : 3,
"active_primary_shards" : 0,
"active_shards" : 0,
"relocating_shards" : 0,
"initializing_shards" : 0,
"unassigned_shards" : 0,
"delayed_unassigned_shards" : 0,
"number_of_pending_tasks" : 0,
"number_of_in_flight_fetch" : 0,
"task_max_waiting_in_queue_millis" : 0,
"active_shards_percent_as_number" : 100.0
}
```

![ELK 日志分析第 57 页插图](assets/img-28c6832a56bbb1b2.png)

### 基于 Kubernetes 部署

### 基于 Operator 实现 ECK（ Elastic Cloud on Kubernetes ) 说明

官方安装说明

<https://www.elastic.co/guide/en/cloud-on-k8s/current/index.html>

<https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html>

<https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html>

<https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-elasticsearch.html>

```text
#1)Install custom resource definitions:
kubectl create -f https://download.elastic.co/downloads/eck/2.12.1/crds.yaml
The following Elastic resources have been created:
customresourcedefinition.apiextensions.k8s.io/agents.agent.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/apmservers.apm.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/beats.beat.k8s.elastic.co created
customresourcedefinition.apiextensions.k8s.io/elasticmapsservers.maps.k8s.elasti
c.co created
customresourcedefinition.apiextensions.k8s.io/elasticsearches.elasticsearch.k8s.
elastic.co created
customresourcedefinition.apiextensions.k8s.io/enterprisesearches.enterprisesearc
h.k8s.elastic.co created
customresourcedefinition.apiextensions.k8s.io/kibanas.kibana.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/logstashes.logstash.k8s.elastic.co
created
#2)Install the operator with its RBAC rules:
kubectl apply -f https://download.elastic.co/downloads/eck/2.12.1/operator.yaml
The ECK operator runs by default in the elastic-system namespace. It is
recommended that you choose a dedicated namespace for your workloads, rather
than using the elastic-system or the default namespace.
#Monitor the operator logs:
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```

```yaml
#3)Apply a simple Elasticsearch cluster specification, with one Elasticsearch
node:
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
name: quickstart
spec:
version: 8.13.2
nodeSets:
- name: default
count: 1
config:
node.store.allow_mmap: false
EOF
```

```text
#4)Monitor cluster health and creation progressedit
#Get an overview of the current Elasticsearch clusters in the Kubernetes cluster,
including health, version and number of nodes:
kubectl get elasticsearch
NAME          HEALTH    NODES     VERSION   PHASE         AGE
quickstart    green     1         8.13.2     Ready         1m
#When you create the cluster, there is no HEALTH status and the PHASE is empty.
After a while, the PHASE turns into Ready, and HEALTH becomes green. The HEALTH
status comes from Elasticsearch’s cluster health API.
#One Pod is in the process of being started:
kubectl get pods --selector='elasticsearch.k8s.elastic.co/cluster-
name=quickstart'
NAME                      READY   STATUS    RESTARTS   AGE
quickstart-es-default-0   1/1     Running   0          79s
#Access the logs for that Pod:
kubectl logs -f quickstart-es-default-0
#Request Elasticsearch accessedit
#A ClusterIP Service is automatically created for your cluster:
kubectl get service quickstart-es-http
NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
quickstart-es-http   ClusterIP   10.15.251.145   <none>        9200/TCP   34m
#Get the credentials.
#A default user named elastic is automatically created with the password stored
in a Kubernetes secret:
PASSWORD=$(kubectl get secret quickstart-es-elastic-user -o go-
template='{{.data.elastic | base64decode}}')
Request the Elasticsearch endpoint.
#From inside the Kubernetes cluster:
curl -u "elastic:$PASSWORD" -k "https://quickstart-es-http:9200"
#From your local workstation, use the following command in a separate terminal:
kubectl port-forward service/quickstart-es-http 9200
#Then request localhost:
curl -u "elastic:$PASSWORD" -k "https://localhost:9200"
```

### 案例：基于 Operator 实现 ECK（ Elastic Cloud on Kubernetes )

注意：Worker 节点内存需要4G以上

2.3.4.2.1 安装 Operator

```bash
#安装Operator
[root@master1 ~]#kubectl create -f
https://download.elastic.co/downloads/eck/2.12.1/crds.yaml
customresourcedefinition.apiextensions.k8s.io/agents.agent.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/apmservers.apm.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/beats.beat.k8s.elastic.co created
customresourcedefinition.apiextensions.k8s.io/elasticmapsservers.maps.k8s.elasti
c.co created
customresourcedefinition.apiextensions.k8s.io/elasticsearchautoscalers.autoscali
ng.k8s.elastic.co created
customresourcedefinition.apiextensions.k8s.io/elasticsearches.elasticsearch.k8s.
elastic.co created
customresourcedefinition.apiextensions.k8s.io/enterprisesearches.enterprisesearc
h.k8s.elastic.co created
customresourcedefinition.apiextensions.k8s.io/kibanas.kibana.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/logstashes.logstash.k8s.elastic.co
created
customresourcedefinition.apiextensions.k8s.io/stackconfigpolicies.stackconfigpol
icy.k8s.elastic.co created
#自动创建相关CRD
[root@master1 ~]#kubectl get crd --sort-by='{.metadata.creationTimestamp}'|tail
enterprisesearches.enterprisesearch.k8s.elastic.co     2024-04-21T03:41:22Z
elasticmapsservers.maps.k8s.elastic.co                 2024-04-21T03:41:22Z
elasticsearchautoscalers.autoscaling.k8s.elastic.co    2024-04-21T03:41:22Z
stackconfigpolicies.stackconfigpolicy.k8s.elastic.co   2024-04-21T03:41:22Z
logstashes.logstash.k8s.elastic.co                     2024-04-21T03:41:22Z
agents.agent.k8s.elastic.co                            2024-04-21T03:41:22Z
kibanas.kibana.k8s.elastic.co                          2024-04-21T03:41:22Z
elasticsearches.elasticsearch.k8s.elastic.co           2024-04-21T03:41:22Z
beats.beat.k8s.elastic.co                              2024-04-21T03:41:22Z
apmservers.apm.k8s.elastic.co                          2024-04-21T03:41:22Z
```

```bash
#安装operator相关RBAC 规则
[root@master1 ~]#kubectl apply -f
https://download.elastic.co/downloads/eck/2.12.1/operator.yaml
namespace/elastic-system created
serviceaccount/elastic-operator created
secret/elastic-webhook-server-cert created
configmap/elastic-operator created
clusterrole.rbac.authorization.k8s.io/elastic-operator created
clusterrole.rbac.authorization.k8s.io/elastic-operator-view created
clusterrole.rbac.authorization.k8s.io/elastic-operator-edit created
clusterrolebinding.rbac.authorization.k8s.io/elastic-operator created
service/elastic-webhook-server created
statefulset.apps/elastic-operator created
validatingwebhookconfiguration.admissionregistration.k8s.io/elastic-
webhook.k8s.elastic.co created
#在elastic-system 名称空间查看相关资源
[root@master1 ~]#kubectl get all -n elastic-system
NAME                     READY   STATUS    RESTARTS   AGE
pod/elastic-operator-0   1/1     Running   0          23s
NAME                             TYPE        CLUSTER-IP       EXTERNAL-IP
PORT(S)   AGE
service/elastic-webhook-server   ClusterIP   10.100.174.107   <none>
443/TCP   23s
NAME                                READY   AGE
statefulset.apps/elastic-operator   1/1     23s
```

2.3.4.2.2 部署 Elasticsearch

```yaml
#准备业务的名称空间
[root@master1 ~]#kubectl create ns demo
#准备elasticsearch-cluster清单文件
[root@master1 ~]#cat operator-elasticsearch-cluster.yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
name: my-es-cluster
#namespace: elastic-system
namespace: demo
spec:
#version: 8.13.2
version: 8.14.0
nodeSets:
- name: default
count: 3                  #3个节点的集群
config:
node.store.allow_mmap: false
volumeClaimTemplates:
- metadata:
name: elasticsearch-data
spec:
accessModes: ["ReadWriteOnce"]
resources:
requests:
storage: 2Gi
storageClassName: sc-nfs     #需要提前准备sc-nfs的storageClass
#注意：节点内存需要4G以上
[root@master1 ~]#kubectl apply -f operator-elasticsearch-cluster.yaml
#查看结果
[root@master1 ~]#kubectl get elasticsearch -n demo
NAME            HEALTH   NODES   VERSION   PHASE   AGE
my-es-cluster   green    3       8.13.2    Ready   51m
```

```bash
#查看结果
[root@master1 ~]#kubectl get all -n demo
NAME                             READY   STATUS    RESTARTS   AGE
pod/my-es-cluster-es-default-0   1/1     Running   0          31s
pod/my-es-cluster-es-default-1   1/1     Running   0          31s
pod/my-es-cluster-es-default-2   1/1     Running   0          31s
NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP
PORT(S)    AGE
service/my-es-cluster-es-default         ClusterIP   None             <none>
9200/TCP   31s
service/my-es-cluster-es-http            ClusterIP   10.99.139.6      <none>
9200/TCP   42s
service/my-es-cluster-es-internal-http   ClusterIP   10.105.185.183   <none>
9200/TCP   42s
service/my-es-cluster-es-transport       ClusterIP   None             <none>
9300/TCP   42s
NAME                                        READY   AGE
statefulset.apps/my-es-cluster-es-default   3/3     31s
[root@master1 ~]#kubectl get secret -n demo
NAME                                          TYPE     DATA   AGE
my-es-cluster-es-default-es-config            Opaque   1      20m
my-es-cluster-es-default-es-transport-certs   Opaque   7      20m
my-es-cluster-es-elastic-user                 Opaque   1      20m
my-es-cluster-es-file-settings                Opaque   1      20m
my-es-cluster-es-http-ca-internal             Opaque   2      20m
my-es-cluster-es-http-certs-internal          Opaque   3      20m
my-es-cluster-es-http-certs-public            Opaque   2      20m
my-es-cluster-es-internal-users               Opaque   4      20m
my-es-cluster-es-remote-ca                    Opaque   1      20m
my-es-cluster-es-transport-ca-internal        Opaque   2      20m
my-es-cluster-es-transport-certs-public       Opaque   1      20m
my-es-cluster-es-xpack-file-realm             Opaque   4      20m
[root@master1 ~]#ls /data/sc-nfs/
demo-elasticsearch-data-my-es-cluster-es-default-0-pvc-2c75f0cd-4f73-42dc-9f00-
80862d43128e
demo-elasticsearch-data-my-es-cluster-es-default-1-pvc-de45a3e6-820f-4e27-b596-
c50eb57e0563
demo-elasticsearch-data-my-es-cluster-es-default-2-pvc-8704ca2c-f0e4-4c1a-90c0-
47c3a9e5f809
#取出ES的访问密码
[root@master1 ~]#PASSWORD=$(kubectl get secret my-es-cluster-es-elastic-user -n
demo -o go-template='{{.data.elastic | base64decode}}')
#或者
[root@master1 ~]#PASSWORD=$(kubectl get secret my-es-cluster-es-elastic-user -n
demo -o jsonpath={.data.elastic} -n demo|base64 -d)
[root@master1 ~]#echo $PASSWORD
r969NUq7Xq3p445XZ46wKqoi
#开启一个新的Pod测试访问ES Cluster
[root@master1 ~]#kubectl run --env="PASSWORD=$PASSWORD" client-$RANDOM --image
registry.cn-beijing.aliyuncs.com/bowenxiaochun/admin-box:v0.1 -it --rm --
restart=Never --command -- /bin/bash
If you don't see a command prompt, try pressing enter.
root@client-6625 /# curl -u "elastic:$PASSWORD" -k https://my-es-cluster-es-
http.demo:9200
{
"name" : "my-es-cluster-es-default-0",
"cluster_name" : "my-es-cluster",
"cluster_uuid" : "Ljm9XSU0SmuvZjVNT8sYFg",
"version" : {
"number" : "8.13.2",
"build_flavor" : "default",
"build_type" : "docker",
"build_hash" : "16cc90cd2d08a3147ce02b07e50894bc060a4cbf",
"build_date" : "2024-04-05T14:45:26.420424304Z",
"build_snapshot" : false,
"lucene_version" : "9.10.0",
"minimum_wire_compatibility_version" : "7.17.0",
"minimum_index_compatibility_version" : "7.0.0"
},
"tagline" : "You Know, for Search"
}
root@client-6625 /#curl -u "elastic:$PASSWORD" -k https://my-es-cluster-es-
http.demo:9200/_cat/health
1713678472 05:47:52 my-es-cluster green 3 3 0 0 0 0 0 0 - 100.0%
root@client-6625 /#curl -u "elastic:$PASSWORD" -k https://my-es-cluster-es-
http.demo:9200/_cat/nodes
10.244.2.76 61 73 4 0.36 0.43 0.45 cdfhilmrstw - my-es-cluster-es-default-2
10.244.3.65 53 71 4 0.81 0.74 0.52 cdfhilmrstw - my-es-cluster-es-default-0
10.244.1.84 39 71 4 0.19 0.19 0.26 cdfhilmrstw * my-es-cluster-es-default-1
#当前没有索引
root@client-6625 /#curl -u "elastic:$PASSWORD" -k https://my-es-cluster-es-
http.demo:9200/_cat/indices
```

2.3.4.2.3 部署 Kibana

```yaml
#部署Kibana
[root@master1 ~]#cat operator-elasticsearch-cluster-kibana.yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
name: kibana
#namespace: elastic-system
namespace: demo
spec:
#version: 8.11.3
#version: 8.13.2
version: 8.14.0
count: 1
elasticsearchRef:
name: "my-es-cluster"
http:
tls:
selfSignedCertificate:
disabled: true
service:
spec:
type: LoadBalancer #
#type: NodePort
---
#apiVersion: networking.k8s.io/v1
#kind: Ingress
#metadata:
#  name: kibana
#  namespace: elastic-system
#spec:
#  ingressClassName: nginx
#  rules:
#  - host: kibana.bowen.org
#    http:
#      paths:
#      - backend:
#          service:
#            name: kibana-kb-http
#            port:
#              number: 5601
#        path: /
#        pathType: Prefix
#  # tls:
#  # - hosts:
#  #   - host-name
#  #   secretName: tls-secret-name
[root@master1 ~]#kubectl apply -f operator-elasticsearch-cluster-kibana.yaml
kibana.kibana.k8s.elastic.co/kibana created
#查看状态
[root@master1 ~]#kubectl get kibana  -n demo
NAME     HEALTH   NODES   VERSION   AGE
kibana   green    1       8.11.3    26m
#查看SVC
[root@master1 ~]#kubectl get svc  -n demo
NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP
PORT(S)          AGE
service/kibana-kb-http                   LoadBalancer  10.108.134.123
10.0.0.10   5601:30635/TCP   2m8s
```

2.3.4.2.4 部署 Filebeat

```yaml
#部署Filebeat
[root@master1 ~]#cat operator-elasticsearch-cluster-filebeat.yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
name: filebeat
#namespace: elastic-system
namespace: demo                #指定名称空间
spec:
type: filebeat
#version: 8.11.3
#version: 8.13.2
version: 8.14.0
elasticsearchRef:
name: "my-es-cluster"       #指定ES的名称
kibanaRef:
name: "kibana"              #指定kibana的名称
config:
filebeat:
autodiscover:
providers:
- type: kubernetes
node: ${NODE_NAME}
hints:
enabled: true
default_config:
type: container
paths:
- /var/log/containers/*${data.kubernetes.container.id}.log
processors:
- add_kubernetes_metadata:
host: ${NODE_NAME}
matchers:
- logs_path:
logs_path: "/var/log/containers/"
- drop_event.when:
or:
- equals:
kubernetes.namespace: "kube-system"
- equals:
kubernetes.namespace: "logging"
- equals:
kubernetes.namespace: "ingress-nginx"
- equals:
kubernetes.namespace: "kube-node-lease"
- equals:
kubernetes.namespace: "elastic-system"
daemonSet:
podTemplate:
spec:
serviceAccountName: filebeat
automountServiceAccountToken: true
terminationGracePeriodSeconds: 30
dnsPolicy: ClusterFirstWithHostNet
hostNetwork: true # Allows to provide richer host metadata
containers:
- name: filebeat
securityContext:
runAsUser: 0
# If using Red Hat OpenShift uncomment this:
#privileged: true
volumeMounts:
- name: varlogcontainers
mountPath: /var/log/containers
- name: varlogpods
mountPath: /var/log/pods
- name: varlibdockercontainers
mountPath: /var/lib/docker/containers
env:
- name: NODE_NAME
valueFrom:
fieldRef:
fieldPath: spec.nodeName
volumes:
- name: varlogcontainers
hostPath:
path: /var/log/containers
- name: varlogpods
hostPath:
path: /var/log/pods
- name: varlibdockercontainers
hostPath:
path: /var/lib/docker/containers
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
name: filebeat
rules:
- apiGroups: [""] # "" indicates the core API group
resources:
- namespaces
- pods
- nodes
verbs:
- get
- watch
- list
---
apiVersion: v1
kind: ServiceAccount
metadata:
name: filebeat
#namespace: elastic-system
namespace: demo
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
name: filebeat
subjects:
- kind: ServiceAccount
name: filebeat
#namespace: elastic-system
namespace: demo
roleRef:
kind: ClusterRole
name: filebeat
apiGroup: rbac.authorization.k8s.io
[root@master1 ~]#kubectl apply -f operator-elasticsearch-cluster-filebeat.yaml
[root@master1 ~]#kubectl get beats -n demo
NAME       HEALTH   AVAILABLE   EXPECTED   TYPE       VERSION   AGE
filebeat   green    3           3          filebeat   8.11.3    28m
```

```bash
[root@master1 ~]#kubectl get all -n demo
NAME                               READY   STATUS    RESTARTS      AGE
pod/filebeat-beat-filebeat-42qfw   1/1     Running   3 (50s ago)   2m6s
pod/filebeat-beat-filebeat-5tmzz   1/1     Running   3 (76s ago)   2m6s
pod/filebeat-beat-filebeat-bqzk8   1/1     Running   4 (50s ago)   2m6s
pod/kibana-kb-6bcdf8d8d8-b2jp2     1/1     Running   0             2m6s
pod/my-es-cluster-es-default-0     1/1     Running   0             58m
pod/my-es-cluster-es-default-1     1/1     Running   0             58m
pod/my-es-cluster-es-default-2     1/1     Running   0             58m
NAME                                     TYPE        CLUSTER-IP       EXTERNAL-IP
PORT(S)          AGE
service/kibana-kb-http                   LoadBalancer  10.108.134.123
10.0.0.10   5601:30635/TCP   2m8s
service/my-es-cluster-es-default         ClusterIP   None             <none>
9200/TCP         58m
service/my-es-cluster-es-http            ClusterIP   10.99.139.6      <none>
9200/TCP         58m
service/my-es-cluster-es-internal-http   ClusterIP   10.105.185.183   <none>
9200/TCP         58m
service/my-es-cluster-es-transport       ClusterIP   None             <none>
9300/TCP         58m
NAME                                    DESIRED   CURRENT   READY   UP-TO-DATE
AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/filebeat-beat-filebeat   3         3         3       3
3           <none>          2m7s
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kibana-kb   1/1     1            1           2m7s
NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/kibana-kb-6bcdf8d8d8   1         1         1       2m7s
NAME                                        READY   AGE
statefulset.apps/my-es-cluster-es-default   3/3     58m
```

2.3.4.2.5 测试访问 Kibana

```bash
#使用ElasticSearch部署时生成的用户elastic及其密码即可登录service的NodePort
#用前面的命令取出密码
[root@master1 ~]#kubectl get secret my-es-cluster-es-elastic-user -n demo -o
jsonpath={.data.elastic} -n demo|base64 -d
r969NUq7Xq3p445XZ46wKqoi
http://10.0.0.200:30635/
#或者通过Kibana的LoadBalancer SVC的IP直接访问
```

如果浏览器如下提示，换一个新的浏览器

![ELK 日志分析第 67 页插图](assets/img-adeb1178db0aa4eb.png)

![ELK 日志分析第 67 页插图](assets/img-9fdcc9f262f68450.png)

![ELK 日志分析第 68 页插图](assets/img-87cbe9e8379e2a60.png)

Kibana会自动加载由filebeat生成的index pattern

![ELK 日志分析第 68 页插图](assets/img-47b14b2a6dfa696f.png)

![ELK 日志分析第 69 页插图](assets/img-92a7d417eec3719d.png)

因此直接进行Discover页面即可查看到数据

![ELK 日志分析第 69 页插图](assets/img-bcafce83d2e01439.png)

```bash
#查看到索引
[root@master1 ~]#PASSWORD=$(kubectl get secret my-es-cluster-es-elastic-user -n
demo -o jsonpath={.data.elastic} -n demo|base64 -d)
[root@master1 ~]#kubectl run --env="PASSWORD=$PASSWORD" client-$RANDOM --image
bowenxiaochun/admin-box:v0.1 -it --rm --restart=Never --command -- /bin/bash
If you don't see a command prompt, try pressing enter.
root@client-20723 /# curl -u "elastic:$PASSWORD" -k https://my-es-cluster-es-
http.demo:9200/_cat/indices
green open .internal.alerts-observability.metrics.alerts-default-000001   MMRQMC-
oSlOgecn87Ps0VQ 1 1    0 0 498b 249b 249b
green open .kibana-observability-ai-assistant-kb-000001
yY4nKSl1QEiBLoWZa1hAHA 1 1    0 0 498b 249b 249b
green open .internal.alerts-observability.logs.alerts-default-000001
0rebNDt6STq4uY2PMvQHsg 1 1    0 0 498b 249b 249b
green open .internal.alerts-observability.uptime.alerts-default-000001
T2TTfGYvTWKRgH2kO603wA 1 1    0 0 498b 249b 249b
green open .internal.alerts-observability.apm.alerts-default-000001
0NbmQkWaSGmER2J4iN0OLQ 1 1    0 0 498b 249b 249b
green open .internal.alerts-stack.alerts-default-000001                   lS-
lNfqrTgiuYRKO2TsJkg 1 1    0 0 498b 249b 249b
green open .internal.alerts-security.alerts-default-000001
9mVaeXk6TsCTYTQcAfZHlA 1 1    0 0 498b 249b 249b
green open .internal.alerts-observability.threshold.alerts-default-000001
N51ZdJrrSFCnT5Z7K-KwzQ 1 1    0 0 498b 249b 249b
green open .kibana-observability-ai-assistant-conversations-000001
8TAi14SnQgye5caorEFeBQ 1 1    0 0 498b 249b 249b
green open .internal.alerts-ml.anomaly-detection.alerts-default-000001
7RGqT7NETAy89tFplSXg8A 1 1    0 0 498b 249b 249b
green open .ds-filebeat-8.11.3-2024.04.21-000001
8tYtJg8GR4qtstr3C8IH6w 1 1 8708 0  8mb  4mb  4mb
green open .internal.alerts-observability.slo.alerts-default-000001       p10vO-
qUQluR1wwqM3U6KQ 1 1    0 0 498b 249b 249b
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/06-elasticsearch-prerequisites.html' | relative_url }}">← Previous: Elasticsearch Prerequisites</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/08-accessing-elasticsearch.html' | relative_url }}">Next: Accessing Elasticsearch →</a>
</nav>
