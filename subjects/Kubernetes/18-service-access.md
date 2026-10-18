---
layout: default
title: 'Kubernetes · Service 访问与负载分发'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 18 Service 访问与负载分发

## 1 Service 为什么需要独立于 Pod

Pod IP 会随重建变化，Service 用稳定的名称和虚拟访问方式表示一组后端。带 `selector` 的 Service 依据 Pod 标签发现后端，EndpointSlice 保存分片后的端点地址、端口和就绪条件；创建 Service 不代表一定有可用端点，必须检查标签与 Pod readiness。旧的 Endpoints 对象仍可能可见，但新集群应优先理解 EndpointSlice 的可扩展发现模型。

```bash
kubectl get service
kubectl get endpointslices -l kubernetes.io/service-name=<服务名>
kubectl describe service <服务名>
kubectl get pods -l app=<标签值> -o wide
```

`ClusterIP` 是集群内服务地址，不是某个节点网卡上的 Pod IP。集群 DNS 通常把 `服务名.命名空间.svc.cluster.local` 解析到 ClusterIP；数据平面再把流量转给后端。Service 不是应用层代理，不会自动解决 HTTP 路径路由、认证或容器本身的健康问题。

## 2 数据平面与 kube-proxy

kube-proxy 观察 Service 和 EndpointSlice，在节点配置转发规则。历史上有 userspace、iptables、IPVS 等模式；userspace 是早期方案，不应用作当前新集群的默认选择。iptables 与 IPVS 各有内核模块、规则维护和性能特性；具体可用模式及默认值随 Kubernetes 版本变化，不能简单声称“IPVS 已成为默认”。某些 CNI（如 eBPF 数据平面）可替代 kube-proxy 的 Service 转发，因此实际排错要先确认集群采用哪种实现。

```bash
kubectl -n kube-system get configmap kube-proxy -o yaml
kubectl -n kube-system get daemonset kube-proxy
kubectl get endpointslices -l kubernetes.io/service-name=<服务名>
```

请求失败时沿“DNS → Service 端口 → EndpointSlice 是否非空且就绪 → Pod 端口/探针 → 节点数据平面与网络策略”逐层检查。把 `ClusterIP` 当成节点接口地址或只根据 `kubectl get svc` 的存在判断可访问，都会误导定位。

## 3 Service 类型与访问范围

| 类型 | 主要用途 | 前提 |
| --- | --- | --- |
| `ClusterIP` | 集群内稳定服务 | 客户端能到达集群 Service 网络 |
| `NodePort` | 在节点端口暴露 TCP/UDP 服务 | 节点地址和端口对客户端可达 |
| `LoadBalancer` | 由云厂商或集群负载均衡控制器提供外部入口 | 已安装相应 LB 实现并配置地址池/权限 |
| `ExternalName` | 在集群 DNS 中返回外部名称的 CNAME | 客户端自行解析并连接目标名称 |

`ExternalName` **不**创建代理或转发规则，也不保证 TLS 证书名称匹配。`externalIPs` 是 Service 的额外接收地址字段，不是一种 Service 类型；Kubernetes 不会替你分配或宣告这些 IP，底层网络必须把流量路由到节点，且要考虑安全与地址冲突。

### 3.1 创建可用的 ClusterIP/NodePort

先部署带 `app=demo` 标签的 Pod，再创建与之匹配的 Service。下面是 Service 清单：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo
spec:
  type: ClusterIP
  selector:
    app: demo
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
```

`port` 是 Service 面向客户端的端口，`targetPort` 是后端 Pod 的端口；`containerPort` 只是 Pod 清单中的声明，不会自动打开端口。若应用容器实际监听 80，则 `targetPort` 也应改成 80。应用后检查 EndpointSlice 的端口与地址是否符合预期。

需要从集群外测试时，可把 `type` 改为 `NodePort`；若未显式指定 `nodePort`，API Server 在其配置范围内动态分配，常见默认范围为 30000–32767。防火墙、网络策略和云安全组要允许访问，客户端使用 `节点IP:实际NodePort`。NodePort 并不是生产中“必然不用”的模式，是否适合取决于边界网络、流量规模和上层负载均衡方式。

`externalTrafficPolicy: Local` 可避免跨节点二次转发并通常保留外部客户端源 IP，但只有拥有就绪本地端点的节点能处理对应流量；上层 LB 要进行健康检查。`Cluster` 模式可在节点间转发，源地址保留语义因具体数据路径而异。变更这一字段前，应检查节点端点分布和 LB 健康检查。

### 3.2 LoadBalancer、MetalLB 与 OpenELB

云环境的 LoadBalancer Service 通常由云控制器创建外部 LB；裸金属集群若没有相应控制器，`EXTERNAL-IP` 可能持续 `<pending>`。MetalLB 或 OpenELB 等实现可以为此提供地址分配与通告，但两者是方案选择，不应在同一地址池上无规划地同时部署。先确认二层通告或 BGP 模式、可用地址池、路由器配置、故障切换与防火墙，再安装与当前 Kubernetes 版本兼容的固定发行版。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-public
spec:
  type: LoadBalancer
  selector:
    app: demo
  ports:
    - name: http
      port: 80
      targetPort: 8080
```

此清单只申请外部入口；是否获得 IP、哪些节点接流量由集群 LB 实现决定。不要仅为消除 `pending` 就给 Service 手填一个未在网络中宣告的 `externalIPs`。

### 3.3 ExternalName 与无选择器 Service

`ExternalName` 仅返回 CNAME，适合给集群外的 DNS 名称提供内部别名：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.example.net
```

若需要为集群外**固定 IP** 提供 ClusterIP 入口，可创建**无 selector** 的 Service 并自行维护 EndpointSlice；此时必须明确端点地址、端口、生命周期和信任边界。API Server 代理端点、端口转发等行为对无 selector Service 有限制，不能当作普通 Pod Service 完全等价使用。

## 4 会话亲和性与负载行为

Service 默认并不承诺严格轮询或请求均匀分布；同一 TCP 连接会保持到一个后端，HTTP keep-alive 也会影响观察到的比例。`sessionAffinity: ClientIP` 可让同一源 IP 在一定时间内倾向同一后端，但经 NAT 的多个用户可能共享源 IP，故它不是可靠的用户会话存储方案。应用状态应放到共享存储或外部会话系统，不依赖 Pod 粘性保证正确性。

```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

这是 Service `spec` 的节选。验证分发时应使用多个连接、多个客户端，并结合后端日志；只连续在同一连接上 `curl` 不足以验证负载均衡策略。

## 5 综合应用时的检查顺序

原 WordPress/MySQL 案例涉及命名空间、Deployment、持久化存储和多个 Service。阅读这类方案时先分清：MySQL 用仅供集群内部访问的 Service，WordPress 可由 ClusterIP 配合 Ingress/Gateway 暴露；数据库数据必须由 PVC 或外部数据库承载，而不是依赖 Pod 文件系统。分别核对两个 Service 的 selector、EndpointSlice、端口映射与探针，再测试应用到数据库的 DNS、凭据和网络策略。完整存储拓扑在后续存储专题展开，避免把一个长终端记录当作可复用生产清单。
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/17-network-policy.html' | relative_url }}">← 上一章：网络策略</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/19-dns-headless-service.html' | relative_url }}">下一章：服务发现、CoreDNS 与 Headless Service →</a>
</nav>
