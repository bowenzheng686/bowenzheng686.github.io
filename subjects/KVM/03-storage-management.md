---
layout: default
title: 'KVM 虚拟化 · 存储管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 03 章 · 存储管理

libvirt 把宿主机存储后端组织为**存储池（pool）**，再在池中管理**存储卷（volume）**。卷附加到虚拟机后表现为块设备；来宾中的分区、文件系统和挂载点属于另一个层次。先分清这三层，再操作创建、扩容与删除，才不容易把“移除定义”误认为“删除数据”。

## 3.1 存储池：定义、启用和移除

存储池可以指向宿主机目录，也可以使用网络文件系统、LVM 或其他后端。它提供统一的卷管理入口，但**不自动提高底层存储的性能或可靠性**；容量、备份和故障域仍由后端决定。

![存储池与宿主机后端关系图]({{ '/subjects/KVM/assets/p080-img01.webp' | relative_url }})

### 创建一个目录型持久存储池

本例选择宿主机目录 `/kvm/images`。创建前先确认目标路径的挂载、容量、权限和安全标签；若该路径已包含业务文件，不要把创建池当成清空目录的操作。

```bash
sudo mkdir -p /kvm/images
virsh pool-define-as gavin_pool dir --target /kvm/images
virsh pool-start gavin_pool
virsh pool-autostart gavin_pool
virsh pool-info gavin_pool
virsh pool-list --all
```

`pool-define-as` 创建**持久定义**，不等于已经启动；本例的目标目录已准备好，因此直接用 `pool-start` 激活，再用 `pool-autostart` 设置宿主机重新启动后的自动激活。若后端尚未准备，可按池类型使用 `pool-build`，但不要在已有业务数据的路径上盲目构建。一次性实验可用 `virsh pool-create-as <名称> dir --target <目录>` 创建临时活动池，它停止后没有持久定义可重新启动。

`pool-list --all` 用于核对状态与自动启动列；配置文件通常由 libvirt 管理，不应为了修改池而直接编辑 `/etc/libvirt/storage/*.xml`。不同后端的创建参数和清理行为不同，NFS、iSCSI 或 LVM 池应阅读对应后端文档，而不能只把目录型命令中的 `dir` 换成别的类型。

### 停用与取消定义不是删卷

先列出卷及引用它的虚拟机，再决定是否可以停用池。一个虚拟机仍在读写其中的卷时，强行停用或删除后端会造成 I/O 错误或数据丢失。

```bash
virsh vol-list gavin_pool
virsh domblklist <虚拟机名>
virsh pool-destroy gavin_pool
virsh pool-undefine gavin_pool
```

`pool-destroy` 在这里表示**停止池管理实例**，不是删除卷文件；`pool-undefine` 删除 libvirt 中的持久定义。二者都不等同于“安全清理磁盘”。`pool-delete` 会尝试清理后端资源，行为依池类型而异；只有确认池为空、没有虚拟机引用且已完成备份时才考虑它。

## 3.2 存储卷：创建、附加和使用

一个目录型池中的卷通常是镜像文件；LVM 池中的卷则可能是逻辑卷。下图将存储池、存储卷与来宾磁盘的关系放在一起。来宾的 `/dev/vdb` 名称可能随控制器与设备顺序变化，不能只凭字母判断它是哪块盘。

![存储池与虚拟机存储卷关系图（高清重绘）]({{ '/subjects/KVM/assets/p087-img01-redrawn.webp' | relative_url }})

### 创建并核对卷

```bash
virsh vol-create-as gavin_pool gavin.img 2G --allocation 1G --format raw
virsh vol-list gavin_pool
virsh vol-info gavin.img gavin_pool
virsh vol-path gavin.img gavin_pool
```

`2G` 是虚拟容量，`--allocation 1G` 是初始分配量。不同格式和文件系统的实际占用可能不同；检查容量应同时看 `vol-info`、宿主机 `ls -lh` 和 `du -h`，并为后续写入预留真实空间。不要把“卷已创建”理解为来宾可直接使用的已格式化文件系统。

### 将卷附加到虚拟机

先确认该卷未被另一台虚拟机以可写方式使用。对运行中的来宾，按需同时修改当前状态和持久定义；实际版本支持的参数可通过 `virsh help attach-disk` 核对。

```bash
virsh attach-disk <虚拟机名> /kvm/images/gavin.img vdb \
  --targetbus virtio --live --config
virsh domblklist <虚拟机名>
```

进入来宾后运行 `lsblk -f`，根据容量、序列号和已有分区识别新设备。**仅在确认是空盘后**，才对目标设备分区或格式化；旧实验直接把整个 `/dev/vdb` 格式化为 ext4，因此不能照搬到已有数据的磁盘上。格式化后可先临时挂载并写入测试文件，确认文件系统工作，再按 UUID 配置持久挂载。

```bash
# 以下命令只在 /dev/vdb 已确认为本次新建的空盘时执行
sudo mkfs.ext4 /dev/vdb
sudo mkdir -p /gavin
sudo mount /dev/vdb /gavin
findmnt /gavin
```

### 安全分离磁盘

先在来宾停止使用该文件系统的进程，卸载它，再在宿主机分离虚拟磁盘。`umount` 失败时应查明仍在使用的进程，而不是强行拔盘。

```bash
# 来宾内
sudo umount /gavin
# 宿主机内
virsh detach-disk <虚拟机名> vdb --live --config
virsh domblklist <虚拟机名>
```

分离只解除虚拟机与卷的关联，卷仍保存在存储池中，可用 `virsh vol-info` 再次确认。

## 3.3 导出、恢复、扩容与删除

### 离线导出与恢复

`vol-download` 可把卷内容导出为文件，`vol-upload` 可将文件写回已存在的目标卷。它们是数据复制工具，不保证运行中的来宾文件系统具有一致快照；本例应先正常关机或使用经过验证的快照/来宾冻结方案，再导出。恢复前核对源文件、目标卷容量和恢复后是否需要修复文件系统。

```bash
virsh domstate <虚拟机名>
sudo mkdir -p /backup
virsh vol-download gavin.img /backup/gavin.img --pool gavin_pool
ls -lh /backup/gavin.img
# 验证备份内容后，才在需要恢复的情形执行：
virsh vol-upload gavin.img /backup/gavin.img --pool gavin_pool
```

不要在演练中先 `vol-wipe` 再把 `vol-upload` 当成必然可成功的回滚：`vol-wipe` 会破坏卷数据，误选卷或备份不完整都不可逆。恢复能力应在独立卷上验证。

### 扩大卷容量

先检查宿主池剩余空间和来宾文件系统类型，再扩大卷的**虚拟容量**。这一步不自动扩展来宾的分区或文件系统；若来宾在线，可能还需刷新它看到的设备容量，之后再按该文件系统的扩容方式处理。

```bash
virsh vol-info gavin.img gavin_pool
virsh vol-resize gavin.img 3G --pool gavin_pool
virsh vol-info gavin.img gavin_pool
```

扩容后在来宾执行 `lsblk`、`df -h` 核对设备与文件系统的差异。缩容需要先处理文件系统和数据边界，操作风险高，不能把 `vol-resize 1G` 作为“缩小文件”的对称命令。

### 克隆与删除卷

克隆可用于创建独立副本，但源卷若仍被来宾写入，副本可能不一致；先关机或使用一致性快照。新旧卷必须使用不同名称，克隆后核对卷路径和数据。

```bash
virsh vol-clone gavin.img gavin-2.img --pool gavin_pool
virsh vol-list gavin_pool
virsh vol-info gavin-2.img gavin_pool
```

删除卷前用 `virsh domblklist <虚拟机名>` 确认没有虚拟机引用它，并验证独立备份可读。`virsh vol-delete gavin-2.img --pool gavin_pool` 删除的是卷数据；重新定义存储池不会把它找回来。

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/02-create-vm-from-cli.html' | relative_url }}">← 上一章：命令创建虚拟机</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/04-network-management.html' | relative_url }}">下一章：网络管理 →</a>
</nav>
