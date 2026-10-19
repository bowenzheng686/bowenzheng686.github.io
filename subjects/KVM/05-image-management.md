---
layout: default
title: 'KVM 虚拟化 · 镜像管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 05 章 · 镜像管理

管理虚拟磁盘时，要区分**镜像虚拟容量**、**宿主机实际占用**与**来宾文件系统可用空间**。格式转换只改变镜像容器，不会自动替来宾扩容；创建空盘也不会复制原系统。本章按格式、转换、差分链与克隆逐步说明。

## 5.1 格式与分配方式

raw 结构简单，也可以是稀疏文件；`ls -lh` 显示逻辑大小，`du -h` 显示当前占用。qcow2 支持按需分配、后备文件和内部快照，但不意味着必然比 raw 更快或更小。raw 如需快照，可借助底层存储。选择格式要综合性能、快照、备份与迁移要求。

![基础镜像与变化层的历史概念图]({{ '/subjects/KVM/assets/p117-img01.webp' | relative_url }})

`qemu-img info` 的 `virtual size` 是来宾可见容量，`disk size` 是宿主当前占用。不要仅凭文件扩展名判断格式：

```bash
qemu-img info /var/lib/libvirt/images/system.raw
ls -lh /var/lib/libvirt/images/system.raw
du -h /var/lib/libvirt/images/system.raw
qemu-img create -f qcow2 -o help
```

## 5.2 空盘与已有系统盘不是一回事

### 给虚拟机添加空白数据盘

`qemu-img create` 创建的是**没有分区、文件系统或操作系统的空盘**。原案例把它替换为启动盘，随后出现“not a bootable disk”；这不是 qcow2 故障，而是原系统根本不在该盘上。

```bash
qemu-img create -f qcow2 /var/lib/libvirt/images/data.qcow2 3G
qemu-img info /var/lib/libvirt/images/data.qcow2
virsh domblklist --details VM_NAME
```

如果虚拟机已关闭，且 `vdb` 未占用，可将它作为**第二块盘**写入持久配置：

```bash
virsh attach-disk VM_NAME /var/lib/libvirt/images/data.qcow2 vdb \
  --driver qemu --subdriver qcow2 --targetbus virtio --config
virsh start VM_NAME
virsh domblklist --details VM_NAME
```

运行中热插盘须先验证来宾支持，再使用 `--live --config`。在来宾内以 `lsblk -f` 核对容量、序列号和现有文件系统；设备名可能随枚举变化，不能仅凭 `/dev/vdb` 就格式化。

![将空白盘误作启动盘后的历史报错]({{ '/subjects/KVM/assets/p120-img01.webp' | relative_url }})

### 离线转换已有系统盘

若目标是把**已有系统的 raw 镜像**转换为 qcow2，先正常关机、确认状态、导出虚拟机定义并保留原盘。`virsh shutdown` 只是发关机请求；状态仍为运行中时不得对正在写入的盘执行离线转换。

```bash
virsh shutdown VM_NAME
virsh domstate VM_NAME
virsh domblklist --details VM_NAME
virsh dumpxml VM_NAME > VM_NAME.before-convert.xml
qemu-img info /var/lib/libvirt/images/system.raw
qemu-img convert -p -f raw -O qcow2 \
  /var/lib/libvirt/images/system.raw \
  /var/lib/libvirt/images/system.qcow2
qemu-img info /var/lib/libvirt/images/system.qcow2
qemu-img check /var/lib/libvirt/images/system.qcow2
```

在 `virsh edit VM_NAME` 中只修改原启动盘的格式和路径，保留 `target`、总线与启动顺序。下列是**单个磁盘条目**，不是一份可直接覆盖整个域定义的 XML：

```xml
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2'/>
  <source file='/var/lib/libvirt/images/system.qcow2'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

原示例在 XML 标签后写 `# 注释`，并把修改前后两份 `<devices>` 结构粘在一起，都不是有效配置。还要确保新文件能由 QEMU 进程读取，SELinux 等安全上下文正确。保存后用 `virsh dumpxml VM_NAME` 核对，启动并验证：

```bash
virsh start VM_NAME
virsh domblklist --details VM_NAME
virsh domstate VM_NAME
```

进入来宾确认能启动、原有分区与业务文件都在；`qemu-img check` 只能检查镜像结构，不代替应用检查。旧截图展示的是历史环境中的启动结果。

![已有系统盘转换为 qcow2 后的历史登录画面]({{ '/subjects/KVM/assets/p121-img01.webp' | relative_url }})

如启动失败，停机后把驱动格式与源路径指回保留的 raw 文件，再启动回滚。新盘验证和备份完成前，不要删除原盘。

## 5.3 qcow2 后备链

覆盖层只保存相对基础镜像的变化。后备文件在覆盖层使用期间必须保持路径可达、内容不变；只备份覆盖层文件不足以恢复虚拟机。

```bash
qemu-img info /var/lib/libvirt/images/base.raw
qemu-img create -f qcow2 -F raw \
  -b /var/lib/libvirt/images/base.raw \
  /var/lib/libvirt/images/overlay.qcow2
qemu-img info --backing-chain /var/lib/libvirt/images/overlay.qcow2
```

覆盖层的虚拟容量通常沿用基础盘。若要迁移或合并链条，应先离线备份，再按目标存储规划 rebase 或 convert；不要直接改名、移动基础盘。

## 5.4 克隆与身份去重

`virt-clone` 从已有域创建新定义和新磁盘，通常生成新的域 UUID 与虚拟网卡 MAC；**来宾内的主机名、静态 IP、机器 ID 和应用身份未必变化**。先关源机并确认；若有多块盘或后备链，要逐一核对克隆范围。

```bash
virsh shutdown SOURCE_VM
virsh domstate SOURCE_VM
virsh domblklist --details SOURCE_VM
virt-clone --original SOURCE_VM --name CLONE_VM \
  --file /var/lib/libvirt/images/clone.qcow2
virsh list --all
virsh domblklist --details CLONE_VM
virsh dumpxml CLONE_VM
```

不要手动复制 `/etc/libvirt/qemu/*.xml` 取代 `virsh edit` 或 `virt-clone`，否则 libvirt 内存定义、UUID、MAC 与磁盘路径可能不一致。首次启动克隆机前先隔离网络，按来宾系统重新配置主机名、静态 IP、机器 ID、SSH 主机密钥或其他应用身份；Windows 模板见第 08 章。分别核对两台机器的身份和业务服务，不只看 `virsh list`。

![源虚拟机与克隆机的历史对照；两者能启动不表示身份已经去重]({{ '/subjects/KVM/assets/p125-img01.webp' | relative_url }})

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/04-network-management.html' | relative_url }}">← 上一章：网络管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/06-resource-management.html' | relative_url }}">下一章：资源管理 →</a>
</nav>
