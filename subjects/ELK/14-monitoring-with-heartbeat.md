---
layout: default
title: "ELK 日志分析 · 利用 Heartbeat 监控"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 14 利用 Heartbeat 监控
### 3.2 利用 Heartbeat 监控

Heartbeat 定时检查目标是否可达，支持 HTTP、TCP、ICMP 及相关 TLS 配置。它回答的是“从探测节点看，服务在该时刻是否可达”，不能代替应用内部健康检查，也不能保证所有用户路径都正常。参考[官方 Heartbeat 配置文档](https://www.elastic.co/guide/en/beats/heartbeat/current/configuring-howto-heartbeat.html)。

### 安装与版本准备

从[官方 Heartbeat 下载页](https://www.elastic.co/downloads/beats/heartbeat)选择与宿主机平台和 Elasticsearch 集群兼容的版本。旧资料中的 7.6.2/8.6.1 安装包 URL 只是历史示例，不宜直接复制。安装后先确认服务名称及默认配置文件位置；在 Debian/Ubuntu 包安装方式下，通常是 `/etc/heartbeat/heartbeat.yml` 与 `heartbeat-elastic.service`。

### 配置三种探测

以下示例展示配置层级与探测目标的区别。请把地址换成自己的服务，并按实际 Elasticsearch 安全配置补充 HTTPS、凭据与证书；这里的 `http://` 输出仅适用于已隔离且未启用认证的实验集群。

```yaml
heartbeat.monitors:
  - type: http
    id: web-health
    name: Web 健康检查
    urls: ["http://web.example.org/health"]
    schedule: '@every 10s'
    timeout: 6s
    check.response.status: [200]

  - type: tcp
    id: web-tcp
    name: Web TCP 端口
    hosts: ["web.example.org:80"]
    schedule: '@every 10s'

  - type: icmp
    id: gateway-ping
    name: 网关连通性
    hosts: ["192.0.2.1"]
    schedule: '@every 30s'

output.elasticsearch:
  hosts: ["http://es.example.org:9200"]

setup.kibana:
  host: "http://kibana.example.org:5601"
```

HTTP 探测检查响应状态；TCP 探测只能证明端口可连接，不代表业务请求成功；ICMP 可能因权限或网络策略失败。`@every 10s` 比被 PDF 换行打断的 cron 表达式更容易读懂。生产环境还应考虑探测节点位置、超时、重试和告警抑制，避免把一次短暂网络抖动当成服务整体故障。

保存配置后先校验，再启动服务并查看日志：

```bash
sudo heartbeat test config -e
sudo heartbeat test output -e
sudo systemctl enable --now heartbeat-elastic
sudo journalctl -u heartbeat-elastic -n 50 --no-pager
```

测试输出连接是否成功需要与集群实际认证方式一致。不要通过删除 Elasticsearch 认证配置来“修复”输出失败。

### 在 Elasticsearch 中确认探测数据

较新的版本可能使用以 `.ds-heartbeat-` 开头的数据流后备索引；先按当前版本实际数据流或索引名查询最近事件。

![ELK 日志分析第 129 页插图](assets/img-2be1bdf3f8ecab80.webp)

较早版本常见以 `heartbeat-` 开头的索引。截图中的命名与 Head 插件界面仅供对照，不应作为新版部署的固定要求。

![ELK 日志分析第 129 页插图](assets/img-daa558028147aef6.webp)

### 在 Kibana 中查看可用性

在 Kibana 的可观测性或 Uptime/Synthetics 相关入口查看探测结果；菜单名称随版本变化。先确认时间范围、探测器 ID 和所在位置，再比较最近成功率与响应时间。

![ELK 日志分析第 130 页插图](assets/img-467cc0e62e7782a1.webp)

![ELK 日志分析第 130 页插图](assets/img-ac24feef5c2869ad.webp)

![ELK 日志分析第 131 页插图](assets/img-667460f78cdecf68.webp)

以下是旧版界面截图，便于对照：

![ELK 日志分析第 131 页插图](assets/img-1f07180e522a6f1c.webp)

![ELK 日志分析第 132 页插图](assets/img-9cebfa8c57459c35.webp)

![ELK 日志分析第 132 页插图](assets/img-b68fa6ad3287762a.webp)

![ELK 日志分析第 132 页插图](assets/img-d8786fd1c8c0d5f2.webp)

![ELK 日志分析第 133 页插图](assets/img-b0894fd8a8e7f7df.webp)

![ELK 日志分析第 133 页插图](assets/img-5e51199e9d55eba8.webp)

### 验证故障状态

仅在测试环境中停止被探测的 Apache 服务，再观察下一次 Heartbeat 探测及 Kibana 状态变化。颜色与状态展示取决于版本和视图，重点是确认事件中的失败原因与时间戳。

```bash
[root@elk-web2 ~]#systemctl stop apache2
```

新版界面示例：

![ELK 日志分析第 134 页插图](assets/img-413f74e264578f52.webp)

![ELK 日志分析第 134 页插图](assets/img-9fec3b22f3146f80.webp)

旧版界面示例：

![ELK 日志分析第 135 页插图](assets/img-8db2743e73a652cc.webp)

![ELK 日志分析第 135 页插图](assets/img-b9de4f872c9a0604.webp)

![ELK 日志分析第 135 页插图](assets/img-328f4b9f09e9b3c6.webp)

![ELK 日志分析第 136 页插图](assets/img-c71e7377ec321dd0.webp)

![ELK 日志分析第 136 页插图](assets/img-e65848409a9281b3.webp)

### 利用 Kibana 可视化探测数据

旧版界面示例展示了从探测事件创建图表的过程。实际制作仪表板时，建议分别显示可用率、失败次数、响应时间和探测位置，并保留足够的时间上下文。

![ELK 日志分析第 137 页插图](assets/img-522ca9aad573d7b9.webp)

![ELK 日志分析第 137 页插图](assets/img-8aa0263fd71ccd14.webp)

![ELK 日志分析第 137 页插图](assets/img-8cd2dc3b94de0145.webp)

![ELK 日志分析第 138 页插图](assets/img-8d48e4b506167800.webp)

![ELK 日志分析第 138 页插图](assets/img-60e23ade6a3c4ee5.webp)

![ELK 日志分析第 138 页插图](assets/img-6f34d0fc3b4e2d70.webp)

![ELK 日志分析第 139 页插图](assets/img-e691ea7af64b6786.webp)

![ELK 日志分析第 139 页插图](assets/img-e02e79bd1fdceebf.webp)

![ELK 日志分析第 139 页插图](assets/img-60111d812b64ae94.webp)

![ELK 日志分析第 140 页插图](assets/img-b56184a2be554574.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/13-monitoring-performance-with-metricbeat.html' | relative_url }}">← 上一篇：利用 Metricbeat 监控性能相关指标</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/15-collecting-logs-with-filebeat.html' | relative_url }}">下一篇：利用 Filebeat 收集日志 →</a>
</nav>
