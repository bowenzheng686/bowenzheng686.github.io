---
layout: default
title: 'KVM 虚拟化 · 镜像管理'
subject_page: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 05 章 · 镜像管理

> 公开版已将实验密码、主机标识和网络地址替换为示例值，并省略可能包含环境信息的原始截图。执行命令前请按实际环境调整。

## 5.1 磁盘基础

### 磁盘模式

根据存储数据方式的不同可以分为两种格式，一种是稀疏模式、一种是全镜像模式，全镜像模式无法做快照，IO层面是有qemu模拟的，CPU和内存是有KVM实现的

raw：

**指定多大就创建多大，直接占用指定大小的空间：**

老牌的格式了，性能上来说的话还是不错的。由于原生的裸格式，不支持snapshot。在虚拟机迁移方面还是有很大的限制。qcow2:是openstack默认也是比较推荐的格式，将差异保存在一个文件，文件比较小而且做快照也比较小，空间是动态增长的.现在比较主流的一种虚拟化镜像格式，支持快照功能。


### 确认模式

**查看虚拟机支持的磁盘格式种类**

````bash
[root@kvm-host ~]# qemu-img --help
qemu-img version 9.0.0 (qemu-kvm-9.0.0-10.el9_5.2)
Copyright (c) 2003-2024 Fabrice Bellard and the QEMU Project developers
usage: qemu-img [standard options] command [command options]
QEMU disk image utility
    '-h', '--help' display this help and exit
    '-V', '--version' output version information and exit
    '-T', '--trace' [[enable=]<pattern>][,events=<file>][,file=<file>]
                         specify tracing options
...
````

可以看到，qemu支持的磁盘种类很多

````text
Supported formats: blkdebug blklogwrites blkverify compress copy-before-write
copy-on-read file ftp ftps host_cdrom host_device http https io_uring luks nbd
null-aio null-co nvme nvme-io_uring preallocate qcow2 quorum raw rbd snapshot-
access throttle vdi vhdx virtio-blk-vfio-pci virtio-blk-vhost-user virtio-blk-
vhost-vdpa vmdk vpc
See <https://qemu.org/contribute/report-a-bug> for how to report bugs.
More information on the QEMU project at <https://qemu.org>.
````

## 5.2 功能实践

### 基本语法

**创建磁盘**

**创建磁盘**

````bash
    qemu-img create [-q] [-f fmt] [-o options] filename [size]
查看某个具体磁盘格式的帮助信息：
    qemu-img create -f qcow2 -o ? file.qcow
    注意：在“-o”选项中各个选项用逗号来分隔
````

**查看磁盘**

````bash
    qemu-img info 磁盘名称
````

**磁盘转换**

````bash
    qemu-img convert -f 原格式 旧磁盘名称 -O 转换后格式 新磁盘名称
````

### 创建磁盘

创建一个3G大小的raw格式的虚拟磁盘CentOS-7-x86_64.raw

**基本动作执行命令**

````bash
[root@kvm-host ~]# qemu-img create -f raw /opt/CentOS-7-x86_64-1.raw 3G
Formatting '/opt/CentOS-7-x86_64-1.raw', fmt=raw size=3221225472
确认效果
[root@kvm-host ~]# ls /opt/CentOS-7-x86_64-1.raw -lh
-rw-r--r-- 1 root root 3.0G 3月 26 21:55 /opt/CentOS-7-x86_64-1.raw
````

**创建一个基于前后端模式的qcow2的磁盘文件**

````bash
[root@kvm-host ~]# qemu-img create -f qcow2 -o
backing_file=/kvm/images/gavin.img test-1.qcow2 3G
qemu-img: test-1.qcow2: Backing file specified without backing format
Detected format of raw.
[root@kvm-host ~]# ll /kvm/images/gavin.img -h
-rw------- 1 root root 5.0G 3月 25 22:23 /kvm/images/gavin.img
注意：
    这里的容量为5G，根源追究 "2.1.3.1.5 容量变动" 一节
````

**确认效果**

````bash
[root@kvm-host ~]# ll /opt/ -lh
总用量 1.7G
-rw-r--r-- 1 root root 3.0G 3月 26 21:55 CentOS-7-x86_64-1.raw
-rw-r--r-- 1 qemu qemu 10G 3月 26 22:03 CentOS-7-x86_64.raw
````

**查看磁盘的基本信息**

````bash
[root@kvm-host ~]# qemu-img info /opt/CentOS-7-x86_64-1.raw
image: /opt/CentOS-7-x86_64-1.raw
file format: raw
virtual size: 3 GiB (3221225472 bytes)
disk size: 1 MiB
Child node '/file':
    filename: /opt/CentOS-7-x86_64-1.raw
    protocol type: file
    file length: 3 GiB (3221225472 bytes)
    disk size: 1 MiB
    Format specific information:
        extent size hint: 1048576
````

### 磁盘格式转换

raw磁盘转换qcow2, 注意：正在使用的磁盘无法转换

````bash
[root@kvm-host ~]# cd /opt/
[root@kvm-host opt]# ls
CentOS-7-x86_64-1.raw CentOS-7-x86_64.raw
格式转换
[root@kvm-host opt]# qemu-img convert -f raw CentOS-7-x86_64-1.raw -O qcow2
CentOS-7-x86_64-1.qcow2
````

**确认效果**

````bash
[root@kvm-host opt]# ll -h
总用量 1.7G
-rw-r--r-- 1 root root 193K 3月 26 22:07 CentOS-7-x86_64-1.qcow2
-rw-r--r-- 1 root root 3.0G 3月 26 21:55 CentOS-7-x86_64-1.raw
-rw-r--r-- 1 qemu qemu 10G 3月 26 22:03 CentOS-7-x86_64.raw
````

### 空磁盘实践

刚才我们生成了一个新的磁盘，现在虚拟机使用新的磁盘

**关闭虚拟机**

````bash
[root@kvm-host opt]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host opt]# virsh list --all
 Id 名称 状态
------------------------------
 - CentOS-7-x86_64 关闭
````

**编辑vm配置**

````bash
[root@kvm-host opt]# virsh edit CentOS-7-x86_64
域'CentOS-7-x86_64' XML 配置已被编辑。
# 源内容
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/opt/CentOS-7-x86_64.raw'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
# 替换后内容
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/> # type更改为qcow2
      <source file='/opt/CentOS-7-x86_64-1.qcow2'/> # 文件名修改
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
````

**启动虚拟机**

````bash
[root@kvm-host opt]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
注意：由于是一个新的磁盘，所以系统在启动的时候，会导致失败，效果如下
````


### 非空磁盘实践

**格式转换**

````bash
[root@kvm-host opt]# qemu-img convert -f raw CentOS-7-x86_64.raw -O qcow2
CentOS-7-x86_64.qcow2
````

**检查效果**

````bash
[root@kvm-host opt]# qemu-img convert -f raw CentOS-7-x86_64.raw -O qcow2
CentOS-7-x86_64.qcow2
[root@kvm-host opt]# ll -h
总用量 3.2G
-rw-r--r-- 1 qemu qemu 193K 3月 26 22:07 CentOS-7-x86_64-1.qcow2
-rw-r--r-- 1 root root 3.0G 3月 26 21:55 CentOS-7-x86_64-1.raw
-rw-r--r-- 1 root root 1.6G 3月 26 22:16 CentOS-7-x86_64.qcow2
-rw-r--r-- 1 root root 10G 3月 26 22:11 CentOS-7-x86_64.raw
````

**关闭vm**

````bash
[root@kvm-host opt]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
注意：一定要确认一下，是否真的关闭了
````

**修改配置**

````bash
[root@kvm-host opt]# virsh edit CentOS-7-x86_64
# 修改后内容如下
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/opt/CentOS-7-x86_64.qcow2'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
````

**启动虚拟机**

````bash
[root@kvm-host opt]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host opt]# virsh list
 Id 名称 状态
------------------------------
 5 CentOS-7-x86_64 运行
````

**查看登录效果**


## 5.3 克隆

### 基础知识

**需求**

在某些特殊场景下，我们需要批量安装多台虚拟机，目前我们学习的虚拟机安装的方式是逐一的，效率太低了，有什么方法能解决这个痛点呢？ -- 虚拟机克隆

**实现方式**

kvm虚拟机的克隆分为两种情况。(1) KVM主机本机虚拟机直接克隆。(2) 通过复制配置文件与磁盘文件的虚拟机复制克隆(适用于异机的静态迁移)。

### 命令解析

**镜像克隆**

````bash
virt-clone -o <被克隆的虚拟机名称> -n <生成的虚拟机名称> -f <新的磁盘文件>
virt-clone -o <被克隆的虚拟机名称> --auto-clone
````

### 镜像实践

#### 关闭虚拟机

**关闭虚拟机**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
------------------------------
 - CentOS-7-x86_64 关闭
````

#### 克隆镜像

**克隆vm需要时间**

````bash
[root@kvm-host ~]# virt-clone -o CentOS-7-x86_64 -n CentOS-7-clone -f
/opt/CentOS-7-clone.img
正在分配 'CentOS-7-clone.img' 4% [=- ] 273 MB/s | 444 MB
 00:00:35
正在分配 'CentOS-7-clone.img' 5% [== ] 237 MB/s | 539 MB
 00:00:40
正在分配 'CentOS-7-clone.img' 6% [== ] 208 MB/s | 638 MB
 00:00:46
正在分配 'CentOS-7-clone.img' 7% [==- ] 186 MB/s | 740 MB
 00:00:51
````

````text
正在分配 'CentOS-7-clone.img' 8% [=== ] 166 MB/s | 828 MB
 00:00:56
正在分配 'CentOS-7-clone.img' 8% [===- ] 151 MB/s | 920 MB
 00:01:01
正在分配 'CentOS-7-clone.img' 9% [===- ] 137 MB/s | 1.0 GB
 00:01:07
正在分配 'CentOS-7-clone.img' 10% [==== ] 131 MB/s | 1.1 GB
 00:01:09
正在分配 'CentOS-7-clone.img' 11% [====- ] 123 MB/s | 1.2 GB
 00:01:13
正在分配 'CentOS-7-clone.img' 12% [====- ] 116 MB/s | 1.3 GB
 00:01:17
正在分配 'CentOS-7-clone.img' 13% [===== ] 111 MB/s | 1.4 GB
 00:01:20
正在分配 'CentOS-7-clone.img' 14% [=====- ] 106 MB/s | 1.4 GB
 00:01:22
正在分配 'CentOS-7-clone.img' 15% [====== ] 107 MB/s | 1.5 GB
 00:01:21
正在分配 'CentOS-7-clone.img' | 10 GB
 00:00:13
成功克隆 'CentOS-7-clone'。
````

**查看虚拟机**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
----------------------------------
 - CentOS-7-clone 关闭
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-bak 关闭
````

**查看虚拟机相关文件**

````bash
[root@kvm-host ~]# ls /opt/
CentOS-7-clone.img CentOS-7-x86_64-1.qcow2 CentOS-7-x86_64-1.raw CentOS-7-
x86_64.qcow2 CentOS-7-x86_64.raw
[root@kvm-host ~]# ls /etc/libvirt/qemu
autostart CentOS-7-clone.xml CentOS-7-x86_64.xml CentOS-backup.xml networks
````

#### 对比配置

**查看文件区别**

````bash
[root@kvm-host ~]# cd /etc/libvirt/qemu/
[root@kvm-host qemu]# diff CentOS-7-clone.xml CentOS-7-x86_64.xml
4c4
< virsh edit CentOS-7-clone
---
> virsh edit CentOS-7-x86_64
````

````text
9,10c9,10
< <name>CentOS-7-clone</name>
< <uuid>00000000-0000-4000-8000-00000000000a</uuid>
---
> <name>CentOS-7-x86_64</name>
> <uuid>00000000-0000-4000-8000-000000000001</uuid>
44c44
< <source file='/opt/CentOS-7-clone.img'/>
---
> <source file='/opt/CentOS-7-x86_64.qcow2'/>
135c135
< <mac address='02:00:00:00:00:08'/>
---
> <mac address='02:00:00:00:00:07'/>
可以看到：
    我们克隆的虚拟机创建了新的磁盘文件/配置文件/虚拟机
    克隆的虚拟机和源虚拟机的配置文件主要改变的方在：name/uuid/source/mac 这四方面
````

#### 启动虚拟机

**查看虚拟机**

````bash
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
----------------------------------
 - CentOS-7-clone 关闭
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-bak 关闭
````

**启动两台虚拟机**

````bash
[root@kvm-host qemu]# virsh start CentOS-7-clone
域 'CentOS-7-clone' 已启动
[root@kvm-host qemu]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
````

**查看效果**

````bash
[root@kvm-host qemu]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-clone 运行
 2 CentOS-7-x86_64 运行
````

登录后确认效果，因为我们之前定制的是静态ip，所以只能从mac地址上查看到时不同的主机


<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/04-network-management.html' | relative_url }}">← 上一章：网络管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/06-resource-management.html' | relative_url }}">下一章：资源管理 →</a>
</nav>
