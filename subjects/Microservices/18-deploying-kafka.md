---
layout: default
title: "微服务架构 · Kafka 部署"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 18 Kafka 部署
### 3.6 Kafka 部署

### Kafka 部署说明

kafka 版本选择

kafka 基于scala语言实现,所以使用kafka需要指定scala的相应的版本.kafka 为多个版本的Scala构建。这仅在使用 Scala 时才重要，并且希望为使用的相同 Scala 版本构建一个版本。否则，任何版本都可以

kafka下载链接

<http://kafka.apache.org/downloads>

kafka版本格式

```text
kafka_<scala 版本>_<kafka 版本>
#示例:
kafka_2.13-2.7.0.tgz
kafka_2.12-3.9.0.tgz
```

![微服务技术第 46 页插图](assets/img-403de8490911109b.png)

scala 语言官网: https://www.scala-lang.org/

scale 与 java关系:https://baike.baidu.com/item/Scala/2462287?fr=aladdin

Kafka 支持单机和集群部署，生产通常为集群模式

官方文档:

<http://kafka.apache.org/quickstart>

![微服务技术第 46 页插图](assets/img-d48243fee2894d72.png)

### 单机部署

### 安装说明

注意：Kafka提供的脚本不支持创建软链接到/usr/local/bin/路径，只支持绝对路径或相对径执行

Download the latest Kafka release and extract it:

```bash
$ apt update && apt -y install openjdk-8-jdk
$ tar -xzf kafka_2.13-3.4.0.tgz
$ cd kafka_2.13-3.4.0
```

NOTE: Your local environment must have Java 8+ installed.

Apache Kafka can be started using ZooKeeper or KRaft. To get started with either configuration follow one the sections below but not both.

Kafka with ZooKeeper

Kafka-v4.0开始即将不再支持Zookeeper

![微服务技术第 47 页插图](assets/img-43dc445f5002b661.png)

Run the following commands in order to start all services in the correct order:

```text
# Start the ZooKeeper service
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open another terminal session and run:

```bash
#默认kafka配置文件，指定zookeeper服务器地址信息（可选）
[root@ubuntu2204 ~]#grep zookeeper /usr/local/kafka/config/server.properties
# Zookeeper connection string (see zookeeper docs for details).
zookeeper.connect=localhost:2181
# Timeout in ms for connecting to zookeeper
zookeeper.connection.timeout.ms=18000
#启动单机kafka
$ bin/kafka-server-start.sh config/server.properties
```

### 旧版基于 zookeeper 部署 kafka单机

注意：Kafka-4.0.0 版本不再支持Zookeeper

范例：基于 zookeeper 部署 kafka单机

```bash
#注意主机名解析,默认主机名称反向解析IP进行访问
[root@ubuntu2404 ~]#hostname
ubuntu2404.bowen.org
[root@ubuntu2404 ~]#vim /etc/hosts
10.0.0.201 ubuntu2404.bowen.org
#支持多个JAVA版本
[root@ubuntu2404 ~]#apt update && apt install -y openjdk-21-jdk
[root@ubuntu2204 ~]#apt update && apt install -y openjdk-8-jdk
[root@ubuntu2204 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.9.0/kafka_2.13-3.9.1.tgz
[root@ubuntu2204 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.9.0/kafka_2.13-3.9.0.tgz
[root@ubuntu2204 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.8.0/kafka_2.13-3.8.0.tgz
[root@ubuntu2204 ~]#tar xf kafka_2.13-3.8.0.tgz  -C /usr/local/
[root@ubuntu2204 ~]#cd /usr/local/
[root@ubuntu2204 local]#ls
bin  etc  games  include  kafka_2.13-3.8.0  lib  man  sbin  share  src
[root@ubuntu2204 local]#ln -s kafka_2.13-3.8.0/ kafka
[root@ubuntu2204 local]#ls kafka
bin  config  libs  LICENSE  licenses  NOTICE  site-docs
[root@ubuntu2204 local]#cd kafka
[root@ubuntu2204 kafka]#ls
bin  config  libs  LICENSE  licenses  NOTICE  site-docs
[root@ubuntu2204 kafka]#ls bin/
connect-distributed.sh        kafka-console-consumer.sh    kafka-get-offsets.sh          kafka-replica-
verification.sh       kafka-verifiable-producer.sh
connect-mirror-maker.sh       kafka-console-producer.sh    kafka-jmx.sh                  kafka-run-class.sh
trogdor.sh
connect-plugin-path.sh        kafka-consumer-groups.sh     kafka-leader-election.sh      kafka-server-start.sh
windows
connect-standalone.sh         kafka-consumer-perf-test.sh  kafka-log-dirs.sh             kafka-server-stop.sh
zookeeper-security-migration.sh
kafka-acls.sh                 kafka-delegation-tokens.sh   kafka-metadata-quorum.sh      kafka-storage.sh
zookeeper-server-start.sh
kafka-broker-api-versions.sh  kafka-delete-records.sh      kafka-metadata-shell.sh       kafka-streams-
application-reset.sh  zookeeper-server-stop.sh
kafka-client-metrics.sh       kafka-dump-log.sh            kafka-mirror-maker.sh         kafka-topics.sh
zookeeper-shell.sh
kafka-cluster.sh              kafka-e2e-latency.sh         kafka-producer-perf-test.sh   kafka-transactions.sh
kafka-configs.sh              kafka-features.sh            kafka-reassign-partitions.sh  kafka-verifiable-
consumer.sh
[root@ubuntu2204 kafka]#ls config/
connect-console-sink.properties    connect-file-sink.properties    connect-mirror-maker.properties  kraft
server.properties       zookeeper.properties
connect-console-source.properties  connect-file-source.properties  connect-standalone.properties
log4j.properties     tools-log4j.properties
connect-distributed.properties     connect-log4j.properties        consumer.properties
producer.properties  trogdor.conf
#修改配置文件
[root@ubuntu2204 kafka]#vim config/zookeeper.properties
dataDir=/data/zookeeper #此目录无需手动创建，启动会自动创建
[root@ubuntu2204 kafka]#bin/zookeeper-server-start.sh config/zookeeper.properties
#修改配置文件
[root@ubuntu2204 kafka]#vim config/server.properties
log.dirs=/data/kafka-logs
[root@ubuntu2204 kafka]#bin/kafka-server-start.sh config/server.properties
[root@ubuntu2204 ~]#ss -ntlp
State           Recv-Q          Send-Q                   Local Address:Port                    Peer
Address:Port         Process
LISTEN          0               128                          127.0.0.1:6010                         0.0.0.0:*
users:(("sshd",pid=1055,fd=7))
LISTEN          0               128                          127.0.0.1:6011                         0.0.0.0:*
users:(("sshd",pid=1568,fd=7))
LISTEN          0               128                          127.0.0.1:6012                         0.0.0.0:*
users:(("sshd",pid=4986,fd=7))
LISTEN          0               128                          127.0.0.1:6013                         0.0.0.0:*
users:(("sshd",pid=5554,fd=7))
LISTEN          0               4096                     127.0.0.53%lo:53                           0.0.0.0:*
users:(("systemd-resolve",pid=794,fd=14))
LISTEN          0               128                            0.0.0.0:22                           0.0.0.0:*
users:(("sshd",pid=839,fd=3))
LISTEN          0               128                              [::1]:6010                            [::]:*
users:(("sshd",pid=1055,fd=5))
LISTEN          0               128                              [::1]:6011                            [::]:*
users:(("sshd",pid=1568,fd=5))
LISTEN          0               128                              [::1]:6012                            [::]:*
users:(("sshd",pid=4986,fd=5))
LISTEN          0               128                              [::1]:6013                            [::]:*
users:(("sshd",pid=5554,fd=5))
LISTEN          0               50                                   *:42243                              *:*
users:(("java",pid=5088,fd=147))
LISTEN          0               50                                   *:9092                               *:*
users:(("java",pid=5088,fd=187))
LISTEN          0               50                                   *:2181                               *:*
users:(("java",pid=4556,fd=157))
LISTEN          0               50                                   *:45197                              *:*
users:(("java",pid=4556,fd=147))
LISTEN          0               128                               [::]:22                              [::]:*
users:(("sshd",pid=839,fd=4))
```

范例：一键安装 Kafka 单机版脚本

```bash
#!/bin/bash
#
#FileName:          install_kafka_single_node.sh
#Description:       The test script
#支持在线和离线安装安装
KAFKA_VERSION=3.6.0
#KAFKA_VERSION=3.5.1
#KAFKA_VERSION=3.5.0
#KAFKA_VERSION=3.4.0
#KAFKA_VERSION=3.3.2
#KAFKA_VERSION=3.2.0
#KAFKA_VERSION=-3.0.0
SCALA_VERSION=2.13
KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_V
ERSION}.tgz"
#KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.8.1/kafka_2.13-2.8.1.tgz"
#KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.7.1/kafka_2.13-2.7.1.tgz"
KAFKA_INSTALL_DIR=/usr/local/kafka
HOST=`hostname -I|awk '{print $1}'`
```

```text
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
env () {
echo $HOST `hostname` >> /etc/hosts
}
install_jdk() {
java -version &>/dev/null && { color "JDK 已安装!" 1 ; return;  }
if command -v yum &>/dev/null ; then
yum -y install java-1.8.0-openjdk-devel || { color "安装JDK失败!" 1; exit 1; }
elif command -v apt &>/dev/null ; then
apt update
#apt install openjdk-11-jdk -y || { color "安装JDK失败!" 1; exit 1; }
apt install openjdk-8-jdk -y || { color "安装JDK失败!" 1; exit 1; }
else
color "不支持当前操作系统!" 1
exit 1
fi
java -version && { color "安装 JDK 完成!" 0 ; } || { color "安装JDK失败!" 1; exit 1; }
}
install_zookeeper() {
cat > ${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh <<EOF
#!/bin/bash
nohup ${KAFKA_INSTALL_DIR}/bin/zookeeper-server-start.sh ${KAFKA_INSTALL_DIR}/config/zookeeper.properties   &
EOF
chmod +x ${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh
cat > /lib/systemd/system/zookeeper.service <<EOF
[Unit]
Description=zookeeper.service
After=network.target
[Service]
Type=forking
ExecStart=${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh
ExecStop=${KAFKA_INSTALL_DIR}/bin/zookeeper-server-stop.sh
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now  zookeeper.service
systemctl is-active zookeeper.service
if [ $? -eq 0 ] ;then
color "zookeeper 安装成功!" 0
else
color "zookeeper 安装失败!" 1
exit 1
fi
}
install_kafka(){
if [ ! -f kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz ];then
wget -P /usr/local/src/  --no-check-certificate $KAFKA_URL  || { color  "下载失败!" 1 ;exit ; }
fi
tar xf /usr/local/src/${KAFKA_URL##*/}  -C /usr/local/
ln -s /usr/local/kafka_${SCALA_VERSION}-${KAFKA_VERSION}  ${KAFKA_INSTALL_DIR}
install_zookeeper
echo PATH=${KAFKA_INSTALL_DIR}/bin:'$PATH' >> /etc/profile
cat > ${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh <<EOF
#!/bin/bash
nohup ${KAFKA_INSTALL_DIR}/bin/kafka-server-start.sh  ${KAFKA_INSTALL_DIR}/config/server.properties &
EOF
chmod +x ${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh
cat > /lib/systemd/system/kafka.service <<EOF
[Unit]
Description=Apache kafka
After=network.target
[Service]
Type=forking
ExecStart=${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh
ExecStop=/bin/kill  -TERM \${MAINPID}
Restart=always
RestartSec=20
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now kafka.service
#kafka-server-start.sh -daemon ${KAFKA_INSTALL_DIR}/config/server.properties
systemctl is-active kafka.service
if [ $? -eq 0 ] ;then
color "kafka 安装成功!" 0
else
color "kafka 安装失败!" 1
exit 1
fi
}
env
install_jdk
install_kafka
```

![微服务技术第 51 页插图](assets/img-7cd765af0e2af88c.png)

### 基于KRaft 部署 kafka单机

注意：Kafka-4.0.0 版本不再支持Zookeeper，使用Kraft

范例：基于KRaft 部署 kafka单机

```bash
#https://kafka.apache.org/quickstart
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-21-jdk
[root@ubuntu2404 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/4.1.0/kafka_2.13-4.1.0.tgz
[root@ubuntu2404 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/4.0.0/kafka_2.13-4.0.0.tgz
[root@ubuntu2404 ~]#tar xf kafka_2.13-4.0.0.tgz  -C /usr/local/
[root@ubuntu2404 ~]#cd /usr/local/
[root@ubuntu2404 local]#ls
bin  etc  games  include  kafka_2.13-4.0.0  lib  man  sbin  share  src
[root@ubuntu2404 local]#ln -s kafka_2.13-4.0.0/ kafka
[root@ubuntu2404 local]#cd kafka
[root@ubuntu2404 kafka]#pwd
/usr/local/kafka
#生成集群唯一ID,Generate a Cluster UUID,集群内的多个节点需使用同一集群ID
[root@ubuntu2404 kafka]#KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
Format Log Directories
#建议修改数据日录
#4.0.0版本路径
[root@ubuntu2404 kafka]#vim config/server.properties
#旧版路径
[root@ubuntu2404 kafka]#vim config/kraft/server.properties
#log.dirs=/tmp/kraft-combined-logs
log.dirs=/data/kraft-combined-logs
#格式化初始数据
#4.0.0版本以后路径
[root@ubuntu2404 kafka]#bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c
config/server.properties
#3.X以前旧版路径
[root@ubuntu2404 kafka]#bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c
config/kraft/server.properties
Start the Kafka Serve
#自动创建目录
[root@ubuntu2404 kafka]#ls /data/kraft-combined-logs
bootstrap.checkpoint  meta.properties
#启动
#4.0.0版本路径
[root@ubuntu2404 kafka]#bin/kafka-server-start.sh config/server.properties
#旧版路径
[root@ubuntu2404 kafka]#bin/kafka-server-start.sh config/kraft/server.properties
[root@ubuntu2404 kafka]#ss -ntlp|grep java
LISTEN 0      50                 *:9093             *:*    users:(("java",pid=35179,fd=146))
LISTEN 0      50                 *:9092             *:*    users:(("java",pid=35179,fd=174))
LISTEN 0      50                 *:35565            *:*    users:(("java",pid=32799,fd=126))
LISTEN 0      50                 *:33431            *:*    users:(("java",pid=26718,fd=126))
LISTEN 0      50                 *:35079            *:*    users:(("java",pid=27146,fd=126))
LISTEN 0      50                 *:46365            *:*    users:(("java",pid=26325,fd=126))
LISTEN 0      50                 *:43399            *:*    users:(("java",pid=35179,fd=127))
LISTEN 0      50                 *:37933            *:*    users:(("java",pid=27604,fd=126))
```

### 集群部署

### 基于 zookeeper 模式的集群（重点）

3.6.3.1.1 环境准备

3.6.3.1.1.1 主机名解析

注意：每个kafka节点的主机名称解析需要提前准备，否则会导致失败

```bash
#修改每个kafka节点的主机名
[root@ubuntu2204 ~]#hostnamectl hostname node1
[root@ubuntu2204 ~]#hostnamectl hostname node2
[root@ubuntu2204 ~]#hostnamectl hostname node3
#在所有kafka节点上实现主机名称解析
[root@ubuntu2204 ~]#cat /etc/hosts
10.0.0.201 node1
10.0.0.202 node2
10.0.0.203 node3
```

3.6.3.1.1.2 安装 JAVA

```bash
[root@ubuntu24.04-node1 ~]#apt update && apt  -y install openjdk-21-jre
[root@ubuntu24.04-node1 ~]#java -version
openjdk version "21.0.6" 2025-01-21
OpenJDK Runtime Environment (build 21.0.6+7-Ubuntu-124.04.1)
OpenJDK 64-Bit Server VM (build 21.0.6+7-Ubuntu-124.04.1, mixed mode, sharing)
[root@node1 ~]#apt update && apt install openjdk-8-jdk -y
```

3.6.3.1.1.3 安装 ZooKeeper

4.0以前版本 Kafka 依赖 Zookeeper 服务,但以后将不再依赖

```text
http://kafka.apache.org/quickstart
# Note: Soon, ZooKeeper will no longer be required by Apache Kafka.
```

环境说明

```text
#在三个Ubuntu18.04节点提前部署zookeeper和kafka三个节点复用
node1:10.0.0.201
node2:10.0.0.202
node3:10.0.0.203
#注意:生产中zookeeper和kafka一般是分开独立部署的,kafka安装前需要安装java环境
```

确保三个节点的zookeeper启动

```bash
[root@node1 ~]#zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: follower
[root@node2 ~]#zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: leader
[root@node3 ~]#zkServer.sh status
/usr/bin/java
ZooKeeper JMX enabled by default
Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
Client port found: 2181. Client address: localhost. Client SSL: false.
Mode: follower
```

注意:如果使用kafka自带的zookeeper，需要修改配置文件,如下示例

范例：

```bash
#注意如果使用kafka自带的zookeeper，需要修改配置文件
[root@ubuntu24.04-node1 ~]#apt update && apt  -y install openjdk-21-jre
[root@node1 ~]#apt update && apt install openjdk-8-jdk -y
[root@node1 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.8.0/kafka_2.13-3.8.0.tgz
[root@node1 ~]#tar xf kafka_2.13-3.8.0.tgz  -C /usr/local
[root@node1 ~]#ln -s /usr/local/kafka_2.13-3.8.0/ /usr/local/kafka
[root@node1 ~]#ls /usr/local/kafka
bin  config  libs  LICENSE  licenses  NOTICE  site-docs
#集群配置必须配置时间相关
[root@node1 ~]#vim /usr/local/kafka/config/zookeeper.properties
#必须添加时间相关配置
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
#保留下面内容
clientPort=2181
maxClientCnxns=0
admin.enableServer=false
#添加下面集群配置
dataDir=/usr/local/kafka/data/
server.1=10.0.0.201:2888:3888
server.2=10.0.0.202:2888:3888
server.3=10.0.0.203:2888:3888
[root@node1 ~]#mkdir /usr/local/kafka/data
[root@node1 ~]#echo 1 > /usr/local/kafka/data/myid
[root@node1 ~]#rsync -av /usr/local/kafka* 10.0.0.202|203:/usr/local
#修改各个节点的MyID
[root@node2 ~]#echo 2 > /usr/local/kafka/data/myid
[root@node3 ~]#echo 3 > /usr/local/kafka/data/myid
#在所有节点上启动
[root@node1 ~]#/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties
```

3.6.3.1.2 各节点部署 Kafka

3.6.3.1.2.1 Kafka 节点配置

配置文件说明

```text
#配置文件 ./conf/server.properties内容说明
############################# Server Basics###############################
# broker的id，值为整数，且必须唯一，在一个集群中不能重复，此行必须修改
broker.id=1
############################# Socket ServerSettings ######################
# kafka监听端口，默认9092
listeners=PLAINTEXT://10.0.0.101:9092
# 处理网络请求的线程数量，默认为3个
num.network.threads=3
# 执行磁盘IO操作的线程数量，默认为8个
num.io.threads=8
# socket服务发送数据的缓冲区大小，默认100KB
socket.send.buffer.bytes=102400
# socket服务接受数据的缓冲区大小，默认100KB
socket.receive.buffer.bytes=102400
# socket服务所能接受的一个请求的最大大小，默认为100M
socket.request.max.bytes=104857600
############################# Log Basics###################################
# kafka存储消息数据的目录
log.dirs=/usr/local/kafka/data
# 每个topic默认的partition
num.partitions=1
# 设置副本数量为3,当Leader的Replication故障，会进行故障自动转移。
default.replication.factor=3
# 在启动时恢复数据和关闭时刷新数据时每个数据目录的线程数量
num.recovery.threads.per.data.dir=1
############################# Log FlushPolicy #############################
# 消息刷新到磁盘中的消息条数阈值
log.flush.interval.messages=10000
# 消息刷新到磁盘中的最大时间间隔1s,单位是ms
log.flush.interval.ms=1000
############################# Log RetentionPolicy #########################
# 日志保留小时数，超时会自动删除，默认为7天
log.retention.hours=168
# 日志保留大小，超出大小会自动删除，默认为1G
#log.retention.bytes=1073741824
# 日志分片策略，单个日志文件的大小最大为1G，超出后则创建一个新的日志文件
log.segment.bytes=1073741824
# 每隔多长时间检测数据是否达到删除条件,300s
log.retention.check.interval.ms=300000
############################# Zookeeper ####################################
# Zookeeper连接信息，如果是zookeeper集群，则以逗号隔开，此行必须修改
zookeeper.connect=10.0.0.101:2181,10.0.0.102:2181,10.0.0.103:2181
# 连接zookeeper的超时时间,6s
zookeeper.connection.timeout.ms=6000
# 是否允许删除topic，默认为false，topic只会标记为marked for deletion
delete.topic.enable=true
```

范例：配置kafka_2.13-3.9.1

```bash
[root@node1 ~]#vim /usr/local/kafka/config/server.properties
#修改下面五行
broker.id=0 #每个节点不同
listeners=PLAINTEXT://10.0.0.201:9092 #每个节点不同
log.dirs=/usr/local/kafka/data
zookeeper.connect=10.0.0.201:2181,10.0.0.202:2181,10.0.0.203:2181
zookeeper.connect=10.0.0.201:2181,10.0.0.202:2181,10.0.0.203:2181
```

范例：

```bash
#在所有节点上执行安装java
[root@node1 ~]#apt install openjdk-8-jdk -y
#在所有节点上执行下载，官方下载
[root@node1 ~]#wget https://downloads.apache.org/kafka/3.3.1/kafka_2.13-3.3.1.tgz
[root@node1 ~]#wget https://archive.apache.org/dist/kafka/2.7.0/kafka_2.13-2.7.0.tgz
#国内镜像下载
[root@node1 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.3.1/kafka_2.13-3.3.1.tgz
[root@node1 ~]#wget https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/3.0.0/kafka_2.13-3.0.0.tgz
[root@node1 ~]#wget https://mirror.bit.edu.cn/apache/kafka/2.7.0/kafka_2.13-2.7.0.tgz
#解压缩
[root@node1 ~]#tar xf kafka_2.13-2.7.0.tgz  -C /usr/local/
[root@node1 ~]#ln -s /usr/local/kafka_2.13-2.7.0/ /usr/local/kafka
#配置PATH变量
[root@node1 ~]#echo 'PATH=/usr/local/kafka/bin:$PATH' > /etc/profile.d/kafka.sh
[root@node1 ~]#. /etc/profile.d/kafka.sh
#修改配置文件
[root@node1 ~]#vim /usr/local/kafka/config/server.properties
broker.id=1 #每个broker在集群中每个节点的正整数唯一标识，此值保存在log.dirs下的meta.properties文件，修改此行
listeners=PLAINTEXT://10.0.0.101:9092 #指定当前主机的IP做为监听地址,注意:不支持0.0.0.0
log.dirs=/usr/local/kafka/data #kakfa用于保存数据的目录，所有的消息都会存储在该目录当中，修改此行
num.partitions=1 #设置创建新的topic时默认分区数量,建议和kafka的节点数量一致
default.replication.factor=3 #指定默认的副本数为3，可以实现故障的自动转移
log.retention.hours=168 #设置kafka中消息保留时间，默认为168小时即7天
zookeeper.connect=10.0.0.101:2181,10.0.0.102:2181,10.0.0.103:2181 #指定连接的zk的地址,zk中存储了broker的元数据信息，
修改此行
zookeeper.connection.timeout.ms=6000 #设置连接zookeeper的超时时间，单位为ms,默认6秒钟
#准备数据目录
[root@node1 ~]#mkdir /usr/local/kafka/data
[root@node1 ~]#scp /usr/local/kafka/config/server.properties 10.0.0.102:/usr/local/kafka/config
[root@node1 ~]#scp /usr/local/kafka/config/server.properties 10.0.0.103:/usr/local/kafka/config
#修改第2个节点配置
[root@node2 ~]#vim /usr/local/kafka/config/server.properties
broker.id=2 #每个broker 在集群中的唯一标识，正整数。
listeners=PLAINTEXT://10.0.0.102:9092 #指定当前主机的IP做为监听地址,注意:不支持0.0.0.0
#修改第3个节点配置
[root@node3 ~]#vim /usr/local/kafka/config/server.properties
broker.id=3  #每个broker 在集群中的唯一标识，正整数。
listeners=PLAINTEXT://10.0.0.103:9092 #指定当前主机的IP做为监听地址,注意:不支持0.0.0.0
#可以调整内存
[root@node1 ~]#vim /usr/local/kafka/bin/kafka-server-start.sh
......
if[ " x$KAFKA_HEAP_OPTS"="x"] ; then
export KAFKA_HEAP_OPTS=" -Xmx1G -Xms1G"
fi
......
```

3.6.3.1.2.2 启动服务

在所有kafka节点执行下面操作

```bash
#前台启动
[root@node1 ~]#/usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server.properties
#后台启动
[root@node1 ~]#/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties
```

3.6.3.1.2.3 确保服务启动状态

```bash
[root@node1 ~]#ss -ntl|grep 9092
LISTEN  0        50          [::ffff:10.0.0.101]:9092                  *:*
[root@node1 ~]#tail /usr/local/kafka/logs/server.log
[2021-02-16 12:10:01,276] INFO [ExpirationReaper-1-AlterAcls]: Starting
(kafka.server.DelayedOperationPurgatory$ExpiredOperationReaper)
[2021-02-16 12:10:01,311] INFO [/config/changes-event-process-thread]: Starting
(kafka.common.ZkNodeChangeNotificationListener$ChangeEventProcessThread)
[2021-02-16 12:10:01,332] INFO [SocketServer brokerId=1] Starting socket server acceptors and processors
(kafka.network.SocketServer)
[2021-02-16 12:10:01,339] INFO [SocketServer brokerId=1] Started data-plane acceptor and processor(s) for
endpoint : ListenerName(PLAINTEXT) (kafka.network.SocketServer)
[2021-02-16 12:10:01,340] INFO [SocketServer brokerId=1] Started socket server acceptors and processors
(kafka.network.SocketServer)
[2021-02-16 12:10:01,344] INFO Kafka version: 2.7.0 (org.apache.kafka.common.utils.AppInfoParser)
[2021-02-16 12:10:01,344] INFO Kafka commitId: 448719dc99a19793 (org.apache.kafka.common.utils.AppInfoParser)
[2021-02-16 12:10:01,344] INFO Kafka startTimeMs: 1613448601340 (org.apache.kafka.common.utils.AppInfoParser)
[2021-02-16 12:10:01,346] INFO [KafkaServer id=1] started (kafka.server.KafkaServer)
[2021-02-16 12:10:01,391] INFO [broker-1-to-controller-send-thread]: Recorded new controller, from now on will
use broker 1 (kafka.server.BrokerToControllerRequestThread)
#如果使用id,还需要修改/usr/local/kafka/data/meta.properties
#打开zooinspector可以看到三个id
```

![微服务技术第 56 页插图](assets/img-434f253678ed468b.png)

Broker 依赖于 Zookeeper，每个Broker 的id 和 Topic、Partition这些元数据信息都会写入Zookeeper 的 ZNode 节点中 consumer 依赖于Zookeeper，Consumer 在消费消息时，每消费完一条消息，会将产生的offset 保存到 Zookeeper 中，下次消费在当前offset往后继续消费.kafka0.9 之前Consumer 的offset 存储在 Zookeeper 中，kafka0.9 以后offset存储在本地。 Partition 依赖于 Zookeeper，Partition 完成Replication 备份后，选举出一个Leader，这个是依托于 Zookeeper 的选举机制实现的

3.6.3.1.2.4 准备Kafka的service文件

```bash
[root@node1 ~]#cat /lib/systemd/system/kafka.service
[unit]
Description=Apache kafka
After=network.target
[service]
Type=simple
#Environment=JAVA_HOME=/data/server/java
PIDFile=/usr/local/kafka/kafka.pid
Execstart=/usr/local/kafka/bin/kafka-server-start.sh  /usr/local/kafka/config/server. properties
Execstop=/bin/kill  -TERM ${MAINPID}
Restart=always
RestartSec=20
[Install]
wantedBy=multi-user.target
[root@node1 ~]#systemctl daemon-load
[root@node1 ~]#systemctl restart kafka.service
```

3.6.3.1.3 Kafka 集群部署脚本

```bash
#!/bin/bash
#
#FileName:          install_kafka.sh
#Description:       The test script
#支持在线和离线安装安装
NODE1=10.0.0.101
NODE2=10.0.0.102
NODE3=10.0.0.103
KAFKA_VERSION=3.5.1
#KAFKA_VERSION=3.5.0
#KAFKA_VERSION=3.4.0
#KAFKA_VERSION=3.3.2
#KAFKA_VERSION=3.2.0
#KAFKA_VERSION=-3.0.0
SCALA_VERSION=2.13
KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_V
ERSION}.tgz"
#KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.8.1/kafka_2.13-2.8.1.tgz"
#KAFKA_URL="https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/2.7.1/kafka_2.13-2.7.1.tgz"
KAFKA_INSTALL_DIR=/usr/local/kafka
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
env () {
if hostname -I |grep -q $NODE1;then
ID=1
hostnamectl set-hostname node1
elif hostname -I |grep -q $NODE2;then
ID=2
hostnamectl set-hostname node2
elif hostname -I |grep -q $NODE3;then
ID=3
hostnamectl set-hostname node3
else
color 'IP地址错误' 1
exit
fi
cat >> /etc/hosts <<EOF
$NODE1   node1
$NODE2   node2
$NODE3   node3
EOF
}
install_jdk() {
java -version &>/dev/null && { color "JDK 已安装!" 1 ; return;  }
if command -v yum &>/dev/null ; then
yum -y install java-1.8.0-openjdk-devel || { color "安装JDK失败!" 1; exit 1; }
elif command -v apt &>/dev/null ; then
apt update
#apt install openjdk-11-jdk -y || { color "安装JDK失败!" 1; exit 1; }
apt install openjdk-8-jdk -y || { color "安装JDK失败!" 1; exit 1; }
else
color "不支持当前操作系统!" 1
exit 1
fi
java -version && { color "安装 JDK 完成!" 0 ; } || { color "安装JDK失败!" 1; exit 1; }
}
install_zookeeper() {
mv ${KAFKA_INSTALL_DIR}/config/zookeeper.properties{,.bak}
cat > ${KAFKA_INSTALL_DIR}/config/zookeeper.properties <<EOF
tickTime=2000
initLimit=10
syncLimit=5
dataDir=${KAFKA_INSTALL_DIR}/data
clientPort=2181
maxClientCnxns=128
autopurge.snapRetainCount=3
autopurge.purgeInterval=24
server.1=${NODE1}:2888:3888
server.2=${NODE2}:2888:3888
server.3=${NODE3}:2888:3888
EOF
mkdir -p ${KAFKA_INSTALL_DIR}/data
echo $ID > ${KAFKA_INSTALL_DIR}/data/myid
cat > ${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh <<EOF
#!/bin/bash
nohup ${KAFKA_INSTALL_DIR}/bin/zookeeper-server-start.sh ${KAFKA_INSTALL_DIR}/config/zookeeper.properties   &
EOF
chmod +x ${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh
cat > /lib/systemd/system/zookeeper.service <<EOF
[Unit]
Description=zookeeper.service
After=network.target
[Service]
Type=forking
ExecStart=${KAFKA_INSTALL_DIR}/bin/zookeeper-startup.sh
ExecStop=${KAFKA_INSTALL_DIR}/bin/zookeeper-server-stop.sh
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now  zookeeper.service
systemctl is-active zookeeper.service
if [ $? -eq 0 ] ;then
color "zookeeper 安装成功!" 0
else
color "zookeeper 安装失败!" 1
exit 1
fi
}
install_kafka(){
if [ ! -f kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz ];then
wget -P /usr/local/src/  --no-check-certificate $KAFKA_URL  || { color  "下载失败!" 1 ;exit ; }
fi
tar xf /usr/local/src/${KAFKA_URL##*/}  -C /usr/local/
ln -s /usr/local/kafka_${SCALA_VERSION}-${KAFKA_VERSION}  ${KAFKA_INSTALL_DIR}
install_zookeeper
echo PATH=${KAFKA_INSTALL_DIR}/bin:'$PATH' >> /etc/profile
mv ${KAFKA_INSTALL_DIR}/config/server.properties{,.bak}
cat > ${KAFKA_INSTALL_DIR}/config/server.properties <<EOF
broker.id=$ID
listeners=PLAINTEXT://${HOST}:9092
log.dirs=${KAFKA_INSTALL_DIR}/data
num.partitions=1
log.retention.hours=168
zookeeper.connect=${NODE1}:2181,${NODE2}:2181,${NODE3}:2181
zookeeper.connection.timeout.ms=6000
delete.topic.enable=true
EOF
cat > ${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh <<EOF
#!/bin/bash
nohup ${KAFKA_INSTALL_DIR}/bin/kafka-server-start.sh  ${KAFKA_INSTALL_DIR}/config/server.properties &
EOF
chmod +x ${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh
cat > /lib/systemd/system/kafka.service <<EOF
[Unit]
Description=Apache kafka
After=network.target
[Service]
Type=forking
ExecStart=${KAFKA_INSTALL_DIR}/bin/kafka-startup.sh
ExecStop=/bin/kill  -TERM \${MAINPID}
Restart=always
RestartSec=20
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now kafka.service
#kafka-server-start.sh -daemon ${KAFKA_INSTALL_DIR}/config/server.properties
systemctl is-active kafka.service
if [ $? -eq 0 ] ;then
color "kafka 安装成功!" 0
else
color "kafka 安装失败!" 1
exit 1
fi
}
env
install_jdk
install_kafka
```

### 基于Kraft模式的集群（了解）

3.6.3.2.1 基础环境准备

1. 节点规划

准备3个节点（例如kafka01、kafka02、kafka03），每个节点同时作为Broker和Controller运行确保节点间网络互通，并配置主机名解析（修改/etc/hosts 或DNS）

2. 软件安装

安装 JAVA 下载Kafka安装包（推荐3.0+版本），解压至统一目录（如/opt/kafka ） 所有节点安装相同版本的Kafka

案例: 基于Kraft模式的Kafka 集群基础环境准备

```bash
[root@ubuntu2404 ~]#cat >> /etc/hosts <<EOF
10.0.0.201 kafka01
10.0.0.202 kafka02
10.0.0.203 kafka03
EOF
[root@ubuntu2404 ~]#apt update && apt -y install openjdk-21-jre
[root@ubuntu2404 ~]#VERSION=4.0.0
[root@ubuntu2404 ~]#VERSION=3.9.0
[root@ubuntu2404 ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/apache/kafka/${VERSION}/kafka_2.13-${VERSION}.tgz
[root@ubuntu2404 ~]#tar xf kafka_2.13-${VERSION}.tgz -C /usr/local/
[root@ubuntu2404 ~]#cd /usr/local/
[root@ubuntu2404 local]#ln -s kafka_2.13-${VERSION}/ kafka
[root@ubuntu2404 local]#cd kafka
[root@ubuntu2404 kafka]#pwd
/usr/local/kafka
[root@ubuntu2404 kafka]#ls
bin  config  libs  LICENSE  licenses  NOTICE  site-docs
[root@ubuntu2404 kafka]#tree -d
.
├── bin
│   └── windows
├── config
│   └── kraft
├── libs
├── licenses
└── site-docs
8 directories
```

3.6.3.2.2 集群配置

1. 修改server.properties 文件

关键参数配置,所有节点均需修改，以下以节点kafka01为例

```bash
#4.0.0版本路径
[root@ubuntu2404 kafka]#vim config/server.properties
#旧版路径
[root@ubuntu2404 kafka]#vim config/kraft/server.properties
# 角色定义（同时作为Broker和Controller）
process.roles=broker,controller
# 节点唯一ID（不同节点需不同）
node.id=1
# 控制器节点列表（格式：node.id@host:port）
controller.quorum.voters=1@kafka01:9093,2@kafka02:9093,3@kafka03:9093
# 监听地址（Broker通信端口和Controller端口）
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
# 对外暴露的地址（根据实际IP或域名配置）注意:不支持0.0.0.0
advertised.listeners=PLAINTEXT://kafka01:9092,CONTROLLER://kafka01:9093
# 日志存储目录
log.dirs=/data/kafka-logs
[root@ubuntu2404 kafka]#grep -Ev "#|^$" config/server.properties
process.roles=broker,controller
node.id=1 #每个节点不同
controller.quorum.voters=1@kafka01:9093,2@kafka02:9093,3@kafka03:9093
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
inter.broker.listener.name=PLAINTEXT
advertised.listeners=PLAINTEXT://kafka01:9092,CONTROLLER://kafka01:9093 #每个节点不同
log.dirs=/data/kafka-logs
.....
```

2. 生成集群唯一ID

```bash
# 生成UUID
[root@ubuntu2404 kafka]#./bin/kafka-storage.sh random-uuid
# 示例输出：iT0tvD1wSPGusA1SWlRNOQ
```

所有节点需使用同一集群ID 。

3. 初始化元数据存储

每个节点均需执行此操作

```bash
# 使用生成的UUID初始化存储目录
#4.0.0版本路径
[root@ubuntu2404 kafka]#./bin/kafka-storage.sh format -t <生成的UUID> -c config/server.properties
#旧版
[root@ubuntu2404 kafka]#./bin/kafka-storage.sh format -t <生成的UUID> -c ./config/kraft/server.properties
```

3.6.3.2.3 集群启动

```bash
# 后台启动服务
#4.0.0版本路径
[root@ubuntu2404 kafka]#./bin/kafka-server-start.sh -daemon config/server.properties
#旧版
[root@ubuntu2404 kafka]#./bin/kafka-server-start.sh -daemon ./config/kraft/server.properties
```

按顺序启动所有节点

3.6.3.2.4 集群验证

通过生产/消费消息验证集群可用性

创建Topic测试 ：

```bash
[root@ubuntu2404 kafka]#./bin/kafka-topics.sh --create --topic foo --partitions 3 --replication-factor 3 --
bootstrap-server kafka01:9092
[root@ubuntu2404 kafka]#./bin/kafka-topics.sh --list --bootstrap-server kafka01:9092
test
#生产消费信息：
[root@ubuntu2404 kafka]#./bin/kafka-console-producer.sh --broker-list kafka01:9092 --topic foo
[root@ubuntu2404 kafka]#./bin/kafka-console-consumer.sh --bootstrap-server kafka01:9092 --from-beginning --
topic  foo  --group foo_group
```

检查节点状态：

```bash
[root@ubuntu2404 kafka]#./bin/kafka-metadata-shell.sh --snapshot /data/kafka-logs/__cluster_metadata-
0/00000000000000000000.log
```

### Kubernetes 部署 Kafka

基于Kubernetes的 Operator 安装 Kafka 集群

<https://strimzi.io/quickstarts/>

<https://operatorhub.io/operator/strimzi-kafka-operator>

![微服务技术第 61 页插图](assets/img-bf2c2a708fd424ce.png)

```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
name: my-cluster
spec:
kafka:
version: 3.8.0
replicas: 3
listeners:
- name: plain
port: 9092
type: internal
tls: false
- name: tls
port: 9093
type: internal
tls: true
config:
offsets.topic.replication.factor: 3
transaction.state.log.replication.factor: 3
transaction.state.log.min.isr: 2
default.replication.factor: 3
min.insync.replicas: 2
inter.broker.protocol.version: '3.8'
storage:
type: ephemeral
zookeeper:
replicas: 3
storage:
type: ephemeral
entityOperator:
topicOperator: {}
userOperator: {}
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/17-kafka-roles-and-workflow.html' | relative_url }}">← Previous: Kafka Roles and Workflow</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/19-reading-and-writing-kafka-data.html' | relative_url }}">Next: Reading and Writing Kafka Data →</a>
</nav>
