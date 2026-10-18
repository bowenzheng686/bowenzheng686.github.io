---
layout: default
title: 'KVM 虚拟化 · 存储管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 03 章 · 存储管理

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 3.1 存储池

### 存储池环境

#### 基础知识

**需求**

为了使虚拟机获得更强大的后端存储能力，libvirt 提供了对各种各样的存储介质支持，包括本地文件系统，网络文件系统，iSCSI，LVM 等多种后端存储系统。在虚拟机中主要以存储池(pool)与存储卷(volume)的形式存在。libvirt 中的存储管理独立于虚拟机管理。也就是存储池和存储卷的操作独立于虚拟机的操作存在，即使是没有虚拟机的场景。工作中我们可以当虚拟机需要存储资源时再进行灵活分配。

**存储池**

KVM平台以存储池的形式对存储进行统一管理。它可以理解为一种映射关系，即将宿主机器上的存储空间形成可被KVM使用的逻辑存储池，以方便虚拟主机存储资源的统一管理。宿主机的存储空间，可以是本地的、网络的等kvm支持的任意形式。

![原文插图（第 80 页）]({{ '/subjects/KVM/assets/p080-img01.webp' | relative_url }})

默认KVM将这些存储池的配置文件存放于/etc/libvirt/storage，因为我在创建虚拟机的时候，涉及到两个目录，所以这两个目录在虚拟机创建的时候，自动有存在了。通过virsh中pool命令能够查看、创建、激活、注册、删除存储池

````bash
    virsh --help | grep pool
````

#### 基本操作

**信息查看**

用 `virsh pool-list --all` 列出池；用 `virsh pool-info <池名>` 查看容量、状态等信息。

**创建存储池**

````text
常见两种创建方法，基于文件夹和文件系统，我们主要介绍基于文件夹的方式。
    定义永久池+创建池：virsh pool-define-as + virsh pool-build
    创建临时池+启动池：virsh pool-create-as
命令格式一：virsh pool-define-as vmware_pool --type dir --target /kvm/images
    注释：
        vmware_pool 定义的存储池名称
        --type dir 我们的类型是一个dir
        --target /kvm/images 存储池的在宿主机上的目录是/kvm/images
命令格式二：virsh pool-create-as --name vmware_pool --type dir --target /kvm/images
    注释：直接创建并启动一个存储池
        vmware_pool 定义的存储池名称
        --type dir 我们的类型是一个dir
        --target /kvm/images 存储池的在宿主机上的目录是/kvm/images
````

**其他的创建命令**

**基于分区创建存储池：**

````text
virsh pool-define-as <存储池名> fs --source-dev <分区名称> --target <挂载目录>
基于磁盘创建存储池:
virsh pool-define-as <存储池名> disk --source-dev <磁盘名称> --source-format gpt --target <挂载目录>
基于lvm创建存储池:
virsh pool-define-as <存储池名> logical --source-name <vg名称> --target <挂载目录>
基于iscsi创建存储池:
virsh pool-define-as <存储池名> iscsi --source-host <存储主机 IP> --source-dev <存储目标> --target <挂载目录>
基于nfs创建存储池:
virsh pool-define-as <存储池名> netfs --source-host <NFS 主机 IP> --source-path <NFS 共享目录> --target <挂载目录>
````

#### 永久存储池

**创建目录**

````console
[root@kvm-host ~]# mkdir /kvm/images -p
````

**创建存储池**

````console
[root@kvm-host ~]# virsh pool-define-as gavin_dpool --type dir --target /kvm/images
定义池 gavin_dpool
[root@kvm-host ~]# virsh pool-build gavin_dpool
构建池 gavin_dpool
````

**检查效果**

````console
[root@kvm-host ~]# virsh pool-list --persistent
 名称 状态 自动开始
----------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
[root@kvm-host ~]# ls /etc/libvirt/storage/
autostart default.xml images.xml opt.xml gavin_dpool.xml
可以看到：
    pool-define-as创建的存储池没有启动,在存储目录中有定义文件
````

#### 临时存储池

**创建目录**

````console
[root@kvm-host ~]# mkdir /gavin/images -p
````

**创建存储池**

````console
[root@kvm-host ~]# virsh pool-create-as gavin_cpool --type dir --target /gavin/images
创建池 gavin_cpool
````

**检查效果**

````console
[root@kvm-host ~]# virsh pool-list --transient
 名称 状态 自动开始
---------------------------------
 gavin_cpool 活动 否
[root@kvm-host ~]# ls /etc/libvirt/storage/
autostart default.xml images.xml opt.xml gavin_dpool.xml
可以看到：
    pool-create-as创建的存储池启动成功了,在存储目录中没有定义文件
````

### 存储池实践

#### 启动实践

##### 命令解析

**需求**

**启动存储池**

**语法**

**启动命令：**

````bash
    virsh pool-start 存储池名称
开机自启动：
    virsh pool-autostart 存储池名称
````

##### 启动存储池

刚才创建的 gavin_dpool存储池没有启动，现在我们启动它,使它生效。

**启动创建的 gavin_dpool 存储池**

````console
[root@kvm-host ~]# virsh pool-start gavin_dpool
池 gavin_dpool 已启动
````

**检查效果**

````console
[root@kvm-host ~]# virsh pool-list
 名称 状态 自动开始
---------------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
 gavin_cpool 活动 否
 gavin_dpool 活动 否
可以看到：
    这个是时候，启用仅仅是让存储池生效了，但是还没有自动运行，如果要自动运行的话，还需要另一个命
令
````

##### 设置为开机自启动

设置刚才启用的存储池自动运行。

````console
[root@kvm-host ~]# virsh pool-autostart gavin_dpool
池 gavin_dpool 标记为自动启动
````

**检查效果**

````console
[root@kvm-host ~]# virsh pool-list
 名称 状态 自动开始
---------------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
 gavin_cpool 活动 否
 gavin_dpool 活动 是
注意：
    只有定义好的存储池，才可以设置为开机自启动，临时的存储池没有该功能。
````

#### 关闭实践

**需求**

若不再需要对某个存储池进行 libvirt 管理，可先停用它。`pool-destroy` 在这里表示停用池，不等于删除池中的卷文件；但停用前应确认没有虚拟机正在依赖该池。

**语法**

**关闭命令：**

````bash
    virsh pool-destroy 存储池
````

**关闭存储池**

````console
[root@kvm-host ~]# virsh pool-destroy gavin_dpool
销毁池 gavin_dpool
[root@kvm-host ~]# virsh pool-destroy gavin_cpool
销毁池 gavin_cpool
````

检查效果，临时存储池一旦关闭后，就不再存在了

````console
[root@kvm-host ~]# virsh pool-list
 名称 状态 自动开始
----------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
[root@kvm-host ~]# virsh pool-list --all
 名称 状态 自动开始
-----------------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
 gavin_dpool 不活跃 是
````

#### 取消实践

2.1.1.2.3.1基础语法

**需求**

取消存储池分为两种不同操作：`pool-undefine` 删除 libvirt 中的池定义；`pool-delete` 可能删除或修改后端存储资源，具体行为依池类型而异。**不要把取消定义当作释放磁盘空间的自动步骤。**先用 `virsh vol-list <池名>`、`virsh domblklist <虚拟机>` 核对卷与虚拟机引用，完成独立备份后才考虑删除后端资源。

**注意：**

这两步都要求我们的存储对象在virsh pool-list的列表中

**语法**

**删除存储目录：**

````bash
    virsh pool-delete 存储池  # 可能影响后端资源；先核对池类型和内容
删除存储配置文件：
    virsh pool-undefine 存储池
````

##### 取消存储池

**删除实验用空存储池的后端目录**

````console
[root@kvm-host ~]# virsh pool-delete gavin_dpool
池 gavin_dpool 被删除
````

**检查效果**

**检查对象**

````console
[root@kvm-host ~]# virsh pool-list --all
 名称 状态 自动开始
-----------------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
 gavin_dpool 不活跃 是
查看目录
[root@kvm-host ~]# ls /kvm
[root@kvm-host ~]#
````

**删除存储池配置文件**

````console
[root@kvm-host ~]# virsh pool-undefine gavin_dpool
池 gavin_dpool 已经被取消定义
[root@kvm-host ~]# ls /etc/libvirt/storage/
autostart default.xml images.xml opt.xml
````

## 3.2 存储卷

### 存储卷环境

#### 基础知识

**需求**

有了存储池，代表我们有存储数据的基本前提了，但是还不能正常使用，需要借助于存储卷才可以。

存储卷是 libvirt 管理的存储单元，可能对应镜像文件、逻辑卷或块设备。它附加到虚拟机后通常显示为一块虚拟磁盘；来宾系统是否分区、格式化并挂载到目录，是独立的后续步骤，不能把卷与挂载点直接等同。

![存储池与虚拟机存储卷关系图（高清重绘）]({{ '/subjects/KVM/assets/p087-img01-redrawn.webp' | relative_url }})

#### 准备工作

存储卷是结合存储池来使用的，所以我们就先来做存储卷的准备工作：创建存储池

````console
[root@kvm-host ~]# mkdir /kvm/images
[root@kvm-host ~]# virsh pool-define-as gavin_pool --type dir --target /kvm/images
定义池 gavin_pool
[root@kvm-host ~]# virsh pool-start gavin_pool
池 gavin_pool 已启动
````

**检查效果**

````console
[root@kvm-host ~]# virsh pool-list
 名称 状态 自动开始
--------------------------------
 default 活动 是
 images 活动 是
 opt 活动 是
 gavin_pool 活动 否
````

#### 命令解析

**通过virsh中vol命令能够查看、创建、激活、注册、删除存储卷**

````console
[root@kvm-host ~]# virsh --help | grep vol
 Storage Volume (指定关键字'volume'时可以显示此部分帮助信息)
    vol-clone 克隆卷。
    vol-create-as 从一组变量中创建卷
    vol-create 从一个 XML 文件创建一个卷
    vol-create-from 生成卷，使用另一个卷作为输入。
    vol-delete 删除卷
    vol-download 将卷内容下载到文件中
    vol-dumpxml XML 中的卷信息
    vol-info 存储卷信息
    vol-key 为给定密钥或者路径返回卷密钥
    vol-list 列出卷
````

````text
    vol-name 为给定密钥或者路径返回卷名
    vol-path 为给定密钥或者路径返回卷路径
    vol-pool 为给定密钥或者路径返回存储池
    vol-resize 创新定义卷大小
    vol-upload 将文件内容上传到卷
    vol-wipe 擦除卷
````

**创建存储卷主要有两种方式：**

创建新的: virsh vol-create-as

**查看存储卷信息**

查看列表用 `virsh vol-list <存储池>`；查看属性用 `virsh vol-info <卷名> <存储池>`；查看 XML 定义用 `virsh vol-dumpxml <卷名> <存储池>`。

**新建命令**

**命令格式：**

````bash
virsh vol-create-as --pool gavin_pool --name gavin.img --capacity 2G --allocation 1G --format raw
注释：
    virsh vol-create-as 命令
    --pool gavin_pool 指定存储池
    --name gavin.img 支持创建的磁盘卷
    --capacity 2G 存储卷的虚拟容量
    --allocation 1G 存储卷的初始分配大小
    --format raw 存储卷的格式
````

#### 简单实践

**创建存储卷**

````console
[root@kvm-host ~]# virsh vol-create-as --pool gavin_pool --name gavin.img --capacity 2G --allocation 1G --format raw
卷 gavin.img 创建了
````

**查看存储位置**

````console
[root@kvm-host ~]# ll /kvm/images
总用量 1048576
-rw------- 1 root root 2147483648 3月 25 22:03 gavin.img
````

**查看存储池的存储卷列表**

````console
[root@kvm-host ~]# virsh vol-list gavin_pool
 名称 路径
--------------------------------------
 gavin.img /kvm/images/gavin.img
````

**查看存储卷信息**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 1.00 GiB
````

**查看存储卷配置信息**

````console
[root@kvm-host ~]# virsh vol-dumpxml gavin.img gavin_pool
<volume type='file'>
  <name>gavin.img</name>
  <key>/kvm/images/gavin.img</key>
  <capacity unit='bytes'>2147483648</capacity>
  <allocation unit='bytes'>1073741824</allocation>
  <physical unit='bytes'>2147483648</physical>
  <target>
    <path>/kvm/images/gavin.img</path>
    <format type='raw'/>
    <permissions>
      <mode>0600</mode>
      <owner>0</owner>
      <group>0</group>
    </permissions>
    <timestamps>
      <atime>1742911401.107933868</atime>
      <mtime>1742911401.106933853</mtime>
      <ctime>1742911401.106933853</ctime>
      <btime>0</btime>
    </timestamps>
  </target>
</volume>
````

### 挂载、卸载

#### 基础知识

**需求**

虚拟机在需要更多存储空间或者精简存储空间的时候，就遇到了存储卷的 挂载和卸载动作

**方法指令**

**附加磁盘到虚拟机：**

````text
    virsh attach-disk <虚拟机> <存储卷> <挂载设备>
    注意：挂载设备可以是vdx或者sdx，x是从b开始的字母
从虚拟机分离磁盘：
    virsh detach-disk <虚拟机> <挂载设备>
    注意：挂载格式可以是vdx或者sdx
````

#### 准备工作

**磁盘的挂载和卸载操作依赖于运行中的虚拟机**

````console
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 10 CentOS-7-x86_64 运行
````

#### 挂载实践

**挂载操作**

````console
[root@kvm-host ~]# virsh attach-disk CentOS-7-x86_64 /kvm/images/gavin.img vdb
成功附加磁盘
````

**检查效果**

````console
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ])
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Tue Mar 25 20:30:10 on ttyS0
[root@localhost ~]# fdisk -l
磁盘 /dev/vda：10.7 GB, 10737418240 字节，20971520 个扇区
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
磁盘标签类型：dos
磁盘标识符：0x000aecd9
...
磁盘 /dev/vdb：2147 MB, 2147483648 字节，4194304 个扇区 # 挂载的磁盘
````

````text
Units = 扇区 of 1 * 512 = 512 bytes
扇区大小(逻辑/物理)：512 字节 / 512 字节
I/O 大小(最小/最佳)：512 字节 / 512 字节
````

#### 使用磁盘

**在来宾系统内格式化新磁盘。** 以下命令会覆盖目标设备上的现有文件系统；必须先用 `lsblk -f` 核对 `/dev/vdb` 确实为新附加的空盘。

````console
[root@localhost ~]# mkfs.ext4 /dev/vdb
mke2fs 1.42.9 (28-Dec-2013)
文件系统标签=
OS type: Linux
块大小=4096 (log=2)
分块大小=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
131072 inodes, 524288 blocks
26214 blocks (5.00%) reserved for the super user
第一个数据块=0
Maximum filesystem blocks=536870912
16 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912
Allocating group tables: 完成
正在写入inode表: 完成
Creating journal (16384 blocks): 完成
Writing superblocks and filesystem accounting information: 完成
````

**挂载虚拟磁盘**

````console
[root@localhost ~]# mkdir /gavin
[root@localhost ~]# mount /dev/vdb /gavin/
````

**确认效果**

````console
[root@localhost ~]# df -h | grep vdb
/dev/vdb 2.0G 6.0M 1.8G 1% /gavin
````

**测试效果**

````console
[root@localhost ~]# dd if=/dev/zero of=/gavin/test.1.txt bs=1M count=200
记录了200+0 的读入
记录了200+0 的写出
209715200字节(210 MB)已复制，0.46875 秒，447 MB/秒
[root@localhost ~]# ll /gavin/
总用量 204816
drwx------. 2 root root 16384 3月 25 22:10 lost+found
-rw-r--r--. 1 root root 209715200 3月 25 22:12 test.1.txt
````

#### 卸载实践

**卸载目录**

````console
[root@localhost ~]# umount /gavin/
[root@localhost ~]# # Ctrl + ] 退出虚拟机
[root@kvm-host ~]#
````

**卸载磁盘**

````console
[root@kvm-host ~]# virsh detach-disk CentOS-7-x86_64 vdb
成功分离磁盘
````

**确认效果**

````console
[root@kvm-host ~]# virsh console CentOS-7-x86_64
[root@localhost ~]#fdisk -l
````

**检查磁盘效果**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 1.06 GiB
````

## 3.3 其他实践

### 数据实践

#### 基础知识

**需求**

在我们使用数据卷操作的时候，不可避免的涉及到 数据导出、数据清除、数据导入、容量变动 等操作。

**语法格式**

**数据导出**

````text
    virsh vol-download <存储卷名称> <导出文件名> --pool <存储池>
数据清除
    virsh vol-wipe <存储卷名称> --pool <存储池>
数据导入
    virsh vol-upload <存储卷名称> <导出文件名> --pool <存储池>
容量变动
    virsh vol-resize <已存在的存储卷名称> <新的容量大小> --pool <存储池>
    注意：容量的变动主要针对的是磁盘容量，而不是磁盘里面存储的数据
````

#### 导出实践

**导出卷中数据**

````console
[root@kvm-host ~]# virsh vol-download gavin.img file.txt --pool gavin_pool
# 会有几秒的卡顿过程
````

**查看效果**

````console
[root@kvm-host ~]# ll file.txt
-rw-r--r-- 1 root root 2147483648 3月 25 22:17 file.txt
结果显示：
    将一个磁盘文件的所有信息都备份出来了，容量大小与数据卷大小一致
````

#### 清除实践

**清除卷中数据前查看效果**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 1.06 GiB
````

**清除卷中数据。** `vol-wipe` 会擦除卷内容，不能靠随后 `vol-upload` 必然恢复；仅在已验证离线备份、卷未被虚拟机使用且确实需要清空时执行。

````console
[root@kvm-host ~]# virsh vol-wipe gavin.img --pool gavin_pool
擦除卷 gavin.img
````

**再次查看效果**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 0.00 B
````

#### 导入实践

**导入数据前检查效果**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 0.00 B
````

**导入卷中数据**

````console
[root@kvm-host ~]# virsh vol-upload gavin.img file.txt --pool gavin_pool
# 会有几秒的卡顿过程
````

**再次测试效果**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 2.00 GiB
注意：
    如果没有数据卷，则无法导入数据
````

#### 容量变动

**查看当前卷信息**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 2.00 GiB
分配： 2.00 GiB
````

**调整卷容量为3G**

````console
[root@kvm-host ~]# virsh vol-resize gavin.img 3G --pool gavin_pool
成功将卷 'gavin.img' 大小改为 3G
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 3.00 GiB
分配： 2.00 GiB
````

**调整卷容量为5G**

````console
[root@kvm-host ~]# virsh vol-resize gavin.img 5G --pool gavin_pool
成功将卷 'gavin.img' 大小改为 5G
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 5.00 GiB
分配： 2.00 GiB
````

默认情况下不支持直接缩容。扩容存储卷也不会自动扩展来宾中的分区和文件系统；应在来宾内另行检查并调整。缩容涉及数据迁移和文件系统处理，不能只修改卷容量。

````console
[root@kvm-host ~]# virsh vol-resize gavin.img 1G --pool gavin_pool
错误： 将卷 'gavin.img' 的大小改为 1G 失败
错误： 无效参数：无法缩小现有分配的容量
````

### 克隆、删除

#### 基础知识

**需求**

当我们定制好应用数据卷之后，可能需要快速的复制一个，这就用到了数据卷的克隆操作；当我们数据卷的使命结束后，我们就要删除数据卷了。

**语法解析**

**克隆存储卷**

````text
    virsh vol-clone <已存在的存储卷名称> <新的存储卷名称> --pool <存储池>
删除存储卷
    virsh vol-delete <已存在的存储卷> <存储池>
````

#### 克隆实践

**克隆一个新的存储卷**

````console
[root@kvm-host ~]# virsh vol-clone gavin.img gavin-2.img gavin_pool
从 gavin-2.img 克隆的卷 gavin.img
[root@kvm-host ~]# virsh vol-list gavin_pool
 名称 路径
------------------------------------------
 gavin-2.img /kvm/images/gavin-2.img
 gavin.img /kvm/images/gavin.img
[root@kvm-host ~]# ls /kvm/images/
gavin-2.img gavin.img
````

**查看两个存储卷信息**

````console
[root@kvm-host ~]# virsh vol-info gavin.img gavin_pool
名称： gavin.img
类型： 文件
容量： 5.00 GiB
分配： 2.00 GiB
[root@kvm-host ~]# virsh vol-info gavin-2.img gavin_pool
名称： gavin-2.img
类型： 文件
容量： 5.00 GiB
分配： 1.18 MiB
````

#### 删除实践

**删除存储卷。** 先通过 `virsh domblklist` 确认没有虚拟机仍引用该卷，并验证备份可读；`vol-delete` 删除的是卷数据，不能仅通过重新定义存储池找回。

````console
[root@kvm-host ~]# virsh vol-delete gavin-2.img gavin_pool
卷 gavin-2.img 被删除
````

**查看存储卷列表**

````console
[root@kvm-host ~]# virsh vol-list gavin_pool
 名称 路径
--------------------------------------
 gavin.img /kvm/images/gavin.img
[root@kvm-host ~]# ls /kvm/images/
gavin.img
````

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/02-create-vm-from-cli.html' | relative_url }}">← 上一章：命令创建虚拟机</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/04-network-management.html' | relative_url }}">下一章：网络管理 →</a>
</nav>
