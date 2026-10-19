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

Kafka 的安装重点是**先确定版本与元数据模式**。Kafka 3.9 可以部署 KRaft 或维护已有 ZooKeeper 模式；Kafka 4.0 起不再支持 ZooKeeper 模式。两种模式的配置和数据目录不能混用，旧集群迁移也不是将目录直接格式化。下文先给出可验证的 KRaft 单机试验，再扩展到三节点；旧 ZooKeeper 和 Kubernetes 资料置于末尾作为独立路径。

Kafka 发布包名称包含 Scala 二进制版本与 Kafka 版本，例如 `kafka_2.13-3.9.0.tgz`。运行 Broker 时首先核对 Kafka 与 Java 的兼容要求；开发 Scala 客户端或插件时还需关注 Scala 二进制兼容性。下载地址和校验值以 [Apache Kafka 下载页](https://kafka.apache.org/downloads)为准，不把多年前的镜像地址或终端输出当作当前可执行命令。

![Kafka 发行包命名参考](assets/img-403de8490911109b.webp)

## 一、KRaft 单机试验

以下选择 Kafka 3.9.0 和 Java 17，在隔离的 Linux 测试机上运行。单机同时承担 Broker 和 Controller，**没有节点故障容忍**。下载后应按照官方 SHA512 文件校验包完整性。

```bash
sudo apt update
sudo apt install -y openjdk-17-jre-headless curl
java -version
VERSION=3.9.0
curl -fLO "https://archive.apache.org/dist/kafka/$VERSION/kafka_2.13-$VERSION.tgz"
tar -xzf "kafka_2.13-$VERSION.tgz"
cd "kafka_2.13-$VERSION"
```

先查看 `config/kraft/server.properties` 的 `node.id`、`listeners`、`advertised.listeners` 和 `log.dirs`。默认示例仅适合本机演示，若改了日志目录，确保它是一个**新的空目录**。下面的 Cluster ID 只为此新集群生成一次；`format` 也只对新目录执行一次，切勿在已有数据上重复格式化。

```bash
CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t "$CLUSTER_ID" -c config/kraft/server.properties
bin/kafka-server-start.sh config/kraft/server.properties
```

另开终端进入同一安装目录，检查服务并创建测试 Topic。`--bootstrap-server` 应指向 Broker 的客户端监听地址，而非 Controller 端口。

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic demo-events --partitions 1 --replication-factor 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic demo-events
```

若客户端连接失败，先检查 Broker 日志、9092 监听端口和 `advertised.listeners`。Kafka 返回给客户端的广告地址必须从客户端所在网络可达；仅仅让启动命令成功并不足以证明远端客户端能使用集群。

## 二、三节点 KRaft 集群

三台机器使用同一 Kafka 版本，示例主机名分别为 `kafka01`、`kafka02`、`kafka03`，须互相解析，9092 与 9093 端口在可信网络内连通。三台均承担 Broker 和 Controller 角色，适合教学与小规模起点；生产中应再评估独立 Controller、故障域、磁盘容量、备份、认证和加密。

| 节点 | `node.id` | 客户端/Broker 端口 | Controller 端口 |
| --- | ---: | --- | --- |
| kafka01 | 1 | kafka01:9092 | kafka01:9093 |
| kafka02 | 2 | kafka02:9092 | kafka02:9093 |
| kafka03 | 3 | kafka03:9092 | kafka03:9093 |

各节点安装 Kafka 3.9.0，并准备彼此独立的空数据目录。下方是 **kafka01** 的 `config/kraft/server.properties` 核心配置；另两台保持相同 `controller.quorum.voters`，分别将 `node.id` 改为 2/3、将 `advertised.listeners` 改为自己的主机名。不要把这三个节点的同一目录挂到共享文件系统。

```properties
process.roles=broker,controller
node.id=1
controller.quorum.voters=1@kafka01:9093,2@kafka02:9093,3@kafka03:9093
listeners=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
advertised.listeners=PLAINTEXT://kafka01:9092
listener.security.protocol.map=PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
inter.broker.listener.name=PLAINTEXT
controller.listener.names=CONTROLLER
log.dirs=/data/kafka-logs
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=2
default.replication.factor=3
min.insync.replicas=2
```

`PLAINTEXT` 只用于受限网络中的实验，生产应配置 TLS/SASL 和访问控制。`advertised.listeners` 不应包含 Controller 监听器，也不能填写仅本机可见的地址。三节点使用**同一个 Cluster ID**，但 `node.id` 各不相同。先确认数据目录为空，再各格式化一次：

```bash
# 只在一台机器生成并记录 ID
bin/kafka-storage.sh random-uuid
# 在三台机器分别执行，填入同一个真实 ID，不要照抄字面量 CLUSTER_ID
bin/kafka-storage.sh format -t CLUSTER_ID -c config/kraft/server.properties
bin/kafka-server-start.sh -daemon config/kraft/server.properties
```

待三台 Broker 启动和 Controller 多数派形成后，检查仲裁、分区副本及端到端读写；副本因子 3 要求三个健康 Broker 均在场。

```bash
bin/kafka-metadata-quorum.sh --bootstrap-server kafka01:9092 describe --status
bin/kafka-topics.sh --bootstrap-server kafka01:9092 \
  --create --topic demo-events --partitions 3 --replication-factor 3
bin/kafka-topics.sh --bootstrap-server kafka01:9092 --describe --topic demo-events
bin/kafka-console-producer.sh --bootstrap-server kafka01:9092 --topic demo-events
# 另开终端，输入一行测试消息后观察输出
bin/kafka-console-consumer.sh --bootstrap-server kafka01:9092 \
  --topic demo-events --from-beginning --group demo-check
```

除 Broker 存活外，还需核对 Topic 无离线分区、ISR 满足预期、消费者能继续读取。若创建失败，优先检查主机名解析、Controller 法定多数派、广告地址、磁盘权限和日志，**不要清空 `log.dirs` 重新格式化**。部署完成后再为持久化目录、滚动升级和故障演练制定备份与恢复流程。

## 三、旧版 ZooKeeper 模式：仅供维护现有集群

旧课件里的 `zookeeper.connect`、`broker.id`、ZooKeeper znode 和截图对应 Kafka 4.0 以前的运行模式。其完整旧终端记录混用了 Kafka 2.7、3.4、3.8、3.9，Java 8/21、不同 IP、重复配置项及无效的 systemd 语法，不能串起来执行。旧集群运维的起点应是**记录正在运行的版本与配置**，而不是换一份“一键安装脚本”。

![旧版 ZooKeeper 模式启动参考](assets/img-43dc445f5002b661.webp)

对于一个既有 ZooKeeper 模式集群，至少核对：每台 Broker 的 `broker.id` 唯一；`listeners` 为实际监听地址，`advertised.listeners` 能被客户端解析；`log.dirs` 对应原数据目录；`zookeeper.connect` 指向当前可用的 ZooKeeper 法定多数派。现代消费者组的位点主要存储在 Kafka 内部 `__consumer_offsets` Topic 中，不应再依据早期 `/consumers/...` 路径定位所有位点。先做配置与数据备份，变更时逐节点观察 ISR 和客户端读写。迁移到 KRaft 必须按**目标版本官方迁移流程**操作，绝不能把旧数据目录直接用于 `kafka-storage.sh format`。

![ZooKeeper 模式下 Broker 与元数据的历史界面](assets/img-434f253678ed468b.webp)

## 四、Kubernetes：让 Operator 管理生命周期

在 Kubernetes 中，Kafka 需要稳定网络身份、持久化卷、副本跨故障域放置与滚动升级协调。Strimzi Operator 可管理 Kafka 集群及部分配套对象，但其 Kafka 自定义资源、节点池和 KRaft 字段随 Operator 版本演进。旧截图中的 ZooKeeper/ephemeral YAML 既不能代表当前推荐架构，也不具备持久化能力，不应直接部署到生产。

![Strimzi Operator 集群示意](assets/img-bf2c2a708fd424ce.webp)

从 [Strimzi Quickstart](https://strimzi.io/quickstarts/)选择与目标 Kubernetes、Kafka 兼容的 Operator 版本，先安装 CRD，再选用该版本提供的 **KRaft + 持久卷**示例。创建后检查 Operator 日志、Kafka Pod、PVC、Listener 地址、Topic 副本与消费者读写；还需在存储、滚动升级和节点驱逐演练中验证恢复。部署说明应与实际安装的 Operator 版本一起保存，避免复制不同版本的 YAML 片段。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/17-kafka-roles-and-workflow.html' | relative_url }}">← 上一篇：Kafka 角色和流程</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/19-reading-and-writing-kafka-data.html' | relative_url }}">下一篇：Kafka 读写数据 →</a>
</nav>
