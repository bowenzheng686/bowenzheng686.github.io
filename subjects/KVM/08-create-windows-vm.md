---
layout: default
title: 'KVM 虚拟化 · 创建 Windows 虚拟机'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 08 章 · 创建 Windows 虚拟机

本章以 Windows Server 2016 为例，完成安装、VirtIO 驱动配置及模板克隆。与 Linux 来宾相比，关键区别是 Windows 安装程序未必内置所选 VirtIO 设备的驱动：安装时看不到磁盘、首次登录后看不到网卡，通常分别对应存储和网络驱动尚未加载，而不是虚拟机创建失败。

> 文中的镜像名、路径和虚拟机配置是实验示例。实际操作前，应确认 Windows 安装介质、VirtIO 驱动版本和授权条件适用于自己的环境。截图只用于辨认关键界面，驱动目录以命令中配置的设备类型为准。

## 8.1 准备安装介质与驱动

准备 Windows 安装 ISO 和 VirtIO 驱动 ISO，并让运行 libvirt 的宿主机可以读取。VirtIO 驱动可从 [virtio-win 发布目录](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/)获取；旧版本位于[历史版本目录](https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/)。本例使用 `virtio-win-0.1.266.iso`，版本号不是通用要求，选择时应核对驱动包中是否有对应的 Windows 版本目录。

以下三种驱动与本章直接相关：

| 虚拟设备 | 安装阶段或使用阶段 | 驱动 ISO 中的常见目录 |
| --- | --- | --- |
| VirtIO 块设备（`bus=virtio`） | 安装时识别系统盘 | `viostor/2k16/amd64` |
| VirtIO SCSI 控制器（`bus=scsi`，且配置 VirtIO SCSI 控制器） | 安装时识别系统盘 | `vioscsi/2k16/amd64` |
| VirtIO 网卡（`model=virtio`） | 系统安装后识别网卡 | `NetKVM/2k16/amd64` |

**存储总线与驱动必须对应。** 本章的创建命令使用 `bus=virtio`，因此在 Windows 安装程序中应加载 `viostor`，而非 `vioscsi`。原实验截图展示过 `vioscsi` 目录，那对应另一种磁盘控制器配置，不能照着截图与本章命令混用。不同驱动 ISO 的目录名称可能略有差异，应以 ISO 实际内容为准。

VirtIO 让来宾系统通过为虚拟化设计的设备和驱动完成 I/O，通常比完全模拟旧式硬件更高效。并非所有 Windows 虚拟机都“必须”使用 VirtIO：IDE/SATA 磁盘或模拟网卡可能可以直接安装，但性能和功能取舍不同；这里选择 VirtIO，因此需要额外加载驱动。

## 8.2 创建虚拟机

先确认镜像文件和桥接网络存在，并为系统盘选定足够的空间。以下命令示例使用 2 个 vCPU、4 GiB 内存和 20 GiB QCOW2 系统盘；实际资源应满足所选 Windows 版本及工作负载的要求。

````bash
ls -lh /data/images/cn_windows_server_2016_x64_dvd_9718765.iso \
       /data/images/virtio-win-0.1.266.iso
ip link show br0
osinfo-query os | grep -i 'win2k16'
````

若本机 `osinfo-query` 列出的系统标识不同，应将下面的 `--os-variant` 调整为实际可用的值。`--cdrom` 指向 Windows 安装介质；第二个只读光驱装载 VirtIO 驱动 ISO。

````bash
virt-install \
  --name win2016 \
  --virt-type kvm \
  --os-variant win2k16 \
  --memory 4096 --vcpus 2 \
  --cdrom /data/images/cn_windows_server_2016_x64_dvd_9718765.iso \
  --disk path=/opt/win2016.qcow2,size=20,format=qcow2,bus=virtio \
  --disk path=/data/images/virtio-win-0.1.266.iso,device=cdrom \
  --network bridge=br0,model=virtio \
  --graphics vnc,listen=127.0.0.1 \
  --noautoconsole
````

这里将 VNC 绑定在宿主机回环地址；可在宿主机图形桌面使用 `virt-manager` 打开控制台。远程管理时应通过受控连接访问 libvirt 或控制台，不要为了连接方便直接把未加密的 VNC 暴露到公网。创建后可用 `virsh list --all` 确认域存在并查看状态。

## 8.3 安装 Windows 并加载存储驱动

在虚拟机控制台启动 Windows 安装程序，选择语言、系统版本并接受许可条款；安装类型选择“自定义”。这些向导页面不影响 KVM 配置，本章不逐屏重复。

如果“你想将 Windows 安装在哪里？”没有显示目标磁盘，点击“加载驱动程序”，浏览 VirtIO 光驱，选择与**本章 `bus=virtio` 命令**对应的 `viostor/2k16/amd64` 目录，然后继续加载。若更改了虚拟磁盘总线或 Windows 版本，需重新匹配驱动，不能只按截图中的目录名选择。

驱动加载后，安装目标列表应出现约 20 GiB 的虚拟磁盘；若仍为空，依次核对域的磁盘总线、驱动目录的系统版本与架构、VirtIO ISO 是否成功挂载。确认目标盘后继续安装，等待自动重启和首次启动，不需要依据旧截图中的固定耗时判断是否成功。

![加载匹配的存储驱动后，安装程序显示虚拟磁盘]({{ '/subjects/KVM/assets/p169-img02.webp' | relative_url }})

首次登录时为管理员设置独立密码。若控制台截获了组合键，可在 `virt-manager` 的“发送按键”菜单发送 Ctrl+Alt+Del。密码及画面布局可能随 Windows 版本不同而变化。

## 8.4 安装 VirtIO 网卡驱动

桌面已出现但网络未连接时，先在“设备管理器”检查网卡或带感叹号的以太网设备。对该设备选择“更新驱动程序”→“浏览我的计算机以查找驱动程序”，指向 VirtIO 光驱中的 `NetKVM/2k16/amd64`（或选择驱动光驱根目录并勾选“包括子文件夹”）。**不要将存储驱动 `viostor` 用作网卡驱动。**

![在设备管理器中定位尚未识别的网络设备]({{ '/subjects/KVM/assets/p175-img01.webp' | relative_url }})

![驱动安装完成后的设备状态]({{ '/subjects/KVM/assets/p177-img02.webp' | relative_url }})

安装后检查设备管理器中是否出现 VirtIO Ethernet Adapter，再验证 IP 地址与连通性；仅凭任务栏图标颜色不足以证明桥接网络、DHCP 和路由均正常。在来宾 PowerShell 中可运行：

````powershell
Get-NetAdapter
Get-NetIPConfiguration
Test-NetConnection <网关或已知可达地址>
````

如果驱动已安装而仍未联网，继续核对宿主机 `br0` 的配置、虚拟网卡连接状态及来宾的地址设置。其他未识别设备可按设备硬件 ID 和驱动 ISO 中的相应目录逐一匹配，不应一概使用同一个驱动，也不应忽略仍有警告标志的设备。

## 8.5 制作通用模板并克隆

直接复制已配置的系统盘可能把计算机名、网络设置和系统定制状态一并带入克隆机。先完成必要更新与驱动安装，并清理临时数据；然后在来宾系统中运行 Sysprep，选择“进入系统全新体验(OOBE)”、勾选“通用”、关机。命令行与图形界面等价的示例为：

````powershell
& "$env:WINDIR\System32\Sysprep\Sysprep.exe" /oobe /generalize /shutdown
````

![Sysprep 中选择 OOBE、通用和关机]({{ '/subjects/KVM/assets/p180-img02.webp' | relative_url }})

等待虚拟机**完全关机**后再克隆，不要先重新启动模板；否则模板自身也会进入首次配置流程。`whoami /user` 显示的是当前账户 SID，不能据此验证所谓“机器 SID 已被去除”。Sysprep 的目的也不只是更换 SID，还包括重置一系列系统专有状态；克隆后仍需按部署要求分别设置计算机名、网络、授权及应用配置。

在宿主机确认源虚拟机状态，随后克隆系统盘和虚拟机定义：

````bash
virsh domstate win2016
virt-clone --original win2016 \
  --name win2016-2 \
  --file /opt/win2016-2.qcow2
virsh list --all
virsh domblklist win2016-2
````

`virt-clone` 会为克隆机生成新的虚拟机标识与网卡 MAC；克隆完成后仍应检查域定义及光驱挂载情况，并在不再需要时卸载安装 ISO。保持源模板关机，将其作为后续克隆的起点。

启动 `win2016-2`，在 OOBE 中完成首次配置，再检查系统盘、网卡、计算机名、IP 与业务应用。看到首次配置页面只能说明 Sysprep 流程进入了预期阶段，不能代替这些验证。

![克隆机首次启动进入 OOBE 配置]({{ '/subjects/KVM/assets/p182-img01.webp' | relative_url }})

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/07-virtualization-principles.html' | relative_url }}">← 上一章：虚拟化原理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
</nav>
