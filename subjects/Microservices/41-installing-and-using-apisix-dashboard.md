---
layout: default
title: "微服务架构 · APISIX Dashboard 安装和使用"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 41 APISIX Dashboard 安装和使用

Dashboard 是可选的图形化管理界面，帮助操作 Route、Upstream、Service、证书和插件。**代理请求仍由 APISIX 处理，动态配置仍保存在 etcd**。本篇原始截图主要来自 Dashboard 3.0.1 的历史实验；当前 APISIX 版本是否支持该 Dashboard，必须先查看对应项目的兼容说明，不要把旧镜像与新版 APISIX 默认组合使用。

![Dashboard 主要功能](assets/img-d5770dbd53603685.webp)
![Dashboard、APISIX 与 etcd 的关系](assets/img-0e759c93ae91f142.webp)

## 先确认兼容性，再安装

[Dashboard 旧版安装文档](https://apisix.apache.org/zh/docs/dashboard/install/)列出过容器、RPM 和源码方式。原资料从旧 `apisix-docker` 提取 3.0.1 镜像配置；某些较新的 Compose 示例已不再包含 Dashboard。这不是“APISIX 必须回退到旧提交”的理由。应先固定**已验证兼容的一组 APISIX、Dashboard 与 etcd 版本**，再选择部署方式；若没有合适的 Dashboard，仍可用 Admin API 或 Kubernetes 控制器管理配置。

![Dashboard 历史镜像信息](assets/img-36968940442d4287.webp)

以 Dashboard 3.0.1 的容器布局为例，配置文件要告诉 Dashboard **从它自己的网络视角**如何访问 etcd。若 etcd 在同一个 Docker 网络，写服务名 `etcd:2379`；容器中的 `127.0.0.1:2379` 指向 Dashboard 容器自身，通常会得到连接拒绝。以下仅展示关键层级，完整字段以匹配版本自带的 `conf.yaml` 为准：

```yaml
conf:
  listen:
    host: 0.0.0.0
    port: 9000
  allow_list:
    - 127.0.0.1/32
    - MANAGEMENT_SUBNET

etcd:
  endpoints:
    - http://etcd:2379

authentication:
  secret: REPLACE_WITH_RANDOM_SECRET
  expire_time: 3600
  users:
    - username: admin
      password: REPLACE_WITH_STRONG_PASSWORD
```

`allow_list` 应写实际管理网段；示例槽位不可直接运行。若把 `allow_list` 设成 `0.0.0.0/0` 并保留 `admin/admin`，就把可修改网关路由的管理界面交给所有可达主机。正式环境还需 TLS、身份管理、审计、etcd 访问控制和备份。管理页面的 9000 与 APISIX 代理端口 9080、Admin API 端口 9180 各有不同职责。

将配置挂载到该镜像实际读取的路径，固定镜像标签并检查日志：

```bash
docker run -d --name apisix-dashboard \
  --network APISIX_ETCD_NETWORK \
  -p 127.0.0.1:9000:9000 \
  -v /ABSOLUTE_PATH/conf.yaml:/usr/local/apisix-dashboard/conf/conf.yaml:ro \
  apache/apisix-dashboard:3.0.1-alpine
docker logs apisix-dashboard
```

若 APISIX、etcd 是系统服务而 Dashboard 在容器里，应给容器一个**可达的 etcd 地址**，不必一律使用 host 网络。日志显示 `manager-api is running successfully` 证明 Dashboard 启动；还要确认它能读取与 APISIX 相同的 etcd 前缀。容器日志中的 `127.0.0.1:2379 connection refused` 首先是网络地址问题，而不是路由配置问题。

![Dashboard 连接 etcd 后的页面](assets/img-8be03810a2cf9982.webp)
![Dashboard 初始资源列表](assets/img-c489b0845c9925d8.webp)
![RPM 部署的管理页面示例](assets/img-3d50f463dd01bef3.webp)

RPM 和源码构建是上述容器方式的替代部署途径。若选 RPM，应核对发行版、架构、所需配置路径和服务状态；若从源码构建，应固定源码标签、Go 与 Node 工具链版本。原资料的 systemd 样例出现 `Conflicts=apisix-dashboard.service`，与自身冲突，不能直接作为服务文件；优先采用发行包自带的单位文件并核对启动日志。

## 通过界面创建一条路由

先准备一个从 APISIX **所在主机或容器**可达的测试上游，例如内部 HTTP echo 服务，并先直连其 `/anything/test` 确认成功。不要让第三方公共测试站点的网络波动干扰路由验证。

### 做法 A：直接在 Route 中填写上游

1. 在 Dashboard 创建 Route，设置唯一名称、请求 Host 和 URI，例如 `Host: www.example.test`、`URI: /anything/*`。
2. 填写上游节点的**实际可达 IP:端口**与权重；确认 HTTP/HTTPS 协议和后端路径。
3. 保存后从代理入口请求，而不是请求 Dashboard 9000：

```bash
curl -H 'Host: www.example.test' \
  'http://127.0.0.1:9080/anything/test?name=demo'
```

如果返回 echo 服务的响应，再检查 Dashboard 中的路由状态和 APISIX 日志。后端停掉后可能得到 502/503，取决于健康检查、重试和具体错误；**404 Route Not Found** 则通常表示 Host、URI 或方法没有匹配路由，先排查匹配条件而非上游。原图中的两个测试主机说明“补充上游节点后可恢复”，但仅添加节点不等于负载均衡或健康检查已经正确配置。

![准备 echo 测试服务](assets/img-4c9077661a52d432.webp)
![直连 echo 服务](assets/img-0af3798d1f45821a.webp)
![创建 Route 入口](assets/img-a22df916a99a15ff.webp)
![填写路由名称](assets/img-cf398f3c29b8e51f.webp)
![设置 Host 和 URI](assets/img-9200f58a4cd81440.webp)
![选择请求方法](assets/img-7e37cb05ab4ea06e.webp)
![填写上游节点](assets/img-15657038fb34619f.webp)
![保存路由](assets/img-66ba42031f5fbd49.webp)
![路由列表](assets/img-583e8c6ab637e00b.webp)
![经代理访问上游](assets/img-2a11dcf716ba2eaa.webp)
![新增备用节点](assets/img-85c6f61369583daf.webp)
![调整节点权重](assets/img-152b858d6b848d66.webp)
![查看更新后的路由](assets/img-7166b12f726ea509.webp)
![再次验证转发](assets/img-ccc946d775088067.webp)

### 做法 B：先创建 Upstream，再让 Route 引用

当多个路由复用同一组后端时，先建 Upstream 更便于统一维护节点、权重、健康检查和负载均衡算法。再创建 Route、设置匹配条件、关联该 Upstream。此时调整 Upstream 的节点可影响引用它的多个路由，应先确认影响范围并保留回滚方案。

![创建 Upstream 入口](assets/img-c793e45844bb5675.webp)
![设置 Upstream 节点](assets/img-4ce8a0a4e5397e69.webp)
![保存 Upstream](assets/img-80c06407be74a55c.webp)
![新建 Route](assets/img-3ba0d8b623d77f76.webp)
![选择已有 Upstream](assets/img-4acc1b28e19e81d6.webp)
![确认路由与上游关系](assets/img-9723fb11fbca1554.webp)
![查看路由结果](assets/img-33c158214b68c207.webp)

直接填写上游与引用 Upstream 是两种组织配置的方法，不表示流量处理性能必然不同。测试时同时覆盖“正确 Host + 正确 URI”“错误 Host”“错误 URI”和“后端不可达”四类请求，分别识别路由未匹配与上游故障。

## Grafana 不是 Dashboard 自带监控

原资料的 Compose 环境另外运行了 Prometheus 和 Grafana，截图展示的是**独立观测链路**。要看到请求指标，需要在 APISIX 启用相应插件或导出端点，让 Prometheus 抓取，再在 Grafana 配置数据源与面板。浏览器里的 `127.0.0.1` 指用户自己的电脑，容器里的 `127.0.0.1` 指容器自身，因此 Grafana 数据源地址必须从 Grafana 所在网络可达。先在 Prometheus 的 Targets 页面确认采集成功，再检查 Grafana 图表。

![Grafana 登录](assets/img-f56aeafe24c1f428.webp)
![添加 Prometheus 数据源](assets/img-0c7d670cf53cf4e9.webp)
![验证数据源连接](assets/img-846e9b3ea991bb09.webp)
![APISIX 指标面板](assets/img-80661a6f5759929f.webp)
![网关请求趋势](assets/img-ed0b34e6e0d77fed.webp)
![节点运行指标](assets/img-9cb58fc881ccff36.webp)

本篇的交付结果是：管理界面能读取正确的 etcd、创建路由后代理入口能转发、故障时能区分 404 与上游错误、监控链路有真实采集数据。下一篇用 Admin API 完成同一类配置操作，便于自动化管理。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/40-apisix-configuration-management.html' | relative_url }}">← 上一篇：APISIX 配置管理</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/Microservices/42-accessing-apisix-apis.html' | relative_url }}">下一篇：调用 APISIX API →</a>
</nav>
