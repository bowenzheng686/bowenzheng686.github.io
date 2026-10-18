---
layout: default
title: "Docker 容器技术 · Docker的默认的网络通信（学习）"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 14 Docker的默认的网络通信（学习）
## 4 Docker 网络管理

![Docker 容器技术第 271 页插图](assets/img-cace5f8f392e04e4.png)

docker容器创建后，通常需要和其它主机或容器进行网络通信

官方文档:

<https://docs.docker.com/network/>

### 4.1 Docker的默认的网络通信（学习）

### Docker安装后默认的网络设置

Docker服务安装完成之后，默认在每个宿主机会生成一个名称为docker0的网卡其IP地址都是 172.17.0.1/16

范例:  安装Docker的默认的网络配置

```bash
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:34:df:91 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe34:df91/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:02:7f:a8:c6 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:2ff:fe7f:a8c6/64 scope link
valid_lft forever preferred_lft forever
[root@ubuntu1804 ~]#apt update && apt -y install bridge-utils
[root@ubuntu1804 ~]#brctl show
bridge name bridge id       STP enabled interfaces
docker0     8000.0242027fa8c6   no
```

范例:  安装Harbor的默认网络配置

```bash
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:01:f3:0c brd ff:ff:ff:ff:ff:ff
inet 10.0.0.102/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe01:f30c/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:f4:23:e8:29 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
4: br-9af624ecd23e: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
state UP group default
link/ether 02:42:e9:1c:1a:7b brd ff:ff:ff:ff:ff:ff
inet 172.18.0.1/16 brd 172.18.255.255 scope global br-9af624ecd23e
valid_lft forever preferred_lft forever
inet6 fe80::42:e9ff:fe1c:1a7b/64 scope link
valid_lft forever preferred_lft forever
6: veth225895c@if5: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether a6:f3:0f:ae:4b:43 brd ff:ff:ff:ff:ff:ff link-netnsid 0
inet6 fe80::a4f3:fff:feae:4b43/64 scope link
valid_lft forever preferred_lft forever
8: veth244c237@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether 72:12:35:11:e8:14 brd ff:ff:ff:ff:ff:ff link-netnsid 1
inet6 fe80::7012:35ff:fe11:e814/64 scope link
valid_lft forever preferred_lft forever
10: veth81ab8cb@if9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether 5e:07:f2:eb:43:c2 brd ff:ff:ff:ff:ff:ff link-netnsid 2
inet6 fe80::5c07:f2ff:feeb:43c2/64 scope link
valid_lft forever preferred_lft forever
12: vethf8499d4@if11: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether 4e:df:12:c5:58:83 brd ff:ff:ff:ff:ff:ff link-netnsid 4
inet6 fe80::4cdf:12ff:fec5:5883/64 scope link
valid_lft forever preferred_lft forever
14: vethceabf74@if13: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether 06:c0:58:ea:51:2e brd ff:ff:ff:ff:ff:ff link-netnsid 5
inet6 fe80::4c0:58ff:feea:512e/64 scope link
valid_lft forever preferred_lft forever
16: veth47c5069@if15: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether c6:6f:aa:51:be:38 brd ff:ff:ff:ff:ff:ff link-netnsid 3
inet6 fe80::c46f:aaff:fe51:be38/64 scope link
valid_lft forever preferred_lft forever
18: veth83fde4a@if17: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether 32:74:1e:e2:81:50 brd ff:ff:ff:ff:ff:ff link-netnsid 6
inet6 fe80::3074:1eff:fee2:8150/64 scope link
valid_lft forever preferred_lft forever
20: veth2c51f87@if19: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether ca:b7:c9:da:87:92 brd ff:ff:ff:ff:ff:ff link-netnsid 7
inet6 fe80::c8b7:c9ff:feda:8792/64 scope link
valid_lft forever preferred_lft forever
22: veth0f4a931@if21: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether fa:29:a4:4d:b1:c2 brd ff:ff:ff:ff:ff:ff link-netnsid 8
inet6 fe80::f829:a4ff:fe4d:b1c2/64 scope link
valid_lft forever preferred_lft forever
24: veth55b6555@if23: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master br-9af624ecd23e state UP group default
link/ether aa:87:c4:2c:de:7c brd ff:ff:ff:ff:ff:ff link-netnsid 9
inet6 fe80::a887:c4ff:fe2c:de7c/64 scope link
valid_lft forever preferred_lft forever
```

```bash
[root@ubuntu1804 ~]#apt -y install bridge-utils
[root@ubuntu1804 ~]#brctl show
bridge name bridge id       STP enabled interfaces
br-9af624ecd23e     8000.0242e91c1a7b   no      veth0f4a931
veth225895c
veth244c237
veth2c51f87
veth47c5069
veth55b6555
veth81ab8cb
veth83fde4a
vethceabf74
vethf8499d4
docker0     8000.0242f423e829   no
```

### 创建容器后的网络配置

veth（Virtual Ethernet）是Linux内核中的一种虚拟网络设备，通常用于连接两个网络命名空间。veth 设备总是成对出现，当在一个网络命名空间中创建veth设备时，会同时创建两个端点。veth设备的两个端点可以被看作是一个虚拟的以太网电缆，任何发送到其中一个端点的数据包都会被立即从另一个端点传出。以下是veth设备的一些主要特性：

1. 命名空间间通信：veth设备主要用于连接不同的网络命名空间，允许它们之间进行通信。这使得在

一个隔离的环境中运行的进程可以与外部世界交互，而不会影响到其它网络命名空间。

2. 成对出现：veth设备总是成对创建的，形成一个虚拟的双向通道。当数据包发送到一个端点时，它

会从另一个端点出来。因此，你可以把veth设备看作是一个虚拟的以太网电缆。

3. 灵活性：veth设备的两个端点可以分别位于不同的网络命名空间中，甚至可以在同一命名空间中。

这为设置复杂的网络拓扑提供了很大的灵活性。

4. 和其他网络设备相互操作：veth设备可以和Linux的其他网络设备（如bridge、veth pair、

physical NIC等）一起使用，创建复杂的网络配置。

veth设备在一些网络虚拟化技术中被广泛使用，例如Docker容器。每一个Docker容器都有自己的网络命名空间，Docker使用veth设备连接容器的网络命名空间和主机的网络命名空间，使得容器可以和外部网络进行通信。

每次新建容器后

宿主机多了一个虚拟网卡vethxxxxx，和容器的网卡组合成一个网卡，比如:  137: veth8ca6d43@if136，而在容器内的网卡名为136，可以看出和宿主机的网卡之间的关联容器会自动获取一个172.17.0.0/16网段的随机地址，默认从172.17.0.2开始，第二次容器为 172.17.0.3，以此类推容器获取的地址并不固定,每次容器重启,可能会发生地址变化

范例：veth特性

```bash
[root@ubuntu2404 ~]#ip netns add c1-net
[root@ubuntu2404 ~]#ip netns add c2-net
[root@ubuntu2404 ~]#ip link add eth1 type veth peer eth2
[root@ubuntu2404 ~]#ip link set eth1 netns c1-net
[root@ubuntu2404 ~]#ip link set eth2 netns c2-net
[root@ubuntu2404 ~]#ip netns exec c1-net ip a a 1.1.1.1/24 dev eth1
[root@ubuntu2404 ~]#ip netns exec c2-net ip a a 1.1.1.2/24 dev eth2
[root@ubuntu2404 ~]#ip netns exec c1-net ip link set eth1 up
[root@ubuntu2404 ~]#ip netns exec c2-net ip link set eth2 up
[root@ubuntu2404 ~]#ip netns exec c1-net ping -c1  1.1.1.2
PING 1.1.1.2 (1.1.1.2) 56(84) bytes of data.
64 bytes from 1.1.1.2: icmp_seq=1 ttl=64 time=0.030 ms
--- 1.1.1.2 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.030/0.030/0.030/0.000 ms
[root@ubuntu2404 ~]#ip netns exec c2-net ping 1.1.1.1
#默认无法ping通信自身
[root@ubuntu2404 ~]#ip netns exec c1-net ping 1.1.1.1
#启劝lo可以实现ping通信自身
[root@ubuntu2404 ~]#ip netns exec c1-net ip link set lo up
[root@ubuntu2404 ~]#ip netns exec c1-net ping -c1 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=64 time=0.021 ms
--- 1.1.1.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.021/0.021/0.021/0.000 ms
```

范例:  veth 桥接

```bash
#创建网桥
[root@node1 ~]#ip link add br0 type bridge
#创建虚拟网卡对veth
[root@node1 ~]#ip link add veth1 type veth peer veth1-eth0
#veth桥接
[root@node1 ~]#ip link set veth1-eth0 master br0
#查看桥接
[root@node1 ~]#ip link show master br0
9: veth1-eth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop master br0
state DOWN mode DEFAULT group default qlen 1000
link/ether 56:e8:ef:3f:8e:af brd ff:ff:ff:ff:ff:ff
#veth桥接
[root@node1 ~]#ip link set veth1 master br0
[root@node1 ~]#ip link show master br0
9: veth1-eth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop master br0
state DOWN mode DEFAULT group default qlen 1000
link/ether 56:e8:ef:3f:8e:af brd ff:ff:ff:ff:ff:ff
10: veth1@veth1-eth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop master
br0 state DOWN mode DEFAULT group default qlen 1000
link/ether a6:55:12:8c:96:c6 brd ff:ff:ff:ff:ff:ff
```

### 创建第一个容器后的网络状态

范例:  创建容器，容器自动获取IP地址

```bash
[root@ubuntu1804 ~]#docker run -it --rm  alpine:3.11 sh
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
136: eth0@if137: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
state UP
link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
valid_lft forever preferred_lft forever
/ # cat /etc/hosts
127.0.0.1   localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.17.0.2  6b8d9f3a653e
[root@ubuntu1804 ~]#docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED
STATUS              PORTS               NAMES
6b8d9f3a653e        alpine:3.11         "sh"                13 seconds ago
Up 12 seconds                           pensive_chandrasekhar
```

范例:  新建一个容器，在宿主机的会生成一个新网卡，和容器成对儿的出现

```yaml
[root@ubuntu1804 ~]#docker run -it  ubuntu bash
root@d57f2df8ad40:/# apt update && apt install ethtool iproute2 -y
root@d57f2df8ad40:/# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
#if8 表示容器的eth0网卡对应宿主机的8号网卡
7: eth0@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
group default
link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
valid_lft forever preferred_lft forever
#查看容器的类型为veth
root@d57f2df8ad40:/# ethtool -i eth0
driver: veth
version: 1.0
firmware-version:
expansion-rom-version:
bus-info:
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: no
#查看容器网卡和宿主机网卡的对应关系
root@d57f2df8ad40:/# ethtool -S eth0
NIC statistics:
peer_ifindex: 8   #表示对应宿主机的8号网卡
rx_queue_0_xdp_packets: 0
rx_queue_0_xdp_bytes: 0
rx_queue_0_drops: 0
rx_queue_0_xdp_redirect: 0
rx_queue_0_xdp_drops: 0
rx_queue_0_xdp_tx: 0
rx_queue_0_xdp_tx_errors: 0
tx_queue_0_xdp_xmit: 0
tx_queue_0_xdp_xmit_errors: 0
#宿主机查看8号网卡
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:34:df:91 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe34:df91/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
group default
link/ether 02:42:02:7f:a8:c6 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:2ff:fe7f:a8c6/64 scope link
valid_lft forever preferred_lft forever
#8号网卡
8: veth151f8fa@if7: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master docker0 state UP group default
link/ether fa:d5:35:85:1d:c4 brd ff:ff:ff:ff:ff:ff link-netnsid 0
inet6 fe80::f8d5:35ff:fe85:1dc4/64 scope link
valid_lft forever preferred_lft forever
#查看宿主机网卡类型
[root@ubuntu1804 ~]#ethtool -i veth151f8fa
driver: veth
version: 1.0
firmware-version:
expansion-rom-version:
bus-info:
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: no
#查看宿主机网卡和容器的对应关系
[root@ubuntu1804 ~]#ethtool -S veth151f8fa
NIC statistics:
peer_ifindex: 7 #对应容器的7号网卡
rx_queue_0_xdp_packets: 0
rx_queue_0_xdp_bytes: 0
rx_queue_0_drops: 0
rx_queue_0_xdp_redirect: 0
rx_queue_0_xdp_drops: 0
rx_queue_0_xdp_tx: 0
rx_queue_0_xdp_tx_errors: 0
tx_queue_0_xdp_xmit: 0
tx_queue_0_xdp_xmit_errors: 0
```

范例:  查看新建容器后桥接状态

```bash
[root@ubuntu1804 ~]#brctl show
bridge name bridge id       STP enabled interfaces
docker0     8000.0242027fa8c6   no      veth8ca6d43
```

### 创建第二个容器后面的网络状态

范例:  再次创建第二个容器

```bash
[root@ubuntu1804 ~]#docker run -it --rm  alpine:3.11 sh
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
140: eth0@if141: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
state UP
link/ether 02:42:ac:11:00:03 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.3/16 brd 172.17.255.255 scope global eth0
valid_lft forever preferred_lft forever
/ # cat /etc/hosts
127.0.0.1   localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.17.0.3  ab3ea580804a
/ # ping ab3ea580804a
PING ab3ea580804a (172.17.0.3): 56 data bytes
64 bytes from 172.17.0.3: seq=0 ttl=64 time=0.037 ms
64 bytes from 172.17.0.3: seq=1 ttl=64 time=0.132 ms
^C
--- ab3ea580804a ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.037/0.084/0.132 ms
/ # ping 6b8d9f3a653e
ping: bad address '6b8d9f3a653e'
/ #
```

```bash
[root@ubuntu1804 ~]#docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED
STATUS              PORTS               NAMES
ab3ea580804a        alpine:3.11         "sh"                9 seconds ago
Up 7 seconds                            vigilant_jones
6b8d9f3a653e        alpine:3.11         "sh"                13 seconds ago
Up 12 seconds                           pensive_chandrasekhar
```

范例:  新建第二个容器后宿主机又多了一个虚拟网卡

```bash
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:34:df:91 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe34:df91/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
group default
link/ether 02:42:02:7f:a8:c6 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:2ff:fe7f:a8c6/64 scope link
valid_lft forever preferred_lft forever
137: veth8ca6d43@if136: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master docker0 state UP group default
link/ether fa:96:37:77:a9:a9 brd ff:ff:ff:ff:ff:ff link-netnsid 0
inet6 fe80::f896:37ff:fe77:a9a9/64 scope link
valid_lft forever preferred_lft forever
141: vethf599a47@if140: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master docker0 state UP group default
link/ether 96:e7:52:fe:67:54 brd ff:ff:ff:ff:ff:ff link-netnsid 1
inet6 fe80::94e7:52ff:fefe:6754/64 scope link
valid_lft forever preferred_lft forever
```

范例:  查看新建第二个容器后桥接状态

```bash
[root@ubuntu1804 ~]#brctl  show
bridge name bridge id       STP enabled interfaces
docker0     8000.0242027fa8c6   no      veth8ca6d43
vethf599a47
```

### 容器间的通信

### 同一个宿主机的不同容器可相互通信

默认情况下

同一个宿主机的不同容器之间可以相互通信

```text
dockerd   --icc    Enable inter-container communication (default true)
--icc=false  #此配置可以禁止同一个宿主机的容器之间通信
```

不同宿主机之间的容器IP地址重复，默认不能相互通信

范例:  同一个宿主机的容器之间访问

```bash
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:34:df:91 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe34:df91/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
group default
link/ether 02:42:02:7f:a8:c6 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:2ff:fe7f:a8c6/64 scope link
valid_lft forever preferred_lft forever
137: veth8ca6d43@if136: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master docker0 state UP group default
link/ether fa:96:37:77:a9:a9 brd ff:ff:ff:ff:ff:ff link-netnsid 0
inet6 fe80::f896:37ff:fe77:a9a9/64 scope link
valid_lft forever preferred_lft forever
141: vethf599a47@if140: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue
master docker0 state UP group default
link/ether 96:e7:52:fe:67:54 brd ff:ff:ff:ff:ff:ff link-netnsid 1
inet6 fe80::94e7:52ff:fefe:6754/64 scope link
valid_lft forever preferred_lft forever
[root@ubuntu1804 ~]#docker run -it --rm  alpine:3.11 sh
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
136: eth0@if137: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
state UP
link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
valid_lft forever preferred_lft forever
/ # ping 172.17.0.3
PING 172.17.0.3 (172.17.0.3): 56 data bytes
64 bytes from 172.17.0.3: seq=0 ttl=64 time=0.452 ms
64 bytes from 172.17.0.3: seq=1 ttl=64 time=0.190 ms
^C
--- 172.17.0.3 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.190/0.321/0.452 ms
/ # ping 172.17.0.1
PING 172.17.0.1 (172.17.0.1): 56 data bytes
64 bytes from 172.17.0.1: seq=0 ttl=64 time=0.139 ms
64 bytes from 172.17.0.1: seq=1 ttl=64 time=0.183 ms
^C
--- 172.17.0.1 ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 0.139/0.161/0.183 ms
/ #
```

### 禁止同一个宿主机的不同容器间通信

范例: 同一个宿主机不同容器间禁止通信

```bash
#dockerd 的 --icc=false 选项可以禁止同一个宿主机的不同容器间通信
[root@ubuntu1804 ~]#vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
--icc=false
[root@ubuntu1804 ~]#systemctl daemon-reload
[root@ubuntu1804 ~]#systemctl restart docker
#创建两个容器,测试无法通信
[root@ubuntu1804 ~]#docker run -it --name test1 --rm alpine  sh
/ # hostname -i
172.17.0.2
[root@ubuntu1804 ~]#docker run -it --name test2 --rm alpine  sh
/ # hostname -i
172.17.0.3
/ # ping 172.17.0.2
```

```bash
#添加--icc选项，本质上就是修改iptables规则 -A FORWARD -i docker0 -o docker0 -j
ACCEPT修改为DROP
[root@ubuntu2204 ~]#iptables -S > icc.txt
[root@ubuntu2204 ~]#diff icc.txt no_icc.txt
13c13
< -A FORWARD -i docker0 -o docker0 -j DROP
---
> -A FORWARD -i docker0 -o docker0 -j ACCEPT
```

范例:  在第二个宿主机上创建容器，跨宿主机的容器之间默认不能通信

```bash
[root@ubuntu1804 ~]#docker pull alpine
Using default tag: latest
latest: Pulling from library/alpine
c9b1b535fdd9: Pull complete
Digest: sha256:ab00606a42621fb68f2ed6ad3c88be54397f981a7b70a79db3d1172b11c4367d
Status: Downloaded newer image for alpine:latest
docker.io/library/alpine:latest
[root@ubuntu1804 ~]#docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED
STATUS              PORTS               NAMES
cab76bbb3db2        alpine              "sh"                About a minute ago
Up About a minute                       jolly_rosalind
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:6b:54:d3 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.101/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe6b:54d3/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:1d:73:8b:71 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
[root@ubuntu1804 ~]#docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED
STATUS              PORTS               NAMES
[root@ubuntu1804 ~]#docker run -it --rm  alpine sh
/ # ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
4: eth0@if5: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue
state UP
link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
valid_lft forever preferred_lft forever
/ # ping -c 1 172.17.0.3
PING 172.17.0.3 (172.17.0.3): 56 data bytes
--- 172.17.0.3 ping statistics ---
1 packets transmitted, 0 packets received, 100% packet loss
```

### 修改默认docker0网桥的网络配置

默认docker后会自动生成一个docker0的网桥,使用的IP是172.17.0.1/16,可能和宿主机的网段发生冲突, 可以将其修改为其它网段的地址,避免冲突

范例: 将docker0的IP修改为指定IP

```json
#方法1
[root@ubuntu1804 ~]#vim /etc/docker/daemon.json
[root@ubuntu1804 ~]#cat /etc/docker/daemon.json
{
"bip": "192.168.100.1/24",
"registry-mirrors": ["https://si7y70hh.mirror.aliyuncs.com"]
}
[root@ubuntu1804 ~]#systemctl restart docker.service
#方法2
[root@ubuntu1804 ~]#vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
--bip=192.168.100.1/24
[root@ubuntu1804 ~]#systemctl daemon-reload
[root@ubuntu1804 ~]#systemctl restart docker.service
#注意两种方法不可混用,否则将无法启动docker服务
#验证结果
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:48:f0:a2 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe48:f0a2/64 scope link
valid_lft forever preferred_lft forever
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:c5:a7:cf:5c brd ff:ff:ff:ff:ff:ff
inet 192.168.100.1/24 brd 192.168.100.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:c5ff:fea7:cf5c/64 scope link
valid_lft forever preferred_lft forever
```

### 修改默认网络设置使用自定义网桥

新建容器默认使用docker0的网络配置,可以修改默认指向自定义的网桥网络

范例:  用自定义的网桥代替默认的docker0

```bash
#查看默认网络
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:40:27:06 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe40:2706/64 scope link
valid_lft forever preferred_lft forever
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:35:ba:e7:ce brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:35ff:feba:e7ce/64 scope link
valid_lft forever preferred_lft forever
[root@ubuntu1804 ~]#apt -y install bridge-utils
[root@ubuntu1804 ~]#brctl addbr br0
#给网桥添加IP，用于给容器分配置IP，如果不指定IP，会自动向后续网段，默认是172.18.0.0/16
[root@ubuntu1804 ~]#ip a a 192.168.100.1/24 dev br0
[root@ubuntu1804 ~]#brctl  show
bridge name bridge id       STP enabled interfaces
br0     8000.000000000000   no
docker0     8000.024235bae7ce   no
[root@ubuntu1804 ~]#ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group
default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
group default qlen 1000
link/ether 00:0c:29:40:27:06 brd ff:ff:ff:ff:ff:ff
inet 10.0.0.100/24 brd 10.0.0.255 scope global eth0
valid_lft forever preferred_lft forever
inet6 fe80::20c:29ff:fe40:2706/64 scope link
valid_lft forever preferred_lft forever
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state
DOWN group default
link/ether 02:42:35:ba:e7:ce brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
valid_lft forever preferred_lft forever
inet6 fe80::42:35ff:feba:e7ce/64 scope link
valid_lft forever preferred_lft forever
18: br0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
group default qlen 1000
link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
inet 192.168.100.1/24 scope global br0
valid_lft forever preferred_lft forever
inet6 fe80::9cf2:e0ff:fe4e:96b3/64 scope link
valid_lft forever preferred_lft forever
[root@ubuntu1804 ~]#vim /lib/systemd/system/docker.service
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
-b br0
[root@ubuntu1804 ~]#systemctl daemon-reload
[root@ubuntu1804 ~]#systemctl restart docker
[root@ubuntu1804 ~]#ps -ef |grep dockerd
root      15773      1  0 11:12 ?        00:00:00 /usr/bin/dockerd -H fd:// --
containerd=/run/containerd/containerd.sock -b br0
root      15960   2300  0 11:14 pts/0    00:00:00 grep --color=auto dockerd
[root@ubuntu1804 ~]#docker run  -it alpine sh
/ #hostname -i
192.168.100.2
/ # ping www.baidu.com
PING www.baidu.com (220.181.38.150): 56 data bytes
64 bytes from 220.181.38.150: seq=0 ttl=127 time=4.028 ms
[root@ubuntu1804 ~]#
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/13-data-volume-containers.html' | relative_url }}">← Previous: Data Volume Containers</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/15-container-name-networking.html' | relative_url }}">Next: Container Name Networking →</a>
</nav>
