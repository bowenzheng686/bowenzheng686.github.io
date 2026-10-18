---
layout: default
title: "Redis 数据库 · 使用 CONFIG 动态修改配置"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 Redis 数据库目录]({{ '/subjects/Redis/' | relative_url }})

{% raw %}

# 06 使用 CONFIG 动态修改配置

`CONFIG GET` 查看**当前进程的生效值**，`CONFIG SET` 尝试在线修改支持动态调整的参数。它们属于管理操作，需要合适的 ACL 权限。不是所有配置都可在线修改；同一配置项在不同 Redis 版本中也可能改变行为。原文把这个过程统称“热加载”，容易误以为编辑配置文件会自动生效，实际上 Redis 并不会因文件改动就自动重新读取所有设置。

## 先查再改

下面以测试实例的 `maxmemory` 为例。正式修改前记录当前值、主机可用内存、数据集大小和持久化 fork 所需余量，不能因为机器有 8 GiB RAM 就无条件把 `maxmemory` 设为 8 GiB。

```text
CONFIG GET maxmemory
CONFIG SET maxmemory 1073741824
CONFIG GET maxmemory
```

这里的整数是字节数，`1073741824` 为 1 GiB。`CONFIG SET` 返回 `OK` 后新值对当前实例立即生效；若返回 immutable 或 unsupported，则此版本不支持在线调整该参数，应按文档修改文件并安排重启。**不要在读写高峰尝试动态修改 `port`、`bind` 等连接参数**，即使某些版本允许，也会影响已有和新建连接。

## 如何持久化修改

在线修改不一定写回启动配置文件。先用 `INFO server` 确认 `config_file`，再决定由哪个配置管理系统维护它。Redis 提供 `CONFIG REWRITE` 将可重写的当前配置写入启动配置文件，但要求文件存在且服务进程有写权限；包安装、容器挂载和自动化部署不一定允许这样做。若配置由 Ansible、Helm 或其他系统管理，直接 `CONFIG REWRITE` 还可能与下次部署相互覆盖。

```text
CONFIG GET maxmemory
CONFIG REWRITE
```

生产流程应记录变更、更新配置源、在可控窗口验证重启后仍生效，并准备回滚值。`CONFIG GET *` 会返回大量参数，其中可能包含敏感配置，不宜把完整结果贴到日志或文档中。

## 密码与版本差异

Redis 6 以后应优先用 ACL 管理用户和权限，而不是用 `CONFIG SET requirepass` 临时设置单个全局密码。后者可能使现有客户端在重连时失败，也会在命令历史中留下明文。原资料又用 `CONFIG GET requirepass` 展示密码，更不适合共享输出。

判断一个参数能否动态修改，以**当前实例返回的结果与对应版本文档**为准，而不是从旧截图推断“Redis 5 不支持、Redis 7 支持”。第 05 篇解释主要配置项，第 07 篇会用 `CONFIG GET` 检查慢日志阈值。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Redis/05-redis-configuration-files.html' | relative_url }}">← 上一篇：配置文件</a>
  <a href="{{ '/subjects/Redis/' | relative_url }}">返回 Redis 数据库目录</a>
  <a href="{{ '/subjects/Redis/07-slow-queries.html' | relative_url }}">下一篇：慢查询 →</a>
</nav>
