---
layout: default
title: "微服务架构 · ZooKeeper 客户端访问"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 12 ZooKeeper 客户端访问

上一章已经部署 ZooKeeper。本篇从同一个 `/demo` 节点出发，分别用命令行观察数据、用四字命令检查服务状态，再看图形工具和程序客户端。连接地址、认证方式和 ACL 都要与目标集群保持一致；不要把不同版本终端记录中的提示符和输出当作待执行命令。

## `zkCli.sh`：先掌握节点生命周期

连接字符串可以列出多个节点，客户端会在可用成员之间重连。以下交互命令是在 `zkCli.sh` 提示符内输入的，不是在 Linux shell 中执行。

```bash
/opt/zookeeper/bin/zkCli.sh -server 10.0.0.101:2181,10.0.0.102:2181,10.0.0.103:2181
```

```text
ls /
create /demo "hello"
get /demo
stat /demo
set /demo "updated"
get /demo
delete /demo
quit
```

`create` 默认创建持久节点；`create -e` 创建与当前会话绑定的临时节点，会话过期后自动删除，不能在临时节点下再建子节点。`get` 读取数据，`stat` 查看节点版本、时间和子节点数量。`set` 与 `delete` 在多人并发修改时应带上读取到的版本号，避免覆盖其他客户端的更新；具体参数以当前版本 `help` 为准。`delete` 只删除没有子节点的节点，`deleteall` 会递归删除，执行前要确认路径和业务影响。

## 四字命令：诊断服务器，而不是读写业务数据

四字命令通过客户端端口查询服务状态，例如 `ruok`、`stat`、`mntr`、`conf`。它们并非任意版本都默认可用；某些命令可能披露连接和环境信息或修改状态，**不要将 `4lw.commands.whitelist=*` 作为通用解决办法**。在受限管理网络内，仅为所需命令设置白名单，并按版本文档核对语义。

```properties
# 写在每台服务器的 zoo.cfg 中，变更后按部署方式重启
4lw.commands.whitelist=ruok,stat,mntr
```

```bash
printf ruok | nc 127.0.0.1 2181
printf stat | nc 127.0.0.1 2181
printf mntr | nc 127.0.0.1 2181
```

`ruok` 返回 `imok` 只能证明进程对该命令有响应，不能独自证明节点拥有法定多数、能够处理写入。还应检查 `zkServer.sh status`、客户端读写和集群告警。如果出现 `not in the whitelist`，先检查当前版本和白名单配置，避免直接开放全部运维命令。

## 图形工具：把旧截图当作界面参考

ZooInspector 可浏览 znode 层级、查看值并编辑节点。原课件截图依次展示连接、浏览、编辑与删除过程；操作前先确认连接的是测试环境，特别是删除操作。

![连接参数界面](assets/img-2bdc34c390a8d905.webp)

![节点浏览界面](assets/img-8a0d2664941409a6.webp)

![节点数据编辑界面](assets/img-acc160a270882f26.webp)

![删除操作示意](assets/img-8894f435d6cdcdd8.webp)

ZooInspector 的部分社区构建已久未维护，课件中的 Java 8、Maven 镜像和 Windows 包路径不应直接照搬到当前系统。若确实需要此工具，可查其[源码与构建说明](https://github.com/zzhang5/zooinspector)，在隔离环境核对来源、Java 兼容性和依赖后构建；日常诊断优先用 `zkCli.sh` 和指标。图形界面也不会绕过服务端 ACL。

## Python：显式连接与关闭

Kazoo 是 ZooKeeper 的 Python 客户端。以下示例在测试路径创建、读取并删除节点，`finally` 保证连接关闭。真实应用应处理连接状态、会话过期、节点已存在及版本冲突；不要在生产根路径上运行演示程序。

```bash
python3 -m pip install kazoo
```

```python
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError

zk = KazooClient(hosts="10.0.0.101:2181,10.0.0.102:2181,10.0.0.103:2181")
zk.start(timeout=10)
try:
    zk.ensure_path("/demo")
    path = "/demo/python-example"
    try:
        zk.create(path, b"hello")
    except NodeExistsError:
        pass
    data, stat = zk.get(path)
    print(data.decode(), stat.version)
    zk.delete(path, version=stat.version)
finally:
    zk.stop()
    zk.close()
```

`version=stat.version` 使删除成为条件操作；如果其他客户端已修改数据，删除会失败，调用方应重新读取并决定是否重试。`ensure_path` 创建的是持久父节点，本示例只删除叶节点。

## Go：同样遵守版本与 ACL 约束

使用 [go-zookeeper/zk](https://github.com/go-zookeeper/zk) 时，`Create` 的 flags 为 `0` 表示持久节点；`Get` 返回的 `Stat.Version` 可用于条件更新和删除。下面使用开放 ACL 只为了本地隔离试验，线上应配置与服务身份匹配的 ACL。

```go
package main

import (
    "fmt"
    "log"
    "time"

    "github.com/go-zookeeper/zk"
)

func main() {
    conn, events, err := zk.Connect([]string{"127.0.0.1:2181"}, 5*time.Second)
    if err != nil { log.Fatal(err) }
    defer conn.Close()

    timeout := time.NewTimer(10 * time.Second)
    defer timeout.Stop()
    for conn.State() != zk.StateConnected && conn.State() != zk.StateHasSession {
        select {
        case event := <-events:
            if event.State == zk.StateConnected || event.State == zk.StateHasSession { break }
        case <-timeout.C:
            log.Fatal("ZooKeeper 连接超时")
        }
    }

    path := "/go-example"
    _, err = conn.Create(path, []byte("hello"), 0, zk.WorldACL(zk.PermAll))
    if err != nil { log.Fatal(err) }
    data, stat, err := conn.Get(path)
    if err != nil { log.Fatal(err) }
    fmt.Printf("%s: %s\n", path, data)
    if err := conn.Delete(path, stat.Version); err != nil { log.Fatal(err) }
}
```

重复运行这个最小示例会遇到节点已存在；在实际程序里应显式处理 `ErrNodeExists`，而不是盲目覆盖。客户端语言不同，但共同的责任不变：正确设置连接超时和身份、处理会话变化、使用版本号控制并发，并在测试后清理节点。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/11-installing-zookeeper.html' | relative_url }}">← 上一篇：ZooKeeper 安装</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/13-introduction-to-message-queues.html' | relative_url }}">下一篇：消息队列简介 →</a>
</nav>
