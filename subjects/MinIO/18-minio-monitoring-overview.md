---
layout: default
title: "MinIO Object Storage · MinIO Monitoring Overview"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to MinIO Object Storage Index]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 18 MinIO Monitoring Overview
## 7 MINIO 监控

### 7.1. MINIO 监控说明

<https://min.io/docs/minio/linux/operations/monitoring/collect-minio-metrics-using-prometheus.html?ref=docs-redirect>

minio监控内置支持Prometheus,推荐使用Prometheus和grafana进行监控

```bash
#Prometheus配置
scrape_configs:
#监控MinIO集群
- job_name: minio-job
#bearer_token: <secret>
metrics_path: /minio/v2/metrics/cluster
scheme: http
static_configs:
- targets: ['minio.bowen.org:9000']
#minio集群grafana模板
https://grafana.com/grafana/dashboards/13502-minio-dashboard/
#minio节点主机grafana模板:8919,1860,11074,13978模板
https://grafana.com/grafana/dashboards/13978-node-exporter-quickstart-and-
dashboard/?pg=dashboards&plcmt=featured-sub1
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/17-backup-and-restore-examples.html' | relative_url }}">← Previous: Backup and Restore Examples</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">Back to MinIO Object Storage Index</a>
  <a href="{{ '/subjects/MinIO/19-monitoring-minio-with-prometheus-and-grafana.html' | relative_url }}">Next: Monitoring MinIO with Prometheus and Grafana →</a>
</nav>
