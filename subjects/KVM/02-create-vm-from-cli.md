---
layout: default
title: 'KVM 虚拟化 · 命令创建虚拟机'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 02 章 · 命令创建虚拟机

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 2.1 常见命令

### 基础知识

**工具体系**

![原文插图（第 48 页）]({{ '/subjects/KVM/assets/p048-img01.webp' | relative_url }})

本章用三个层次的工具：

QEMU 提供设备模拟和虚拟机进程；启用 KVM 加速后，CPU 虚拟化由内核模块与硬件扩展协作完成。`qemu-img` 管理磁盘镜像。libvirt 则在上层提供统一管理接口，`virt-install`、`virsh` 和 `virt-manager` 都可借助它工作。

具体分工是：`qemu-img` 创建或检查磁盘镜像，`virt-install` 通过 libvirt 定义并启动虚拟机，`virsh` 管理其生命周期。`virt-manager` 提供图形界面；它们不是互不兼容的“两套管理工具”。

### 配置保存在哪里

libvirt 将来宾定义、虚拟网络和存储池信息分别管理。传统 QEMU/libvirt 安装中常能在 `/etc/libvirt/qemu/` 看到域 XML，在 `networks/` 看到网络定义；实际路径可能因发行版和守护进程布局不同而变化。日常查看与编辑应通过 `virsh`，而不是直接改写这些文件：

```bash
virsh list --all
virsh dumpxml CentOS-7-x86_64
virsh net-list --all
virsh pool-list --all
```

创建虚拟机时，`virt-install` 会把来宾名称、资源、磁盘与网络写入 libvirt 定义。后续 `virsh` 查到的内容才是核对当前配置的依据。

### 用工作流理解 virt-install

`virt-install` 创建并定义虚拟机，`virsh` 管理生命周期，`qemu-img` 处理磁盘镜像。与其阅读整页 `--help` 输出，不如先确定四个问题：来宾从哪里安装、磁盘保存在哪里、接入哪张网络、如何连接控制台。

| 任务 | 常用参数 | 需要核对的内容 |
| --- | --- | --- |
| 标识与资源 | `--name`、`--memory`、`--vcpus` | 名称唯一，内存和 vCPU 不超出容量规划 |
| 安装来源 | `--cdrom`、`--location`、`--import` | ISO 安装、网络安装和已有系统盘是三种不同路径 |
| 磁盘 | `--disk path=...,format=qcow2` | 路径、格式、容量、权限和是否已有数据 |
| 网络 | `--network network=default,model=virtio` 或 `bridge=br0` | NAT 网络与宿主机桥接不是同一拓扑 |
| 图形与控制台 | `--graphics`、`--console`、`--noautoconsole` | 与来宾安装方式匹配，避免暴露 VNC 到不受控网络 |
| 来宾类型 | `--osinfo` | 用 `virt-install --osinfo list` 查当前支持值 |

`--cdrom` 通常启动交互式 ISO 安装；`--location` 可配合内核参数做自动化安装；`--import` 直接启动已有可引导磁盘，不会替来宾安装系统。涉及已有镜像时，先确认它是否为系统盘，不能对空白磁盘直接使用 `--import` 期待进入操作系统。

完整参数可在当前主机运行 `virt-install --help` 或阅读 `man virt-install`。帮助输出随版本变化，旧讲义的长清单不应作为固定命令模板。

## 2.2 初始化

### 基础知识

#### 创建磁盘

本例先创建 10 GiB 的 raw 磁盘，再用 ISO 安装来宾系统。CentOS 7 已结束常规维护，镜像在这里仅作历史实验；新环境应选仍受支持的来宾系统。磁盘路径可按宿主机存储规划调整，不必固定放在 `/opt`。

`qemu-img create` 创建的 raw 文件可采用稀疏分配：`ls -lh` 显示逻辑容量，`du -h` 显示实际占用。写入数据后实际占用会增长，不能只看初始大小判断存储是否足够。

````bash
qemu-img create -f <磁盘格式> <镜像路径> <虚拟容量>
````

创建前确认目标文件不存在，避免覆盖已有数据。

````console
[root@kvm-host ~]# qemu-img create -f raw /opt/CentOS-7-x86_64.raw 10G
Formatting '/opt/CentOS-7-x86_64.raw', fmt=raw size=10737418240
````

创建后核对逻辑容量与实际占用：

````console
[root@kvm-host ~]# ls -lh /opt/CentOS-7-x86_64.raw
-rw-r--r-- 1 root root 10G 3月 24 22:59 CentOS-7-x86_64.raw
[root@kvm-host ~]# du -h /opt/CentOS-7-x86_64.raw
1.0M /opt/CentOS-7-x86_64.raw
````

#### 创建虚拟机

使用 `virt-install` 将 ISO、磁盘、网络和资源组合为虚拟机定义。本例配置 VNC 只监听宿主机回环地址；可从宿主机本地连接，或先建立 SSH 隧道再用远端客户端，不需要在命令执行前暴露 VNC 端口。

````console
[root@kvm-host ~]# virt-install --virt-type kvm --name CentOS-7-x86_64 \
  --memory 1024 --vcpus 1 \
  --cdrom /data/images/CentOS-7-x86_64-Minimal-2009.iso \
  --disk path=/opt/CentOS-7-x86_64.raw,format=raw,bus=virtio \
  --network network=default,model=virtio \
  --graphics vnc,listen=127.0.0.1 --noautoconsole
````

`--memory 1024` 以 MiB 为单位分配 1 GiB 内存，`--vcpus 1` 指定一个虚拟 CPU。`--cdrom` 指向安装 ISO，`--disk` 指向前一步创建的系统盘，`--network network=default` 接入 libvirt 默认 NAT 网络。`--noautoconsole` 仅表示命令完成后不自动打开控制台，不影响来宾能否使用 VNC。

#### 连接虚拟机

先查询来宾控制台信息，再选择本地管理器或 VNC 客户端连接。

![原文插图（第 54 页）]({{ '/subjects/KVM/assets/p054-img01.webp' | relative_url }})

先用 `virsh vncdisplay CentOS-7-x86_64` 查询显示编号；若沿用旧截图的远程 VNC 连接方式，必须确认服务监听地址和访问控制。上方新示例只监听 `127.0.0.1`，远程客户端需要通过 SSH 隧道或本地管理器连接，不能直接输入宿主机地址。

![原文插图（第 54 页）]({{ '/subjects/KVM/assets/p054-img02.webp' | relative_url }})

VNC 显示号与端口通常有对应关系，但仍应以 `virsh vncdisplay <虚拟机名>` 和实际监听地址为准。旧截图里的 `192.0.2.12` 不能直接连到上方仅监听 `127.0.0.1` 的实例。

![原文插图（第 55 页）]({{ '/subjects/KVM/assets/p055-img01.webp' | relative_url }})

#### 系统安装

启动 ISO 安装程序后，按来宾发行版的安装向导配置语言、网络、磁盘和账户。旧实验在启动项后添加 `net.ifnames=0 biosdevname=0`，这会改变网卡命名方式；除非确实依赖传统接口名，否则无需照做，应以安装后实际接口名配置网络。

![原文插图（第 55 页）]({{ '/subjects/KVM/assets/p055-img02.webp' | relative_url }})

确保安装器中启用网卡并确认地址获取方式（DHCP 或静态配置）；虚拟网卡接入默认 NAT 网络并不保证来宾内部自动启用网络。

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img01.webp' | relative_url }})

示例选择最小化安装；生产用途还应核对软件包、驱动与系统维护周期。

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img02.webp' | relative_url }})

检查 ISO 安装源与目标磁盘，避免把系统装到错误的设备。

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img03.webp' | relative_url }})

为来宾设置独立强密码或 SSH 密钥，不使用固定教程密码；安装完成后按组织要求更新系统。

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img04.webp' | relative_url }})

安装完成后重启来宾，再确认它从系统盘启动，能够登录并访问网络。

### 简单操作

#### 连接虚拟机

安装程序退出或虚拟机关机后，可在宿主机用 `virsh list --all` 确认状态，再视情况执行 `virsh start <名称>`。不要把安装阶段一次重启失败归因于 VNC 本身。

`virsh start` 用于启动已定义但处于关闭状态的来宾；运行 ID 可能变化，因此后续操作仍应使用名称。

````console
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
````

控制台能够登录后，还需要从来宾内部检查 IP 与默认路由。

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img01.webp' | relative_url }})

旧截图中的地址仅是当时的实验结果，应以当前网络配置为准。

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img02.webp' | relative_url }})

若来宾无法访问外部网络，先检查默认网关，再回到宿主机核对 libvirt 网络和转发规则。

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img03.webp' | relative_url }})

可以看到：操作方式是跟正常操作linux系统的方式是一致的。

#### 宿主机检查

来宾启动后，宿主机一般会出现对应的 QEMU 进程；若接入 libvirt 默认 NAT 网络，还会出现 `virbr0` 网桥及 `vnet*` 端口。网桥通常有 IPv4 网关地址，`vnet*` 是来宾网卡接入点，不要求它自己配置 IPv4 地址。

```bash
ip -brief address show virbr0
virsh domiflist CentOS-7-x86_64
virsh domblklist CentOS-7-x86_64
virsh dominfo CentOS-7-x86_64
```

`domiflist` 中的接口名可与宿主机 `ip link show` 对照。若来宾无法联网，依次检查来宾 IP/默认路由、虚拟网卡所属网络、libvirt NAT 网络状态及宿主机转发与防火墙，而不是直接修改 `vnet*` 地址。

一台运行中的来宾通常对应一个 QEMU 进程，vCPU 在其中以线程运行。查看进程可帮助排障，但正常关机、暂停或强制停止都应通过 `virsh` 完成；直接终止 QEMU 进程可能造成数据丢失。
#### 配置解析

##### 配置目录

**虚拟机配置**

````console
[root@kvm-host ~]# tree /etc/libvirt/qemu
/etc/libvirt/qemu
├── autostart
├── CentOS-7-x86_64.xml
└── networks
    ├── autostart
    │ └── default.xml -> ../default.xml
    └── default.xml
3 directories, 3 files
可以看到：
    我们创建的虚拟机配置文件都在 /etc/libvirt/qemu 目录下
    这个目录下的networks目录是存放的虚拟机的网络配置，文件名称是default.xml
    CentOS-7-x86_64.xml是我们定义的虚拟机的配置文件，原则上，这个文件只能用virsh edit进行编
辑
````

##### 读取虚拟机定义

libvirt 把虚拟机定义保存为 XML。直接改写 `/etc/libvirt/qemu/*.xml` 可能被守护进程覆盖；查看当前定义用 `virsh dumpxml <虚拟机名>`，需要修改时用 `virsh edit <虚拟机名>`，并在改动前导出备份。

```bash
virsh dumpxml CentOS-7-x86_64 > CentOS-7-x86_64.xml.bak
virsh edit CentOS-7-x86_64
```

以下是**结构示意**，只保留与本案例有关的关键节点，不是可直接导入的完整域定义：

```xml
<domain type='kvm'>
  <name>CentOS-7-x86_64</name>
  <memory unit='KiB'>1048576</memory>
  <vcpu>1</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/opt/CentOS-7-x86_64.raw'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <graphics type='vnc' autoport='yes' listen='127.0.0.1'/>
  </devices>
</domain>
```

`<memory>` 的单位在此为 KiB，`1048576` 约等于 1 GiB；`<vcpu>` 给出来宾可用的虚拟 CPU 数；`<source file>` 指向宿主机磁盘镜像，`<target bus='virtio'>` 决定来宾看到的磁盘接口；`network='default'` 连接 libvirt 默认网络。显卡和控制台设置随安装方式变化，不应把旧实验中监听 `0.0.0.0` 的 VNC 配置当作默认做法。

机器类型、CPU 模型和 PCI 地址由 libvirt/QEMU 按宿主环境生成；迁移到另一台宿主机前应检查兼容性，不能直接复制旧主机的完整 XML 文件。

### 用 virsh 管理虚拟机

#### 先辨认状态和定义

`virsh list` 只显示运行中的来宾；`virsh list --all` 还显示已关闭的来宾。列表中的 ID 是一次运行实例的编号，重启后可能变化；脚本和操作说明应使用稳定的虚拟机名称或 UUID，而不是 ID。

```bash
virsh list --all
virsh dominfo CentOS-7-x86_64
virsh domblklist CentOS-7-x86_64
virsh domiflist CentOS-7-x86_64
```

`domblklist` 与 `domiflist` 分别核对磁盘和网卡。定义中的设备路径可能指向已有数据，修改或删除前必须先确认对象。

#### 临时域与持久域

`virsh create <XML 文件>` 按 XML 启动**临时域**：来宾关闭后，这个定义不再保留。`virsh define <XML 文件>` 注册**持久域**：定义会保留，之后再用 `virsh start <名称>` 启动。已由 `virt-install` 创建的来宾通常已经是持久域，不需要再次 `define`。

```bash
virsh dumpxml CentOS-7-x86_64 > CentOS-7-x86_64.xml.bak
virsh dominfo CentOS-7-x86_64
# 只有确需从独立 XML 注册新定义时才执行：
virsh define /path/to/new-domain.xml
virsh start NEW_VM
```

**不要通过只改 `<name>` 和 `<uuid>` 复制正在运行的来宾。** 若两个定义仍指向同一可写系统盘，第二个来宾可能因文件锁启动失败；即使绕过锁，同时写入也会破坏文件系统。新来宾必须有独立磁盘和网卡标识。复制已有系统可用后文的 `virt-clone`；仅需保留配置则导出 XML，而不是复制整个 `/etc/libvirt/qemu` 目录。

#### 图形与串口控制台

来宾启用 VNC 时，先查询 libvirt 返回的地址，而非猜测端口。上节的示例让 VNC 只监听 `127.0.0.1`，因此远端客户端需先建立受控连接通道，不能直接访问宿主机公网地址。

```bash
virsh domdisplay CentOS-7-x86_64
virsh vncdisplay CentOS-7-x86_64
```

旧实验截图展示了通过 VNC 客户端连接的界面；显示号 `:0` 通常对应 5900 端口，但实际访问仍以当前监听地址与配置为准。

![原文插图（第 66 页）]({{ '/subjects/KVM/assets/p066-img01.webp' | relative_url }})

若来宾配置了串口设备，且操作系统在串口上启动登录服务，可在宿主机执行 `virsh console <名称>`。很多 ISO 安装的系统默认未启用串口登录；需要在**来宾内部**配置内核控制台和 `serial-getty@ttyS0.service`，而不是只在宿主机上运行 `grubby`。以下命令是来宾使用 GRUB 时的一种做法，具体应以发行版启动配置为准：

```bash
# 在来宾内部执行，先确认存在 ttyS0，再修改启动参数
sudo grubby --update-kernel=ALL --args='console=ttyS0,115200n8'
sudo systemctl enable --now serial-getty@ttyS0.service
# 回到宿主机，来宾重启后连接
virsh console CentOS-7-x86_64
```

在 `virsh console` 中按 `Ctrl+]` 返回宿主机终端。若无法登录，检查域 XML 的串口设备、来宾的内核参数及 getty 服务；不要把黑屏直接归因于 libvirt 故障。

### 生命周期操作

#### 暂停与恢复

`virsh suspend` 暂停来宾的 vCPU 执行，内存状态仍占用宿主机资源；它不是保存状态或关机。需要继续运行时执行 `virsh resume`。暂停期间图形画面停止刷新，下面的截图是旧实验的可见效果。

```bash
virsh suspend CentOS-7-x86_64
virsh domstate CentOS-7-x86_64
virsh resume CentOS-7-x86_64
```

![原文插图（第 68 页）]({{ '/subjects/KVM/assets/p068-img01.webp' | relative_url }})

恢复后应看到 `domstate` 回到 `running`，并在来宾内部确认业务正常；不要仅凭 VNC 画面重新变化判断应用已经恢复。

![原文插图（第 69 页）]({{ '/subjects/KVM/assets/p069-img01.webp' | relative_url }})

#### 正常关机与强制停止

优先使用 `virsh shutdown` 请求来宾操作系统正常关机，它依赖 ACPI 或来宾代理等机制响应，命令返回后状态可能仍暂时为 `running`。用 `virsh domstate` 等待确认；来宾长期无响应时，再考虑 `virsh destroy` 强制断电，并评估未写入数据的风险。`destroy` 不删除磁盘或定义。

```bash
virsh shutdown CentOS-7-x86_64
virsh domstate CentOS-7-x86_64
# 仅在正常关机失败且已接受断电风险时执行：
virsh destroy CentOS-7-x86_64
```

旧系统若缺少 ACPI 支持或关机服务配置，先从来宾内部排查，不要把安装 `acpid` 当作所有来宾的通用步骤。恢复运行用 `virsh start`，而不是 `resume`；后者只适用于暂停状态。

#### 开机自启动与取消

自启动属于**持久域定义**。启用后，libvirt 在宿主机启动流程中尝试启动来宾；是否成功还受存储池、网络、服务顺序及资源容量影响。先核对目标定义和依赖，再执行：

```bash
virsh autostart CentOS-7-x86_64
virsh list --all --autostart
# 取消时：
virsh autostart --disable CentOS-7-x86_64
virsh list --all --no-autostart
```

不要只依据 `/etc/libvirt/qemu/autostart/` 中的符号链接判断所有发行版的行为；以 `virsh` 查询及一次计划内重启验证为准。

#### 注销定义

`virsh undefine` 注销持久域定义，**默认不会删除磁盘**。应先备份 XML，确认来宾已关闭，检查其磁盘是否还被快照或其他定义使用，再根据保留数据的意图决定后续清理。带有 UEFI NVRAM 或快照元数据的来宾可能还需附加选项，应先阅读当前版本的 `virsh help undefine`。

```bash
virsh dumpxml OLD_VM > OLD_VM.xml.bak
virsh shutdown OLD_VM
virsh domstate OLD_VM
virsh domblklist OLD_VM
virsh undefine OLD_VM
```
### 备份定义、克隆与编辑

`virsh dumpxml` 导出的是**虚拟机定义**，不是系统盘数据备份。保存 XML 可以帮助回看配置，但若把它改个名称和 UUID 就 `virsh define`，新旧虚拟机仍可能指向**同一个可写磁盘**，并造成文件系统损坏。要制作独立副本，应先正常关机，再使用 `virt-clone` 或在确认格式和链关系后复制磁盘，并核对新虚拟机的磁盘路径、MAC 地址与来宾标识。

```bash
virsh shutdown CentOS-7-x86_64
virsh domstate CentOS-7-x86_64
virsh dumpxml CentOS-7-x86_64 > CentOS-7-x86_64.xml.bak
virt-clone --original CentOS-7-x86_64 \
  --name CentOS-7-x86_64-copy \
  --file /var/lib/libvirt/images/CentOS-7-x86_64-copy.raw
virsh domblklist CentOS-7-x86_64-copy
virsh domiflist CentOS-7-x86_64-copy
```

`virt-clone` 的可用选项与源镜像格式、存储池有关，执行前运行 `virt-clone --help`；源虚拟机应处于已关机状态。克隆后的来宾还可能保留原主机名、系统身份与静态 IP，首次启动前应制定变更方案。真正的数据备份仍需要独立副本和恢复验证。

编辑现有虚拟机使用 `virsh edit <名称>`，改动前导出 XML，改动后用 `virsh dumpxml` 核对，必要时重启来宾以使设备设置生效。编辑图形控制台时，不要把旧实验中 `listen='0.0.0.0'` 加固定密码的 VNC 配置直接用于共享网络；优先保持回环监听并通过 SSH 隧道或受控管理界面访问。

下列两张原课程图片记录旧实验修改 VNC 配置与连接结果，供识别界面；其中固定端口和密码不作为推荐配置。

![旧版 VNC 编辑界面]({{ '/subjects/KVM/assets/p076-img01.webp' | relative_url }})

![旧版 VNC 登录结果]({{ '/subjects/KVM/assets/p077-img01.webp' | relative_url }})

## 2.3 其他内容

### 查询来宾系统类型

`virt-install` 的 `--osinfo` 值来自当前宿主机的 osinfo 数据库。支持列表与版本会变化，不要把旧实验中数百行的操作系统名称当成兼容性承诺；“有名称”也不代表安装镜像仍获得安全更新。

```bash
virt-install --osinfo list | grep -i centos
virt-install --osinfo list | grep -i win
```

选择与来宾版本相符的标识；如果安装介质较新而本机列表过旧，先更新 osinfo 数据和相关工具，再参考当前文档选择相近配置并测试驱动、启动和网络功能。

### 让 virt-install 创建新磁盘

上面的主案例先用 `qemu-img` 创建磁盘；也可以在 `virt-install --disk` 中同时给出路径、容量与格式，由工具创建**新的空白磁盘**，再从 ISO 安装系统。这不等于「无磁盘虚拟机」，也不能把空盘与 `--import` 混用。

先查询当前宿主机支持的系统标识；这里的 CentOS 7 仅用于重现旧实验，新部署应选择受支持版本。

````console
[root@kvm-host ~]# virt-install --osinfo list |grep centos7
centos7, centos7.0
````

确认镜像路径和目标磁盘路径均可由 libvirt 访问，且目标文件尚不存在，然后创建来宾：

````console
[root@kvm-host ~]# virt-install --virt-type kvm --osinfo centos7 --name centos7 \
  --memory 1024 --vcpus 1 \
  --cdrom /data/images/CentOS-7-x86_64-Minimal-2009.iso \
  --disk path=/opt/centos7-new.qcow2,size=10,format=qcow2,bus=virtio \
  --network network=default,model=virtio \
  --graphics vnc,listen=127.0.0.1 --noautoconsole
````

创建后执行 `virsh domblklist centos7` 和 `qemu-img info /opt/centos7-new.qcow2`，分别确认来宾挂载的磁盘路径及镜像格式/容量；不要只看 `virsh list` 中是否出现名称。

### 桥接方式创建VM

桥接方式让来宾通过宿主机外部桥接入局域网，与 `network=default` 的 libvirt NAT 网络不同。先按第 04 章建立并验证宿主机桥 `br0`，核对物理网卡、DHCP 与防火墙策略，再创建来宾；不要把 `virbr0` 当作外部桥。

````console
[root@kvm-host ~]# virt-install --virt-type kvm --osinfo centos7 --name centos7-bridge \
  --memory 1024 --vcpus 1 \
  --cdrom /data/images/CentOS-7-x86_64-Minimal-2009.iso \
  --disk path=/opt/centos7-bridge.qcow2,size=10,format=qcow2,bus=virtio \
  --network bridge=br0,model=virtio \
  --graphics vnc,listen=127.0.0.1 --noautoconsole
````

两台来宾必须使用**不同的可写磁盘镜像**。创建后通过 `virsh domiflist centos7-bridge` 确认网卡确实连接 `br0`，并在来宾内检查 IP 地址与网关。

### 克隆VM

命令行可用上一节的 `virt-clone`，图形界面则可在 `virt-manager` 中选择已关机的源虚拟机并执行克隆。克隆应产生独立磁盘，不能只复制虚拟机定义。

````console
[root@kvm-host ~]# virt-manager
````

下列截图展示旧版向导；实际操作时要核对新名称与目标磁盘路径。

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img01.webp' | relative_url }})

完成克隆后先检查 `domblklist`，再启动新来宾。

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img02.webp' | relative_url }})

首次登录还应调整来宾内部的主机名、固定 IP 和身份信息，避免克隆实例与原实例冲突。

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img03.webp' | relative_url }})

### 本章要点

创建虚拟机前确认安装镜像、独立磁盘、网络和控制台访问方式；运行后用 `virsh dominfo`、`domblklist` 和 `domiflist` 分别核对资源、磁盘与网卡。关闭、强制断电、取消定义和删除磁盘是不同操作，先确认影响范围再执行。

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/01-virtualization-basics.html' | relative_url }}">← 上一章：虚拟化基础</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/03-storage-management.html' | relative_url }}">下一章：存储管理 →</a>
</nav>
