---
layout: default
title: "Redis 数据库 · 配置文件说明"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Redis 数据库目录]({{ '/subjects/Redis/' | relative_url }})

{% raw %}

# 05 配置文件说明

Redis 的配置文件决定监听、持久化、内存上限、复制与集群行为。启动时可通过 `redis-server /path/to/redis.conf` 指定文件；包安装与容器镜像的默认路径不同，先用 `INFO server` 的 `config_file` 字段确认**当前进程实际读取的文件**。配置项会随版本改变，本章按作用归类，不把旧版 `redis.conf` 的全部注释当成现行默认值。

![Redis 配置文件结构示意](assets/img-6709bda6922f6f4c.webp)

## 网络与进程

| 配置项 | 作用与注意点 |
| --- | --- |
| `bind`、`port` | 指定监听地址与端口。`bind 0.0.0.0` 会监听所有 IPv4 接口，不等于允许安全的远程访问。 |
| `protected-mode` | 防止某些未妥善配置的实例被远程直接访问；不是认证、TLS 或防火墙的替代品。 |
| `timeout`、`tcp-keepalive`、`tcp-backlog` | 分别涉及空闲客户端超时、TCP 保活和监听队列；调优时结合客户端连接特征和内核参数。 |
| `daemonize`、`supervised` | 由 systemd 管理时通常前台运行，并让 `supervised` 与 service 单元类型匹配。 |
| `loglevel`、`logfile`、`pidfile` | 决定日志与进程文件位置；目录权限要与服务用户一致。 |
| `databases` | 单机逻辑数据库数量；Redis Cluster 仅使用 DB 0。 |

本机测试可只监听环回地址：

```conf
bind 127.0.0.1
protected-mode yes
port 6379
daemonize no
supervised systemd
dir /var/lib/redis
```

这不是可以直接覆盖发行版完整配置文件的“万能模板”。启用远程访问时还需配置 ACL、TLS、网络隔离和访问控制。Redis 6 起支持 ACL 用户，不能再把所有认证都简化为 `requirepass` 一个全局密码。隐藏或重命名危险命令并不能代替 ACL，且可能影响客户端与运维工具。

## RDB 与 AOF 持久化

`save <秒数> <写入次数>` 指定在时间窗口内达到写入次数时触发 RDB 快照。`dbfilename` 与 `dir` 决定快照文件名和目录；目录必须能由 Redis 用户写入。是否启用默认快照、触发条件是什么，应查询当前配置而不是套用旧资料中的 `save 900 1` 等示例。

`stop-writes-on-bgsave-error yes` 会在 RDB 背景保存失败时阻止某些写入，以避免实例继续接受无法按预期持久化的数据。原资料一边提到磁盘满导致保存失败，一边建议生产环境统一改成 `no`，这会隐藏严重故障；是否改变应由业务的数据丢失容忍度决定。

`appendonly yes` 启用 AOF；`appendfsync` 的常见值为 `always`、`everysec` 与 `no`。`everysec` 在正常情况下约每秒同步一次，但异常故障时不能承诺严格只丢一秒；`no` 交由操作系统安排写盘，也不能简单保证“最多丢 30 秒”。`auto-aof-rewrite-*` 控制重写触发条件；新版本 AOF 可能由多个文件组成，不应只寻找单个 `appendonly.aof`。第 08 篇会进一步解释恢复顺序与故障边界。

## 内存与连接数

`maxclients` 限制客户端连接数量，同时受文件描述符上限影响。`maxmemory` 限制 Redis 纳入驱逐计算的内存，但复制缓冲、AOF 缓冲、进程开销等也占主机 RAM；不能机械设成“物理内存的一半”。应按数据集、持久化 fork 的额外内存、操作系统和同机进程预留余量。

达到 `maxmemory` 后，`maxmemory-policy` 决定如何处理新写入：

| 策略族 | 适用情形 |
| --- | --- |
| `noeviction` | 不驱逐键；可能让需要更多内存的写命令返回错误，适合不能悄然丢键的场景。 |
| `allkeys-lru`／`allkeys-lfu` | 允许在所有键中近似选取较少使用的键，常用于纯缓存。 |
| `volatile-*` | 只从设置过过期时间的键中选取；没有合适键时写入仍可能失败。 |

LRU、LFU 实现是近似策略；`volatile-ttl` 倾向选择较早过期的键。选择策略要先确定数据是缓存还是主数据，不能为了避免写入失败就无条件打开驱逐。

## 复制与 Sentinel

`replicaof` 指向主节点，旧版本曾用 `slaveof`；`masterauth`／ACL 凭据用于副本连接。`replica-read-only yes` 可防止普通客户端写副本，但不是数据完整性的唯一保证。

`repl-backlog-size` 决定主节点保留多少复制历史，影响断线后的部分重同步机会；应根据写入速率和期望可容忍的断线时间估算，不是“越大越好”。`repl-diskless-sync` 控制全量同步的数据传输方式，不同版本默认值和效率取舍会变化；不能一概推荐磁盘方式或说 socket 方式只能逐个副本传输。

`replica-serve-stale-data yes` 允许断开主节点的副本继续响应某些读请求，但可能返回旧数据；是否适合由应用的一致性要求决定。`replica-priority` 会影响 Sentinel 选主，值为 0 通常表示不参与自动提升。`min-replicas-to-write` 与 `min-replicas-max-lag` 可限制主节点在副本不足或滞后过大时接受写入，但**不提供同步复制或零数据丢失保证**。

## Cluster 与慢日志

Cluster 部署时，`cluster-enabled yes` 开启模式，`cluster-config-file` 是节点自动维护的状态文件，不应手工编辑；`cluster-node-timeout` 影响故障判断与转移时机。`cluster-require-full-coverage yes` 要求全部槽位可服务；设为 `no` 可以让健康槽位继续服务，但缺失槽位的键仍不可访问，应用必须处理部分失败。原资料直接推荐生产环境设为 `no`，忽略了业务对完整性的要求。

`slowlog-log-slower-than` 的单位是**微秒**，只计命令执行阶段，不包括网络收发；`slowlog-max-len` 控制内存中保存的记录条数。慢日志是定位高耗时命令的线索，不是请求全链路的耗时测量。设置为 `0` 会记录所有命令，负载高时需谨慎；第 07 篇会介绍如何阅读。

## 修改配置的基本流程

先记录当前值与版本，备份原配置，修改对应文件，检查启动参数与目录权限，再按维护窗口重启并验证：

```bash
redis-cli CONFIG GET maxmemory
redis-cli INFO server
systemctl cat redis-server.service
```

部分配置可通过 `CONFIG SET` 动态修改，但是否能持久化和是否允许在线改变取决于配置项及部署方式；第 06 篇专门讨论。不要在配置文件、运维文档或命令历史中放入真实密钥。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Redis/04-common-redis-commands.html' | relative_url }}">← 上一篇：常用命令</a>
  <a href="{{ '/subjects/Redis/' | relative_url }}">返回 Redis 数据库目录</a>
  <a href="{{ '/subjects/Redis/06-changing-configuration-dynamically-with-config.html' | relative_url }}">下一篇：动态配置 →</a>
</nav>
