---
layout: default
title: 'Kubernetes · 证书续期与故障处理'
subject_page: true
syntax_highlight: true
---

[← 返回 Kubernetes 目录]({{ '/subjects/Kubernetes/' | relative_url }})

{% raw %}

# 35 证书续期与故障处理

# 3 Kubernetes 证书有效期的续期和过期故障解决

## 3.1 Kubernetes 证书机制

Kubernetes 集群中，各个组件间通信需要以安全加密的方式通信, 而证书是保障组件间安全通信的关键基础设施。Kubernetes 是基于 PKI 证书实现基于 TLS 的身份验证和安全通信。

### 3.1.1 Kubernetes 证书分类

```text
https://kubernetes.io/zh-cn/docs/setup/best-practices/certificates/
```

![原 PDF 第 95 页插图](assets/Kubernetes集群维护管理-6fa2a0e84f8d/img-3748bd8e852f89be.png)

Kubernetes集群内部使用双向证书实现双向认证。如果你是使用 kubeadm 安装的 Kubernetes， 则会自动生成集群所需的证书。证书相关文件放在 /etc/kubernetes/pki/ 目录下。

**服务器证书**

API 服务器端点的证书

Server certificate for the API server endpoint

etcd 服务器的服务器证书

Server certificate for the etcd server

每个 kubelet 的服务器证书（每个节点运行一个 kubelet）。

Server certificates for each kubelet (every node runs a kubelet)

可选的前端代理的服务器证书 Optional server certificate for the [front-proxy](

**客户端证书**

针对每个 kubelet 的客户端证书，用于 API 服务器作为 Kubernetes API 的客户端进行身份验证。

Client certificates for each kubelet, used to authenticate to the API server as a client of the Kubernetes API

每个 API 服务器的客户端证书，用于向 etcd 进行身份验证。

Client certificate for each API server, used to authenticate to etcd

控制器管理器与 API 服务器进行安全通信的客户端证书

Client certificate for the controller manager to securely communicate with the API server

调度程序与 API 服务器进行安全通信的客户端证书

Client certificate for the scheduler to securely communicate with the API server

客户端证书（每个节点一个），用于 kube-proxy 向 API 服务器进行身份验证。

Client certificates, one for each node, for kube-proxy to authenticate to the API server

集群管理员向 API 服务器进行身份验证的可选客户端证书

Optional client certificates for administrators of the cluster to authenticate to the API server

前端代理的可选客户端证书

Optional client certificate for the front-proxy

**kubelet 的服务器和客户端证书**

为了建立安全连接并向 kubelet 进行身份验证，API 服务器需要客户端证书和密钥对。To establish a secure connection and authenticate itself to the kubelet, the API Server requires a client certificate and key pair.

在此场景中，证书的使用有两种方法：

**共享证书**：kube-apiserver 可以使用与验证其客户端相同的证书和密钥对。 这意味着现有证书（例如 apiserver.crt 和 apiserver.key ）可用于与 kubelet 服务器进行通信。

Shared Certificates: The kube-apiserver can utilize the same certificate and key pair it uses to authenticate its clients. This means that the existing certificates, such as apiserver.crt and apiserver.key , can be used for communicating with the kubelet servers.

**单独的证书**：或者，kube-apiserver 可以生成新的客户端证书和密钥对，以验证其与 kubelet 服务器的通信。 在这种情况下，将创建一个名为 kubelet-client.crt 的不同证书及其对应的私钥kubelet-client.key 。

Separate Certificates: Alternatively, the kube-apiserver can generate a new client certificate and key pair to authenticate its communication with the kubelet servers. In this case, a distinct certificate named kubelet-client.crt and its corresponding private key, kubelet-client.key are created.

### 3.1.2 根 CA

对于一个kubernetes集群，它依赖三个CA颁发的所有相关的证书。

![原 PDF 第 96 页插图](assets/Kubernetes集群维护管理-6fa2a0e84f8d/img-3de89ecdef3c6fd2.png)

路径默认 CN描述

Kubernetes 通用 CAETCD 集群的根证书Kubernetes 集群的根证书，用于签署 API Server、

ca.crt、key kubernetes-ca

kubelet 等核心组件的证书。所有组件默认信任此 CA，是集群信任体系的基础。基于kubeadm安装的有效期默认10年。与 etcd 相关的所有功能用于签署其他 ETCD 组件证书（如 server、peer、client证书）。

etcd/ca.crt、key etcd-ca

客户端（如 API Server）和 ETCD 节点之间通过此 CA 验证对方证书的有效性，建立信任链。基于kubeadm安装的有效期默认10年。用于前端代理前端代理（如 Ingress Controller）的根证书。

front-proxy-

kubernetes-

用于验证客户端证书（如front-proxy-client.crt ），

ca.crt、key

front-proxy-ca

确保代理通信的安全性基于kubeadm安装的有效期默认10年。

范例:

```text
[root@master1 ~]#openssl x509 -in /etc/kubernetes/pki/ca.crt -text -noout  |head
```

```text
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 5233378791977057484 (0x48a0b2489edafccc)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN = kubernetes
Validity
Not Before: May 22 01:27:53 2025 GMT
Not After : Apr  4 01:32:53 2225 GMT
Subject: CN = kubernetes
```

```text
[root@master1 ~]#openssl x509 -in /etc/kubernetes/pki/front-proxy-ca.crt -text -
noout |head
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 1009344092950537829 (0xe01e91ad474a665)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN = front-proxy-ca
Validity
Not Before: Dec 19 01:00:54 2024 GMT
Not After : Dec 17 01:05:54 2034 GMT
Subject: CN = front-proxy-ca
[root@master1 ~]#openssl x509 -in /etc/kubernetes/pki/etcd/ca.crt -text -noout
|head
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 9189548314639296484 (0x7f87d580fc5d67e4)
Signature Algorithm: sha256WithRSAEncryption
```

```text
Issuer: CN = etcd-ca
Validity
Not Before: Dec 19 01:00:54 2024 GMT
Not After : Dec 17 01:05:54 2034 GMT
Subject: CN = etcd-ca
```

范例: 每个Kubelet 也是一个API Server 对外提供服务,同时也提供自已的 CA

```text
[root@node1 ~]#openssl x509 -in /var/lib/kubelet/pki/kubelet.crt -text |head
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 2 (0x2)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN = node1.wang.org-ca@1678165168
Validity
Not Before: Mar  7 03:59:28 2023 GMT
Not After : Mar  6 03:59:28 2024 GMT
Subject: CN = node1.wang.org@1678165168
```

```text
#10250/tcp是 Kubelet 的主要 API 端口，用于与 Kubernetes API Server 进行通信，接收 Pod
规范并汇报节点和 Pod 的状态等信息，同时也是获取节点资源等操作的接口。
[root@node1 ~]#openssl s_client  -connect 127.0.0.1:10250
CONNECTED(00000003)
Can't use SSL_get_servername
depth=1 CN = node1.wang.org-ca@1734571091
verify error:num=19:self-signed certificate in certificate chain
verify return:1
depth=1 CN = node1.wang.org-ca@1734571091
verify return:1
depth=0 CN = node1.wang.org@1734571091
verify return:1
---
Certificate chain
0 s:CN = node1.wang.org@1734571091
i:CN = node1.wang.org-ca@1734571091
a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
v:NotBefore: Dec 19 00:18:11 2024 GMT; NotAfter: Dec 19 00:18:11 2025 GMT
1 s:CN = node1.wang.org-ca@1734571091
i:CN = node1.wang.org-ca@1734571091
a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
v:NotBefore: Dec 19 00:18:11 2024 GMT; NotAfter: Dec 19 00:18:11 2025 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDPjCCAiagAwIBAgIISu9k23rXp7IwDQYJKoZIhvcNAQELBQAwJzElMCMGA1UE
Awwcbm9kZTEud2FuZy5vcmctY2FAMTczNDU3MTA5MTAeFw0yNDEyMTkwMDE4MTFa
Fw0yNTEyMTkwMDE4MTFaMCQxIjAgBgNVBAMMGW5vZGUxLndhbmcub3JnQDE3MzQ1
NzEwOTEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCj/Cz2hmUMA3ta
Hxpz4Sz/Am0Zc60Nc5NC0JH7boAc05d4b4A+rfmbajkaQY2O7SoHu+f2NSJBYCwI
QPreigxtEeyveEYUhIdv+a02WsPctvCDbWUv92xxvHdXgLNYlzIr0KRcy3fdiQiO
l4z1shY1YQLgsCTgtp2j8XM/mcWn2+/dGGetPlbogmIPTghGstZMCqZhGzf3H7Zy
yTqCa8y06cO7ORZsdWrwZm24CWoMwQruj0sCm9b2PZxOxWGeQIXGyhZPVofs+ebs
dmMMc62pyokgpY2NigJIESzFdFEMSv+YAi9LcHoswHfPLNI1rDot4+t7o4u14QOj
+qUX3A2VAgMBAAGjcTBvMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEF
BQcDATAMBgNVHRMBAf8EAjAAMB8GA1UdIwQYMBaAFI/biWIEexJnO3ZrzmKoJ81o
```

```text
6MO6MBkGA1UdEQQSMBCCDm5vZGUxLndhbmcub3JnMA0GCSqGSIb3DQEBCwUAA4IB
AQBxkH8v4Zoegac7BCmzf4QIHw7qD1In8LlTmVK4zI2m5sh4abCjM/jryZisfgr9
VWOX4j3oGw/2L5sO7ZVxwyR7DEFnieiHFIwMg7T16hRhoCfpjg3yVMAZ6ST/TGgr
eT9l3EhD6Ssm0kSQwMpbB5cv0uQT6/ab5N5reQ3p9cY2uMX31w3w2Ap30u0Q05+Z
l8t80zp2sVnNKc+RNRudU3DTqsPelStKOC6QDiafCTP389fPN7SyXnctu2OegFyQ
GCzv7fct2y1QhXwmjgiA8wbg7MNwUmewdxtu/TDPa8hFOxa7WciDO+bQwfNoeDr6
nDvy9ibKnPSakTaoWc8G0NaJ
-----END CERTIFICATE-----
subject=CN = node1.wang.org@1734571091
issuer=CN = node1.wang.org-ca@1734571091
---
Acceptable client certificate CA names
CN = kubernetes
Requested Signature Algorithms: RSA-PSS+SHA256:ECDSA+SHA256:Ed25519:RSA-
PSS+SHA384:RSA-
PSS+SHA512:RSA+SHA256:RSA+SHA384:RSA+SHA512:ECDSA+SHA384:ECDSA+SHA512:RSA+SHA1:E
CDSA+SHA1
Shared Requested Signature Algorithms: RSA-PSS+SHA256:ECDSA+SHA256:Ed25519:RSA-
PSS+SHA384:RSA-
PSS+SHA512:RSA+SHA256:RSA+SHA384:RSA+SHA512:ECDSA+SHA384:ECDSA+SHA512
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 2267 bytes and written 387 bytes
Verification error: self-signed certificate in certificate chain
---
New, TLSv1.3, Cipher is TLS_AES_128_GCM_SHA256
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 19 (self-signed certificate in certificate chain)
---
---
Post-Handshake New Session Ticket arrived:
SSL-Session:
Protocol  : TLSv1.3
Cipher    : TLS_AES_128_GCM_SHA256
Session-ID: 163F22955FC96D488D5E1A351D4CCB0CEFAFDA7D2E56415698CEC58698AF10CE
Session-ID-ctx:
Resumption PSK:
269A6CEF40C296FFED40BA9D6B749D11B3130E295F71DC3AA25C4652DB97FA11
PSK identity: None
PSK identity hint: None
SRP username: None
TLS session ticket lifetime hint: 604800 (seconds)
TLS session ticket:
0000 - 83 63 8d f5 d3 ca 1c df-bb f2 cf 0d e3 4f 74 62   .c...........Otb
0010 - 03 bf 11 86 f2 97 22 38-b0 b5 73 b3 f4 c7 cc ea   ......"8..s.....
0020 - 42 42 6f ed f7 57 c7 7d-c3 09 c6 9f 29 df 9c 19   BBo..W.}....)...
0030 - a0 29 c4 3a de 94 34 7c-07 75 d6 48 ce 3d 00 dc   .).:..4|.u.H.=..
0040 - 60 0d fc f9 b4 42 38 d0-96 3f 0f 55 19 00 b5 50   `....B8..?.U...P
0050 - 89 02 2a 1c 89 a1 f1 10-d8 64 71 2c 77 77 04 6d   ..*......dq,ww.m
0060 - ef 3e 91 1d ae b4 77 29-dd                        .>....w).
```

```text
Start Time: 1747899000
Timeout   : 7200 (sec)
Verify return code: 19 (self-signed certificate in certificate chain)
Extended master secret: no
Max Early Data: 0
---
read R BLOCK
```

### 3.1.3 API Server 相关证书

API Server 是 Kubernetes 的核心控制平面，依赖多组证书与不同组件通信。除CA证书外,基于kubeadm安装的有效期默认1年。

ca.crt

功能：Kubernetes 集群的根证书，用于签署 API Server、kubelet 等核心组件的证书。作用：所有组件默认信任此 CA，是集群信任体系的基础。

apiserver.crt

功能：API Server 的服务器证书，包含 API Server 的域名或 IP 地址（如kubernetes.default.svc ）。作用：客户端（如 kubectl、kubelet）通过验证此证书确认连接的是合法 API Server。

apiserver-etcd-client.crt

功能：API Server 作为 ETCD 客户端的证书。作用：ETCD 集群通过验证此证书，仅允许授权的 API Server 访问数据存储。

apiserver-kubelet-client.crt

功能：API Server 与 kubelet 通信时使用的客户端证书。作用：kubelet 通过验证此证书，确保请求来自合法的 API Server（例如获取节点状态或执行远程命令）。

### 3.1.4 ETCD 证书

ETCD 是 Kubernetes 的核心数据存储，使用独立的证书体系确保数据安全性。除CA证书外,基于kubeadm安装的有效期默认1年。

ETCD 相关证书在/etc/kubernetes/pki/etcd/ 目录下

ca.crt

功能：ETCD 集群的根证书，用于签署其他 ETCD 组件证书（如 server、peer、client 证书）。作用：客户端（如 API Server）和 ETCD 节点之间通过此 CA 验证对方证书的有效性，建立信任链。

server.crt

功能：ETCD 服务器证书，用于对外提供服务（如接收客户端请求）。作用：客户端（如 API Server）通过验证此证书确认连接的是合法 ETCD 实例。

peer.crt

功能：ETCD 节点间通信的证书（用于集群内部复制和同步）。作用：每个 ETCD 节点使用此证书证明自己的身份，确保节点间通信加密且可信。

healthcheck-client.crt

功能：健康检查客户端证书，用于 kubelet 或监控系统检查 ETCD 健康状态。作用：通过 TLS 验证，确保只有授权组件可以访问 ETCD 的健康检查接口（如/health 端点）。注意：健康检查证书实际没有被使用。

### 3.1.5 前端代理相关证书

除CA证书外,基于kubeadm安装的有效期默认1年。

front-proxy-ca.crt

功能：前端代理（如 Ingress Controller）的根证书。作用：用于验证客户端证书（如front-proxy-client.crt ），确保代理通信的安全性。

front-proxy-client.crt

功能：前端代理客户端证书（如 Ingress Controller 访问 API Server 时使用）。作用：API Server 通过验证此证书，确认请求来自受信任的代理。

### 3.1.6 用户账号配置证书

用户证书基于kubeadm安装的有效期默认1年。

这些文件用途如下：

文件名默认 CN命令说明

admin.conf kubernetes-admin kubectl配置集群的管理员。super-admin.conf kubernetes-super-admin kubectl为集群配置超级管理员用户。

kubelet.conf system:node: <nodeName>kubelet集群中的每个节点都需要一份

kube-

必须添加到 manifests/kube-co

controller-

system:kube-controller-

controller-

manager.conf

manager

manager.yaml 清单中

manager

必须添加到 manifests/kube-

scheduler.conf system:kube-scheduler kube-

scheduler

scheduler.yaml 清单中

下面是前表中所列文件的完整路径。

```text
/etc/kubernetes/admin.conf
/etc/kubernetes/super-admin.conf
/etc/kubernetes/kubelet.conf
/etc/kubernetes/controller-manager.conf
/etc/kubernetes/scheduler.conf
```

kubeadm 在 kubeconfig 文件中生成两个单独的管理员证书。

一个是在 admin.conf 中，带有 Subject: O = kubeadm:cluster-admins, CN = kubernetes-admin 。 kubeadm:cluster-admins 是绑定到 cluster-admin ClusterRole 的自定义组。 这个文件在所有由 kubeadm 管理的控制平面机器上生成。

另一个是在 super-admin.conf 中，具有 Subject: O = system:masters, CN = kubernetes-super-admin 。 这个文件只在调用了 kubeadm init 的节点上生成。system:masters 是一个紧急情况下的超级用户组，可以绕过 Kubernetes 的授权层，如 RBAC。

### 3.1.7 证书工作机制总结

1. 双向 TLS 认证

客户端（如 API Server）和服务器（如 ETCD）互相验证对方证书，确保通信双方身份合法。例如：API Server 访问 ETCD 时，API Server 验证 ETCD 的服务端证书server.crt ，同时ETCD 验证 API Server 的客户端证书。apiserver-etcd-client.crt 。

2. 证书与权限绑定

证书中的Common Name (CN) 和Subject Alternative Name (SAN) 字段会被映射到Kubernetes 的用户和组，作为 RBAC 权限控制的依据。例如：apiserver-kubelet-client.crt 的 CN 可能被映射为system:kube-apiserver ，赋予其访问 kubelet 的权限。

3. 证书有效期

除CA外的证书默认有效期为 1 年（kubeadm 创建的集群），需定期续签（通过kubeadm certs renew 命令），避免因证书过期导致集群中断。

### 3.1.8 查看默认证书的有效期

证书默认有效期

```text
/etc/kubernetes/pki/ca.crt                       #10年有效期
/etc/kubernetes/pki/apiserver.crt                #1年有效期
/etc/kubernetes/pki/apiserver-etcd-client.crt    #1年有效期
/etc/kubernetes/pki/front-proxy-ca.crt           #10年有效期
/etc/kubernetes/pki/front-proxy-client.crt       #1年有效期
/etc/kubernetes/pki/etcd/server.crt              #1年有效期
/etc/kubernetes/pki/etcd/ca.crt                  #10年有效期
/etc/kubernetes/pki/etcd/peer.crt                #1年有效期
/etc/kubernetes/pki/etcd/healthcheck-client.crt  #1年有效期
/etc/kubernetes/pki/apiserver-kubelet-client.crt #1年有效期
```

**查看证书有效期**

```text
kubeadm certs check-expiration
```

```text
#该命令显示 /etc/kubernetes/pki 文件夹中的客户端证书以及 kubeadm（admin.conf、
controller-manager.conf 和 scheduler.conf） 使用的 KUBECONFIG 文件中嵌入的客户端证书的
到期时间/剩余时间。
#另外，kubeadm 会通知用户证书是否由外部管理； 在这种情况下，用户应该小心的手动/使用其他工具来管
理证书更新。
#注意: kubeadm 不能管理由外部 CA 签名的证书
```

范例: 查看证书有效期

```text
[root@k8s-master pki]#pwd
/etc/kubernetes/pki
```

```text
[root@k8s-master pki]#ls -1
apiserver.crt
apiserver-etcd-client.crt
apiserver-etcd-client.key
apiserver.key
apiserver-kubelet-client.crt
apiserver-kubelet-client.key
ca.crt
ca.key
etcd
front-proxy-ca.crt
front-proxy-ca.key
front-proxy-client.crt
front-proxy-client.key
sa.key
sa.pub
[root@k8s-master pki]#ls -1 etcd
ca.crt
ca.key
healthcheck-client.crt
healthcheck-client.key
peer.crt
peer.key
server.crt
server.key
```

```text
[root@k8s-master pki]#ls *.crt
apiserver.crt  apiserver-etcd-client.crt  apiserver-kubelet-client.crt  ca.crt
front-proxy-ca.crt  front-proxy-client.crt
```

```text
#查看证书有效期
[root@k8s-master pki]#openssl x509 -in  /etc/kubernetes/pki/ca.crt  -noout -
dates
notBefore=May 21 03:04:20 2022 GMT
notAfter=May 18 03:04:20 2032 GMT
```

```text
[root@k8s-master pki]#openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -
dates
notBefore=May 21 03:04:20 2022 GMT
notAfter=May 21 03:04:20 2023 GMT
```

```text
[root@k8s-master pki]#openssl x509 -in  /etc/kubernetes/pki/etcd/ca.crt  -noout -
dates
notBefore=May 21 03:04:20 2022 GMT
notAfter=May 18 03:04:20 2032 GMT
[root@k8s-master pki]#openssl x509 -in  /etc/kubernetes/pki/etcd/server.crt  -
noout -dates
notBefore=May 21 03:04:20 2022 GMT
notAfter=May 21 03:04:20 2023 GMT
```

```text
#查看master节点的kubelet证书过期时间
[root@master1 ~]#openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem
-noout -dates
notBefore=May 21 03:04:20 2022 GMT
notAfter=May 21 03:04:20 2023 GMT
```

```text
#查看所有证书有效期
[root@k8s-master ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-
system get cm kubeadm-config -o yaml'
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 May 21, 2023 03:04 UTC   363d
no
apiserver                  May 21, 2023 03:04 UTC   363d            ca
no
apiserver-etcd-client      May 21, 2023 03:04 UTC   363d            etcd-ca
no
apiserver-kubelet-client   May 21, 2023 03:04 UTC   363d            ca
no
controller-manager.conf    May 21, 2023 03:04 UTC   363d
no
etcd-healthcheck-client    May 21, 2023 03:04 UTC   363d            etcd-ca
no
etcd-peer                  May 21, 2023 03:04 UTC   363d            etcd-ca
no
etcd-server                May 21, 2023 03:04 UTC   363d            etcd-ca
no
front-proxy-client         May 21, 2023 03:04 UTC   363d            front-proxy-
ca          no
scheduler.conf             May 21, 2023 03:04 UTC   363d
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      May 18, 2032 03:04 UTC   9y              no
etcd-ca                 May 18, 2032 03:04 UTC   9y              no
front-proxy-ca          May 18, 2032 03:04 UTC   9y              no
```

## 3.2 Kubernetes 未过期的证书如何续期

官方文档:

```text
https://kubernetes.io/zh/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/
```

如果过期会出现下面提示

```text
[root@k8s-master ~]#date -s '1 year';kubectl get nodes
2023年 05月 22日 星期一 11:26:27 CST
Unable to connect to the server: x509: certificate has expired or is not yet
valid: current time 2023-05-22T11:26:27+08:00 is after 2023-05-21T03:04:20Z
```

**更新证书有效期命令**

```text
#查看证书有效期
kubeadm certs check-expiration
```

```text
#更新/etc/kubernetes/pki下面的相关证书文件,并更新对应
/etc/kubernetes/admin.conf,controller-manager.conf,scheduler.conf的kubeconfig文件
kubeadm certs renew all        #签发所有文件的证书
kubeadm certs renew admin.conf #只签发指定文件的证书
#注意: 如果运行了一个多节点高可用集群，这个命令需要在所有控制面板节点上执行。
```

```text
#上面不会签发Kubelet证书，一般也无需手工续期，因为此证书文件具有自动续期功能，在到期前30-120天
会自动触发续期机制
```

```text
#此命令可以自动更新/etc/kubernetes/kubelet.conf
kubeadm init --kubernetes-version=v1.22.2  phase kubeconfig all
```

范例:

```text
#查看证书有效期,发现即将过期
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the "kubeadm-config" ConfigMap in
namespace "kube-system"...
[check-expiration] Use 'kubeadm init phase upload-config --config your-
config.yaml' to re-upload it.
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 19, 2025 01:05 UTC   203d            ca
no
apiserver                  Dec 19, 2025 01:05 UTC   203d            ca
no
apiserver-etcd-client      Dec 19, 2025 01:05 UTC   203d            etcd-ca
no
apiserver-kubelet-client   Dec 19, 2025 01:05 UTC   203d            ca
no
controller-manager.conf    Dec 19, 2025 01:05 UTC   203d            ca
no
etcd-healthcheck-client    Dec 19, 2025 01:05 UTC   203d            etcd-ca
no
etcd-peer                  Dec 19, 2025 01:05 UTC   203d            etcd-ca
no
etcd-server                Dec 19, 2025 01:05 UTC   203d            etcd-ca
no
front-proxy-client         Dec 19, 2025 01:05 UTC   203d            front-proxy-
ca          no
scheduler.conf             Dec 19, 2025 01:05 UTC   203d            ca
no
```

```text
super-admin.conf           Dec 19, 2025 01:05 UTC   203d            ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Dec 17, 2034 01:05 UTC   9y              no
etcd-ca                 Dec 17, 2034 01:05 UTC   9y              no
front-proxy-ca          Dec 17, 2034 01:05 UTC   9y              no
```

```text
[root@master1 ~]#ls -l /etc/kubernetes/
total 44
-rw------- 1 root root 5656 Dec 19 09:06 admin.conf
-rw------- 1 root root 5678 Dec 19 09:06 controller-manager.conf
-rw------- 1 root root 2012 Dec 19 09:06 kubelet.conf
drwxrwxr-x 2 root root 4096 Dec 19 09:06 manifests
drwxr-xr-x 3 root root 4096 Dec 19 09:06 pki
-rw------- 1 root root 5626 Dec 19 09:06 scheduler.conf
-rw------- 1 root root 5680 Dec 19 09:06 super-admin.conf
```

```text
[root@master1 ~]#ls -l /etc/kubernetes/pki/
total 60
-rw-r--r-- 1 root root 1322 Dec 19 09:06 apiserver.crt
-rw-r--r-- 1 root root 1123 Dec 19 09:06 apiserver-etcd-client.crt
-rw------- 1 root root 1675 Dec 19 09:06 apiserver-etcd-client.key
-rw------- 1 root root 1679 Dec 19 09:06 apiserver.key
-rw-r--r-- 1 root root 1176 Dec 19 09:06 apiserver-kubelet-client.crt
-rw------- 1 root root 1675 Dec 19 09:06 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1107 Dec 19 09:06 ca.crt
-rw------- 1 root root 1679 Dec 19 09:06 ca.key
drwxr-xr-x 2 root root 4096 Dec 19 09:06 etcd
-rw-r--r-- 1 root root 1123 Dec 19 09:06 front-proxy-ca.crt
-rw------- 1 root root 1679 Dec 19 09:06 front-proxy-ca.key
-rw-r--r-- 1 root root 1119 Dec 19 09:06 front-proxy-client.crt
-rw------- 1 root root 1675 Dec 19 09:06 front-proxy-client.key
-rw------- 1 root root 1675 Dec 19 09:06 sa.key
-rw------- 1 root root  451 Dec 19 09:06 sa.pub
[root@master1 ~]#ls -l /etc/kubernetes/pki/etcd
total 32
-rw-r--r-- 1 root root 1094 Dec 19 09:06 ca.crt
-rw------- 1 root root 1675 Dec 19 09:06 ca.key
-rw-r--r-- 1 root root 1123 Dec 19 09:06 healthcheck-client.crt
-rw------- 1 root root 1679 Dec 19 09:06 healthcheck-client.key
-rw-r--r-- 1 root root 1220 Dec 19 09:06 peer.crt
-rw------- 1 root root 1679 Dec 19 09:06 peer.key
-rw-r--r-- 1 root root 1220 Dec 19 09:06 server.crt
-rw------- 1 root root 1675 Dec 19 09:06 server.key
```

```text
[root@master1 ~]#ls -l  .kube/config
-rw------- 1 root root 5656 Dec 19 09:06 .kube/config
```

```text
#证书续期
[root@master1 ~]#kubeadm certs renew all
[renew] Reading configuration from the "kubeadm-config" ConfigMap in namespace
"kube-system"...
[renew] Use 'kubeadm init phase upload-config --config your-config.yaml' to re-
upload it.
```

```text
certificate embedded in the kubeconfig file for the admin to use and for kubeadm
itself renewed
certificate for serving the Kubernetes API renewed
certificate the apiserver uses to access etcd renewed
certificate for the API server to connect to kubelet renewed
certificate embedded in the kubeconfig file for the controller manager to use
renewed
certificate for liveness probes to healthcheck etcd renewed
certificate for etcd nodes to communicate with each other renewed
certificate for serving etcd renewed
certificate for the front proxy client renewed
certificate embedded in the kubeconfig file for the scheduler manager to use
renewed
certificate embedded in the kubeconfig file for the super-admin renewed
```

```text
Done renewing certificates. You must restart the kube-apiserver, kube-
controller-manager, kube-scheduler and etcd, so that they can use the new
certificates.
```

```text
#在所有master节点上执行重启相关Pod
[root@master1 ~]#kubectl delete pod -n kube-system -l 'component in (etcd,kube-
apiserver,kube-controller-manager,kube-scheduler)'
[root@master1 ~]#kubectl get pod -n kube-system  -l 'component in (etcd,kube-
apiserver,kube-controller-manager,kube-scheduler)'
NAME                                       READY   STATUS    RESTARTS      AGE
etcd-master1.wang.org                      1/1     Running   1 (94m ago)   18s
kube-apiserver-master1.wang.org            1/1     Running   1 (94m ago)   18s
kube-controller-manager-master1.wang.org   1/1     Running   1 (94m ago)   18s
kube-scheduler-master1.wang.org            1/1     Running   1 (94m ago)   18s
```

```text
#确认证书更新成功
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the "kubeadm-config" ConfigMap in
namespace "kube-system"...
[check-expiration] Use 'kubeadm init phase upload-config --config your-
config.yaml' to re-upload it.
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 May 29, 2026 01:44 UTC   364d            ca
no
apiserver                  May 29, 2026 01:44 UTC   364d            ca
no
apiserver-etcd-client      May 29, 2026 01:44 UTC   364d            etcd-ca
no
apiserver-kubelet-client   May 29, 2026 01:44 UTC   364d            ca
no
controller-manager.conf    May 29, 2026 01:44 UTC   364d            ca
no
etcd-healthcheck-client    May 29, 2026 01:44 UTC   364d            etcd-ca
no
etcd-peer                  May 29, 2026 01:44 UTC   364d            etcd-ca
no
etcd-server                May 29, 2026 01:44 UTC   364d            etcd-ca
no
front-proxy-client         May 29, 2026 01:44 UTC   364d            front-proxy-
ca          no
```

```text
scheduler.conf             May 29, 2026 01:44 UTC   364d            ca
no
super-admin.conf           May 29, 2026 01:44 UTC   364d            ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Dec 17, 2034 01:05 UTC   9y              no
etcd-ca                 Dec 17, 2034 01:05 UTC   9y              no
front-proxy-ca          Dec 17, 2034 01:05 UTC   9y              no
```

```text
[root@master1 ~]#ls -l /etc/kubernetes/
total 44
-rw------- 1 root root 5660 May 29 09:44 admin.conf
-rw------- 1 root root 5674 May 29 09:44 controller-manager.conf
-rw------- 1 root root 2012 Dec 19 09:06 kubelet.conf
drwxrwxr-x 2 root root 4096 Dec 19 09:06 manifests
drwxr-xr-x 3 root root 4096 Dec 19 09:06 pki
-rw------- 1 root root 5626 May 29 09:44 scheduler.conf
-rw------- 1 root root 5680 May 29 09:44 super-admin.conf
[root@master1 ~]#ls -l /etc/kubernetes/pki/
total 60
-rw-r--r-- 1 root root 1322 May 29 09:44 apiserver.crt
-rw-r--r-- 1 root root 1123 May 29 09:44 apiserver-etcd-client.crt
-rw------- 1 root root 1675 May 29 09:44 apiserver-etcd-client.key
-rw------- 1 root root 1679 May 29 09:44 apiserver.key
-rw-r--r-- 1 root root 1176 May 29 09:44 apiserver-kubelet-client.crt
-rw------- 1 root root 1675 May 29 09:44 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1107 Dec 19 09:06 ca.crt
-rw------- 1 root root 1679 Dec 19 09:06 ca.key
drwxr-xr-x 2 root root 4096 Dec 19 09:06 etcd
-rw-r--r-- 1 root root 1123 Dec 19 09:06 front-proxy-ca.crt
-rw------- 1 root root 1679 Dec 19 09:06 front-proxy-ca.key
-rw-r--r-- 1 root root 1119 May 29 09:44 front-proxy-client.crt
-rw------- 1 root root 1679 May 29 09:44 front-proxy-client.key
-rw------- 1 root root 1675 Dec 19 09:06 sa.key
-rw------- 1 root root  451 Dec 19 09:06 sa.pub
```

```text
[root@master1 ~]#ls -l /etc/kubernetes/pki/etcd
total 32
-rw-r--r-- 1 root root 1094 Dec 19 09:06 ca.crt
-rw------- 1 root root 1675 Dec 19 09:06 ca.key
-rw-r--r-- 1 root root 1123 May 29 09:44 healthcheck-client.crt
-rw------- 1 root root 1679 May 29 09:44 healthcheck-client.key
-rw-r--r-- 1 root root 1220 May 29 09:44 peer.crt
-rw------- 1 root root 1679 May 29 09:44 peer.key
-rw-r--r-- 1 root root 1220 May 29 09:44 server.crt
-rw------- 1 root root 1679 May 29 09:44 server.key
```

```text
[root@master1 ~]#ls -l  .kube/config
-rw------- 1 root root 5656 Dec 19 09:06 .kube/config
```

```text
#还需要手动更新授权文件
[root@master1 ~]#cp /etc/kubernetes/admin.conf  .kube/config
```

## 3.3 Kubernetes 证书过期导致集群异常解决方案

上面不会签发Kubelet证书，一般也无需手工续期，因为此证书文件具有自动续期功能，在到期前30-120天会自动触发续期机制。对集群的证书到期时间进行监控，只要确保Kubelet证书大于30天即可，如果小于30天，说明自动续期机制出现问题，需要检查为什么自动续期失败，再手工续期。

范例：基于kubeadm安装默认会自动对Kubelet证书续期

```text
[root@node2 ~]#grep rotateCertificates /var/lib/kubelet/config.yaml
rotateCertificates: true
```

但是如果已经过期,需要手动解决此证书的过期问题。也可以删除此节点,重新加入节点,但此方式不建议。

### 3.3.1 Kubelet 证书说明

```text
https://kubernetes.io/zh-cn/docs/setup/production-
environment/tools/kubeadm/troubleshooting-kubeadm/#kubelet-client-cert
```

默认情况下，kubeadm 使用 /etc/kubernetes/kubelet.conf 中指定的/var/lib/kubelet/pki/kubelet-client-current.pem 符号链接来配置 kubelet 自动轮换客户端证书。如果此轮换过程失败，你可能会在 kube-apiserver 日志中看到诸如 x509: certificate has expired or is not yet valid 之类的错误。要解决此问题，你必须执行以下步骤：

1. 从故障节点备份和删除 /etc/kubernetes/kubelet.conf 和 /var/lib/kubelet/pki/kubelet-client* 。

2. 在集群中具有 /etc/kubernetes/pki/ca.key 的、正常工作的控制平面节点上 执行 kubeadm kubeconfig user --org system:nodes --client-name system:node:$NODE >kubelet.conf 。 $NODE 必须设置为集群中现有故障节点的名称。 手动修改生成的kubelet.conf 以调整集群名称和服务器端点， 或传递 kubeconfig user --config （请参阅为其他用户生成 kubeconfig 文件）。 如果你的集群没有 ca.key ，你必须在外部对 kubelet.conf中的嵌入式证书进行签名。

```text
[root@master1 ~]#kubeadm config print init-defaults > kubeadm-init.yaml
[root@master1 ~]#kubeadm kubeconfig user --org system:nodes --client-name
system:node:master1.wang.org --config kubeadm-init.yaml
```

3. 将得到的 kubelet.conf 文件复制到故障节点上，作为 /etc/kubernetes/kubelet.conf 。

4. 在故障节点上重启 kubelet（systemctl restart kubelet ），等待/var/lib/kubelet/pki/kubelet-client-current.pem 重新创建。

5. 手动编辑 kubelet.conf 指向轮换的 kubelet 客户端证书，方法是将 client-certificate-data和 client-key-data 替换为：

```text
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```

6. 重新启动 kubelet。

7. 确保节点状况变为 Ready

### 3.3.2 范例：证书已经过期的情况，使用下面方法解决

```text
#如果证书过期,出现下面提示错误
[root@master1 ~]#kubectl get nodes
E0416 08:54:51.411777   38932 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": x509:
certificate has expired or is not yet valid: current time 2024-04-
16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
E0416 08:54:51.415062   38932 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": x509:
certificate has expired or is not yet valid: current time 2024-04-
16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
E0416 08:54:51.418866   38932 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": x509:
certificate has expired or is not yet valid: current time 2024-04-
16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
E0416 08:54:51.422846   38932 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": x509:
certificate has expired or is not yet valid: current time 2024-04-
16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
E0416 08:54:51.426610   38932 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": x509:
certificate has expired or is not yet valid: current time 2024-04-
16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
Unable to connect to the server: x509: certificate has expired or is not yet
valid: current time 2024-04-16T08:54:51+08:00 is after 2024-03-06T04:30:12Z
```

```text
#或者重启后出现下面提示
[root@master1 ~]#kubectl get nodes
E0326 10:25:24.884044   42286 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0326 10:25:24.884842   42286 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0326 10:25:24.887876   42286 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0326 10:25:24.889820   42286 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0326 10:25:24.891463   42286 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
The connection to the server kubeapi.wang.org:6443 was refused - did you specify
the right host or port?
```

```text
#发现API Server 端口没有打开
[root@master1 ~]#ss -ntl|grep 6443
```

```text
#查看相关容器
[root@master1 ~]#docker ps -a
CONTAINER ID   IMAGE                                               COMMAND
CREATED             STATUS                      PORTS     NAMES
```

```text
5a6851984c46   63d3239c3c15                                        "kube-
apiserver --ad…"   38 seconds ago      Exited (1) 17 seconds ago
k8s_kube-apiserver_kube-apiserver-master1.wang.org_kube-
system_fda209139dbd4aedcf2e79c2333d7121_390
7fed7b7ee287   fce326961ae2                                        "etcd --
advertise-cl…"   3 minutes ago       Up 3 minutes
k8s_etcd_etcd-master1.wang.org_kube-system_cbdab6d9873f587f7bc39afad444ef28_18
ce8a65e3ed2c   db8f409d9a5d                                        "kube-
scheduler --au…"   3 minutes ago       Up 3 minutes
k8s_kube-scheduler_kube-scheduler-master1.wang.org_kube-
system_c7993324932f5b798845ba77ed5138b2_18
a562c4266b8e   240e201d5b0d                                        "kube-
controller-man…"   3 minutes ago       Up 3 minutes
k8s_kube-controller-manager_kube-controller-manager-master1.wang.org_kube-
system_759c9b699af95705ce07bf1fd74c154a_18
6d8ce649e9b8   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
3 minutes ago       Up 3 minutes
k8s_POD_kube-scheduler-master1.wang.org_kube-
system_c7993324932f5b798845ba77ed5138b2_18
ba2c51fbdb01   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
3 minutes ago       Up 3 minutes
k8s_POD_kube-controller-manager-master1.wang.org_kube-
system_759c9b699af95705ce07bf1fd74c154a_18
c64496b10ee8   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
3 minutes ago       Up 3 minutes
k8s_POD_kube-apiserver-master1.wang.org_kube-
system_fda209139dbd4aedcf2e79c2333d7121_18
56de8805f5c6   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
3 minutes ago       Up 3 minutes
k8s_POD_etcd-master1.wang.org_kube-system_cbdab6d9873f587f7bc39afad444ef28_18
7fdbed942736   fce326961ae2                                        "etcd --
advertise-cl…"   About an hour ago   Exited (0) 3 minutes ago
k8s_etcd_etcd-master1.wang.org_kube-system_cbdab6d9873f587f7bc39afad444ef28_17
8781ac78dc2e   240e201d5b0d                                        "kube-
controller-man…"   About an hour ago   Exited (2) 3 minutes ago
k8s_kube-controller-manager_kube-controller-manager-master1.wang.org_kube-
system_759c9b699af95705ce07bf1fd74c154a_17
99ef3a5c1288   db8f409d9a5d                                        "kube-
scheduler --au…"   About an hour ago   Exited (0) 3 minutes ago
k8s_kube-scheduler_kube-scheduler-master1.wang.org_kube-
system_c7993324932f5b798845ba77ed5138b2_17
14376c3bba3c   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
About an hour ago   Exited (0) 3 minutes ago
k8s_POD_kube-scheduler-master1.wang.org_kube-
system_c7993324932f5b798845ba77ed5138b2_17
05d0ec4b6f3b   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
About an hour ago   Exited (0) 3 minutes ago
k8s_POD_kube-controller-manager-master1.wang.org_kube-
system_759c9b699af95705ce07bf1fd74c154a_17
8c2895e929ff   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
About an hour ago   Exited (0) 3 minutes ago
k8s_POD_etcd-master1.wang.org_kube-system_cbdab6d9873f587f7bc39afad444ef28_17
142e18a16d7a   7b7f3acab868
"/opt/bin/flanneld -…"   4 weeks ago         Exited (255) 2 weeks ago
k8s_kube-flannel_kube-flannel-ds-7z42x_kube-flannel_6d40601c-6c87-4f3b-9edb-
db7d6af637f5_13
```

```text
c7e8486a716b   7b7f3acab868                                        "cp -f
/etc/kube-fla…"   4 weeks ago         Exited (0) 4 weeks ago
k8s_install-cni_kube-flannel-ds-7z42x_kube-flannel_6d40601c-6c87-4f3b-9edb-
db7d6af637f5_0
9c027ae9374d   6f64e7135a6e
"/usr/local/bin/kube…"   4 weeks ago         Exited (255) 2 weeks ago
k8s_kube-proxy_kube-proxy-vbbkc_kube-system_e144597e-dbe7-4836-952f-
7de369e8d3dc_12
7d01fb847451   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
4 weeks ago         Exited (255) 2 weeks ago
k8s_POD_kube-proxy-vbbkc_kube-system_e144597e-dbe7-4836-952f-7de369e8d3dc_12
377ad8e1a73a   7a2dcab94698                                        "cp -f
/flannel /opt…"   4 weeks ago         Exited (0) 4 weeks ago
k8s_install-cni-plugin_kube-flannel-ds-7z42x_kube-flannel_6d40601c-6c87-4f3b-
9edb-db7d6af637f5_12
0661002fd947   registry.aliyuncs.com/google_containers/pause:3.7   "/pause"
4 weeks ago         Exited (255) 2 weeks ago
k8s_POD_kube-flannel-ds-7z42x_kube-flannel_6d40601c-6c87-4f3b-9edb-
db7d6af637f5_12
```

```text
#查看kube-apiserver的容器日志,可以看到证书过期
[root@master1 ~]#docker logs k8s_kube-apiserver_kube-apiserver-
master1.wang.org_kube-system_fda209139dbd4aedcf2e79c2333d7121_390
I0326 01:50:21.890581       1 server.go:555] external host was not specified,
using 10.0.0.200
I0326 01:50:21.891531       1 server.go:163] Version: v1.26.2
I0326 01:50:21.891565       1 server.go:165] "Golang settings" GOGC=""
GOMAXPROCS="" GOTRACEBACK=""
I0326 01:50:22.084438       1 shared_informer.go:273] Waiting for caches to sync
for node_authorizer
I0326 01:50:22.085169       1 plugins.go:158] Loaded 12 mutating admission
controller(s) successfully in the following order:
NamespaceLifecycle,LimitRanger,ServiceAccount,NodeRestriction,TaintNodesByCondit
ion,Priority,DefaultTolerationSeconds,DefaultStorageClass,StorageObjectInUseProt
ection,RuntimeClass,DefaultIngressClass,MutatingAdmissionWebhook.
I0326 01:50:22.085194       1 plugins.go:161] Loaded 12 validating admission
controller(s) successfully in the following order:
LimitRanger,ServiceAccount,PodSecurity,Priority,PersistentVolumeClaimResize,Runt
imeClass,CertificateApproval,CertificateSigning,CertificateSubjectRestriction,Va
lidatingAdmissionPolicy,ValidatingAdmissionWebhook,ResourceQuota.
W0326 01:50:22.089732       1 logging.go:59] [core] [Channel #1 SubChannel #2]
grpc: addrConn.createTransport failed to connect to {
"Addr": "127.0.0.1:2379",
"ServerName": "127.0.0.1",
"Attributes": null,
"BalancerAttributes": null,
"Type": 0,
"Metadata": null
}. Err: connection error: desc = "transport: authentication handshake failed:
x509: certificate has expired or is not yet valid: current time 2024-03-
26T01:50:22Z is after 2024-03-06T04:30:12Z"
W0326 01:50:23.087709       1 logging.go:59] [core] [Channel #4 SubChannel #6]
grpc: addrConn.createTransport failed to connect to {
```

```text
#确认证书有效期已过期
[root@master1 ~]#date
```

```text
Tue Apr 16 09:06:18 AM CST 2024
```

```text
#检查证书有效期
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-
system get cm kubeadm-config -o yaml'
[check-expiration] Error reading configuration from the Cluster. Falling back to
default configuration
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Mar 06, 2024 04:30 UTC   <invalid>       ca
no
apiserver                  Mar 06, 2024 04:30 UTC   <invalid>       ca
no
apiserver-etcd-client      Mar 06, 2024 04:30 UTC   <invalid>       etcd-ca
no
apiserver-kubelet-client   Mar 06, 2024 04:30 UTC   <invalid>       ca
no
controller-manager.conf    Mar 06, 2024 04:30 UTC   <invalid>       ca
no
etcd-healthcheck-client    Mar 06, 2024 04:30 UTC   <invalid>       etcd-ca
no
etcd-peer                  Mar 06, 2024 04:30 UTC   <invalid>       etcd-ca
no
etcd-server                Mar 06, 2024 04:30 UTC   <invalid>       etcd-ca
no
front-proxy-client         Mar 06, 2024 04:30 UTC   <invalid>       front-proxy-
ca          no
scheduler.conf             Mar 06, 2024 04:30 UTC   <invalid>       ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Mar 04, 2033 04:30 UTC   8y              no
etcd-ca                 Mar 04, 2033 04:30 UTC   8y              no
front-proxy-ca          Mar 04, 2033 04:30 UTC   8y              no
```

```text
#查看证书文件的生成时间
[root@master1 ~]#ll /etc/kubernetes/pki
total 68
drwxr-xr-x 3 root root 4096 Mar  4  2023 ./
drwxr-xr-x 5 root root 4096 Jul 22  2023 ../
-rw-r--r-- 1 root root 1322 Mar  4  2023 apiserver.crt
-rw-r--r-- 1 root root 1155 Mar  4  2023 apiserver-etcd-client.crt
-rw------- 1 root root 1675 Mar  4  2023 apiserver-etcd-client.key
-rw------- 1 root root 1675 Mar  4  2023 apiserver.key
-rw-r--r-- 1 root root 1164 Mar  4  2023 apiserver-kubelet-client.crt
-rw------- 1 root root 1679 Mar  4  2023 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1099 Mar  4  2023 ca.crt
-rw------- 1 root root 1679 Mar  4  2023 ca.key
drwxr-xr-x 2 root root 4096 Mar  4  2023 etcd/
-rw-r--r-- 1 root root 1115 Mar  4  2023 front-proxy-ca.crt
-rw------- 1 root root 1679 Mar  4  2023 front-proxy-ca.key
-rw-r--r-- 1 root root 1119 Mar  4  2023 front-proxy-client.crt
-rw------- 1 root root 1679 Mar  4  2023 front-proxy-client.key
-rw------- 1 root root 1679 Mar  4  2023 sa.key
```

```text
-rw------- 1 root root  451 Mar  4  2023 sa.pub
```

```text
#在所有master节点上执行下面操作更新证书有效期
[root@master1 ~]#kubeadm certs renew all
[renew] Reading configuration from the cluster...
[renew] FYI: You can look at this config file with 'kubectl -n kube-system get
cm kubeadm-config -o yaml'
```

```text
certificate embedded in the kubeconfig file for the admin to use and for kubeadm
itself renewed
certificate for serving the Kubernetes API renewed
certificate the apiserver uses to access etcd renewed
certificate for the API server to connect to kubelet renewed
certificate embedded in the kubeconfig file for the controller manager to use
renewed
certificate for liveness probes to healthcheck etcd renewed
certificate for etcd nodes to communicate with each other renewed
certificate for serving etcd renewed
certificate for the front proxy client renewed
certificate embedded in the kubeconfig file for the scheduler manager to use
renewed
```

```text
#提示重启kube-apiserver, kube-controller-manager, kube-scheduler and etcd
Done renewing certificates. You must restart the kube-apiserver, kube-
controller-manager, kube-scheduler and etcd, so that they can use the new
certificates.
```

```text
#确认证书有效期更新
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the cluster...
[check-expiration] FYI: You can look at this config file with 'kubectl -n kube-
system get cm kubeadm-config -o yaml'
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Mar 26, 2025 01:55 UTC   364d            ca
no
apiserver                  Mar 26, 2025 01:55 UTC   364d            ca
no
apiserver-etcd-client      Mar 26, 2025 01:55 UTC   364d            etcd-ca
no
apiserver-kubelet-client   Mar 26, 2025 01:55 UTC   364d            ca
no
controller-manager.conf    Mar 26, 2025 01:55 UTC   364d            ca
no
etcd-healthcheck-client    Mar 26, 2025 01:55 UTC   364d            etcd-ca
no
etcd-peer                  Mar 26, 2025 01:55 UTC   364d            etcd-ca
no
etcd-server                Mar 26, 2025 01:55 UTC   364d            etcd-ca
no
front-proxy-client         Mar 26, 2025 01:55 UTC   364d            front-proxy-
ca          no
scheduler.conf             Mar 26, 2025 01:55 UTC   364d            ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Mar 04, 2033 04:30 UTC   8y              no
etcd-ca                 Mar 04, 2033 04:30 UTC   8y              no
front-proxy-ca          Mar 04, 2033 04:30 UTC   8y              no
```

```text
#自动更新证书文件内容和时间
[root@master1 ~]#ll /etc/kubernetes/pki/
总计 68
drwxr-xr-x 3 root root 4096  3月  7  2023 ./
drwxr-xr-x 4 root root 4096  3月  7  2023 ../
-rw-r--r-- 1 root root 1322  3月 26 09:55 apiserver.crt
-rw-r--r-- 1 root root 1155  3月 26 09:55 apiserver-etcd-client.crt
-rw------- 1 root root 1679  3月 26 09:55 apiserver-etcd-client.key
-rw------- 1 root root 1675  3月 26 09:55 apiserver.key
-rw-r--r-- 1 root root 1164  3月 26 09:55 apiserver-kubelet-client.crt
-rw------- 1 root root 1679  3月 26 09:55 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1099  3月  7  2023 ca.crt
-rw------- 1 root root 1675  3月  7  2023 ca.key
drwxr-xr-x 2 root root 4096  3月  7  2023 etcd/
-rw-r--r-- 1 root root 1115  3月  7  2023 front-proxy-ca.crt
-rw------- 1 root root 1679  3月  7  2023 front-proxy-ca.key
-rw-r--r-- 1 root root 1119  3月 26 09:55 front-proxy-client.crt
-rw------- 1 root root 1679  3月 26 09:55 front-proxy-client.key
-rw------- 1 root root 1679  3月  7  2023 sa.key
-rw------- 1 root root  451  3月  7  2023 sa.pub
```

```text
#发现只有kubelet.conf文件没有更新
[root@master1 ~]#ll /etc/kubernetes/*.conf
-rw-r--r-- 1 root root 1322  3月 26 09:55 /etc/kubernetes/admin.conf
-rw-r--r-- 1 root root 1322  3月 26 09:55 /etc/kubernetes/controller-manager.conf
-rw------- 1 root root 2004  3月  7  2023 /etc/kubernetes/kubelet.conf
-rw-r--r-- 1 root root 1322  3月 26 09:55 /etc/kubernetes/scheduler.conf
```

```text
#kubeconfig文件也自动更新
[root@master1 ~]#ll /etc/kubernetes/admin.conf
-rw------- 1 root root 5644  3月 26 09:55 /etc/kubernetes/admin.conf
```

```text
#所有Master节点上的kubeconfig文件也需要更新
[root@k8s-master ~]#ll  /etc/kubernetes/admin.conf $HOME/.kube/config
-rw------- 1 root root 5644  3月 26 09:55 /etc/kubernetes/admin.conf
-rw------- 1 root root 5644  3月  7  2023 /root/.kube/config
```

```text
#更新和覆盖kubeconfig文件
[root@master1 ~]#cp  /etc/kubernetes/admin.conf $HOME/.kube/config
```

```text
#确认
[root@master1 ~]#ll !*
ll /etc/kubernetes/admin.conf $HOME/.kube/config
-rw------- 1 root root 5644  3月 26 09:55 /etc/kubernetes/admin.conf
-rw------- 1 root root 5644  3月 26 09:55 /root/.kube/config
```

```text
#在所有master节点上执行仍然失败
[root@master1 ~]#kubectl delete pod -n kube-system -l 'component in (etcd,kube-
apiserver,kube-controller-manager,kube-scheduler)'
```

```text
[root@master1 ~]#kubectl get pod -n kube-system | awk '/^(kube-apiserver|kube-
controller-manager|kube-scheduler|etcd)/{print $1}'|xargs kubectl -n kube-system
delete pod --force --grace-period=0
```

```text
#因为Kubelet 客户端证书轮换失败导致仍然失败
[root@master1 ~]#kubectl get nodes
E0416 09:14:25.408132    2404 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0416 09:14:25.408934    2404 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0416 09:14:25.410427    2404 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0416 09:14:25.413151    2404 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
E0416 09:14:25.415127    2404 memcache.go:238] couldn't get current server API
group list: Get "https://kubeapi.wang.org:6443/api?timeout=32s": dial tcp
10.0.0.200:6443: connect: connection refused
The connection to the server kubeapi.wang.org:6443 was refused - did you specify
the right host or port?
```

```text
#查看服务无法启动
[root@master1 ~]#systemctl status kubelet.service
● kubelet.service - kubelet: The Kubernetes Node Agent
Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset:
enabled)
Drop-In: /etc/systemd/system/kubelet.service.d
└─10-kubeadm.conf
Active: activating (auto-restart) (Result: exit-code) since Sun 2024-03-31
10:13:26 CST; 9s ago
Docs: https://kubernetes.io/docs/home/
Process: 2211 ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS
$KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARG>
Main PID: 2211 (code=exited, status=1/FAILURE)
CPU: 55ms
```

```text
3月 31 10:13:26 master1.wang.org systemd[1]: kubelet.service: Main process
exited, code=exited, status=1/FAILURE
3月 31 10:13:26 master1.wang.org systemd[1]: kubelet.service: Failed with result
'exit-code'.
```

```text
#查看日志，提示证书过期
[root@master1 ~]#journalctl -u kubelet.service |grep  expired
3月 31 10:01:29 master1.wang.org kubelet[2024]: E0331 10:01:29.662259    2024
bootstrap.go:265] part of the existing bootstrap client certificate in
/etc/kubernetes/kubelet.conf is expired: 2024-03-03 15:36:25 +0000 UTC
```

```text
[root@master1 ~]#cat /etc/kubernetes/kubelet.conf
apiVersion: v1
clusters:
- cluster:
```

```text
certificate-authority-data:
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
server: https://kubeapi.wang.org:6443
name: kubernetes
contexts:
- context:
cluster: kubernetes
user: system:node:master1.wang.org
name: system:node:master1.wang.org@kubernetes
current-context: system:node:master1.wang.org@kubernetes
kind: Config
preferences: {}
users:
- name: system:node:master1.wang.org
user:
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```

```text
#查看证书没有更新
[root@master1 ~]#ll /var/lib/kubelet/pki/
总计 20
drwxr-xr-x 2 root root 4096  3月  4  2023 ./
drwx------ 8 root root 4096  3月  4  2023 ../
-rw------- 1 root root 2834  3月  4  2023 kubelet-client-2023-03-04-23-36-26.pem
lrwxrwxrwx 1 root root   59  3月  4  2023 kubelet-client-current.pem ->
/var/lib/kubelet/pki/kubelet-client-2023-03-04-23-36-26.pem
-rw-r--r-- 1 root root 2307  3月  4  2023 kubelet.crt
-rw------- 1 root root 1675  3月  4  2023 kubelet.key
```

```text
#文件中保存证书和key
[root@master1 ~]#cat /var/lib/kubelet/pki/kubelet-client-current.pem
-----BEGIN CERTIFICATE-----
MIIDKzCCAhOgAwIBAgIIXRpdhWJnjdgwDQYJKoZIhvcNAQELBQAwFTETMBEGA1UE
AxMKa3ViZXJuZXRlczAeFw0yMzAzMDcwNDMwMTJaFw0yNDAzMDYwNDMwMTNaMD4x
FTATBgNVBAoTDHN5c3RlbTpub2RlczElMCMGA1UEAxMcc3lzdGVtOm5vZGU6bWFz
dGVyMS53YW5nLm9yZzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJuz
X3zg87xNUnTG7SkhK1Avm5bXpzqHHCRVp5hjNrsipLYBtj7fVaD4Vr4BcFWpT99l
OwNIcFV4wmEqcmUpyEUWW2uj5tNDYE576KBl2p5xdVcdvh3AWxNqoffOn/v9yCKX
cXr4Dg+cnSyiIf/4bo3Ww04Khbzy657dLs7Tidngp5tAWcAbBTFuFwTz8tcRcut6
LKKsXv+dWARMCGdxW9bdqLk3ArLvOC8H5rtAO/d8kHlPtjyWHbhnUrHHlGNDJh7y
```

```text
fbBGf7BCEtWPJ7kOeeC1UBUpQi3/YRai/dY6At8UmSMOdeiozxrgUpRXozVvrTnt
u3G/cVc5dNrI9HpmJcsCAwEAAaNWMFQwDgYDVR0PAQH/BAQDAgWgMBMGA1UdJQQM
MAoGCCsGAQUFBwMCMAwGA1UdEwEB/wQCMAAwHwYDVR0jBBgwFoAUjy6wDRMtFLfe
0Cv3M2Z7CzLSYfcwDQYJKoZIhvcNAQELBQADggEBAKPlO4H11WxV4YGZnJo7XL3t
9tKl0JhOQwlWpTrwGSoeLKsBXHA2/ZVWZn6HcsFEIVsUtdAb8qzItggU4X91KHaY
ZapRPfexzSR8PoNDH6Rw6uK7w48v9uy2QxCARyWM3/CFJL0UPaVuC4mHSRDeUMq0
+SRKe5Z/UI+akQ+ysBDA+9QoF16bdzRlxKVAMO6ki+WScHSKU+PsmOz5IAK2DsBu
om0GFeRVKjkXy10HbkY2RdwXQhnUuC3SHNk4I6ymD+2hRjofoRUx9zBTgS0heAwY
kLAclbXx3i+QxCh2ve1qUMQKtlzq76+IQLnJoxzWrY66tY2Agke6qOH4R59bvFY=
-----END CERTIFICATE-----
-----BEGIN RSA PRIVATE KEY-----
<REDACTED_PRIVATE_KEY>
-----END RSA PRIVATE KEY-----
```

```text
[root@master1 ~]#openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem
-noout -text
Certificate:
Data:
Version: 3 (0x2)
Serial Number: 6708777422384762328 (0x5d1a5d8562678dd8)
Signature Algorithm: sha256WithRSAEncryption
Issuer: CN = kubernetes
Validity
Not Before: Mar  7 04:30:12 2023 GMT
Not After : Mar  6 04:30:13 2024 GMT
Subject: O = system:nodes, CN = system:node:master1.wang.org
```

```text
[root@master1 ~]#openssl x509 -in /var/lib/kubelet/pki/kubelet-client-current.pem
-noout -dates
notBefore=Mar  7 04:30:12 2023 GMT
notAfter=Mar  6 04:30:13 2024 GMT
```

```text
#更新kubelet的客户端证书
```

```text
#方法1：
#生成初始化文件
[root@master1 ~]#cp /etc/kubernetes/kubelet.conf{,.bak}
#基于上面文件对应节点的生成证书信息
#方法1
[root@master1 ~]#kubeadm kubeconfig user --org system:nodes --client-name
system:node:master1.wang.org > /etc/kubernetes/kubelet.conf
```

```text
#方法2：
[root@master1 ~]#kubeadm kubeconfig user --org system:nodes --client-name
system:node:master1.wang.org | tail -n 3 >> /etc/kubernetes/kubelet.conf
[root@master1 ~]#vim /etc/kubernetes/kubelet.conf
users:
- name: system:node:master1.wang.org
user: 将下面两行注释或删除
#client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
#client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
client-certificate-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLekNDQWhPZ0F3SUJBZ0l.....
client-key-data:
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBcVJFZ0p......
```

```text
#可选，会自动重启
[root@master1 ~]#systemctl restart kubelet.service
```

```text
#在所有节点重复上面过程，修改kubelet.conf文件
#方法1
[root@master1 ~]#kubeadm kubeconfig user --org system:nodes --client-name
system:node:nodeX.wang.org > nodeX.conf
#方法2
[root@master1 ~]#kubeadm kubeconfig user --org system:nodes --client-name
system:node:nodeX.wang.org |tail -n 3 >> nodeX.conf
[root@master1 ~]#scp nodeX.conf nodeX:
[root@nodeX ~]#cat nodeX.conf >>  /etc/kubernetes/kubelet.conf
[root@nodeX ~]#vim /etc/kubernetes/kubelet.conf
users:
- name: system:node:master1.wang.org
user: 将下面两行注释或删除
#client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
#client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
client-certificate-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURLekNDQWhPZ0F3SUJBZ0l.....
client-key-data:
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBcVJFZ0p......
```

```text
[root@nodeX ~]#systemctl restart kubelet.service
```

```text
#方法2: 直接修改kubelet.conf文件
#复制admin.conf最后两行
[root@master1 ~]#cp /etc/kubernetes/kubelet.conf{,.bak}
[root@master1 ~]#tail -n2 /etc/kubernetes/admin.conf  >>
/etc/kubernetes/kubelet.conf
```

```text
client-certificate-data:
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURJVENDQWdtZ0F3SUJBZ0lJWVQyZ1AzSkgyMmd3
RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TXpB
ek1EUXhOVE0yTWpOYUZ3MHlOVEF6TXpFd01qUXdNVE5hTURReApGekFWQmdOVkJBb1REbk41YzNSbGJU
cHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Fo
a2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTVmZzNtaVZ4eGxMbkFVNjYKSHJQRG5rQ2NmZkRL
RXFPcGtpQ0Fsa28zczFnMU52R1BuODE3eFd0TlYvc005SktQcVhKL1FRSVBxM3BFRmZPbApEVjJIN2RS
WSs5LzJhS0Nua0VkaDNNb01ZSTQ5MVpXVU5MekVJY0FSVE04aitCWnFxYVFiUjJTbmlZZ2E5NHpuCkdI
d09wRGRkaldVbTZxckZHTTh3anVid1VOVEtkUnFrQUE2cE5jUEJPUXhuSS9iNm1YUHpuUnpaSCtydENv
bjcKZFVPVG5mSmQrc0RUQ2E3NkhOU1dOUUhialVKeGVNdGdhdnZMOFVNZGVFNEtNR0JjVzczZ0VIN05X
eXJ2azVNRgpZdmd1NG9RY3QwaTFGY2RubjB5aXdLd2hpR0Z6bE9UVXJVdi96MWZZOWExdXJaUTBmczVV
Y2huYkdJcVRFbU1aCmVMUWU1UUlEQVFBQm8xWXdWREFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIw
bEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RBWURWUjBUQVFIL0JBSXdBREFmQmdOVkhTTUVHREFXZ0JRWUJ3
NzFnODl4UkcrbWRsNFg3NTZBb3VHSQpMVEFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBSW4vdUpta0Fw
QnY2UmJweVRFOFlRdmt6Smk5dnAwVU1rK25XClpFL3ZXOTBkT29CL2VqdDJ6ME51RW0rYnRsemZLU2JT
VS9RNHM4OXljbzN6dEZSbmNDRGZRTHBnVmdzMmp4ekQKSnZRWDBtTGFyd0drT2RwT3o2eGwxZ0h6NUxv
aFFCZy9xWG5EbThlbjQzSHgzUTdCRVRJdmxYd2tEVVkva0hYawpKSVU3SWdtNmNEc0IxYUNiWTltNmRl
UWllYXR0Z0ZBYlFQRHJaQmVMYjN2Z0haa240dXkzL3pZNjBXaXdTOUlxCitvYmxycWRiZ2p1bmtJeHl4
b0ZzMHgxRUNsaFN2WDBZYWR2MkJoMHZZQ2Fxd3lNUkhPUnFnS0QwQ2p6QnVZakYKZ1dOcmFtUC93dDFI
a3Z1UTUzdjM5Q3JpcXpmd1ZpZHlFbW9mVEhaWFJvbytMbHF5VkE9PQotLS0tLUVORCBDRVJUSUZJQ0FU
RS0tLS0tCg==
client-key-data:
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBNWZnM21pVnh4bExu
QVU2NkhyUERua0NjZmZES0VxT3BraUNBbGtvM3MxZzFOdkdQCm44MTd4V3ROVi9zTTlKS1BxWEovUVFJ
UHEzcEVGZk9sRFYySDdkUlkrOS8yYUtDbmtFZGgzTW9NWUk0OTFaV1UKTkx6RUljQVJUTThqK0JacXFh
UWJSMlNuaVlnYTk0em5HSHdPcERkZGpXVW02cXJGR004d2p1YndVTlRLZFJxawpBQTZwTmNQQk9ReG5J
L2I2bVhQem5SelpIK3J0Q29uN2RVT1RuZkpkK3NEVENhNzZITlNXTlFIYmpVSnhlTXRnCmF2dkw4VU1k
ZUU0S01HQmNXNzNnRUg3Tld5cnZrNU1GWXZndTRvUWN0MGkxRmNkbm4weWl3S3doaUdGemxPVFUKclV2
L3oxZlk5YTF1clpRMGZzNVVjaG5iR0lxVEVtTVplTFFlNVFJREFRQUJBb0lCQUZqbHFPakhqTUd6am1U
cwovL21hV0FZMng4ZlBhdTNsb2tsQWt6U0ZvQjZOL0pRdXNPeC9URmMyY1lHUEpLVHVldVp2d2sxbzlK
Ry9BODdRCmpuOHFKcitERkpyWktyR3JXTnJuSFNkeVczSi95ZHRrcFJQMTNJT0hjYWlWY2p3V3ZraXhq
WEg5c04zelpTbEkKcUpUSWNBaCs5b1VRRXdrbjFtVU93cUNiR1U3RkY1NTgyUG1iYWhZODF0aDg4M2dR
a3BQRGFGa1NTS0R5R3NyaQo4RUZjRHc2K2QyWXRhMTFjbmFWN1FORGpUK080bnhqdzk1ck5BR0RBQXRU
ZURNMUlHMjNHM1FyS2ZRMVlyalNoCitKK2ZGVmJ3cFFyYTN0WXhZeFJ5RjRadG9FTTNMbXZ5c3pTNG53
dUwvMmt1c0tuVFlWRVhBYWtSYzcvSUJJN0oKM3diVVpNa0NnWUVBOFRhWEladTJmRTlKd3g5R0lmcEFV
U3YwR3BxQ2UzYm9SWlVnNXBZZ1VuOGRaZVkvU1lCZQpHSlJvdW8vM1dIajRRTXFQMDh1cGVHa2o2eWxN
ZlVlMHVCTkUyWXlvd3hkSHJOVUhZbzFJY2p4REVUYzhXYUdKCmxEcXlzaFI2TzZ4SzdibVlqVjJDSkQx
RnZGMlFZRkhPNmd6MTh5UnpJT1Q3RFdBSGxoYzIwSGNDZ1lFQTlCRXQKajhsZXlZTFU5NDgzZ2RmaUFY
cXlXZkh4amdmTzI4cmhtamJUWVZqbWFLblpmdXNTWnRaSUJjMGk2dmZvNlVOTgpCb0xjR3lzbTVwZlZm
dmlCaEZVUGhXQnBwODNEVlYxYWt0OTRtQ1ppdHdjSUhjTXQ4ck12cC9PcWdSQmdlWlBuCnFWc3dUZlVj
QVVJam9EcWdOdERvNTM4M0ZENmpXRWJXQWdKeW5vTUNnWUFYRzBtaStJMmtudHZNQzBUbW9GaGsKN2pi
MkRYTU9iTGVYWXMvQ0J3T1ZvNE9uYlVVR3YzdEVFNE5zeTduQUNlYU9IbGxreW8remJ5NzNxZjhmeVN5
dwpyWGZjOXpKN2JkRjU1dlpNSklpYUdOZTc0SFN4aVYzcWl5enZEak1mWUVQVlBnQTFHbzRLOXF1bGZi
a0U0UkZYCkxtS3BKZ2E1VWZZU3MrNUdISGN0eFFLQmdFMUZod1JILysrU3NYUnpibUo0aEFCdDVUdWU0
eGhSbG9kMTB6bHMKOUQyVTFOWDhPSFQ3WGNjYlBwQS9vemQ3SjgxNlZrK2liS2RaWVNhT21iUnFYeThU
Y3llS0g4bFYxdXNXOUU4ZAoyMk5vZThad3Zud1Z5RjFYcDlYbnltcTBVYWNNVWNNSHNPSnRvT0V4SEhC
bFAwWTduQkYyOEd4RGJKbk5TNEkxClhpNmJBb0dCQU9GMzh3aGE2Ui9xQVJoWnQ4R0x0clZsL1ZiWXlG
UW10UGRZcW1KR29lY3RxMEFXR3hMQlM4ZWsKbFRkOURGK2JCemp0M1FhdUU2ZkhGbUk0Y256NmxjVnZ3
OTY4SnB6MWdqTC9Rc2lzaE5ZdDg1UFlEeFg3MmxtZwpoa3ZpNzVxaEFMNXZ1d3hpYzZGdG4wTktUVkFm
RU1BTlY0Y1ZOWll3MGllZ21QZUhsZncxCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==
```

```text
#修改kubelet.conf文件，将上面操作增加的两行替换此文件的最后两行
[root@master1 ~]#vim /etc/kubernetes/kubelet.conf
#删除下面两行
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```

```text
[root@master1 ~]#systemctl restart kubelet.service
```

```text
#确认只有当前节点正常,其它节点仍然异常
[root@master1 ~]#kubectl get nodes
NAME               STATUS     ROLES           AGE    VERSION
master1.wang.org   Ready      control-plane   392d   v1.26.2
node1.wang.org     NotReady   <none>          392d   v1.26.2
node2.wang.org     NotReady   <none>          392d   v1.26.2
node3.wang.org     NotReady   <none>          392d   v1.26.2
```

```text
#在所有节点修改kubelet.conf文件
[root@master1 ~]#rsync -a /etc/kubernetes/kubelet.conf
node{1..3}.wang.org:/etc/kubernetes/kubelet.conf
#所有节点重启服务,可选
[root@node1 ~]#systemctl restart kubelet.service
```

```text
#方法3:
#重新创建软链接
[root@master1 ~]#rm -f /var/lib/kubelet/pki/kubelet-client-current.pem
[root@master1 ~]#TIME=$(date +%F-%H-%M-%S);touch /var/lib/kubelet/pki/kubelet-
client-$TIME.pem
[root@master1 ~]#ln -s /var/lib/kubelet/pki/kubelet-client-$TIME.pem
/var/lib/kubelet/pki/kubelet-client-current.pem
#将/etc/kubernetes/admin.conf的client-certificate-data和client-key-data用base64 反
转码导入/var/lib/kubelet/pki/kubelet-client-current.pem文件
[root@master1 ~]#tail -n 2  /etc/kubernetes/admin.conf |awk '{print $NF}' |base64
-d >  /var/lib/kubelet/pki/kubelet-client-current.pem
#或者手动转换
[root@master1 ~]#echo
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURJVENDQWdtZ0F3SUJBZ0lJWVQyZ1AzSkgyMmd3
RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TXpB
ek1EUXhOVE0yTWpOYUZ3MHlOVEF6TXpFd01qUXdNVE5hTURReApGekFWQmdOVkJBb1REbk41YzNSbGJU
cHRZWE4wWlhKek1S.....
S0QwQ2p6QnVZakYKZ1dOcmFtUC93dDFIa3Z1UTUzdjM5Q3JpcXpmd1ZpZHlFbW9mVEhaWFJvbytMbHF5
VkE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg== |base64 -d  >
/var/lib/kubelet/pki/kubelet-client-current.pem
```

```text
[root@master1 ~]#echo
LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb3dJQkFBS0NBUUVBNWZnM21pVnh4bExu
QVU2NkhyUERua0NjZmZES0VxT3BraUNBbGtvM3MxZzFOdkdQ
.....
MGllZ21QZUhsZncxCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg== | base64 -d >>
/var/lib/kubelet/pki/kubelet-client-current.pem
```

```text
#确定文件更新
[root@master1 ~]#cat /var/lib/kubelet/pki/kubelet-client-current.pem
-----BEGIN CERTIFICATE-----
MIIDITCCAgmgAwIBAgIIYT2gP3JH22gwDQYJKoZIhvcNAQELBQAwFTETMBEGA1UE
AxMKa3ViZXJuZXRlczAeFw0yMzAzMDQxNTM2MjNaFw0yNTAzMzEwMjQwMTNaMDQx
FzAVBgNVBAoTDnN5c3RlbTptYXN0ZXJzMRkwFwYDVQQDExBrdWJlcm5ldGVzLWFk
bWluMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA5fg3miVxxlLnAU66
HrPDnkCcffDKEqOpkiCAlko3s1g1NvGPn817xWtNV/sM9JKPqXJ/QQIPq3pEFfOl
DV2H7dRY+9/2aKCnkEdh3MoMYI491ZWUNLzEIcARTM8j+BZqqaQbR2SniYga94zn
GHwOpDddjWUm6qrFGM8wjubwUNTKdRqkAA6pNcPBOQxnI/b6mXPznRzZH+rtCon7
dUOTnfJd+sDTCa76HNSWNQHbjUJxeMtgavvL8UMdeE4KMGBcW73gEH7NWyrvk5MF
Yvgu4oQct0i1Fcdnn0yiwKwhiGFzlOTUrUv/z1fY9a1urZQ0fs5UchnbGIqTEmMZ
eLQe5QIDAQABo1YwVDAOBgNVHQ8BAf8EBAMCBaAwEwYDVR0lBAwwCgYIKwYBBQUH
AwIwDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBQYBw71g89xRG+mdl4X756AouGI
LTANBgkqhkiG9w0BAQsFAAOCAQEAIn/uJmkApBv6RbpyTE8YQvkzJi9vp0UMk+nW
```

```text
ZE/vW90dOoB/ejt2z0NuEm+btlzfKSbSU/Q4s89yco3ztFRncCDfQLpgVgs2jxzD
JvQX0mLarwGkOdpOz6xl1gHz5LohQBg/qXnDm8en43Hx3Q7BETIvlXwkDUY/kHXk
JIU7Igm6cDsB1aCbY9m6deQieattgFAbQPDrZBeLb3vgHZkn4uy3/zY60WiwS9Iq
+oblrqdbgjunkIxyxoFs0x1EClhSvX0Yadv2Bh0vYCaqwyMRHORqgKD0CjzBuYjF
gWNramP/wt1HkvuQ53v39CriqzfwVidyEmofTHZXRoo+LlqyVA==
-----END CERTIFICATE-----
-----BEGIN RSA PRIVATE KEY-----
<REDACTED_PRIVATE_KEY>
-----END RSA PRIVATE KEY-----
```

```text
#确认证书文件更新
[root@master1 ~]#ll /var/lib/kubelet/pki
total 24
drwxr-xr-x 2 root root 4096 Apr 16 09:35 ./
drwx------ 8 root root 4096 Mar  7  2023 ../
-rw------- 1 root root 2822 Apr 16 09:27 kubelet-client-2023-03-07-12-30-14.pem
-rw-r--r-- 1 root root 2822 Apr 16 09:35 kubelet-client-2024-04-16-09-28-28.pem
lrwxrwxrwx 1 root root   59 Apr 16 09:35 kubelet-client-current.pem ->
/var/lib/kubelet/pki/kubelet-client-2024-04-16-09-28-28.pem
-rw-r--r-- 1 root root 2307 Mar  7  2023 kubelet.crt
-rw------- 1 root root 1675 Mar  7  2023 kubelet.key
```

```text
#在所有节点同步证书信息
[root@master1 ~]#rsync -a /var/lib/kubelet/pki/*.pem
node{1..3}.wang.org:/var/lib/kubelet/pki/
```

```text
#所有节点重启服务,可选
[root@node1 ~]#systemctl restart kubelet.service
```

```text
#最后确认所有节点正常
[root@master1 ~]#kubectl get nodes
NAME               STATUS   ROLES           AGE    VERSION
master1.wang.org   Ready    control-plane   392d   v1.26.2
node1.wang.org     Ready    <none>          392d   v1.26.2
```

```text
node2.wang.org     Ready    <none>          392d   v1.26.2
node3.wang.org     Ready    <none>          392d   v1.26.2
```

```text
#测试创建Pod
[root@master1 ~]#kubectl create  deployment myapp --image=registry.cn-
beijing.aliyuncs.com/wangxiaochun/pod-test:v0.1  --replicas=3
```

```text
[root@master1 ~]#kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
myapp-7bbdff8fc8-b74fx   1/1     Running   0          17m
myapp-7bbdff8fc8-csczr   1/1     Running   0          16m
myapp-7bbdff8fc8-tdgqn   1/1     Running   0          17m
```

## 3.4 Kubernetes 证书终极解决方案"永久有效"

```text
#检查证书当前有效期
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the "kubeadm-config" ConfigMap in
namespace "kube-system"...
[check-expiration] Use 'kubeadm init phase upload-config --config your-
config.yaml' to re-upload it.
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 19, 2025 01:05 UTC   211d            ca
no
apiserver                  Dec 19, 2025 01:05 UTC   211d            ca
no
apiserver-etcd-client      Dec 19, 2025 01:05 UTC   211d            etcd-ca
no
apiserver-kubelet-client   Dec 19, 2025 01:05 UTC   211d            ca
no
controller-manager.conf    Dec 19, 2025 01:05 UTC   211d            ca
no
etcd-healthcheck-client    Dec 19, 2025 01:05 UTC   211d            etcd-ca
no
etcd-peer                  Dec 19, 2025 01:05 UTC   211d            etcd-ca
no
etcd-server                Dec 19, 2025 01:05 UTC   211d            etcd-ca
no
front-proxy-client         Dec 19, 2025 01:05 UTC   211d            front-proxy-
ca          no
scheduler.conf             Dec 19, 2025 01:05 UTC   211d            ca
no
super-admin.conf           Dec 19, 2025 01:05 UTC   211d            ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Dec 17, 2034 01:05 UTC   9y              no
etcd-ca                 Dec 17, 2034 01:05 UTC   9y              no
front-proxy-ca          Dec 17, 2034 01:05 UTC   9y              no
```

```text
[root@master1 ~]#apt update && apt -y  install git
```

```text
#查看当前版本
```

```text
[root@master1 ~]#kubeadm version
kubeadm version: &version.Info{Major:"1", Minor:"32", GitVersion:"v1.32.0",
GitCommit:"70d3cc986aa8221cd1dfb1121852688902d3bf53", GitTreeState:"clean",
BuildDate:"2024-12-11T18:04:20Z", GoVersion:"go1.23.3", Compiler:"gc",
Platform:"linux/amd64"}
```

```text
#下载指定版本的源码
#方法1：全部下载,此方式下载慢,不推存
[root@master1 ~]#git clone   https://githubfast.com/kubernetes/kubernetes.git
[root@master1 ~]#cd kubernetes/
[root@master1 kubernetes]#du -sh .
1.5G    .
[root@master1 kubernetes]#git branch
* master
[root@master1 kubernetes]#git checkout release-1.32
[root@master1 kubernetes]#git branch
master
* release-1.32
```

```text
#方法2: 只下载指定版本的分支,此方式下载更,推存使用
[root@master1 ~]#git clone --depth 1  --branch v1.32.0
https://github.com/kubernetes/kubernetes.git
Cloning into 'kubernetes'...
fatal: unable to access 'https://github.com/kubernetes/kubernetes.git/': Failed
to connect to github.com port 443 after 21059 ms: Connection refused
```

```text
#如果下载失败，可以用如下代理重新下载
[root@master1 ~]#git clone --depth 1  --branch v1.32.0
https://githubfast.com/kubernetes/kubernetes.git
Cloning into 'kubernetes'...
remote: Enumerating objects: 26015, done.
remote: Counting objects: 100% (26015/26015), done.
remote: Compressing objects: 100% (17142/17142), done.
remote: Total 26015 (delta 7422), reused 24275 (delta 7028), pack-reused 0 (from
0)
Receiving objects: 100% (26015/26015), 39.16 MiB | 3.16 MiB/s, done.
Resolving deltas: 100% (7422/7422), done.
Note: switching to '70d3cc986aa8221cd1dfb1121852688902d3bf53'.
```

```text
You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by switching back to a branch.
```

```text
If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -c with the switch command. Example:
```

```text
git switch -c <new-branch-name>
```

```text
Or undo this operation with:
```

```text
git switch -
```

```text
Turn off this advice by setting config variable advice.detachedHead to false
```

```text
Updating files: 100% (26242/26242), done.
```

```text
#查看大小
```

```text
[root@master1 ~]#du -sh kubernetes/
353M    kubernetes/
```

```text
[root@master1 ~]#cd kubernetes/
[root@master1 kubernetes]#git log
commit 70d3cc986aa8221cd1dfb1121852688902d3bf53 (grafted, HEAD, tag: v1.32.0)
Author: Kubernetes Release Robot <k8s-release-robot@users.noreply.github.com>
Date:   Wed Dec 11 17:59:15 2024 +0000
```

```text
Release commit for Kubernetes v1.32.0
[root@master1 kubernetes]#git branch
* (no branch)
```

```text
#修改源码中的证书有效期
#1)修改ca证书到200年,注意：1.32版本以前版本才需要修改此文件,1.32版本以后无需修改此文件
[root@master1 kubernetes]#vim staging/src/k8s.io/client-go/util/cert/cert.go
......
DNSNames:              []string{cfg.CommonName},
NotBefore:             notBefore,
//NotAfter:              now.Add(duration365d * 10).UTC(), #注释此行
NotAfter:              now.Add(duration365d * 200).UTC(),  #修改为此行
KeyUsage:              x509.KeyUsageKeyEncipherment |
x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
......
```

```text
#2)修改指定服务器的证书的有效期,1.32版本以后只需修改此文件
#把24*365 换成 24*365*100
[root@master1 ~]#cd kubernetes/
[root@master1 kubernetes]#vim cmd/kubeadm/app/constants/constants.go
#1.30版之前
// CertificateValidity defines the validity for all the signed certificates
generated by kubeadm
CertificateValidity = time.Hour * 24 * 365 * 100 #1.30版之前修改此行
```

```text
#1.32版之后
// CertificateValidityPeriod defines the validity period for all the signed
certificates generated by kubeadm
// CertificateValidityPeriod = time.Hour * 24 * 365    #原代码,修改为如下
CertificateValidityPeriod = time.Hour * 24 * 365 * 100 #修改此行,指定服务器的证书
的有效期，1.32版
// CACertificateValidityPeriod defines the validity period for all the
signed CA certificates generated by kubeadm
// CACertificateValidityPeriod = time.Hour * 24 * 365 * 10 #原代码,修改为如下
CACertificateValidityPeriod = time.Hour * 24 * 365 * 200 #修改此行,指定CA的证书
的有效期200年
```

```text
#编译一两分钟
[root@master1 kubernetes]#apt update && apt -y  install make
[root@master1 kubernetes]#make all WHAT=cmd/kubeadm GOFLAGS=-v
```

```text
#编译完成以后，获取对应的kubeadm二进制包。
[root@master1 kubernetes]#ls -l _output/bin/kubeadm
-rwxr-xr-x 1 root root 70942872 May 20 18:06 _output/bin/kubeadm
```

```text
[root@master1 kubernetes]#_output/bin/kubeadm version
```

```text
kubeadm version: &version.Info{Major:"1", Minor:"32+", GitVersion:"v1.32.0-
dirty", GitCommit:"70d3cc986aa8221cd1dfb1121852688902d3bf53",
GitTreeState:"dirty", BuildDate:"2025-05-20T10:03:36Z", GoVersion:"go1.23.3",
Compiler:"gc", Platform:"linux/amd64"}
```

```text
#查看当前版本的kubeadm路径
[root@master1 kubernetes]#which kubeadm
/usr/bin/kubeadm
```

```text
[root@master1 kubernetes]#ls -l /usr/bin/kubeadm
-rwxr-xr-x 1 root root 70942872 Dec 12 02:37 /usr/bin/kubeadm
```

```text
#在所有节点上覆盖当前版本的kubeadm命令
[root@master1 kubernetes]#cp -b _output/bin/kubeadm /usr/bin/kubeadm
[root@master1 kubernetes]#scp /usr/bin/kubeadm nodeX.wang.org:/usr/bin/kubeadm
```

```text
[root@master1 kubernetes]#ls /usr/bin/kubeadm* -l
-rwxr-xr-x 1 root root 70942872 May 20 18:09 /usr/bin/kubeadm
-rwxr-xr-x 1 root root 70942872 Dec 12 02:37 /usr/bin/kubeadm~
```

```text
#更新CA和服务的证书,注意:只能重新安装k8s集群才能更新有效期生效,只执行kubeadm certs renew
all是不生效的
#如果已经安装好的Kubernetes集群,需要先删除Kubernetes集群再重新创建和初始化Kubernetes集群
#方法1:手动执行命令
[root@master1 ~]#kubeadm reset -f --cri-socket unix:///run/cri-dockerd.sock
[root@nodeX ~]#kubeadm reset -f --cri-socket unix:///run/cri-dockerd.sock
#方法2:基于脚本删除k8s
[root@master1 ~]#bash install/install_kubernetes_docker.sh
1) 初始化新的Kubernetes集群
2) 加入已有的Kubernetes集群
3) 退出Kubernetes集群
4) 退出本程序
请选择编号(1-4): 3
#所有其它节点重新退出并加入集群
[root@nodeX ~]#bash install/install_kubernetes_docker.sh
1) 初始化新的Kubernetes集群
2) 加入已有的Kubernetes集群
3) 退出Kubernetes集群
4) 退出本程序
请选择编号(1-4): 3
```

```text
#如果没有安装Kubernetes集群,利用新版本的kubeadm 创建集群
#方法1:手动执行命令
[root@master1 ~]#kubeadm init .....
[root@nodeX ~]#kubeadm join .....
```

```text
#方法2:基于脚本创建k8s
[root@master1 ~]#bash install/install_kubernetes_docker.sh
1) 初始化新的Kubernetes集群
2) 加入已有的Kubernetes集群
3) 退出Kubernetes集群
4) 退出本程序
请选择编号(1-4): 1
#所有其它节点重新退出并加入集群
[root@nodeX ~]#bash install/install_kubernetes_docker.sh
1) 初始化新的Kubernetes集群
2) 加入已有的Kubernetes集群
```

```text
3) 退出Kubernetes集群
4) 退出本程序
请选择编号(1-4): 2
```

```text
#验证和检查证书有效期已经永久
[root@master1 ~]#kubeadm certs check-expiration
[check-expiration] Reading configuration from the "kubeadm-config" ConfigMap in
namespace "kube-system"...
[check-expiration] Use 'kubeadm init phase upload-config --config your-
config.yaml' to re-upload it.
```

```text
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE
AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Apr 26, 2125 10:20 UTC   99y             ca
no
apiserver                  Apr 26, 2125 10:20 UTC   99y             ca
no
apiserver-etcd-client      Apr 26, 2125 10:20 UTC   99y             etcd-ca
no
apiserver-kubelet-client   Apr 26, 2125 10:20 UTC   99y             ca
no
controller-manager.conf    Apr 26, 2125 10:20 UTC   99y             ca
no
etcd-healthcheck-client    Apr 26, 2125 10:20 UTC   99y             etcd-ca
no
etcd-peer                  Apr 26, 2125 10:20 UTC   99y             etcd-ca
no
etcd-server                Apr 26, 2125 10:20 UTC   99y             etcd-ca
no
front-proxy-client         Apr 26, 2125 10:20 UTC   99y             front-proxy-
ca          no
scheduler.conf             Apr 26, 2125 10:20 UTC   99y             ca
no
super-admin.conf           Apr 26, 2125 10:20 UTC   99y             ca
no
```

```text
CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY
MANAGED
ca                      Apr 02, 2225 10:20 UTC   199y            no
etcd-ca                 Apr 02, 2225 10:20 UTC   199y            no
front-proxy-ca          Apr 02, 2225 10:20 UTC   199y            no
```

```text
#手动更新授权文件
[root@master1 ~]#cp /etc/kubernetes/admin.conf  .kube/config
```

```text
#检查证书
[root@master1 ~]#ll /etc/kubernetes/pki/
[root@master1 ~]#openssl x509 -in /etc/kubernetes/pki/apiserver.crt -dates -
noout
notBefore=May 20 10:15:13 2025 GMT
notAfter=Apr 26 10:20:13 2125 GMT
[root@master1 ~]#openssl x509 -in /etc/kubernetes/pki/ca.crt -dates -noout
notBefore=May 20 10:15:13 2025 GMT
notAfter=Apr  2 10:20:13 2225 GMT
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Kubernetes/34-backup-restore.html' | relative_url }}">← 上一章：集群备份、恢复与迁移</a>
  <a href="{{ '/subjects/Kubernetes/' | relative_url }}">返回 Kubernetes 目录</a>
  <a href="{{ '/subjects/Kubernetes/36-upgrade-optimization.html' | relative_url }}">下一章：版本升级与性能优化 →</a>
</nav>
