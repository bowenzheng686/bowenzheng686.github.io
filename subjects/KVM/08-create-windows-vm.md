---
layout: default
title: 'KVM 虚拟化 · 创建 Windows 虚拟机'
subject_page: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 08 章 · 创建 Windows 虚拟机

> 公开版已将实验密码、主机标识和网络地址替换为示例值，并省略可能包含环境信息的原始截图。执行命令前请按实际环境调整。

## 3.2.1 准备工作

### 3.2.1.1 资源获取

**获取资源**

**VirtIO 下载地址：**
https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/
**VirtIO 历史版本下载地址：**
https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/

**注意:** 建议下载virtio-win-0.1.141版本，


可以检索 latest-virtio 和 stable-virtio

**获取稳定版本**

https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.141-1/virtio-win-0.1.141.iso https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.266-1/virtio-win-0.1.266.iso

**注意：**

141 版本，支持的windows最低版本为 2008的服务器版本 266 版本，支持的windows最低版本为 2016的服务器版本

### 3.2.1.2 virtio定位

在 KVM 中创建 Windows 虚拟机时，VirtIO 是一套由 Red Hat 开发的开源虚拟化驱动程序和设备规范，主要作用是优化虚拟机与宿主机之间的 I/O 性能，解决传统虚拟化中 “模拟设备” 效率低下的问题。

1 KVM 作为 Type-1 虚拟化技术，宿主机内核直接提供虚拟化支持。但 Windows 系统默认没有针对 KVM 的原生驱动

若不使用 VirtIO，虚拟机只能通过 KVM 模拟的 “标准硬件设备”（如 Intel E1000 网卡、IDE 硬盘控制器等）与宿主机交互。这些模拟设备的兼容性好，但性能差（模拟过程会消耗大量 CPU 资源，且 I/O 延迟高）。

**VirtIO 采用 “半虚拟化” 模式：**

宿主机提供专门的 VirtIO 虚拟设备（如 VirtIO 网卡、VirtIO 块设备）；虚拟机中安装 VirtIO 驱动后，可直接与宿主机的 VirtIO 设备通信，跳过冗余的硬件模拟环节，大幅提升磁盘 I/O、网络传输等性能（尤其是高负载场景下）。

2 Windows 系统默认不包含 KVM 虚拟设备的驱动，若直接在 KVM 中安装 Windows，可能出现磁盘无法识别、网卡无法识别等问题。VirtIO 为 Windows 虚拟机提供了多种核心虚拟设备的驱动，从而解决 Windows 对 KVM 的兼容性问题

**VirtIO 块设备驱动：**

优化虚拟机磁盘（如 QCOW2、RAW 镜像）的读写性能，替代传统的 IDE/SATA 模拟驱动。

**VirtIO 网卡驱动：**

提升网络吞吐量和响应速度，替代 E1000 等模拟网卡驱动。

**VirtIO 气球驱动（Balloon）：**

实现虚拟机内存的动态分配（宿主机可根据需求调整虚拟机的实际内存占用）。

**VirtIO 控制台驱动：**

支持虚拟机与宿主机的控制台交互（类似串口通信）。

因此，在 KVM 中部署 Windows 时，几乎都会使用 VirtIO 驱动（需在安装系统时手动加载），否则会面临性能瓶颈或设备无法识别的问题。

## 3.2.2 部署实践

### 3.2.2.1 创建虚拟机

**安装虚拟机**

````bash
[root@kvm-host ~]# cd /data/images/
[root@kvm-host images]# mv 14393.0.161119-
1705.RS1_REFRESH_SERVER_EVAL_X64FRE_ZH-CN.ISO
cn_windows_server_2016_x64_dvd_9718765.iso
[root@kvm-host images]# ls
CentOS-7-x86_64-Minimal-2009.iso cn_windows_server_2016_x64_dvd_9718765.iso
 virtio-win-0.1.266.iso
````

**创建虚拟机**

````bash
[root@kvm-host ~]# virt-install \
--os-variant=win2k16 --virt-type=kvm \
--name win2016 --ram 4096 --vcpus=2 \
--cdrom=/data/images/cn_windows_server_2016_x64_dvd_9718765.iso \
--network=bridge=br0,model=virtio \
--graphics vnc,listen=0.0.0.0 --noautoconsole \
````

````bash
--disk path=/opt/win2016.qcow2,size=20,bus=virtio,format=qcow2 \
--disk path=/data/images/virtio-win-0.1.266.iso,device=cdrom
开始安装......
正在分配 'win2016.qcow2' | 20 GB 00:00:00
创建域...... | 00:00:00
域仍在运行。安装可能正在进行中。
可以重新连接到控制台以完成安装过程。
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 4 win2008 运行
````

### 3.2.2.2 配置windows

#### 3.2.2.2.1 连接windows

**打开虚拟机管理工具**

````bash
[root@kvm-host ~]# virt-manager
````


**双击打开 win2008**


#### 3.2.2.2.2 选择语言




注意：该画面会持续20s左右

#### 3.2.2.2.3 选择图形版本


**点击下一步**


勾选 我接受许可条款，点击下一步

#### 3.2.2.2.4 选择安装方式



#### 3.2.2.2.5 确定驱动

**选择 加载驱动程序**


**点击浏览**


点击 virtio-win-0.1.266


找到amd64 下面的2k16，点击确定


点击下一步即可，该画面会持续 20s 左右，需要检测驱动是否正常


#### 3.2.2.2.6 安装系统

验证通过后，会出现如下画面


直接点击下一步即可，整个安装过程会持续9min 【第二步解压会持续7min左右】


安装完毕后，会直接关闭主机

### 3.2.2.3 配置windows

#### 3.2.2.3.1 启动vm

点击启动虚拟机，启动画面会持续 1min左右，会进行初始化环境


#### 3.2.2.3.2 基本配置

设定密码，不能太简单，W!@#$%^w


点击完成后，进入到画面


不要使用 键盘，传输快捷键解锁，通过 “发送按键” 来实现


发送按键后，查看效果


输入密码 W!@#$%^w ，进行登录


稍等10s钟，查看效果


#### 3.2.2.3.3 网络配置

目前的服务器的右下角可以看到 网卡 是红色的，原因是网卡的驱动没有识别出来。

点击 左下角，点击管理工具


点击计算机管理后，点击设备管理器



右键后，点击 更新驱动程序软件


**点击 浏览计算机以查找驱动程序软件**


点击浏览，


选中 E盘 virtio-win-0.1.266 即可，然后点击确定


确保 勾选 包括 子文件夹，然后点击下一步，稍等10s后，可以看到驱动自动安装完毕


安装完成后，稍等一下，网络就会出现了


点击 是即可，确认最后效果


以同样的方式安装其他的几个叹号设备即可，但是注意关于人体学输入设备处，即使我们安装完毕后，依然会出现黄色叹号


### 3.2.2.4 模版制作

#### 3.2.2.4.1 查看主机的sid

**每一台windows都有自己唯一的身份id信息**

命令：whoami/user


如果基于现有的镜像进行克隆的话，会导致所有的windows的sid都是相同的。

#### 3.2.2.4.2 去除主机的sid

进入到VM主机的 C:\Windows\System32\Sysprep 目录下，找到一个文件


**双击 sysprep 程序**


勾选 通用，然后关机选项 选择 关机。 这就意味着，我一旦关机后，当前主机的所有定制信息都会被清理掉，重启后，会生成新的主机身份信息。

点击确定后，查看效果


该过程会持续 1min左右，然后会自动关闭主机

#### 3.2.2.4.3 克隆windows主机

执行如下命令,该过程可能会持续7分钟，当然也看主机，有些主机可能只需要 几十秒

````bash
[root@kvm-host ~]# virt-clone -o win2016 -n win2016-2 -f /opt/win2016-2.qcow2
正在分配 'win2016-2.qcow2' 3% [= ] 496 MB/s | 707 MB
 00:00:39
正在分配 'win2016-2.qcow2' 3% [=- ] 417 MB/s | 814 MB
 00:00:47
正在分配 'win2016-2.qcow2' 3% [=- ] 333 MB/s | 814 MB
 00:00:58
...
正在分配 'win2016-2.qcow2' | 20 GB
 00:07:20
成功克隆 'win2016-2'。
````

**查看克隆后效果**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
----------------------------------
 - CentOS-7-clone 关闭
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-bak 关闭
 - win2016 关闭
 - win2016-2 关闭
````

#### 3.2.2.4.4 启动克隆windows主机

启动主机后，通过vnc查看效果，启动后的vm主机需要自定义信息了


<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/07-virtualization-principles.html' | relative_url }}">← 上一章：虚拟化原理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
</nav>
