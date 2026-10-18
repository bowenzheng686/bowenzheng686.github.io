---
layout: default
title: "Redis 数据库 · config 命令实现动态修改配置（热加载）"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Redis 数据库目录]({{ '/subjects/Redis/' | relative_url }})

{% raw %}

# 06 config 命令实现动态修改配置（热加载）
### 2.3 config 命令实现动态修改配置（热加载）

config 命令用于查看当前redis配置、以及不重启redis服务实现动态更改redis配置等

注意：不是所有配置都可以动态修改,且此方式无法持久保存

```text
CONFIG SET parameter value
时间复杂度：O(1)
CONFIG SET 命令可以动态地调整 Redis 服务器的配置(configuration)而无须重启。
可以使用它修改配置参数，或者改变 Redis 的持久化(Persistence)方式。
CONFIG SET 可以修改的配置参数可以使用命令 CONFIG GET * 来列出，所有被 CONFIG SET 修改的配
置参数都会立即生效。
CONFIG GET parameter
时间复杂度： O(N)，其中 N 为命令返回的配置选项数量。
CONFIG GET 命令用于取得运行中的 Redis 服务器的配置参数(configuration parameters)，在
Redis 2.4 版本中， 有部分参数没有办法用 CONFIG GET 访问，但是在最新的 Redis 2.6 版本中，所
有配置参数都已经可以用 CONFIG GET 访问了。
CONFIG GET 接受单个参数 parameter 作为搜索关键字，查找所有匹配的配置参数，其中参数和值以“键-
值对”(key-value pairs)的方式排列。
比如执行 CONFIG GET s* 命令，服务器就会返回所有以 s 开头的配置参数及参数的值：
```

范例：版本差异

```text
#redis-7支持动态修改端口
127.0.0.1:6379> config set port 8888
OK
#redis-7 不支持动态修改日志文件路径
127.0.0.1:6379> config set logfile /tmp/redis.log
(error) ERR CONFIG SET failed (possibly related to argument 'logfile') - can't
set immutable config
```

```text
#redis-5不支持动态修改端口
127.0.0.1:6379> config set port 8888
(error) ERR Unsupported CONFIG parameter: port
```

### 设置客户端连接密码

```text
#设置连接密码
127.0.0.1:6379> CONFIG SET requirepass 123456
OK
#查看连接密码
127.0.0.1:6379> CONFIG GET requirepass
1) "requirepass"
2) "123456"
```

### 获取当前配置

```text
#奇数行为键，偶数行为值
127.0.0.1:6379> CONFIG GET *
1) "dbfilename"
2) "dump.rdb"
3) "requirepass"
4) ""
5) "masterauth"
6) ""
7) "cluster-announce-ip"
8) ""
9) "unixsocket"
10) ""
11) "logfile"
12) "/var/log/redis/redis.log"
13) "pidfile"
14) "/var/run/redis_6379.pid"
15) "slave-announce-ip"
16) ""
17) "replica-announce-ip"
18) ""
19) "maxmemory"
20) "0"
......
#查看bind
127.0.0.1:6379> CONFIG GET bind
1) "bind"
2) "0.0.0.0"
#Redis5.0有些设置无法修改,Redis6.2.6版本支持修改bind
127.0.0.1:6379> CONFIG SET bind 127.0.0.1
(error) ERR Unsupported CONFIG parameter: bind
```

### 设置 Redis 使用的最大内存量

```text
127.0.0.1:6379> CONFIG SET maxmemory 8589934592 或 1g|G # 默认以字节为单位,1G以10的n
次
127.0.0.1:6379> CONFIG GET maxmemory
1) "maxmemory"
2) "8589934592"
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Redis/05-redis-configuration-files.html' | relative_url }}">← Previous: Redis Configuration Files</a>
  <a href="{{ '/subjects/Redis/' | relative_url }}">Back to Redis Database Index</a>
  <a href="{{ '/subjects/Redis/07-slow-queries.html' | relative_url }}">Next: Slow Queries →</a>
</nav>
