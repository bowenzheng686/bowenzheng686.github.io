---
layout: default
title: "ELK 日志分析 · Elasticsearch 插件"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 09 Elasticsearch 插件
本章介绍 Head 与 Cerebro 这两种**独立运行的集群可视化工具**，不是 Elasticsearch 进程内安装的插件。它们便于观察节点、索引与分片，但生产监控不能只依赖界面颜色：还需看预期节点数、未分配分片、磁盘水位与写入错误。对于较新的 Elasticsearch，也可优先使用 Kibana 的 Stack Monitoring 和索引管理功能。

先理解集群健康状态，才能读懂后面的截图：

| 状态 | 分片含义 | 排查重点 |
| --- | --- | --- |
| green | 所有主分片、副本分片均已分配 | 再核对预期节点数和资源使用情况。 |
| yellow | 主分片均已分配，但至少一个副本分片未分配 | 数据通常仍可读取，但冗余不足；单节点集群配置副本时也可能长期呈 yellow。 |
| red | 至少一个主分片未分配 | 部分索引可能不可读写，**不等于已经确认数据永久丢失**；应立即查找未分配原因并检查快照。 |

可先执行 `GET /_cluster/health` 与 `GET /_cat/shards?v` 定位问题；“green”也不保证每个预期节点都在线，因此还要核对 `number_of_nodes`。

### Head 插件

### Head 介绍

Head 是较早期的社区工具，后续维护和与新版 Elasticsearch 的兼容性有限。以下截图及安装方法保留为旧环境示例；不要把它作为现代集群的默认管理入口，尤其不要把集群管理接口暴露给公网。

git地址：https://github.com/mobz/elasticsearch-head

![ELK 日志分析第 84 页插图](assets/img-2469bb5ef41e63ed.webp)

它可作为独立 Node.js 服务、Docker 容器或浏览器扩展运行。三者都是连接 Elasticsearch HTTP API，而非装入 Elasticsearch 进程。

### 独立服务方式运行 Head

当浏览器页面与 Elasticsearch API 不同源时，才需要考虑 CORS；浏览器扩展是否需要 CORS 取决于其实现。**不要直接在生产集群启用任意来源访问。**仅在隔离的演示环境中可用下面的宽松配置；真实环境应限制来源，并结合认证、TLS 与网络边界。

官方文档:

<https://www.elastic.co/guide/en/elasticsearch/reference/6.8/modules-http.html>

范例:

```bash
[root@es-node1 ~]# vim /etc/elasticsearch/elasticsearch.yml
#在文件最后添加下面两行
http.cors.enabled: true      #开启支持跨域访问
http.cors.allow-origin: "*"   #指定允许访问范围
[root@es-node1 ~]# systemctl restart elasticsearch
```

2.5.1.2.2 服务方式启动

在elasticsearch 5.x版本以后不再支持直接安装head插件，而是通过服务启动

此安装方式通过 npm 工具实现

npm(Node Package Manager)是和NodeJS一起安装的包管理和分发工具，使用npm 可以很方便让 JavaScript开发者下载、安装、上传以及管理已经安装的相关包。

以下是旧版环境中的构建流程。先确认项目所需 Node.js 版本；旧教程里的 `git://`、已迁移的镜像地址和把 `npm run start &` 当作长期服务的做法都不宜照搬。

```bash
sudo yum install -y npm git
git clone https://github.com/mobz/elasticsearch-head.git
cd elasticsearch-head
npm install
npm run start
```

Ubuntu 上只需把第一条安装命令换为 `sudo apt install -y npm git`，其余流程相同。安装失败时先检查 Node.js 与依赖版本，而不是反复切换不可信的 npm 镜像。

服务默认在 9100 端口提供页面，应仅允许管理端访问；若需要长期运行，请配置进程管理器，而非依赖终端后台任务。

### Docker 方式启动 Head 插件

```bash
docker run -d --name head -p 127.0.0.1:9100:9100 mobz/elasticsearch-head:5
```

浏览器访问 `http://127.0.0.1:9100`。此镜像属于旧社区项目，部署前应检查镜像来源、标签和与目标 Elasticsearch 版本的兼容性；上面的端口仅绑定本机。

![ELK 日志分析第 86 页插图](assets/img-87d3133664fb4698.webp)

### 浏览器安装插件

#### 在线安装（旧版浏览器示例）

从谷歌应用商店下载安装插件,支持chrome和edge浏览器

在浏览器扩展商店搜索并核对扩展发布者、权限及最近更新时间。扩展将访问集群管理 API，不应随意授予来源不明的扩展读取权限。下列链接和截图为原教程记录的入口，商店页面可能变化。

<https://chrome.google.com/webstore/category/extensions?hl=en-US>

<https://chrome.google.com/webstore/detail/multi-elasticsearch-head/cpmmilfkofbeimbmgiclohpodggeheim?hl=en-US>

<https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm/related>

![ELK 日志分析第 87 页插图](assets/img-f0a027496cfe5a9e.webp)

![ELK 日志分析第 87 页插图](assets/img-3084b3c33c5ddfbd.webp)

![ELK 日志分析第 88 页插图](assets/img-90cbcb3b97248ae1.webp)

![ELK 日志分析第 88 页插图](assets/img-36b814a1f2e9eba3.webp)

安装完插件,点击图标就可以打开插件

![ELK 日志分析第 89 页插图](assets/img-ea90ca645e9e2535.webp)

#### 离线安装（旧版浏览器示例）

只有可信来源的扩展包才应通过开发者模式加载；离线安装不解决扩展与 Elasticsearch 新版 API 的兼容问题。下面的连续截图展示进入扩展管理页、启用开发者模式与加载扩展的过程。

![ELK 日志分析第 89 页插图](assets/img-4eef921a7628415f.webp)

![ELK 日志分析第 89 页插图](assets/img-349b05ba27245b3c.webp)

![ELK 日志分析第 90 页插图](assets/img-39e24dc7097fc4dc.webp)

![ELK 日志分析第 90 页插图](assets/img-946b2423379116f1.webp)

![ELK 日志分析第 90 页插图](assets/img-2f55b2ba0b3bb5ce.webp)

![ELK 日志分析第 90 页插图](assets/img-9be08d1c628b70dd.webp)

### 利用 Head 插件观察状态

Head 中的绿色、黄色、红色对应前述健康状态；紫色是该工具表现分片迁移或恢复中的过渡颜色，并非 Elasticsearch 健康 API 的第四种状态。图中数字表示分片编号；粗框与细框用于区分主、副分片，星形标出当时的主节点。界面标记需结合 `_cat/shards` 等 API 核实，不能只凭颜色断定是否发生永久数据丢失。

![ELK 日志分析第 91 页插图](assets/img-608abbfcc49e9a68.webp)

以下连续截图观察创建索引后的分片分布，以及节点停止和恢复时的变化。停止节点会影响可用性，操作前应确认这是隔离实验集群；生产环境应先检查副本、快照与维护窗口。

![ELK 日志分析第 91 页插图](assets/img-863e07c20f50e13b.webp)

![ELK 日志分析第 91 页插图](assets/img-c94f706a6012c592.webp)

![ELK 日志分析第 92 页插图](assets/img-4cae311f84dce1f0.webp)

![ELK 日志分析第 92 页插图](assets/img-9616cc2bf39464b5.webp)

![ELK 日志分析第 92 页插图](assets/img-e115e01f8b2dc129.webp)

![ELK 日志分析第 93 页插图](assets/img-b86db6d6966fd6d3.webp)

```bash
[root@node3 ~]#systemctl stop  elasticsearch.service
```

![ELK 日志分析第 93 页插图](assets/img-a93650aad66fd9bf.webp)

```bash
[root@node3 ~]#systemctl start  elasticsearch.service
```

![ELK 日志分析第 93 页插图](assets/img-da31e6ae81cdb345.webp)

节点恢复时可能短暂出现紫色迁移状态，应持续观察直到分片分配结束。

![ELK 日志分析第 94 页插图](assets/img-94358e4718777b2d.webp)

`index2` 是索引而非数据库；截图中展示其 2 个主分片与 3 个副本的设置。若集群节点数不足以容纳各副本，健康状态会持续为 yellow。

![ELK 日志分析第 94 页插图](assets/img-89d5cf7d7babe318.webp)

### Cerebro 插件

### Cerebro 介绍

![ELK 日志分析第 94 页插图](assets/img-e2ee5fd51f192732.webp)

Cerebro 是独立运行的 Elasticsearch 集群 Web 管理程序，可集中查看节点、索引和分片。原教程以 v0.9.4 为例，**“2021 年最新版本”只反映写作当时，不代表现在**。安装前核对项目发布页中的当前版本、Java 要求及 Elasticsearch 兼容范围。

github链接：

<https://github.com/lmenezes/cerebro>

![ELK 日志分析第 95 页插图](assets/img-a6caee2590807819.webp)

### 包安装

包安装示例以 v0.9.4 为历史参考，目标机器需预留 Java 进程可用内存。以下命令保留关键流程，并修正原文被换行截断的下载地址；实际版本与校验信息以发布页为准。

```bash
sudo apt update && sudo apt install -y openjdk-11-jre-headless
wget https://github.com/lmenezes/cerebro/releases/download/v0.9.4/cerebro_0.9.4_all.deb
sudo dpkg -i cerebro_0.9.4_all.deb
sudo systemctl start cerebro
sudo systemctl status cerebro
sudo journalctl -u cerebro -n 50 --no-pager
```

如果日志出现 `opening db: './cerebro.db': 权限不够`，检查 `/etc/cerebro/application.conf` 中 `data.path` 是否指向服务用户可写的目录（例如 `/var/lib/cerebro/cerebro.db`），并核对目录属主，再重启服务。先看日志确认故障，不能认为所有包安装都一定失败。默认 Web 端口为 9000；管理界面应限制访问来源，连接受认证保护的 Elasticsearch 时还需配置对应凭据。

![ELK 日志分析第 96 页插图](assets/img-4af0c49dbc990049.webp)

单节点ES显示如下

![ELK 日志分析第 97 页插图](assets/img-2242213160d0f100.webp)

显示特殊索引

![ELK 日志分析第 97 页插图](assets/img-a040bbbb5c6f8da7.webp)

![ELK 日志分析第 97 页插图](assets/img-95de6799bcd5fda2.webp)

三节点集群显示如下，实心的五角星表示Master节点

![ELK 日志分析第 98 页插图](assets/img-6e03b16a5aafa37a.webp)

如果数据丢失，会显示红色

![ELK 日志分析第 98 页插图](assets/img-8b85ffe0f052cced.webp)

### 二进制安装

压缩包安装适合不使用 DEB/RPM 包的环境。原文把 v0.9.4 的下载命令与 v0.9.3 的解压命令混在一起，下面统一以 v0.9.4 演示；先检查发布页的 Java 要求。

```bash
wget https://github.com/lmenezes/cerebro/releases/download/v0.9.4/cerebro-0.9.4.tgz
sudo tar -xzf cerebro-0.9.4.tgz -C /usr/local/
sudo ln -s /usr/local/cerebro-0.9.4 /usr/local/cerebro
/usr/local/cerebro/bin/cerebro
```

若要预设连接地址，在 `/usr/local/cerebro/conf/application.conf` 的 `hosts` 列表中填写 Elasticsearch HTTP 地址和显示名称；有认证时还需配置相应凭据。浏览器访问受限的管理地址 `http://CEREBRO_HOST:9000`，确认能看到集群概览。

![ELK 日志分析第 99 页插图](assets/img-8a848ba502b78359.webp)

点击集群名es-cluster 就可以进入下面界面

![ELK 日志分析第 100 页插图](assets/img-fe5f55856c1291e8.webp)

![ELK 日志分析第 100 页插图](assets/img-284dcc8e266a0747.webp)

### Docker 运行

<https://hub.docker.com/r/lmenezes/cerebro>

范例:

```bash
docker run --rm -p 127.0.0.1:9000:9000 lmenezes/cerebro:0.9.4
```

先确认镜像标签实际存在且来源可信，再执行。默认端口为 9000；如需自定义容器监听端口，可按镜像文档设置 `CEREBRO_PORT` 并同步修改端口映射。不要把管理界面直接映射到所有网络接口。

### 其它插件

Edge 浏览器应用中还有其它ES插件,可以使用

![ELK 日志分析第 100 页插图](assets/img-cf9e2abb23fe0dab.webp)

### 利用插件管理索引

### 利用 cerebro 插件创建索引

![ELK 日志分析第 101 页插图](assets/img-605ed4f426e2a638.webp)

创建索引时，应先估算数据量、增长速度和单分片目标大小，再确定主分片数；**主分片数不应机械等于集群节点数**。副本数为 1 表示每个主分片有 1 份副本，它需要放在不同节点上；单节点集群无法分配副本时会呈 yellow。下列截图展示在 Cerebro 中填写设置并确认分片分布。

![ELK 日志分析第 101 页插图](assets/img-10eca26d77c1dd7a.webp)

![ELK 日志分析第 102 页插图](assets/img-108c9dcb7ca36039.webp)

![ELK 日志分析第 102 页插图](assets/img-220f63d730d44384.webp)

再创建一个索引，不指定分片信息

![ELK 日志分析第 103 页插图](assets/img-3ac7ff4764389cf7.webp)

### 利用 cerebro 插件验证分片

Elasticsearch 7.x 起，新建索引在未被模板覆盖时默认 1 个主分片、1 个副本；较早 6.x 版本的默认主分片数曾为 5。**模板和版本设置会覆盖默认值**，最终结果应通过 `GET /索引名/_settings` 或 `GET /_cat/shards/索引名?v` 核对。

![ELK 日志分析第 103 页插图](assets/img-4154972fec4cc561.webp)

![ELK 日志分析第 104 页插图](assets/img-e05205cfa6e3147c.webp)

### 利用 head 插件验证

![ELK 日志分析第 104 页插图](assets/img-05554b04485bb372.webp)

截图中编号为 2 的粗框表示该编号的主分片；同编号的细框代表副本。界面样式只用于辅助观察，准确的分片角色应以 API 返回值为准。

![ELK 日志分析第 105 页插图](assets/img-0e4aa5338a38d973.webp)

### 利用 Head 删除索引

删除索引会删除其中全部文档。操作前确认索引名、快照与权限，不要把演示截图中的动作当成日常清理步骤；生产环境应优先使用索引生命周期策略。

![ELK 日志分析第 105 页插图](assets/img-0075423c6851a361.webp)

### 节点上的数据目录

下面的旧环境输出展示索引在不同节点上的本地分片目录。目录名是索引 UUID，不是索引名称；节点之间的目录数量不同，不能直接据此判断副本是否齐全。应使用 `_cat/shards` 对照分片分配，**不要直接修改或删除这些目录**。

```bash
[root@es-node1 ~]#ll /data/es-data/nodes/0/indices/
total 16
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 32A1_WR4QEKmTfKFe61JjA/
drwxr-xr-x 6 elasticsearch elasticsearch 4096 Jan 26 13:31 TPUrqHNdRT2lCNVPMPF2eg/
[root@es-node2 ~]#ll /data/es-data/nodes/0/indices/
total 12
drwxr-xr-x 3 elasticsearch elasticsearch 4096 Jan 26 13:31 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 7 elasticsearch elasticsearch 4096 Jan 26 13:32 TPUrqHNdRT2lCNVPMPF2eg/
[root@es-node3 ~]#ll /data/es-data/nodes/0/indices/
total 16
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 ./
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:31 ../
drwxr-xr-x 4 elasticsearch elasticsearch 4096 Jan 26 13:39 32A1_WR4QEKmTfKFe61JjA/
drwxr-xr-x 6 elasticsearch elasticsearch 4096 Jan 26 13:31 TPUrqHNdRT2lCNVPMPF2eg/
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/08-accessing-elasticsearch.html' | relative_url }}">← 上一篇：访问 Elasticsearch</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/10-how-elasticsearch-clusters-work.html' | relative_url }}">下一篇：Elasticsearch 集群原理 →</a>
</nav>
