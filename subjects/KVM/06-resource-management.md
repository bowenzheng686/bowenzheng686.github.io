---
layout: default
title: 'KVM 虚拟化 · 资源管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 06 章 · 资源管理

CPU、内存与磁盘的调整不处在同一层：libvirt 域定义决定虚拟机能看到什么设备，来宾内核决定是否识别热插拔，来宾分区和文件系统决定新增磁盘容量是否可用。操作前先记录原配置和业务负载，明确修改**当前运行态**还是**下次启动的持久配置**，再选择命令。

## 6.1 vCPU：上限、当前值和亲和性

`<vcpu>` 的元素值是最大 vCPU 数，`current` 是启动时使用数。热增加不能超过已配置的上限，也取决于 QEMU/libvirt 版本、CPU 拓扑和来宾热插拔支持。不能凭一个 CentOS 7 实验推断所有来宾都能在线减少 vCPU；公有云能否变更规格还受平台策略约束。

先查宿主可用逻辑 CPU 与虚拟机状态：

```bash
lscpu
cat /sys/devices/system/cpu/online
virsh dominfo VM_NAME
virsh vcpucount VM_NAME
virsh vcpuinfo VM_NAME
virsh dumpxml VM_NAME > VM_NAME.before-cpu.xml
```

历史日志里没有 `cpu0/online` 文件，这是某些内核的正常表现；不应创建 sysfs 文件。“8 个逻辑 CPU”也不等于 8 个独立物理核心，解释性能时还要看插槽、核心与超线程拓扑。

### 先设定最大值，再验证热调整

若原定义只允许 2 个 vCPU，先在维护窗口关机，通过 `virsh edit VM_NAME` 设置最大值与启动值，例如：

```xml
<vcpu placement='static' current='2'>4</vcpu>
```

这表示**启动时 2 个、上限 4 个**，不是“当前 4 个”。启动后分别看 libvirt 和来宾：

```bash
virsh start VM_NAME
virsh vcpucount VM_NAME
virsh setvcpus VM_NAME 3 --live
virsh vcpucount VM_NAME
virsh vcpuinfo VM_NAME
```

`--live` 只改变运行态；来宾内还应检查 `lscpu`、在线 CPU 列表和应用指标。若来宾拒绝热拔出，不能靠强行重试解决，应在下一次重启时变更启动值。希望下次也以 3 个 vCPU 启动，可另执行：

```bash
virsh setvcpus VM_NAME 3 --config
virsh vcpucount VM_NAME
```

`--config` 改持久定义，不代表运行态立即改变。需要回滚时按原记录恢复 live 与 config 的数量，并验证下次启动结果。不要从仍在运行的虚拟机直接修改 `/etc/libvirt/qemu/*.xml` 文件；应使用 libvirt 命令。

### CPU 绑定只在有测量依据时使用

`virsh vcpupin` 控制 vCPU 可在哪些宿主逻辑 CPU 上运行，不增加宿主机总算力。假设宿主 CPU 1 在线，可以临时将来宾 vCPU 0 绑定到它：

```bash
virsh vcpupin VM_NAME 0 1 --live
virsh vcpuinfo VM_NAME
```

若要重启后保持，应核对当前 libvirt 版本支持的 `--config` 用法，再将相同策略写入持久定义。过度绑定会减少调度空间，可能与 NUMA、其他虚拟机或宿主任务争抢；验证时应比较吞吐、延迟和 CPU steal，而不是只看亲和性字符串中的 `y`。

## 6.2 内存：最大值、当前值与气球驱动

域 XML 中 `<memory>` 通常表示启动后可用的上限，`<currentMemory>` 表示启动配置的当前值；它们不等于宿主机瞬时物理占用。内存超配允许配置总量大于物理内存，但若多个来宾同时实际使用，宿主可能交换或 OOM，因此应保留余量并监控。

```bash
virsh dominfo VM_NAME
virsh dommemstat VM_NAME
virsh dumpxml VM_NAME > VM_NAME.before-memory.xml
```

如果来宾安装并启用了 virtio-balloon，可在上限内尝试在线调整：

```bash
virsh setmem VM_NAME 1572864 --live
virsh dominfo VM_NAME
virsh dommemstat VM_NAME
```

此处参数按 KiB 计，1572864 KiB 对应 1536 MiB。缩小前先确认来宾工作集、剩余内存和应用 SLA。libvirt 接受命令并不代表来宾立即释放了预期物理页；应在来宾内同时查看 `free -h`、交换和内存压力。原文用 QEMU HMP 的 `balloon 512` 直接改内存，是底层调试接口；日常配置优先用 `virsh setmem`，避免 libvirt 持久定义与运行态认知不一致。

若目标值超过域的最大内存，先停机并在 `virsh edit` 中调整 `<memory>`、`<currentMemory>`，使数值与单位明确，例如最大 3 GiB、启动 2 GiB：

```xml
<memory unit='MiB'>3072</memory>
<currentMemory unit='MiB'>2048</currentMemory>
```

重新启动后检查 `virsh dominfo` 和来宾实际识别情况。是否支持真正在线增加最大内存，还与内存热插拔设备及来宾支持有关；不能把修改配置文件等同于运行态立即扩容。

## 6.3 扩大现有磁盘：镜像与来宾要分两步

**先确认磁盘链、备份和宿主可用空间。** 对正在运行的 qcow2 文件直接用 `qemu-img resize` 可能遇到锁冲突或造成不一致。以下演示离线扩容；先让虚拟机正常关机并确认已经停止：

```bash
virsh domblklist --details VM_NAME
virsh shutdown VM_NAME
virsh domstate VM_NAME
qemu-img info /var/lib/libvirt/images/system.qcow2
qemu-img resize /var/lib/libvirt/images/system.qcow2 +3G
qemu-img info /var/lib/libvirt/images/system.qcow2
virsh start VM_NAME
```

`qemu-img info` 中虚拟容量增加，仅意味着来宾块设备变大；分区、LVM PV/LV 和文件系统不会自动扩展。原实验从 10 GiB 增到 13 GiB，在十进制工具中约显示 14 GB，这是单位换算而非又增长了 1 GiB。

在来宾内先查看真实拓扑，不要把示例设备名照搬：

```bash
lsblk -f
findmnt /
df -hT
```

若确认 `/dev/vda2` 是某个 LVM PV，且分区后是未分配空间，可按实际分区表和文件系统类型规划：扩展分区（例如用 `growpart`）、执行 `pvresize`，再用 `lvextend -r` 扩大目标 LV 和文件系统。XFS 只能在线增长，ext4 的在线/离线约束也需按实际情况检查。**不应直接对包含数据的分区执行 mkfs，也不应未备份就缩小镜像。** 每一步后检查 `lsblk`、`pvs`、`lvs`、`df -hT`。

## 6.4 新增数据盘、挂载与迁移

新增盘与扩大系统盘是两种方案。先创建文件，再明确 libvirt 目标设备、格式和作用范围：

```bash
qemu-img create -f qcow2 /var/lib/libvirt/images/data.qcow2 2G
virsh domblklist --details VM_NAME
virsh attach-disk VM_NAME /var/lib/libvirt/images/data.qcow2 vdb \
  --driver qemu --subdriver qcow2 --targetbus virtio --live --config
virsh domblklist --details VM_NAME
```

`--live --config` 用于运行中的持久虚拟机，分别更新当前状态和下次启动配置；若虚拟机已经停机，只用 `--config` 并在启动后验证。来宾内的 `/dev/vdb` 不一定和宿主 target 永远一一对应，应以 `lsblk`、容量和设备标识为准。

**以下初始化会清除目标盘已有内容，只对确认的新空盘执行。** 若文件系统直接建在整盘上，可在来宾内：

```bash
lsblk -f
sudo mkfs.ext4 /dev/vdb
sudo mkdir -p /data
sudo blkid /dev/vdb
sudo mount /dev/vdb /data
df -hT /data
```

将 `blkid` 得到的**实际 UUID**写入 `/etc/fstab`，不要复制教程中的 UUID。编辑后先 `sudo mount -a` 并用 `findmnt /data` 验证，再重启抽查；开机挂载失败可能影响启动。

迁移数据盘到另一台虚拟机时，先停止应用写入，在原来宾 `umount /data`，移除或调整其 fstab 条目，确认文件系统干净；随后在宿主机分离并核对：

```bash
virsh detach-disk SOURCE_VM vdb --live --config
virsh domblklist --details SOURCE_VM
virsh attach-disk TARGET_VM /var/lib/libvirt/images/data.qcow2 vdb \
  --driver qemu --subdriver qcow2 --targetbus virtio --live --config
virsh domblklist --details TARGET_VM
```

目标虚拟机必须能访问同一镜像文件；**同一可写文件不能同时接到两台普通虚拟机**。在目标来宾先只读检查文件系统与数据，再按业务需要挂载读写。原日志出现宿主配置写 `vdc`、来宾却看到 `vdb` 的不一致，正说明不能凭设备字母确认磁盘身份。回滚时先在目标机卸载并分离，再接回原机，保持单写者原则。

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/05-image-management.html' | relative_url }}">← 上一章：镜像管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/07-virtualization-principles.html' | relative_url }}">下一章：虚拟化原理 →</a>
</nav>
