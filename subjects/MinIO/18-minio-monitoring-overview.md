---
layout: default
title: "MinIO 对象存储 · 监控概述"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 18 监控概述

MinIO 提供 Prometheus 格式的指标端点，可以由 Prometheus 定期抓取，再用 Grafana 展示。监控不仅要看容量曲线，还要尽早发现离线节点／磁盘、请求错误、延迟升高、后台修复、备份失败和入口健康问题。仪表盘不能代替告警与恢复演练。

参考[官方指标采集说明](https://min.io/docs/minio/linux/operations/monitoring/collect-minio-metrics-using-prometheus.html)。不同版本的指标路径、名称和鉴权方式可能变化，先用所部署版本生成或核对抓取配置，再将其写入 Prometheus。`/minio/v2/metrics/cluster` 是旧版常见的集群指标路径，不能据此假设所有新版本完全一致。

一个最小的 Prometheus 抓取任务结构如下；实际环境需将目标地址、scheme 和鉴权信息替换为真实配置，并保持 YAML 缩进：

```yaml
scrape_configs:
  - job_name: minio-cluster
    scheme: https
    metrics_path: /minio/v2/metrics/cluster
    bearer_token_file: /etc/prometheus/secrets/minio-metrics-token
    static_configs:
      - targets:
          - minio.example.internal:9000
```

若使用当前版本的 v3 指标端点，应按官方生成的具体端点路径设置。不要为了省去 Token 而将 `MINIO_PROMETHEUS_AUTH_TYPE` 无条件设为 `public`，尤其不能把指标端口直接暴露给公网。集群指标可经稳定 API 入口抓取；节点级指标应针对各个节点分别抓取，否则负载均衡可能只返回其中一个节点的数据。

Grafana 的 MinIO 仪表盘（如 [13502](https://grafana.com/grafana/dashboards/13502-minio-dashboard/)）可作为起点，但面板查询必须与当前服务版本的指标名称匹配。主机 CPU、内存、磁盘与网络指标来自 Node Exporter 等系统监控组件，而不是 MinIO 的对象指标；可结合 [Node Exporter 仪表盘](https://grafana.com/grafana/dashboards/13978-node-exporter-quickstart-and-dashboard/) 查看。

下一章按“暴露端点 → Prometheus 抓取 → Grafana 展示 → 告警验证”的顺序完成实际配置。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/17-backup-and-restore-examples.html' | relative_url }}">← 上一篇：备份与恢复示例</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/19-monitoring-minio-with-prometheus-and-grafana.html' | relative_url }}">下一篇：Prometheus 与 Grafana 监控 →</a>
</nav>
