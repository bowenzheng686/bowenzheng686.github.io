---
layout: default
title: 'KVM 虚拟化 · 网络管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 04 章 · 网络管理

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 4.1 网络基础

### 基础知识

#### 网络模型

kvm类型的虚拟机，默认情况下使用的是nat网络，同一网络模型下创建的多虚拟机之间可以彼此通信，这种网络模型与外界网络进行通信依赖于nat服务，nat服务正常的话，该模型的网络是通过数据包的转换来达到通信的效果的，在网络流量比较大的场景下，该模式的网络模型会成为虚拟机的瓶颈。生产中我们一般采用桥接的网络模型，这种模型是借助于宿主机的网卡设备，直接与外网进行通信，效果很好。

![原文插图（第 97 页）]({{ '/subjects/KVM/assets/p097-img01.png' | relative_url }})

#### 配置流程

对于kvm来说，它有两种网络：永久网络和临时网络

- 前提：保证宿主机网络正常，网络服务使用network
- 首先：生成新的桥接设备
- 其次：关联桥设备和物理网卡设备
- 然后：清空物理网卡地址，启用桥设备地址，设置网络网关为桥设备地址
- 最后：虚拟机使用桥设备

### 简单实践

#### 基本配置

**查看kvm的网络配置目录**

````console
[root@kvm-host ~]# tree /etc/libvirt/qemu/networks/
/etc/libvirt/qemu/networks/
├── autostart
│ └── default.xml -> ../default.xml
└── default.xml
1 directory, 2 files
````

**查看虚拟网络**

````console
[root@kvm-host ~]# ifconfig
。。。
````

````text
virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet 198.18.122.1 netmask 255.255.255.0 broadcast 198.18.122.255
        ether 02:00:00:00:00:04 txqueuelen 1000 (Ethernet)
        RX packets 185 bytes 13811 (13.4 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 120 bytes 12842 (12.5 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
vnet1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet6 fe80::fc54:ff:fea1:6008 prefixlen 64 scopeid 0x20<link>
        ether 02:00:00:00:00:09 txqueuelen 1000 (Ethernet)
        RX packets 117 bytes 10411 (10.1 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 223 bytes 17382 (16.9 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
````

**查看所有网络相关命令**

````console
[root@kvm-host ~]# virsh -h | grep net-
    net-autostart 自动开始网络
    net-create 从一个 XML 文件创建一个网络
    net-define 定义不活跃的持久性虚拟网络，或者从 XML 文件中修改现有
的持久性虚拟网络
    net-desc show or set network's description or title
    net-destroy 销毁（停止）网络
    net-dhcp-leases 打印给定网络的租期信息
    net-dumpxml XML 中的网络信息
    net-edit 为网络编辑 XML 配置
    net-event 网络事件
    net-info 网络信息
    net-list 列出网络
    net-metadata show or set network's custom XML metadata
    net-name 把一个网络UUID 转换为网络名
    net-start 启动一个(以前定义的)不活跃的网络
    net-undefine 取消持久性网络的定义
    net-update 更新现有网络配置的部分
    net-uuid 把一个网络名转换为网络UUID
    net-port-list 列出网络端口
    net-port-create 从 XML 文件创建网络端口
    net-port-dumpxml XML 中的网络端口信息
    net-port-delete 删除指定的网络端口
````

#### 网络信息

**查看网络列表**

````console
[root@kvm-host ~]# virsh net-list
 名称 状态 自动开始 持久
-----------------------------------
 default 活动 是 是
[root@kvm-host ~]# virsh net-list --all
 名称 状态 自动开始 持久
-----------------------------------
 default 活动 是 是
````

**查看网络信息**

````console
[root@kvm-host ~]# virsh net-info default
名称： default
UUID: 00000000-0000-4000-8000-000000000007
活跃： 是
持久： 是
自动启动： 是
桥接： virbr0
````

**查看网络配置**

````console
[root@kvm-host ~]# virsh net-dumpxml default
<network connections='1'>
  <name>default</name>
  <uuid>00000000-0000-4000-8000-000000000007</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='02:00:00:00:00:04'/>
  <ip address='198.18.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='198.18.122.2' end='198.18.122.254'/>
    </dhcp>
  </ip>
</network>
````

## 4.2 网络操作

### 基础知识

**需求**

如果我们不想用默认的网络的话，可以自己定义一个专用的网络。

**命令解析**

````text
创建网络
    临时：virsh net-create <xml配置文件>
    永久：virsh net-define <xml配置文件>
关闭网络
virsh net-destroy <网络名称>
开启网络
virsh net-start <网络名称>
删除网络
virsh net-undefine <网络名称>
````

### 网络实践

#### 临时网络

##### 定制配置文件

**设置配置文件**

````console
[root@kvm-host ~]# cd /etc/libvirt/qemu/networks/
[root@kvm-host networks]# ls
autostart default.xml
[root@kvm-host networks]# cp default.xml gavin-linshi.xml
````

**定制配置**

````console
[root@kvm-host networks]# vim gavin-linshi.xml
[root@kvm-host networks]# cat gavin-linshi.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh net-edit default
or other application using the libvirt API.
-->
<network>
  <name>gavin-linshi</name> # 名字修改
  <uuid>00000000-0000-4000-8000-000000000008</uuid> # id修改
  <forward mode='nat'/>
  <bridge name='virbr1' stp='on' delay='0'/> # 名字修改为virbr1
  <mac address='02:00:00:00:00:03'/> # mac修改
  <ip address='198.18.123.1' netmask='255.255.255.0'> # ip网段修改
    <dhcp>
      <range start='198.18.123.2' end='198.18.123.254'/> # ip段修改
    </dhcp>
  </ip>
</network>
````

##### 创建网络

**创建临时网络**

````console
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
-----------------------------------
 default 活动 是 是
[root@kvm-host networks]# vim gavin-linshi.xml
[root@kvm-host networks]# virsh net-create gavin-linshi.xml
从gavin-linshi创建网络gavin-linshi.xml
````

查看效果,创建的是一个临时的网络

````console
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
-----------------------------------------
 default 活动 是 是
 gavin-linshi 活动 否 否
[root@kvm-host networks]# virsh net-list --transient
 名称 状态 自动开始 持久
-----------------------------------------
 gavin-linshi 活动 否 否
````

**确认网络**

````console
[root@kvm-host networks]# ifconfig
。。。
virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet 198.18.122.1 netmask 255.255.255.0 broadcast 198.18.122.255
        ether 02:00:00:00:00:04 txqueuelen 1000 (Ethernet)
        RX packets 224 bytes 16199 (15.8 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 157 bytes 15596 (15.2 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
virbr1: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
        inet 198.18.123.1 netmask 255.255.255.0 broadcast 198.18.123.255
        ether 02:00:00:00:00:03 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
vnet1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet6 fe80::fc54:ff:fea1:6008 prefixlen 64 scopeid 0x20<link>
        ether 02:00:00:00:00:09 txqueuelen 1000 (Ethernet)
        RX packets 156 bytes 13345 (13.0 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 461 bytes 30624 (29.9 KiB)
````

TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0

#### 永久网络

##### 定制配置文件

**设置配置文件**

````console
[root@kvm-host ~]# cd /etc/libvirt/qemu/networks/
[root@kvm-host networks]# ls
autostart default.xml gavin-linshi.xml
[root@kvm-host networks]# cp default.xml gavin-yongjiu.xml
````

**定制配置**

````console
[root@kvm-host networks]# vim gavin-yongjiu.xml
[root@kvm-host networks]# cat gavin-yongjiu.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh net-edit default
or other application using the libvirt API.
-->
<network>
  <name>gavin-yongjiu</name>
  <uuid>00000000-0000-4000-8000-000000000009</uuid>
  <forward mode='nat'/>
  <bridge name='virbr2' stp='on' delay='0'/>
  <mac address='02:00:00:00:00:02'/>
  <ip address='198.18.124.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='198.18.124.2' end='198.18.124.254'/>
    </dhcp>
  </ip>
</network>
````

##### 创建永久网络

**查看网络效果**

````console
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
-----------------------------------------
 default 活动 是 是
 gavin-linshi 活动 否 否
````

**定义永久网络**

````console
[root@kvm-host networks]# virsh net-define gavin-yongjiu.xml
从 gavin-yongjiu定义网络gavin-yongjiu.xml
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
--------------------------------------------
 default 活动 是 是
 gavin-linshi 活动 否 否
 gavin-yongjiu 不活跃 否 是
````

**启动网络**

````console
[root@kvm-host networks]# virsh net-start gavin-yongjiu
网络 gavin-yongjiu 已开始
````

**查看效果**

````console
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
------------------------------------------
 default 活动 是 是
 gavin-linshi 活动 否 否
 gavin-yongjiu 活动 否 是
[root@kvm-host networks]# virsh net-list --persistent
 名称 状态 自动开始 持久
------------------------------------------
 default 活动 是 是
 gavin-yongjiu 活动 否 是
````

**查看网卡**

````console
[root@kvm-host networks]# ifconfig
...
virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet 198.18.122.1 netmask 255.255.255.0 broadcast 198.18.122.255
        ether 02:00:00:00:00:04 txqueuelen 1000 (Ethernet)
        RX packets 251 bytes 17771 (17.3 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 184 bytes 17546 (17.1 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
virbr1: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
        inet 198.18.123.1 netmask 255.255.255.0 broadcast 198.18.123.255
        ether 02:00:00:00:00:03 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
virbr2: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
````

````text
        inet 198.18.124.1 netmask 255.255.255.0 broadcast 198.18.124.255
        ether 02:00:00:00:00:02 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
vnet1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet6 fe80::fc54:ff:fea1:6008 prefixlen 64 scopeid 0x20<link>
        ether 02:00:00:00:00:09 txqueuelen 1000 (Ethernet)
        RX packets 183 bytes 15295 (14.9 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 641 bytes 40530 (39.5 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
````

#### 关闭和开启

**关闭实践**

**停止网络**

````console
[root@kvm-host networks]# virsh net-destroy default
网络 default 被删除
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
--------------------------------------------
 default 不活跃 是 是
 gavin-linshi 活动 否 否
 gavin-yongjiu 活动 否 是
[root@kvm-host networks]# ls
autostart default.xml gavin-linshi.xml gavin-yongjiu.xml
````

**开启实践**

````console
[root@kvm-host networks]# virsh net-start default
网络 default 已开始
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
------------------------------------------
 default 活动 是 是
 gavin-linshi 活动 否 否
 gavin-yongjiu 活动 否 是
````

#### 删除实践

删除网络需要有两步：取消注册+关闭网络

##### 关闭网络

**关闭网络**

````console
[root@kvm-host networks]# virsh net-undefine default
网络 default 已经被取消定义
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
------------------------------------------
 default 活动 否 否
 gavin-linshi 活动 否 否
 gavin-yongjiu 活动 否 是
配置文件已经被清理掉了
[root@kvm-host networks]# ls /etc/libvirt/qemu/networks
autostart gavin-linshi.xml gavin-yongjiu.xml
````

##### 删除网络

**删除网络**

````console
[root@kvm-host networks]# virsh net-destroy default
网络 default 被删除
查看效果
[root@kvm-host networks]# virsh net-list --all
 名称 状态 自动开始 持久
------------------------------------------
 gavin-linshi 活动 否 否
 gavin-yongjiu 活动 否 是
````

##### 确认效果

查看网络,virbr0 网卡被清理掉了

````console
[root@kvm-host networks]# ifconfig
...
virbr1: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
        inet 198.18.123.1 netmask 255.255.255.0 broadcast 198.18.123.255
        ether 02:00:00:00:00:03 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
virbr2: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
        inet 198.18.124.1 netmask 255.255.255.0 broadcast 198.18.124.255
````

````text
        ether 02:00:00:00:00:02 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
vnet1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        ether 02:00:00:00:00:09 txqueuelen 1000 (Ethernet)
        RX packets 202 bytes 16477 (16.0 KiB)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 660 bytes 41766 (40.7 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
````

虽然virbr0网卡被清理掉了，但是运行中的虚拟机的网络依然是看到网卡的信息，只不过是无法访问网络了

![原文插图（第 106 页）]({{ '/subjects/KVM/assets/p106-img01.png' | relative_url }})

## 4.3 自定义网络

### 准备工作

#### 基本信息查看

**命令帮助**

````console
[root@kvm-host ~]# brctl --help
Usage: brctl [commands]
commands:
        addbr <bridge> add bridge
        delbr <bridge> delete bridge
        addif <bridge> <device> add interface to bridge
        delif <bridge> <device> delete interface from bridge
        hairpin <bridge> <port> {on|off} turn hairpin on/off
        setageing <bridge> <time> set ageing time
        setbridgeprio <bridge> <prio> set bridge priority
        setfd <bridge> <time> set bridge forward delay
        sethello <bridge> <time> set hello time
        setmaxage <bridge> <time> set max message age
        setpathcost <bridge> <port> <cost> set path cost
        setportprio <bridge> <port> <prio> set port priority
        show [ <bridge> ] show a list of bridges
        showmacs <bridge> show a list of mac addrs
        showstp <bridge> show bridge stp info
        stp <bridge> {on|off} turn stp on/off
````

**查看网络基本信息**

**查看ip地址信息**

````console
[root@kvm-host ~]# ip addr
...
5: vnet1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
group default qlen 1000
    link/ether 02:00:00:00:00:09 brd ff:ff:ff:ff:ff:ff
6: virbr1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
group default qlen 1000
    link/ether 02:00:00:00:00:03 brd ff:ff:ff:ff:ff:ff
    inet 198.18.123.1/24 brd 198.18.123.255 scope global virbr1
       valid_lft forever preferred_lft forever
7: virbr2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
group default qlen 1000
    link/ether 02:00:00:00:00:02 brd ff:ff:ff:ff:ff:ff
    inet 198.18.124.1/24 brd 198.18.124.255 scope global virbr2
       valid_lft forever preferred_lft forever
查看路由信息
[root@kvm-host ~]# route -n
Kernel IP routing table
Destination Gateway Genmask Flags Metric Ref Use Iface
0.0.0.0 192.0.2.2 0.0.0.0 UG 100 0 0 ens160
192.0.2.0 0.0.0.0 255.255.255.0 U 100 0 0 ens160
198.18.123.0 0.0.0.0 255.255.255.0 U 0 0 0 virbr1
198.18.124.0 0.0.0.0 255.255.255.0 U 0 0 0 virbr2
````

#### 准备工作

安装桥操作工具：bridge-utils

**Ubuntu系统**

````bash
apt install bridge-utils -y
apt-file list bridge-utils
centos系统
yum install bridge-utils
````

**dns解析**

````console
[root@kvm-host ~]# grep namese /etc/resolv.conf
nameserver 192.0.2.2
````

**查看当前主机的桥接状态**

````console
[root@kvm-host ~]# brctl show
bridge name bridge id STP enabled interfaces
virbr1 8000.5254006b688d yes
virbr2 8000.5254006b687d yes
````

### 桥接环境

#### 手工实践

**创建桥接网卡设备**

````console
[root@kvm-host ~]# brctl addbr br0
[root@kvm-host ~]# brctl stp br0 on
[root@kvm-host ~]# brctl show
bridge name bridge id STP enabled interfaces
br0 8000.000000000000 yes
virbr1 8000.5254006b688d yes
virbr2 8000.5254006b687d yes
````

**删除物理网卡的ip地址**

````console
[root@kvm-host ~]# ifconfig ens160 0 up
````

**关联桥接设备和物理网卡设备**

````console
[root@kvm-host ~]# brctl addif br0 ens160
````

**给桥接网卡配置ip地址并启动**

````console
[root@kvm-host ~]# ifconfig br0 192.0.2.12/24 up
````

**给桥接网卡配置路由**

````console
[root@kvm-host ~]# route add default gw 192.0.2.2
注意：
    操作br0的另一种方法是 ip set dev br0 up/down
````

#### 脚本实践

##### 脚本内容

如果将命令分开执行的话，则会在关联桥接网卡和物理网卡的时候造成断网现象，所以建议将这几条命令同时执行或者使用脚本执行命令

````console
[root@kvm-host ~]# vim bridge_setup_function.sh
#!/bin/bash
````

````bash
# *************************************
# * 功能: 脚本方式定制虚拟网卡
# *************************************
# 定义网桥名称
BRIDGE_NAME="br0"
# 定义网络接口名称
INTERFACE_NAME="ens160"
# 定义网桥的 IP 地址
BRIDGE_IP="192.0.2.12/24"
# 定义默认网关
DEFAULT_GATEWAY="192.0.2.2"
# 检查命令是否可用
check_command() {
    local cmd=$1
    if ! command -v "$cmd" &> /dev/null
    then
        echo "$cmd 命令未找到，请安装相关包。"
        exit 1
    fi
}
# 创建网桥
create_bridge() {
    if brctl addbr "$BRIDGE_NAME" 2>/dev/null; then
        echo "成功创建网桥 $BRIDGE_NAME"
    else
        echo "创建网桥 $BRIDGE_NAME 失败"
        cleanup
        exit 1
    fi
}
# 开启网桥的生成树协议
enable_stp() {
    if brctl stp "$BRIDGE_NAME" on 2>/dev/null; then
        echo "成功开启 $BRIDGE_NAME 的生成树协议"
    else
        echo "开启 $BRIDGE_NAME 的生成树协议失败"
        cleanup
        exit 1
    fi
}
# 关闭网络接口的 IP 地址并启动接口
prepare_interface() {
    if ifconfig "$INTERFACE_NAME" 0 up 2>/dev/null; then
        echo "成功关闭 $INTERFACE_NAME 的 IP 地址并启动接口"
    else
        echo "关闭 $INTERFACE_NAME 的 IP 地址并启动接口失败"
        cleanup
        exit 1
````

````bash
    fi
}
# 将网络接口添加到网桥
add_interface_to_bridge() {
    if brctl addif "$BRIDGE_NAME" "$INTERFACE_NAME" 2>/dev/null; then
        echo "成功将 $INTERFACE_NAME 添加到 $BRIDGE_NAME"
    else
        echo "将 $INTERFACE_NAME 添加到 $BRIDGE_NAME 失败"
        cleanup
        exit 1
    fi
}
# 为网桥设置 IP 地址并启动网桥
configure_bridge_ip() {
    if ifconfig "$BRIDGE_NAME" "$BRIDGE_IP" up 2>/dev/null; then
        echo "成功为 $BRIDGE_NAME 设置 IP 地址 $BRIDGE_IP 并启动网桥"
    else
        echo "为 $BRIDGE_NAME 设置 IP 地址 $BRIDGE_IP 并启动网桥失败"
        cleanup
        exit 1
    fi
}
# 添加默认网关
add_default_gateway() {
    if route add default gw "$DEFAULT_GATEWAY" 2>/dev/null; then
        echo "成功添加默认网关 $DEFAULT_GATEWAY"
    else
        echo "添加默认网关 $DEFAULT_GATEWAY 失败"
        cleanup
        exit 1
    fi
}
# 清理操作
cleanup() {
    brctl delbr "$BRIDGE_NAME" 2>/dev/null
}
# 主函数
main() {
    check_command "brctl"
    create_bridge
    enable_stp
    prepare_interface
    add_interface_to_bridge
    configure_bridge_ip
    add_default_gateway
    echo "网桥配置完成"
}
# 执行主函数
main
````

##### 执行脚本

执行脚本的过程中，会出现网络中断

````console
[root@kvm-host ~]# /bin/bash bridge_setup_function.sh
成功创建网桥 br0
成功开启 br0 的生成树协议
Network error: Software caused connection abort
─────────────────────────────────────────────────────────────────────────────────
───────
Session stopped
    - Press <return> to exit tab
    - Press R to restart session
    - Press S to save terminal output to file
````

稍等5秒钟之后，尝试按 R 重新连接，查看效果

````text
     ┌────────────────────────────────────────────────────────────────────┐
     │ • MobaXterm 20.2 • │
     │ (SSH client, X-server and networking tools) │
     │ │
     │ ➤ SSH session to root@192.0.2.12 │
     │ • SSH compression : ✔ │
     │ • SSH-browser : ✔ │
     │ • X11-forwarding : ✔ (remote display is forwarded through SSH) │
     │ • DISPLAY : ✔ (automatically set on remote server) │
     │ │
     │ ➤ For more info, ctrl+click on help or visit our website │
     └────────────────────────────────────────────────────────────────────┘
Activate the web console with: systemctl enable --now cockpit.socket
Last login: Wed Mar 26 21:29:52 2025 from 192.0.2.1
[root@kvm-host ~]#
````

**查看新的网络网卡配置**

````console
[root@kvm-host ~]# ip a
...
# ens160 已经没有网卡信息了
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq master br0 state
UP group default qlen 1000
    link/ether 02:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    altname enp3s0
    inet6 fe80::250:56ff:fe38:d5d0/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
5: vnet1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN
group default qlen 1000
    link/ether 02:00:00:00:00:09 brd ff:ff:ff:ff:ff:ff
````

````text
6: virbr1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
group default qlen 1000
    link/ether 02:00:00:00:00:03 brd ff:ff:ff:ff:ff:ff
    inet 198.18.123.1/24 brd 198.18.123.255 scope global virbr1
       valid_lft forever preferred_lft forever
7: virbr2: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
group default qlen 1000
    link/ether 02:00:00:00:00:02 brd ff:ff:ff:ff:ff:ff
    inet 198.18.124.1/24 brd 198.18.124.255 scope global virbr2
       valid_lft forever preferred_lft forever
# br0应用的是 ens160之前的网卡信息
11: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group
default qlen 1000
    link/ether 02:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    inet 192.0.2.12/24 brd 192.0.2.255 scope global br0
       valid_lft forever preferred_lft forever
    inet6 fe80::250:56ff:fe38:d5d0/64 scope link
       valid_lft forever preferred_lft forever
````

**确认桥接设备信息**

````console
[root@kvm-host ~]# brctl show
bridge name bridge id STP enabled interfaces
br0 8000.00505638d5d0 yes ens160
virbr1 8000.5254006b688d yes
virbr2 8000.5254006b687d yes
````

### 使用设备

#### 应用网卡设备

**查看虚拟机的网卡默认配置**

````bash
virsh edit CentOS-7-x86_64
````

**修改虚拟机的网卡配置**

````console
[root@kvm-host ~]# virsh edit CentOS-7-x86_64
域'CentOS-7-x86_64' XML 配置已被编辑。
# 源内容
    <interface type='network'>
      <mac address='02:00:00:00:00:07'/>
      <source network='default'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
# 修改后内容
    <interface type='bridge'>
      <mac address='02:00:00:00:00:07'/>
````

````xml
      <source bridge='br0'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
注意：
    修改了三处地方：
        type后面的network修改为了bridge
        source后面的network修改为了bridge,network后面的default修改为了br0
````

**重启虚拟机**

````console
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
------------------------------
 - CentOS-7-x86_64 关闭
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
````

#### 连接VM

##### 连接虚拟机

方法1：通过vnc连接到虚拟机

因为默认的虚拟机使用的是nat模型，而net模型有专用的dnsmasq软件提供dns服务，我们现在使用桥接模型，所以我们需要自己来设置虚拟机的网卡信息。

方法2：通过console连接虚拟机

````console
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Wed Mar 26 20:58:27 on tty1
[root@localhost ~]#
````

##### 配置网络

因为我们的本地DHCP能力是正常的，所以vm主机启动后，会自动分配一个ip地址

**查看虚拟机网络信息**

````console
[root@localhost ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP
group default qlen 1000
    link/ether 02:00:00:00:00:07 brd ff:ff:ff:ff:ff:ff
    inet 192.0.2.140/24 brd 192.0.2.255 scope global noprefixroute dynamic eth0
       valid_lft 1728sec preferred_lft 1728sec
    inet6 fe80::daa6:18a2:ae68:8186/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
````

**测试网络联通**

````console
[root@localhost ~]# ping -c1 www.baidu.com
PING www.a.shifen.com (180.101.49.44) 56(84) bytes of data.
64 bytes from 180.101.49.44 (180.101.49.44): icmp_seq=1 ttl=128 time=24.2 ms
--- www.a.shifen.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 24.261/24.261/24.261/0.000 ms
````

##### 定制网络

如果默认的dhcp不喜欢的话，可以编辑网卡配置

````console
[root@localhost ~]# vim /etc/sysconfig/network-scripts/ifcfg-eth0
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
TYPE="Ethernet"
PROXY_METHOD="none"
BROWSER_ONLY="no"
BOOTPROTO="none"
DEFROUTE="yes"
IPV4_FAILURE_FATAL="no"
NAME="eth0"
UUID="00000000-0000-4000-8000-000000000006"
DEVICE="eth0"
ONBOOT="yes"
IPADDR="192.0.2.200"
NETMASK=255.255.255.0
GATEWAY=192.0.2.2
DNS=192.0.2.2
````

**重启网络**

````console
[root@localhost ~]# service network restart
Restarting network (via systemctl): [ 确定 ]
[root@localhost ~]# ip a s eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP
group default qlen 1000
    link/ether 02:00:00:00:00:07 brd ff:ff:ff:ff:ff:ff
    inet 192.0.2.200/24 brd 192.0.2.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fea1:6008/64 scope link
       valid_lft forever preferred_lft forever
````

##### 网络功能测试

**定制dns环境**

````console
[root@localhost ~]# cat /etc/resolv.conf
# Generated by NetworkManager
nameserver 192.0.2.2
测试网络
[root@localhost ~]# ping www.baidu.com -c1
PING www.a.shifen.com (180.101.49.44) 56(84) bytes of data.
64 bytes from 180.101.49.44 (180.101.49.44): icmp_seq=1 ttl=128 time=24.1 ms
--- www.a.shifen.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 24.173/24.173/24.173/0.000 ms
````

宿主机连接虚拟机，可以正常联通

````console
[root@kvm-host ~]# ssh root@192.0.2.200
The authenticity of host '192.0.2.200 (192.0.2.200)' can't be established.
ED25519 key fingerprint is SHA256:LuAC3WTX+gjlRAPZeVejVEljaxui2LRUJE8V64jMFzY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.0.2.200' (ED25519) to the list of known hosts.
root@192.0.2.200's password:
Last login: Wed Mar 26 21:39:00 2025
[root@localhost ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP
group default qlen 1000
    link/ether 02:00:00:00:00:07 brd ff:ff:ff:ff:ff:ff
    inet 192.0.2.200/24 brd 192.0.2.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
````

````text
    inet6 fe80::5054:ff:fea1:6008/64 scope link
       valid_lft forever preferred_lft forever
````

#### 问题解析

##### selinux问题

**常见报错：**

````text
错误：开始域 gavin-web 失败
错误：不支持的配置：Unable to find security driver for model selinux
````

**解决办法：**

将虚拟机中的"<seclabel type='dynamic' model='selinux' relabel='yes'/>" 删除即可

##### Centos8问题

centos8环境下重启网络的命令有些繁琐，不能使用 systemctl restart network

````bash
nmcli c reload
nmcli c up eth0
nmcli d reapply eth0
nmcli d connect eth0
````

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/03-storage-management.html' | relative_url }}">← 上一章：存储管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/05-image-management.html' | relative_url }}">下一章：镜像管理 →</a>
</nav>
