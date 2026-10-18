---
layout: default
title: 'Kubernetes · Calico 网络部署与管理'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 16 Calico 网络部署与管理

## 3.1 Calico 解决什么问题

Calico 为 Kubernetes Pod 提供跨节点网络连接和网络策略执行。它与 Flannel 不是简单的“增强版”关系：两者的数据路径、路由模式和运维复杂度不同。Calico 可采用 Linux 路由配合 BGP，也可用 IP-in-IP 或 VXLAN 封装；是否需要 BGP 取决于选定的数据平面模式。网络策略只有在 Calico 等实际执行策略的组件工作正常时才生效。

在常见 Linux 数据平面中，Pod 的 veth 对一端位于 Pod，另一端在节点上表现为 `cali...` 接口；节点上的路由和策略规则处理 Pod 流量，通常不像 Flannel 那样借助 `cni0` 网桥。`Felix` 负责节点路由与策略编程，`calico-kube-controllers` 同步相关 Kubernetes 状态；采用 BGP 的模式还涉及路由进程与 peer，较大集群可引入 Typha 降低 API watch 压力。具体组件会随 Calico 发布版本和选用的数据平面变化，不应把旧版清单中的进程名当成永久固定结构。

### 3.1.1 地址池与节点 PodCIDR

Calico IPPool 定义可分配给 Pod 的网段与封装模式。地址池不得与节点、Service 或其他现有网络重叠，所选 CIDR 应与集群规划保持一致。`kubeadm init --pod-network-cidr` 可让控制平面分配 Node PodCIDR，但 Calico 的 IPAM 不一定直接使用 `Node.spec.podCIDR`：要看安装清单的 IPAM 模式和 IPPool 配置。不要认为 kubeadm 参数会自动覆盖 Calico 自身的地址池。

## 3.2 三种典型跨节点数据路径

| 模式 | 节点间流量 | 对底层网络的要求 | 常见检查点 |
| --- | --- | --- | --- |
| 原生路由/BGP | 不封装 Pod IP，向其他节点或上游路由器传播 Pod 路由 | 底层网络必须能转发 Pod 网段，BGP peer/路由策略正确 | BGP 会话、路由表、反欺骗策略 |
| IP-in-IP | 将 Pod IP 包再封装在外层 IP 包中，Calico 仍需分发相关路由信息 | 允许 IP 协议号 4，MTU 足够 | `tunl0`、路由、BGP 状态 |
| VXLAN | 用 UDP 封装 Pod 流量，通常不依赖 BGP 传播路由 | 允许 VXLAN UDP 端口（Calico 常用 4789），MTU 足够 | `vxlan.calico`、封装路由、UDP 放通 |

**BGP 不要求所有节点都在同一个二层网段。** 跨子网能否使用原生路由，取决于底层路由器或云网络能否学习、接受并转发 Pod 路由。公有云可能因源/目的检查或 BGP 限制不适合原生路由，此时考虑受支持的 VXLAN 或云厂商专用 CNI。

`CrossSubnet` 是封装策略：同一底层子网的节点可直接路由，跨子网时才封装。`IPIP CrossSubnet` 仍需满足 IPIP 模式的路由分发要求；`VXLAN CrossSubnet` **不等同于“VXLAN 加 BGP”**。不要同时给同一地址池开启相互冲突的 IPIP 与 VXLAN 模式。封装会减少有效 MTU；跨节点大包异常时要检查节点网卡、云网络与 Pod 接口 MTU。

## 3.3 安装与验证

先选与 Kubernetes 版本兼容的固定 Calico 发布版，阅读 [Calico 安装要求](https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements) 和该发布版清单。新集群优先按该版本推荐的 Operator 流程安装，并在自定义资源里明确 Pod CIDR 与封装模式；旧式直接应用单个大 YAML 的做法只适用于对应发布版，不要把不同版本的清单、镜像和 CRD 混用。

```bash
# 下列两个文件先从同一固定发布版本下载、审查，再保存到本地
kubectl apply -f ./tigera-operator.yaml
kubectl apply -f ./custom-resources.yaml
kubectl get pods -n tigera-operator
kubectl get pods -n calico-system -o wide
kubectl get nodes -o wide
```

不同安装方式可能使用 `calico-system` 或 `kube-system` 命名空间，以所选清单为准。切换 Flannel→Calico 不是无损“删除旧清单、立即应用新清单”：节点 CNI 配置、Pod 网络、策略和路由都会变化。生产迁移应在测试环境验证、备份现有配置、安排维护窗口，并遵循所用发布版的迁移文档。

跨节点测试必须让两个测试 Pod 分布在不同节点，再检查 Pod IP 互通、DNS 和 Service 访问；若只测同节点通信，无法验证封装或 BGP。观察节点数据路径时可用：

```bash
ip route
ip -d link show tunl0
ip -d link show vxlan.calico
kubectl get pods -A -o wide
```

`tunl0` 与 `vxlan.calico` 不会在每一种模式中同时存在；缺少某一接口要结合 IPPool 模式判断。若 Pod 无法跨节点访问，依次核查 IPPool 与节点 PodCIDR、CNI 插件日志、节点防火墙/安全组、BGP peer 或 VXLAN/IPIP 封装端口、路由和 MTU，而不是直接清空 `/etc/cni/net.d`。

## 3.4 calicoctl、地址池与 BGP 管理

`calicoctl` 应与集群 Calico 版本匹配，通过受控的 Kubernetes Datastore 配置访问 Calico API。先用只读命令确认现状，再编辑 IPPool 或 BGP 配置；不要在正在承载业务 Pod 的地址池上直接改 CIDR、`blockSize` 或封装模式。现有地址分配与节点路由可能不会仅靠字段修改就完成迁移。

```bash
calicoctl version
calicoctl get ippool -o wide
calicoctl get ippool -o yaml
calicoctl node status
```

少量节点的 BGP mesh 比较直观；规模较大时可使用 Route Reflector 减少全互联 peer 数量。但 RR 的数量、故障域、BGP ASN、peer 关系和切换顺序都须提前设计。先让 RR 与所有节点建立稳定会话并验证路由，再考虑关闭 node-to-node mesh；反过来操作会让 Pod 路由短暂或持续丢失。VXLAN-only 部署不需要仅为“优化”而照搬 RR 配置。

网络策略可在下一章按命名空间与标签逐步实施。上线策略前先观察现有流量和 DNS 依赖，避免把“Calico Pod 都是 Running”误当成业务连通与策略正确的充分证据。
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/15-network-flannel.html' | relative_url }}">← 上一章：网络基础与 Flannel</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/17-network-policy.html' | relative_url }}">下一章：网络策略 →</a>
</nav>
