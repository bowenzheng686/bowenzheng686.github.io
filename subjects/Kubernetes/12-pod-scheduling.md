---
layout: default
title: 'Kubernetes · Pod 调度、拓扑与驱逐'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 12 Pod 调度、拓扑与驱逐

## 1 调度器如何选择节点

kube-scheduler 观察尚未绑定节点的 Pod，先过滤掉不满足资源和硬性约束的节点，再给候选节点评分并绑定。当前调度框架通过 PreFilter、Filter、Score、Reserve、Permit、Bind 等扩展点组织插件；旧文献中的 Predicates/Priorities 名称可帮助理解“过滤/打分”，但不应直接当作当前配置接口。

调度主要依据容器的 **resource requests**、节点可分配资源、节点选择器/亲和性、Pod 亲和性、污点容忍、拓扑分布以及卷拓扑等。CPU/memory limits 和 QoS 并不是“调度所需资源”的替代品；LimitRange 与 ResourceQuota 在准入阶段起作用。Pod 已绑定后，普通的 `nodeSelector` 或 `requiredDuringSchedulingIgnoredDuringExecution` 条件变化通常不会把它自动搬走。

```bash
kubectl get pod -o wide
kubectl describe pod <Pending的Pod名>
kubectl get nodes --show-labels
kubectl describe node <节点名>
```

排查 `Pending` 时先看 Events 中的 `FailedScheduling`，识别是资源不足、污点、亲和性冲突还是存储卷约束，而不是反复删除 Pod。

## 2 指定节点与节点亲和性

`spec.nodeName` 直接指定节点，绕过普通调度器选择，可能仍因 kubelet 的资源、污点等运行条件无法启动；除特定系统场景外不推荐。`nodeSelector` 要求节点同时具有列出的全部标签。node affinity 支持更丰富的操作符及“必须满足/尽量满足”两类约束：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: affinity-demo
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: topology.kubernetes.io/zone
                operator: In
                values: ["zone-a", "zone-b"]
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 80
          preference:
            matchExpressions:
              - key: node-type
                operator: In
                values: ["ssd"]
  containers:
    - name: app
      image: nginx:stable
```

`required` 条件找不到节点时 Pod 会停留 `Pending`；`preferred` 只影响评分，不保证一定落到偏好节点。多个 `nodeSelectorTerms` 之间为“或”，同一 term 中多个要求为“且”。`IgnoredDuringExecution` 表示已运行 Pod 通常不会因标签后来变化而被驱逐。请使用真实且稳定的节点标签；`topology.kubernetes.io/zone` 与 `kubernetes.io/hostname` 是常见拓扑键。

## 3 Pod 亲和与反亲和

Pod affinity 依据**其他 Pod 的标签**把新 Pod 放到相同拓扑域，例如同一可用区；Pod anti-affinity 则尽量或强制分开相同类型副本，以降低单点故障。拓扑域由节点上的 `topologyKey` 标签定义。硬反亲和可能在节点数不足时使副本无法调度，因此资源规划和故障域标签必须先做好。

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app: web
          topologyKey: kubernetes.io/hostname
```

这是 Deployment `spec.template.spec` 下的字段节选，表示尽量不与其他 `app=web` Pod 同节点。若业务要求硬隔离，可改用 `requiredDuringSchedulingIgnoredDuringExecution`，但必须保证足够的可用节点。跨命名空间匹配时还要明确 `namespaces` 或 `namespaceSelector`，不能想当然地匹配全局 Pod。

## 4 污点与容忍

节点污点写成 `key=value:effect`，Pod 的 toleration 表示允许某类污点；**容忍并不保证会调度到该节点**，若需要吸引 Pod，还应配合节点亲和性。

| effect | 未容忍时的含义 |
| --- | --- |
| `NoSchedule` | 新 Pod 不会被调度到此节点，已有 Pod 不受影响 |
| `PreferNoSchedule` | 调度器尽量避开，非硬约束 |
| `NoExecute` | 新 Pod 不可调度，已有 Pod 可能被驱逐；可用 `tolerationSeconds` 延迟 |

```bash
kubectl taint nodes node1.bowen.org dedicated=infra:NoSchedule
kubectl describe node node1.bowen.org
# 清除同一污点
kubectl taint nodes node1.bowen.org dedicated=infra:NoSchedule-
```

相应的 Pod 模板节选：

```yaml
tolerations:
  - key: dedicated
    operator: Equal
    value: infra
    effect: NoSchedule
```

不要为了让业务 Pod 上控制平面就无差别删除 `node-role.kubernetes.io/control-plane` 污点；应先明确隔离目标和容量。节点失联等系统污点还涉及额外的默认容忍策略，不应与人为专用节点污点混淆。

## 5 拓扑分布约束

Pod anti-affinity 常表达“不能同域”，`topologySpreadConstraints` 则表达“各域尽量或必须均衡”。`maxSkew` 是匹配 Pod 数量相对最少合格拓扑域的最大偏差；`whenUnsatisfiable` 为 `DoNotSchedule` 时是硬约束，为 `ScheduleAnyway` 时成为打分偏好。

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: web
```

这也是 Pod 模板 `spec` 的字段节选。需先确保候选节点都有相应 zone 标签，考虑只有一个故障域、域数不足、污点过滤和节点亲和性的影响。均匀分布不能凭几次 `kubectl get pod -o wide` 的巧合推断，应检查每个副本的实际拓扑域。

## 6 优先级、抢占和节点压力驱逐

PriorityClass 是集群级对象，Pod 引用后获得优先级。资源不足时，调度器可能抢占较低优先级 Pod，为高优先级 Pod 腾出调度空间；这不保证高优先级 Pod 立即运行，也不会自动扩大集群。业务优先级要少而清晰，避免所有应用都被设置为“最高”。

节点压力驱逐由 kubelet 监测内存、磁盘、inode、PID 等阈值后触发；它与调度器的抢占不是同一机制。节点可能因 `MemoryPressure`、`DiskPressure` 等条件影响新 Pod 调度，已有 Pod 可能由 kubelet 按压力、资源使用、requests 和优先级选择驱逐。压力污点与驱逐阈值并非“统一加 NoExecute 污点后按 tolerationSeconds 逐个驱逐”这么简单。

```bash
kubectl describe node <节点名>
kubectl get pods -A --field-selector=status.phase=Failed
kubectl describe pod <被驱逐的Pod名> -n <命名空间>
```

排查时查看节点 Conditions、`Allocated resources`、kubelet Events 与磁盘/内存指标；被驱逐 Pod 原对象不会迁移，控制器会根据期望副本数创建替代实例。预防要从合理 requests/limits、镜像与日志清理、容量余量和故障域分布入手。
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/11-daemonset-jobs.html' | relative_url }}">← 上一章：DaemonSet、Job 与 CronJob</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/13-hpa-core-metrics.html' | relative_url }}">下一章：HPA 原理与核心指标 →</a>
</nav>
