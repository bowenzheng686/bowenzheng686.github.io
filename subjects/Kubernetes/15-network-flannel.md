---
layout: default
title: 'Kubernetes · 网络基础与 Flannel'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 15 网络基础与 Flannel

## 1 Kubernetes 的网络模型

Kubernetes 至少涉及三类地址：**节点地址**用于主机与控制平面互通，**Pod 地址**用于工作负载通信，**Service 虚拟地址**由 kube-proxy 或其他数据平面实现稳定服务访问。三个地址段必须规划为互不重叠；Service IP 不是某个固定节点上的真实网卡地址。

基本目标是每个 Pod 有自己的 IP，同一 Pod 内容器共享网络命名空间，不同节点的 Pod 在允许的网络策略下可互通。容器运行时在创建 Pod sandbox 时调用 CNI 插件，插件负责把网络接口接入 Pod 网络、分配 IP、设置路由等；kubelet 与运行时通过 CRI/CNI 协同，而不是 kube-scheduler直接配置网卡。

### 1.1 Veth、网桥与 Underlay/Overlay

`veth` 是一对虚拟以太网接口，常用一端放进 Pod 网络命名空间，另一端连到节点上的网桥 `cni0`。Pod 同节点通信可经网桥转发；跨节点通信还需隧道或路由。veth 本身只是接口，不等于 VXLAN，也不会自动产生额外 IP 封装。

**Underlay** 指实际承载报文的节点网络；**Overlay** 在其上封装逻辑网络流量。VXLAN 把以太网帧封进 UDP/IP 报文，允许 Pod 网段跨不同三层节点网络，但增加封装开销和 MTU 需求。MACVLAN/IPVLAN 是其他接入方式：MACVLAN 常让子接口有独立 MAC，IPVLAN 可共享父接口 MAC；它们是否适合取决于交换机、云网络和 IP 地址管理能力，不是 Flannel 默认转发路径。

选择网络插件时，应同时评估节点网络是否允许所需 UDP/路由协议、Pod CIDR 与主机网段是否冲突、网络策略要求、可观测性、性能、升级支持及云厂商集成。Flannel 偏重简洁的 Pod 网络互通；若需要原生、细粒度的 NetworkPolicy，应确认另有可执行策略的插件或选择 Calico/Cilium 等方案，不能仅创建 NetworkPolicy 对象就认定隔离生效。

## 2 Flannel 的节点间通信

Flannel 为不同节点分配不重叠的 Pod 子网，并通过后端机制使跨节点报文到达目标节点。每个节点上的 CNI 配置将 Pod 接入本地子网；Flannel 与 CNI 插件、IPAM 插件共同完成网络接入和跨节点转发。安装前，`kubeadm init --pod-network-cidr` 与 Flannel 网络配置要一致；在使用 Kubernetes subnet manager 的部署中还要确认节点已分配 `spec.podCIDR`。

### 2.1 VXLAN 后端

默认 VXLAN 模式通常创建 `flannel.1` 设备，将跨节点 Pod 报文封装为 UDP 8472 的外层报文（具体端口以所用 Flannel 配置为准）。节点网络只需能互通这些外层地址与端口，不必直接路由每一个 Pod 子网。数据路径概念上为：

```text
源 Pod → veth/cni0 → flannel.1 封装 → 节点网络 → 目标 flannel.1 解封装 → cni0/veth → 目标 Pod
```

隧道封装使有效 MTU 小于底层网卡 MTU；如小报文可通、大报文卡住，除防火墙外还要检查路径 MTU、Flannel 配置与云网络的额外封装。VXLAN 的 MAC/FDB 与内核路由表可帮助定位目的节点，但不要把抓包中的外层节点 IP 误当成 Pod IP。

### 2.2 host-gw 与 DirectRouting

`host-gw` 不封装跨节点报文，而是给远端 Pod 子网安装以远端节点 IP 为下一跳的路由。它通常要求节点在可直接以彼此为网关的同一二层网络，或底层网络另有明确的路由保障；仅“IP 能 ping 通”不足以保证所有节点都能作为下一跳。它减少封装开销，但受网络拓扑约束更强。

VXLAN 后端的 `DirectRouting` 在节点可直接路由的同网段场景走直连路由，其他节点仍走 VXLAN，兼顾部分直连性能与跨网段连通。它并不自动解决所有跨子网路由、MTU 或云网络安全组问题。三种模式是替代/组合关系，不应同时复制多套相互矛盾的 ConfigMap 示例。

### 2.3 部署与验证

从 [Flannel 发布页](https://github.com/flannel-io/flannel/releases) 选择与目标 Kubernetes 版本兼容的固定发布清单，先审查镜像、Pod 网段、RBAC、CNI 配置和后端参数，再保存为本地文件。不要直接应用不断变化的 `master` 分支。以下假定清单文件为 `kube-flannel.yml` 且网络为 `10.244.0.0/16`：

```bash
kubectl apply -f ./kube-flannel.yml
kubectl -n kube-flannel get daemonset,pod -o wide
kubectl -n kube-flannel rollout status daemonset/kube-flannel-ds --timeout=180s
kubectl get nodes -o wide
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
```

不同发布版本的命名空间和 DaemonSet 名称可能变化，以实际清单为准。`Ready` 只说明节点网络基本可用，还应在**不同节点**放置测试 Pod，验证 Pod IP 互通、DNS 和 Service 访问；测试 Pod 应使用可控镜像，并在结束后清理。

在节点上可用以下只读命令观察数据路径：

```bash
ip addr show cni0
ip addr show flannel.1
ip route
bridge fdb show dev flannel.1
ss -ulnp | grep 8472
```

`host-gw` 模式可能没有 `flannel.1`，因此不能把该接口不存在一律判作故障。排错从 `kubectl -n kube-flannel logs <Pod名>`、节点 `journalctl -u kubelet -u containerd`、`/etc/cni/net.d` 实际加载配置、节点 PodCIDR、路由与安全组逐层检查。若 CNI 配置冲突，先备份并识别来源，不直接删除整个目录或重启所有节点。

### 2.4 修改后端的边界

变更 `VXLAN`、`host-gw` 或 `DirectRouting` 涉及全体节点的路由与 Pod 网络连接，不是只编辑 ConfigMap 就立即无损生效。先在测试集群验证底层网络条件、MTU、防火墙和跨节点通信；生产环境应安排维护窗口，备份现有清单，按所用 Flannel 版本的升级说明滚动更新 DaemonSet，并准备回退。更新后用多节点 Pod、Service 与 DNS 的实际请求验证，而不是只看 flannel Pod 为 `Running`。
{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/14-hpa-custom-metrics.html' | relative_url }}">← 上一章：自定义指标、Prometheus Adapter 与 KEDA</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/16-calico-network.html' | relative_url }}">下一章：Calico 网络部署与管理 →</a>
</nav>
