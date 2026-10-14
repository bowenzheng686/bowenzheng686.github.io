---
layout: default
title: 'KVM 虚拟化 · 资源管理'
subject_page: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 06 章 · 资源管理

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 6.1 cpu简介

### 基础知识

#### 场景需求

**简介**

在虚拟机不关机的情况下，对CPU进行调整操作叫热调整。它是在Redhat7.0以后才出现的功能，所以要使用这功能，那必须要求KVM宿主机和虚拟机规格必须一致，而且在7.0+版本。目前cpu热调整命令，只能增加，不能减少，想要减少的话，可以进入虚拟机中，关闭某个使用的CPU即可。

**公有云上的虚拟机为什么不支持cpu的热调整**

1、因为客户创建的虚拟机类型不一致，不满足热添加和热删除的前提条件，所以为了管理的方便就统一不允许了 2、因为创建虚拟机会有个调度的问题，创建的虚拟机的命令，会将创建的虚拟机调度到某一台宿主机上，具体调度到哪台宿主机上，没有办法保证，由于受宿主机的配置影响，所以热添加和热删除的功能没有办法保证

#### 常见命令

**热调整**

````bash
virsh setvcpus <虚拟机名称> <cpu个数> --live
    注意：
        默认后面会有 --live 属性，标识热调整，默认不会更改后端的配置
        如果需要更改后端的配置，需要使用 --config
````

**cpu绑定**

````bash
virsh vcpupin <虚拟机名称> <虚拟机CPU号> <宿主机CPU号>
````

**cpu重置**

````bash
virsh shutdown <虚拟机名称>
virsh start <虚拟机名称>
````

#### 准备工作

**查看宿主机的cpu个数**

````bash
[root@kvm-host ~]# lscpu
架构： x86_64
  CPU 运行模式： 32-bit, 64-bit
  Address sizes: 45 bits physical, 48 bits virtual
  字节序： Little Endian
CPU: 8
  在线 CPU 列表： 0-7
厂商 ID： GenuineIntel
  BIOS Vendor ID: GenuineIntel
  型号名称： Intel(R) Core(TM) i7-14700
可以看到：
    我们的宿主机的cpu个数为8个,目前全部在线
````

宿主机查看所有的cpu状态,宿主机的7个cpu都是处于工作状态中

````bash
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu1/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu2/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu3/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu4/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu5/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu6/online
1
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu7/online
1
````

cpu0里面有可能没有online，这不影响，如果非要看的话，可以手工添加个

````bash
[root@kvm-host ~]# cat /sys/devices/system/cpu/cpu0/online
cat: /sys/devices/system/cpu/cpu0/online: 没有那个文件或目录
[root@kvm-host ~]# ls /sys/devices/system/cpu/cpu0/
cache cpuidle crash_notes crash_notes_size driver firmware_node hotplug
 node0 power subsystem topology uevent
````

**看虚拟机当前的cpu状态**

````bash
[root@kvm-host ~]# virsh edit CentOS-7-x86_64
        ...
  <vcpu placement='static'>2</vcpu>
````

#### 让cpu支持动态调整功能

**关闭虚拟机**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
----------------------------------
 - CentOS-7-clone 关闭
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-bak 关闭
````

**编辑虚拟机配置**

````bash
[root@kvm-host ~]# virsh edit CentOS-7-x86_64
域'CentOS-7-x86_64' XML 配置已被编辑。
# 原内容
    <vcpu placement='static'>2</vcpu>
# 修改后
    <vcpu placement='static' current='1'>4</vcpu>
注意：
    意思就是，当前的cpu可以动态调整，当前的cpu个数为1，可调整的最大个数为4
    经过测试，我的虚拟机可以支持255个，但是最大只能设置253个。
    如果操作异常，有可能导致以下异常情况
    error: operation failed: Failed to query numad for the advisory nodeset
````

**启动虚拟机后查看效果**

````bash
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host ~]# virsh dominfo CentOS-7-x86_64
Id: 4
名称： CentOS-7-x86_64
UUID: 00000000-0000-4000-8000-000000000001
OS 类型： hvm
状态： 运行
CPU： 1
CPU 时间： 8.0s
最大内存： 1048576 KiB
使用的内存： 1048576 KiB
持久： 是
````

````bash
自动启动： 禁用
管理的保存： 否
安全性模式： none
安全性 DOI： 0
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 4
状态： 运行
CPU 时间： 13.4s
CPU关系: yyyyyyyy
CPU关系的值：
    如果是 y，表示该虚拟 CPU 可以在对应的物理 CPU 核心上运行；如果是 n，则表示不可以。
    上面有 8 个 y，说明这个虚拟 CPU 可以在系统中的所有 8 个物理 CPU 核心上运行，也就是说它与
所有 8 个物理 CPU 核心都具有亲和性，调度程序可以根据系统负载等情况将这个虚拟 CPU 的任务分配到这
8 个核心中的任意一个上执行。
````

### 简单实践

#### 动态调整

##### 增加cpu

**增加cpu的数量不能超过限制**

````bash
[root@kvm-host ~]# virsh setvcpus CentOS-7-x86_64 8
错误： 无效参数：请求的 vcpu 大于活动域的最大允许的 vcpu：8 > 4
````

**增加cpu后检查**

````bash
[root@kvm-host ~]# virsh setvcpus CentOS-7-x86_64 4
````

确认效果,cpu已经添加为4个了

````bash
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 7
状态： 运行
CPU 时间： 22.4s
CPU关系: yyyyyyyy
VCPU: 1
CPU: 3
状态： 运行
CPU 时间： 0.1s
CPU关系: yyyyyyyy
````

````text
VCPU: 2
CPU: 7
状态： 运行
CPU 时间： 0.1s
CPU关系: yyyyyyyy
VCPU: 3
CPU: 2
状态： 运行
CPU 时间： 0.0s
CPU关系: yyyyyyyy
````

##### 删减cpu

**删减cpu**

````bash
[root@kvm-host ~]# virsh setvcpus CentOS-7-x86_64 2
````

删减cpu后检查，cpu的数量减少为2个

````bash
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 1
状态： 运行
CPU 时间： 22.9s
CPU关系: yyyyyyyy
VCPU: 1
CPU: 2
状态： 运行
CPU 时间： 0.1s
CPU关系: yyyyyyyy
````

查看配置,配置没有发生变动

````bash
[root@kvm-host ~]# grep vcpu /etc/libvirt/qemu/CentOS-7-x86_64.xml
  <vcpu placement='static' current='1'>4</vcpu>
````

#### 配置实践

##### 更新配置

**修改配置**

````bash
[root@kvm-host ~]# virsh setvcpus CentOS-7-x86_64 3 --config
````

**cpu的运行数量没有变化**

````bash
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 6
状态： 运行
CPU 时间： 24.7s
CPU关系: yyyyyyyy
VCPU: 1
CPU: 1
状态： 运行
CPU 时间： 0.6s
CPU关系: yyyyyyyy
````

**但是配置文件发生了改变**

````bash
[root@kvm-host ~]# grep vcpu /etc/libvirt/qemu/CentOS-7-x86_64.xml
  <vcpu placement='static' current='3'>4</vcpu>
````

##### 重置cpu

**普通重置**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host ~]# virsh list
 Id 名称 状态
-------------------
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
````

查看效果,会按照配置里面的 信息进行加载环境信息

````bash
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 2
状态： 运行
CPU 时间： 6.2s
CPU关系: yyyyyyyy
VCPU: 1
CPU: 2
状态： 运行
CPU关系: yyyyyyyy
VCPU: 2
CPU: 1
状态： 运行
CPU关系: yyyyyyyy
````

##### cpu绑定

**将kvm的0号cpu绑定在宿主机的1号cpu上**

````bash
[root@kvm-host ~]# virsh vcpupin CentOS-7-x86_64 0 1
````

**将kvm的1号cpu绑定在宿主机的2号cpu上**

````bash
[root@kvm-host ~]# virsh vcpupin CentOS-7-x86_64 1 2
````

**将kvm的3号cpu绑定在宿主机的0号cpu上**

````bash
[root@kvm-host ~]# virsh vcpupin CentOS-7-x86_64 2 0
````

**查看效果**

````bash
[root@kvm-host ~]# virsh vcpuinfo CentOS-7-x86_64
VCPU: 0
CPU: 1
状态： 运行
CPU 时间： 13.1s
CPU关系: -y------
VCPU: 1
CPU: 2
状态： 运行
CPU 时间： 6.1s
CPU关系: --y-----
VCPU: 2
CPU: 0
状态： 运行
CPU 时间： 5.5s
CPU关系: y-------
````

## 6.2 内存实践

### 基础知识

#### 场景需求

**需求**

需要根据实际情况，对kvm进行内存资源调整

**注意：**

不推荐频繁切换，否则导致虚拟机启动异常

#### 基本语法

**立刻生效**

````bash
virsh qemu-monitor-command <虚拟机名称> --hmp --cmd 命令
    命令解析：
        查看所有信息 info
        查看内存 info balloon
        调整内存 balloon 定制容量
    特点：
        只管调整，不管系统是否重启成功
````

**重启后生效**

````bash
virsh setmem <虚拟机名称> 定制容量
    注意：
        该方法上课时候不推荐，因为不是及时生效
        因为它涉及到虚拟机资源的重新加载(重启主机)，如果内存过小，导致系统无法启动。
        再一个，频繁执行次数过多导致虚拟机卡死
````

#### 资源超配

**超限使用**

原则上，宿主机的资源是不允许超限使用的，比如，我要在 100G的电脑上，存储 200G的资源。这是不可能的。根据我们之前对虚拟磁盘的原理解析，我们知道，分配的资源和使用的资源是有区别的，实际使用的远远小于分配的资源。所以我们在分配内存的时候，可以对内存进行超配的使用

**查看配置文件**

````bash
[root@kvm-host ~]# virsh dumpxml CentOS-7-x86_64|grep -i memo
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
````

**查看虚拟机内存信息**

````bash
[root@kvm-host ~]# virsh dominfo CentOS-7-x86_64| grep -E "mem|内存"
最大内存： 1048576 KiB
使用的内存： 1048576 KiB
````

### 简单实践

#### 调整内存

**查看内存信息**

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd info
balloon
balloon: actual=1024
````

**调整内存信息**

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd
balloon 512
````

**确认内存信息**

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd info
balloon
balloon: actual=512
[root@kvm-host ~]# virsh dumpxml CentOS-7-x86_64|grep -i memo
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
[root@kvm-host ~]# virsh dominfo CentOS-7-x86_64| grep -E "mem|内存"
最大内存： 1048576 KiB
使用的内存： 524288 KiB
结果显示：
    主机的内存信息和配置信息都同步更改了
````

在存在最大内存的前提下，是无法调整到限制之外的

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd
balloon 3000
因为最大内存的限制，所以最大的值只能调整到1G
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd info
balloon
balloon: actual=1024
````

#### 调整最大上限

**调整内存的限制**

````bash
[root@kvm-host ~]# virsh edit CentOS-7-x86_64
        ...
      4 <memory unit='KiB'>3170304</memory>
      5 <currentMemory unit='KiB'>1048576</currentMemory>
    说明：
        调整了内存的最大值为3G，当前的内存大小为1G
````

**但是实际运行确没有生效**

````bash
[root@kvm-host ~]# virsh dumpxml CentOS-7-x86_64|grep -i memo
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
````

重启vm之后，生效

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host ~]# virsh dumpxml CentOS-7-x86_64|grep -i memo
  <memory unit='KiB'>3170304</memory>
  <currentMemory unit='KiB'>3170304</currentMemory>
````

#### 调整实践

**动态调大内存**

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd
balloon 2048
查看当前内存大小
[root@kvm-host ~]# virsh dominfo CentOS-7-x86_64| grep -E "mem|内存"
最大内存： 3170304 KiB
使用的内存： 2097152 KiB
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd info
balloon
balloon: actual=2048
````

**动态调大内存**

````bash
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd
balloon 3000
查看当前内存大小
[root@kvm-host ~]# virsh qemu-monitor-command CentOS-7-x86_64 --hmp --cmd info
balloon
balloon: actual=3000
````

**确认虚拟机效果**

````bash
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Thu Mar 27 20:12:32 on ttyS0
[root@localhost ~]# free -m
              total used free shared buff/cache available
Mem: 2706 214 2321 8 171 2288
Swap: 1023 0 1023
````

## 6.3 磁盘实践

### 基础知识

#### 场景需求

虚拟机在操作过程中，会遇到各种数据容量操作，我们常见的操作就是

初始化时候，磁盘容量不合适，我们可以进行调整数据容量不足，我们就增加一块数据磁盘数据容量过大，我们就删减一块数据磁盘

#### 常见语法

**磁盘基本信息**

````bash
virsh domblklist --details 虚拟磁盘名称
````

**磁盘容量调整**

````bash
qemu-img resize 虚拟磁盘名称 +5G
````

**挂载磁盘**

````bash
virsh attach-disk <虚拟机名称> --source <新磁盘名> --target <磁盘类型名> --persistent
注意：
    磁盘类型名一般是 sda~ 或者 vda~
    这里的 vda 不一定是磁盘内部的信息，而是kvm管理的名称
````

**卸载磁盘**

````bash
virsh detach-disk <虚拟机名称> <磁盘类型名>
````

### 简单实践

#### 磁盘容量调整

##### 调整前确认效果

查看磁盘空间效果，大概是11G

````bash
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Thu Mar 27 20:19:42 on ttyS0
[root@localhost ~]# fdisk -l
磁盘 /dev/vda：10.7 GB, 10737418240 字节，20971520 个扇区 # 目前磁盘的空间大
概11G
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c17c2
   设备 Boot Start End Blocks Id System
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
````

##### 关闭虚拟机

**确认磁盘文件**

````bash
[root@kvm-host ~]# virsh dumpxml CentOS-7-x86_64 | grep opt
      <source file='/opt/CentOS-7-x86_64.qcow2' index='2'/>
````

**正常运行的vm主机无法查看磁盘状态**

````bash
[root@kvm-host ~]# qemu-img info /opt/CentOS-7-x86_64.qcow2
qemu-img: Could not open '/opt/CentOS-7-x86_64.qcow2': Failed to get shared
"write" lock
Is another process using the image [/opt/CentOS-7-x86_64.qcow2]?
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
````

**关闭虚拟机**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
````

**正常运行的磁盘**

**查看当前磁盘状态**

````bash
[root@kvm-host ~]# qemu-img info /opt/CentOS-7-x86_64.qcow2
image: /opt/CentOS-7-x86_64.qcow2
file format: qcow2
virtual size: 10 GiB (10737418240 bytes)
disk size: 1.57 GiB
cluster_size: 65536
Format specific information:
    compat: 1.1
    compression type: zlib
    lazy refcounts: false
    refcount bits: 16
    corrupt: false
    extended l2: false
Child node '/file':
    filename: /opt/CentOS-7-x86_64.qcow2
    protocol type: file
    file length: 1.57 GiB (1682309120 bytes)
    disk size: 1.57 GiB
    Format specific information:
        extent size hint: 1048576
````

##### 调整大小

**调整磁盘大小**

````bash
[root@kvm-host ~]# qemu-img resize /opt/CentOS-7-x86_64.qcow2 +1G
Image resized. # 调整成功的标识
````

**查看磁盘状态**

````bash
[root@kvm-host ~]# qemu-img info /opt/CentOS-7-x86_64.qcow2
````

````text
image: /opt/CentOS-7-x86_64.qcow2
file format: qcow2
virtual size: 11 GiB (11811160064 bytes) # 标称容量增加了1G
disk size: 1.57 GiB
cluster_size: 65536
Format specific information:
    compat: 1.1
    compression type: zlib
    lazy refcounts: false
    refcount bits: 16
    corrupt: false
    extended l2: false
Child node '/file':
    filename: /opt/CentOS-7-x86_64.qcow2
    protocol type: file
    file length: 1.57 GiB (1682309632 bytes)
    disk size: 1.57 GiB
    Format specific information:
        extent size hint: 1048576
````

##### 调整大小

**再次调整磁盘大小**

````bash
[root@kvm-host ~]# qemu-img resize /opt/CentOS-7-x86_64.qcow2 +2G
Image resized. # 调整成功的标识
````

**查看磁盘状态**

````bash
[root@kvm-host ~]# qemu-img info /opt/CentOS-7-x86_64.qcow2
image: /opt/CentOS-7-x86_64.qcow2
file format: qcow2
virtual size: 13 GiB (13958643712 bytes) # 标称容量增加了2G
disk size: 1.57 GiB
cluster_size: 65536
Format specific information:
    compat: 1.1
    compression type: zlib
    lazy refcounts: false
    refcount bits: 16
    corrupt: false
    extended l2: false
Child node '/file':
    filename: /opt/CentOS-7-x86_64.qcow2
    protocol type: file
    file length: 1.57 GiB (1682309632 bytes)
    disk size: 1.57 GiB
    Format specific information:
        extent size hint: 1048576
````

##### 确认效果

**重启虚拟机**

````bash
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
````

**进入虚拟机查看磁盘大小**

````bash
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Thu Mar 27 20:19:42 on ttyS0
[root@localhost ~]# fdisk -l
# 虽然标称14G，但是字节是和qemu-img info查看到的字节效果一样
磁盘 /dev/vda：14.0 GB, 13958643712 字节，27262976 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000c17c2
   设备 Boot Start End Blocks Id System
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
根据上面实验得知：
    动态调整磁盘容量大小调整成功
````

Gi 和 G

````bash
[root@kvm-host ~]# echo "scale=2; 13958643712 /1000 /1000 / 1000"| bc
13.95
[root@kvm-host ~]# echo "scale=2; 13958643712 /1024 /1024 / 1024"| bc
13.00
````

#### 磁盘基本操作

##### 新增磁盘

**创建新磁盘**

````bash
[root@kvm-host ~]# qemu-img create -f raw /opt/storage.qcow2 2G
Formatting '/opt/storage.qcow2', fmt=raw size=2147483648
````

**增加新磁盘到虚拟机**

````bash
[root@kvm-host ~]# virsh attach-disk CentOS-7-x86_64 --source /opt/storage.qcow2
--target vdb --persistent
成功附加磁盘
[root@kvm-host ~]# virsh domblklist --details CentOS-7-x86_64
 类型 Device 目标 源
----------------------------------------------------
 file disk vda /opt/CentOS-7-x86_64.qcow2
 file disk vdb /opt/storage.qcow2
 file cdrom sda -
````

##### 确认效果

**登录虚拟机**

````bash
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Thu Mar 27 20:32:36 on ttyS0
[root@localhost ~]#
````

**登录到虚拟机中检查效果**

````bash
[root@localhost ~]# fdisk -l | grep vd
磁盘 /dev/vda：14.0 GB, 13958643712 字节，27262976 个扇区
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
磁盘 /dev/vdb：2147 MB, 2147483648 字节，4194304 个扇区
````

##### 移除磁盘

**删除虚拟机的某磁盘**

````bash
[root@kvm-host ~]# virsh detach-disk CentOS-7-x86_64 --target vdb --persistent
成功分离磁盘
[root@kvm-host ~]# virsh domblklist --details CentOS-7-x86_64
 类型 Device 目标 源
----------------------------------------------------
 file disk vda /opt/CentOS-7-x86_64.qcow2
 file cdrom sda -
````

登录到虚拟机中检查效果，立刻生效了

````bash
[root@localhost ~]# fdisk -l | grep vd
磁盘 /dev/vda：14.0 GB, 13958643712 字节，27262976 个扇区
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
[root@localhost ~]#
````

#### 新增磁盘实践

##### 新增磁盘

**关闭虚拟机**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
````

**新增一块磁盘**

````bash
[root@kvm-host ~]# qemu-img create -f raw /opt/image.raw 2G
Formatting '/opt/image.raw', fmt=raw size=2147483648
````

**查看效果**

````bash
[root@kvm-host ~]# ll /opt/
总用量 4991908
-rw------- 1 qemu qemu 1681063936 3月 26 23:01 CentOS-7-clone.img
-rw-r--r-- 1 root root 196656 3月 26 22:07 CentOS-7-x86_64-1.qcow2
-rw-r--r-- 1 root root 3221225472 3月 26 21:55 CentOS-7-x86_64-1.raw
-rw-r--r-- 1 qemu qemu 1682374656 3月 27 20:41 CentOS-7-x86_64.qcow2
-rw-r--r-- 1 root root 13958643712 3月 27 20:22 CentOS-7-x86_64.raw
-rw-r--r-- 1 root root 2147483648 3月 27 20:41 image.raw
-rw-r--r-- 1 root root 2147483648 3月 27 20:37 storage.qcow2
````

##### 关联磁盘

**编辑配置文件**

````bash
[root@linux-node1 ~]# virsh edit CentOS-7-x86_64
                ...
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/opt/CentOS-7-x86_64.qcow2'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
    # 增加如下磁盘内容
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/opt/image.raw'/>
      <target dev='vdc' bus='virtio'/> # dev的名字不能重复
    </disk>
                ...
注意：
    添加 38-42行的内容
    和之前的disk配置缺少了<address type='pci'... 的内容。 -- 该部分内容会自动增加
````

**启动虚拟机**

````bash
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host ~]# virsh domblklist --details CentOS-7-x86_64
 类型 Device 目标 源
----------------------------------------------------
 file disk vda /opt/CentOS-7-x86_64.qcow2
 file disk vdc /opt/image.raw
 file cdrom sda -
````

连接进入虚拟机确认新增磁盘已识别，但是，盘标识是 递增出来的

````bash
[root@localhost ~]# fdisk -l | grep vd
磁盘 /dev/vda：14.0 GB, 13958643712 字节，27262976 个扇区
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
磁盘 /dev/vdb：2147 MB, 2147483648 字节，4194304 个扇区
````

在基于 Linux 内核的虚拟机里，通常会按照设备被检测到的顺序来命名，依次为 vda、vdb、vdc 等。宿主机指定的设备名不会影响虚拟机内核的命名规则。

##### 使用磁盘

**格式化磁盘**

````bash
[root@localhost ~]# mkfs.ext4 /dev/vdb
mke2fs 1.42.9 (28-Dec-2013)
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
...
Writing superblocks and filesystem accounting information: 完成
````

**新建一个目录来挂载新硬盘**

````bash
[root@localhost ~]# mkdir /data
[root@localhost ~]# mount /dev/vdb /data/
[root@localhost ~]# mount | grep vdb
/dev/vdb on /data type ext4 (rw,relatime,seclabel,data=ordered)
[root@localhost ~]# umount /data
````

**开机自动挂载**

````bash
[root@localhost ~]# blkid /dev/vdb
/dev/vdb: UUID="00000000-0000-4000-8000-00000000000c" TYPE="ext4"
[root@localhost ~]# echo 'UUID=00000000-0000-4000-8000-00000000000c /data ext4
defaults 0 0'>> /etc/fstab
[root@localhost ~]# mount -a
[root@localhost ~]# mount | grep vdb
/dev/vdb on /data type ext4 (rw,relatime,seclabel,data=ordered)
[root@localhost ~]# df -h | egrep 'Files|vd'
/dev/vda1 1014M 150M 865M 15% /boot
/dev/vdb 2.0G 6.0M 1.8G 1% /data
可以看到：
    新增磁盘的方法调整虚拟机的磁盘容量，在虚拟机中想要看到效果，必须重启虚拟机
````

**向磁盘中增加数据**

````bash
[root@localhost ~]# dd if=/dev/zero of=/data/1M.img bs=10M count=1
记录了1+0 的读入
记录了1+0 的写出
10485760字节(10 MB)已复制，0.0256097 秒，409 MB/秒
[root@localhost ~]# ll /data/ -h
总用量 11M
-rw-r--r--. 1 root root 10M 3月 27 20:50 1M.img
drwx------. 2 root root 16K 3月 27 20:46 lost+found
````

#### 磁盘迁移

##### 磁盘移除

**从 CentOS-7-x86_64 中移除磁盘**

````bash
[root@kvm-host ~]# virsh detach-disk CentOS-7-x86_64 --target vdc --persistent
成功分离磁盘
[root@kvm-host ~]# virsh domblklist --details CentOS-7-x86_64
 类型 Device 目标 源
----------------------------------------------------
 file disk vda /opt/CentOS-7-x86_64.qcow2
 file cdrom sda -
````

直接查看效果,CentOS-7-x86_64 中已看不到磁盘了

````bash
[root@localhost ~]# fdisk -l | grep vd
磁盘 /dev/vda：14.0 GB, 13958643712 字节，27262976 个扇区
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
[root@localhost ~]#
````

##### 磁盘挂载

**启动vm主机**

````bash
[root@kvm-host ~]# virsh start CentOS-7-clone
域 'CentOS-7-clone' 已启动
````

**挂载新磁盘**

````bash
[root@kvm-host ~]# virsh attach-disk CentOS-7-clone --source /opt/image.raw --
target vdx --persistent
成功附加磁盘
[root@kvm-host ~]# virsh domblklist --details CentOS-7-clone
 类型 Device 目标 源
-------------------------------------------------
 file disk vda /opt/CentOS-7-clone.img
 file disk vdx /opt/image.raw
 file cdrom sda -
````

**登录到虚拟机确认效果**

````bash
[root@kvm-host ~]# virsh console CentOS-7-clone
连接到域 'CentOS-7-clone'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Wed Mar 26 22:41:28 on tty1
[root@localhost ~]# fdisk -l | grep vd
磁盘 /dev/vda：10.7 GB, 10737418240 字节，20971520 个扇区
/dev/vda1 * 2048 2099199 1048576 83 Linux
/dev/vda2 2099200 20971519 9436160 8e Linux LVM
磁盘 /dev/vdb：2147 MB, 2147483648 字节，4194304 个扇区
````

挂载磁盘确认效果,可以看到迁移之前的数据效果

````bash
[root@localhost ~]# mkdir /data
[root@localhost ~]# mount /dev/vdb /data
[root@localhost ~]# ll -h /data/
总用量 11M
-rw-r--r--. 1 root root 10M 3月 27 20:50 1M.img
drwx------. 2 root root 16K 3月 27 20:46 lost+found
````

# 3 拓展思考

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/05-image-management.html' | relative_url }}">← 上一章：镜像管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/07-virtualization-principles.html' | relative_url }}">下一章：虚拟化原理 →</a>
</nav>
