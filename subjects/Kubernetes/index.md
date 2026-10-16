---
layout: default
title: Kubernetes 学习笔记
subject_page: true
---

# Kubernetes 学习笔记

从云原生背景与集群部署开始，依次阅读资源与工作负载、网络与流量、存储与应用交付、安全及运维。共 36 章，可按顺序学习，也可直接查阅需要的主题。

公开版保留章节正文和示例结构。私钥、集群加入令牌等敏感示例值使用占位符，实际操作时需替换为当前环境生成的值。

## 基础与部署

<ol start="1">
  <li><a href="{{ '/subjects/Kubernetes/01-cloud-native-architecture.html' | relative_url }}">云原生生态与 Kubernetes 架构</a></li>
  <li><a href="{{ '/subjects/Kubernetes/02-deployment-overview.html' | relative_url }}">部署模型与 Minikube</a></li>
  <li><a href="{{ '/subjects/Kubernetes/03-kubeadm-docker-ha.html' | relative_url }}">Kubeadm 与 Docker 高可用部署</a></li>
  <li><a href="{{ '/subjects/Kubernetes/04-kubeadm-containerd-ha.html' | relative_url }}">Kubeadm 与 Containerd 高可用部署</a></li>
  <li><a href="{{ '/subjects/Kubernetes/05-kubeasz-binary-deployment.html' | relative_url }}">Kubeasz 二进制部署与集群初始化</a></li>
  <li><a href="{{ '/subjects/Kubernetes/06-kubectl-management.html' | relative_url }}">kubectl 集群管理命令</a></li>
</ol>

## 资源与工作负载

<ol start="7">
  <li><a href="{{ '/subjects/Kubernetes/07-api-objects-namespaces.html' | relative_url }}">API 资源对象、清单与命名空间</a></li>
  <li><a href="{{ '/subjects/Kubernetes/08-pod-basics-lifecycle.html' | relative_url }}">Pod 基础与工作机制</a></li>
  <li><a href="{{ '/subjects/Kubernetes/09-pod-health-resources.html' | relative_url }}">Pod 健康、资源、安全与设计模式</a></li>
  <li><a href="{{ '/subjects/Kubernetes/10-workload-controllers.html' | relative_url }}">控制器、标签与 Deployment</a></li>
  <li><a href="{{ '/subjects/Kubernetes/11-daemonset-jobs.html' | relative_url }}">DaemonSet、Job 与 CronJob</a></li>
  <li><a href="{{ '/subjects/Kubernetes/12-pod-scheduling.html' | relative_url }}">Pod 调度、拓扑与驱逐</a></li>
  <li><a href="{{ '/subjects/Kubernetes/13-hpa-core-metrics.html' | relative_url }}">HPA 原理与核心指标</a></li>
  <li><a href="{{ '/subjects/Kubernetes/14-hpa-custom-metrics.html' | relative_url }}">自定义指标、Prometheus Adapter 与 KEDA</a></li>
</ol>

## 网络与流量

<ol start="15">
  <li><a href="{{ '/subjects/Kubernetes/15-network-flannel.html' | relative_url }}">网络基础与 Flannel</a></li>
  <li><a href="{{ '/subjects/Kubernetes/16-calico-network.html' | relative_url }}">Calico 网络部署与管理</a></li>
  <li><a href="{{ '/subjects/Kubernetes/17-network-policy.html' | relative_url }}">网络策略</a></li>
  <li><a href="{{ '/subjects/Kubernetes/18-service-access.html' | relative_url }}">Service 访问与负载分发</a></li>
  <li><a href="{{ '/subjects/Kubernetes/19-dns-headless-service.html' | relative_url }}">服务发现、CoreDNS 与 Headless Service</a></li>
  <li><a href="{{ '/subjects/Kubernetes/20-ingress.html' | relative_url }}">Ingress 流量治理与发布</a></li>
</ol>

## 存储与应用交付

<ol start="21">
  <li><a href="{{ '/subjects/Kubernetes/21-storage-volumes-pv-pvc.html' | relative_url }}">存储卷、PV 与 PVC</a></li>
  <li><a href="{{ '/subjects/Kubernetes/22-storageclass-openebs.html' | relative_url }}">StorageClass 与 OpenEBS</a></li>
  <li><a href="{{ '/subjects/Kubernetes/23-configmap-secret.html' | relative_url }}">ConfigMap、Secret 与配置注入</a></li>
  <li><a href="{{ '/subjects/Kubernetes/24-storage-wordpress-mysql.html' | relative_url }}">存储与配置综合实践</a></li>
  <li><a href="{{ '/subjects/Kubernetes/25-statefulset.html' | relative_url }}">StatefulSet 与有状态应用</a></li>
  <li><a href="{{ '/subjects/Kubernetes/26-crd-operator.html' | relative_url }}">CRD 与 Operator</a></li>
  <li><a href="{{ '/subjects/Kubernetes/27-helm-basics.html' | relative_url }}">Helm 基础、部署与命令</a></li>
  <li><a href="{{ '/subjects/Kubernetes/28-helm-cases.html' | relative_url }}">Helm 应用部署案例</a></li>
  <li><a href="{{ '/subjects/Kubernetes/29-helm-charts.html' | relative_url }}">自定义 Helm Chart</a></li>
</ol>

## 安全与运维

<ol start="30">
  <li><a href="{{ '/subjects/Kubernetes/30-security-authentication.html' | relative_url }}">安全体系与身份认证</a></li>
  <li><a href="{{ '/subjects/Kubernetes/31-security-rbac.html' | relative_url }}">授权机制与 RBAC</a></li>
  <li><a href="{{ '/subjects/Kubernetes/32-security-admission.html' | relative_url }}">准入控制</a></li>
  <li><a href="{{ '/subjects/Kubernetes/33-cluster-nodes.html' | relative_url }}">节点增删与 Token 管理</a></li>
  <li><a href="{{ '/subjects/Kubernetes/34-backup-restore.html' | relative_url }}">集群备份、恢复与迁移</a></li>
  <li><a href="{{ '/subjects/Kubernetes/35-certificates.html' | relative_url }}">证书续期与故障处理</a></li>
  <li><a href="{{ '/subjects/Kubernetes/36-upgrade-optimization.html' | relative_url }}">版本升级与性能优化</a></li>
</ol>
