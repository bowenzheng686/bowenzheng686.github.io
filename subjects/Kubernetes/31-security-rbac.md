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

认证解决“请求者是谁”，RBAC 授权解决“这个身份能对哪些 API 资源执行哪些操作”。API Server 通常以 `Node,RBAC` 组合保护节点组件和用户请求；具体配置可在 kubeadm 的静态 Pod 清单中查看。RBAC 是**只授予、不显式拒绝**的规则系统，多个绑定的权限相加。因此排查 `403 Forbidden` 时要找缺失的动词、资源和作用域，而不是直接赋予 `cluster-admin`。

```bash
sudo grep -- '--authorization-mode=' /etc/kubernetes/manifests/kube-apiserver.yaml
kubectl auth can-i get pods -n default
```

## 31.1 四种对象与三种绑定方式

`Role` 和 `ClusterRole` 定义权限规则；`RoleBinding` 和 `ClusterRoleBinding` 把规则授予 User、Group 或 ServiceAccount。规则可按 `apiGroups`、`resources`、`verbs` 配置；`pods/log`、`pods/exec` 是不同的子资源。非资源 URL 使用 `nonResourceURLs`，不属于 Namespace。

| 角色 | 绑定 | 最终作用域 |
| --- | --- | --- |
| Role | RoleBinding | 绑定所在的一个 Namespace |
| ClusterRole | RoleBinding | 绑定所在的一个 Namespace，复用其中的名称空间级规则 |
| ClusterRole | ClusterRoleBinding | 全集群，包括规则适用的所有 Namespace |

RoleBinding 只能引用同名称空间的 Role，却可以引用其他名称空间的 ServiceAccount 主体，此时必须在 `subjects[].namespace` 中写清来源。ClusterRole 经 RoleBinding 绑定时，不能由此获得节点等集群级资源的权限。若要让同一个用户管理三个 Namespace，可在三个 Namespace 分别创建 RoleBinding，而不是为了省事创建全局 ClusterRoleBinding。

![RBAC 主体与权限关系](assets/Kubernetes安全机制_Password_Removed1/img-9700f85713461321.webp)

![Role 与 RoleBinding 组合示意](assets/Kubernetes安全机制_Password_Removed1/img-e141f68f7ad9ad9b.webp)

![名称空间级 RBAC 关系之一](assets/Kubernetes安全机制_Password_Removed1/img-cb59b65b5faad5c0.webp)

![名称空间级 RBAC 关系之二](assets/Kubernetes安全机制_Password_Removed1/img-453462b139f7ad8d.webp)

![跨名称空间复用 ClusterRole 的示意](assets/Kubernetes安全机制_Password_Removed1/img-d77c3cb30994217e.webp)

## 31.2 给专用 ServiceAccount 授予只读权限

以下清单创建一个 `team-a` 名称空间中的服务账户，只允许它读取该名称空间的 Pod 和 Pod 日志。`get` 读取单个对象，`list` 列表，`watch` 持续观察；若需要 `exec`，还须考虑 `pods/exec` 子资源及其请求动词，不能误把日志读取权限当成执行权限。

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: team-a
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: log-reader
  namespace: team-a
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-log-reader
  namespace: team-a
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods/log"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: log-reader-binding
  namespace: team-a
subjects:
  - kind: ServiceAccount
    name: log-reader
    namespace: team-a
roleRef:
  kind: Role
  name: pod-log-reader
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl apply -f team-a-rbac.yaml
kubectl -n team-a get role,rolebinding,serviceaccount
kubectl auth can-i get pods \
  --as=system:serviceaccount:team-a:log-reader -n team-a
kubectl auth can-i get pods/log \
  --as=system:serviceaccount:team-a:log-reader -n team-a
kubectl auth can-i delete pods \
  --as=system:serviceaccount:team-a:log-reader -n team-a
```

最后一个查询应返回 `no`。`--as` 是管理员常用的模拟检查方式，执行者自身必须获准使用 impersonate；真实应用的访问还应使用该 ServiceAccount 的实际令牌测试。

## 31.3 ClusterRole：复用规则与集群级授权

若多个团队都需要同样的只读规则，可定义一个 ClusterRole，再分别在目标 Namespace 创建 RoleBinding。这样只维护一份规则，却不会把权限扩展到所有 Namespace。只有确实要读取 `nodes`、`namespaces` 等集群级对象，或要跨所有 Namespace 授权时，才考虑 ClusterRoleBinding。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: workload-reader
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: team-readers
  namespace: team-a
subjects:
  - kind: Group
    name: team-a-readers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: workload-reader
  apiGroup: rbac.authorization.k8s.io
```

这里分别为核心组的 `pods/services` 和 `apps` 组的 `deployments` 定义规则，避免把不相关的 API Group 与资源交叉组合。验证时分别测试目标 Namespace 与其他 Namespace。

```bash
kubectl auth can-i list deployments --as=team-user --as-group=team-a-readers -n team-a
kubectl auth can-i list deployments --as=team-user --as-group=team-a-readers -n kube-system
kubectl -n team-a describe rolebinding team-readers
```

内置 `view`、`edit`、`admin`、`cluster-admin` 权限范围不同：`view` 通常不读取 Secret，`edit` 可能读取 Secret 并通过 Pod 间接获取其他凭据；`cluster-admin` 近乎完全控制。不要仅凭角色名称推断细节，使用 `kubectl describe clusterrole NAME` 查看当前集群的实际规则。

## 31.4 Dashboard 与 Kuboard 的权限边界

Dashboard 和 Kuboard 是不同的管理界面，不会替 API Server 绕过 RBAC。原课件记录了多个版本的安装清单、登录截图与端口转发输出；这些界面的 Chart、默认 Service 名和登录机制会随版本变化，应以所选项目的**当前维护文档**为准。部署前先明确谁能访问入口、如何认证、需要哪个 Namespace 的管理权限、是否持久化数据，以及升级/卸载后的保留策略。

- Dashboard：放在独立 Namespace，用项目支持的 Helm Chart 安装；先查询实际 Service 名，再通过本机回环端口转发或受保护的 HTTPS Ingress 访问。不要为了登录界面创建全局 `cluster-admin` 的长期 ServiceAccount Token。
- Kuboard：属于第三方产品，安装方式可能是 Kubernetes 清单、Chart 或容器。核对与当前 Kubernetes 版本的兼容性，控制公开入口和持久化位置；其界面账户与 Kubernetes RBAC 身份之间的映射需单独检查。
- 两者都应使用最小权限的专用身份进行测试。登录成功只证明界面可访问，还需用只读与拒绝写入的实际操作验证 RBAC 生效。

```bash
kubectl get service -A | grep -E 'dashboard|kuboard'
kubectl auth can-i --list -n team-a
kubectl get rolebinding -A
kubectl get clusterrolebinding
```

在 PowerShell 下可将 `grep -E` 换成 `Select-String`。展示管理界面时，不要把真实令牌、管理员密码或 kubeconfig 贴到日志、截图和仓库中。

## 31.5 排错与复核

遇到 `Forbidden`，按“身份 → API Group/资源/子资源 → 动词 → Namespace → Binding → Role 规则”顺序核查。`kubectl auth can-i` 可模拟权限，但对 `resourceNames` 限定的规则，`list/watch` 往往还需要客户端使用 `metadata.name` 字段选择器；`create` 请求事先没有对象名，不能用 `resourceNames` 可靠限制创建。权限改动后再用真实凭据执行一次允许操作和一次应拒绝的操作。

```bash
kubectl -n team-a describe role pod-log-reader
kubectl -n team-a describe rolebinding log-reader-binding
kubectl auth can-i --as=system:serviceaccount:team-a:log-reader \
  get pods/log -n team-a
kubectl auth can-i --as=system:serviceaccount:team-a:log-reader \
  delete pods -n team-a
```

以下原课件截图按原顺序保留作界面/历史案例参考。它们对应的组件版本可能早于当前集群，**以本章文字和所选版本的官方文档为操作依据**；需要查看时再展开，不让大量截图打断主线阅读。

<details markdown="1"><summary>默认角色与进阶 RBAC 原图</summary>

![原 PDF 第 89 页插图](assets/Kubernetes安全机制_Password_Removed1/img-1ad559371717cc6e.webp)

![原 PDF 第 130 页插图](assets/Kubernetes安全机制_Password_Removed1/img-5cb66877a7dd9b62.webp)

</details>

<details markdown="1"><summary>Dashboard 安装与授权原图</summary>

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-d67d320e11eebcac.webp)

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6bc301e8a97ae9b4.webp)

![原 PDF 第 134 页插图](assets/Kubernetes安全机制_Password_Removed1/img-4fbeb97e63cc5316.webp)

![原 PDF 第 143 页插图](assets/Kubernetes安全机制_Password_Removed1/img-aad4813d5b133584.webp)

![原 PDF 第 143 页插图](assets/Kubernetes安全机制_Password_Removed1/img-8e4641a7cb48e73f.webp)

![原 PDF 第 144 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c888df68ca5d8159.webp)

![原 PDF 第 145 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9c6cb0a1452e641c.webp)

![原 PDF 第 153 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c90b6a1ccf387341.webp)

![原 PDF 第 153 页插图](assets/Kubernetes安全机制_Password_Removed1/img-63dc62caaaa69f47.webp)

![原 PDF 第 156 页插图](assets/Kubernetes安全机制_Password_Removed1/img-29cce8d2dcd9eaa5.webp)

![原 PDF 第 156 页插图](assets/Kubernetes安全机制_Password_Removed1/img-b84afecdd892f71d.webp)

![原 PDF 第 160 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3e7ba2801c99a06a.webp)

![原 PDF 第 161 页插图](assets/Kubernetes安全机制_Password_Removed1/img-73a2ab0c7932d95c.webp)

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c8db1837ce8189a3.webp)

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c079c0181746d768.webp)

![原 PDF 第 162 页插图](assets/Kubernetes安全机制_Password_Removed1/img-4e31d0797583ce01.webp)

![原 PDF 第 163 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6d0e9da06176de59.webp)

![原 PDF 第 164 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6290091737174074.webp)

</details>

<details markdown="1"><summary>Kuboard 部署与界面原图</summary>

![原 PDF 第 173 页插图](assets/Kubernetes安全机制_Password_Removed1/img-6d6fb7b91bdad012.webp)

![原 PDF 第 174 页插图](assets/Kubernetes安全机制_Password_Removed1/img-dc795ae7655d23a5.webp)

![原 PDF 第 175 页插图](assets/Kubernetes安全机制_Password_Removed1/img-35b4cb113f4db4cd.webp)

![原 PDF 第 178 页插图](assets/Kubernetes安全机制_Password_Removed1/img-80bec465ce538d31.webp)

![原 PDF 第 178 页插图](assets/Kubernetes安全机制_Password_Removed1/img-2ae0643b6a701241.webp)

![原 PDF 第 179 页插图](assets/Kubernetes安全机制_Password_Removed1/img-aaedc7c2564a8584.webp)

![原 PDF 第 179 页插图](assets/Kubernetes安全机制_Password_Removed1/img-75fb58c35a97cde6.webp)

![原 PDF 第 180 页插图](assets/Kubernetes安全机制_Password_Removed1/img-7fba59faf4912691.webp)

![原 PDF 第 181 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9da50a94527359ef.webp)

![原 PDF 第 181 页插图](assets/Kubernetes安全机制_Password_Removed1/img-fbb3d91afcda3299.webp)

![原 PDF 第 182 页插图](assets/Kubernetes安全机制_Password_Removed1/img-10f23be6b07f033f.webp)

![原 PDF 第 182 页插图](assets/Kubernetes安全机制_Password_Removed1/img-741af159714f05b2.webp)

![原 PDF 第 183 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9b3b18f6f0538b23.webp)

![原 PDF 第 183 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c397fc632ce4ab7a.webp)

![原 PDF 第 184 页插图](assets/Kubernetes安全机制_Password_Removed1/img-48df935a9820bc3c.webp)

![原 PDF 第 184 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9b2808fea0acdbd2.webp)

![原 PDF 第 185 页插图](assets/Kubernetes安全机制_Password_Removed1/img-a8ac038534846e8a.webp)

![原 PDF 第 185 页插图](assets/Kubernetes安全机制_Password_Removed1/img-8a0bbc84987a1e9e.webp)

![原 PDF 第 186 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c2097bb2263eecbb.webp)

![原 PDF 第 186 页插图](assets/Kubernetes安全机制_Password_Removed1/img-9dc769263b8ad62d.webp)

![原 PDF 第 187 页插图](assets/Kubernetes安全机制_Password_Removed1/img-2e6f2577269b30bc.webp)

![原 PDF 第 187 页插图](assets/Kubernetes安全机制_Password_Removed1/img-885624a1711868af.webp)

![原 PDF 第 188 页插图](assets/Kubernetes安全机制_Password_Removed1/img-0fa33bed033eef6f.webp)

![原 PDF 第 188 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c60495e4f126e355.webp)

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-0d997599b7b25e3f.webp)

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c999bfe1ecd9ede3.webp)

![原 PDF 第 189 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c4a6c2483f37efff.webp)

![原 PDF 第 190 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c8e8a100009e53ae.webp)

![原 PDF 第 190 页插图](assets/Kubernetes安全机制_Password_Removed1/img-45ed19d529d2322f.webp)

![原 PDF 第 191 页插图](assets/Kubernetes安全机制_Password_Removed1/img-895ef1e6c0c9140f.webp)

![原 PDF 第 191 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c1b8b6636c948832.webp)

![原 PDF 第 192 页插图](assets/Kubernetes安全机制_Password_Removed1/img-f896f0e5f979bc3c.webp)

![原 PDF 第 192 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c4699b2c54df5276.webp)

![原 PDF 第 193 页插图](assets/Kubernetes安全机制_Password_Removed1/img-d84374c497f24296.webp)

![原 PDF 第 193 页插图](assets/Kubernetes安全机制_Password_Removed1/img-f71496b9c133df5a.webp)

![原 PDF 第 194 页插图](assets/Kubernetes安全机制_Password_Removed1/img-c35f56ecfd5f7919.webp)

![原 PDF 第 194 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3d634659d9aee565.webp)

![原 PDF 第 195 页插图](assets/Kubernetes安全机制_Password_Removed1/img-3ab332d14daeeb63.webp)

</details>

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/30-security-authentication.html' | relative_url }}">← 上一章：安全体系与身份认证</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/32-security-admission.html' | relative_url }}">下一章：准入控制 →</a>
</nav>