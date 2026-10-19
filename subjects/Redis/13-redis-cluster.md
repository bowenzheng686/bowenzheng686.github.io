---
layout: default
title: "Redis 数据库 · Redis 集群"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Redis 数据库目录]({{ '/subjects/Redis/' | relative_url }})

{% raw %}

# 13 Redis 集群

前一篇的 Sentinel 能在单主节点故障后发现并切换主节点，但所有写入仍落在一个主节点上。Redis Cluster 则将键分散到多个主节点，既能横向分摊数据与写入，也能在主节点故障时由其副本接管。它并非 Sentinel 的简单升级：应用必须使用支持 Cluster 的客户端，跨键操作、事务和 Lua 脚本也会受到槽位约束。

![Redis 集群主题示意](assets/img-c587f78f05b602e1.webp)

## 先理解槽位，而不是先背部署命令

Cluster 固定使用 **16,384 个哈希槽**，编号为 0～16,383。每个主节点负责一部分槽，副本复制对应主节点的数据。默认情况下，键的槽号由 `CRC16(key) mod 16384` 得到；键中若有合法的 `{...}` 哈希标签，则只对花括号内的内容计算槽号。例如 `cart:{u42}` 与 `profile:{u42}` 会落入同一槽，可用于确需多键原子操作的场景，但大量键共用标签也可能形成热点。

![多主节点与副本的拓扑](assets/img-238634b7c065c377.webp)

![三主节点的槽位划分](assets/img-36204838a010db45.webp)

三主节点平均分配时，区间可以是 `0–5460`、`5461–10922` 和 `10923–16383`。**槽数接近不代表负载接近**：每槽的键数、键大小和请求量都可能不同。新增主节点也不会自动分得槽；只有把槽和槽内数据一起迁过去，它才真正承担业务流量。

![从单机存储过渡到分区](assets/img-0f2b3b2cfd60f8f6.webp)

![不同分区方式示意](assets/img-93149fd4df49f34a.webp)

![键到哈希槽的映射](assets/img-163f9d8b4e3d0f98.webp)

客户端可以连接任意可达节点，但应使用 **Cluster-aware 客户端**。当请求落在别的主节点的槽上，服务器返回 `MOVED`，客户端更新槽位映射并重发；迁槽期间可能返回 `ASK`，客户端应先向目标节点发送 `ASKING` 再处理本次请求。节点之间通过集群总线交换拓扑与故障信息。网络变化、故障或连续迁槽时可能多次重试，原资料所谓“最多两次命中”不是可靠的延迟保证。

![集群节点传播拓扑信息](assets/img-8af7152a8b67a3cb.webp)

![加入节点与槽位迁移](assets/img-ead962122666f365.webp)

### 故障判断与可用性

节点之间探测到某个主节点不可达，先把它标为疑似故障（`PFAIL`）；当足够多的持槽主节点报告故障后，才形成 `FAIL`。符合条件的副本通过选举取得多数持槽主节点授权后接管槽位，向其他节点传播新拓扑。副本是否有资格参选还受复制状态、断线时长及配置影响。故障期间仍可能出现短暂请求失败或最近一次异步复制尚未完成的数据丢失；Cluster 不是强一致复制。

![主观故障检测](assets/img-6b5c5c5f504851e3.webp)

![故障报告汇聚](assets/img-60dcc8371a2dc286.webp)

![副本参选示意](assets/img-8d0f691d21f623be.webp)

![主节点授权选举](assets/img-8ba71408a0a1197b.webp)

![新主节点接管槽位](assets/img-ae0c8e3ceca9d740.webp)

常见起点是 **三主三从，分布在至少三个故障域**，并让每个主节点的副本与它不在同一故障域。三主只是方便形成多数的起点，不是“只要半数主节点在线便能访问所有数据”。还要看每个槽是否由可用主节点覆盖、故障主节点是否存在合格副本、主节点多数是否能投票，以及 `cluster-require-full-coverage` 的设置。默认要求槽位完整覆盖；将它设为 `no` 只会允许部分可用槽继续服务，**不会让缺失槽的数据变得可读**，应用必须能处理局部失败。

## 部署：以 Redis 5 及之后版本的工具为主

![六节点跨故障域部署](assets/img-36892c150a7b7fd6.webp)

以下使用六个彼此可达、尚未加入其他集群的 Redis 实例示意：三个主节点及各自一个副本。可以在三台主机各运行两个实例做功能验证；生产环境应按故障域、容量和资源隔离要求部署，避免一台宿主机故障同时带走互为主从的两个实例。加入集群的节点应为空，迁移已有业务数据须走专门流程，不能通过 `FLUSHALL` 清空在线数据来消除创建错误。

![三机六实例的测试布局](assets/img-36892c150a7b7fd6.webp)

先核对所有实例的 Redis 版本、持久化、ACL/TLS、内存限制、时间同步、端口和网络。集群总线端口默认是客户端端口加 10000，例如 `6379` 对应 `16379`；两类端口都要在**节点之间**可达，而非暴露到公网。使用 `cluster-announce-ip` 等配置确保节点发布的是其他节点与客户端可达的地址，尤其在容器或 NAT 环境中。

每个实例至少启用集群模式，并使用**本实例独立**的数据目录和 `cluster-config-file`；该文件由 Redis 自动维护，不应人工复制同一个节点 ID 到其他实例。

```conf
port 6379
cluster-enabled yes
cluster-config-file nodes-6379.conf
cluster-node-timeout 5000
appendonly yes
dir /var/lib/redis/6379
```

此处省略了部署环境必需的访问控制、绑定地址、TLS、服务单元和资源限制。不要把原文中 `bind 0.0.0.0`、关闭保护模式、固定示例密码当作默认配置；按实际网络和密钥管理方式设置。先逐一确认六个空实例可以启动并相互通信，再执行创建：

```bash
redis-cli --cluster create \
  10.0.0.8:6379 10.0.0.18:6379 10.0.0.28:6379 \
  10.0.0.38:6379 10.0.0.48:6379 10.0.0.58:6379 \
  --cluster-replicas 1
redis-cli --cluster check 10.0.0.8:6379
redis-cli -h 10.0.0.8 -p 6379 CLUSTER INFO
redis-cli -h 10.0.0.8 -p 6379 CLUSTER NODES
```

若启用了认证/TLS，请给 `redis-cli` 提供对应用户、密码和 TLS 参数；密码可由环境或受控配置传入，避免写入共享脚本和终端历史。创建工具会显示拟议的主从映射与槽位分配，确认**主从没有落在同一故障域**后再接受。成功标志不是命令返回零，而是 `cluster_state:ok`、16,384 个槽完整覆盖、三个主节点分别有在线副本，且各节点视图一致。

### 写入、重定向与应用连接

```bash
redis-cli -c -h 10.0.0.8 -p 6379 SET demo:cluster ok
redis-cli -c -h 10.0.0.8 -p 6379 GET demo:cluster
redis-cli -h 10.0.0.8 -p 6379 CLUSTER KEYSLOT demo:cluster
```

`-c` 会按重定向继续执行；不加 `-c` 时可能直接看到 `MOVED`，这不是数据丢失。需要在应用侧配置多个种子地址、连接超时与重试，而不是把一个节点地址当作永久入口。以当前 `redis` Python 包为例：

```python
import os
from redis.cluster import RedisCluster

client = RedisCluster(
    host="10.0.0.8",
    port=6379,
    username=os.getenv("REDIS_USER") or None,
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True,
    socket_connect_timeout=2,
)
client.set("demo:cluster", "ok", ex=60)
assert client.get("demo:cluster") == "ok"
```

不同 `redis-py` 版本的 Cluster 初始化参数有差异，实际安装版本应先在预发布环境验证；多种子节点、TLS 与认证按客户端版本配置。旧文的 `redis-py-cluster` 示例属于历史 API，且循环体缩进损坏，不能直接复制执行。

在受控演练中停止某个主节点后，应观察 `CLUSTER NODES` 中副本升主、槽位仍完整、客户端重试后读写恢复；启动旧主节点后再确认其变成副本并完成同步。不要以停止整台主机上所有 Redis 进程的方式验证单节点故障。

## Redis 4 旧版案例如何阅读

![Redis 4 三机六实例旧版截图](assets/img-43f8db6ac40de529.webp)

Redis 3/4 使用 Ruby 脚本 `redis-trib.rb` 管理集群，Redis 5 起相应能力整合进 `redis-cli --cluster`。原资料中的 Ruby 2.5 编译、`gem install redis`、修改 gem 源码注入密码等步骤，只说明**当时**为何使用旧工具，不适用于当前部署。尤其不要为运行管理工具而修改已安装库代码或降低集群认证要求。

![旧版 Ruby 客户端认证修改截图](assets/img-ea2dd32ec8a80289.webp)

若必须维护 Redis 4，先确认具体小版本和官方工具帮助，再在隔离环境用 `redis-trib.rb create --replicas 1 ...`、`check`、`reshard` 等命令演练，并保留完整备份。旧版终端输出里的固定地址、密码、`FLUSHALL`、`CLUSTER RESET` 仅是历史记录，不能当作线上修复步骤；清空或重置节点会破坏现有数据和集群身份。

## 扩容：加节点之后还要迁槽

![扩容后的主从拓扑](assets/img-95c4fdf827c06b44.webp)

![扩容时槽位和键一同迁移](assets/img-1774220abb4ab9cc.webp)

扩容前先确认剩余容量、备份可恢复、当前没有未完成的迁槽或故障、客户端能处理 `ASK`/`MOVED`。新节点采用兼容配置、空数据目录并与集群双向可达。添加一个主节点与一个副本时，按顺序操作：

```bash
redis-cli --cluster check 10.0.0.8:6379
redis-cli --cluster add-node 10.0.0.68:6379 10.0.0.8:6379
redis-cli -h 10.0.0.8 -p 6379 CLUSTER NODES
redis-cli --cluster reshard 10.0.0.8:6379
redis-cli --cluster check 10.0.0.8:6379
```

刚加入的主节点通常是 **0 槽、0 键**。`reshard` 中指定新主节点 ID 为接收方，从原主节点选择迁出的槽，并审阅迁移计划。三主扩为四主时，为平均分配可考虑给新节点约 4096 槽，但真实计划还要看键大小、热度和目标容量。迁移过程中工具会移动槽内的键并更新所有权；要持续监测请求错误、延迟、复制延迟和剩余内存。原文称“旧版本迁槽必须先清空数据”并不准确，不能据此清库。

从 `CLUSTER NODES` 取得**新主节点 ID** 后再添加副本：

```bash
redis-cli --cluster add-node 10.0.0.78:6379 10.0.0.8:6379 \
  --cluster-slave --cluster-master-id 新主节点ID
redis-cli --cluster check 10.0.0.8:6379
```

新副本应与新主节点处在不同故障域，且复制状态在线。若它已经作为空主节点加入，先确认其没有槽和数据，再在该节点执行 `CLUSTER REPLICATE 新主节点ID`。最后检查 16,384 槽无缺口、每个主节点都有预期副本、业务键可读写；不要只看节点数增长。

## 缩容：先迁出数据，再移除节点

![缩容前的槽位迁出](assets/img-1c5799cdad300b1a.webp)

待删除主节点只要还拥有槽，就不能直接退出。先算清其他主节点的内存、QPS 与副本承载能力，再把该主节点负责的**全部槽及槽内键**迁给其他主节点。迁槽源节点有数据是正常的；原资料所说“源服务器必须没有数据，否则迁移报错”颠倒了前提。可以分批 `reshard` 到多个接收节点，每批后检查状态：

```bash
redis-cli --cluster check 10.0.0.8:6379
redis-cli --cluster reshard 10.0.0.8:6379
redis-cli --cluster check 10.0.0.8:6379
redis-cli -h 10.0.0.8 -p 6379 CLUSTER NODES
```

只有确认待删主节点 **0 槽、0 键**，全体槽仍完整、业务数据及副本关系正常，才用 `redis-cli --cluster del-node 10.0.0.8:6379 待删节点ID` 移除。若还要移除其副本，先核对它当前究竟跟随哪个主节点，并确保留下的主节点仍有足够副本；再按副本 ID 移除。Redis 可能自动重配副本，不能只按旧拓扑假定关系未变。删除节点后备份其数据与配置，确认不再有应用连接，再回收服务；不要随手删除仍可能需要的 `nodes.conf`。

缩容不是原操作的简单逆命令。发生迁槽中断时，先保留现状并检查开放槽、多个所有者、键归属和业务读写；评估后再使用修复工具，不能无条件运行 `--cluster fix` 或 `CLUSTER FORGET`。可回退到迁槽前备份和拓扑，或把槽与数据迁回，但每一步都必须重新核对数据。

## 从独立 Redis 导入已有数据

`redis-cli --cluster import` 可以把独立实例的键按目标槽导入集群，适合**经过验证的迁移窗口**，不是无感在线同步。先盘点源库键量、TTL、数据类型、键冲突、写入速率和停机窗口；准备可恢复备份，并决定迁移期间是冻结写入、双写还是通过其他工具做增量同步。Cluster 只支持 DB 0，其他逻辑库需先处理；导入后用样本键、键数、TTL 与业务读写核对，而不是仅在某个主节点执行 `KEYS *`。

```bash
redis-cli --cluster import 10.0.0.8:6379 \
  --cluster-from 10.0.0.78:6379 --cluster-copy
```

`--cluster-copy` 保留源数据；是否再加 `--cluster-replace` 取决于明确的冲突策略，不能默认覆盖目标业务键。`redis-cli` 的认证与源、目标认证兼容性依版本而异，先查当前版本帮助并在同配置环境试迁。**不需要把全部源节点和集群节点的密码、保护模式关闭**；原资料的这项建议会扩大暴露面。若工具不能满足认证、TLS 或增量迁移需求，应选择支持这些能力的迁移方案，而不是降低访问控制。

![旧版导入示例截图](assets/img-2ecb592d401d4a98.webp)

## 负载偏斜：先找原因，再决定是否平衡槽位

`--cluster info` 和 `--cluster check` 能看槽数与键数，`INFO memory`、`INFO commandstats`、延迟和客户端指标能看资源与请求负载。槽数均匀但内存不均时，优先排查大键、TTL 差异和数据结构；QPS 不均时，检查热点键与 hash tag 是否把大量请求压进同一槽。`--cluster rebalance` 主要调整槽位分配，**不能自动拆开单个热点键**。

```bash
redis-cli -h 10.0.0.8 -p 6379 CLUSTER KEYSLOT 'cart:{u42}'
redis-cli -h 对应主节点 -p 6379 CLUSTER COUNTKEYSINSLOT 槽号
redis-cli --cluster rebalance 10.0.0.8:6379 --cluster-simulate
```

先用模拟结果审阅迁移量和目标，再决定是否在低峰实施。`--bigkeys` 按连接到的**单个节点**扫描，并不能一次覆盖全体集群节点；宜分节点执行并控制扫描速率。大键可考虑拆分、分页或变更数据模型；热键可结合本地缓存、请求合并或业务层分流处理，但须审视一致性语义。

## 局限与选型

Cluster 只使用 DB 0。多键命令、事务和 Lua 脚本涉及的键必须能在同一槽处理，例如 `MGET key1 key2` 若跨槽会报 `CROSSSLOT`；合理的 hash tag 可以让相关键同槽，但过度使用又会导致偏斜。`SCAN`、`KEYS` 等是节点局部视角，需要按主节点分别处理。副本默认不承接常规读请求；客户端可发送 `READONLY` 从副本读取其对应槽的数据，但须接受复制延迟并处理拓扑变化，不能把它理解为自动、强一致的读写分离。

若单主节点容量与吞吐足够，目标只是自动故障转移，主从加 Sentinel 的应用复杂度通常更低。若需要跨多个主节点分摊数据或写入，再选择 Cluster，并把客户端兼容、键设计、故障域、扩缩容和监控一起纳入设计。不要因为“集群”二字就默认它总比单机或 Sentinel 更可靠。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Redis/12-redis-sentinel.html' | relative_url }}">← 上一篇：Sentinel 哨兵</a>
  <a href="{{ '/subjects/Redis/' | relative_url }}">返回 Redis 数据库目录</a>
  <a href="{{ '/subjects/Redis/14-common-interview-questions.html' | relative_url }}">下一篇：常见面试题 →</a>
</nav>
