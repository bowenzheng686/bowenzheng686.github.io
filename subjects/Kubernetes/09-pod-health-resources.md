---
layout: default
title: 'Kubernetes · Pod 健康、资源、安全与设计模式'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 09 Pod 健康、资源、安全与设计模式

## 3.3 Pod 健康检查

容器进程仍在运行，并不代表它已能处理请求。kubelet 可针对**每个容器**配置三类探针：`startupProbe` 保护慢启动过程，`livenessProbe` 判断是否需要重启容器，`readinessProbe` 判断是否可接收 Service 流量。探针失败不会“重置整个 Pod”：存活探针触发的是相应容器重启；就绪探针失败会让 Pod 暂时退出可服务端点，但容器继续运行。

| 探针 | 失败后的主要动作 | 适用判断 |
| --- | --- | --- |
| 启动探针 | 未达阈值前暂不执行存活/就绪探针；最终失败则重启容器 | 应用是否已完成启动 |
| 存活探针 | 重启该容器 | 应用是否已陷入不可恢复的卡死 |
| 就绪探针 | 从 Service 可用端点移出，恢复后重新加入 | 此刻是否能接收新流量 |

执行机制不止旧记录中的三种：`exec` 在容器内运行命令；`httpGet` 发 HTTP 请求；`tcpSocket` 检查连接能否建立；支持的 Kubernetes 版本还可使用 `grpc`。TCP 连接成功只表示端口开放，不保证业务就绪；HTTP 端点应区分“活着”和“已准备好”，避免依赖外部服务的小波动触发重启风暴。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: health-demo
  labels:
    app: health-demo
spec:
  containers:
    - name: web
      image: nginx:stable
      ports:
        - containerPort: 80
      startupProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 5
        failureThreshold: 24
      readinessProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 5
        failureThreshold: 2
      livenessProbe:
        httpGet:
          path: /
          port: 80
        periodSeconds: 10
        failureThreshold: 3
```

这组阈值给启动过程约 120 秒窗口，具体值必须根据应用启动分布和故障恢复目标调整。验证时看 `kubectl describe pod health-demo` 的 Events、`kubectl get pod health-demo -o yaml` 中的容器状态及 Service 的 EndpointSlice；不要仅凭 `Running` 推断就绪。

## 3.4 CPU、内存与配额

`requests` 表示调度器为容器预留的资源估计，也用于资源分配和 QoS；`limits` 是运行时上限。CPU 是可压缩资源，达到 limit 时主要表现为节流；内存不可压缩，超过 limit 可能导致容器 `OOMKilled`。节点内存压力也可能触发 Pod 驱逐，而“驱逐到其他宿主机”并非原 Pod 自动迁移：控制器通常会创建一个新 Pod。

`1` CPU 大致代表一个逻辑核的计算配额，`100m` 为 0.1 CPU。内存 `Mi` 为二进制单位，`M` 为十进制单位；`400m` 不能表示 400 MB。资源字段写在每个容器的 `resources` 下：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-demo
spec:
  containers:
    - name: app
      image: nginx:stable
      resources:
        requests:
          cpu: 100m
          memory: 64Mi
        limits:
          cpu: 500m
          memory: 256Mi
```

调度时先比较 requests 与节点的可分配资源；limit 并不保证一定能在节点上获得该用量。`kubectl top pod` 依赖 Metrics Server，只能看近期使用量，不能替代容量规划和长周期监控。需要判断节流与 OOM 时结合容器指标、`kubectl describe pod` 的 Last State/Events 和节点压力。

`LimitRange` 在一个命名空间内为单个 Pod/容器设置默认值、最小值和最大值；`ResourceQuota` 限制该命名空间的总 requests、limits、对象数量等。它们并不彼此替代：如果配额要求每个容器都声明 requests/limits，可用 LimitRange 提供默认值，或在清单中显式设置。先用 `kubectl describe limitrange -n <空间>` 与 `kubectl describe resourcequota -n <空间>` 理解当前策略，再解释创建失败的准入错误。

## 3.5 Pod 安全上下文

`securityContext` 决定容器进程的 UID/GID、Linux capabilities、文件系统和特权等运行属性，可在 Pod 级和容器级配置；同名字段的容器级设置通常覆盖 Pod 级。旧记录中的 PodSecurityPolicy（PSP）已被移除，当前集群可用 Pod Security Admission 的命名空间级 `enforce/audit/warn` 标签配合准入策略，并与 RBAC、NetworkPolicy、镜像来源控制共同使用。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: restricted-demo
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: nginxinc/nginx-unprivileged:stable
      ports:
        - containerPort: 8080
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
```

此清单仅展示字段关系；只读根文件系统要求镜像把缓存、临时文件和日志写入可写 Volume 或标准输出，实际应用前应先测试。`runAsNonRoot` 要与镜像中的用户和端口相容。不要默认加 `privileged: true` 或 `SYS_ADMIN`；先识别真正需要的系统调用与能力，按最小权限授予。`hostNetwork`、`hostPID`、`hostPath` 会扩大与节点的耦合，也应单独审查。

Pod 级 `sysctls` 只能设置集群允许的内核参数，安全与非安全 sysctl 的可用范围取决于 Kubernetes、kubelet 配置和节点内核；共享节点的全局内核参数不能因单个 Pod 的请求而无约束修改。

## 3.6 QoS 与驱逐

Kubernetes 根据资源 requests/limits 自动归类 Pod 的 QoS，并非用户手工设置一个独立的“QoS 级别”字段：

| 类别 | 条件 | 内存压力下的意义 |
| --- | --- | --- |
| `Guaranteed` | 每个容器的 CPU、内存 request 与 limit 都存在且相等 | 通常比其他类别更晚被驱逐 |
| `Burstable` | 不满足 Guaranteed，但至少有资源 request 或 limit | 还要结合实际使用与超额情况 |
| `BestEffort` | 所有容器均未指定 CPU、内存 request/limit | 压力下优先驱逐 |

QoS 不是服务可用性承诺，也不能防止自身超过 memory limit 后被 OOMKill。驱逐还取决于节点资源压力、使用量和优先级；Pod Priority 与 QoS 是两个不同机制。

## 3.7 多容器 Pod 的设计模式

只有需要共享 Pod 网络、Volume 和生命周期的紧耦合组件，才适合放在同一个 Pod；否则拆为独立工作负载并通过 Service 通信，更便于扩容与故障隔离。

- **Init container** 在普通应用容器启动前依次运行并完成，可准备配置、等待必要的本地前置条件；不应无限循环地等待外部系统。
- **Sidecar** 与主容器协同工作，例如日志收集或代理。常规 sidecar 作为普通容器运行；支持原生 sidecar 的集群也可把 `restartPolicy: Always` 的 init container 用于更明确的启动/终止顺序。须按集群版本确认其语义。
- **Ambassador** 在 Pod 内代理主应用的对外请求，屏蔽服务发现或连接细节。
- **Adapter** 将主容器的输出转换为统一格式，如把应用指标转成 Prometheus 可抓取的格式。

下面的清单用共享 `emptyDir` 演示“先准备文件，再让应用读取”。镜像与命令应按实际应用替换：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: init-demo
spec:
  volumes:
    - name: shared
      emptyDir: {}
  initContainers:
    - name: prepare
      image: busybox:stable
      command: ["/bin/sh", "-c", "echo ready > /work/status.txt"]
      volumeMounts:
        - name: shared
          mountPath: /work
  containers:
    - name: app
      image: busybox:stable
      command: ["/bin/sh", "-c", "cat /work/status.txt; sleep 3600"]
      volumeMounts:
        - name: shared
          mountPath: /work
```

`emptyDir` 与 Pod 生命周期绑定，Pod 被替换后数据丢失；持久化状态应使用 PVC。无论选哪种模式，都要分别设计每个容器的资源请求、健康检查和失败时的行为，避免辅助容器故障导致主服务一直不可用。
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/08-pod-basics-lifecycle.html' | relative_url }}">← 上一章：Pod 基础与工作机制</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/10-workload-controllers.html' | relative_url }}">下一章：控制器、标签与 Deployment →</a>
</nav>
