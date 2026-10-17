---
layout: default
title: Prometheus 学习笔记
subject_page: true
prometheus_notes: true
---

# Prometheus 学习笔记

从监控基础、部署与数据采集开始，依次阅读 PromQL、标签、告警、服务发现、Exporter、存储与 Kubernetes 集成。共 33 章。

[关于文档、贡献者与使用协议]({{ '/subjects/Prometheus/00-about.html' | relative_url }})

## 基础与部署

<ol start="1">
  <li><a href="{{ '/subjects/Prometheus/01-prometheus-introduction.html' | relative_url }}">Prometheus 介绍</a></li>
  <li><a href="{{ '/subjects/Prometheus/02-prometheus-deployment.html' | relative_url }}">Prometheus 部署与配置</a></li>
  <li><a href="{{ '/subjects/Prometheus/03-node-exporter.html' | relative_url }}">Node Exporter 安装与采集</a></li>
  <li><a href="{{ '/subjects/Prometheus/04-grafana.html' | relative_url }}">Grafana 展示与监控</a></li>
  <li><a href="{{ '/subjects/Prometheus/05-zookeeper-monitoring.html' | relative_url }}">Zookeeper 监控</a></li>
  <li><a href="{{ '/subjects/Prometheus/06-pushgateway.html' | relative_url }}">Pushgateway 自定义数据</a></li>
</ol>

## 查询与标签

<ol start="7">
  <li><a href="{{ '/subjects/Prometheus/07-promql-foundations.html' | relative_url }}">PromQL 指标与基础</a></li>
  <li><a href="{{ '/subjects/Prometheus/08-promql-operators.html' | relative_url }}">PromQL 运算</a></li>
  <li><a href="{{ '/subjects/Prometheus/09-exporter-development-grafana.html' | relative_url }}">Exporter 开发与 PromQL 可视化</a></li>
  <li><a href="{{ '/subjects/Prometheus/10-label-management.html' | relative_url }}">标签管理</a></li>
</ol>

## 记录与告警

<ol start="11">
  <li><a href="{{ '/subjects/Prometheus/11-recording-rules.html' | relative_url }}">记录规则</a></li>
  <li><a href="{{ '/subjects/Prometheus/12-alertmanager-rules.html' | relative_url }}">Alertmanager 部署与告警规则</a></li>
  <li><a href="{{ '/subjects/Prometheus/13-alert-templates-routing.html' | relative_url }}">告警模板、路由与抑制</a></li>
  <li><a href="{{ '/subjects/Prometheus/14-wechat-alerting.html' | relative_url }}">微信告警</a></li>
  <li><a href="{{ '/subjects/Prometheus/15-dingtalk-alerting.html' | relative_url }}">钉钉告警</a></li>
  <li><a href="{{ '/subjects/Prometheus/16-alertmanager-ha.html' | relative_url }}">Alertmanager 高可用与其他应用</a></li>
</ol>

## 服务发现

<ol start="17">
  <li><a href="{{ '/subjects/Prometheus/17-service-discovery-basics.html' | relative_url }}">服务发现基础、文件与 DNS</a></li>
  <li><a href="{{ '/subjects/Prometheus/18-consul-introduction-single.html' | relative_url }}">Consul 简介与单机部署</a></li>
  <li><a href="{{ '/subjects/Prometheus/19-consul-cluster.html' | relative_url }}">Consul 集群部署</a></li>
  <li><a href="{{ '/subjects/Prometheus/20-consul-registration-prometheus.html' | relative_url }}">Consul 自动注册与监控采集</a></li>
  <li><a href="{{ '/subjects/Prometheus/21-kubernetes-service-discovery.html' | relative_url }}">Kubernetes 服务发现</a></li>
</ol>

## Exporter 与容器监控

<ol start="22">
  <li><a href="{{ '/subjects/Prometheus/22-node-mysql-exporters.html' | relative_url }}">Node Exporter 与 MySQL 监控</a></li>
  <li><a href="{{ '/subjects/Prometheus/23-haproxy-java-exporters.html' | relative_url }}">HAProxy 与 Java 监控</a></li>
  <li><a href="{{ '/subjects/Prometheus/24-redis-nginx-exporters.html' | relative_url }}">Redis 与 Nginx 监控</a></li>
  <li><a href="{{ '/subjects/Prometheus/25-consul-blackbox-exporters.html' | relative_url }}">Consul 与 Blackbox Exporter</a></li>
  <li><a href="{{ '/subjects/Prometheus/26-container-monitoring.html' | relative_url }}">容器监控与 cAdvisor</a></li>
</ol>

## 联邦与存储

<ol start="27">
  <li><a href="{{ '/subjects/Prometheus/27-federation.html' | relative_url }}">Prometheus 联邦</a></li>
  <li><a href="{{ '/subjects/Prometheus/28-local-storage.html' | relative_url }}">Prometheus 本地存储</a></li>
  <li><a href="{{ '/subjects/Prometheus/29-victoriametrics.html' | relative_url }}">VictoriaMetrics 远程存储</a></li>
</ol>

## Kubernetes 集成

<ol start="30">
  <li><a href="{{ '/subjects/Prometheus/30-kubernetes-yaml-deployment.html' | relative_url }}">Kubernetes YAML 部署</a></li>
  <li><a href="{{ '/subjects/Prometheus/31-kubernetes-helm.html' | relative_url }}">Kubernetes Helm 部署</a></li>
  <li><a href="{{ '/subjects/Prometheus/32-kubernetes-operator.html' | relative_url }}">Kubernetes Operator 部署</a></li>
  <li><a href="{{ '/subjects/Prometheus/33-kubernetes-monitoring-operations.html' | relative_url }}">Kubernetes 监控应用与组件</a></li>
</ol>

