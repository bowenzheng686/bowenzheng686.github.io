---
layout: default
title: 'KVM 虚拟化 · 虚拟化基础'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 01 章 · 虚拟化基础

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 1.1 虚拟化基础

### 基础知识

#### 技术发展趋势

![原文插图（第 8 页）]({{ '/subjects/KVM/assets/p008-img01.webp' | relative_url }})

#### 传统基础设施

![原文插图（第 8 页）]({{ '/subjects/KVM/assets/p008-img02.webp' | relative_url }})

**常见工作内容**

- IDC选择,如:联通,电信,世纪互联,鹏博士等
- 网络和存储规划
- 服务器选型及采购
- 服务器系统选择、系统安装、上架、配置网络
- 应用规划及部署
- 域名选择及注册,DNS配置名称解析
- 测试外网访问

**面对问题**

1. **资源利用率不均。** 每套业务独占物理服务器时，低负载机器的空闲容量难以直接分配给其他业务。
2. **扩缩容慢。** 已购置的硬件资源不易按短期负载变化调整，需要重新采购或迁移。
3. **交付与迁移耗时。** 系统安装、网络配置及业务迁移如果主要依靠人工，标准化程度和速度都会受限。
4. **成本较高。** 多套独立硬件增加采购、机房、电力和维护投入。虚拟化可改善其中一部分问题，但不能消除硬件和运维成本。

#### 虚拟化技术

##### 技术理解

**虚拟化技术是什么**

虚拟化（Virtualization）把物理 CPU、内存、存储和网络设备抽象为来宾系统可见的虚拟资源，使一台宿主机能运行多台相互隔离的虚拟机。资源分配可以灵活调整，但仍受物理容量、I/O 争用和故障域约束；虚拟化的目标是提高交付和管理弹性，而不是保证资源利用率必然最大。

参考资料可从 [KVM 项目文档](https://www.linux-kvm.org/page/Main_Page) 与后文的 libvirt 文档继续阅读。

##### 一个直观例子

一台物理主机可以向多台虚拟机分别呈现 vCPU、内存、磁盘和网卡。每台虚拟机拥有独立的操作系统视图，但底层资源仍由宿主机共享和调度。隔离使业务互不直接干扰；资源规划不足或宿主机故障仍可能同时影响多台虚拟机。

##### 虚拟化优势

**简介**

虚拟化能缩短环境交付时间，便于统一管理和在满足兼容条件时迁移工作负载。是否降低总成本、提高可用性，取决于容量规划、自动化程度、冗余设计及许可费用，不能由“使用虚拟机”本身保证。

**其优势包括：**

- 在监控和容量规划前提下进行一定程度的资源超配；配置内存总量高于物理内存并不代表可同时实际使用。
- 降低资金成本和运维成本
- 配合冗余、监控和迁移策略减少计划内停机；单宿主机故障仍会影响其上的来宾。
- 提高 IT 部门的工作效率和响应能力
- 加快应用和资源的调配速度
- 提高业务连续性和灾难恢复能力
- 简化数据中心管理
- 借助独立网络命名空间和虚拟网络减少配置相互干扰；IP 与端口冲突仍需正确规划。
- 在硬件与驱动兼容范围内运行部分旧系统或应用；仍需考虑其安全维护状态。

##### 虚拟化目标

从时间维度看，多个来宾可由宿主机调度并发运行；从空间维度看，多台来宾共享一台物理主机的容量。两者都以隔离与资源控制为前提，不能把“并发”理解为 CPU、内存和磁盘都不再存在竞争。

![原文插图（第 10 页）]({{ '/subjects/KVM/assets/p010-img01.webp' | relative_url }})

##### 虚拟化技术发展

![原文插图（第 11 页）]({{ '/subjects/KVM/assets/p011-img01.webp' | relative_url }})

大型机时代就有分时和虚拟机技术。个人计算机普及后，计算形态更加分散；随后 x86 性能、硬件辅助扩展和数据中心整合需求推动服务器虚拟化广泛应用。它并非经历了一个完全“消失”的阶段，今天也与容器、云平台共同存在。

### 虚拟分类

#### 应用级别分类

**主要方向**

**服务器虚拟化**

服务器虚拟化支持在单个物理服务器上运行多个操作系统,每个操作系统作为虚拟机独立运行。

**网络虚拟化**

通过软件定义网络(Software Defined Network，SDN)，即网络的创建不再依赖于物理设备，如公有云厂商支持用户自己通过配置界面创建新的网络，在 KVM、docker、kubernetes、openstack等虚拟化技术中都使用到了网络虚拟化。

**桌面虚拟化**

将桌面部署为托管的服务,使 IT 组织能够更快地响应不断变化的工作场所需求和新出现的机会。还可以将虚拟化桌面和应用快速、轻松地交付给分支机构、外包和远程员工以及使用 iPad 和 Android 平板电脑的移动员工。

**其他方向**

- **应用虚拟化：** 将应用执行环境与底层系统抽象或隔离；在线办公服务不一定属于应用虚拟化。
- **存储虚拟化：** 将多个物理存储资源组织为统一的逻辑存储池，Ceph 等可提供分布式存储能力；NFS/Samba 是网络文件共享协议或服务，不等同于存储虚拟化本身。
- **兼容层：** Wine、CrossOver 通过兼容接口运行部分 Windows 程序，与虚拟整台机器不同。
- **容器：** Docker、Podman、containerd、LXC 等利用操作系统内核的隔离能力运行工作负载；容器共享宿主机内核，不是完整的虚拟机。

#### 应用技术分类

##### 系统层面

**模拟**

模拟器以软件实现来宾所见的处理器或设备，因此可在不同架构之间运行，例如在 x86 宿主机模拟 ARM 来宾；代价通常是较高的指令处理开销。QEMU 既能纯软件模拟，也能与 KVM 结合使用，不能简单归为“只做低速模拟”。

**全虚拟化**

全虚拟化强调来宾系统无需为虚拟化专门修改内核，就能看到足以启动和运行的虚拟硬件。实现可以依赖软件翻译，也可以使用硬件辅助；它与“是否使用硬件扩展”是两个不同维度。

**半虚拟化**

半虚拟化表示来宾与虚拟化平台协作，例如加载 VirtIO 驱动以高效访问虚拟设备。它不等于“只虚拟出部分功能”，也不必然要求修改来宾内核源码；闭源系统安装相应驱动后同样可以使用半虚拟化 I/O。早期 Xen 的半虚拟化来宾与现代 KVM/VirtIO 应区分讨论。

**硬件辅助虚拟化**

硬件辅助虚拟化利用 Intel VT-x、AMD-V 等 CPU 扩展运行来宾，并可借助 EPT/NPT 加速地址转换。KVM、现代 Xen 和多种商业 Hypervisor 都能使用这些能力；它是实现手段，不是与全虚拟化互斥的来宾类型。

**代表软件**

Xen 与 KVM 是两条重要的开源服务器虚拟化路线。KVM 自 2007 年起进入 Linux 主线内核，随后被多种 Linux 发行版和云平台采用。不同云厂商的底层实现持续变化，不宜用“全部转向某一方案”概括；选型还应看来宾兼容性、设备支持、管理平台与运维经验。

##### 软件层面

**容器**

容器将应用与依赖封装在镜像中，并借助 namespaces、cgroups 等内核机制隔离进程及限制资源。镜像不自动保留应用运行时状态；持久数据需要另行配置卷或外部存储。

##### KVM属于哪里

KVM 利用了现代 CPU 中的硬件辅助虚拟化扩展，如 Intel VT-x 和 AMD-V。这些扩展为虚拟化提供了专门的指令集和 CPU 模式，使虚拟机能够直接执行 CPU 指令，而不需要像传统仿真那样对每一条指令进行翻译。

**CPU 虚拟化：**

KVM 将每个 vCPU 暴露为宿主机可调度的执行线程；默认并非一个 vCPU 永久绑定一个物理核心。来宾的大部分普通指令可在硬件辅助下直接运行，敏感操作仍可能发生 VM Exit，并由 KVM/QEMU 或硬件机制处理。CPU 特性是否向来宾暴露，还受虚拟 CPU 模型设置影响。

**内存虚拟化：**

KVM 借助内存虚拟化让来宾管理自己的地址空间，同时由宿主机控制实际物理页。EPT/NPT 等二级地址转换可加速从来宾物理地址到宿主机物理地址的映射；这不意味着来宾能不受限制地直接访问宿主机内存。

**I/O 虚拟化：**

VirtIO 是来宾与宿主协作的虚拟设备接口，常用于磁盘和网络。I/O 可由 QEMU 用户空间、vhost 内核加速或其他后端处理，具体取决于设备配置；设备直通或 SR-IOV 还需要 IOMMU、设备与驱动支持，并会影响迁移能力。

##### KVM实现细节

虽然 KVM 本身不直接模拟硬件，但它与 QEMU 紧密集成。

QEMU 提供设备的仿真，包括 BIOS、硬盘控制器、网络接口等。在 KVM 环境中，QEMU 主要用于仿真那些无法直接由硬件虚拟化的设备，并管理虚拟机的生命周期。通过 QEMU 的设备仿真，虚拟机能够看到一个完整的虚拟硬件环境。

KVM本身不直接模拟CPU，而是通过虚拟化技术使得虚拟机可以直接利用物理CPU的能力。

在KVM中，虚拟机可以使用宿主机的物理CPU资源，且通过硬件虚拟化（如Intel VT-x或AMD-V）提供的支持，使虚拟机能够接近原生性能地执行指令。如果宿主机的CPU不支持硬件虚拟化，KVM将无法直接使用CPU的虚拟化扩展功能，这时虚拟机的性能可能会大打折扣，并且可能需要依赖其他手段进行部分的指令模拟，但这不是KVM本身的核心功能。

**KVM 是硬件辅助的虚拟化技术**

主要负责比较繁琐的 CPU 和内存虚拟化，而 Qemu 则负责 I/O 虚拟化，两者合作各自发挥自身的功能

#### 虚拟机

**简介**

虚拟机（VM）是由虚拟硬件、来宾操作系统、应用和配置共同构成的运行环境。来宾之间有隔离边界，但共享宿主机的处理器、内存、存储及网络，也共享宿主机故障风险；不能把“独立”理解为绝对隔绝。

虚拟机具有以下特征，这些特征可提供多项优势

虚拟机的关键特征包括：

- **分区：** 一台宿主机运行多台来宾，按需分配 CPU、内存和 I/O 资源。
- **隔离：** 来宾之间有虚拟化边界，但共享宿主机仍可能形成共同故障点。
- **封装：** 配置和磁盘可作为文件或卷管理；迁移还需考虑运行状态、网络及共享存储。
- **可迁移性：** 在满足 CPU、设备、存储与软件版本兼容条件时，可在宿主机之间迁移，不是任意两台主机都能无条件互迁。

### 虚拟方式

#### hypervisor

##### 监视器

**简介**

Hypervisor（虚拟机监视器，VMM）负责提供运行来宾的虚拟化边界，并协调底层资源。不同实现可能由独立系统、宿主机内核和用户空间组件共同组成。在线迁移需要源/目标主机、网络、存储与来宾配置共同支持，不是所有 Hypervisor 自带且始终无中断的基本能力。

**特点**

**Hypervisor 允许多种操作系统在相同的物理系统中运行**

Hypervisor 控制硬件并向来宾操作系统提供访问底层硬件的途径 Hypervisor 向来宾操作系统提供虚拟化的硬件

##### 权限保护

![原文插图（第 15 页）]({{ '/subjects/KVM/assets/p015-img01.webp' | relative_url }})

CPU为了保证程序代码执行的安全性、多用户的独立性、保护OS的正常运行，提出了CPU执行状态的概念。

这样能够限制不同程序之间的访问能力，避免一个程序获取另一个程序的内存数据造成数据混乱，同时也避免了程序错误的操作物理硬件。一般CPU都会划分为 用户态 和内核态 ，x86的CPU架构更是细分为了 Ring3~0四种状态。

##### 用户态和内核态

**Ring3 用户态(User Mode)**

运行在用户态的程序代码需要受到CPU的检查，用户态程序代码只能访问内存页表项中规定能被用户态程序代码访问的页面虚拟地址(受限的内存访问)，而且还只能访问任务描述符TSS中的I/O Permission Bitmap中规定能被用户态程序代码访问的端口。甚至不能直接访问外围硬件设备、不能抢占CPU。所有的应用程序都运行在用户态上。当运行在用户态的Application需要调用只能被核心态代码直接访问的硬件设备时，CPU会通过特别的接口去调用核心态的代码，以此来实现Application对硬件设备的调用。如果用户态的Application直接调用硬件设备时，就会被Host OS捕捉到并触发异常，弹出警告窗口。

**Ring0 核心态(Kernel Mode)**

是Host OS Kernel运行的模式，运行在核心态的代码可以无限制的对系统内存、设备驱动程序、网卡接口、显卡接口等外围硬件设备进行访问。只有Host OS能够无限制的访问磁盘、键盘等外围硬件设备的数据，但是首先需要在Host OS上安装驱动程序。

#### 两种风格

##### 表现样式

基于其软件架构和运行方式，主机的两种虚拟化实现方式主要有以下两种

![原文插图（第 16 页）]({{ '/subjects/KVM/assets/p016-img01.webp' | relative_url }})

##### 架构差异

**Type-I（裸机型）**由专门的虚拟化系统直接管理硬件和来宾，VMware ESXi、Hyper-V 的 Hypervisor 层是常见例子。

**Type-II（宿主型）**通常作为通用宿主操作系统上的应用安装，例如 VMware Workstation、VirtualBox 和 Parallels Desktop。不能仅因 Windows 中有 Hyper-V 管理界面，就把 Hyper-V 列为典型 Type-II。

##### 特点和场景

**实现特点**

Type-I/II 便于理解系统层次，但不直接给出性能排名。实际开销还取决于硬件辅助、设备模型、VirtIO、存储和网络路径，以及工作负载。KVM 与 QEMU 的组合更难用简单二分法归类，后文将按组件职责分析。

**应用场景**

裸机型产品常用于集中管理的数据中心，宿主型产品常见于个人学习与开发测试。不过高可用、资源池化和多租户隔离需要管理平台及配套架构，不能只看 Hypervisor 类型。

##### kvm定位

KVM 是 Linux 内核中的虚拟化模块，和用户空间的 QEMU 一起工作。由于 Linux 内核本身直接管理硬件，有资料把 KVM 归为 Type-I；由于它运行在通用宿主操作系统中，也有资料将 QEMU/KVM 整体归为 Type-II。此二分法不足以准确描述其架构：学习时更重要的是区分 KVM 的 CPU/内存虚拟化职责、QEMU 的设备模型，以及 Linux 内核的调度与驱动作用。

## 1.2 kvm简介

### 基础知识

#### 官方介绍

**官方介绍**

![原文插图（第 18 页）]({{ '/subjects/KVM/assets/p018-img01.webp' | relative_url }})

KVM 是 Linux 内核中的虚拟化基础设施，与 QEMU 等用户空间组件配合运行虚拟机。可从 [KVM 项目主页](https://www.linux-kvm.org/page/Main_Page) 查阅概念与资料。

**2025年官网介绍效果**

![原文插图（第 18 页）]({{ '/subjects/KVM/assets/p018-img02.webp' | relative_url }})

KVM（ Kernel-based Virtual Machine）是一个完整的虚拟化解决方案，适用于包含虚拟化扩展（Intel-VT或AMD-V）的x86硬件上的Linux。目前也支持ARM等其它硬件平台. 它由可加载的内核模块kvm.ko组成，它提供核心虚拟化基础架构和处理器特定模块，kvm-intel.ko或kvm-amd.ko，KVM的用户空间组件包含在QEMU1.3后续版本中,KVM目前已成为学术界的主流 VMM (virtual machine monitor，虚拟机监视器，也称为 hypervisor)之一。

#### 其他介绍

KVM是开源软件，可运行多个运行未修改的Linux或Windows映像的虚拟机，依赖于HVM；Intel VT-x, AMD AMD-V

官网： https://www.Linux-kvm.org

- 2006年10月，以色列 Qumranet 公司发布 KVM,早期开发者 Avi Kivity
- 2007年2月，KVM内核组件收录至Linux 2.6.20及后续版本中
- 2008年9月，Redhat 1.7亿美元收购
- 2009年9月, RHEL5.4 中在集成XEN的同时,也将KVM添加进来
- 2011年11月，RHEL6使用KVM代替XEN

**其他资料**

**红帽 kvm 介绍**

https://www.redhat.com/zh/topics/virtualization/what-is-KVM

**RedHat虚拟化指南**

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_Linux/7/html/virtualization_getting_started_guide/index

**RedHat 创建虚拟机数量限制：**

https://access.redhat.com/articles/rhel-kvm-limits

#### kvm到底是哪种方案？

KVM（Kernel-based Virtual Machine）既是全虚拟化解决方案，也是硬件辅助虚拟化解决方案，这两个概念并不冲突，而是从不同维度描述 KVM 的特性。

从功能维度来说，kvm属于全虚拟化解决方案，因为虚拟化层（Hypervisor）能够模拟完整的硬件环境，让 Guest OS 无需修改即可直接运行。

**Guest OS 兼容性：**

KVM 支持运行未修改的 Windows、Linux 等操作系统，无需为虚拟化专门适配内核。

**硬件模拟：**

通过 QEMU（用户空间组件）模拟硬件设备（如网卡、硬盘控制器），Guest OS 认为自己直接操作物理硬件。

**特权指令处理：**

早期全虚拟化通过 “二进制翻译”（Binary Translation）截获特权指令，而 KVM 依赖硬件辅助技术更高效地处理。

从实现维度来说，kvm本身仅提供虚拟化框架，必须利用 CPU（如 Intel VT-x/AMD-V）和芯片组（如 EPT/NPT）提供的虚拟化扩展，降低虚拟化开销。KVM 属于硬件辅助虚拟化，如果CPU不支持，kvm模块无法创建虚拟机。

**CPU 虚拟化：**

在 x86 硬件辅助模式下，来宾运行于 VMX non-root 等来宾上下文；某些敏感操作会触发 VM Exit，由 KVM 处理后再返回来宾。这里的 non-root 是处理器虚拟化术语，不是 Linux 的“非 root 用户”。

**内存虚拟化：**

EPT/NPT 帮助硬件完成来宾物理地址到宿主机物理地址的二级转换；来宾虚拟地址首先仍由来宾页表转换。具体实现可能结合软件管理的映射、缺页处理和 TLB 维护。

**性能优化：**

硬件辅助使 KVM 的虚拟化开销大幅降低，性能接近物理机，远超早期纯软件模拟的全虚拟化方案（如 VMware Workstation 早期版本）。

KVM 是全虚拟化解决方案：从功能上，它支持未修改的 Guest OS 运行。KVM 依赖硬件辅助虚拟化：从实现上，它利用 VT-x/AMD-V 等硬件特性提升性能。

两者的结合使 KVM 兼具兼容性（无需修改 OS）和高性能（接近物理机），成为现代 Linux 服务器虚拟化的主流方案。如果一定要选一个更核心的描述，硬件辅助虚拟化更能体现 KVM 的技术本质，因为离开 VT-x/AMD-V，KVM 将无法工作。

#### 全虚拟化 与 硬件辅助虚拟化冲突么？

**技术比对**

| 维度 | 全虚拟化 | 硬件辅助虚拟化 |
| --- | --- | --- |
| 描述对象 | 虚拟化的功能特性：来宾 OS 是否需要修改 | 虚拟化的实现方式：是否使用 CPU 扩展 |
| 两者关系 | 可借助软件翻译或硬件辅助实现 | 可支撑无需修改来宾 OS 的全虚拟化 |
| 示例 | 未修改的 Windows 来宾运行于虚拟机 | KVM 使用 VT-x / AMD-V 等扩展 |

硬件辅助是全虚拟化的技术优化，而非替代关系。

纯软件全虚拟化：不依赖硬件扩展，通过二进制翻译模拟特权指令（如早期 VMware）。硬件辅助全虚拟化：利用 VT-x/AMD-V 加速特权指令处理（如 KVM、现代 VMware）。

### 原理解析

#### 原理介绍

**运行前提**

KVM 是 Linux 内核提供的虚拟化能力，负责利用处理器扩展运行来宾 vCPU；它不单独提供完整的设备模型。通常由用户空间的 QEMU 创建虚拟机、分配内存并提供磁盘、网络和显示等设备，再通过 `/dev/kvm` 使用硬件加速。因此日常所说的「KVM 虚拟机」通常是 QEMU/KVM 与 libvirt 协作的结果。

![原文插图（第 20 页）]({{ '/subjects/KVM/assets/p020-img01.webp' | relative_url }})

KVM 需要宿主机处理器及固件提供相应虚拟化扩展；它不仅支持 x86_64，也支持部分 ARM 等架构。加载 KVM 模块后，用户空间的 QEMU 通过 `/dev/kvm` 与内核交互，为每台虚拟机创建进程和 vCPU 线程。管理虚拟机应使用 `virsh` 等工具完成正常关机或受控强制停止，直接 `kill` 进程可能导致来宾数据丢失。

#### 特点介绍

**优势**

- 支持 CPU 和 memory 超载（Overcommit）
- 支持 半虚拟化I/O （virtio）
- 支持 热插拔 （cpu，块设备、网络设备等）
- 支持 多存储管理
- 支持 实时迁移（Live Migration）
- 支持 PCI 设备直接分配和 单根I/O 虚拟化 （SR-IOV）
- 支持 内核同页合并 （KSM ）
- 支持 NUMA （Non-Uniform Memory Access，非一致存储访问结构 ）

**关键点**

创建虚拟机前确认 CPU 与固件已启用硬件虚拟化，并结合负载规划 vCPU 超配比例。迁移前核对 CPU 模型、设备、存储与目标主机软件兼容性，不能只比较核心数。

#### kvm实现细节

**各执其职**

- **KVM 内核模块：** 通过 `/dev/kvm` 接口提供创建来宾、运行 vCPU、处理中断和维护虚拟化状态的能力。
- **QEMU 进程：** 在用户空间建立虚拟机实例、配置内存与设备模型，并与 KVM 协同运行；部分 I/O 可交给 vhost 等后端加速。
- **libvirt：** 提供管理 API 和 `virsh`、`virt-manager` 等工具；不同发行版可能使用拆分后的守护进程，而不只一个 `libvirtd`。

**运行模式**

![原文插图（第 22 页）]({{ '/subjects/KVM/assets/p022-img01.webp' | relative_url }})

运行过程中，QEMU 用户空间进程调用 `/dev/kvm`，宿主机内核执行必要的虚拟化操作，vCPU 则在来宾上下文运行。来宾触发 VM Exit 后可能进入 KVM 内核路径，也可能需要返回 QEMU 处理设备请求；它不是固定的“来宾 I/O 都在宿主用户模式，其他操作都在来宾模式”三段划分。

#### 管理软件

KVM 提供单机内核虚拟化能力；跨主机清单、调度和生命周期管理通常由 libvirt 及更上层的平台承担。选择管理平台时要比较维护状态、集群规模、存储/网络集成和团队经验。

![原文插图（第 22 页）]({{ '/subjects/KVM/assets/p022-img02.webp' | relative_url }})

- **virt-manager / virsh：** 借助 libvirt 管理单机或已连接的远端宿主机，适合学习和小规模运维。
- **Proxmox VE：** 在集成平台中管理 KVM 虚拟机和容器，并提供集群、存储与 Web 管理能力。
- **OpenStack：** 面向大规模云资源编排，可与 KVM 后端配合，但部署和维护复杂度较高。
- **oVirt、WebVirtMgr：** 可作为历史或特定环境资料阅读，采用前应先核对项目维护与当前系统兼容性。

#### 环境支持

Rocky Linux 与 Ubuntu 的内核配置文件中都可以找到 `CONFIG_KVM` 以及与处理器架构对应的 `CONFIG_KVM_INTEL` 或 `CONFIG_KVM_AMD`。配置为 `m` 表示模块可按需加载，`y` 表示直接编入内核。文件路径、模块扩展名随发行版和内核版本变化，不必照抄旧实验中几十项配置值。

```bash
grep -E '^CONFIG_KVM(_INTEL|_AMD)?=' /boot/config-$(uname -r)
lsmod | grep '^kvm'
ls -l /dev/kvm
```

第一条命令说明**内核是否提供**对应功能，后两条检查**当前是否已加载并可访问**；真正能否创建加速虚拟机还取决于 CPU、固件设置和访问权限。部署时应结合下文的 `virt-host-validate qemu` 一起判断，而不是仅凭配置文件中的 `CONFIG_KVM=m` 下结论。

## 1.3 部署KVM

### 基础环境

#### 虚拟调整

**前提**

1. 有一台创建好的虚拟机
   - 资源给的多一些
2. 因为我们实验kvm，所以要指定虚拟化引擎，不然的话，无法做虚拟化实验，效果如下勾选虚拟化引擎

![原文插图（第 25 页）]({{ '/subjects/KVM/assets/p025-img01.webp' | relative_url }})

#### 异常处理

但是点击 启动虚拟机【无论Rocky还是Ubuntu】之后，会发生如下提示

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img01.webp' | relative_url }})

若在 Windows 宿主机上的另一层虚拟机内安装 KVM，首先检查是否启用了**嵌套虚拟化**，以及内层来宾能否看到 `vmx` 或 `svm`。Hyper-V 与其他虚拟化产品的兼容性取决于具体版本；关闭 Hyper-V 会影响 WSL2 等功能，不应作为所有“无法启动”的通用修复。

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img02.webp' | relative_url }})

**执行如下命令**

**禁用Hyper-V Hypervisor**

旧实验记录中的 `bcdedit /set hypervisorlaunchtype off` 会改变 Windows 的启动配置。仅在确认冲突并记录原值后才考虑执行；问题排查优先检查产品的嵌套虚拟化设置、固件 VT-x/AMD-V 和虚拟机日志。

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img03.webp' | relative_url }})

重启主机后，重新打开虚拟机即可

#### 验证宿主机是否可运行 KVM

不要用整页 `/proc/cpuinfo` 标志位转储判断结果。按“CPU 与固件 → 内核模块 → 设备访问 → libvirt”逐层检查，能更快定位故障；在 VMware、Hyper-V 等虚拟机内做本实验时，还须先启用**嵌套虚拟化**。

```bash
lscpu | grep -E 'Virtualization|虚拟化'
grep -m1 -Eo 'vmx|svm' /proc/cpuinfo
lsmod | grep '^kvm'
ls -l /dev/kvm
virt-host-validate qemu
```

x86 宿主机出现 `vmx`（Intel）或 `svm`（AMD）说明来宾能看到相应 CPU 扩展；`kvm_intel` 或 `kvm_amd` 模块与 `/dev/kvm` 则说明内核侧设备可用。若标志缺失，先检查物理机固件设置或外层虚拟机的嵌套虚拟化开关。即使模块已加载，当前用户也可能没有访问 `/dev/kvm` 的权限，不能仅凭 `lsmod` 宣称全部就绪。

`virt-host-validate qemu` 汇总可用性检查；有 `WARN` 时根据输出判断影响，不要把每条警告都当成不可运行。Ubuntu 还可安装 `cpu-checker` 使用 `kvm-ok`；它是发行版工具，不是 KVM 核心命令。完成验证后再安装管理组件。

### 环境部署

#### kvm工具包

KVM 环境中的工具可按职责区分，避免把安装包、服务与客户端混为一谈：

| 层次 | 常见组件 | 用途 |
| --- | --- | --- |
| 虚拟机运行 | `qemu-kvm`、内核 KVM 模块 | 创建 QEMU 进程，利用硬件扩展运行来宾 |
| 管理接口 | libvirt 守护进程与 QEMU 驱动 | 维护虚拟机定义，并提供统一管理 API |
| 命令行 | `virt-install`、`virsh`、`qemu-img` | 安装来宾、管理生命周期、处理磁盘镜像 |
| 图形与 Web | `virt-manager`、`virt-viewer`、Cockpit Machines | 配置虚拟机、查看控制台或在浏览器中管理 |

不同发行版的包名与 libvirt 服务拆分方式不完全相同。先按发行版安装相应软件包，再用 `virt-host-validate qemu` 与 `virsh list --all` 验证，而不是以某一个包名是否存在判断部署成功。

#### libvirt

##### 简介

![原文插图（第 30 页）]({{ '/subjects/KVM/assets/p030-img01.webp' | relative_url }})

libvirt 在 QEMU/KVM 等虚拟化后端之上提供统一 API。`virsh`、`virt-manager` 和 Cockpit 可通过它查看与管理虚拟机定义、存储池和虚拟网络；虚拟机运行时仍由 QEMU/KVM 承担计算与设备工作。libvirt 可连接远端宿主机，但跨主机的调度、容量规划和故障切换仍需要额外的平台或运维流程。

##### 结构图

![原文插图（第 30 页）]({{ '/subjects/KVM/assets/p030-img02.webp' | relative_url }})

#### 镜像准备

**准备课程需要的几个镜像**

可按实验目的准备 Linux 或 Windows 安装镜像。Linux 镜像从相应发行版官方镜像页选择仍受支持的版本；Windows Server 评估镜像从 [Microsoft 评估中心](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2025) 获取。原实验使用 CentOS 7 和 Windows Server 2016 等旧版本，学习命令可作参考，但新环境应核对系统支持周期、许可和镜像校验值。

参考资料：https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2025

### 在 Ubuntu 上安装

先完成上一节的 CPU、固件和内核检查，再安装运行与管理组件。`virt-manager` 需要图形桌面；纯服务器环境只需命令行工具和可选的 Cockpit。

````console
root@ubuntu-host:~# apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager virt-viewer cpu-checker
````

安装后用 `kvm-ok` 检查加速能力，再用 `virsh net-list --all` 确认 libvirt 网络。`kvm-ok` 是 Ubuntu 的 `cpu-checker` 工具；若提示缺少 KVM 扩展，应回到固件或外层虚拟机检查，而不是反复重装软件包。默认网络未启用时，可通过 `virsh net-start default` 启动，并按需要设置自启动。

```bash
kvm-ok
virsh net-list --all
virsh list --all
```

#### 使用 Cockpit 管理 Ubuntu 宿主机

Cockpit 是可选的 Web 管理界面；安装 Machines 插件后才能在其中管理虚拟机。

````console
root@ubuntu-host:~# apt -y install cockpit cockpit-machines
````

保持 Cockpit 默认的 root 登录限制，使用具备适当管理权限的个人账户。启动 socket 后，确认其监听 9090 端口；远程访问前还要核对主机防火墙、访问范围和 TLS 证书。

```bash
systemctl enable --now cockpit.socket
systemctl is-active cockpit.socket
ss -ltn '( sport = :9090 )'
```

浏览器访问 `https://<宿主机地址>:9090`。下面的截图记录了旧实验界面，按钮文字可能因版本不同而变化。

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img01.webp' | relative_url }})

若浏览器提示证书未受信任，先核对访问地址和证书指纹；自签名证书是实验环境常见原因，不代表可以忽略异常。

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img02.webp' | relative_url }})

确认访问的确为目标宿主机后，才能决定是否继续；长期使用时应配置可信证书。

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img03.webp' | relative_url }})

登录后进入「虚拟机」页面，先检查 libvirt 连接和默认网络，再创建来宾。

![原文插图（第 34 页）]({{ '/subjects/KVM/assets/p034-img01.webp' | relative_url }})

#### 图形管理器

`virt-manager` 适合在有图形会话的工作站运行；无桌面的服务器可通过远程 libvirt 连接管理，不必为了打开界面而安装完整桌面。

````console
root@ubuntu-host:~# virt-manager
````

成功连接后可在图形界面查看虚拟机与宿主机资源。

![原文插图（第 34 页）]({{ '/subjects/KVM/assets/p034-img02.webp' | relative_url }})

### 在 Rocky Linux 上安装

Rocky Linux 可通过虚拟化软件包组安装常用组件，也可按需单独安装。先确认启用的软件仓库与发行版版本相符；EPEL 不是运行 KVM 本身的必要条件。

可二选一安装；如果宿主机没有图形桌面，第二种方式可省去 `virt-manager` 与 `virt-viewer`。

```bash
dnf group install "Virtualization Host"
# 或按需安装：
dnf install qemu-kvm libvirt virt-install virt-manager virt-viewer
```

启动 libvirt。某些新版发行版采用拆分后的模块化守护进程，若 `libvirtd` 不存在，应依据所安装的 libvirt 包与发行版文档启用相应 socket。

````console
[root@kvm-host ~]# systemctl enable --now libvirtd
````

用 `virsh list --all` 验证管理连接，再用 `virsh net-list --all` 检查网络。默认 NAT 网络通常对应 `virbr0`，但它是否存在、是否开机自启动取决于实际配置；libvirt 常通过 `dnsmasq` 为该网络提供 DHCP/DNS。不要把 Ubuntu 的路由示例当成 Rocky 的固定结果。

```bash
virsh list --all
virsh net-list --all
ip address show virbr0
```

#### 使用 Cockpit 管理 Rocky 宿主机

Cockpit 与 Ubuntu 部分的用途相同：提供可选 Web 界面，Machines 插件用于管理虚拟机。

````console
[root@kvm-host ~]# yum install cockpit cockpit-machines
````

保持默认的 root 登录限制，使用具备管理权限的个人账户。Rocky 通常由 `cockpit.socket` 按需拉起服务；查看 `cockpit.service` 是否长期处于 `running` 并不是唯一验证方式。

```bash
systemctl enable --now cockpit.socket
systemctl is-active cockpit.socket
ss -ltn '( sport = :9090 )'
```

浏览器访问 `https://<宿主机地址>:9090`，并核对证书和访问范围。下列截图是旧实验的界面路径。

![原文插图（第 36 页）]({{ '/subjects/KVM/assets/p036-img01.webp' | relative_url }})

出现证书提示时，先核对地址与证书来源。

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img01.webp' | relative_url }})

确认目标无误后再继续；长期使用应配置可信证书。

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img02.webp' | relative_url }})

使用有管理权限的个人账户登录，而不是在教程中复用固定密码。

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img03.webp' | relative_url }})

#### 创建虚拟机

先将从官方渠道获取并校验过的 ISO 放到宿主机可读取的目录。以下旧实验以 CentOS 7 镜像为例，它已结束常规维护；在新环境应选受支持的系统。

````console
[root@kvm-host ~]# mkdir -p /data/images
[root@kvm-host ~]# ls /data/images/
CentOS-7-x86_64-Minimal-2009.iso
````

在 Cockpit 左栏进入「虚拟机」，选择创建虚拟机。不同版本的按钮名称可能略有差异，核心是选择安装介质、设定资源并确认存储位置。

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img01.webp' | relative_url }})

向导中选择本地 ISO，核对来宾系统类型、名称、vCPU、内存和磁盘容量。文件选择器可能需要逐级进入 `/data/images`；若无法看到文件，还应检查 libvirt 进程的目录权限，而不只是重试浏览器。

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img02.webp' | relative_url }})

确认配置后创建并运行，再打开新建来宾的控制台完成安装。创建动作与来宾操作系统安装是两个阶段，看到虚拟机列表中的名称不代表系统已安装完成。

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img03.webp' | relative_url }})

进入虚拟机详情检查运行状态、控制台与磁盘信息。

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img01.webp' | relative_url }})

#### 移除虚拟机

从虚拟机列表找到目标来宾并先正常关机；随后在操作菜单中选择删除。

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img02.webp' | relative_url }})

操作菜单的位置可能随 Cockpit 版本变化，应以虚拟机名称和磁盘路径确认对象。

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img03.webp' | relative_url }})

**点击删除前先区分“移除虚拟机定义”和“删除关联磁盘”。** 若勾选磁盘，数据将随之删除；应先核对虚拟机名称、卷路径和备份，再按实际需要选择。

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img01.webp' | relative_url }})

最后确认删除范围；仅删除定义会保留磁盘文件，勾选磁盘会删除来宾数据。

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img02.webp' | relative_url }})

#### virt-manager工具

有图形会话时，在其中启动 `virt-manager`：

````console
[root@kvm-host ~]# virt-manager
````

启动后应能看到本地或已配置的远端 libvirt 连接。

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img03.webp' | relative_url }})

若提示 `cannot open display`，原因通常是当前会话没有可用的图形显示，而不是虚拟机服务损坏：

````console
[root@kvm-host ~]# virt-manager
[root@kvm-host ~]#
(virt-manager:37183): Gtk-WARNING **: 11:36:38.431: cannot open display:
````

无桌面服务器可从本地桌面客户端通过 libvirt 远程连接，或改用 Cockpit/`virsh`；不必仅为运行管理器安装整个桌面环境并重启服务器。

#### 网络信息

启用 libvirt 默认 NAT 网络后，宿主机通常出现 `virbr0` 网桥。它连接到来宾的虚拟网卡，并通过 NAT 让来宾访问外部网络；这与直接桥接到物理局域网不同。网桥地址及 DHCP 范围以实际网络定义为准。

```console
[root@kvm-host ~]# ip -brief address show virbr0
virbr0 UP 198.18.122.1/24
```

下面的网络定义示例说明 `forward mode='nat'`、`bridge` 和 DHCP 地址池的关系。文件由 libvirt 管理；如需调整，用 `virsh net-edit default`，不要直接覆盖自动生成的 XML。

````console
[root@kvm-host ~]# cat /etc/libvirt/qemu/networks/default.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh net-edit default
or other application using the libvirt API.
-->
<network>
  <name>default</name>
  <uuid>00000000-0000-4000-8000-000000000007</uuid>
  <forward mode='nat'/>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='02:00:00:00:00:04'/>
  <ip address='198.18.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='198.18.122.2' end='198.18.122.254'/>
    </dhcp>
  </ip>
</network>
````

### 用 virt-manager 创建虚拟机

#### 打开创建向导

图形桌面安装了 `virt-manager` 后，可从本地会话启动它；若管理的是远端宿主机，应先在管理器中配置 libvirt 连接。远端 Windows 电脑不必通过 X Server 转发整个 Linux 图形程序，使用本机客户端连接通常更直接。

````console
[root@kvm-host ~]# virt-manager
````

确认管理器连接到目标宿主机，再点击新建虚拟机；后续界面因版本不同可能略有变化。

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img01.webp' | relative_url }})

选择「本地安装介质」，而非导入已有系统盘；两种方式后续的启动行为不同。

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img02.webp' | relative_url }})

#### 选择安装介质

点击浏览并选择宿主机上可被 libvirt 读取的 ISO。若文件未出现在列表中，检查所选存储池和目录权限。

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img03.webp' | relative_url }})

示例 ISO 位于 `/data/images`；也可以把镜像导入管理器可访问的存储池，路径不必固定。

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img01.webp' | relative_url }})

#### 分配资源

确认 ISO 后进入资源页面。示例配置 2 vCPU、2 GiB 内存与 20 GiB 磁盘，仅供低负载实验；实际配置应参照来宾系统要求与宿主机剩余容量。

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img02.webp' | relative_url }})

在最后一步核对名称、网络与磁盘位置，避免默认存储池空间不足或来宾误接入其他网络。

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img03.webp' | relative_url }})

#### 安装并核验

需要调整磁盘总线、网卡型号或启动顺序时，可勾选「安装前自定义配置」，检查后再启动安装程序。

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img01.webp' | relative_url }})

在来宾控制台完成分区、账户和网络配置。ISO 安装完毕后，来宾应从系统盘启动，而不是再次进入安装器。

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img02.webp' | relative_url }})

安装程序提示重启时，先确认安装步骤已结束。

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img03.webp' | relative_url }})

重启后在控制台登录，并检查来宾 IP 与磁盘挂载情况。

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img01.webp' | relative_url }})

#### 查看运行状态

管理器可显示来宾状态与资源曲线；曲线反映宿主机侧观测，不等同于来宾内部全部性能指标。

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img02.webp' | relative_url }})

如果 CPU 曲线未显示，可在「查看」菜单启用相关统计；同时可用 `virsh dominfo <虚拟机名>` 独立核对状态。

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img03.webp' | relative_url }})

#### 确认效果

最后检查生成的磁盘镜像。`ls -lh` 显示逻辑容量，`du -h` 显示实际占用；qcow2 支持稀疏分配，二者不必相等。

````console
[root@kvm-host ~]# du -sh /var/lib/libvirt/images/
1.7G /var/lib/libvirt/images/
[root@kvm-host ~]# ll /var/lib/libvirt/images -h
总用量 1.7G
-rw------- 1 qemu qemu 21G 3月 24 22:44 centos7.0.qcow2
````

**核对虚拟机磁盘与定义**

图形向导创建完成后，不要只凭界面显示「运行中」就认为配置正确。先查询来宾状态、磁盘路径和磁盘占用，再检查 XML 中的关键资源：

```bash
virsh list --all
virsh domblklist centos7.0
virsh dumpxml centos7.0 | grep -E '<name>|<memory |<vcpu |<source file=|<source network='
ls -lh /var/lib/libvirt/images/centos7.0.qcow2
du -h /var/lib/libvirt/images/centos7.0.qcow2
```

示例中 `ls -lh` 显示镜像的标称容量约 21 GiB，`du -h` 显示当时实际占用约 1.7 GiB，这是 qcow2 稀疏分配的正常差异；随着写入，实际占用可能增加，存储池必须保留余量。`domblklist` 可确认磁盘确实挂载到目标来宾，`dumpxml` 则可核对 vCPU、内存、系统盘与网络来源。需要修改虚拟机定义时使用 `virsh edit centos7.0`，不要直接修改 libvirt 自动生成的 `/etc/libvirt/qemu/centos7.0.xml`。
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/02-create-vm-from-cli.html' | relative_url }}">下一章：命令创建虚拟机 →</a>
</nav>
