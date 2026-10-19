---
layout: default
title: 'Kubernetes · 自定义指标、Prometheus Adapter 与 KEDA'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 14 自定义指标、Prometheus Adapter 与 KEDA

## 3 自定义指标流水线解决什么问题

上一章的 Metrics Server 提供 CPU、内存等资源指标；业务扩缩容还可能需要每秒请求数、队列积压量或其他应用指标。HPA 不会直接运行 PromQL。通常先由 Prometheus 抓取应用或 Exporter 指标，再由 Adapter 把查询结果通过 Kubernetes 聚合 API 暴露给 HPA。

![HPA 与指标 API 的关系](assets/Kubernetes的HPA动态扩缩容/img-e6352cf1eee66424.webp)

| API | 关联对象 | 典型用途 |
| --- | --- | --- |
| `metrics.k8s.io` | Pod、Node | CPU/内存资源指标，通常由 Metrics Server 提供。 |
| `custom.metrics.k8s.io` | Pod、Service 等 Kubernetes 对象 | 每个 Pod 的 QPS、某个 Service 的请求量等。 |
| `external.metrics.k8s.io` | 不要求关联 Kubernetes 对象 | 队列长度、外部云服务指标等。 |

`Prometheus Adapter` 可以按配置暴露自定义或外部指标；它也具备资源指标适配能力，但**安装 Adapter 不等于自动替换 Metrics Server**。是否启用哪类 API 取决于部署清单和规则。kube-state-metrics 则把 Deployment、StatefulSet、PVC 等 Kubernetes 对象的**状态**转换为 Prometheus 指标，是可选的采集来源；它既不是 Adapter，也不直接提供 HPA 的 Custom Metrics API。

```text
应用 / Exporter / kube-state-metrics → Prometheus 抓取与存储
                                 → Prometheus Adapter 查询并映射
                                 → API Server 聚合层
                                 → HPA 读取 custom.metrics.k8s.io 或 external.metrics.k8s.io
```

原文说“有 Pod 注解就会自动被 Prometheus 抓取”并不普遍成立：`prometheus.io/scrape`、`prometheus.io/path`、`prometheus.io/port` 只有在实际 Prometheus 抓取配置或 Operator 的发现规则读取这些注解时才生效。先检查 Prometheus Targets 页面，确认目标为 UP，再调试 Adapter。

## 3.1 Prometheus Adapter 的四个映射步骤

[Adapter 配置文档](https://github.com/kubernetes-sigs/prometheus-adapter/blob/master/docs/config.md)将自定义指标规则拆成四部分：

1. **发现（`seriesQuery`）**：哪些 Prometheus 时间序列候选可暴露。
2. **资源关联（`resources`）**：哪个标签对应 Kubernetes 的 `namespace`、`pod` 等资源。
3. **命名（`name`）**：把 Prometheus 指标名映射成 API 中可查询的名字。
4. **查询（`metricsQuery`）**：收到 HPA 请求后执行怎样的 PromQL。

![Prometheus 与 Adapter 映射关系](assets/Kubernetes的HPA动态扩缩容/img-a119e2ef79a2e398.webp)

下面是 **Adapter 规则片段**，不是独立 Kubernetes 对象。它假设 Prometheus 中有带 `namespace`、`pod` 标签的 `http_requests_total` 计数器，并把它转换为每个 Pod 的每秒请求率。若实际抓取标签叫 `kubernetes_namespace`、`kubernetes_pod_name`，必须同步修改资源映射；仅复制规则而不核对真实序列会得到 `<unknown>`。

```yaml
rules:
  custom:
    - seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace:
            resource: namespace
          pod:
            resource: pod
      name:
        matches: '^http_requests_total$'
        as: 'http_requests_per_second'
      metricsQuery: 'sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)'
```

`rate` 用于单调递增计数器；如果应用已经暴露名为 `http_requests_per_second` 的 Gauge，不应再对 Gauge 取 `rate`。原文同时展示 Gauge 和从 `http_requests_total` 推导的同名指标，却未区分来源，容易导致查询结果不一致。规则中的 `<<.LabelMatchers>>` 会带入目标 Pod 的标签条件，`<<.GroupBy>>` 保留资源维度。PromQL 需先在 Prometheus 中验证，确认每个目标 Pod 都有数据。

## 3.2 安装与连通性检查

选择与集群版本兼容的 Prometheus 和 Adapter 发行版。可采用官方清单或 Helm，但旧文档中手工生成证书、固定镜像标签、重复安装同一 Adapter 的命令不应组合执行。以下以 Helm 为流程示意；Chart 的配置键和值应以当前 `helm show values` 与实际 Prometheus Service 为准：

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm show values prometheus-community/prometheus-adapter > prometheus-adapter-defaults.yaml
# 核对 Prometheus 的 Service 名称、命名空间和端口，再编写本地 values 文件。
helm upgrade --install prometheus-adapter prometheus-community/prometheus-adapter \
  --namespace monitoring --create-namespace --values prometheus-adapter-values.yaml
kubectl get apiservice | grep custom.metrics.k8s.io
```

在 `prometheus-adapter-values.yaml` 中把规则放入当前 Chart 所要求的 `rules.custom` 位置，把 `prometheus.url` 指向**实际可访问**的 Prometheus Service。原文在同一示例中先将 `rules.custom: []`，又把 Pod 指标规则放到 `rules.external`，与后续 HPA 的 `type: Pods` 不匹配；这里的规则应配置为 **Custom Metrics**。若用原生清单安装，则应把相同规则写进 Adapter 实际挂载的 ConfigMap，并检查 Deployment 中挂载路径和服务证书，不要假定 ConfigMap 名称固定。

```bash
kubectl get apiservice | grep -E 'custom.metrics|external.metrics'
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1
kubectl logs deployment/prometheus-adapter -n monitoring --tail=100
```

仅看到 API 组不等于具体指标已可用。下一步还须查询目标 Pod 的指标值；路径中的 `*` 需由 shell 正确引用或 URL 编码，推荐把整个 API 路径加引号：

```bash
kubectl get --raw '/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/http_requests_per_second'
```

若查询为空，按“应用 `/metrics` → Prometheus Targets → PromQL 序列与标签 → Adapter 发现与日志 → Custom Metrics API → HPA”顺序排查，不要先改 HPA 阈值。

## 3.3 kube-state-metrics 何时需要

[kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)监听 Kubernetes API，暴露对象状态，例如 Deployment 副本数、Pod 状态和 PVC 信息。它补充 Prometheus 的监控视角，但不会替代应用自身的 QPS 指标，也不是实现本章 `http_requests_total` 示例的必要组件。

![Kubernetes 对象状态指标示意图](assets/Kubernetes的HPA动态扩缩容/img-554283b651a2ea16.webp)

```bash
# 如果监控方案确实需要对象状态指标，再选择兼容的发行版部署。
# 部署后核对服务、就绪状态与 Prometheus 抓取目标：
kubectl get deployment,service -A | grep kube-state-metrics
```

资源使用量随对象规模和开启的指标集变化，不能把旧版示例中的固定 CPU/内存值当成所有集群的容量规划依据。原文把“Prometheus 服务发现支持的资源角色”说成“Prometheus 只能采集五种资源”也不准确：服务发现角色不等于可观测对象类型；Exporter 和应用接口都能提供额外指标。

## 3.4 按每 Pod 请求率伸缩的完整逻辑

原实验的测试应用在 `/metrics` 暴露 `http_requests_total`，Prometheus 应抓取每个 Pod 的端点并附加 `namespace`、`pod` 标签。HPA 的 `Pods` 指标目标是每 Pod 平均 `3` 次/秒：

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: metrics-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: metrics-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "3"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

这一清单只定义 HPA；须先准备真正暴露指标的 `metrics-app` Deployment、让 Prometheus 正确抓取，再确认 Adapter API 能返回每个 Pod 的速率。Service 可用于对应用产生测试请求，集群内用 ClusterIP 即可，不需要为了 HPA 额外部署 MetalLB、Ingress 或 NFS 存储。

```bash
kubectl apply -f metrics-app-hpa.yaml
kubectl get hpa metrics-app-hpa --watch
kubectl describe hpa metrics-app-hpa
kubectl get deployment metrics-app
```

看到 `TARGETS: <unknown>/3` 时不要以为“稍等一定会好”：它可能来自 Prometheus 未抓到样本、指标缺少 `pod` 标签、Adapter 规则映射错误、APIService 不可用，也可能只是刚启动尚无完整 `rate[2m]` 时间窗口。指标一旦有效，HPA 根据当前值与目标值计算建议副本数，但实际 Pod 还受调度容量限制。高负载结束后的缩容由稳定窗口与缩容策略控制；原截图的时间和副本数不是保证。

## 4 事件驱动扩缩：KEDA 与其他方案

![KEDA 事件驱动扩缩示意图](assets/Kubernetes的HPA动态扩缩容/img-4da1b288cfd92329.webp)

[KEDA](https://keda.sh/) 通过 ScaledObject 和触发器连接 Kafka、RabbitMQ、云队列、Prometheus 等事件源，通常与 HPA 协作处理活动时的水平扩缩，并能在适合的工作负载上实现零到非零副本的激活。并非所有触发器和所有工作负载都支持相同的伸缩范围；还要考虑队列语义、积压消费速度和冷启动。

[Kapacity](https://github.com/traas-stack/kapacity) 面向更广泛的容量管理与智能伸缩实践，可以作为扩展方案了解，但不属于 Kubernetes 内置 HPA 或本文演示流水线的前提。选择扩缩方案时先明确目标指标、数据可靠性、延迟、伸缩上限和失败时的回退方式，避免因为组件更多而增加不可解释的控制环路。

<details class="historical-figures" markdown="1">
<summary>查看原始讲义中的其余配图与历史操作截图（28 张）</summary>

![原 PDF 第 38 页插图](assets/Kubernetes的HPA动态扩缩容/img-fda944248b625333.webp)

![原 PDF 第 39 页插图](assets/Kubernetes的HPA动态扩缩容/img-dd1bea9c272b8044.webp)

![原 PDF 第 41 页插图](assets/Kubernetes的HPA动态扩缩容/img-5c5926da13330bed.webp)

![原 PDF 第 42 页插图](assets/Kubernetes的HPA动态扩缩容/img-b4b371961dcf1fd2.webp)

![原 PDF 第 43 页插图](assets/Kubernetes的HPA动态扩缩容/img-404f6b8609205d80.webp)

![原 PDF 第 44 页插图](assets/Kubernetes的HPA动态扩缩容/img-1907988d158137df.webp)

![原 PDF 第 48 页插图](assets/Kubernetes的HPA动态扩缩容/img-441812f8df6cf01f.webp)

![原 PDF 第 54 页插图](assets/Kubernetes的HPA动态扩缩容/img-6e30e9147734e40c.webp)

![原 PDF 第 55 页插图](assets/Kubernetes的HPA动态扩缩容/img-902cfdd3fe07d7d7.webp)

![原 PDF 第 55 页插图](assets/Kubernetes的HPA动态扩缩容/img-13d74584fa5c3919.webp)

![原 PDF 第 56 页插图](assets/Kubernetes的HPA动态扩缩容/img-a15f80998bea3d2e.webp)

![原 PDF 第 56 页插图](assets/Kubernetes的HPA动态扩缩容/img-c0d43a9dc03bfe86.webp)

![原 PDF 第 56 页插图](assets/Kubernetes的HPA动态扩缩容/img-219660a401391fac.webp)

![原 PDF 第 59 页插图](assets/Kubernetes的HPA动态扩缩容/img-d37abf238b971fc1.webp)

![原 PDF 第 60 页插图](assets/Kubernetes的HPA动态扩缩容/img-381f078d8ed4b04e.webp)

![原 PDF 第 60 页插图](assets/Kubernetes的HPA动态扩缩容/img-1331007d24b7447e.webp)

![原 PDF 第 61 页插图](assets/Kubernetes的HPA动态扩缩容/img-8a2aba6a955fc97d.webp)

![原 PDF 第 61 页插图](assets/Kubernetes的HPA动态扩缩容/img-5d6e040ca203dc17.webp)

![原 PDF 第 62 页插图](assets/Kubernetes的HPA动态扩缩容/img-0075564c8f2a5e42.webp)

![原 PDF 第 65 页插图](assets/Kubernetes的HPA动态扩缩容/img-6f5acacffc7f492f.webp)

![原 PDF 第 67 页插图](assets/Kubernetes的HPA动态扩缩容/img-b8152af6d444a777.webp)

![原 PDF 第 67 页插图](assets/Kubernetes的HPA动态扩缩容/img-95b3d171292adb71.webp)

![原 PDF 第 71 页插图](assets/Kubernetes的HPA动态扩缩容/img-db7077997ecf2413.webp)

![原 PDF 第 73 页插图](assets/Kubernetes的HPA动态扩缩容/img-bf6581a90349be02.webp)

![原 PDF 第 82 页插图](assets/Kubernetes的HPA动态扩缩容/img-8b0c0eee9a508a65.webp)

![原 PDF 第 82 页插图](assets/Kubernetes的HPA动态扩缩容/img-be9cedca62873320.webp)

![原 PDF 第 83 页插图](assets/Kubernetes的HPA动态扩缩容/img-fb00a5139757cb91.webp)

![原 PDF 第 83 页插图](assets/Kubernetes的HPA动态扩缩容/img-e78a864a6a17ff09.webp)

</details>

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/13-hpa-core-metrics.html' | relative_url }}">← 上一章：HPA 原理与核心指标</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/15-network-flannel.html' | relative_url }}">下一章：网络基础与 Flannel →</a>
</nav>
