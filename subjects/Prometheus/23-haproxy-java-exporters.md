---
layout: default
title: "Prometheus · HAProxy 与 Java 监控"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 23 HAProxy 与 Java 监控

本章有两条独立的采集链路：HAProxy 可通过旧版外置 Exporter 解析状态 CSV，也可使用其内置 Prometheus 指标端点；Java/Tomcat 可通过 JMX Exporter Java Agent 暴露 MBean 指标。每种方式只选一种作为主要抓取源，避免重复采集，并先确认指标端点确实输出数据，再配置 Prometheus。

## 7.3 HAProxy 监控

### 7.3.1 外置 haproxy_exporter：读取状态 CSV

外置 [haproxy_exporter](https://github.com/prometheus/haproxy_exporter) 读取 HAProxy 状态页的 CSV 或本机 Unix Socket，再在默认 `9101` 端口暴露 Prometheus 指标。这适合暂不能使用 HAProxy 内置指标的版本。状态页的 `/haproxy-status` 用于人看，`/haproxy-status;csv` 则供 Exporter 解析，两者都要在 HAProxy 中启用统计功能。

```haproxy
listen stats
    bind 127.0.0.1:9999
    mode http
    stats enable
    stats uri /haproxy-status
    stats auth monitor:STRONG_PASSWORD
```

先用 `haproxy -c -f /etc/haproxy/haproxy.cfg` 检查配置并重启，再在同一主机验证 CSV：

```bash
curl -fsS -u monitor:STRONG_PASSWORD 'http://127.0.0.1:9999/haproxy-status;csv' | head
```

原资料把统计页监听到 `0.0.0.0:9999`，并使用简单密码。若 Exporter 与 HAProxy 在同一台主机，用本机地址或 Unix Socket 可减少暴露范围；分机部署时则需限制统计页访问，并管理凭据。Exporter 的 `--haproxy.scrape-uri` 参数必须保持一行，不能照搬 PDF 中 `--` 与参数名之间的换行：

```ini
[Unit]
Description=HAProxy Exporter
After=haproxy.service

[Service]
Type=simple
ExecStart=/usr/local/haproxy_exporter/haproxy_exporter --haproxy.scrape-uri=http://monitor:STRONG_PASSWORD@127.0.0.1:9999/haproxy-status;csv
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

这里仅展示启动结构，生产中不宜把密码直接放进可被进程列表读取的启动参数；可使用受保护的本机 Unix Socket 并授予 Exporter 服务账户读取权限。启动后验证 `http://127.0.0.1:9101/metrics`，再把 **Exporter 所在主机**的 `9101` 加入 Prometheus；原资料先部署在一台机器，后又抓取另一个地址，容易查不到数据。

```yaml
scrape_configs:
  - job_name: haproxy-exporter
    static_configs:
      - targets: ['10.0.0.106:9101']
```

![HAProxy 统计页与 CSV](assets/img-b535f928366445ff.webp)

![外置 Exporter 在 Prometheus 中的结果](assets/img-88d26e4992210192.webp)

### 7.3.2 HAProxy 内置 Prometheus 指标

支持 `USE_PROMEX` 的 HAProxy 可以直接在 HTTP frontend 暴露 `/metrics`，省去外置 Exporter。先运行 `haproxy -vv` 检查构建选项中是否有 `USE_PROMEX=1`；Ubuntu 22.04 的原实验包已经支持，不必为了监控再次编译一整套 HAProxy。若当前包没有该能力，应评估官方支持的包或编译版本，而不是把不同版本的 `EXTRA_OBJS`、`USE_PROMEX` 命令混合执行。

```haproxy
frontend prometheus-metrics
    bind 127.0.0.1:9999
    mode http
    http-request use-service prometheus-exporter if { path /metrics }
    http-request deny
```

统计页和指标端点可以在同一配置中分别提供，但不是“必须同时启用”的关系。上例只开放指标路径，其他路径拒绝；若 Prometheus 在另一主机，应将监听地址与网络访问控制调整为它可达，仍不应把整个统计接口无差别开放。验证 `curl -fsS http://127.0.0.1:9999/metrics | head` 后，Prometheus 抓取 HAProxy 主机的 `9999`：

```yaml
scrape_configs:
  - job_name: haproxy-native
    static_configs:
      - targets: ['10.0.0.106:9999']
```

外置 Exporter 与内置端点的指标名和 Grafana 面板可能不同；导入原资料提到的 Dashboard 2428 或 12693 前先查看真实指标。若 Targets 为 `UP` 而面板为空，先检查查询中的指标名、`job` 和实例选择。

![HAProxy 内置指标端点](assets/img-8872212d37031767.webp)

![HAProxy Grafana 面板](assets/img-835a6a1bdc2eafc6.webp)

## 7.4 Java/Tomcat：JMX Exporter Java Agent

### 7.4.1 Agent 如何接入 JVM

[JMX Exporter](https://github.com/prometheus/jmx_exporter) 的 Java Agent 随应用 JVM 启动，从 JVM 内部读取 MBean 并暴露 HTTP 指标端点。它与远程 JMX 连接不是同一模式：这里**不需要**把 JMX RMI 端口暴露给 Prometheus，Prometheus 只抓取 Agent 的 HTTP 端口。

选择与 Java 版本兼容的 JMX Exporter 版本，并从官方发布页取得 `jmx_prometheus_javaagent-<版本>.jar`。原资料罗列了多个版本和过期的 Java 8/Tomcat 包；实际只需按当前 Tomcat 与 JVM 版本选择一套。Tomcat 的 MBean 名称可能随版本变化，规则文件也应与当前版本核对。下载配置时应使用原始 YAML 文件，而不是 GitHub 的 `blob` HTML 页面。

示例约定 JAR 在 `/opt/jmx/jmx_prometheus_javaagent.jar`，规则在 `/opt/jmx/tomcat.yml`，端口为 `9527`。不要直接修改发行版管理的 `catalina.sh`；可由 Tomcat 的 `setenv.sh` 或 systemd 环境配置注入 JVM 参数：

```bash
export CATALINA_OPTS="$CATALINA_OPTS -javaagent:/opt/jmx/jmx_prometheus_javaagent.jar=9527:/opt/jmx/tomcat.yml"
```

`CATALINA_OPTS` 应保留原有值，不能用新值覆盖其他 JVM 启动参数。JAR 和配置文件需对 Tomcat 服务账户可读。重启 Tomcat 后先检查应用 `8080` 正常，再查询 Agent 的 `9527/metrics`；如果应用启动失败，优先看 Tomcat 日志中的 Java Agent 错误，而不是修改 Prometheus。

![JMX Exporter 指标端点](assets/img-32a1bcd48afb965a.webp)

### 7.4.2 Prometheus 与 Grafana 验证

```yaml
scrape_configs:
  - job_name: tomcat-jmx
    static_configs:
      - targets: ['10.0.0.106:9527']
```

检查 Prometheus 配置并重载，在 Targets 页面确认 `UP`，再搜索 Tomcat/JVM 指标。若 Agent 暴露端口但没有预期的 Tomcat 指标，检查 MBean 名称与 `tomcat.yml` 的匹配规则；端口 `UP` 只表示 HTTP 抓取成功。Grafana 原教程使用的 Dashboard 8704、14845 可能假设 `job="java"`，本例是 `tomcat-jmx`，导入后需调整变量与查询。

![Tomcat JMX 目标](assets/img-dfaeb9f2474f54e9.webp)

![Tomcat Grafana 面板](assets/img-d62b6db57434c767.webp)

### 7.4.3 容器中的 Tomcat

容器场景仍推荐先把 Java Agent、规则文件放进镜像或只读卷，再通过 `CATALINA_OPTS` 启动；由 Prometheus 抓取容器可达的 Agent 端口。原资料另用第三方 Tomcat Exporter WAR，需要自制镜像、改 Manager 配置并设置简单口令，这与前面的 JMX Agent 是**另一条方案**，不应混成同一部署。若沿用 WAR 方案，应确认其项目仍受维护，并分别验证 `/metrics`、权限与实际端口。

一个可读的 Compose 结构是：

```yaml
services:
  tomcat:
    image: your-tomcat-with-jmx-agent:VERSION
    environment:
      CATALINA_OPTS: '-javaagent:/opt/jmx/jmx_prometheus_javaagent.jar=9527:/opt/jmx/tomcat.yml'
    ports:
      - '8080:8080'
      - '9527:9527'
```

此示例要求镜像中确实包含 JAR 与 YAML；镜像构建方式取决于项目使用的 Tomcat/JDK 基础镜像。不要因为应用在 `8080` 提供服务，就把 Prometheus 目标写成 `8080`：JMX Agent 的指标目标是 `9527`。若 Prometheus 与容器在同一个 Compose 网络内，可使用服务名 `tomcat:9527`，不必向宿主机发布指标端口。

![容器中 Tomcat 的监控结果](assets/img-cacb00c8f9c9c6e0.webp)
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/22-node-mysql-exporters.html' | relative_url }}">← 上一章：Node Exporter 与 MySQL 监控</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/24-redis-nginx-exporters.html' | relative_url }}">下一章：Redis 与 Nginx 监控 →</a>
</nav>
