---
layout: default
title: "MinIO 对象存储 · Kubernetes 部署"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 08 Kubernetes 部署

Kubernetes 中可以直接编写 StatefulSet 清单，也可以使用 MinIO Operator 或 Helm Chart。选用哪一种方式，首先取决于存储：**每个数据 PVC 必须有稳定持久的后端和清晰的故障域**。四个 PVC 若都落在同一台 NFS 服务器或同一组底层磁盘上，Pod 数量增加并不会消除该存储单点。生产环境优先按当前官方[Operator 文档](https://github.com/minio/operator)规划多节点和多个独立数据卷。

## 手写清单：四 Pod 教学示例

下面的例子帮助理解 StatefulSet、Headless Service 和 Pod DNS 的关系。每个 Pod 挂载一个独立 PVC；还需要让调度器把 Pod 分散到不同节点，并让 `sc-block-rwo` 实际提供独立的存储故障域。若集群没有该 StorageClass，先替换为真实名称。清单仅适于理解和测试，不是完整的生产配置。

先创建命名空间与凭据。不要把真实密码或 base64 编码后的 Secret 提交到仓库；Kubernetes Secret 的 `data` 字段只是编码，不等于加密。

```bash
kubectl create namespace minio
kubectl -n minio create secret generic minio-root \
  --from-literal=MINIO_ROOT_USER=admin \
  --from-literal=MINIO_ROOT_PASSWORD='请替换为独立的强密码'
```

以下保存为 `minio.yaml`。Headless Service 的稳定 DNS 为各 Pod 提供固定端点，`publishNotReadyAddresses` 允许新集群在 Pod 尚未就绪时发现其他节点；对外 Service 独立暴露 API 和 Console。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio-headless
  namespace: minio
spec:
  clusterIP: None
  publishNotReadyAddresses: true
  selector:
    app: minio
  ports:
    - name: api
      port: 9000
      targetPort: api
---
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: minio
spec:
  type: ClusterIP
  selector:
    app: minio
  ports:
    - name: api
      port: 9000
      targetPort: api
    - name: console
      port: 9001
      targetPort: console
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
  namespace: minio
spec:
  serviceName: minio-headless
  replicas: 4
  podManagementPolicy: Parallel
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  app: minio
              topologyKey: kubernetes.io/hostname
      containers:
        - name: minio
          image: quay.io/minio/minio:RELEASE.2024-11-07T00-52-20Z
          args:
            - server
            - http://minio-{0...3}.minio-headless.minio.svc.cluster.local/data
            - --console-address=:9001
          env:
            - name: MINIO_ROOT_USER
              valueFrom:
                secretKeyRef:
                  name: minio-root
                  key: MINIO_ROOT_USER
            - name: MINIO_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: minio-root
                  key: MINIO_ROOT_PASSWORD
          ports:
            - name: api
              containerPort: 9000
            - name: console
              containerPort: 9001
          volumeMounts:
            - name: data
              mountPath: /data
          startupProbe:
            httpGet:
              path: /minio/health/live
              port: api
            periodSeconds: 10
            failureThreshold: 30
          livenessProbe:
            httpGet:
              path: /minio/health/live
              port: api
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /minio/health/ready
              port: api
            periodSeconds: 15
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes:
          - ReadWriteOnce
        storageClassName: sc-block-rwo
        resources:
          requests:
            storage: 10Gi
```

由于采用必需的 Pod 反亲和性，集群少于四个可调度节点时，部分 Pod 会保持 Pending。这比四个 Pod 全挤在一台节点上却误以为高可用更容易排查。清单中的容量、资源请求和镜像版本仅是教学值，应按当前版本文档与业务负载调整。

```bash
kubectl apply --dry-run=client -f minio.yaml
kubectl apply -f minio.yaml
kubectl -n minio get pods,pvc,svc -o wide
kubectl -n minio logs minio-0
kubectl -n minio port-forward svc/minio 9001:9001
```

最后一条命令只在本机打开 Console 访问通道，可访问 `http://127.0.0.1:9001`。API 同理可以转发 `9000`。测试时再用 `mc admin info`、跨 Pod 的对象读写和 PVC／节点故障演练确认预期容错，而不只看 Pod 为 Running。

### Ingress 与监控

若需要给 API 或 Console 配置 Ingress，应分别设置域名、TLS 与对外 URL；不要把 API 和 Console 混在同一后端端口。原清单中的 Ingress 缩进损坏，且只指向 Console。不同控制器对大文件上传、超时及 WebSocket 的处理也不同，应用前应检查对应控制器配置。Prometheus 指标端点的认证方式应与采集器配置匹配，不要仅为抓取方便就将管理指标公开。

## Operator 与 Helm

MinIO Operator 管理 Tenant 的创建与生命周期，适合需要多个独立 Tenant、滚动维护和 Kubernetes 原生管理的场景。先核对当前[Operator 安装说明](https://github.com/minio/operator/blob/master/README.md)与 Kubernetes 版本兼容性，再按存储与故障域规划 Tenant。

![MinIO Operator 管理界面](assets/img-fd63e628ad2cbfa4.webp)

Helm Chart 则通过版本化模板生成资源。原材料中的 `helm install --name` 是旧版 Helm 语法，在 Helm 3 中应把 release 名称作为位置参数；`--generate-name` 与固定 release 名二选一。先检查 Chart 版本和值文件，再安装：

```bash
helm repo add minio https://charts.min.io/
helm repo update
helm show values minio/minio > minio-values.yaml
# 人工编辑 minio-values.yaml：模式、PVC、资源、镜像和凭据
helm upgrade --install my-minio minio/minio \
  --namespace minio --create-namespace -f minio-values.yaml
helm -n minio status my-minio
```

已有 PVC 的使用方式取决于所选 Chart 版本的 values 结构，不能不看模板就照搬旧参数 `persistence.existingClaim`。关闭持久化一般会使用临时卷，Pod 删除后数据可能丢失，只适合明确接受这一后果的短期实验。升级前备份当前 values、核对 Chart 与服务版本的兼容性，并在测试环境演练回滚。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/07-distributed-cluster-deployment.html' | relative_url }}">← 上一篇：分布式集群部署</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/09-minio-console-management.html' | relative_url }}">下一篇：Console 管理 →</a>
</nav>
