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

# 1 Kubernetes 集群中添加和删除节点

## 1.1 添加和删除 Master 节点

当一个Master出现故障时,需要添加或删除Master节点操作,从而修复节点后, 再重新加入集群,避免ETCD错误。

### 1.1.1 kubernetes 节点信息
```bash
[root@master1 ~]#kubectl get nodes
NAME                      STATUS   ROLES    AGE   VERSION
master1.bowen.org   Ready    master   56m   v1.17.2
master2.bowen.org   Ready    master   29m   v1.17.2
master3.bowen.org   Ready    master   29m   v1.17.2
node1.bowen.org          Ready    <none>   28m   v1.17.2
node2.bowen.org          Ready    <none>   23m   v1.17.2
node3.bowen.org          Ready    <none>   23m   v1.17.2
```

### 1.1.2 删除其中一个 Master 节点

注意：删除Master节点后，要保留至少半数以上个Master节点，否则集群失败。

当对删除其中的一个master节点时，可以执行下面操作。
```bash
#在保留的其中一个节点上master1执行下面操作，指定删除master3.bowen.org 节点
[root@master1 ~]#kubectl drain master3.bowen.org --ignore-daemonsets
[root@master1 ~]#kubectl delete node master3.bowen.org

#在master3执行删除本机上面的信息
[root@master3 ~]#kubeadm reset -f  --cri-socket=unix:///run/cri-dockerd.sock
[root@master3 ~]#rm -rf /etc/cni/net.d/ .kube
```

### 1.1.3 删除 Master 在etcd中信息
```bash
#进入容器
[root@master1 ~]#kubectl exec -it etcd-master1.bowen.org  -n kube-system -- sh
#在容器内列出节点的ID
# etcdctl --endpoints 127.0.0.1:2379 --cacert /etc/kubernetes/pki/etcd/ca.crt --
cert /etc/kubernetes/pki/etcd/server.crt --key
/etc/kubernetes/pki/etcd/server.key member list

cdc4bd12aef76ff, started, master2.bowen.org, https://10.0.0.102:2380,
https://10.0.0.102:2379, false
aaf08cd1e960ce20, started, master3.bowen.org, https://10.0.0.103:2380,
https://10.0.0.103:2379, false
f2fd0c12369e0d75, started, master1.bowen.org, https://10.0.0.101:2380,
https://10.0.0.101:2379, false

#根据上面命令列出的Master3节点的ID,在容器内删除相应节点
# etcdctl --endpoints 127.0.0.1:2379 --cacert /etc/kubernetes/pki/etcd/ca.crt --
cert /etc/kubernetes/pki/etcd/server.crt --key
/etc/kubernetes/pki/etcd/server.key member remove aaf08cd1e960ce20
```

### 1.1.4 获取添加 Master 的命令
```bash
#在master1节点执行,上传CA证书，并生成加入集群所需的key
[root@master1 ~]#kubeadm init phase upload-certs --upload-certs
......
[upload-certs] Storing the certificates in Secret "kubeadm-certs" in the "kube-
system" Namespace
[upload-certs] Using certificate key:
75d7b4c68674cff2f1bda7c69f668f2a850649031fb413e75096ee814307f9fe #记录此key

#生成添加控制平面节点的命令
[root@master1 ~]#kubeadm token create --print-join-command --certificate-key <上
面生成的key>
#结果如下
kubeadm join kubeapi.bowen.org:6443 --token BOOTSTRAP_TOKEN  --discovery-
token-ca-cert-hash
sha256:CA_CERT_HASH --
control-plane --control-plane --certificate-key
CERTIFICATE_KEY
```

### 1.1.5 将 Master 重新加入集群
```bash
#在需要加入的master节点上执行上面生成的命令，如下面操作加入集群
[root@master3 ~]#kubeadm join kubeapi.bowen.org:6443 --token
BOOTSTRAP_TOKEN  --discovery-token-ca-cert-hash
sha256:CA_CERT_HASH --
control-plane --control-plane --certificate-key
CERTIFICATE_KEY --cri-
socket=unix:///run/cri-dockerd.sock

To start administering your cluster from this node, you need to run the
following as a regular user:

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

Run 'kubectl get nodes' to see this node join the cluster.
```

### 1.1.6 授权Master管理功能
```bash
[root@master3 ~]#mkdir -p $HOME/.kube
[root@master3 ~]#sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
[root@master3 ~]#sudo chown $(id -u):$(id -g) $HOME/.kube/config

#验证节点加入
[root@master3 ~]#kubectl get nodes
NAME                 STATUS   ROLES                  AGE     VERSION
master1.bowen.org   Ready    control-plane,master   44h     v1.22.1
master2.bowen.org   Ready    control-plane,master   42h     v1.22.1
master3.bowen.org   Ready    control-plane,master   2m56s   v1.22.1
node1.bowen.org     Ready    <none>                 42h     v1.22.1
node2.bowen.org     Ready    <none>                 42h     v1.22.1
node3.bowen.org     Ready    <none>                 19m     v1.22.1
```

## 1.2 添加和删除 Worker 节点

### 1.2.1 添加新worker节点和删除worker节点说明

生产中,有时需要对 Worker 节点进行添加和删除操作。

缩容：

**排空节点上所有Pod**

delete node 删除节点，过一会儿上面的Pod自动迁移到其它节点，重启kubelet.service服务后会自动再加该节点回到集群中。

或者用下面方式立即驱离节点上面的Pod。

cordon：标记为不可被作为调度目标, uncordon：标记为可被作业调度目标。

drain：排空

下线节点

删除节点资源

**节点移除过程**
```bash
#在master节点上删除worker节点信息

#添加污点node.kubernetes.io/unschedulable:NoSchedule,只影响新Pod
kubectl cordon node3.bowen.org

#驱离要删除worker节点上的所有pod
kubectl drain node3.bowen.org --delete-emptydir-data --force --ignore-daemonsets

#从集群中删除节点
kubectl delete node node3.bowen.org

#在node节点上移除数据和历史记录文件
kubeadm reset
systemctl disable --now  kubelet docker
rm -rf /etc/kubernetes/ /etc/cni/net.d
```

**新worker节点加入集群**
```bash
#生成将worker节点加集群的命令
[root@master1 ~]#kubeadm token create --print-join-command

#在worker节点执行上面生成的命令结果,重新加入集群
[root@node3 ~]#kubeadm join kubeapi.bowen.org:6443 --token
BOOTSTRAP_TOKEN --discovery-token-ca-cert-hash
sha256:CA_CERT_HASH
```

### 1.2.2 范例: 删除再重新加入worker节点
```bash
#1)添加污点node.kubernetes.io/unschedulable:NoSchedule,只影响新Pod
[root@master1 ~]#kubectl cordon node3.bowen.org

#2)驱离已有的pod
#新版
[root@master1 ~]#kubectl drain node3.bowen.org --delete-emptydir-data  --force --
ignore-daemonsets
#旧版
[root@master1 ~]#kubectl drain node3.bowen.org --delete-local-data --force --
ignore-daemonsets
Flag --delete-local-data has been deprecated, This option is deprecated and will
be deleted. Use --delete-emptydir-data.
node/node3.bowen.org cordoned
WARNING: deleting Pods not managed by ReplicationController, ReplicaSet, Job,
DaemonSet or StatefulSet: default/test2; ignoring DaemonSet-managed Pods: kube-
system/kube-flannel-ds-rl6r4, kube-system/kube-proxy-cpzjl
evicting pod default/test2
evicting pod default/pod-test-5f7d8f9847-mn2bp
pod/pod-test-5f7d8f9847-mn2bp evicted
pod/test2 evicted
node/node3.bowen.org evicted

[root@master1 ~]#kubectl get nodes
NAME                 STATUS                     ROLES                  AGE
VERSION
master1.bowen.org   Ready                      control-plane,master   43h
v1.22.1
master2.bowen.org   Ready                      control-plane,master   41h
v1.22.1

master3.bowen.org   Ready                      control-plane,master   41h
v1.22.1
node1.bowen.org     Ready                      <none>                 41h
v1.22.1
node2.bowen.org     Ready                      <none>                 41h
v1.22.1
node3.bowen.org     Ready,SchedulingDisabled   <none>                 41h
v1.22.1

#3)删除节点
[root@master1 ~]#kubectl delete node node3.bowen.org
node "node3.bowen.org" deleted

[root@master1 ~]#kubectl get nodes
NAME                 STATUS   ROLES                  AGE   VERSION
master1.bowen.org   Ready    control-plane,master   43h   v1.22.1
master2.bowen.org   Ready    control-plane,master   41h   v1.22.1
master3.bowen.org   Ready    control-plane,master   41h   v1.22.1
node1.bowen.org     Ready    <none>                 41h   v1.22.1
node2.bowen.org     Ready    <none>                 41h   v1.22.1

#4)清除worker节点的k8s信息
[root@node3 ~]#kubeadm reset  --cri-socket=unix:///run/cri-dockerd.sock
[reset] WARNING: Changes made to this host by 'kubeadm init' or 'kubeadm join'
will be reverted.
[reset] Are you sure you want to proceed? [y/N]: y
[preflight] Running pre-flight checks
W0224 11:12:42.174404  107190 removeetcdmember.go:80] [reset] No kubeadm config,
using etcd pod spec to get data directory
[reset] No etcd config found. Assuming external etcd
[reset] Please, manually reset etcd to prevent further issues
[reset] Stopping the kubelet service
[reset] Unmounting mounted directories in "/var/lib/kubelet"
[reset] Deleting contents of config directories: [/etc/kubernetes/manifests
/etc/kubernetes/pki]
[reset] Deleting files: [/etc/kubernetes/admin.conf /etc/kubernetes/kubelet.conf
/etc/kubernetes/bootstrap-kubelet.conf /etc/kubernetes/controller-manager.conf
/etc/kubernetes/scheduler.conf]
[reset] Deleting contents of stateful directories: [/var/lib/kubelet
/var/lib/dockershim /var/run/kubernetes /var/lib/cni]

The reset process does not clean CNI configuration. To do so, you must remove
/etc/cni/net.d
```


The reset process does not reset or clean up iptables rules or IPVS tables. If you wish to reset iptables, you must do so manually by using the "iptables"command.

```text
If your cluster was setup to utilize IPVS, run ipvsadm --clear (or similar)
to reset your system's IPVS tables.
```


The reset process does not clean your kubeconfig files and you must remove them manually. Please, check the contents of the $HOME/.kube/config file.

```bash
[root@node3 ~]#systemctl stop  kubelet docker

[root@node3 ~]#rm -rf /etc/kubernetes/ /etc/cni/net.d

#重新加集群
#1)生成将worker节点加集群的命令
[root@master1 ~]#kubeadm token create --print-join-command
kubeadm join kubeapi.bowen.org:6443 --token BOOTSTRAP_TOKEN --discovery-
token-ca-cert-hash
sha256:CA_CERT_HASH

#2)在worker节点执行命令,重新加入集群
[root@node3 ~]#kubeadm join kubeapi.bowen.org:6443 --token
BOOTSTRAP_TOKEN --discovery-token-ca-cert-hash
sha256:CA_CERT_HASH  --cri-
socket=unix:///run/cri-dockerd.sock
[preflight] Running pre-flight checks
[preflight] Reading configuration from the cluster...
[preflight] FYI: You can look at this config file with 'kubectl -n kube-system
get cm kubeadm-config -o yaml'
[kubelet-start] Writing kubelet configuration to file
"/var/lib/kubelet/config.yaml"
[kubelet-start] Writing kubelet environment file with flags to file
"/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Starting the kubelet
[kubelet-start] Waiting for the kubelet to perform the TLS Bootstrap...
```


This node has joined the cluster:* Certificate signing request was sent to apiserver and a response was received.* The Kubelet was informed of the new secure connection details.

```bash
Run 'kubectl get nodes' on the control-plane to see this node join the cluster.

#验证加入成功
[root@master1 ~]#kubectl get nodes
NAME                 STATUS   ROLES                  AGE   VERSION
master1.bowen.org   Ready    control-plane,master   43h   v1.22.1
master2.bowen.org   Ready    control-plane,master   41h   v1.22.1
master3.bowen.org   Ready    control-plane,master   41h   v1.22.1
node1.bowen.org     Ready    <none>                 41h   v1.22.1
node2.bowen.org     Ready    <none>                 41h   v1.22.1
node3.bowen.org     Ready    <none>                 11s   v1.22.1
```

## 1.3 Token 管理

默认情况下，kubeadm在创建集群的时候，会使用tls的方式传输信息，而node在加入集群的时候，也会应用该即token信息 ，如果忘了保存,也可以通过如下方式来获取，然后将kubeadm join的命令更改一下即可。

### 1.3.1 查看当前 token
```bash
#查看token的时效
kubeadm token list

#查看hash值
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -
outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'

#生成添加Worker节点命令
kubeadm join kubeapi.bowen.org:6443 --token <token值> --discovery-token-ca-cert-
hash sha256:<hash值>
```

范例:
```bash
[root@master1 ~]#kubeadm token list
TOKEN      TTL         EXPIRES   USAGES         DESCRIPTION
EXTRA GROUPS
BOOTSTRAP_TOKEN   <forever>   <never>   authentication,signing   The
default bootstrap token generated by 'kubeadm init'.
system:bootstrappers:kubeadm:default-node-token

[root@master1 ~]#openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl
rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
cf6d6b66275bd9917563004bc6f71eb3391f083dcd434d109361ea0a7e5db2a8

#利用上面信息生成加入Worker节点的命令
[root@nodeX ~]#kubeadm join kubeapi.bowen.org:6443 --token
BOOTSTRAP_TOKEN \
--discovery-token-ca-cert-hash
sha256:CA_CERT_HASH
```

### 1.3.2 重新生成 token

如果Token过期,也可以重新生成 Token 信息,但原有token还可以使用。
```text
kubeadm token create --print-join-command
```

范例:
```bash
[root@master1 ~]#kubeadm token create --print-join-command
#生成以下信息
kubeadm join kubeapi.bowen.org:6443 --token BOOTSTRAP_TOKEN --discovery-
token-ca-cert-hash
sha256:CA_CERT_HASH
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/32-security-admission.html' | relative_url }}">← 上一章：准入控制</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/34-backup-restore.html' | relative_url }}">下一章：集群备份、恢复与迁移 →</a>
</nav>
