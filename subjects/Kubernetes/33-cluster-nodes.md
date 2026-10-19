---
layout: default
title: 'Kubernetes · 节点增删与 Token 管理'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 33 节点增删与 Token 管理

节点维护不是简单地执行 `kubectl delete node`：它只删除 API 中的 Node 对象，不会重置机器上的 kubelet、CNI 或容器运行时，也不会替应用迁移本地数据。本章以 kubeadm 管理的集群为例，区分**短时维护、永久移除、故障替换、重新加入**。文中的节点名、地址、Token、哈希和密钥均须从当前集群取得，不能沿用旧日志里的示例值。

## 1. 先确认目标和节点状态

操作前记录集群版本、节点角色、Pod 分布和容器运行时。新节点的 kubeadm/kubelet 版本须与集群兼容，CRI Socket 须与本机运行时一致。

```bash
kubectl get nodes -o wide
kubectl describe node <NODE_NAME>
kubectl get pods -A --field-selector spec.nodeName=<NODE_NAME> -o wide
kubectl -n kube-system get cm kubeadm-config -o yaml
```

若只是短时维护，`cordon` 阻止新 Pod 调度，`drain` 驱逐可驱逐的现有 Pod，维护完成后 `uncordon`。此时不必删除 Node 对象或执行 `kubeadm reset`。

```bash
kubectl cordon <NODE_NAME>
kubectl drain <NODE_NAME> --ignore-daemonsets
# 维护完成并确认节点正常后
kubectl uncordon <NODE_NAME>
```

`drain` 可能被 PodDisruptionBudget 阻挡，应先调整副本与预算，而非直接强制驱逐。DaemonSet Pod 与静态 Pod 不会由它删除。仅在确认 `emptyDir` 临时数据可丢弃时，才加 `--delete-emptydir-data`；只有查清无控制器 Pod 的重建方式后，才考虑 `--force`。StatefulSet、本地卷和外部负载还需按应用的迁移方案处理。

## 2. 移除控制平面：先守住 etcd 法定多数

控制平面可能使用本地堆叠式 etcd，也可能使用外部 etcd。先检查拓扑、备份与剩余成员健康状况。三成员堆叠式 etcd 在其余两成员健康时可移除一个；两成员集群失去一个就不再有多数。若已失去多数，应先走备份恢复流程，不要继续盲目删成员。快照应存于节点之外且经过恢复验证；备份细节见下一章。

```bash
kubectl -n kube-system get pods -o wide | grep '^etcd-'
kubectl -n kube-system get cm kubeadm-config -o yaml
```

在**保留的健康控制平面节点**核对端点与成员。以下证书路径只适用于 kubeadm 默认堆叠式 etcd；其他部署方式应使用实际的端点和客户端证书。

```bash
KEEP_CP=<HEALTHY_CONTROL_PLANE_NODE>
kubectl -n kube-system exec "etcd-${KEEP_CP}" -- env ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key endpoint health
kubectl -n kube-system exec "etcd-${KEEP_CP}" -- env ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key member list -w table
```

### 2.1 计划移除健康的控制平面节点

先确认 API 负载均衡器仍有健康后端，并摘除待移除节点的后端。迁走业务工作负载，检查无遗留业务后删除 Node 对象，然后**登录待移除节点本机**执行 `kubeadm reset`。kubeadm 对本地 etcd 会尝试移除本机成员，因此不要预先手工重复执行 `member remove`。

```bash
REMOVE_CP=<CONTROL_PLANE_NODE_TO_REMOVE>
kubectl drain "$REMOVE_CP" --ignore-daemonsets
kubectl get pods -A --field-selector spec.nodeName="$REMOVE_CP"
kubectl delete node "$REMOVE_CP"

# 在 REMOVE_CP 本机执行；单一 CRI 且可自动识别时可省略 --cri-socket
sudo kubeadm reset -f --cri-socket=<CRI_SOCKET>
```

`reset` 不会清理用户 kubeconfig、全部网络规则或所有 CNI 配置。只有确实需要重装或更换 CNI，并核对文件内容后，才按该 CNI 的卸载说明清理；不要将清空 `/etc/cni/net.d` 作为固定步骤。

回到健康控制平面复查 Node、etcd 成员和端点。仅当待移除成员**仍残留**时，核对成员名与 Peer URL，确认 ID 确属目标，再删除该成员；如果 reset 已移除它，不要再次执行：

```bash
kubectl -n kube-system exec "etcd-${KEEP_CP}" -- env ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key member remove <VERIFIED_MEMBER_ID>
```

### 2.2 控制平面故障且无法执行 reset

先隔离故障主机，防止恢复后带旧身份意外重连；确认剩余 etcd 成员有法定多数、备份可用，并从负载均衡器摘除故障后端。随后检查节点上的工作负载与卷是否需手工迁移，再删除 API 中失效的 Node 对象。若使用堆叠式 etcd，且故障成员仍在成员列表中，依上节步骤仅移除核实过的故障成员；外部 etcd 应遵循其自身成员管理流程。替代主机准备好后再重新加入集群。

## 3. 增加或替换控制平面节点

先为新节点准备兼容版本的 kubelet、kubeadm、CRI、网络、主机名、时间同步与 API 地址解析。若复用旧主机，要先完成旧身份清理。使用外部 CA 管理证书的集群应遵循其证书分发流程，不适用默认的 `upload-certs` 示例。

在现存控制平面节点上传共享证书并生成**本次**加入命令。输出的证书密钥和 Bootstrap Token 都是敏感凭据；证书 Secret 与 Token 均有时效，过期要重新生成。

```bash
sudo kubeadm init phase upload-certs --upload-certs
# 将输出密钥保存为 CERTIFICATE_KEY
sudo kubeadm token create --print-join-command --certificate-key <CERTIFICATE_KEY>
```

在新控制平面节点执行实际生成的命令。下方仅示参数结构；`--control-plane` 只出现一次，多运行时机器需显式指定实际 CRI Socket。

```bash
sudo kubeadm join <API_ENDPOINT>:6443 \
  --token <BOOTSTRAP_TOKEN> \
  --discovery-token-ca-cert-hash sha256:<CA_CERT_HASH> \
  --control-plane --certificate-key <CERTIFICATE_KEY> \
  --cri-socket=<CRI_SOCKET>
```

加入后确认 Node 为 `Ready`、静态控制平面 Pod 正常、API 可访问；堆叠式 etcd 还需核对新成员及端点健康，最后才将新节点纳入 API 负载均衡器。仅有 `kubeadm join` 返回成功，不等于扩容完成。

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
kubectl -n kube-system get pods -o wide | grep '^etcd-'
```

新节点上若需使用 kubectl 管理集群，只将高权限的 `/etc/kubernetes/admin.conf` 复制给可信管理员，并设置合适权限；普通业务账户不应共享它。

## 4. Worker：移除、维护与重新加入

### 4.1 永久下线或更换 Worker

先检查该节点的 Pod、卷、PodDisruptionBudget 与其他节点容量。 `cordon` 仅阻止新调度，`drain` 才尝试驱逐已有 Pod；`kubectl delete node` 本身不会迁移业务。

```bash
WORKER=<WORKER_NODE_TO_REMOVE>
kubectl get pods -A --field-selector spec.nodeName="$WORKER" -o wide
kubectl cordon "$WORKER"
kubectl drain "$WORKER" --ignore-daemonsets
kubectl get pods -A --field-selector spec.nodeName="$WORKER" -o wide
kubectl delete node "$WORKER"
```

若 `drain` 因 `emptyDir` 或无控制器 Pod 停住，先确认数据是否可丢、Pod 如何重建，再按需分别加 `--delete-emptydir-data`、`--force`；这些不是默认安全选项。旧版 `--delete-local-data` 已弃用。

旧 Worker 仍可登录且准备退役或原机重新加入时，在**该 Worker 本机**执行 reset。它只重置 kubeadm 管理的状态，不会卸载容器运行时，也不会清除所有 CNI、iptables/IPVS 或用户 kubeconfig。剩余清理要结合 CNI 文档与机器复用计划，不应无差别删除目录。

```bash
sudo kubeadm reset -f --cri-socket=<CRI_SOCKET>
```

若 Worker 已失联，先删除 API 中 Node 对象并隔离旧主机，再部署替代主机；远程删除不会重置失联机器。若只是短时维护，则无需 `delete node` 或 reset，恢复后 `uncordon` 即可。

### 4.2 加入新 Worker

在控制平面节点生成实际加入命令，再到新 Worker 执行。不要把命令输出按终端自动换行拆成多条，也不要使用旧日志里的占位 Token。

```bash
# 控制平面节点
sudo kubeadm token create --print-join-command

# 新 Worker：执行上一条的实际输出；以下仅展示参数结构
sudo kubeadm join <API_ENDPOINT>:6443 \
  --token <BOOTSTRAP_TOKEN> \
  --discovery-token-ca-cert-hash sha256:<CA_CERT_HASH> \
  --cri-socket=<CRI_SOCKET>
```

确认新节点达到 `Ready`，网络插件、kube-proxy（如使用）及业务 Pod 均正常。若长时间 `NotReady`，先检查 kubelet 日志、CRI、CNI 与证书签发，而非不断创建新 Token。

```bash
kubectl get nodes -o wide
kubectl -n kube-system get pods -o wide
# 新 Worker 上排查
sudo systemctl status kubelet
sudo journalctl -u kubelet -n 100 --no-pager
```

## 5. Bootstrap Token 与 CA 哈希

Bootstrap Token 用于节点 TLS Bootstrap，不是永久的节点身份凭据。`kubeadm token list` 可查看用途与到期时间。Token 过期可新建；**新建不会自动撤销旧 Token**。扩容完成后检查长期 Token，删除不再需要的凭据。有效 Token 不应写入公开网页、工单或仓库。

```bash
sudo kubeadm token list
sudo kubeadm token create --ttl 2h --print-join-command
# 确认旧 Token 不再需要后
sudo kubeadm token delete <TOKEN_ID>
```

`--discovery-token-ca-cert-hash` 是集群 CA **公钥**的 SHA-256 哈希，用于校验发现的 API Server 身份，不是 Token 的哈希。更换 Token 通常不改变它；轮换 CA 才要重新获取。优先使用 `--print-join-command` 的输出，需独立核对时从当前 CA 证书计算：

```bash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt \
  | openssl pkey -pubin -outform DER \
  | openssl dgst -sha256 -hex
```

控制平面加入使用的 `--certificate-key` 是另一项独立凭据，用于解密 `upload-certs` 上传的共享证书；不要与 CA 哈希或 Token 混淆。加入命令失效时分别检查 Token TTL、证书 Secret 时效、API 连通性与 CA 哈希，而不是关闭发现校验。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/32-security-admission.html' | relative_url }}">← 上一章：准入控制</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/34-backup-restore.html' | relative_url }}">下一章：集群备份、恢复与迁移 →</a>
</nav>
