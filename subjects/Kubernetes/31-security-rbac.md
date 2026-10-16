---
layout: default
title: 'Kubernetes · 授权机制与 RBAC'
subject_page: true
kubernetes_notes: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 31 授权机制与 RBAC

# 3 授权机制

## 3.1 授权机制

授权主要是在认证的基础上，用于对集群资源的访问控制权限设置，通过检查请求包含的相关属性值，与相对应的访问策略相比较，API请求必须满足某些策略才能被处理。对于k8s集群会根据实际的业务应用场景，采用不同级别的授权方式，称为授权策略。这些授权策略很多，只要一个授权成功即可以,即或关系。

常见的方式有：

授权方式解析

**Node 授权**：主要针对集群节点间的通信，例如 kubelet 的通信。该专用授权模块会对需要运行 Pod 的 kubelet 进行授权。

**RBAC（Role Based Access Control，基于角色的访问控制）**：Kubernetes 1.6 及之后版本主推的授权策略，按用户所属角色管理对计算机或网络资源的访问。先通过 API 将权限赋予自定义 Role 或 ClusterRole，再将角色绑定到用户、用户组或 Service Account。结合 Namespace 可实现多租户隔离。

**ABAC（Attribute Based Access Control，基于属性的访问控制）**：较早版本使用的授权方式，基于资源、用户、对象和环境等属性组合编写策略。策略规则写在 kube-apiserver 本地文件中，满足其中一条即可通过授权。新增规则通常需要重启 kube-apiserver，因此生产环境较少使用。此类外部策略也可借助 OPA（Open Policy Agent）等第三方组件实现。

**Webhook**：通过 HTTP Callback 调用 Kubernetes 外部的授权组件，由该组件实施访问控制。

**AlwaysDeny**：拒绝所有请求，主要用于测试。**AlwaysAllow**：允许所有请求，仅适用于不需要对 API 请求做授权的场景。

本材料所述集群默认启用 Node 与 RBAC 授权模式。如果没有任何授权模式允许请求，则默认拒绝。

**配置方法**

在kube-apiserver上使用 --authorization-mode 选项进行定义多个模块彼此间以逗号分隔。
```yaml
[root@master1 ~]#cat /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
annotations:
kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint:
10.0.0.101:6443
creationTimestamp: null
labels:
component: kube-apiserver
tier: control-plane
name: kube-apiserver
namespace: kube-system
spec:
containers:
- command:

- kube-apiserver
- --advertise-address=10.0.0.101
- --allow-privileged=true
- --authorization-mode=Node,RBAC                      #授权方法，默认只支持Node
和RBAC
- --client-ca-file=/etc/kubernetes/pki/ca.crt
- --enable-admission-plugins=NodeRestriction
- --enable-bootstrap-token-auth=true
- --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
- --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
- --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
- --etcd-servers=https://127.0.0.1:2379
- --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-
client.crt
- --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
- --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
- --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
- --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
- --requestheader-allowed-names=front-proxy-client
- --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
- --requestheader-extra-headers-prefix=X-Remote-Extra-
- --requestheader-group-headers=X-Remote-Group
- --requestheader-username-headers=X-Remote-User
- --secure-port=6443
- --service-account-issuer=https://kubernetes.default.svc.cluster.local
- --service-account-key-file=/etc/kubernetes/pki/sa.pub
- --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
- --service-cluster-ip-range=10.96.0.0/12
- --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
- --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
image: registry.cn-hangzhou.aliyuncs.com/google_containers/kube-
apiserver:v1.22.1
imagePullPolicy: IfNotPresent
livenessProbe:
failureThreshold: 8
httpGet:
host: 10.0.0.101
path: /livez
port: 6443
scheme: HTTPS
initialDelaySeconds: 10
periodSeconds: 10
timeoutSeconds: 15
name: kube-apiserver
readinessProbe:
failureThreshold: 3
httpGet:
host: 10.0.0.101
path: /readyz
port: 6443
scheme: HTTPS
periodSeconds: 1
timeoutSeconds: 15
resources:
requests:
cpu: 250m
startupProbe:
failureThreshold: 24

httpGet:
host: 10.0.0.101
path: /livez
port: 6443
scheme: HTTPS
initialDelaySeconds: 10
periodSeconds: 10
timeoutSeconds: 15
volumeMounts:
- mountPath: /etc/ssl/certs
name: ca-certs
readOnly: true
- mountPath: /etc/ca-certificates
name: etc-ca-certificates
readOnly: true
- mountPath: /etc/pki
name: etc-pki
readOnly: true
- mountPath: /etc/kubernetes/pki
name: k8s-certs
readOnly: true
- mountPath: /usr/local/share/ca-certificates
name: usr-local-share-ca-certificates
readOnly: true
- mountPath: /usr/share/ca-certificates
name: usr-share-ca-certificates
readOnly: true
hostNetwork: true
priorityClassName: system-node-critical
securityContext:
seccompProfile:
type: RuntimeDefault
volumes:
- hostPath:
path: /etc/ssl/certs
type: DirectoryOrCreate
name: ca-certs
- hostPath:
path: /etc/ca-certificates
type: DirectoryOrCreate
name: etc-ca-certificates
- hostPath:
path: /etc/pki
type: DirectoryOrCreate
name: etc-pki
- hostPath:
path: /etc/kubernetes/pki
type: DirectoryOrCreate
name: k8s-certs
- hostPath:
path: /usr/local/share/ca-certificates
type: DirectoryOrCreate
name: usr-local-share-ca-certificates
- hostPath:
path: /usr/share/ca-certificates
type: DirectoryOrCreate
name: usr-share-ca-certificates
status: {}

[root@master1 ~]#
```

## 3.2 RBAC 机制


- <https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/authorization/>
- <https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/>


RBAC (Role-based access control) 基于角色Role的访问控制使用rbac.authorization.k8s.io API Group来实现授权决策。允许管理员通过 Kubernetes API 动态配置策略。

要启用RBAC，需要在 apiserver 中添加参数--authorization-mode=RBAC

kubeadm安装的集群默认开启了RBAC，可以通过查看 Master 节点上 apiserver 的静态Pod定义文件：
```bash
[root@master1 ~]#cat /etc/kubernetes/manifests/kube-apiserver.yaml
...
- --authorization-mode=Node,RBAC
...
```

### 3.2.1 RBAC 基础概念

实体（Entity）：在RBAC也称为Subject，通常指的是UserAccount、ServiceAccount 或者Group,即对哪些人进行授权。

资源（Resource）：在RBAC中也称为Object，指代Subject期望操作的目标，例如Secret、Pod及Service对象等。

仅限于/api/v1/ 或 /apis/// 开始的路径其它路径对应的端点均被视作“非资源类请求（Non-Resource Requests）”，例如: /healthz端点。

动作（Actions）：Subject可以于Object上有权限执行的特定操作，具体的可用动作取决于Kubernetes的定义。

Object

读操作：get、list、watch等写操作：create、update、patch、delete、deletecollection等

非Object: 仅支持get操作

规则Rules:  是一组属于不同 API Group 资源上的操作的权限集合,即资源Resource和动作Actions的组合的授权规则。

角色（Role）：承载资源操作权限的容器,包含一组权限的规则,只有允许没有拒绝权限。

**Role**：名称空间级别，生效范围为其所属的名称空间ClusterRole：集群级别，生效范围为整个集群。

角色绑定（Role Binding）：将角色关联至实体上，它能够将角色具体的操作权限赋予给实体,即将角色上的权限授予给账号，标准的资源类型 ,此资源决定了用户具有的是名称空间级或者集群级权限,而非由role决定。

**RoleBinding**：绑定在名称空间级别,即只授权拥有指定名称空间范围的权限ClusterRoleBinding:  绑定在集群级别,即授权拥有集群范围中所有名称空间的权限。

### 3.2.2 RBAC 授权机制

![原 PDF 第 85 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9700f85713461321.png)

#### 3.2.2.1 角色和角色绑定

授权指的是将某些subject对象赋予执行某些资源动作的权限。有时候会将其称为Group(权限组)，有两部分组成：角色（组名）和角色绑定(组关联)。

简单来说：授权为用户授予某种角色

**组成解析**

其实是附加在某些资源上的一系列权限的集合，对于k8s来说，它主要有两类：Role和clusterRole。

角

其中Role主要是作用于namespace，而clusterRole主要作用于多个namespace，它们之间。

色

是一对多的关系。为了将权限应用和具体权限列表分开描述，一般称权限列表为规则-rules。

角

所谓的组关联其实是将之前定义的Subject和对应的权限组关联在一起，表示某个Subject具。

色

有执行某个资源的一系列动作权限。它主要涉及到两个RoleBinding和

绑

ClusterRoleBinding。

定

**属性解析**

![原 PDF 第 85 页插图](assets/Kubernetes安全机制_Password_Removed1/img-e141f68f7ad9ad9b.png)

角色Role分类：

**ClusterRole**：集群范围内的资源的操作权限的集合,存在于所有名称空间。

**Role**：名称空间范围内资源操作的权限的集合,只存在于特定的名称空间。

**角色绑定 RoleBinding 分类**：**ClusterRoleBinding**：集群范围内的角色绑定,即分配给集群中所有名称空间相应的权限RoleBinding：名称空间范围内的角色绑定,,即只分配给指定名称空间相应的权限。

#### 3.2.2.2 角色和角色绑定组合

按照授权的范围将其划分为三类:

![原 PDF 第 86 页插图](assets/Kubernetes安全机制_Password_Removed1/img-cb59b65b5faad5c0.jpeg)

![原 PDF 第 86 页插图](assets/Kubernetes安全机制_Password_Removed1/img-453462b139f7ad8d.png)

namespace 级别cluster 级别混合级别

namespace级别组合

术语解析

rules

名称空间级别，生效范围为其所属的名称空间。

role

表示在一个namespace中基于rules使用资源的权限，属于集群内部的 API 资源，主要涉及到操作和对象。

将Subject关联至Role,授权给Subject可以在RoleBinding所在的名称空间使用指定资源的role角色权限也可以将Subject使用RoleBinding关联至ClusterRole上，该角色赋予到Subject的

RoleBinding

权限也会降级到RoleBinding所属的Namespace范围之内注意：支持在不同一个名称空间的用户和role进行RoleBinding。

注意: 在名称空间级授权时,必须要保证ServiceAccounts (SA) and RoleBindings 都在同个名称空间下。

cluster级别组合

术语解析

定义集群范围内的资源操作权限集合，包括集群级别及名称空间级别的资源对象。

ClusterRole

表示在一个cluster中基于rules使用资源的权限，属于集群内部的 API 资源，一个cluster有多个namespace即有多个role。将Subject关联至ClusterRole，授权给Subject可以在集群中使用指定资源。

ClusterRoleBinding

的ClusterRole角色权限即将实体（User、Group或ServiceAccount）关联至ClusterRole。

混合级别组合

术语解析

定义集群范围内的资源操作权限集合，包括集群级别及名称空间级别的资源对象。

ClusterRole

表示在一个cluster中基于rules使用资源的权限，属于集群内部的 API 资源，一个cluster有多个namespace即有多个role。将Subject基于RoleBinding与ClusterRole绑定在一起，表示Subject可以使用所有namespace中指定资源的role角色，从而避免了多次role和user的RoleBinding。

RoleBinding

同样的操作，站在ClusterRole的角度，我们可以理解为，用户得到的权限仅是ClusterRole的权限在Rolebinding所属的名称空间上的一个子集，也就是所谓的"权限降级"。

场景1：多个namespace中的role角色都一致，如果都使用内部的RoleBinding，每个namespace都必须单独创建role，而使用ClusterRole，只需要一个就可以了，大大的减轻批量使用namespace中的RoleBinding 操作。场景2：公司对A用户要提升权限，但是，由于A处于考察期，那么暂时给他分配一个区域，测试一下效果。生活中的场景，提升张三为公司副总裁，但是由于是试用期，所以加了一个限制:只临时主管销售范围的副总裁。
```text
ClusterRoleBinding:
Subject --> ClusterRole #授权Subject集群范围内的资源操作权限
```


RoleBinding: Subject --> Role        #授权Subject具有Role和RoleBinding所在的名称空间内的资源操作权限 Subject --> ClusterRole #授权Subject具有RoleBinding所在的名称空间内的资源操作权限,即 ClusterRole和 RoleBinding 二者的交集


Namespace、Subject、Role和RoleBinding之间的关系

![原 PDF 第 88 页插图](assets/Kubernetes安全机制_Password_Removed1/img-d77c3cb30994217e.png)

### 3.2.3 默认的Role，ClusterRole和RoleBinding，ClusterRoleBinding

启用RBAC鉴权模块时，API Server会自动创建一组ClusterRole和ClusterRoleBinding对象。

多数都以“system:”为前缀，也有几个面向用户的ClusterRole未使用该前缀，如cluster-admin、admin等它们都默认使用“kubernetes.io/bootstrapping: rbac-defaults”这一标签。

默认的ClusterRole大体可以分为如下5个类别。

**API发现相关的角色**

包括system:basic-user、system:discovery和system:public-info-viewer

面向用户的角色

包括cluster-admin、admin、edit和view

**核心组件专用的角色**

包括system:kube-scheduler、system:volume-scheduler、system:kube-controller-manager、system:node和system:node-proxier等

**其它组件专用的角色**

包括system:kube-dns、system:node-bootstrapper、system:node-problem-detector和system:monitoring等

内置控制器专用的角色

**面向用户的角色**

一些默认角色不是system:前缀。 这些旨在成为面向用户的角色。它们包括超级用户角色 (cluster-admin)、旨在使用 ClusterRoleBindings 在集群范围内授予的角色(cluster-status,新版已废弃)，以及旨在使用 RoleBindings (admin、edit、view) 在特定命名空间内授予的角色。

![原 PDF 第 89 页插图](assets/Kubernetes安全机制_Password_Removed1/img-1ad559371717cc6e.png)

**交互式用户常用的默认角色**

- **cluster-admin**：允许在目标范围内对任意资源执行任意操作。通过 ClusterRoleBinding 绑定时，可操作整个集群及所有 Namespace 的资源。通过 RoleBinding 绑定时，权限限定在该绑定所属的 Namespace，并包括 Namespace 资源本身。相关默认绑定涉及 kubeadm:cluster-admins 组（新版）及 system:masters 组（旧版）。
- **admin**：集群级管理员角色，可结合 RoleBinding 为指定 Namespace 授权。它允许读写该 Namespace 的大多数资源，包括创建 Role 和 RoleBinding，但不支持操作 ResourceQuota 和 Namespace 本身。
- **edit**：权限接近 admin，可读写 Namespace 内的大多数对象，包括 Secret，但不允许查看或修改 Role、RoleBinding。
- **view**：可只读访问 Namespace 内的大多数对象，但不包括 Role、RoleBinding 和 Secret。

范例: 查看默认role 和 clusterrole
```bash
[root@master1 ~]#kubectl get role -A
NAMESPACE     NAME                                             CREATED AT
kube-public   kubeadm:bootstrap-signer-clusterinfo             2021-08-
21T01:07:30Z
kube-public   system:controller:bootstrap-signer               2021-08-
21T01:07:21Z
kube-system   extension-apiserver-authentication-reader        2021-08-
21T01:07:21Z
kube-system   kube-proxy                                       2021-08-
21T01:07:30Z

kube-system   kubeadm:kubeadm-certs                            2021-08-
21T01:07:29Z
kube-system   kubeadm:kubelet-config                           2021-08-
21T01:07:26Z
kube-system   kubeadm:nodes-kubeadm-config                     2021-08-
21T01:07:26Z
kube-system   system::leader-locking-kube-controller-manager   2021-08-
21T01:07:21Z
kube-system   system::leader-locking-kube-scheduler            2021-08-
21T01:07:21Z
kube-system   system:controller:bootstrap-signer               2021-08-
21T01:07:21Z
kube-system   system:controller:cloud-provider                 2021-08-
21T01:07:21Z
kube-system   system:controller:token-cleaner                  2021-08-
21T01:07:21Z

[root@master1 ~]#kubectl get clusterrole
NAME                                                                   CREATED
AT
admin                                                                  2021-08-
21T01:07:21Z
cluster-admin                                                          2021-08-
21T01:07:21Z
edit                                                                   2021-08-
21T01:07:21Z
flannel                                                                2021-08-
21T01:09:05Z
kubeadm:get-nodes                                                      2021-08-
21T01:07:30Z
nfs-external-provisioner-role                                          2022-08-
27T13:57:37Z
system:aggregate-to-admin                                              2021-08-
21T01:07:21Z
system:aggregate-to-edit                                               2021-08-
21T01:07:21Z
system:aggregate-to-view                                               2021-08-
21T01:07:21Z
system:auth-delegator                                                  2021-08-
21T01:07:21Z
system:basic-user                                                      2021-08-
21T01:07:21Z
system:certificates.k8s.io:certificatesigningrequests:nodeclient       2021-08-
21T01:07:21Z
system:certificates.k8s.io:certificatesigningrequests:selfnodeclient   2021-08-
21T01:07:21Z
system:certificates.k8s.io:kube-apiserver-client-approver              2021-08-
21T01:07:21Z
system:certificates.k8s.io:kube-apiserver-client-kubelet-approver      2021-08-
21T01:07:21Z
system:certificates.k8s.io:kubelet-serving-approver                    2021-08-
21T01:07:21Z
system:certificates.k8s.io:legacy-unknown-approver                     2021-08-
21T01:07:21Z
system:controller:attachdetach-controller                              2021-08-
21T01:07:21Z
system:controller:certificate-controller                               2021-08-
21T01:07:21Z

system:controller:clusterrole-aggregation-controller                   2021-08-
21T01:07:21Z
system:controller:cronjob-controller                                   2021-08-
21T01:07:21Z
system:controller:daemon-set-controller                                2021-08-
21T01:07:21Z
system:controller:deployment-controller                                2021-08-
21T01:07:21Z
system:controller:disruption-controller                                2021-08-
21T01:07:21Z
system:controller:endpoint-controller                                  2021-08-
21T01:07:21Z
system:controller:endpointslice-controller                             2021-08-
21T01:07:21Z
system:controller:endpointslicemirroring-controller                    2021-08-
21T01:07:21Z
system:controller:ephemeral-volume-controller                          2021-08-
21T01:07:21Z
system:controller:expand-controller                                    2021-08-
21T01:07:21Z
system:controller:generic-garbage-collector                            2021-08-
21T01:07:21Z
system:controller:horizontal-pod-autoscaler                            2021-08-
21T01:07:21Z
system:controller:job-controller                                       2021-08-
21T01:07:21Z
system:controller:namespace-controller                                 2021-08-
21T01:07:21Z
system:controller:node-controller                                      2021-08-
21T01:07:21Z
system:controller:persistent-volume-binder                             2021-08-
21T01:07:21Z
system:controller:pod-garbage-collector                                2021-08-
21T01:07:21Z
system:controller:pv-protection-controller                             2021-08-
21T01:07:21Z
system:controller:pvc-protection-controller                            2021-08-
21T01:07:21Z
system:controller:replicaset-controller                                2021-08-
21T01:07:21Z
system:controller:replication-controller                               2021-08-
21T01:07:21Z
system:controller:resourcequota-controller                             2021-08-
21T01:07:21Z
system:controller:root-ca-cert-publisher                               2021-08-
21T01:07:21Z
system:controller:route-controller                                     2021-08-
21T01:07:21Z
system:controller:service-account-controller                           2021-08-
21T01:07:21Z
system:controller:service-controller                                   2021-08-
21T01:07:21Z
system:controller:statefulset-controller                               2021-08-
21T01:07:21Z
system:controller:ttl-after-finished-controller                        2021-08-
21T01:07:21Z
system:controller:ttl-controller                                       2021-08-
21T01:07:21Z

system:coredns                                                         2021-08-
21T01:07:30Z
system:discovery                                                       2021-08-
21T01:07:21Z
system:heapster                                                        2021-08-
21T01:07:21Z
system:kube-aggregator                                                 2021-08-
21T01:07:21Z
system:kube-controller-manager                                         2021-08-
21T01:07:21Z
system:kube-dns                                                        2021-08-
21T01:07:21Z
system:kube-scheduler                                                  2021-08-
21T01:07:21Z
system:kubelet-api-admin                                               2021-08-
21T01:07:21Z
system:monitoring                                                      2021-08-
21T01:07:21Z
system:node                                                            2021-08-
21T01:07:21Z
system:node-bootstrapper                                               2021-08-
21T01:07:21Z
system:node-problem-detector                                           2021-08-
21T01:07:21Z
system:node-proxier                                                    2021-08-
21T01:07:21Z
system:persistent-volume-provisioner                                   2021-08-
21T01:07:21Z
system:public-info-viewer                                              2021-08-
21T01:07:21Z
system:service-account-issuer-discovery                                2021-08-
21T01:07:21Z
system:volume-scheduler                                                2021-08-
21T01:07:21Z
view                                                                   2021-08-
21T01:07:21Z
```

范例：查看内置的 rolebinding和clusterrolebinding
```bash
[root@master1 ~]#kubectl get rolebindings -A
NAMESPACE              NAME                                                ROLE
AGE
ingress-nginx          ingress-nginx
Role/ingress-nginx                                    16d
ingress-nginx          ingress-nginx-admission
Role/ingress-nginx-admission                          16d
kube-public            kubeadm:bootstrap-signer-clusterinfo
Role/kubeadm:bootstrap-signer-clusterinfo             44d
kube-public            system:controller:bootstrap-signer
Role/system:controller:bootstrap-signer               44d
kube-system            kube-proxy
Role/kube-proxy                                       44d
kube-system            kubeadm:kubeadm-certs
Role/kubeadm:kubeadm-certs                            44d
kube-system            kubeadm:kubelet-config
Role/kubeadm:kubelet-config                           44d

kube-system            kubeadm:nodes-kubeadm-config
Role/kubeadm:nodes-kubeadm-config                     44d
kube-system            system::extension-apiserver-authentication-reader
Role/extension-apiserver-authentication-reader        44d
kube-system            system::leader-locking-kube-controller-manager
Role/system::leader-locking-kube-controller-manager   44d
kube-system            system::leader-locking-kube-scheduler
Role/system::leader-locking-kube-scheduler            44d
kube-system            system:controller:bootstrap-signer
Role/system:controller:bootstrap-signer               44d
kube-system            system:controller:cloud-provider
Role/system:controller:cloud-provider                 44d
kube-system            system:controller:token-cleaner
Role/system:controller:token-cleaner                  44d
kubernetes-dashboard   kubernetes-dashboard
Role/kubernetes-dashboard                             16d

[root@master1 ~]#kubectl get clusterrolebindings.rbac.authorization.k8s.io
NAME                                                   ROLE
AGE
cluster-admin                                          ClusterRole/cluster-admin
44d
flannel                                                ClusterRole/flannel
44d
ingress-nginx                                          ClusterRole/ingress-nginx
16d
ingress-nginx-admission                                ClusterRole/ingress-nginx-
admission                                                16d
kubeadm:get-nodes                                      ClusterRole/kubeadm:get-
nodes                                                      44d
kubeadm:kubelet-bootstrap                              ClusterRole/system:node-
bootstrapper                                               44d
kubeadm:node-autoapprove-bootstrap
ClusterRole/system:certificates.k8s.io:certificatesigningrequests:nodeclient
44d
kubeadm:node-autoapprove-certificate-rotation
ClusterRole/system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
44d
kubeadm:node-proxier                                   ClusterRole/system:node-
proxier                                                    44d
kubernetes-dashboard                                   ClusterRole/kubernetes-
dashboard                                                   16d
system:basic-user                                      ClusterRole/system:basic-
user                                                      44d
system:controller:attachdetach-controller
ClusterRole/system:controller:attachdetach-controller
44d
system:controller:certificate-controller
ClusterRole/system:controller:certificate-controller
44d
system:controller:clusterrole-aggregation-controller
ClusterRole/system:controller:clusterrole-aggregation-controller
44d
system:controller:cronjob-controller
ClusterRole/system:controller:cronjob-controller
44d

system:controller:daemon-set-controller
ClusterRole/system:controller:daemon-set-controller
44d
system:controller:deployment-controller
ClusterRole/system:controller:deployment-controller
44d
system:controller:disruption-controller
ClusterRole/system:controller:disruption-controller
44d
system:controller:endpoint-controller
ClusterRole/system:controller:endpoint-controller
44d
system:controller:endpointslice-controller
ClusterRole/system:controller:endpointslice-controller
44d
system:controller:endpointslicemirroring-controller
ClusterRole/system:controller:endpointslicemirroring-controller
44d
system:controller:ephemeral-volume-controller
ClusterRole/system:controller:ephemeral-volume-controller
44d
system:controller:expand-controller
ClusterRole/system:controller:expand-controller
44d
system:controller:generic-garbage-collector
ClusterRole/system:controller:generic-garbage-collector
44d
system:controller:horizontal-pod-autoscaler
ClusterRole/system:controller:horizontal-pod-autoscaler
44d
system:controller:job-controller
ClusterRole/system:controller:job-controller
44d
system:controller:namespace-controller
ClusterRole/system:controller:namespace-controller
44d
system:controller:node-controller
ClusterRole/system:controller:node-controller
44d
system:controller:persistent-volume-binder
ClusterRole/system:controller:persistent-volume-binder
44d
system:controller:pod-garbage-collector
ClusterRole/system:controller:pod-garbage-collector
44d
system:controller:pv-protection-controller
ClusterRole/system:controller:pv-protection-controller
44d
system:controller:pvc-protection-controller
ClusterRole/system:controller:pvc-protection-controller
44d
system:controller:replicaset-controller
ClusterRole/system:controller:replicaset-controller
44d
system:controller:replication-controller
ClusterRole/system:controller:replication-controller
44d

system:controller:resourcequota-controller
ClusterRole/system:controller:resourcequota-controller
44d
system:controller:root-ca-cert-publisher
ClusterRole/system:controller:root-ca-cert-publisher
44d
system:controller:route-controller
ClusterRole/system:controller:route-controller
44d
system:controller:service-account-controller
ClusterRole/system:controller:service-account-controller
44d
system:controller:service-controller
ClusterRole/system:controller:service-controller
44d
system:controller:statefulset-controller
ClusterRole/system:controller:statefulset-controller
44d
system:controller:ttl-after-finished-controller
ClusterRole/system:controller:ttl-after-finished-controller
44d
system:controller:ttl-controller
ClusterRole/system:controller:ttl-controller
44d
system:coredns                                         ClusterRole/system:coredns
44d
system:discovery
ClusterRole/system:discovery
44d
system:kube-controller-manager                         ClusterRole/system:kube-
controller-manager                                         44d
system:kube-dns                                        ClusterRole/system:kube-
dns                                                        44d
system:kube-scheduler                                  ClusterRole/system:kube-
scheduler                                                  44d
system:monitoring
ClusterRole/system:monitoring
44d
system:node                                            ClusterRole/system:node
44d
system:node-proxier                                    ClusterRole/system:node-
proxier                                                    44d
system:public-info-viewer                              ClusterRole/system:public-
info-viewer                                              44d
system:service-account-issuer-discovery
ClusterRole/system:service-account-issuer-discovery
44d
system:volume-scheduler                                ClusterRole/system:volume-
scheduler                                                44d
```

范例: 查看交互式用户授权目的的常见角色内置role
```yaml
#可以通过clusterrole 资源来查看cluster-admin的所有权限信息
[root@master1 ~]#kubectl describe clusterrole cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true

PolicyRule:
Resources  Non-Resource URLs  Resource Names  Verbs
---------  -----------------  --------------  -----
*.*        []                 []              [*]
[*]                []              [*]
#结果显示：对于cluster-admin来说，它拥有所有资源在所有空间的所有权限。

#查看cluster-admin角色
[root@master1 ~]#kubectl get clusterrole cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: "2021-08-21T01:07:21Z"
labels:
kubernetes.io/bootstrapping: rbac-defaults
name: cluster-admin
resourceVersion: "76"
uid: d44b78d0-74dc-4b85-ab65-0a4e46e72966
rules:
- apiGroups:
- '*'
resources:
- '*'
verbs:
- '*'
- nonResourceURLs:
- '*'
verbs:
- '*'

#查看role角色cluster-admin同名的clusterrolebinding
[root@master1 ~]#kubectl get clusterrolebinding  cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: "2021-08-21T01:07:21Z"
labels:
kubernetes.io/bootstrapping: rbac-defaults
name: cluster-admin
resourceVersion: "138"
uid: 67e002c3-1deb-47c8-9e4e-f5e932633610
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: Group
name: system:masters        #对组system:masters进行角色绑定

[root@master1 ~]#kubectl get clusterrole admin -o yaml
aggregationRule:
clusterRoleSelectors:

- matchLabels:
rbac.authorization.k8s.io/aggregate-to-admin: "true"
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: "2021-08-21T01:07:21Z"
labels:
kubernetes.io/bootstrapping: rbac-defaults
name: admin
resourceVersion: "114025"
uid: 4a15dbac-1178-4651-a477-23d1a58ced94
rules:
- apiGroups:
- ""
resources:
- pods/attach
- pods/exec
- pods/portforward
- pods/proxy
- secrets
- services/proxy
verbs:
- get
- list
- watch
- apiGroups:
- ""
resources:
- serviceaccounts
verbs:
- impersonate
- apiGroups:
......
```
```yaml
[root@master1 ~]#kubectl get clusterrole edit -o yaml
aggregationRule:
clusterRoleSelectors:
- matchLabels:
rbac.authorization.k8s.io/aggregate-to-edit: "true"
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: "2021-08-21T01:07:21Z"
labels:
kubernetes.io/bootstrapping: rbac-defaults
rbac.authorization.k8s.io/aggregate-to-admin: "true"
name: edit
resourceVersion: "114024"
uid: d938217e-4a61-414d-a45e-8fbb524ec2f8
rules:
- apiGroups:
- ""
resources:

- pods/attach
- pods/exec
- pods/portforward
- pods/proxy
- secrets
- services/proxy
.....

[root@master1 ~]#kubectl get clusterrole view -o yaml
aggregationRule:
clusterRoleSelectors:
- matchLabels:
rbac.authorization.k8s.io/aggregate-to-view: "true"
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
creationTimestamp: "2021-08-21T01:07:21Z"
labels:
kubernetes.io/bootstrapping: rbac-defaults
rbac.authorization.k8s.io/aggregate-to-edit: "true"
name: view
resourceVersion: "345"
uid: 566daa52-45bb-4fb4-a8ba-0d3e2ed295d4
rules:
- apiGroups:
- ""
resources:
- configmaps
- endpoints
- persistentvolumeclaims
- persistentvolumeclaims/status
- pods
- replicationcontrollers
- replicationcontrollers/scale
- serviceaccounts
- services
- services/status
verbs:
......
```

范例：cluster-admin 绑定关系
```yaml
#在集群中有一个名为cluster-admin的clusterrolebindings，该资源将组system:masters绑定到一
个权限列表中(即clusterrole)。
[root@master1 ~]#kubectl describe clusterrolebindings cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
Role:
Kind:  ClusterRole
Name:  cluster-admin
Subjects:
Kind   Name            Namespace
----   ----            ---------
Group  system:masters

[root@master1 ~]#kubectl get clusterrolebindings cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
...
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: Group
name: system:masters
#结果显示：只要是"system:masters"组中的成员，都具有cluster-admin的所有权限
```

## 3.3 Role 和 RoleBinding 组合实现

### 3.3.1 创建 Role
<https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/#kubectl-create-role>

**属性解析**
```bash
#因为角色由于级别不一样，作用的范围也不同，Role的属性，可以使用 kubectl explain role 的方式
来查看
[root@master1 ~]#kubectl explain role.rules
apiVersion <string>
kind <string>
metadata     <Object>
rules        <[]Object>
apiGroups             <[]string>
nonResourceURLs       <[]string>
resourceNames         <[]string>
resources             <[]string>
verbs                 <[]string> -required-
```


#结果显示：对于role来说，其核心的内容主要是rules的权限规则在这么多rules属性中，最重要的是verbs就是权限条目，而且所有的属性都是可以以列表的形式累加存在

```text
#命令式命令
kubectl create role NAME --verb=verb --resource=resource.group/subresource [--
resource-name=resourcename]
verb：#允许在资源上使用的操作（verb）列表
resources.group/subresource：#操作可施加的目标资源类型或子资源列表
resourcename：#特定的资源对象列表，可选

#关于api组的信息参照https://kubernetes.io/docs/reference/#api-reference
```

范例：查看系统内置 role
```yaml
[root@master1 ~]#kubectl get role -A
NAMESPACE              NAME                                             CREATED
AT

ingress-nginx          ingress-nginx                                    2021-04-
02T09:47:23Z
ingress-nginx          ingress-nginx-admission                          2021-04-
02T09:47:23Z
kube-public            kubeadm:bootstrap-signer-clusterinfo             2021-03-
04T15:36:35Z
kube-public            system:controller:bootstrap-signer               2021-03-
04T15:36:34Z
kube-system            extension-apiserver-authentication-reader        2021-03-
04T15:36:34Z
kube-system            kube-proxy                                       2021-03-
04T15:36:36Z
kube-system            kubeadm:kubeadm-certs                            2021-03-
04T15:36:35Z
kube-system            kubeadm:kubelet-config                           2021-03-
04T15:36:34Z
kube-system            kubeadm:nodes-kubeadm-config                     2021-03-
04T15:36:34Z
kube-system            system::leader-locking-kube-controller-manager   2021-03-
04T15:36:34Z
kube-system            system::leader-locking-kube-scheduler            2021-03-
04T15:36:34Z
kube-system            system:controller:bootstrap-signer               2021-03-
04T15:36:34Z
kube-system            system:controller:cloud-provider                 2021-03-
04T15:36:34Z
kube-system            system:controller:token-cleaner                  2021-03-
04T15:36:34Z
kubernetes-dashboard   kubernetes-dashboard                             2021-04-
02T00:09:10Z

[root@master1 ~]#kubectl get role -n kube-system   kubeadm:kubelet-config -o
yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
creationTimestamp: "2021-03-04T15:36:34Z"
name: kubeadm:kubelet-config
namespace: kube-system
resourceVersion: "238"
uid: a555187f-393a-418e-b6d8-37230ccc0b71
rules:
- apiGroups:
- ""
resourceNames:
- kubelet-config
resources:
- configmaps
verbs:
- get
```

范例：命令创建 role
```yaml
#创建一个对所有pod,service,deployment具有get、list权限的role的资源定义文件格式
[root@master1 ~]# kubectl create role pods-viewer --verb=get,list,watch --
resource=pods,services,deployments --dry-run=client -o yaml
apiVersion: rbac.authorization.k8s.io/v1

kind: Role
metadata:
creationTimestamp: null       #时间信息
name: pods-viewer             #role的名称
rules:                          #授权规则
- apiGroups:                    #操作的对象
- ""                          #空，表示核心群组
resources:                    #资源对象
- pods
- services
verbs:                        #对pod允许的权限
- get
- list
- watch
- apiGroups:                    #即使权限相同，但不同的资源组也需要分别授权
- apps
resources:
- deployments
verbs:
- get
- list
- watch

#结果显示：
#role必备的rules主要有三部分组成：apiGroup、resources、verbs
apiGroups   #设定包含资源的api组，如果是多个，表示只要属于api组范围中的任意资源都可以操作
resources   #位于apiGroup范围中的某些具体的资源对象
verbs       #针对具体资源对象的一些具体操作
```

范例:  清单文件创建 role
```yaml
#按照上面的role格式，准备一个role资源文件,允许用户操作 Deployment、Pod、RS 的所有权限
[root@master1 ~]#cat security-role-myrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
name: myrole
rules:
- apiGroups: ["", "extensions", "apps"]
resources: ["pods", "deployments", "replicasets"]
verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

#属性解析：
#Pod属于 core 的 API Group，在YAML中用空字符就可以
#Deployment 属于 apps 的 API Group
#ReplicaSets属于extensions的 API Group
#所以 rules 下面的 apiGroups 的内容：["", "extensions", "apps"]
#verbs是可以对这些资源对象执行的操作，如果是所有动作，也可以使用["*"]来代替。

#初始化实例对象
[root@master1 ~]#kubectl apply  -f  security-role-myrole.yaml

#查看效果
[root@master1 ~]#kubectl  get role
NAME     CREATED AT
myrole   2021-03-31T14:48:43Z

[root@master1 ~]#kubectl  describe role myrole
Name:         myrole
Labels:       <none>
Annotations:  <none>
PolicyRule:
Resources               Non-Resource URLs  Resource Names  Verbs
---------               -----------------  --------------  -----
deployments             []                 []              [get list watch
create update patch delete]
pods                    []                 []              [get list watch
create update patch delete]
replicasets             []                 []              [get list watch
create update patch delete]
deployments.apps        []                 []              [get list watch
create update patch delete]
pods.apps               []                 []              [get list watch
create update patch delete]
replicasets.apps        []                 []              [get list watch
create update patch delete]
deployments.extensions  []                 []              [get list watch
create update patch delete]
pods.extensions         []                 []              [get list watch
create update patch delete]
replicasets.extensions  []                 []              [get list watch
create update patch delete]
```

范例：
```yaml
[root@master1 ~]#cat security-role-demo.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
namespace: default
name: demo-role
rules:
- apiGroups: [""]
resources: ["pods/exec"]   #exec表示进入Pod终端的权限，必须给create权限才能创建终端进
入Pod
verbs: ["*"]

- apiGroups: [""]
resources: ["pods"]
verbs: ["get", "list", "watch"]   #只能查看，由于没有给create和delete权限，所以无法创
建和删除Pod

- apiGroups: ["apps/v1"]
resources: ["deployments"]
verbs: ["get","list","watch","create","update","patch","delete"]

- apiGroups: [""]
resources: ["services"]
verbs: ["get","list","watch","create","update","patch","delete"]

[root@master1 ~]#kubectl apply -f security-role-demo.yaml
role.rbac.authorization.k8s.io/demo-role created

[root@master1 ~]#kubectl get role demo-role
NAME        CREATED AT
demo-role   2021-07-23T08:54:25Z

[root@master1 ~]#kubectl describe role demo-role
Name:         demo-role
Labels:       <none>
Annotations:  <none>
PolicyRule:
Resources            Non-Resource URLs  Resource Names  Verbs
---------            -----------------  --------------  -----
pods/exec            []                 []              [*]
services             []                 []              [get list watch create
update patch delete]
deployments.apps/v1  []                 []              [get list watch create
update patch delete]
pods                 []                 []              [get list watch]

[root@master1 ~]#kubectl get role demo-role -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
annotations:
kubectl.kubernetes.io/last-applied-configuration: |
{"apiVersion":"rbac.authorization.k8s.io/v1","kind":"Role","metadata":
{"annotations":{},"name":"demo-role","namespace":"default"},"rules":
[{"apiGroups":[""],"resources":["pods/exec"],"verbs":["*"]},{"apiGroups":
[""],"resources":["pods"],"verbs":["get","list","watch"]},{"apiGroups":
["apps/v1"],"resources":["deployments"],"verbs":
["get","list","watch","create","update","patch","delete"]},{"apiGroups":
[""],"resources":["services"],"verbs":
["get","list","watch","create","update","patch","delete"]}]}
creationTimestamp: "2021-07-23T08:54:25Z"
name: demo-role
namespace: default
resourceVersion: "121498"
uid: 1c10e0dc-8529-4ff3-a325-5d70543985bd
rules:
- apiGroups:
- ""
resources:
- pods/exec
verbs:
- '*'
- apiGroups:
- ""
resources:
- pods
verbs:
- get
- list
- watch
- apiGroups:
- apps/v1
resources:
- deployments
verbs:

- get
- list
- watch
- create
- update
- patch
- delete
- apiGroups:
- ""
resources:
- services
verbs:
- get
- list
- watch
- create
- update
- patch
- delete

#清理环境
[root@master1 ~]#kubectl delete  -f security-role-demo.yaml
```

### 3.3.2 角色绑定 rolebinding

#### 3.3.2.1  rolebinding 说明
```text
https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/#role-binding-
examples说明
```

**对主体的引用**

RoleBinding 或者 ClusterRoleBinding 可绑定角色到某主体（Subject） 上。

subject主体可以是组，用户或者服务账户。Kubernetes 用字符串来表示用户名。 用户名可以是普通的用户名，像 "alice"；或者是邮件风格的名称，如 "bob@example.com"， 或者是以字符串形式表达的数字 ID。你作为 Kubernetes 管理员负责配置身份认证模块， 以便后者能够生成你所期望的格式的用户名。

注意：

前缀 system: 是 Kubernetes 系统保留的，所以你要确保所配置的用户名或者组名不能出现上述system: 前缀。除了对前缀的限制之外，RBAC 鉴权系统不对用户名格式作任何要求。在 Kubernetes 中，身份认证（Authenticator）模块提供用户组信息。 与用户名一样，用户组名也用字符串来表示，而且对该字符串没有格式要求， 只是不能使用保留的前缀 system:。服务账户（ServiceAccount） 的用户名前缀为 system:serviceaccount:，属于前缀为system:serviceaccounts: 的用户组。

说明：

system:serviceaccount: （单数）是用于服务账户用户名的前缀。

system:serviceaccounts: （复数）是用于服务账户组名的前缀。

RoleBinding 示例

下面示例是 RoleBinding 中的片段，仅展示其 subjects 的部分。

对于名称为 alice@example.com 的用户：
```yaml
subjects:
- kind: User
name: "alice@example.com"
apiGroup: rbac.authorization.k8s.io
```

对于名称为 frontend-admins 的用户组：
```yaml
subjects:
- kind: Group
name: "frontend-admins"
apiGroup: rbac.authorization.k8s.io
```

对于 kube-system 名字空间中的默认服务账户：
```yaml
subjects:
- kind: ServiceAccount
name: default
namespace: kube-system
```

对于 "qa" 名称空间中的所有服务账户：
```yaml
subjects:
- kind: Group
name: system:serviceaccounts:qa
apiGroup: rbac.authorization.k8s.io
```

对于在任何名字空间中的服务账户：
```yaml
subjects:
- kind: Group
name: system:serviceaccounts
apiGroup: rbac.authorization.k8s.io
```

对于所有已经过身份认证的用户：
```yaml
subjects:
- kind: Group
name: system:authenticated
apiGroup: rbac.authorization.k8s.io
```

对于所有未通过身份认证的用户：
```yaml
subjects:
- kind: Group
name: system:unauthenticated
apiGroup: rbac.authorization.k8s.io
```

对于所有用户：
```yaml
subjects:
- kind: Group
name: system:authenticated
apiGroup: rbac.authorization.k8s.io
- kind: Group
name: system:unauthenticated
apiGroup: rbac.authorization.k8s.io
```

范例: 查看内置rolebindings
```bash
[root@master1 ~]#kubectl get rolebindings -A
NAMESPACE       NAME                                                ROLE
AGE
ingress-nginx   ingress-nginx                                       Role/ingress-
nginx                                    46d
ingress-nginx   ingress-nginx-admission                             Role/ingress-
nginx-admission                          46d
kube-public     kubeadm:bootstrap-signer-clusterinfo
Role/kubeadm:bootstrap-signer-clusterinfo             91d
kube-public     system:controller:bootstrap-signer
Role/system:controller:bootstrap-signer               91d
kube-system     kube-proxy                                          Role/kube-
proxy                                       91d
kube-system     kubeadm:kubeadm-certs
Role/kubeadm:kubeadm-certs                            91d
kube-system     kubeadm:kubelet-config
Role/kubeadm:kubelet-config                           91d
kube-system     kubeadm:nodes-kubeadm-config
Role/kubeadm:nodes-kubeadm-config                     91d
kube-system     metrics-server-auth-reader
Role/extension-apiserver-authentication-reader        5d3h
kube-system     system::extension-apiserver-authentication-reader
Role/extension-apiserver-authentication-reader        91d
kube-system     system::leader-locking-kube-controller-manager
Role/system::leader-locking-kube-controller-manager   91d
kube-system     system::leader-locking-kube-scheduler
Role/system::leader-locking-kube-scheduler            91d
kube-system     system:controller:bootstrap-signer
Role/system:controller:bootstrap-signer               91d
kube-system     system:controller:cloud-provider
Role/system:controller:cloud-provider                 91d
kube-system     system:controller:token-cleaner
Role/system:controller:token-cleaner                  91d
```

#### 3.3.2.2 UA 绑定

**用户绑定属性简介**
```bash
#查看rolebinding的属性信息
#] kubectl explain rolebinding
apiVersion   <string>
kind <string>
metadata     <Object>
roleRef      <Object> -required-
subjects     <[]Object>

#结果显示：对于角色绑定来说，主要涉及到两点：subject和对应的role权限列表，其中roleRef是必选
项。

#命令式命令：
kubectl create rolebinding NAME --clusterrole=NAME|--role=NAME [--user=username]
[--group=groupname] [--namespace=namespace_name]

#可以绑定到Role，也可以绑定到ClusterRole，后者会将ClusterRole的权限缩减至当前名称空间之内
#Subject可以是User、Group或者ServiceAccount

#示例：将用户tom绑定至角色pods-viewer之上,注意：pods-viewer和tom-attachto-pods-viewer都
要求在default名称空间中
kubectl create rolebinding tom-attachto-pods-viewer --role=pods-viewer --
user=tom --namespace=default
#而后可测试tom用户是否可读取default名称空间内的pods资源，以及其它资源
```

范例: 配置文件
```yaml
#以pod-sa-admin或者bowen的subject来与myrole进行一次模拟绑定查看属性效果
[root@master1 ~]#kubectl create rolebinding bowen-myrole --role=myrole --user=bowen
-o yaml --dry-run
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
creationTimestamp: null
name: bowen-myrole
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: Role
name: myrole
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User
name: bowen

#创建配置文件
[root@master1 ~]#kubectl create rolebinding bowen-myrole --role=myrole --user=bowen
-o yaml --dry-run > /data/kubernetes/yaml/security-rolebinding.yaml

[root@master1 ~]#cat security-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: bowen-myrole
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: Role
name: myrole
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User
name: bowen

#基于bowen的token测试访问
[root@master1 ~]#cat /etc/kubernetes/auth/token.csv
BOOTSTRAP_TOKEN,bowen,1001,kubeadm:ops

BOOTSTRAP_TOKEN,test,1002,dev

[root@master1 ~]#TOKEN="BOOTSTRAP_TOKEN"
[root@master1 ~]#curl -k -H "Authorization: Bearer $TOKEN"
https://kubeapi.bowen.org:6443/api/v1/namespaces/default/pods/
```

范例:
```bash
#创建rolebinding
[root@master1 ~]#kubectl create rolebinding myrolebinding --role=myrole --
user=bowen
#或者
[root@master1 ~]#kubectl apply -f security-rolebinding.yaml

#注意：如果是多个用户，可以多来几个 --user=subject 彼此间使用空格隔开即可

#检查效果
[root@master1 ~]#kubectl get rolebindings
NAME          ROLE          AGE
bowen-myrole   Role/myrole   15s

[root@master1 ~]#kubectl describe rolebindings. bowen-myrole
Name:         bowen-myrole
Labels:       <none>
Annotations:  <none>
Role:
Kind:  Role
Name:  myrole
Subjects:
Kind  Name  Namespace
----  ----  ---------
User  bowen

#bowen 已经加入到 myrolebinding 角色绑定组中,这里的namespace没有写，表示默认的default命名
空间

#查看当前namespace中资源效果
[root@master1 ~]#kubectl get pod --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf
NAME       READY   STATUS    RESTARTS       AGE
pod-test   1/1     Running   1 (125m ago)   2d2h

#注意：我们在创建bowen的时候没有指定命名空间，表示默认的default

#查看default命名空间中，非pod、deployment、rs之外的资源
[root@master1 ~]#kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-mbnrx   kubernetes.io/service-account-token   3      2d2h

[root@master1 ~]#kubectl get secrets --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf
Error from server (Forbidden): secrets is forbidden: User "bowen" cannot list
resource "secrets" in API group "" in the namespace "default"
#结果显示：在我们role之外的内容我们都没有权限查看

#查看非当前namespace中的资源

[root@master1 ~]#kubectl get pod -n kube-system --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf
Error from server (Forbidden): pods is forbidden: User "bowen" cannot list
resource "pods" in API group "" in the namespace "kube-system"
#结果显示：在当前role权限范围内容，其它namespace中的资源，我们生效不了，因为role只是针对某个
具体的ns
```

#### 3.3.2.3 SA 绑定

注意：SA可以跨名称空间进行授权，比如:名称空间A的SA帐号可以绑定授权给名称空间B的角色，甚至对所有名称空间授权。

**命令格式**
```bash
#查看SA的角色绑定格式
kubectl create rolebinding NAME --role=NAME [--
serviceaccount=namespace:serviceaccountname] [--namespace=namespace_name]
#属性解析：在基于服务账号进行关联的时候，需要关注一下该SA所属的namespace信息。

#验证权限

#方法1：在Pod内执行
kubectl exec -it pod -- sh
cd /run/secrets/kubernetes.io/serviceaccount
TOKEN=$(cat token)

curl --cacert /etc/kubernetes/pki/ca.crt -H "Authorization: Bearer ${TOKEN}"
https://kubernetes.default/api/v1/pod/namespaces/{namespace}
curl -k -H "Authorization: Bearer ${ToKEN}" https://kubernetes.
<namespace>/api/v1/namespaces/<namespace>/pods/
curl -k -H "Authorization: Bearer ${ToKEN}" https://kubernetes.
<namespace>/api/v1/namespaces/<namespace>/pods/<pod_name>
curl -k -H "Authorization: Bearer ${ToKEN}" https://kubernetes.
<namespace>/apis/apps/v1/namespaces/<namespace>/deployments

#方法2：在集群节点上执行
kubectl --insecure-skip-tls-verify  --token=${TOKEN} -s
https://kubeapi.bowen.org:6443 get pod
kubectl --insecure-skip-tls-verify  --token=${TOKEN} -s
https://kubeapi.bowen.org:6443 get pods -n <namespace>

#方法3：在集群节点上执行
curl -s -H "Authorization: Bearer $TOKEN"  --cacert /etc/kubernetes/pki/ca.crt
https://API_SERVER:6443/api/v1/namespaces/default/pods/
```

范例:
```text
#自建的sa是admin而且是属于default空间，先将admin和myrole进行绑定，查看一下效果
kubectl create rolebinding myrolebinding1 --role=myrole --
serviceaccount=default:admin

#检查效果
]# kubectl describe rolebindings myrolebinding1
Name:         myrolebinding1
...
Subjects:
Kind            Name   Namespace
----            ----   ---------
ServiceAccount  admin  default

#结果显示:admin加入到了myrolebinding1的绑定组中，而且显示了特定的命名空间
```

### 3.2.3 综合案例

范例: 实现 Jenkins的权限

运行Kubernetes上的Jenkins，为能够动态创建jenkins-slave相关的Pod，需要对运行该Pod对应的ServiceAccount进行认证和授权。
```yaml
#创建ROle
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
name: jenkins-master
namespace: jenkins
rules:
- apiGroups: [""]
resources: ["pods"]
verbs: ["create","delete","get","list","patch","update","watch"]
- apiGroups: [""]
resources: ["pods/exec"]
verbs: ["create","delete","get","list","patch","update","watch"]
- apiGroups: [""]
resources: ["pods/log"]
verbs: ["get","list","watch"]
- apiGroups: [""]
resources: ["events"]
verbs: ["watch"]
- apiGroups: [""]
resources: ["secrets"]
verbs: ["get"]

---
#创建 SA
apiVersion: v1
kind: ServiceAccount
metadata:
name: jenkins-master
namespace: jenkins

---
#角色绑定
apiVersion: rbac.authorization.k8s.io/v1

kind: RoleBinding
metadata:
name: jenkins-master
namespace: jenkins
roleRef:
kind: Role
name: jenkins-master
apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
name: jenkins-master
namespace: jenkins
```

## 3.4 ClusterRole 和 ClusterRoleBinding 组合实现

cluster级别的实践主要涉及到clusterRole和ClusterRoleBinding之间的操作，即可以操作集群内所有namespace空间的资源。

### 3.4.1 创建 clusterrole
<https://kubernetes.io/zh-cn/docs/reference/access-authn-authz/rbac/#kubectl-create-clusterrole>

说明
```yaml
#] kubectl explain clusterrole
aggregationRule      <Object>   #可以实现role的嵌套关系
apiVersion <string>
kind <string>
metadata     <Object>
rules        <[]Object>
apiGroups               <[]string>
nonResourceURLs         <[]string>
resourceNames           <[]string>
resources               <[]string>
verbs                   <[]string> -required-

#结果显示：clusterrole相对于role的属性多了一个集中控制器的属性aggregationRule，而这是一个可
选的属性

#查看配置格式
]# kubectl create clusterrole myclusterrole --verb=get,list --resource=pods -o
yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
creationTimestamp: null
name: myclusterrole
rules:
- apiGroups:
- ""
resources:
- pods
verbs:
- get
- list

#结果显示：单从模板的资源配置样式来说，其配置信息与role的配置信息几乎一样。
```

范例: 查看内置 Clusterrole
```bash
[root@master1 ~]#kubectl get clusterrole
NAME                                                                   CREATED
AT
admin                                                                  2023-03-
07T04:30:21Z
cluster-admin                                                          2023-03-
07T04:30:21Z
edit                                                                   2023-03-
07T04:30:21Z
flannel                                                                2023-03-
07T05:01:45Z
ingress-nginx                                                          2023-04-
20T09:10:45Z
ingress-nginx-admission                                                2023-04-
20T09:10:45Z
jenkins-admin                                                          2023-06-
06T06:08:36Z
kubeadm:get-nodes                                                      2023-03-
07T04:30:23Z
nfs-client-provisioner-runner                                          2023-06-
01T09:09:58Z
prometheus                                                             2023-06-
01T06:45:22Z
system:aggregate-to-admin                                              2023-03-
07T04:30:21Z
system:aggregate-to-edit                                               2023-03-
07T04:30:21Z
system:aggregate-to-view                                               2023-03-
07T04:30:21Z
system:aggregated-metrics-reader                                       2023-06-
01T03:58:44Z
system:auth-delegator                                                  2023-03-
07T04:30:21Z
system:basic-user                                                      2023-03-
07T04:30:21Z
system:certificates.k8s.io:certificatesigningrequests:nodeclient       2023-03-
07T04:30:21Z
system:certificates.k8s.io:certificatesigningrequests:selfnodeclient   2023-03-
07T04:30:21Z
system:certificates.k8s.io:kube-apiserver-client-approver              2023-03-
07T04:30:21Z
system:certificates.k8s.io:kube-apiserver-client-kubelet-approver      2023-03-
07T04:30:21Z
system:certificates.k8s.io:kubelet-serving-approver                    2023-03-
07T04:30:21Z
system:certificates.k8s.io:legacy-unknown-approver                     2023-03-
07T04:30:21Z
system:controller:attachdetach-controller                              2023-03-
07T04:30:21Z
system:controller:certificate-controller                               2023-03-
07T04:30:21Z
system:controller:clusterrole-aggregation-controller                   2023-03-
07T04:30:21Z

system:controller:cronjob-controller                                   2023-03-
07T04:30:21Z
system:controller:daemon-set-controller                                2023-03-
07T04:30:21Z
system:controller:deployment-controller                                2023-03-
07T04:30:21Z
system:controller:disruption-controller                                2023-03-
07T04:30:21Z
system:controller:endpoint-controller                                  2023-03-
07T04:30:21Z
system:controller:endpointslice-controller                             2023-03-
07T04:30:21Z
system:controller:endpointslicemirroring-controller                    2023-03-
07T04:30:21Z
system:controller:ephemeral-volume-controller                          2023-03-
07T04:30:21Z
system:controller:expand-controller                                    2023-03-
07T04:30:21Z
system:controller:generic-garbage-collector                            2023-03-
07T04:30:21Z
system:controller:horizontal-pod-autoscaler                            2023-03-
07T04:30:21Z
system:controller:job-controller                                       2023-03-
07T04:30:21Z
system:controller:namespace-controller                                 2023-03-
07T04:30:21Z
system:controller:node-controller                                      2023-03-
07T04:30:21Z
system:controller:persistent-volume-binder                             2023-03-
07T04:30:21Z
system:controller:pod-garbage-collector                                2023-03-
07T04:30:21Z
system:controller:pv-protection-controller                             2023-03-
07T04:30:21Z
system:controller:pvc-protection-controller                            2023-03-
07T04:30:21Z
system:controller:replicaset-controller                                2023-03-
07T04:30:21Z
system:controller:replication-controller                               2023-03-
07T04:30:21Z
system:controller:resourcequota-controller                             2023-03-
07T04:30:21Z
system:controller:root-ca-cert-publisher                               2023-03-
07T04:30:21Z
system:controller:route-controller                                     2023-03-
07T04:30:21Z
system:controller:service-account-controller                           2023-03-
07T04:30:21Z
system:controller:service-controller                                   2023-03-
07T04:30:21Z
system:controller:statefulset-controller                               2023-03-
07T04:30:21Z
system:controller:ttl-after-finished-controller                        2023-03-
07T04:30:21Z
system:controller:ttl-controller                                       2023-03-
07T04:30:21Z
system:coredns                                                         2023-03-
07T04:30:23Z

system:discovery                                                       2023-03-
07T04:30:21Z
system:heapster                                                        2023-03-
07T04:30:21Z
system:kube-aggregator                                                 2023-03-
07T04:30:21Z
system:kube-controller-manager                                         2023-03-
07T04:30:21Z
system:kube-dns                                                        2023-03-
07T04:30:21Z
system:kube-scheduler                                                  2023-03-
07T04:30:21Z
system:kubelet-api-admin                                               2023-03-
07T04:30:21Z
system:metrics-server                                                  2023-06-
01T03:58:44Z
system:monitoring                                                      2023-03-
07T04:30:21Z
system:node                                                            2023-03-
07T04:30:21Z
system:node-bootstrapper                                               2023-03-
07T04:30:21Z
system:node-problem-detector                                           2023-03-
07T04:30:21Z
system:node-proxier                                                    2023-03-
07T04:30:21Z
system:persistent-volume-provisioner                                   2023-03-
07T04:30:21Z
system:public-info-viewer                                              2023-03-
07T04:30:21Z
system:service-account-issuer-discovery                                2023-03-
07T04:30:21Z
system:volume-scheduler                                                2023-03-
07T04:30:21Z
view                                                                   2023-03-
07T04:30:21Z
```

### 3.4.2 角色绑定 clusterrolebinding
```yaml
#命令格式
kubectl create clusterrolebinding NAME --clusterrole=NAME [--user=username] [--
group=groupname]
[--serviceaccount=namespace:serviceaccountname] [--dry-run=server|client|none]
[options]

#属性解析:对于clusterrolebinding来说，仅仅允许集群角色进行和其进行绑定，对于普通的role来说就
无效了

#将bowen用户和myclasterrole进行角色绑定，查看资源配置效果
]# kubectl create clusterrolebinding myclusterrolebinding --
clusterrole=myclusterrole --user=bowen --dry-run=client -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
creationTimestamp: null
name: myclusterrolebinding

roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole                         用户绑定类型
name: myclasterrole                       用户绑定名称
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User                                用户类型
name: bowen                                用户名称

#属性解析：这里的属性配置与我们之前的role和rolebinding的方法几乎一样,区别就是kind和--
clusterrole的不同
```

范例: 查看内置rolebindings
```bash
[root@master1 ~]#kubectl get clusterrolebinding
NAME                                                   ROLE
AGE
cluster-admin                                          ClusterRole/cluster-admin
91d
dashboard-admin                                        ClusterRole/cluster-admin
56d
flannel                                                ClusterRole/flannel
91d
ingress-nginx                                          ClusterRole/ingress-nginx
46d
ingress-nginx-admission                                ClusterRole/ingress-nginx-
admission                                                46d
jenkins-admin                                          ClusterRole/jenkins-admin
90m
kubeadm:get-nodes                                      ClusterRole/kubeadm:get-
nodes                                                      91d
kubeadm:kubelet-bootstrap                              ClusterRole/system:node-
bootstrapper                                               91d
kubeadm:node-autoapprove-bootstrap
ClusterRole/system:certificates.k8s.io:certificatesigningrequests:nodeclient
91d
kubeadm:node-autoapprove-certificate-rotation
ClusterRole/system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
91d
kubeadm:node-proxier                                   ClusterRole/system:node-
proxier                                                    91d
metrics-server:system:auth-delegator                   ClusterRole/system:auth-
delegator                                                  5d3h
prometheus                                             ClusterRole/prometheus
5d
run-nfs-client-provisioner                             ClusterRole/nfs-client-
provisioner-runner                                          4d22h
system:basic-user                                      ClusterRole/system:basic-
user                                                      91d
system:controller:attachdetach-controller
ClusterRole/system:controller:attachdetach-controller
91d
system:controller:certificate-controller
ClusterRole/system:controller:certificate-controller
91d

system:controller:clusterrole-aggregation-controller
ClusterRole/system:controller:clusterrole-aggregation-controller
91d
system:controller:cronjob-controller
ClusterRole/system:controller:cronjob-controller
91d
system:controller:daemon-set-controller
ClusterRole/system:controller:daemon-set-controller
91d
system:controller:deployment-controller
ClusterRole/system:controller:deployment-controller
91d
system:controller:disruption-controller
ClusterRole/system:controller:disruption-controller
91d
system:controller:endpoint-controller
ClusterRole/system:controller:endpoint-controller
91d
system:controller:endpointslice-controller
ClusterRole/system:controller:endpointslice-controller
91d
system:controller:endpointslicemirroring-controller
ClusterRole/system:controller:endpointslicemirroring-controller
91d
system:controller:ephemeral-volume-controller
ClusterRole/system:controller:ephemeral-volume-controller
91d
system:controller:expand-controller
ClusterRole/system:controller:expand-controller
91d
system:controller:generic-garbage-collector
ClusterRole/system:controller:generic-garbage-collector
91d
system:controller:horizontal-pod-autoscaler
ClusterRole/system:controller:horizontal-pod-autoscaler
91d
system:controller:job-controller
ClusterRole/system:controller:job-controller
91d
system:controller:namespace-controller
ClusterRole/system:controller:namespace-controller
91d
system:controller:node-controller
ClusterRole/system:controller:node-controller
91d
system:controller:persistent-volume-binder
ClusterRole/system:controller:persistent-volume-binder
91d
system:controller:pod-garbage-collector
ClusterRole/system:controller:pod-garbage-collector
91d
system:controller:pv-protection-controller
ClusterRole/system:controller:pv-protection-controller
91d
system:controller:pvc-protection-controller
ClusterRole/system:controller:pvc-protection-controller
91d

system:controller:replicaset-controller
ClusterRole/system:controller:replicaset-controller
91d
system:controller:replication-controller
ClusterRole/system:controller:replication-controller
91d
system:controller:resourcequota-controller
ClusterRole/system:controller:resourcequota-controller
91d
system:controller:root-ca-cert-publisher
ClusterRole/system:controller:root-ca-cert-publisher
91d
system:controller:route-controller
ClusterRole/system:controller:route-controller
91d
system:controller:service-account-controller
ClusterRole/system:controller:service-account-controller
91d
system:controller:service-controller
ClusterRole/system:controller:service-controller
91d
system:controller:statefulset-controller
ClusterRole/system:controller:statefulset-controller
91d
system:controller:ttl-after-finished-controller
ClusterRole/system:controller:ttl-after-finished-controller
91d
system:controller:ttl-controller
ClusterRole/system:controller:ttl-controller
91d
system:coredns                                         ClusterRole/system:coredns
91d
system:discovery
ClusterRole/system:discovery
91d
system:kube-controller-manager                         ClusterRole/system:kube-
controller-manager                                         91d
system:kube-dns                                        ClusterRole/system:kube-
dns                                                        91d
system:kube-scheduler                                  ClusterRole/system:kube-
scheduler                                                  91d
system:metrics-server
ClusterRole/system:metrics-server
5d3h
system:monitoring
ClusterRole/system:monitoring
91d
system:node                                            ClusterRole/system:node
91d
system:node-proxier                                    ClusterRole/system:node-
proxier                                                    91d
system:public-info-viewer                              ClusterRole/system:public-
info-viewer                                              91d
system:service-account-issuer-discovery
ClusterRole/system:service-account-issuer-discovery
91d
system:volume-scheduler                                ClusterRole/system:volume-
scheduler                                                91d
```

### 3.4.3 综合案例

范例
```yaml
#创建资源定义文件
[root@master1 ~]#cat security-myclusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
name: myclusterrole
rules:
- apiGroups: [""]
resources: ["pods"]
verbs: ["get", "list", "watch"]

#初始化资源对象
[root@master1 ~]#kubectl apply  -f  security-myclusterrole.yaml

#检查效果
[root@master1 ~]#kubectl get clusterrole | egrep 'NAME|my'
NAME                                                 CREATED AT
myclasterrole                                        2021-10-06T23:28:08Z

[root@master1 ~]#kubectl describe clusterrole myclusterrole
Name:         myclusterrole
Labels:       <none>
Annotations:  <none>
PolicyRule:
Resources  Non-Resource URLs  Resource Names  Verbs
---------  -----------------  --------------  -----
pods       []                 []              [get list watch]

#结果显示：在myclusterrole仅仅有pod资源的三种权限

#cluserrolebinding绑定
#方法1：命令行方式
[root@master1 ~]#kubectl create clusterrolebinding myclusterrolebinding --
clusterrole=myclusterrole --user=bowen

#方法2：配置文件方式
[root@master1 ~]#cat security-myclusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
name: myclusterrolebinding
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: myclusterrole
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User
name: bowen

#应用清单文件

[root@master1 ~]#kubectl apply  -f  security-myclusterrolebinding.yaml

#检查效果
[root@master1 ~]#kubectl get clusterrolebinding | egrep 'NAME|my'
NAME                                                   AGE
myclusterrolebinding                                   23s

[root@master1 ~]#kubectl describe clusterrolebinding myclusterrolebinding
Name:         myclusterrolebinding
Labels:       <none>
Annotations:  <none>
Role:
Kind:  ClusterRole
Name:  myclusterrole
Subjects:
Kind  Name  Namespace
----  ----  ---------
User  bowen
#结果显示：将bowen的账号赋予了操作集群角色的权限

#切换账号查看效果
[root@master1 ~]#kubectl get pod --context=bowen@mycluster  --
kubeconfig=/tmp/bowen.conf
NAME       READY   STATUS    RESTARTS       AGE
pod-test   1/1     Running   1 (139m ago)   2d2h

[root@master1 ~]#kubectl get pod --context=bowen@mycluster -n kube-system  --
kubeconfig=/tmp/bowen.conf
NAME                                         READY   STATUS    RESTARTS
AGE
coredns-7d89d9b6b8-kfdvj                     1/1     Running   1 (139m ago)
2d2h
coredns-7d89d9b6b8-mbhtn                     1/1     Running   1 (139m ago)
2d2h
etcd-master1.bowen.org                      1/1     Running   14 (139m ago)
2d2h
......
#结果显示：对于clusterrolebinding来说，绑定后的user account不但可以看到当前namespace中的
资源对象，还能看到其他namespace中的资源对象
```

范例：生成SA和TOKEN，并授权
```yaml
#清单文件
[root@master1 ~]#cat securiy-sa-token-cluster-admin.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: bowen
namespace: kube-system

---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: bowen-secret
namespace: kube-system

annotations:
kubernetes.io/service-account.name: "bowen"

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
name: testsa-clusterrolebinding
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: bowen
namespace: kube-system

#生成资源
[root@master1 ~]#kubectl apply -f securiy-sa-token-cluster-admin.yaml

#查看资源
[root@master1 ~]#kubectl get sa bowen -n kube-system
NAME   SECRETS   AGE
bowen   0         29m

[root@master1 ~]#kubectl get secrets bowen-secret -n kube-system
NAME          TYPE                                  DATA   AGE
bowen-secret   kubernetes.io/service-account-token   3      4m41s

#查看SA对应的TOKEN
[root@master1 ~]#kubectl get secrets -n kube-system bowen-secret -o yaml
apiVersion: v1
data:
ca.crt:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lH
OXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJek1ETXdOREUxTXpZ
eU0xb1hEVE16TURNd01URTFNell5TTFvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FT
SXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBUFVXCit2cFlOS09DOUQ4WHlSL2pM
TjhwbHBxaVQxTk84M3lkcmF0RnhnSXFJYVdvcWlaRnVUNnhMTWF6c1E3SGNvUDMKZWlIWi9naW4xRi80
Wk9GYWpRWUNIYkdEMWpOK2l2cDluWVA0aWRLUGR3U0ZheFFwNGNBdjQwQWxTZ0dlSVlTSgpZemhudmJR
UlFESkR0NWV6TnpHSXBIb3p5VHppb3U0aDVWd1JmdVVOeVYxWVhlZ0tvTDVsUXRnUnNtWHo0UlFQCnNF
Vm9VeUN3YzdwcXIrZFgyU2tkc0JuZGM3WVdQOVdKQW1ZTWpWaEswZUd4UkNKRERTK1N0TE1OdUhOcCsv
TmwKUVh4ZWNEd3hKdzZIVFdBM1JyaUhUeTFIZHYyWWcwZUFCUTZiQW9hZy92cXJ5blVMd3p2Q3VjSUNn
Z29abWk1UwpZTlhDbWVOM2VNR0NNTVQrSzBjQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0tr
TUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZCZ0hEdldEejNGRWI2WjJYaGZ2bm9D
aTRZZ3RNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdn
RUJBRmYrcFltUmxPMm1SWE5VVTZVegpjVTdPOEJycHh5bzlPV0FIZnZZQzducXdiVUdhTDFMeGhxYUwx
QXJOemdiNDZoNnRMd0tnbG9sUTY3WHUxUDdkCkQ5UHVrYWx0UEY4dDJNVERYZkN6aE9XNVFwTzNHVnk1
eEpCTUFnSENJREgxcTdHSmhzcTYxUnVTdkQzNVlpdHkKS01rR1dCVjY5bEZNZHRLOFdLSXNlRG1UN05U
cFBFT1hFTE4zc0hJVGYwMDhFN3RoOFA4RFFRYTlCSC8ycFR3SQpFTzNvL1MxZysyMDZVdW91WDBzNDd2
WnRycW5uKzZaVHZ5amR6THYveXRGcnc2RHNXbWt4cjkxcHdYVVVsU2FzClhGbnovMkJLa0JHS1kvRzRw
bG5xTEFRcFhwT28yYmdIb0FvR2oydzZQcGd6aWR6S1JGTkpUK0xwbUVVUTQ4SksKQ1pVPQotLS0tLUVO
RCBDRVJUSUZJQ0FURS0tLS0tCg==
namespace: a3ViZS1zeXN0ZW0=

token:
ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluVXdYMlZoVUhSdU9GTnFSRmRFVjIxTFYzSmhWMFZ1
WVRSQ0xWVkpjMGRYU2tSUVMweFFTbkpFTW5NaWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxj
blpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZ
VzFsYzNCaFkyVWlPaUpyZFdKbExYTjVjM1JsYlNJc0ltdDFZbVZ5Ym1WMFpYTXVhVzh2YzJWeWRtbGpa
V0ZqWTI5MWJuUXZjMlZqY21WMExtNWhiV1VpT2lKM1lXNW5MWE5sWTNKbGRDSXNJbXQxWW1WeWJtVjBa
WE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWeWRtbGpaUzFoWTJOdmRXNTBMbTVoYldVaU9pSjNZ
VzVuSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXpaWEoyYVdObExXRmpZ
MjkxYm5RdWRXbGtJam9pT1RCa01HUXlaVFV0T1RZek5pMDBOelZtTFdGbU5EY3RORFF4WkdFek56bGpN
alEzSWl3aWMzVmlJam9pYzNsemRHVnRPbk5sY25acFkyVmhZMk52ZFc1ME9tdDFZbVV0YzNsemRHVnRP
bmRoYm1jaWZRLlhwN3I2S29NQ09YQ0dIX1J5UW1uYUtOSXl1MVJpR2JFSktVekhBdE9lY1FtZ21fVUxL
TFNKbldoZDRpMVhHWUpGMTVEeUdUZnAwM2dZUWluNHpJakhWeG1qSl8ycnlmSWVtc1BuQ0g5X3Btd0Ji
eEhGSzBXX1JxcDQ2SktETnhqbE9ybUZzeV9OQ3RUa1hwdnFhSlR4OURodHgtN0tvSDFsODBHNHU3NEZO
cjYxeVctNHV6ODRWaFhEZzRXYzNSSUpJN1dDMm5tLWxsSk9kaXM0N0lQQjhSTlJ3ZE1LMTdsZm9OQXVz
Q0FQcllCcWVlbkNWdmg0blFGbzlIb3JRdk1Fc1ZuejRhTk5wc3NoRFFOTnZUV1RWeDhzM1hvaVNxbVN0
MjRuMXhsdEF3YUNjeDN2cTFtYVV5dDJWUWgxMXE3dDYwTEV4TUc3ekNHcXJoRXg5X3M3dw==
kind: Secret
metadata:
annotations:
kubectl.kubernetes.io/last-applied-configuration: |
{"apiVersion":"v1","kind":"Secret","metadata":{"annotations":
{"kubernetes.io/service-account.name":"bowen"},"name":"bowen-
secret","namespace":"kube-system"},"type":"kubernetes.io/service-account-token"}
kubernetes.io/service-account.name: bowen
kubernetes.io/service-account.uid: 90d0d2e5-9636-475f-af47-441da379c247
creationTimestamp: "2023-06-03T14:29:23Z"
name: bowen-secret
namespace: kube-system
resourceVersion: "1845479"
uid: b44c38ad-4ff0-4944-b34a-cd5ab3525ef3
type: kubernetes.io/service-account-token

#对上面的TOKEN进行base64解码后生成TOKEN变量
[root@master1 ~]#TOKEN=$(echo
ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluVXdYMlZoVUhSdU9GTnFSRmRFVjIxTFYzSmhWMFZ1
WVRSQ0xWVkpjMGRYU2tSUVMweFFTbkpFTW5NaWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxj
blpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZ
VzFsYzNCaFkyVWlPaUpyZFdKbExYTjVjM1JsYlNJc0ltdDFZbVZ5Ym1WMFpYTXVhVzh2YzJWeWRtbGpa
V0ZqWTI5MWJuUXZjMlZqY21WMExtNWhiV1VpT2lKM1lXNW5MWE5sWTNKbGRDSXNJbXQxWW1WeWJtVjBa
WE11YVc4dmMyVnlkbWxqWldGalkyOTFiblF2YzJWeWRtbGpaUzFoWTJOdmRXNTBMbTVoYldVaU9pSjNZ
VzVuSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXpaWEoyYVdObExXRmpZ
MjkxYm5RdWRXbGtJam9pT1RCa01HUXlaVFV0T1RZek5pMDBOelZtTFdGbU5EY3RORFF4WkdFek56bGpN
alEzSWl3aWMzVmlJam9pYzNsemRHVnRPbk5sY25acFkyVmhZMk52ZFc1ME9tdDFZbVV0YzNsemRHVnRP
bmRoYm1jaWZRLlhwN3I2S29NQ09YQ0dIX1J5UW1uYUtOSXl1MVJpR2JFSktVekhBdE9lY1FtZ21fVUxL
TFNKbldoZDRpMVhHWUpGMTVEeUdUZnAwM2dZUWluNHpJakhWeG1qSl8ycnlmSWVtc1BuQ0g5X3Btd0Ji
eEhGSzBXX1JxcDQ2SktETnhqbE9ybUZzeV9OQ3RUa1hwdnFhSlR4OURodHgtN0tvSDFsODBHNHU3NEZO
cjYxeVctNHV6ODRWaFhEZzRXYzNSSUpJN1dDMm5tLWxsSk9kaXM0N0lQQjhSTlJ3ZE1LMTdsZm9OQXVz
Q0FQcllCcWVlbkNWdmg0blFGbzlIb3JRdk1Fc1ZuejRhTk5wc3NoRFFOTnZUV1RWeDhzM1hvaVNxbVN0
MjRuMXhsdEF3YUNjeDN2cTFtYVV5dDJWUWgxMXE3dDYwTEV4TUc3ekNHcXJoRXg5X3M3dw==|base64 -
d)

[root@master1 ~]#curl -s  --cacert /etc/kubernetes/pki/ca.crt -H "Authorization:
Bearer ${TOKEN}" https://kubeapi.bowen.org:6443|head
{
"paths": [
"/.well-known/openid-configuration",
"/api",
"/api/v1",

"/apis",
"/apis/",
"/apis/admissionregistration.k8s.io",
"/apis/admissionregistration.k8s.io/v1",
"/apis/apiextensions.k8s.io",
```

案例: 实现 Prometheus 的权限

将Prometheus部署运行于Kubernetes之上并监控集群时，需要使用专用的ServiceAccount运行该Pod并认证和授权到API Server。
```yaml
#ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRole
metadata:
name: prometheus
rules:
- apiGroups: [""]
resources:
- nodes
- nodes/proxy
- services
- endpoints
- pods
verbs: ["get", "list", "watch"]
- apiGroups:
- extensions
resources:
- ingresses
verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
verbs: ["get"]

#创建 SA
---
apiVersion: v1 kind: ServiceAccount
metadata:
name: prometheus
namespace: prom

---
#ClusterRoleBinding

apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
name: prometheus
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: prometheus
subjects:
- kind: ServiceAccount
name: prometheus
namespace: prom
```

## 3.5 ClusterRole 和 RoleBinding 混合组合实现

### 3.5.1 RBAC 混合绑定说明

即在混合级别实践的场景中，只需要将用户关联同一个clusterrole，那么这个用户只能在指定的namespace空间中进行相应的操作。

**命令格式**
```bash
#查看混合实践格式
kubectl create rolebinding NAME --clusterrole=NAME|--role=NAME [--user=username]
[--namespace=namespace]

#属性解析：对于rolebinding来说，可以基于clusterrole和role两种角色进行绑定操作。

#示例:引用ClusterRole
kubectl create rolebinding jerry-attachto-cluster-admin --clusterrole=cluster-
admin --user=jerry --namespace=test
#而后可测试jerry用户对test及其它名称空间中的资源对象的访问权限
```

### 3.5.2 RBAC 混合绑定案例

#### 3.5.2.1 案例1

范例:
```yaml
#为了避免之前所做的rolebinding和clusterrolebinding对混合实践的影响，需要将之前所做的操作全
部清空，对subject账号和clusterrole、role无需变动
#清理环境
[root@master1 ~]#kubectl  delete  clusterrolebindings myclusterrolebinding
[root@master1 ~]#kubectl  delete  rolebindings  bowen-myrole
[root@master1 ~]#kubectl  delete  roles myrole

#当前subject和clusterrole现状
[root@master1 ~]#kubectl get clusterrole | egrep 'NAME|my'
NAME                                            CREATED AT
myclusterrole                                   2021-03-31T15:32:43Z

[root@master1 ~]# kubectl config get-contexts
CURRENT   NAME                          CLUSTER      AUTHINFO
NAMESPACE
*         kubernetes-admin@kubernetes   kubernetes   kubernetes-admin

#创建绑定角色
[root@master1 ~]#kubectl create rolebinding mixrole --clusterrole=myclusterrole -
-user=bowen  --dry-run=client -o yaml > security-mixbinding.yaml

#定制该资源定义文件
[root@master1 ~]#cat security-mixbinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: mixrole
roleRef:
apiGroup: rbac.authorization.k8s.io

kind: ClusterRole
name: myclusterrole
subjects:
- apiGroup: rbac.authorization.k8s.io
kind: User
name: bowen
#属性解析：将自动生成的配置文件中的时间戳删除，然后给其设定了一个namespace的权限范围属性

#应用资源对象
[root@master1 ~]#kubectl apply  -f  security-mixbinding.yaml

#检查效果
[root@master1 ~]#kubectl get rolebindings
NAME      ROLE                        AGE
mixrole   ClusterRole/myclusterrole   60s

[root@master1 ~]#kubectl describe rolebindings mixrole
Name:         mixrole
Labels:       <none>
Annotations:  <none>
Role:
Kind:  ClusterRole
Name:  myclusterrole
Subjects:
Kind  Name  Namespace
----  ----  ---------
User  bowen

#结果显示：已经将bowen采用rolebinding的方式赋予其clusterrole的角色权限

#检查效果
[root@master1 ~]#kubectl get pod --context=bowen@mycluster  --
kubeconfig=/tmp/bowen.conf
NAME       READY   STATUS    RESTARTS       AGE
pod-test   1/1     Running   1 (157m ago)   2d2h

[root@master1 ~]#kubectl get pod --context=bowen@mycluster -n kube-system --
kubeconfig=/tmp/bowen.conf
Error from server (Forbidden): pods is forbidden: User "bowen" cannot list
resource "pods" in API group "" in the namespace "kube-system"
#结果显示：对于rolebinding的clusterrole来说，我们只能访问指定的default空间中的资源。

[root@master1 ~]#kubectl delete rolebindings mixrole
```

#### 3.5.2.2 案例2

对于自定义的myclusterrole来说，它对于pod只有查看的权限，没有删除的权限。
```yaml
#查看效果
[root@master1 ~]#kubectl delete pod pod-test --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf
Error from server (Forbidden): pods "pod-test" is forbidden: User "bowen" cannot
delete resource "pods" in API group "" in the namespace "default"
#结果显示：我们无法对dafault命名空间的pod资源做权限之外的事情。

#官方给default空间提供了很多权限，admin的权限就是极大的

[root@master1 ~]# kubectl get clusterrole admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
...
- apiGroups:
- ""
resources:
- pods
- pods/attach
- pods/exec
- pods/portforward
- pods/proxy
verbs:
- create
- delete
- deletecollection
- patch
- update
...
#可以看到：admin的clusterrole它是在default命名空间中的，而且对pod有各种操作权限
```

范例:
```bash
#定制混合绑定
[root@master1 ~]# kubectl create rolebinding default-ns-admin  --
clusterrole=admin --user=bowen

#查看效果
[root@master1 ~]#kubectl describe rolebindings default-ns-admin
Name:         default-ns-admin
Labels:       <none>
Annotations:  <none>
Role:
Kind:  ClusterRole
Name:  admin
Subjects:
Kind  Name  Namespace
----  ----  ---------
User  bowen

#资源操作
[root@master1 ~]#kubectl get pod --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf
NAME       READY   STATUS    RESTARTS       AGE
pod-test   1/1     Running   1 (171m ago)   2d3h

#删除default的pod成功
[root@master1 ~]#kubectl delete pod pod-test --context=bowen@mycluster --
kubeconfig=/tmp/bowen.conf

[root@master1 ~]# kubectl get pod --context=bowen@mycluster -n kube-system --
kubeconfig=/tmp/bowen.conf
Error from server (Forbidden): pods is forbidden: User "bowen" cannot list
resource "pods" in API group "" in the namespace "kube-system"
#结果显示：只能管理当前命名空间的资源，其他命名空间的资源是管理不了的。
```

#### 3.5.2.3 案例3
```bash
[root@master1 ~]#kubectl create ns test

#授予bowen用户在名称空间test的集群级的管理员权限
[root@master1 ~]#kubectl create rolebinding bowen-cluster-admin --
clusterrole=cluster-admin --user=bowen -n test

#授予bowen用户在名称空间test的名称空间级的管理员权限
[root@master1 ~]#kubectl create rolebinding bowen-admin --clusterrole=admin --
user=bowen -n test
```

#### 3.5.2.4 案例4： 实现多个名称空间的管理员
```yaml
[root@master1 ~]#cat securiy-admin-ns.yaml
apiVersion: v1
kind: Namespace
metadata:
name: prod-ns
---
apiVersion: v1
kind: ServiceAccount
metadata:
name: tom
#namespace: bowenns  #SA帐号所在名空空间和它所管理的名称空间无关
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: tom-secret
annotations:
kubernetes.io/service-account.name: "tom"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: prod-ns-tom-clusterrolebinding
namespace: prod-ns
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: tom
namespace: default

---
apiVersion: v1
kind: Namespace
metadata:
name: test-ns
---
apiVersion: v1
kind: ServiceAccount

metadata:
name: jerry
#namespace: default
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: jerry-secret
annotations:
kubernetes.io/service-account.name: "jerry"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: test-ns-jerry-clusterrolebinding
namespace: test-ns
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: jerry
namespace: default

---
apiVersion: v1
kind: Namespace
metadata:
name: dev-ns
---
apiVersion: v1
kind: ServiceAccount
metadata:
name: jack
#namespace: dev-ns
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: jack-secret
annotations:
kubernetes.io/service-account.name: "jack"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: dev-ns-jack-clusterrolebinding
namespace: m61
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: jack

namespace: default
```
```bash
[root@master1 ~]#kubectl apply -f  securiy-admin-ns.yaml

[root@master1 ~]#kubectl  get ns
NAME                   STATUS   AGE
default                Active   17d
prod-ns                Active   23s
dev-ns                 Active   23s
test-ns                Active   23s

[root@master1 ~]#kubectl  get sa
NAME      SECRETS   AGE
default   0         17d
jack      0         27s
jerry     0         27s
tom       0         27s

[root@master1 ~]#kubectl  get secrets
NAME           TYPE                                  DATA   AGE
jack-secret    kubernetes.io/service-account-token   3      36s
jerry-secret   kubernetes.io/service-account-token   3      36s
tls-bowen       kubernetes.io/tls                     2      2d3h
tom-secret     kubernetes.io/service-account-token   3      36s

[root@master1 ~]#kubectl  get  rolebindings.rbac.authorization.k8s.io
NAME                ROLE          AGE
admin-rolebinding   Role/myrole   155m

[root@master1 ~]#kubectl  get  rolebindings.rbac.authorization.k8s.io  -n prod-
ns
NAME                         ROLE                        AGE
prod-ns-tom-clusterrolebinding   ClusterRole/cluster-admin   55s

[root@master1 security]#kubectl  get  rolebindings.rbac.authorization.k8s.io  -n
test-ns
NAME                           ROLE                        AGE
test-ns-jerry-clusterrolebinding   ClusterRole/cluster-admin   59s

[root@master1 security]#kubectl  get  rolebindings.rbac.authorization.k8s.io  -n
m61
NAME                          ROLE                        AGE
m61-jack-clusterrolebinding   ClusterRole/cluster-admin   60s

#获取Token
[root@master1 ~]#kubectl  describe  secrets tom-secret
Name:         tom-secret
Namespace:    default
Labels:       kubernetes.io/legacy-token-last-used=2024-10-10
Annotations:  kubernetes.io/service-account.name: tom
kubernetes.io/service-account.uid: 97ad4292-26cc-419f-92c7-
f44675f09981

Type:  kubernetes.io/service-account-token

Data
====

ca.crt:     1107 bytes
namespace:  7 bytes
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6Imp2aFBoSUxLVU5LUUc2aU1LeWloaHlIbjVWZXBuZDlVN2tSRnho
Z0N1RHMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb
3VudC9zZWNyZXQubmFtZSI6InRvbS1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L
3NlcnZpY2UtYWNjb3VudC5uYW1lIjoidG9tIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZ
XJ2aWNlLWFjY291bnQudWlkIjoiOTdhZDQyOTItMjZjYy00MTlmLTkyYzctZjQ0Njc1ZjA5OTgxIiwic
3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6dG9tIn0.HfwL5PIrTNpwd5YAJW_4yC5QU
9bb9qyAb74eB-MlfihJ_VIxsGCTzl4r0IXH1LMETjGEN1cuL5VNvpbTvZNCK-
MeShpB6ZK11VAAJXVw310VIc6Ecx0rjfoj-taLHjYqHW2MXrQjlNYQGZokYJHy0WZ-
D1fISWGou58dn91WChKCYH_xXG7CcT-
HqE23bHds1AK2wi9hkONVgIu3aWTXc1wgU4Sk7Bgeye016ZYfyow69_QIgiKHqjNouz3TcwCqk-
u3tiZ1zDALrR1CkI4K7Jj8JbuBMZbSbElZMFPevkmDFMD-
IWcxaM43nJWZ6EPs11SzQStKrJDXbn_HYtLizg

[root@master1 ~]#kubectl  describe  secrets jerry-secret
[root@master1 ~]#kubectl  describe  secrets jack-secret

#集群外主机,用token测试访问验证权限
[root@ubuntu2204 ~]#TOKEN_TOM=eyJhbGciOiJSUzI1NiIsImtpZCI6Imp
[root@ubuntu2204 ~]#TOKEN_JERRY=eyJhbGciOiJSUzI1NiIsImtpZCI6I
[root@ubuntu2204 ~]#TOKEN_JACK=eyJhbGciOiJSUzI1NiIsImtpZCI6Im

#无权限访问default名称空间
[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_TOM}  get pod   --insecure-skip-tls-verify
Error from server (Forbidden): pods is forbidden: User
"system:serviceaccount:default:tom" cannot list resource "pods" in API group ""
in the namespace "default"

#可以访问授权的名称空间
[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_TOM}  create deploy myapp --image registry.cn-
beijing.aliyuncs.com/bowen/pod-test:v0.1  -n prod-ns --insecure-skip-tls-
verify
deployment.apps/myapp created

[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_TOM}  get pod  -n prod-ns --insecure-skip-tls-verify
NAME                     READY   STATUS    RESTARTS   AGE
myapp-64b4b8487f-5zzb8   1/1     Running   0          8s
```
```bash
[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_JERRY}  get pod  -n prod-ns --insecure-skip-tls-verify
Error from server (Forbidden): pods is forbidden: User
"system:serviceaccount:default:jerry" cannot list resource "pods" in API group
"" in the namespace "prod-ns"

[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_JERRY}  create deploy myapp --image registry.cn-
beijing.aliyuncs.com/bowen/pod-test:v0.1  -n test-ns --insecure-skip-tls-
verify
deployment.apps/myapp created

[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_JERRY}  get pod  -n test-ns --insecure-skip-tls-verify
NAME                     READY   STATUS    RESTARTS   AGE
myapp-64b4b8487f-szscl   1/1     Running   0          4s

[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_JACK}  create deploy myapp --image registry.cn-
beijing.aliyuncs.com/bowen/pod-test:v0.1  -n dev-ns --insecure-skip-tls-
verify
deployment.apps/myapp created

[root@ubuntu2204 ~]#kubectl -s https://kubeapi.bowen.org:6443 --
token=${TOKEN_JACK}  get pod  -n dev-ns --insecure-skip-tls-verify
NAME                     READY   STATUS    RESTARTS   AGE
myapp-64b4b8487f-r96f5   1/1     Running   0          9s
```

## 3.6 案例：Dashboard

### 3.6.1 Dashboard 基本环境

#### 3.6.1.1 dashboard 介绍

Kubernetes 官方提供了基于Web的界面的Dashboard功能。

dashboard组件部署用到了很多和服务认证相关的内容，而且只有先配置serviceaccount才能继续。
```text
#参考资料:
https://kubernetes.io/docs/concepts/cluster-administration/addons/
#kubernetes-dashboard
https://github.com/kubernetes/dashboard

#注意：dashboard版本没有通用的，只能找到适合当前kubernetes版本的软件。
#查看版本支持
https://github.com/kubernetes/dashboard/releases
```

![原 PDF 第 130 页插图](assets/Kubernetes安全机制_Password_Removed1/img-5cb66877a7dd9b62.png)

#### 3.6.1.2 部署 Dashboard

**安装说明**


- <https://github.com/kubernetes/dashboard?tab=readme-ov-file#installation>

```text
#注意:v2.7.0以后版本只支持Helm安装
```

范例: 通过manifest文件安装
```yaml
#获取官方的yaml文件,下载并修改配置文件
[root@master1 ~]#VERSION=v2.7.0
[root@master1 ~]#VERSION=v2.0.0

#通过代理下载
[root@ubuntu2204 ~]#wget
https://mirror.ghproxy.com/https://raw.githubusercontent.com/kubernetes/dashboar
d/${VERSION}/aio/deploy/recommended.yaml
[root@master1 ~]#wget
https://raw.githubusercontent.com/kubernetes/dashboard/${VERSION}/aio/deploy/recommended.yaml

[root@master1 ~]#vim recommended.yaml
.......
kind: Service
apiVersion: v1
metadata:
labels:
k8s-app: kubernetes-dashboard
name: kubernetes-dashboard
namespace: kubernetes-dashboard
spec:
#type: NodePort            # 新增此行，指定类型
type: LoadBalancer         # 新增此行，指定类型
ports:
- port: 443
targetPort: 8443
nodePort: 30000       #新增此行，指定该端口作为外界访问入口的端口,端口必须在30000-
32767之间
..........

#注意：修改主要是镜像源的修改和启动端口的配置，采用NodePort 可以在所有的节点上都开启一个端口用
于dashboard访问
#依赖两个镜像：kubernetesui/dashboard:v2.3.1 和 kubernetesui/metrics-scraper:v1.0.6

#应用配置,会自动下载两个镜像dashboard和metrics-scraper到某个node节点
[root@master1 ~]#kubectl apply -f recommended.yaml

[root@master1 ~]#kubectl get svc -n kubernetes-dashboard   kubernetes-dashboard
NAME                   TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)
AGE
kubernetes-dashboard   NodePort   10.101.2.160   <none>        443:30000/TCP
2m34s

[root@master1 ~]#kubectl get pod -n kubernetes-dashboard

NAME                                        READY   STATUS    RESTARTS   AGE
dashboard-metrics-scraper-7bc864c59-k4q6r   1/1     Running   0          3m5s
kubernetes-dashboard-6c7ccbcf87-bjxvh       1/1     Running   0          3m5s
```

#### 3.6.1.3 部署 metric-server 方便在dashboard中观察性能指标,可选
```yaml
#没有部署metrics-server时,会提示下面错误,此步可选
[root@master1 ~]#kubectl top node
error: Metrics API not available

#建议安装metrics-server,可以通过dashboard查看更多的信息,此步可选
#官方链接:https://github.com/kubernetes-sigs/metrics-server
[root@master1 ~]#curl -LO https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

#默认文件需要修改才能工作,因为默认需要内部证书验证和镜像地址k8s.gcr.io所以修改,此步可选
[root@master1 ~]#vim components.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
labels:
k8s-app: metrics-server
name: metrics-server
namespace: kube-system
spec:
selector:
matchLabels:
k8s-app: metrics-server
strategy:
rollingUpdate:
maxUnavailable: 0
template:
metadata:
labels:
k8s-app: metrics-server
spec:
containers:
- args:
- --cert-dir=/tmp
- --secure-port=4443
- --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
- --kubelet-use-node-status-port
- --metric-resolution=15s
- --kubelet-insecure-tls   #添加此行
image: registry.cn-hangzhou.aliyuncs.com/google_containers/metrics-
server:v0.6.1 #添加此行
#image: k8s.gcr.io/metrics-server/metrics-server:v0.6.1
imagePullPolicy: IfNotPresent
livenessProbe:
……

#应用此文件,此步可选
[root@master1 ~]#kubectl apply -f components.yaml

#添加一个资源群组,此步可选
[root@master1 ~]#kubectl api-versions

admissionregistration.k8s.io/v1
apiextensions.k8s.io/v1
apiregistration.k8s.io/v1
apps/v1
authentication.k8s.io/v1
authorization.k8s.io/v1
autoscaling/v1
autoscaling/v2
autoscaling/v2beta2
batch/v1
certificates.k8s.io/v1
coordination.k8s.io/v1
discovery.k8s.io/v1
events.k8s.io/v1
flowcontrol.apiserver.k8s.io/v1beta1
flowcontrol.apiserver.k8s.io/v1beta2
metrics.k8s.io/v1beta1  #添加一个新的资源群组
networking.k8s.io/v1
node.k8s.io/v1
policy/v1
rbac.authorization.k8s.io/v1
scheduling.k8s.io/v1
storage.k8s.io/v1
storage.k8s.io/v1beta1
v1

#一旦metrics-server部署完成,就可通过下面命令查看CPU/memory相关性能指标,此步可选
[root@master1 ~]#kubectl top node
NAME               CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
master1.bowen.org   145m         7%     1113Mi          60%
master2.bowen.org   128m         6%     1005Mi          54%
master3.bowen.org   113m         5%     1018Mi          54%
node1.bowen.org     61m          3%     904Mi           48%
node2.bowen.org     62m          3%     855Mi           46%
node3.bowen.org     81m          4%     890Mi           48%

[root@master1 ~]#kubectl top pod,此步可选
NAME                       CPU(cores)   MEMORY(bytes)
demoapp-78b49597cf-j2bk2   1m           22Mi
demoapp-78b49597cf-jxtj9   1m           23Mi
demoapp-78b49597cf-lt5qn   1m           23Mi

[root@master1 ~]#kubectl top pod demoapp-78b49597cf-j2bk2,此步可选
NAME                       CPU(cores)   MEMORY(bytes)
demoapp-78b49597cf-j2bk2   1m           22Mi

#查看SVC的地址：https://10.0.0.12/
[root@master1 ~]#kubectl get svc -n kubernetes-dashboard
NAME                        TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)
AGE
dashboard-metrics-scraper   ClusterIP      10.101.57.57   <none>        8000/TCP
2m38s
kubernetes-dashboard        LoadBalancer   10.98.42.43    10.0.0.12
443:32082/TCP   2m38s
```

浏览器访问任意master或worker节点的主机。

访问链接https://node1.bowen.org:30000/ ，可以看到下面提示

访问链接http://<集群任意节点>:30000/ ，可以看到下面提示

注意：对浏览器有兼容性问题，有些浏览器，比如：chrome,edge等无法访问。

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-d67d320e11eebcac.png)

访问链接https://<集群任意节点>:30000/ ，可以看到下面提示

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6bc301e8a97ae9b4.png)

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-4fbeb97e63cc5316.png)

#### 3.6.1.4 部署 ingress
```html
#定制ingress资源配置文件
[root@master1 ~]#cat ingress-https-dashboard.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
name: ingress-dashboard
namespace: kubernetes-dashboard
annotations:
kubernetes.io/ingress.class: "nginx"
ingress.kubernetes.io/ssl-passthrough: "true"              #进行TLS透传，四层代
理
nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"      #指定对后端启用https
协议的访问
nginx.ingress.kubernetes.io/rewrite-target: /$2

spec:
rules:
- host: www.bowen.org
http:
paths:
- path: /dashboard(/|$)(.*)
pathType: Prefix
backend:
service:
name: kubernetes-dashboard
port:
number: 443
#- host: dashboard.bowen.org  #下面相关配置需要配合
nginx.ingress.kubernetes.io/rewrite-target: /$1 使用
#http:
#  paths:
#  - path: /(.*)
#    pathType: Prefix
#    backend:
#      service:
#        name: kubernetes-dashboard
#        port:
#          number: 443

#应用资源文件
[root@master1 ~]#kubectl apply -f ingress-https-dashboard.yaml

#查看效果
[root@master1 ~]#kubectl get ingress -n kubernetes-dashboard
NAME                CLASS    HOSTS             ADDRESS   PORTS   AGE
ingress-dashboard   <none>   www.bowen.org             80      16s

[root@master1 ~]#kubectl describe ingress -n kubernetes-dashboard
Name:             ingress-dashboard
Namespace:        kubernetes-dashboard
Address:          10.0.0.104
Default backend:  default-http-backend:80 (<error: endpoints "default-http-
backend" not found>)
Rules:

Host             Path  Backends
----             ----  --------
www.bowen.org
/dashboard(/|$)(.*)   kubernetes-dashboard:443
(10.244.4.34:8443)
Annotations:       ingress.kubernetes.io/ssl-passthrough: true
kubernetes.io/ingress.class: nginx
nginx.ingress.kubernetes.io/backend-protocol: HTTPS
nginx.ingress.kubernetes.io/rewrite-target: /$2
Events:
Type    Reason  Age                From                      Message
----    ------  ----               ----                      -------
Normal  Sync    56s (x2 over 80s)  nginx-ingress-controller  Scheduled for
sync

#在客户端完成发下名称解析
10.0.0.101 master1 master1.bowen.org www.bowen.org

#HTTP自动跳转HTTPS
[root@ubuntu2004 ~]#curl http://www.bowen.org/dashboard
<html>
<head><title>308 Permanent Redirect</title></head>
<body>
<center><h1>308 Permanent Redirect</h1></center>
<hr><center>nginx</center>
</body>
</html>

[root@ubuntu2004 ~]#curl -Lk http://www.bowen.org/dashboard
<!--
Copyright 2017 The Kubernetes Authors.
```


Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at


- <http://www.apache.org/licenses/LICENSE-2.0>

```html
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
--><!DOCTYPE html><html lang="en" dir="ltr"><head>
<meta charset="utf-8">
<title>Kubernetes Dashboard</title>
<link rel="icon" type="image/png" href="assets/images/kubernetes-logo.png">
<meta name="viewport" content="width=device-width">
<style>html,body{height:100%;margin:0}*::-webkit-
scrollbar{background:transparent;height:8px;width:8px}</style><link
rel="stylesheet" href="BOOTSTRAP_TOKEN.css" media="print"
onload="this.media='all'"><noscript><link rel="stylesheet"
href="BOOTSTRAP_TOKEN.css"></noscript></head>

<body>
<kd-root></kd-root>

<script src="runtime.134ad7745384bed8.js" type="module"></script><script
src="polyfills.5c84b93f78682d4f.js" type="module"></script><script
src="scripts.2c4f58d7c579cacb.js" defer></script><script
src="en.main.3550e3edca7d0ed8.js" type="module"></script>

</body></html>

#浏览器访问 https://www.bowen.org/dashboard/ 查看效果，注意，dashboard后面有/
#结果显示：借助于nginx-controller的tls功能可以正常的实现相关的https的效果。
```

#### 3.6.1.5 认证解析

从界面中可以看到访问dashboard需要通过Token或者kubeconfig授权才能登陆，但是dashboard本身不提供授权，因为dashborad是一个pod，实际上我们是使用这个pod认证到k8s的集群中去的，所以需要为dashborad的pod提供token或者kubeconfig认证，所以这里的认证主体应该是serviceaccount。

对于dashboard的认证方法主要有两种：令牌认证和文件认证。

令牌认证

基于SA认证用户的唯一令牌来进行认证，有默认的超时机制，等一会儿会失效。

文件认证

基于SA账号的token信息，创建kubeconfig文件，实现长久的认证方式。

对于dashboard配置的操作流程：

创建专用的serviceaccount创建对应的权限角色将serviceaccount和权限角色进行关联绑定。

**清理之前的记录**
```bash
kubectl delete clusterrolebindings kubernetes-dashboard
kubectl delete serviceaccount dashboard-admin -n kube-system
```

### 3.6.2 Token 登录认证

#### 3.6.2.1 集群级别用户

##### 3.6.2.1.1 SA帐号的认证和授权

###### 3.6.2.1.1.1 方法1: 命令方式
```bash
#创建专用的SA服务账户,注意SA所在名称空间并不决定可以管理的Pod所在名称空间
kubectl create serviceaccount dashboard-admin -n kube-system

#将SA帐号利用集群角色绑定至集群角色cluster-admin
kubectl create clusterrolebinding  dashboard-admin --clusterrole=cluster-admin -
-serviceaccount=kube-system:dashboard-admin

#参数详解：
--clusterrole=集群角色名称
--serviceaccount=命名空间:serviceaccountname

#SA的命名空间是kube-system
#dashboard需要操作各种资源的所有权限，所以我们需要和cluster-admin的clusterrole进行绑定
```

###### 3.6.2.1.1.2 方法2: 资源清单方式
```yaml
#资源定义文件方式
[root@master1 ~]#cat security-dashboard-admin.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: dashboard-admin
namespace: kube-system
labels:
kubernetes.io/cluster-service: "true"
addonmanager.kubernetes.io/mode: Reconcile
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
name: dashboard-admin
annotations:
rbac.authorization.kubernetes.io/autoupdate: "true"
roleRef:
kind: ClusterRole
name: cluster-admin
apiGroup: rbac.authorization.k8s.io
subjects:
- kind: ServiceAccount
name: dashboard-admin
namespace: kube-system

[root@master1 ~]#kubectl apply -f yaml/security-dashboard-admin.yaml
```

##### 3.6.2.1.2 获取 Token

范例: k8s-v1.24版本后,创建SA帐号后不会自动创建secret,需要手动创建secret
```yaml
[root@master1 ~]#cat security-dashboard-admin-secret.yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: dashboard-admin-secret
namespace: kube-system
annotations:
kubernetes.io/service-account.name: "dashboard-admin"

[root@master1 ~]#kubectl apply  -f security-dashboard-admin-secret.yaml
secret/dashboard-admin-secret created

#查看创建的Secret
[root@master1 ~]#kubectl get secret -A  | grep dashboard-admin
kube-system            dashboard-admin-secret            kubernetes.io/service-
account-token   3      68s

#查看Secret关联的Token
[root@master1 ~]#kubectl describe secrets -n kube-system dashboard-admin-secret
Name:         dashboard-admin-secret
Namespace:    kube-system
Labels:       <none>

Annotations:  kubernetes.io/service-account.name: dashboard-admin
kubernetes.io/service-account.uid: c1a181c6-5e7d-4dd1-a835-
b1bd894a49b4

Type:  kubernetes.io/service-account-token

Data
====
namespace:  11 bytes
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6ImdnWW9DaGdfcFliSU15WnpqemVpaTZZTFFDcTJyS2dWMnBwU0xm
OTVwWmMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tc2VjcmV0Iiwia3ViZXJuZXRlcy5pb
y9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRhc2hib2FyZC1hZG1pbiIsImt1Y
mVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImMxYTE4MWM2LTVlN
2QtNGRkMS1hODM1LWIxYmQ4OTRhNDliNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlL
XN5c3RlbTpkYXNoYm9hcmQtYWRtaW4ifQ.CUzMaGl_6rkAfpvKFfam25URkc5V4Ury_horDJ9vSkXQbP
omYwkNK-oATorY8Fm3x1ozQofOcxuwUD4HHB-
rvmpXhWxDRePHlmXNDyv03RpNjgIT7bgRXF09Wz__6iCQjjXJj-NlRwSrKvNO-
ML4iL1biQbpsxjmsUECxDhG0FULfU2Nuqe1iuaWk7W7bXDS5dsR_242QrGnCboG0N98Z4q1_2sNxUUjz
5daVDDbf6gIKR893zD5EyAJSrYpWu3fUF4fs0fGJq8hMWgFk1gU55g4dWaG4wet_iOUTZkGvrBx9OKeL
FthUtgM-JDScW5lVTKKeP3kvo4ocIaah8BilQ
ca.crt:     1099 bytes
```

范例: k8s-v1.23版本之前创建SA会自动创建secret
```bash
#要使用token的方式来登录dashboard，而token保存在secrets中，所以需要基于该serviceaccount账
号对应secrets中获取令牌信息
#方法1：
[root@master1 ~]#kubectl describe secrets -n kube-system $(kubectl -n kube-system
get secret | awk '/dashboard-admin/{print $1}')

#方法2：
[root@master1 ~]#kubectl -n kube-system get secret | grep dashboard-admin
dashboard-admin-token-hqq7x                      kubernetes.io/service-account-
token   3      49s
[root@master1 ~]#kubectl describe secret  dashboard-admin-token-hqq7x -n kube-
system
Name:         dashboard-admin-token-hqq7x
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: dashboard-admin
kubernetes.io/service-account.uid: d074c5cb-ca75-4bf2-9efc-
472bed38dd4e

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  11 bytes

token:
eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qQVBTeTY0VDVfLTNNeE1yVXpuVmEtaGxkWngtdkozSUluY3ZI
cGJpS0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4taHFxN3giLCJrdWJlcm5ld
GVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluI
iwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDA3NGM1Y
2ItY2E3NS00YmYyLTllZmMtNDcyYmVkMzhkZDRlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50O
mt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.dyBCX-uLYqljBHK8kQ0UjtVtuBOHRwmaF-
LWRU9ZIVMssS9n4ybjnYGfHRNPTpgrRu7fnE5I7HJEwFxAWk-EH-
9VqKtBtNf00eMBqZ1P3W2JqDkR5AW5Tc85Wf-
EvO5uawy_KQF6FwrK1u0nRdu4JgYkf_zRG4KZTqXYemWJ8YbMhgQnVk2DknBrytopMkbT5vhdK7RyAY7
B_eYsssuCxBTs7EcDeaYi0VcGE7Sh08Rx4yLnn4MUUwUXXk9Itu4m4cjfsMyurs5M0usHgQcitmG8ADr
5xM2XVhkqO1ycqcbC4WxlSJmIXMCkqThCGzRTGSLjKOSo4VGsKICNqqIR5Q

#结果显示：配置好serviceaccount之后，会自动生成一个dashboard-admin-token-xxx格式的secret
信息,token：属性后面的加密信息，就是需要的内容，复制该内容到dashboard界面中的令牌输入框
#使用输出的token登录Dashboard。

#方法3:
#进入使用此SA用户dashboard-admin的Pod,访
问/var/run/sercets/kubernetes.io/serviceaccount/tokne
kubect exec pod-test -n testns -- cat
/var/run/sercets/kubernetes.io/serviceaccount/tokne

#注意:使用上面的Token登录dashboard后,只能看到testns的Pod
```

认证通过后，可以登录Dashboard。

结果显示：这里可以对任何用户空间进行管理操作,有时候我们需要不同的用户查看不同的资源内容，那么接下来需要对serviceaccount进行某个特定namespace环境中的实践。

#### 3.6.2.2 命名空间用户

只授权针对特定名称空间的资源进行管理

注意: 要保证sa和rolebinding都在同个名称空间。

方法1: 命令方式
```bash
#创建专用的服务账户
kubectl create serviceaccount def-ns-admin -n default

#使用角色绑定到指定名称空间的角色
kubectl create rolebinding def-ns-admin  --clusterrole=admin --
serviceaccount=default:def-ns-admin -n default
```

方法2: 文件方式
```yaml
#资源配置文件 security-dashboard-admin-ns.yaml
[root@master1 ~]#cat security-dashboard-admin-ns.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
name: def-ns-admin
namespace: default
---

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
name: def-ns-admin
namespace: default
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: admin
subjects:
- kind: ServiceAccount
name: def-ns-admin
namespace: default

[root@master1 ~]#kubectl apply -f yaml/security-dashboard-admin-ns.yaml

#查看sa
[root@master1 ~]#kubectl  get sa
NAME           SECRETS   AGE
def-ns-admin   1         3s
default        1         4d11h

[root@master1 ~]#kubectl  describe  sa def-ns-admin
Name:                def-ns-admin
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   def-ns-admin-token-k2nkb
Tokens:              def-ns-admin-token-k2nkb
Events:              <none>

#k8s-v1.24版本后,需要手动创建secret
[root@master1 ~]#cat security-dashboard-admin-ns-secret.yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: dashboard-def-ns-admin-secret
namespace: default
annotations:
kubernetes.io/service-account.name: "def-ns-admin"

#创建secret
[root@master1 ~]#kubectl apply  -f yaml/security-dashboard-admin-ns-secret.yaml

[root@master1 ~]#kubectl get secrets dashboard-def-ns-admin-secret
NAME                            TYPE                                  DATA   AGE
dashboard-def-ns-admin-secret   kubernetes.io/service-account-token   3      43s

[root@master1 ~]#kubectl describe secrets dashboard-def-ns-admin-secret
Name:         dashboard-def-ns-admin-secret
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: def-ns-admin

kubernetes.io/service-account.uid: 415ac1b9-a45c-4081-9916-
93ce99d7931d

Type:  kubernetes.io/service-account-token

Data
====
namespace:  11 bytes
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6ImdnWW9DaGdfcFliSU15WnpqemVpaTZZTFFDcTJyS2dWMnBwU0xm
OTVwWmMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tc2VjcmV0Iiwia3ViZXJuZXRlcy5pb
y9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRhc2hib2FyZC1hZG1pbiIsImt1Y
mVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImMxYTE4MWM2LTVlN
2QtNGRkMS1hODM1LWIxYmQ4OTRhNDliNCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlL
XN5c3RlbTpkYXNoYm9hcmQtYWRtaW4ifQ.CUzMaGl_6rkAfpvKFfam25URkc5V4Ury_horDJ9vSkXQbP
omYwkNK-oATorY8Fm3x1ozQofOcxuwUD4HHB-
rvmpXhWxDRePHlmXNDyv03RpNjgIT7bgRXF09Wz__6iCQjjXJj-NlRwSrKvNO-
ML4iL1biQbpsxjmsUECxDhG0FULfU2Nuqe1iuaWk7W7bXDS5dsR_242QrGnCboG0N98Z4q1_2sNxUUjz
5daVDDbf6gIKR893zD5EyAJSrYpWu3fUF4fs0fGJq8hMWgFk1gU55g4dWaG4wet_iOUTZkGvrBx9OKeL
FthUtgM-JDScW5lVTKKeP3kvo4ocIaah8BilQ
ca.crt:     1099 bytes

#k8s-v1.23版本之前自动创建secret
#获取全局令牌信息
[root@master1 ~]#kubectl  describe secrets  def-ns-admin-token-k2nkb
Name:         def-ns-admin-token-k2nkb
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: def-ns-admin
kubernetes.io/service-account.uid: df127795-3940-43dd-92ce-
ed7a6cb706d2

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  7 bytes
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qQVBTeTY0VDVfLTNNeE1yVXpuVmEtaGxkWngtdkozSUluY3ZI
cGJpS0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb
3VudC9zZWNyZXQubmFtZSI6ImRlZi1ucy1hZG1pbi10b2tlbi1rMm5rYiIsImt1YmVybmV0ZXMuaW8vc
2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJkZWYtbnMtYWRtaW4iLCJrdWJlcm5ld
GVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJkZjEyNzc5NS0zOTQwLTQzZ
GQtOTJjZS1lZDdhNmNiNzA2ZDIiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpkZ
WYtbnMtYWRtaW4ifQ.U-KdEPRJ4sYlV8VWSGOo57Nt7pq-
yytlEh8K7jdiphudCVzn0difQ2RnNWwfB_qDM60_EKxSOUEKs-
dEyvWSNVXaayZZOeHxZKi4z4lkcUX18BaBsgCg76YXlwPkjdX9YRtmRzpzaA5aJ2iTE61-
Aah7NwDs7tk_7BhZ08CEewE0H-01PDCtVwvbgDWv5OjZshX0Dc4KZTlPGaAEHl63TAerITKh_Uh6hq-
UHu6rRwiPQeMJ41trvn4f8sNNYDH6MUVYIZ4XvPP5FntB-
wESrjbC9pb1PIIOtbE4b81w51uk3sZ3LBLEANI3qkkYcRzzvZPWGc-yWjtV4QjWRfEFqg
#结果显示：token：属性后面的加密信息，就是我们需要的内容，复制该内容到dashboard界面中的令牌输
入框

#认证通过后，查看效果
```

![原 PDF 第 143 页插图](assets/Kubernetes安全机制_Password_Removed1/img-aad4813d5b133584.png)

![原 PDF 第 143 页插图](assets/Kubernetes安全机制_Password_Removed1/img-8e4641a7cb48e73f.png)

![原 PDF 第 144 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c888df68ca5d8159.png)

结果显示：当前的dashboard仅仅能管理default命名空间下的资源。

范例：创建一个管理dev名称空间的dashboard用户
```yaml
[root@master1 ~]#kubectl create ns dev
[root@master1 ~]#kubectl create serviceaccount admin -n dev
[root@master1 ~]#kubectl create rolebinding admin  --clusterrole=admin --
serviceaccount=dev:admin -n dev

[root@master1 ~]#cat security-dashboard-admin-dev-secret.yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: dashboard-admin-dev-secret
namespace: dev
annotations:
kubernetes.io/service-account.name: "admin"

#查看Token,注意：要使用kubectl describe命令查看，不要使用kubectl get命令
[root@master1 ~]#kubectl describe secrets -n dev dashboard-admin-dev-secret
Name:         dashboard-admin-dev-secret
Namespace:    dev
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: admin
kubernetes.io/service-account.uid: 5eab3d6f-54ba-4987-aa76-
aea85a41ea0a

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  3 bytes

token:
eyJhbGciOiJSUzI1NiIsImtpZCI6IjJxV0NPWVNUN0JNcmk3cWNuUjd1MXE3ZC1nT2FoYmtGTGFBYldW
VzVoemsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZXYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L
3NlY3JldC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluLXNlY3JldCIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJhZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjVlYWIzZDZmLTU0YmEtNDk4Ny1hYTc2LWFlYTg1Y
TQxZWEwYSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZXY6YWRtaW4ifQ.pVP27Ig2fxfnMp
KL9KfZH8hZNiMg1RruRj-zSDQkOLVMmkvDnolq_37V0g2ZhVyNYj0S11HQHsyxdXI-
w0TUvqfOPhutXnI4OHAw6ss-c89fWa6W3NZVUf3TyXBdXpSrQ2PVHWFaX4Gf_FT0sxkVzykFkwFpE-
d1X5Mru1df7McfK2JVy6ZcoQA7lDUdXoKcXribROol2CX1pflg6bAFSCpkOv0ZqaQ1maw6XpJgLf2Rv5
4lpkAhsQRRy6JwrQnIa5Uk7L0dPauLFZRoioiBl07Zhoe4SPEdPHM96A4yytjtDa6Pb8eyjkje_X5C01
qshtngSscBD1YFOIqNzU7qMw

#注意：有些版本的dashboard有bug，不能选择除default的其它名称空间，只能手动输入名称空间的名称
才可以
```

![原 PDF 第 145 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9c6cb0a1452e641c.png)

### 3.6.3 Kubeconfig 登录认证

#### 3.6.3.1 集群通用认证

##### 3.6.3.1.1 准备SA服务账号并授权
```bash
#参考token令牌认证当中的serviceaccount创建并做clusterrolebinding
#创建专用的SA服务账户,注意SA所在名称空间并不决定可以管理的Pod所在名称空间
[root@master1 ~]#kubectl create serviceaccount dashboard-admin -n kube-system

#将SA帐号利用集群角色绑定至集群角色cluster-admin
[root@master1 ~]#kubectl create clusterrolebinding  dashboard-admin --
clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin

[root@master1 ~]#kubectl get sa dashboard-admin -n kube-system
NAME              SECRETS   AGE
dashboard-admin   1         36h

[root@master1 ~]#kubectl get sa
NAME           SECRETS   AGE

def-ns-admin   1         80m
default        1         4d13h
```

##### 3.6.3.1.2 生成集群配置kubeconfig文件
```yaml
#设置集群信息
[root@master1 ~]#kubectl config set-cluster kubernetes --certificate-
authority=/etc/kubernetes/pki/ca.crt  --server="https://kubeapi.bowen.org:6443" --
embed-certs=true --kubeconfig=/root/kubeadmin.conf
#注意：设定cluster信息的时候，必须基于集群初始化时候的认证信息--ca证书：证书认证：--
certificate-authority

[root@master1 ~]#ll kubeadmin.conf
-rw------- 1 root root 1672 Apr  3 09:47 kubeadmin.conf

[root@master1 ~]#cat kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lH
OXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeU1ETXlPVEV5TkRB
ME9Wb1hEVE15TURNeU5qRXlOREEwT1Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FT
SXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBS1RBCkZvTGplT3Y2L2xVczZ1dGdH
aFdVV29LNXZkanp4YVkzekhINkFuSjJCVEx0UG5iL2NWdDJGNC9MVjVTY0s4SEYKOXdXYkZVbjBuMVBG
V1d6bi8rS3diRThtZGtZbHNTS09ENG1VdEg5VVN3TlpINnZDTkVBVnBDQ1ovbnRxbnA4dApWVy9xWXdr
T0JIRjY4SDY3aFJETFdVZG9xdDVhbHlXTlQrVjBQQjZLb2NHYnBJUUhXNkI1UGxJVGpkY2xOT3BsCnZh
alUwQk42M1AwR1BIdFdMVTB0YmRwMWlYYlZtQVN2a1BvY0JnL1lPL2JFQXo3by9nR2JQT0pBQXFDV0VN
TXIKcklqZWszSTI2NzNrRk1reER5U3ZTOXZ0SVRJQjdJZHp3T256Y1haaUpvV2V0Z3l1TVlMU3FyVEVR
RVFzd25hMQpyazQweVNpYjMwZHV6TUZHZUprQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0tr
TUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZLNVY5eGRxUGtCdmp1OVVoaVBTdThl
ZWFlWHFNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdn
RUJBRVk1c2FxOXl4ZTVoU0kwZWFaYQpjY2x4aFFmbFZDYXVhZXlHQlZUeThObHdYMmdHVkV5N1U3VllF
dkU2RHAzamZBVlo4KzlqcTZzb3V1V2EzWlQxCklMbWg5OVIveWhWcm5GekJPWS9EczRuS1o0a3dBeS85
QmowWk1yZTl3VWFIZmp1NEh5SkRQWVltdEZrcWNncmoKdlRxWjJnbTJnYS9pVWhxMzNtUlZuZDlyZEMy
ODBJb0p0WWtOaEd6akFtVFBMakQwaFNBVFppc2lQSjFMOUFjVwpRbVViTVE5L0JFOWIzN084bTB5dVpG
Q0tvcC9SVExXbWt3eUkvSEJTT3ExVDZJUytYdmdNRDFvZ2J5WGVuSi9FCmI3SEtzenpSMFZndzhnQTR3
bjNodzJLc2FZbDFQREtBQk9ncmNlaUlYbVo2WHJ1NWNhOFowTkFOem9OQkNSTWUKNy8wPQotLS0tLUVO
RCBDRVJUSUZJQ0FURS0tLS0tCg==
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null

#查看效果
[root@master1 ~]#kubectl config view --kubeconfig=/root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""

kind: Config
preferences: {}
users: null
```

##### 3.6.3.1.3 生成用户配置kubeconfig文件

范例: v1.24版本之后
```yaml
#获取认证信息
[root@master1 ~]#kubectl get secrets -n kube-system dashboard-admin-secret
NAME                     TYPE                                  DATA   AGE
dashboard-admin-secret   kubernetes.io/service-account-token   3      19s

#方法1，直接查看token
[root@master1 ~]#kubectl describe secrets -n kube-system dashboard-admin-secret
#方法2,需要转码
[root@master1 ~]#kubectl get secrets dashboard-admin-secret -n kube-system -o
jsonpath='{.data.token}' | base64 -d
eyJhbGciOiJSUzI1NiIsImtpZCI6IkZJSXBRS19ESnJUQjlaVXZva3Zrakg4b29Bb0gtRjVkd24ybWtt
UXdFcDAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tc2VjcmV0Iiwia3ViZXJuZXRlcy5pb
y9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRhc2hib2FyZC1hZG1pbiIsImt1Y
mVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjQzMzdjOTg2LTE0Y
jktNDRjYy1iODVmLTQ3ZmFkYzE1ZjJlNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlL
XN5c3RlbTpkYXNoYm9hcmQtYWRtaW4ifQ.I7WJmW-NibXR1yIQ1qIcyp4SBOudbDg7AKZ-
qKj09QZml6P4TNMYq-
nIObxi1kABmFC5ls3u0SfszSucFea6h9brnAjhBrgNH9HXGF3q9KgXW9eEChSKkxycCJh5iqpwYr6pN7
JhugK0_DwLqQ5RUn4rYhl_kMtdYz8mbzWtSIZiEuCl9osx_56sc-FmpOA5oQ-
t9AwiP7hIIXRnQSvXfYY1H0dM9r7l8iFxe-1xpHoalR5b9v3vGQO6hYfheNYEywIZIjqbO9dbRR9s-
Cr1lCy1evX2ObNi8doDFvWRTiTVm5YDEaWZsNKF86_HujlX9dqM9ibrj64m8wRZc6Cp8A

[root@master1 ~]#KUBEADMIN_TOKEN=$(kubectl get secret dashboard-admin-secret -n
kube-system -o jsonpath='{.data.token}' |base64 -d)

#设置用户信息
[root@master1 ~]#kubectl config set-credentials kubeadmin --
token=$KUBEADMIN_TOKEN --kubeconfig=/root/kubeadmin.conf

#检查结果
[root@master1 ~]#cat kubeadmin.conf
apiVersion: v1
clusters:
- cluster:

certificate-authority-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lH
OXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJek1ETXdOekEwTXpB
eE1sb1hEVE16TURNd05EQTBNekF4TWxvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FT
SXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTVFUCmpwNm5wbTVicm5ZQjIxa0Nz
K0N2MkpWa0drdnJ2ZndEVjlsZWR4bkcrQnM5eTVEcFRiNTN2OVQ4bS9TNklqNjQKSHpPZkwyMCtHbzBY
WFBDZWFSVVYybDhUSThWdVJBR2NnRFB6Rko4SDNIbXNxbElRZUYrUzJLaGhqUldlWW9GKwo5ZE5hZ1do
VkQrVVZrdStCdldUcnAxS0hFNEcxRUczdm5LV05NSE9pRi9ibzRSNDBxSTM5cnpvT0tpbmgrenRoCkJR
aytqOUpYU0xxNWc3cmVJU2VEVk5HalZlL0lDZkZwdXhCSkpsSCtHc0pOMlJzQmFuYzg1OVNkOUY3MTFz
SFAKbFUrdG5tME92YkV2Z2xSNitjM2hKaHRwbUFiMFlvcGk1ZnlwQVB2T0x6REEwTk42d3RIcnl6K2J4
MlRESlk0aApmWG9HMTRiQVAwVFpEc0JlMzBFQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0tr
TUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZJOHVzQTBUTFJTMzN0QXI5ek5tZXdz
eTBtSDNNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdn
RUJBREVoeU5ob2ZSRTlQQ3dyUW8zSApxMGd5Mk5hY1RDRXZ6VVhQUWhFazA0NFpNRHdmREswRHM2eXA5
QWo3S0dJbGVwd203SzcxZWN2aTg1aFJ3OUJICkhjRHVDOURVamFLeGVBTnBXc2FXcVNkMWxlWWdBazdI
YlFQRktDTnJ5dmpNZkdsNFZCUHBpRmRYYVlKQXZCdG0KUFRvMUF4dE9iWHJ6SlZKN2ZINzhwOWpoNUov
ekdkOVFuV0I1Und1ZmVoU21JaisvUnJDTWJRRU8vYzczVGUybgo2dUY4Y3ZsK0llaTBRck9GQmFMam5y
ZXR6K2dlV2luNEVNa0h4Um42cmYwNkJiNXFrYVZXVjR6Z0JCVTVkNkFhCkRjeGNoclk1aTZRdUtuTkZQ
bVV5WEVTbGw5QmtVTFFxQjVUK3lyalJqNmRJR3ZITUo4OEJpcTl3bTdrdUhRTlkKRUNZPQotLS0tLUVO
RCBDRVJUSUZJQ0FURS0tLS0tCg==
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6IkZJSXBRS19ESnJUQjlaVXZva3Zrakg4b29Bb0gtRjVkd24ybWtt
UXdFcDAifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tc2VjcmV0Iiwia3ViZXJuZXRlcy5pb
y9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImRhc2hib2FyZC1hZG1pbiIsImt1Y
mVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjQzMzdjOTg2LTE0Y
jktNDRjYy1iODVmLTQ3ZmFkYzE1ZjJlNyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlL
XN5c3RlbTpkYXNoYm9hcmQtYWRtaW4ifQ.I7WJmW-NibXR1yIQ1qIcyp4SBOudbDg7AKZ-
qKj09QZml6P4TNMYq-
nIObxi1kABmFC5ls3u0SfszSucFea6h9brnAjhBrgNH9HXGF3q9KgXW9eEChSKkxycCJh5iqpwYr6pN7
JhugK0_DwLqQ5RUn4rYhl_kMtdYz8mbzWtSIZiEuCl9osx_56sc-FmpOA5oQ-
t9AwiP7hIIXRnQSvXfYY1H0dM9r7l8iFxe-1xpHoalR5b9v3vGQO6hYfheNYEywIZIjqbO9dbRR9s-
Cr1lCy1evX2ObNi8doDFvWRTiTVm5YDEaWZsNKF86_HujlX9dqM9ibrj64m8wRZc6Cp8A

[root@master1 ~]#kubectl config view --kubeconfig=/root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:

token: REDACTED
```

范例: v1.23版之前
```yaml
[root@master1 ~]#kubectl get secrets -n kube-system | grep admin-token
dashboard-admin-token-hqq7x                      kubernetes.io/service-account-
token   3      36h

[root@master1 ~]# kubectl get secrets dashboard-admin-token-hqq7x -n kube-system
-o jsonpath='{.data.token}' | base64 -d
eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qQVBTeTY0VDVfLTNNeE1yVXpuVmEtaGxkWngtdkozSUluY3ZI
cGJpS0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4taHFxN3giLCJrdWJlcm5ld
GVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluI
iwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDA3NGM1Y
2ItY2E3NS00YmYyLTllZmMtNDcyYmVkMzhkZDRlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50O
mt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.dyBCX-uLYqljBHK8kQ0UjtVtuBOHRwmaF-
LWRU9ZIVMssS9n4ybjnYGfHRNPTpgrRu7fnE5I7HJEwFxAWk-EH-
9VqKtBtNf00eMBqZ1P3W2JqDkR5AW5Tc85Wf-
EvO5uawy_KQF6FwrK1u0nRdu4JgYkf_zRG4KZTqXYemWJ8YbMhgQnVk2DknBrytopMkbT5vhdK7RyAY7
B_eYsssuCxBTs7EcDeaYi0VcGE7Sh08Rx4yLnn4MUUwUXXk9Itu4m4cjfsMyurs5M0usHgQcitmG8ADr
5xM2XVhkqO1ycqcbC4WxlSJmIXMCkqThCGzRTGSLjKOSo4VGsKICNqqIR5Q
#注意：是 kube-system 命名空间的认证信息

[root@master1 ~]#KUBEADMIN_TOKEN=$(kubectl get secret dashboard-admin-token-hqq7x
-n kube-system -o jsonpath='{.data.token}' |base64 -d)

#设置用户信息
[root@master1 ~]#kubectl config set-credentials kubeadmin --
token=$KUBEADMIN_TOKEN --kubeconfig=/root/kubeadmin.conf

[root@master1 ~]#ll kubeadmin.conf
-rw------- 1 root root 2647 Apr  3 09:52 kubeadmin.conf

#检查效果
[root@master1 ~]#cat kubeadmin.conf
apiVersion: v1
clusters:
- cluster:

certificate-authority-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lH
OXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeU1ETXlPVEV5TkRB
ME9Wb1hEVE15TURNeU5qRXlOREEwT1Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FT
SXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBS1RBCkZvTGplT3Y2L2xVczZ1dGdH
aFdVV29LNXZkanp4YVkzekhINkFuSjJCVEx0UG5iL2NWdDJGNC9MVjVTY0s4SEYKOXdXYkZVbjBuMVBG
V1d6bi8rS3diRThtZGtZbHNTS09ENG1VdEg5VVN3TlpINnZDTkVBVnBDQ1ovbnRxbnA4dApWVy9xWXdr
T0JIRjY4SDY3aFJETFdVZG9xdDVhbHlXTlQrVjBQQjZLb2NHYnBJUUhXNkI1UGxJVGpkY2xOT3BsCnZh
alUwQk42M1AwR1BIdFdMVTB0YmRwMWlYYlZtQVN2a1BvY0JnL1lPL2JFQXo3by9nR2JQT0pBQXFDV0VN
TXIKcklqZWszSTI2NzNrRk1reER5U3ZTOXZ0SVRJQjdJZHp3T256Y1haaUpvV2V0Z3l1TVlMU3FyVEVR
RVFzd25hMQpyazQweVNpYjMwZHV6TUZHZUprQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0tr
TUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZLNVY5eGRxUGtCdmp1OVVoaVBTdThl
ZWFlWHFNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdn
RUJBRVk1c2FxOXl4ZTVoU0kwZWFaYQpjY2x4aFFmbFZDYXVhZXlHQlZUeThObHdYMmdHVkV5N1U3VllF
dkU2RHAzamZBVlo4KzlqcTZzb3V1V2EzWlQxCklMbWg5OVIveWhWcm5GekJPWS9EczRuS1o0a3dBeS85
QmowWk1yZTl3VWFIZmp1NEh5SkRQWVltdEZrcWNncmoKdlRxWjJnbTJnYS9pVWhxMzNtUlZuZDlyZEMy
ODBJb0p0WWtOaEd6akFtVFBMakQwaFNBVFppc2lQSjFMOUFjVwpRbVViTVE5L0JFOWIzN084bTB5dVpG
Q0tvcC9SVExXbWt3eUkvSEJTT3ExVDZJUytYdmdNRDFvZ2J5WGVuSi9FCmI3SEtzenpSMFZndzhnQTR3
bjNodzJLc2FZbDFQREtBQk9ncmNlaUlYbVo2WHJ1NWNhOFowTkFOem9OQkNSTWUKNy8wPQotLS0tLUVO
RCBDRVJUSUZJQ0FURS0tLS0tCg==
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qQVBTeTY0VDVfLTNNeE1yVXpuVmEtaGxkWngtdkozSUluY3ZI
cGJpS0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4taHFxN3giLCJrdWJlcm5ld
GVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluI
iwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDA3NGM1Y
2ItY2E3NS00YmYyLTllZmMtNDcyYmVkMzhkZDRlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50O
mt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.dyBCX-uLYqljBHK8kQ0UjtVtuBOHRwmaF-
LWRU9ZIVMssS9n4ybjnYGfHRNPTpgrRu7fnE5I7HJEwFxAWk-EH-
9VqKtBtNf00eMBqZ1P3W2JqDkR5AW5Tc85Wf-
EvO5uawy_KQF6FwrK1u0nRdu4JgYkf_zRG4KZTqXYemWJ8YbMhgQnVk2DknBrytopMkbT5vhdK7RyAY7
B_eYsssuCxBTs7EcDeaYi0VcGE7Sh08Rx4yLnn4MUUwUXXk9Itu4m4cjfsMyurs5M0usHgQcitmG8ADr
5xM2XVhkqO1ycqcbC4WxlSJmIXMCkqThCGzRTGSLjKOSo4VGsKICNqqIR5Q

[root@master1 ~]#kubectl config view --kubeconfig=/root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:

token: REDACTED
```

##### 3.6.3.1.4 关联集群和用户的上下文配置kubeconfig文件
```yaml
#设置上下文信息
[root@master1 ~]#kubectl config set-context kubeadmin@kubernetes --
cluster=kubernetes --user=kubeadmin --kubeconfig=/root/kubeadmin.conf

#检查效果
[root@master1 ~]#ll /root/kubeadmin.conf
-rw------- 1 root root 2726 Apr  3 09:56 /root/kubeadmin.conf

[root@master1 ~]#cat /root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lH
OXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJeU1ETXlPVEV5TkRB
ME9Wb1hEVE15TURNeU5qRXlOREEwT1Zvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FT
SXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBS1RBCkZvTGplT3Y2L2xVczZ1dGdH
aFdVV29LNXZkanp4YVkzekhINkFuSjJCVEx0UG5iL2NWdDJGNC9MVjVTY0s4SEYKOXdXYkZVbjBuMVBG
V1d6bi8rS3diRThtZGtZbHNTS09ENG1VdEg5VVN3TlpINnZDTkVBVnBDQ1ovbnRxbnA4dApWVy9xWXdr
T0JIRjY4SDY3aFJETFdVZG9xdDVhbHlXTlQrVjBQQjZLb2NHYnBJUUhXNkI1UGxJVGpkY2xOT3BsCnZh
alUwQk42M1AwR1BIdFdMVTB0YmRwMWlYYlZtQVN2a1BvY0JnL1lPL2JFQXo3by9nR2JQT0pBQXFDV0VN
TXIKcklqZWszSTI2NzNrRk1reER5U3ZTOXZ0SVRJQjdJZHp3T256Y1haaUpvV2V0Z3l1TVlMU3FyVEVR
RVFzd25hMQpyazQweVNpYjMwZHV6TUZHZUprQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0tr
TUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZLNVY5eGRxUGtCdmp1OVVoaVBTdThl
ZWFlWHFNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdn
RUJBRVk1c2FxOXl4ZTVoU0kwZWFaYQpjY2x4aFFmbFZDYXVhZXlHQlZUeThObHdYMmdHVkV5N1U3VllF
dkU2RHAzamZBVlo4KzlqcTZzb3V1V2EzWlQxCklMbWg5OVIveWhWcm5GekJPWS9EczRuS1o0a3dBeS85
QmowWk1yZTl3VWFIZmp1NEh5SkRQWVltdEZrcWNncmoKdlRxWjJnbTJnYS9pVWhxMzNtUlZuZDlyZEMy
ODBJb0p0WWtOaEd6akFtVFBMakQwaFNBVFppc2lQSjFMOUFjVwpRbVViTVE5L0JFOWIzN084bTB5dVpG
Q0tvcC9SVExXbWt3eUkvSEJTT3ExVDZJUytYdmdNRDFvZ2J5WGVuSi9FCmI3SEtzenpSMFZndzhnQTR3
bjNodzJLc2FZbDFQREtBQk9ncmNlaUlYbVo2WHJ1NWNhOFowTkFOem9OQkNSTWUKNy8wPQotLS0tLUVO
RCBDRVJUSUZJQ0FURS0tLS0tCg==
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: kubeadmin
name: kubeadmin@kubernetes
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:

token:
eyJhbGciOiJSUzI1NiIsImtpZCI6Il9qQVBTeTY0VDVfLTNNeE1yVXpuVmEtaGxkWngtdkozSUluY3ZI
cGJpS0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4taHFxN3giLCJrdWJlcm5ld
GVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluI
iwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDA3NGM1Y
2ItY2E3NS00YmYyLTllZmMtNDcyYmVkMzhkZDRlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50O
mt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.dyBCX-uLYqljBHK8kQ0UjtVtuBOHRwmaF-
LWRU9ZIVMssS9n4ybjnYGfHRNPTpgrRu7fnE5I7HJEwFxAWk-EH-
9VqKtBtNf00eMBqZ1P3W2JqDkR5AW5Tc85Wf-
EvO5uawy_KQF6FwrK1u0nRdu4JgYkf_zRG4KZTqXYemWJ8YbMhgQnVk2DknBrytopMkbT5vhdK7RyAY7
B_eYsssuCxBTs7EcDeaYi0VcGE7Sh08Rx4yLnn4MUUwUXXk9Itu4m4cjfsMyurs5M0usHgQcitmG8ADr
5xM2XVhkqO1ycqcbC4WxlSJmIXMCkqThCGzRTGSLjKOSo4VGsKICNqqIR5Q

[root@master1 ~]#kubectl config view --kubeconfig=/root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: kubeadmin
name: kubeadmin@kubernetes
current-context: ""
kind: Config
preferences: {}
users:
- name: kubeadmin
user:
token: REDACTED

#指定默认Context
[root@master1 ~]#kubectl config use-context kubeadmin@kubernetes --
kubeconfig=/root/kubeadmin.conf
Switched to context "kubeadmin@kubernetes".

[root@master1 ~]#kubectl config view --kubeconfig=/root/kubeadmin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: kubeadmin
name: kubeadmin@kubernetes
current-context: kubeadmin@kubernetes
kind: Config
preferences: {}
users:
- name: kubeadmin
user:

token: REDACTED

#确认效果
[root@master1 ~]#kubectl get sa --kubeconfig=/root/kubeadmin.conf
NAME           SECRETS   AGE
def-ns-admin   1         95m
default        1         4d13h
```

##### 3.6.3.1.5 使用文件登录验证
```text
#从服务器下载kubeadmin.conf到登录主机,浏览器上采用kubeconfig方式使用kubeadmin.conf文件登
录，查看效果
```

![原 PDF 第 153 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c90b6a1ccf387341.png)

![原 PDF 第 153 页插图](assets/Kubernetes安全机制_Password_Removed1/img-63dc62caaaa69f47.png)

结果显示：可以看到所有用户空间效果。

##### 3.6.3.1.6 利用现有kubeconfig文件直接登录

系统本身存在kubeconfig文件，可以直接利用此文件登录,但内容不全，需要再添加Token信息才可以。

注意：此文件具体内容和用户身份并不决定登录后的权限，主要和Token关联的SA用户权限有关，即只要有此文件存在并格式正确即可，其内容无所谓。

范例：
```yaml
#创建SA帐号
[root@master1 ~]#kubectl create sa cluster-admin -n kube-system

#1）角色绑定集群管理权限，注意：登录用户的权限由此角色决定，而和kubeconfig文件的用户身份无关
[root@master1 ~]#kubectl create clusterrolebinding dashboard-cluster-admin --
clusterrole cluster-admin --serviceaccount kube-system:cluster-admin

#2）角色绑定集群查看权限
[root@master1 ~]#kubectl create clusterrolebinding dashboard-cluster-admin --
clusterrole view --serviceaccount kube-system:cluster-admin

#创建token
[root@master1 ~]#cat security-dashboard-cluster-admin-secret.yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
name: dashboard-cluster-admin-secret
namespace: kube-system
annotations:
kubernetes.io/service-account.name: "cluster-admin"

[root@master1 ~]#kubectl apply -f yaml/security-dashboard-cluster-admin-
secret.yaml

#查看Token
[root@master1 ~]#kubectl describe secrets  -n kube-system dashboard-cluster-
admin-secret
Name:         dashboard-cluster-admin-secret
Namespace:    kube-system
Labels:       kubernetes.io/legacy-token-last-used=2023-07-23
Annotations:  kubernetes.io/service-account.name: cluster-admin
kubernetes.io/service-account.uid: 287bf5c2-9552-48e9-baf4-
fe44d9ccdb1e

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  11 bytes

token:
eyJhbGciOiJSUzI1NiIsImtpZCI6IjJxV0NPWVNUN0JNcmk3cWNuUjd1MXE3ZC1nT2FoYmtGTGFBYldW
VzVoemsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZ
WFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtY2x1c3Rlci1hZG1pbi1zZWNyZXQiLCJrdWJlc
m5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3Rlci1hZG1pb
iIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjI4N2JmN
WMyLTk1NTItNDhlOS1iYWY0LWZlNDRkOWNjZGIxZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3Vud
DprdWJlLXN5c3RlbTpjbHVzdGVyLWFkbWluIn0.m7eHiHzfeHfQ3nqMh2rOPhZoTYMxLBxAHDzd5hHbX
wilQOHlAOnQJqSk8KMVDCWZaXOLL_VUNHIupIu4pUCTlhO4hby0W5e0X78WOeQ27_1uxQpJLPnovKYmD
zfEMhe0v5ls4het6NRg2z_GFkdUG-thfT2XJAxBqdoMcyLwzk9-
cmDK8aJO1g1zEJ6jgECK4eW58lertrpRnYkiUBLE_baAms1yXrQdY7OIkv4Fk0Sez0EVIqvqtTJFd5Oy
qPMSdTbuVMJpO4IzE39nc-X78OK1VzqaH3EX5CC3EiENzRPs1dWDEhwuNSaxxz5zu-E-
ylHuIlShKQRpu8O1Np0xlw

#利用现有kubeconfig文件
[root@master1 ~]#cp .kube/config /tmp/kubeconfig

[root@master1 ~]#vim /tmp/kubeconfig
.....
client-key-data:
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBb2JiTUlNbCs5MFph
THR1MXk1aytWTUNMQjRuQSt3cUxm
#在最后一行加下面内容
token:
eyJhbGciOiJSUzI1NiIsImtpZCI6IjJxV0NPWVNUN0JNcmk3cWNuUjd1MXE3ZC1nT2FoYmtGTGFBYldW
VzVoemsifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3Nlcn
ZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLX
N5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2
VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtY2x1c3Rlci1hZG1pbi1zZWNyZXQiLCJrdWJlcm5ldGVzLmlvL3
NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2
x1c3Rlci1hZG1pbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Ln
VpZCI6IjI4N2JmNWMyLTk1NTItNDhlOS1iYWY0LWZlNDRkOWNjZG
IxZSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlLXN5c3RlbTpjbHVzdGVyLWFkbWluIn
0.m7eHiHzfeHfQ3nqMh2rOPhZoTYMxLBxAHDzd5hHbXwilQOHlAO
nQJqSk8KMVDCWZaXOLL_VUNHIupIu4pUCTlhO4hby0W5e0X78WOeQ27_1uxQpJLPnovKYmDzfEMhe0v5
ls4het6NRg2z_GFkdUG-thfT2XJAxBqdoMcyLwzk9-cmDK8aJO1g
1zEJ6jgECK4eW58lertrpRnYkiUBLE_baAms1yXrQdY7OIkv4Fk0Sez0EVIqvqtTJFd5OyqPMSdTbuVM
JpO4IzE39nc-X78OK1VzqaH3EX5CC3EiENzRPs1dWDEhwuNSaxxz
5zu-E-ylHuIlShKQRpu8O1Np0xlw

#从服务器下载kubeconfig到登录主机,浏览器上采用kubeconfig方式使用kubeconfig文件登录，查看效
果
```

![原 PDF 第 156 页插图](assets/Kubernetes安全机制_Password_Removed1/img-29cce8d2dcd9eaa5.png)

![原 PDF 第 156 页插图](assets/Kubernetes安全机制_Password_Removed1/img-b84afecdd892f71d.png)

#### 3.6.3.2 用户空间认证

##### 3.6.3.2.1 准备服务账户

参考服务认证中命名空间用户当中的 serviceaccount 创建。
```bash
[root@master1 ~]#kubectl get sa
NAME           SECRETS   AGE
def-ns-admin   1         80m
default        1         4d13h
```

##### 3.6.3.2.2 生成集群配置文件
```yaml
#设置集群信息
[root@master1 ~]#kubectl config set-cluster kubernetes --certificate-
authority=/etc/kubernetes/pki/ca.crt  --server="https://kubeapi.bowen.org:6443" --
embed-certs=true --kubeconfig=/root/def-ns-admin.conf

[root@master1 ~]#ll def-ns-admin.conf
-rw------- 1 root root 1672 Apr  3 10:19 def-ns-admin.conf

[root@master1 ~]#cat def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: LS0tLS1CRUdJTiBDRVJUS
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null

[root@master1 ~]#kubectl config view --kubeconfig=/root/def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users: null
```

##### 3.6.3.2.3  生成用户配置
```yaml
#获取秘钥信息
[root@master1 ~]#kubectl get secret
NAME                       TYPE                                  DATA   AGE
def-ns-admin-token-k2nkb   kubernetes.io/service-account-token   3      117m

[root@master1 ~]#kubectl describe secret def-ns-admin-token-k2nkb
Name:         def-ns-admin-token-k2nkb
Namespace:    default
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: def-ns-admin
kubernetes.io/service-account.uid: df127795-3940-43dd-92ce-
ed7a6cb706d2

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1099 bytes
namespace:  7 bytes
token:      eyJhbGciOiJSU

[root@master1 ~]#DEF_NS_ADMIN_TOKEN=$(kubectl get secret  def-ns-admin-token-
k2nkb  -o jsonpath={.data.token} |base64 -d)

#设置用户信息
[root@master1 ~]#kubectl config set-credentials def-ns-admin --
token=$DEF_NS_ADMIN_TOKEN --kubeconfig=/root/def-ns-admin.conf

[root@master1 ~]#ll def-ns-admin.conf
-rw------- 1 root root 2628 Apr  3 10:22 def-ns-admin.conf

[root@master1 ~]#cat def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: LS0tLS1CRUdJTiBDRVJUS
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: eyJhbGciOiJSUzI1NiIsIm

[root@master1 ~]#kubectl config view --kubeconfig=/root/def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts: null
current-context: ""
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: REDACTED
```

##### 3.6.3.2.4 关联集群和用户的上下文配置
```yaml
#配置上下文信息
[root@master1 ~]#kubectl config set-context def-ns-admin@kubernetes --
cluster=kubernetes --user=def-ns-admin --kubeconfig=/root/def-ns-admin.conf
Context "def-ns-admin@kubernetes" created.
[root@master1 ~]#ll def-ns-admin.conf
-rw------- 1 root root 2713 Apr  3 10:23 def-ns-admin.conf
[root@master1 ~]#cat def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: LS0tLS1CRUdJTiBDR
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:

cluster: kubernetes
user: def-ns-admin
name: def-ns-admin@kubernetes
current-context: ""
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: eyJhbGciOiJSU

[root@master1 ~]#kubectl config view --kubeconfig=/root/def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: def-ns-admin
name: def-ns-admin@kubernetes
current-context: ""
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: REDACTED

#切换用户
[root@master1 ~]#kubectl config use-context def-ns-admin@kubernetes --
kubeconfig=/root/def-ns-admin.conf

[root@master1 ~]#cat def-ns-admin.conf
apiVersion: v1
clusters:
- cluster:
certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: def-ns-admin
name: def-ns-admin@kubernetes
current-context: def-ns-admin@kubernetes
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: eyJhbGciOiJSUzI1NiIs

[root@master1 ~]#kubectl config view --kubeconfig=/root/def-ns-admin.conf
apiVersion: v1

clusters:
- cluster:
certificate-authority-data: DATA+OMITTED
server: https://kubeapi.bowen.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: def-ns-admin
name: def-ns-admin@kubernetes
current-context: def-ns-admin@kubernetes
kind: Config
preferences: {}
users:
- name: def-ns-admin
user:
token: REDACTED

#查看效果
[root@master1 ~]#kubectl get sa --kubeconfig=def-ns-admin.conf
NAME           SECRETS   AGE
def-ns-admin   1         122m
default        1         4d13h

[root@master1 ~]#kubectl get sa   -n kube-system --kubeconfig=def-ns-admin.conf
Error from server (Forbidden): serviceaccounts is forbidden: User
"system:serviceaccount:default:def-ns-admin" cannot list resource
"serviceaccounts" in API group "" in the namespace "kube-system"
```

##### 3.6.3.2.5 使用文件登录验证
```text
#下载def-ns-admin.conf

#浏览器上，采用kubeconfig方式上传def-ns-admin.conf文件，查看效果
#结果显示：当前的dashboard，仅仅能管理default命名空间下的资源
```

![原 PDF 第 160 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3e7ba2801c99a06a.png)

![原 PDF 第 161 页插图](assets/Kubernetes安全机制_Password_Removed1/img-73a2ab0c7932d95c.png)

### 3.6.4 用户名和密码验证
```text
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/README.md#basic
https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
```

范例:
```bash
[root@master1 ~]#vim recommended.yaml
.....
containers:
- name: kubernetes-dashboard
image: kubernetesui/dashboard:v2.7.0
imagePullPolicy: Always
ports:
- containerPort: 8443
protocol: TCP
args:
- --auto-generate-certificates
- --namespace=kubernetes-dashboard
- --authentication-mode=basic,token  #添加下面两行
- --token-ttl=86400
......

[root@master1 ~]#kubectl apply -f recommended.yaml

#浏览器访问
https://dashboard.bowen.org:30000/
```

可以看到下面界面

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c8db1837ce8189a3.png)

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c079c0181746d768.png)

## 3.7 案例：Kuboard

### 3.7.1 Kuboard 介绍

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-4e31d0797583ce01.png)

Kuboard是一款免费的 Kubernetes 图形化管理工具，Kuboard 力图帮助用户快速在 Kubernetes 上落地微服务。为了达到此目标，Kuboard 提供了针对上述问题的解决办法：

Kuboard 提供 Kubernetes 免费安装文档、免费在线答疑，每天约有 200 位网友参照 Kuboard 提供的文档进行 K8S 集群安装。

Kuboard 提供 Kubernetes 免费中文教程、用户无需付费购买视频教程或参加线下培训班，就可参照 Kuboard 提供的免费教程完成 K8S 的学习，更有 QQ 社群可以和网友互相讨论，共同进步。Kuboard 是 Kubernetes 的一款图形化管理工具，使用 Kuboard，用户无需编写 YAML 文件，就可以完成应用程序的部署和管理。Kuboard 提供 Spring Cloud 等微服务参考架构在 K8S 上的详细部署文档和步骤，是 Spring Cloud用户将自己的应用迁移到 K8S 部署环境的非常好的参考资料。

Kuboard 是一款专为 Kubernetes 设计的免费管理界面，兼容 Kubernetes 版本 1.13 及以上。Kuboard每周发布一个 beta 版本，最长每月发布一个正式版本，经过两年的不断迭代和优化，已经具备多集群管理、权限管理、监控套件、日志套件等丰富的功能，并且有 1000+ 的企业将 Kuboard 应用于其生产环境。Kuboard 自 2019年8月发布第一个版本以来，得到了众多用户的认可，目前已经获得了 10000+GitHub Star。

Kuboard v3.x 支持 Kubernetes 多集群管理。如果您从 Kuboard v1.0.x 或者 Kuboard v2.0.x 升级到Kuboard。

官网:  https://kuboard.cn/

**安装说明**


- <https://kuboard.cn/install/v3/install-built-in.html#部署计划>


**在线体验**
```text
https://demo.kuboard.cn
用 户： demo
密 码： demo123
```

![原 PDF 第 163 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6d0e9da06176de59.png)

![原 PDF 第 164 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6290091737174074.png)

安装方法介绍

基于 Docker 安装：官方推荐基于 Kubernetes 集群中安装。

### 3.7.2 基于 Kubernetes 集群中安装

**官方说明**


- <https://kuboard.cn/install/v3/install-in-k8s.html>


#### 3.7.2.1 范例: 无数据持久化安装kuboard
```yaml
[root@master1 ~]#cat kuboard-deploy-v3.yaml
---
apiVersion: v1
kind: Namespace
metadata:
name: kuboard
---
apiVersion: v1
kind: ServiceAccount
metadata:
name: kuboard-boostrap
namespace: kuboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
name: kuboard-boostrap-crb
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: kuboard-boostrap

namespace: kuboard
---
apiVersion: apps/v1
kind: Deployment
metadata:
labels:
k8s.kuboard.cn/name: kuboard-v3
name: kuboard-v3
namespace: kuboard
spec:
replicas: 1
selector:
matchLabels:
k8s.kuboard.cn/name: kuboard-v3
template:
metadata:
labels:
k8s.kuboard.cn/name: kuboard-v3
spec:
containers:
- env:
- name: "KUBOARD_ENDPOINT"
value: "http://kuboard-v3:80"
- name: "KUBOARD_AGENT_SERVER_TCP_PORT"
value: "10081"
#image: eipwork/kuboard:v3.5.2.4
#image: eipwork/kuboard:v3
#image: registry.cn-beijing.aliyuncs.com/bowen/kuboard:v3.5.2.4
image: swr.cn-east-2.myhuaweicloud.com/kuboard/kuboard:v3
volumeMounts:
- name: kuboard-data
mountPath: /data
readOnly: false
imagePullPolicy: Always
livenessProbe:
failureThreshold: 3
httpGet:
path: /
port: 80
scheme: HTTP
initialDelaySeconds: 30
periodSeconds: 10
successThreshold: 1
timeoutSeconds: 1
name: kuboard
ports:
- containerPort: 80
name: web
protocol: TCP
- containerPort: 443
name: https
protocol: TCP
- containerPort: 10081
name: peer
protocol: TCP
- containerPort: 10081
name: peer-u
protocol: UDP

readinessProbe:
failureThreshold: 3
httpGet:
path: /
port: 80
scheme: HTTP
initialDelaySeconds: 30
periodSeconds: 10
successThreshold: 1
timeoutSeconds: 1
volumes:
- name: kuboard-data
emptyDir: {}
dnsPolicy: ClusterFirst
restartPolicy: Always
serviceAccount: kuboard-boostrap
serviceAccountName: kuboard-boostrap
---
apiVersion: v1
kind: Service
metadata:
labels:
k8s.kuboard.cn/name: kuboard-v3
name: kuboard-v3
namespace: kuboard
spec:
ports:
- name: web
nodePort: 30080
port: 80
protocol: TCP
targetPort: 80
- name: tcp
nodePort: 30081
port: 10081
protocol: TCP
targetPort: 10081
- name: udp
nodePort: 30081
port: 10081
protocol: UDP
targetPort: 10081
selector:
k8s.kuboard.cn/name: kuboard-v3
#type: NodePort
type: LoadBalancer #需要提前部署Metallb类似的应用
```
```yaml
[root@master1 ~]#kubectl apply -f kuboard-deploy-v3.yaml
namespace/kuboard created
serviceaccount/kuboard-boostrap created
clusterrolebinding.rbac.authorization.k8s.io/kuboard-boostrap-crb created
deployment.apps/kuboard-v3 created
service/kuboard-v3 created

#查看是否安装
[root@master1 ~]#kubectl get pods -n kuboard
NAME                          READY   STATUS    RESTARTS   AGE
kuboard-v3-664cc56698-r4fp7   0/1     Running   0          62s

[root@master1 ~]#kubectl get svc -n kuboard
NAME         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
AGE
kuboard-v3   NodePort   10.105.202.30   <none>
80:30080/TCP,10081:30081/TCP,10081:30081/UDP   93s

#(可选)如果想通过ingress暴Kuboard露，可以执行下面操作，注意：需要提前部署ingress-nginx
[root@master1 ~]#cat ingress-kuboard.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
name: kuboard
namespace: kuboard
spec:
ingressClassName: nginx
rules:
- host: kuboard.bowen.org
http:
paths:
- path: /
backend:
service:
name: kuboard-v3
port:
number: 80
pathType: Prefix

[root@master1 ~]#kubectl apply -f ingress-kuboard.yaml
```

安装后访问 Kuboard

在浏览器中打开链接 http://your-node-ip-address:30080

输入初始用户名和密码，并登录

用户名： admin密码： Kuboard123

#### 3.7.2.2 范例：支持Storage Class 持久化安装kuboard
```yaml
#https://kuboard.cn/install/v3/install-in-k8s.html#%E6%96%B9%E6%B3%95%E4%BA%8C-%E4%BD%BF%E7%94%A8-storageclass-%E6%8F%90%E4%BE%9B%E6%8C%81%E4%B9%85%E5%8C%96

#环境准备，提前准备一个名称为sc-nfs的storageClass
[root@master1 ~]#kubectl get sc
NAME     PROVISIONER                                   RECLAIMPOLICY
VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
sc-nfs   k8s-sigs.io/nfs-subdir-external-provisioner   Delete          Immediate
false                  43d

#注意:官方yaml文件有bug,需要修改
[root@master1 ~]#curl -o kuboard-v3.yaml
https://addons.kuboard.cn/kuboard/kuboard-v3-storage-class.yaml

[root@master1 ~]#vim kuboard-v3.yaml
```

```yaml
---

apiVersion: v1
kind: Namespace
metadata:
name: kuboard
```

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
name: kuboard-v3-config
namespace: kuboard
data:
# 关于如下参数的解释，请参考文档 https://kuboard.cn/install/v3/install-built-in.html
# [common]
#KUBOARD_ENDPOINT: 'http://your-node-ip-address:30080' #注释此行
KUBOARD_ENDPOINT: 'http://kuboard.bowen.org'  #添加此行
KUBOARD_AGENT_SERVER_UDP_PORT: '30081'
KUBOARD_AGENT_SERVER_TCP_PORT: '30081'
KUBOARD_SERVER_LOGRUS_LEVEL: info  # error / debug / trace
# KUBOARD_AGENT_KEY是Agent与Kuboard通信时的密钥，请修改为一个任意的包含字母、数字的32位
字符串，此密钥变更后，需要删除 Kuboard Agent重新导入。
KUBOARD_AGENT_KEY: 32b7d6572c6255211b4eec9009e4a816

# 关于如下参数的解释，请参考文档 https://kuboard.cn/install/v3/install-gitlab.html
# [gitlab login]
# KUBOARD_LOGIN_TYPE: "gitlab"
# KUBOARD_ROOT_USER: "your-user-name-in-gitlab"
# GITLAB_BASE_URL: "http://gitlab.mycompany.com"
# GITLAB_APPLICATION_ID:
"7c10882aa46810a0402d17c66103894ac5e43d6130b81c17f7f2d8ae182040b5"
# GITLAB_CLIENT_SECRET:
"77c149bd3a4b6870bffa1a1afaf37cba28a1817f4cf518699065f5a8fe958889"

# 关于如下参数的解释，请参考文档 https://kuboard.cn/install/v3/install-github.html
# [github login]
# KUBOARD_LOGIN_TYPE: "github"
# KUBOARD_ROOT_USER: "your-user-name-in-github"
# GITHUB_CLIENT_ID: "17577d45e4de7dad88e0"
# GITHUB_CLIENT_SECRET: "ff738553a8c7e9ad39569c8d02c1d85ec19115a7"

# 关于如下参数的解释，请参考文档 https://kuboard.cn/install/v3/install-ldap.html
# [ldap login]
# KUBOARD_LOGIN_TYPE: "ldap"
# KUBOARD_ROOT_USER: "your-user-name-in-ldap"
# LDAP_HOST: "ldap-ip-address:389"
# LDAP_BIND_DN: "cn=admin,dc=example,dc=org"
# LDAP_BIND_PASSWORD: "admin"
# LDAP_BASE_DN: "dc=example,dc=org"
# LDAP_FILTER: "(objectClass=posixAccount)"
# LDAP_ID_ATTRIBUTE: "uid"
# LDAP_USER_NAME_ATTRIBUTE: "uid"
# LDAP_EMAIL_ATTRIBUTE: "mail"
# LDAP_DISPLAY_NAME_ATTRIBUTE: "cn"
# LDAP_GROUP_SEARCH_BASE_DN: "dc=example,dc=org"
# LDAP_GROUP_SEARCH_FILTER: "(objectClass=posixGroup)"
# LDAP_USER_MACHER_USER_ATTRIBUTE: "gidNumber"
# LDAP_USER_MACHER_GROUP_ATTRIBUTE: "gidNumber"
# LDAP_GROUP_NAME_ATTRIBUTE: "cn"
```

```yaml
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
name: kuboard-etcd
namespace: kuboard
labels:
app: kuboard-etcd
spec:
serviceName: kuboard-etcd
replicas: 3
selector:
matchLabels:
app: kuboard-etcd
template:
metadata:
name: kuboard-etcd
labels:
app: kuboard-etcd
spec:
containers:
- name: kuboard-etcd
image: swr.cn-east-2.myhuaweicloud.com/kuboard/etcd:v3.4.14
ports:
- containerPort: 2379
name: client
- containerPort: 2380
name: peer
env:
- name: KUBOARD_ETCD_ENDPOINTS
value: >-
kuboard-etcd-0.kuboard-etcd:2379,kuboard-etcd-1.kuboard-
etcd:2379,kuboard-etcd-2.kuboard-etcd:2379
volumeMounts:
- name: data
mountPath: /data
command:
- /bin/sh
- -c
- |
PEERS="kuboard-etcd-0=http://kuboard-etcd-0.kuboard-
etcd:2380,kuboard-etcd-1=http://kuboard-etcd-1.kuboard-etcd:2380,kuboard-etcd-
2=http://kuboard-etcd-2.kuboard-etcd:2380"
exec etcd --name ${HOSTNAME} \
--listen-peer-urls http://0.0.0.0:2380 \
--listen-client-urls http://0.0.0.0:2379 \
--advertise-client-urls http://${HOSTNAME}.kuboard-etcd:2379 \
--initial-advertise-peer-urls http://${HOSTNAME}:2380 \
--initial-cluster-token kuboard-etcd-cluster-1 \
--initial-cluster ${PEERS} \
--initial-cluster-state new \
--data-dir /data/kuboard.etcd
volumeClaimTemplates:
- metadata:
name: data
spec:
# 请填写一个有效的 StorageClass name

#storageClassName: please-provide-a-valid-StorageClass-name-here #修改此处
storageClassName: sc-nfs
accessModes: [ "ReadWriteMany" ]
resources:
requests:
storage: 5Gi
```

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
name: kuboard-data-pvc
namespace: kuboard               #注意:官方的bug会导致pod/kuboard-v3-xxx处于
pending状态，需要加此行指定名称空间，
spec:
#storageClassName: please-provide-a-valid-StorageClass-name-here #修改此处
storageClassName: sc-nfs
accessModes:
- ReadWriteOnce
resources:
requests:
storage: 10Gi
```

```yaml
---
apiVersion: v1
kind: Service
metadata:
name: kuboard-etcd
namespace: kuboard
spec:
type: ClusterIP
ports:
- port: 2379
name: client
- port: 2380
name: peer
selector:
app: kuboard-etcd
```

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
annotations:
deployment.kubernetes.io/revision: '9'
k8s.kuboard.cn/ingress: 'false'
k8s.kuboard.cn/service: NodePort
k8s.kuboard.cn/workload: kuboard-v3
labels:
k8s.kuboard.cn/name: kuboard-v3
name: kuboard-v3
namespace: kuboard
spec:
replicas: 1
selector:
matchLabels:
k8s.kuboard.cn/name: kuboard-v3

template:
metadata:
labels:
k8s.kuboard.cn/name: kuboard-v3
spec:
containers:
- env:
- name: KUBOARD_ETCD_ENDPOINTS
value: >-
kuboard-etcd-0.kuboard-etcd:2379,kuboard-etcd-1.kuboard-
etcd:2379,kuboard-etcd-2.kuboard-etcd:2379
envFrom:
- configMapRef:
name: kuboard-v3-config
image: 'swr.cn-east-2.myhuaweicloud.com/kuboard/kuboard:v3'
imagePullPolicy: Always
name: kuboard
volumeMounts:
- mountPath: "/data"
name: kuboard-data
volumes:
- name: kuboard-data
persistentVolumeClaim:
claimName: kuboard-data-pvc
```

```yaml
---
apiVersion: v1
kind: Service
metadata:
annotations:
k8s.kuboard.cn/workload: kuboard-v3
labels:
k8s.kuboard.cn/name: kuboard-v3
name: kuboard-v3
namespace: kuboard
spec:
ports:
- name: webui
nodePort: 30080
port: 80
protocol: TCP
targetPort: 80
- name: agentservertcp
nodePort: 30081
port: 10081
protocol: TCP
targetPort: 10081
- name: agentserverudp
nodePort: 30081
port: 10081
protocol: UDP
targetPort: 10081
selector:
k8s.kuboard.cn/name: kuboard-v3
sessionAffinity: None
type: NodePort
```
```yaml
[root@master1 ~]#kubectl apply -f kuboard-v3-storage-class.yaml

[root@master1 ~]#kubectl get all -n kuboard
NAME                              READY   STATUS    RESTARTS        AGE
pod/kuboard-etcd-0                1/1     Running   1 (2m12s ago)   14m
pod/kuboard-etcd-1                1/1     Running   0               12m
pod/kuboard-etcd-2                1/1     Running   0               10m
pod/kuboard-v3-6df7c85ff5-bd2gf   1/1     Running   1 (2m2s ago)    14m

NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)
AGE
service/kuboard-etcd   ClusterIP   10.100.145.165   <none>
2379/TCP,2380/TCP                              14m
service/kuboard-v3     NodePort    10.105.198.193   <none>
80:30080/TCP,10081:30081/TCP,10081:30081/UDP   14m

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kuboard-v3   1/1     1            1           14m

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/kuboard-v3-6df7c85ff5   1         1         1       14m

NAME                            READY   AGE
statefulset.apps/kuboard-etcd   3/3     14m

[root@master1 ~]#kubectl get pvc,pv -n kuboard
\NAME                                        STATUS   VOLUME
CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/data-kuboard-etcd-0   Bound    pvc-53313407-33ba-4358-b5c4-
8f2b7e6c2d8d   5Gi        RWX            sc-nfs         22m
persistentvolumeclaim/data-kuboard-etcd-1   Bound    pvc-f2e2ee76-7cbf-4e47-b53c-
156857b33278   5Gi        RWX            sc-nfs         20m
persistentvolumeclaim/data-kuboard-etcd-2   Bound    pvc-fd0df1ef-9cb6-4fa8-842b-
58a1a2eee6b0   5Gi        RWX            sc-nfs         18m
persistentvolumeclaim/kuboard-data-pvc      Bound    pvc-814ebb26-8111-49de-b64d-
74f836291611   10Gi       RWO            sc-nfs         12m

NAME                                                        CAPACITY   ACCESS
MODES   RECLAIM POLICY   STATUS   CLAIM                         STORAGECLASS
REASON   AGE
persistentvolume/pvc-53313407-33ba-4358-b5c4-8f2b7e6c2d8d   5Gi        RWX
Delete           Bound    kuboard/data-kuboard-etcd-0   sc-nfs
22m
persistentvolume/pvc-814ebb26-8111-49de-b64d-74f836291611   10Gi       RWO
Delete           Bound    kuboard/kuboard-data-pvc      sc-nfs
12m
persistentvolume/pvc-f2e2ee76-7cbf-4e47-b53c-156857b33278   5Gi        RWX
Delete           Bound    kuboard/data-kuboard-etcd-1   sc-nfs
20m
persistentvolume/pvc-fd0df1ef-9cb6-4fa8-842b-58a1a2eee6b0   5Gi        RWX
Delete           Bound    kuboard/data-kuboard-etcd-2   sc-nfs

#如果想通过ingress暴Kuboard露，可以执行下面操作，注意：需要提前部署ingress-nginx(可选)
[root@master1 ~]#cat ingress-kuboard.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress

metadata:
name: kuboard
namespace: kuboard
spec:
ingressClassName: nginx
rules:
- host: kuboard.bowen.org
http:
paths:
- path: /
backend:
service:
name: kuboard-v3
port:
number: 80
pathType: Prefix

[root@master1 ~]#kubectl apply -f ingress-kuboard.yaml

[root@master1 ~]#kubectl get ingress -n kuboard
NAME      CLASS   HOSTS              ADDRESS     PORTS   AGE
kuboard   nginx   kuboard.bowen.org   10.0.0.11   80      3m14s

#做域名解析
kuboard.bowen.org   10.0.0.11

#安装后访问 Kuboard
#在浏览器中打开链接 `http://kuboard.bowen.org
#输入初始用户名和密码，并登录
#用户名： admin
#密码： Kuboard123 #注意大写的K
```

![原 PDF 第 173 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6d6fb7b91bdad012.png)

![原 PDF 第 174 页插图](assets/Kubernetes安全机制_Password_Removed1/img-dc795ae7655d23a5.png)

### 3.7.3 基于 Docker 安装

#### 3.7.3.1 安装说明

**官方安装**


- <https://kuboard.cn/install/v3/install-built-in.html#部署计划>


基于如下原因，建议您以 docker run 的方式运行 Kuboard：

结构更清晰（Kuboard 作为多个集群的管理界面应该独立于任何集群之外，虽然安装在Kubernetes 集群中的 Kuboard 也可以管理多个集群）登录 Kuboard 时使用不同的认证方式问题排查更简单。

**部署计划**

在正式安装 kuboard v3 之前，需做好一个简单的部署计划的设计，在本例中，各组件之间的连接方式，如下图所示：

假设用户通过 http://外网IP:80 访问 Kuboard v3；安装在 Kubernetes 中的 Kuboard Agent 通过 内网IP 访问 Kuboard 的 Web 服务端口 80 和Kuboard Agent Server 端口 10081。

![原 PDF 第 175 页插图](assets/Kubernetes安全机制_Password_Removed1/img-35b4cb113f4db4cd.png)

安装 Kuboard 之前，假设：

您已经准备好了一个 Linux 服务器用于安装 Kuboard-V3，并且该机器上的 docker 版本不低于19.03您已经有自己的 Kubernetes 集群，并且版本不低于 Kubernetes v1.13。

#### 3.7.3.2 基于 docker 安装实现kubernetes 多个集群管理

安装 Kuboard v3.x 版本的指令如下：
```text
sudo docker run -d \
--restart=unless-stopped \
--name=kuboard \
-p 80:80/tcp \
-p 10081:10081/tcp \
-e KUBOARD_ENDPOINT="http://kuboard内网IP:80" \
-e KUBOARD_AGENT_SERVER_TCP_PORT="10081" \
-v /root/kuboard-data:/data \
--add-host kubeapi.bowen.org:10.0.0.100 #可选，k8s-apiserver的名称解释
swr.cn-east-2.myhuaweicloud.com/kuboard/kuboard:v3
#eipwork/kuboard:v3

# 可以使用镜像 swr.cn-east-2.myhuaweicloud.com/kuboard/kuboard:v3 可以更快地完成镜像
下载。
# 请不要使用 127.0.0.1 或者 localhost 作为内网 IP
# Kuboard 不需要和 K8S 在同一个网段，Kuboard Agent 甚至可以通过代理访问 Kuboard Server
```

WARNING

KUBOARD_ENDPOINT 参数的作用是，让部署到 Kubernetes 中的 kuboard-agent 知道如何访问Kuboard Server KUBOARD_ENDPOINT 中也可以使用外网 IP Kuboard 不需要和 K8S 在同一个网段，Kuboard Agent 甚至可以通过代理访问 Kuboard Server建议在 KUBOARD_ENDPOINT 中使用域名如果使用域名，必须能够通过 DNS 正确解析到该域名，如果直接在宿主机配置 /etc/hosts 文件，将不能正常运行。

**参数解释**

建议将此命令保存为一个 shell 脚本，例如 start-kuboard.sh ，后续升级 Kuboard 或恢复Kuboard 时，需要通过此命令了解到最初安装 Kuboard 时所使用的参数；第 4 行，将 Kuboard Web 端口 80 映射到宿主机的 80 端口（您可以根据自己的情况选择宿主机的其他端口）；第 5 行，将 Kuboard Agent Server 的端口 10081/tcp 映射到宿主机的 10081 端口（您可以根据自己的情况选择宿主机的其他端口）；第 6 行，指定 KUBOARD_ENDPOINT 为 http://kuboard内网IP ，如果后续修改此参数，需将已导入的 Kubernetes 集群从 Kuboard 中删除，再重新导入第 7 行，指定 KUBOARD_AGENT_SERVER 的端口为 10081 ，此参数与第 5 行中的宿主机端口应保持一致，修改此参数不会改变容器内监听的端口 10081 ，例如，如果第 5 行为 -p 30081:10081/tcp 则第 7 行应该修改为 -e KUBOARD_AGENT_SERVER_TCP_PORT="30081" ；第 8 行，将持久化数据 /data 目录映射到宿主机的 /root/kuboard-data 路径，请根据您自己的情况调整宿主机路径；

**其他参数**

在启动命令行中增加环境变量 KUBOARD_ADMIN_DERAULT_PASSWORD ，可以设置 admin 用户的初始默认密码。

在浏览器输入 http://your-host-ip:80 即可访问 Kuboard v3.x 的界面，登录方式：

用户名： admin密 码： Kuboard123

浏览器兼容性

请使用 Chrome / FireFox / Safari 等浏览器

不兼容 IE 以及以 IE 为内核的浏览器。

### 3.7.4 Kuboard 管理kubernetes集群

使用默认用户和密码登录: admin/Kuboard123。

#### 3.7.4.1 版本 kuboard-v3.5.2.7 界面

##### 3.7.4.1.1 基于Token导入集群信息

按提示使用Token方式，执行下面命令。
```yaml
[root@master1 ~]#cat << EOF > kuboard-create-token.yaml
---
apiVersion: v1
kind: Namespace
metadata:
name: kuboard

---
apiVersion: v1
kind: ServiceAccount
metadata:
name: kuboard-admin
namespace: kuboard

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:

name: kuboard-admin-crb
roleRef:
apiGroup: rbac.authorization.k8s.io
kind: ClusterRole
name: cluster-admin
subjects:
- kind: ServiceAccount
name: kuboard-admin
namespace: kuboard

---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
annotations:
kubernetes.io/service-account.name: kuboard-admin
name: kuboard-admin-token
namespace: kuboard
EOF

[root@master1 ~]#kubectl apply -f kuboard-create-token.yaml

#方法1：官方获取Token
[root@master1 ~]#echo -e "\033[1;34m将下面这一行红色输出结果填入到 kuboard 界面的 Token
字段：\033[0m"
将下面这一行红色输出结果填入到 kuboard 界面的 Token 字段：
[root@master1 ~]#echo -e "\033[31m$(kubectl -n kuboard get secret $(kubectl -n
kuboard get secret kuboard-admin-token | grep kuboard-admin-token | awk '{print
$1}') -o go-template='{{.data.token}}' | base64 -d)\033[0m"
eyJhbGciOiJSUzI1NiIsImtpZCI6ImtaNThfX084aTBRZDRENThkcjVwYVFpZDNxcFg5ZUdrU0tMZVBP
YXZoeWMifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZ
XJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJvYXJkIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb
3VudC9zZWNyZXQubmFtZSI6Imt1Ym9hcmQtYWRtaW4tdG9rZW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY
2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoia3Vib2FyZC1hZG1pbiIsImt1YmVybmV0ZXMua
W8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImVjYWRjODdmLTgzZmQtNDdlMS1iM
mVmLTVmNTE1NjcyYWIxMCIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJvYXJkOmt1Ym9hc
mQtYWRtaW4ifQ.IumtYx-jnzI9uJjQsmwDep-Skk8fizD6WkaPuWjGELtGoR-
GinGVfFzmzqlSFnLpqczdQ6aX9mqQygzxkNPg2GLHcrRuesZRxFbelZp6qydF282vHoAz7VXnpOkqkOq
QWKZGaDgwdTZB0VnqIpicaRAVWvyWRpYE1w6CSu9KKGOfS2Vd_bOfteEgH_bkfSUGCkTK-
N0pt2Y3lTR6ML7z38F7otnZLbgyHBm2UFLojMNwF3FGkZMs8_yG5HU0KH8s5_GhRwV0go6QrAH6dwW5j
o9a8z7-rzC6xJSabl-hGSfumfhG-aibnW76gmhMaJAygWZwA3GWhaGqtYIS5218xQ

#方法2：
[root@master1 ~]#kubectl describe  -n kuboard secrets  kuboard-admin-token |awk
'/token:/{print $2}'
```

![原 PDF 第 178 页插图](assets/Kubernetes安全机制_Password_Removed1/img-80bec465ce538d31.png)

![原 PDF 第 178 页插图](assets/Kubernetes安全机制_Password_Removed1/img-2ae0643b6a701241.png)

![原 PDF 第 179 页插图](assets/Kubernetes安全机制_Password_Removed1/img-aaedc7c2564a8584.png)

![原 PDF 第 179 页插图](assets/Kubernetes安全机制_Password_Removed1/img-75fb58c35a97cde6.png)

![原 PDF 第 180 页插图](assets/Kubernetes安全机制_Password_Removed1/img-7fba59faf4912691.png)

##### 3.7.4.1.2 基于Kubeconfig 导入集群信息
```bash
#将下面命令执行结果，复制到kubeconfig的框中
[root@master1 ~]#cat /etc/kubernetes/admin.conf

#注意：如果没有实现api-server的域名解析，还需要修改红色部分的内容

#注意：firefox 浏览器不兼容kuboard，会提示下面错误，可以使用edge或 chrome其它浏览器
```

![原 PDF 第 181 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9da50a94527359ef.png)
```text
#如果没有域名解析，需要修改APIServer地址信息，否则提示下面错误
```

![原 PDF 第 181 页插图](assets/Kubernetes安全机制_Password_Removed1/img-fbb3d91afcda3299.png)

![原 PDF 第 182 页插图](assets/Kubernetes安全机制_Password_Removed1/img-10f23be6b07f033f.png)

![原 PDF 第 182 页插图](assets/Kubernetes安全机制_Password_Removed1/img-741af159714f05b2.png)

![原 PDF 第 183 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9b3b18f6f0538b23.png)

##### 3.7.4.1.3 集群管理
```bash
[root@master1 ~]#kubectl create deployment myapp --image registry.cn-
beijing.aliyuncs.com/bowen/pod-test:v0.1 --replicas 3
```

**对deployment进行伸缩**

![原 PDF 第 183 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c397fc632ce4ab7a.png)

#### 3.7.4.2 版本 kuboard-v3.5.2.4 界面

![原 PDF 第 184 页插图](assets/Kubernetes安全机制_Password_Removed1/img-48df935a9820bc3c.png)

![原 PDF 第 184 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9b2808fea0acdbd2.png)

![原 PDF 第 185 页插图](assets/Kubernetes安全机制_Password_Removed1/img-a8ac038534846e8a.png)

![原 PDF 第 185 页插图](assets/Kubernetes安全机制_Password_Removed1/img-8a0bbc84987a1e9e.png)

**在已有的Kubernetes管理节点执行**
```bash
#将下面命令的执行结果都复制,粘贴到kubeconfig对应的框内
#方法1
[root@master1 ~]#kubectl config view --raw
#方法2
[root@master1 ~]#cat .kube/config
```

![原 PDF 第 186 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c2097bb2263eecbb.png)

![原 PDF 第 186 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9dc769263b8ad62d.png)

![原 PDF 第 187 页插图](assets/Kubernetes安全机制_Password_Removed1/img-2e6f2577269b30bc.png)

![原 PDF 第 187 页插图](assets/Kubernetes安全机制_Password_Removed1/img-885624a1711868af.png)

![原 PDF 第 188 页插图](assets/Kubernetes安全机制_Password_Removed1/img-0fa33bed033eef6f.png)
```bash
[root@master1 ~]#kubectl create deployment myapp --image registry.cn-
beijing.aliyuncs.com/bowen/pod-test:v0.1 --replicas 3
```

![原 PDF 第 188 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c60495e4f126e355.png)

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-0d997599b7b25e3f.png)

**查看日志**

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c999bfe1ecd9ede3.png)

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c4a6c2483f37efff.png)

![原 PDF 第 190 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c8e8a100009e53ae.png)

#### 3.7.4.2 版本 kuboard-v3.5.0.3 界面

![原 PDF 第 190 页插图](assets/Kubernetes安全机制_Password_Removed1/img-45ed19d529d2322f.png)

![原 PDF 第 191 页插图](assets/Kubernetes安全机制_Password_Removed1/img-895ef1e6c0c9140f.png)

![原 PDF 第 191 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c1b8b6636c948832.png)

![原 PDF 第 192 页插图](assets/Kubernetes安全机制_Password_Removed1/img-f896f0e5f979bc3c.png)

**在已有的Kubernetes管理节点执行**
```bash
#将下面命令的执行结果都复制,粘贴到kubeconfig对应的框内
[root@master1 ~]#kubectl config view --raw
[root@master1 ~]#cat .kube/config
```

![原 PDF 第 192 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c4699b2c54df5276.png)

![原 PDF 第 193 页插图](assets/Kubernetes安全机制_Password_Removed1/img-d84374c497f24296.png)

![原 PDF 第 193 页插图](assets/Kubernetes安全机制_Password_Removed1/img-f71496b9c133df5a.png)

![原 PDF 第 194 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c35f56ecfd5f7919.png)

![原 PDF 第 194 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3d634659d9aee565.png)

![原 PDF 第 195 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3ab332d14daeeb63.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/30-security-authentication.html' | relative_url }}">← 上一章：安全体系与身份认证</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/32-security-admission.html' | relative_url }}">下一章：准入控制 →</a>
</nav>
