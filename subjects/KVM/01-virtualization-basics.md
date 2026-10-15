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

![原文插图（第 8 页）]({{ '/subjects/KVM/assets/p008-img01.png' | relative_url }})

#### 传统基础设施

![原文插图（第 8 页）]({{ '/subjects/KVM/assets/p008-img02.png' | relative_url }})

**常见工作内容**

- IDC选择,如:联通,电信,世纪互联,鹏博士等
- 网络和存储规划
- 服务器选型及采购
- 服务器系统选择、系统安装、上架、配置网络
- 应用规划及部署
- 域名选择及注册,DNS配置名称解析
- 测试外网访问

**面对问题**

1. 服务器和网络设备资源利用率过低，并且无法共享,导致资源浪费据统计大部分数据中心中的服务器和网络设备的利用率仅在24%～30%之间，有的CPU利用率、硬盘利用率都在10%以下
2. 资源分配后进行调整困难资源分配不合理也是传统网络架构存在的问题，因为资源不能动态调配，分配出去的资源是固定的，不能随意添加或删除。
3. 难以实现自动化初始化成本高,服务器迁移和升级很繁琐，无法实现自动化

4. 成本高昂集群环境需要大量的服务器主机,硬件投入和后期维护管理成本巨大

#### 虚拟化技术

##### 技术理解

**虚拟化技术是什么**

虚拟化（Virtualization）是一种资源分配和管理技术，是将计算机的各种实体资源,比如CPU、内存、磁盘空间、网络适配器等，进行抽象转换后虚拟的设备,可以实现灵活地分割、组合为一个或多个计算机配置环境，并还支持重新分割、重新组合，以达到最大化合理利用物理资源的目的。

**参考资料:** https://www.vmware.com/cn/solutions/virtualization.html

**注意：** 该页面可能因为过期失效

##### 我的理解

**虚拟化是什么**

**虚拟化技术：**

在现有物理主机基础上创造多个彼此独立的具有完整功能主机的技术。将底层的计算机资源，抽象为彼此互相隔离的多组计算平台，每个计算平台都包含计算机的五大部件：cpu(控制器+寄存器)、mem(存储)、IO(输入+输出)，

**我的理解**

**简单来说就是：**

本来没有，但是通过某种特殊的手段，让你以为有，而且确信不已。这些手段就是虚拟化技术。

##### 虚拟化优势

**简介**

虚拟化可以提高 IT 敏捷性、灵活性和可扩展性，同时大幅节约成本。更高的工作负载移动性、更高的性能和资源可用性、自动化运维 - 这些都是虚拟化的优势，虚拟化技术可以使 IT 部门更轻松地进行管理以及降低拥有成本和运维成本。

**其优势包括：**

- 资源超分,如实际的物理内存只有128G,可以给虚拟机分配200G内存
- 降低资金成本和运维成本
- 最大限度减少或消除停机
- 提高 IT 部门的工作效率和响应能力
- 加快应用和资源的调配速度
- 提高业务连续性和灾难恢复能力
- 简化数据中心管理
- 减少资源,比如IP和端口的冲突
- 支持较旧的硬件和操作系统及应用

##### 虚拟化目标

**虚拟化目标**

在时间上和空间上突破我们工作的限制，提升工作效率。

**时间上：** 多种工作在一时间段内同时进行

**空间上：** 在一台物理主机上，虚拟出来多台主机，多台主机共同做一件事情。

![原文插图（第 10 页）]({{ '/subjects/KVM/assets/p010-img01.png' | relative_url }})

##### 虚拟化技术发展

![原文插图（第 11 页）]({{ '/subjects/KVM/assets/p011-img01.png' | relative_url }})

**虚拟化发展**

**起始：**

60年代ibm公司，成本巨大的大型机，企业负担不起业务多环境，虚拟化技术实现多环境。

**没落：**

80年代pc机，pc机很便宜，可以解决虚拟化多环境的问题。

**风云再起：**

随着x86主机硬件性能的增强，各企业业务对资源的需求量增加，自03年以来，虚拟化技术风云归来，现在越来越火

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

- 应用虚拟化
- 将软件应用通过网络实现虚拟化，比如 office 365,钉钉,企业微信
- 存储虚拟化
- 将存储用软件虚拟化实现, 如 SAN/NAS(NFS/Samba)/GlusterFS/ceph等
- 库虚拟化
- 在Linux上使用 wine来运行Windows 程序，在Mac系统使用CrossOver来运行Windows程序
- 容器虚技术
- 当前比较火的虚拟化技术，典型代表: Docker、Containerd、Podman、Linux Container(LXC)、
- Pouch

#### 应用技术分类

##### 系统层面

**模拟**

使用模拟器技术，模拟出来一套完整的主机功能，虚拟出来的主机平台可以跟宿主机平台不一样。可以模拟X86、ARM 、PowerPC等多种CPU,效率比较低.产品或方案:QEMU、Bochs、PearPC

**全虚拟化**

使用软件方式，虚拟出一个功能完整，底层平台与宿主机一致的主机，虚拟机自以为是一个真实的主机,不需要对GuestOS操作系统软件的源代码做任何的修改，就可以运行在这样的VMM中。常见的软件辅助技术：Vmware Workstation,QEMU,Virtual PC 最早出现在1966年

**半虚拟化**

半虚拟化是需要GuestOS协助的虚拟化。因为在半虚拟化VMM中运行的GuestOS，都需要将其内核源码进行都进过了特别的修改。也就是说，结合软件方式，虚拟出一个部分功能，底层平台与宿主机一致的主机，虚拟机知道自己是一个傀儡。常见的技术：xen(2003年发布)半虚拟化要求guest OS 的内核是知道自己运行在虚拟化环境当中的，因此guest OS的系统架构必须和宿主机的系统架构相同，并且要求对guest OS的内核做相应的修改，因此半虚拟化只支持开源内核的系统，不支持闭源的系统，比较常见的半虚拟化就是早期版本的XEN，但是Xen 从其3.0 版本开始，可以支持利用硬件辅助虚拟化技术

**硬件辅助虚拟化**

借助主机硬件的功能，虚拟出一个完全功能的主机。他是全虚拟化技术的一个特殊表现形式常见技术：VT-x/EPT或者AMD-v/RVI，kvm(2006年发布)、vmware esxi、Xen3.0、VirtualBox 最早出现在1972年

**代表软件**

开源的虚拟化技术非常多，著名的就是Xen和KVM。Xen是2003年发布，当时全球虚拟化/公有云，基本都是Xen的天下。2006年，为了对抗Xen，intel，红帽，IBM，联手搞出一个KVM。并与2008年发布，自从2010年kvm添加到RHEL6.0内核中，kvm终于成为了主流。经过了5年的PK，特别是硬件辅助虚拟化技术的应用，xen的性能优势被一点点的超越，目前现在已经是 KVM独大。AWS，阿里云，已经全面转向KVM。

##### 软件层面

**容器**

通过技术手段，将软件应用的运行状态保留下拉，

##### KVM属于哪里

KVM 利用了现代 CPU 中的硬件辅助虚拟化扩展，如 Intel VT-x 和 AMD-V。这些扩展为虚拟化提供了专门的指令集和 CPU 模式，使虚拟机能够直接执行 CPU 指令，而不需要像传统仿真那样对每一条指令进行翻译。

**CPU 虚拟化：**

KVM 将虚拟机的 CPU 作为一个虚拟的 CPU 核心，并映射到物理 CPU 核心上。在硬件虚拟化支持下，虚拟机可以直接运行 CPU 指令，而不需要软件进行额外的仿真。硬件支持的虚拟化扩展能够确保虚拟机与物理机的指令集执行环境保持一致。

**内存虚拟化：**

KVM 使用了内存管理单元（MMU）的虚拟化功能。硬件辅助虚拟化技术提供了二级地址转换（SLAT，或称为 EPT 在 Intel CPU 中，RVI 在 AMD CPU 中），使得虚拟机能够直接访问分配给它的物理内存，并通过硬件进行地址转换，而不需要经过软件仿真。

**I/O 虚拟化：**

KVM 通过 Virtio 驱动程序和设备模型（如 Virtio 磁盘、Virtio 网络）来处理虚拟机的I/O 操作。这些操作由虚拟机发出，然后通过宿主机的 QEMU 组件进行处理，将虚拟 I/O 请求转发给物理设备。对于部分硬件（如网络适配器），现代 CPU 支持直接的 I/O 虚拟化（如 Intel VT-d），这进一步提高了 I/O 性能。

##### KVM实现细节

虽然 KVM 本身不直接模拟硬件，但它与 QEMU 紧密集成。

QEMU 提供设备的仿真，包括 BIOS、硬盘控制器、网络接口等。在 KVM 环境中，QEMU 主要用于仿真那些无法直接由硬件虚拟化的设备，并管理虚拟机的生命周期。通过 QEMU 的设备仿真，虚拟机能够看到一个完整的虚拟硬件环境。

KVM本身不直接模拟CPU，而是通过虚拟化技术使得虚拟机可以直接利用物理CPU的能力。

在KVM中，虚拟机可以使用宿主机的物理CPU资源，且通过硬件虚拟化（如Intel VT-x或AMD-V）提供的支持，使虚拟机能够接近原生性能地执行指令。如果宿主机的CPU不支持硬件虚拟化，KVM将无法直接使用CPU的虚拟化扩展功能，这时虚拟机的性能可能会大打折扣，并且可能需要依赖其他手段进行部分的指令模拟，但这不是KVM本身的核心功能。

**KVM 是硬件辅助的虚拟化技术**

主要负责比较繁琐的 CPU 和内存虚拟化，而 Qemu 则负责 I/O 虚拟化，两者合作各自发挥自身的功能

#### 虚拟机

**简介**

虚拟计算机称为“虚拟机”(VM,Virtual Machine)，它是一种严密隔离且内含操作系统和应用的软件容器。每个虚拟机都是完全独立的。通过将多台虚拟机放置在一台物理计算机上，可仅在一台物理服务器或“主机”上运行多个操作系统和应用，名为“hypervisor”的精简软件层可将虚拟机与主机分离开来，并根据需要为每个虚拟机动态分配计算资源。

虚拟机具有以下特征，这些特征可提供多项优势

分区可在一台物理机上运行多个操作系统可在虚拟机之间分配系统资源。隔离可在硬件级别进行故障和安全隔离。可利用高级资源控制功能保持性能封装可将虚拟机的完整状态保存到文件中。移动和复制虚拟机就像移动和复制文件一样轻松独立于硬件可将任意虚拟机调配或迁移到任意物理服务器上安装系统不会受硬件兼容性的影响

### 虚拟方式

#### hypervisor

##### 监视器

**简介**

Hypervisor是一种运行在基础物理服务器和操作系统之间的中间软件层，其可以允许多个VM操作系统和 VM应用共享宿主机底层的内存、CPU、磁盘等物理硬件，也可叫做VMM（ virtual machine monitor），即虚拟机监视器。Hypervisor是所有虚拟化技术的核心，非中断地支持多工作负载迁移的能力是Hypervisor的基本功能，当服务器启动并执行Hypervisor时，它会给每一台虚拟机分配适量的内存、CPU、网络和磁盘，并加载所有虚拟机的客户操作系统。

**特点**

**Hypervisor 允许多种操作系统在相同的物理系统中运行**

Hypervisor 控制硬件并向来宾操作系统提供访问底层硬件的途径 Hypervisor 向来宾操作系统提供虚拟化的硬件

##### 权限保护

![原文插图（第 15 页）]({{ '/subjects/KVM/assets/p015-img01.png' | relative_url }})

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

![原文插图（第 16 页）]({{ '/subjects/KVM/assets/p016-img01.png' | relative_url }})

##### 架构差异

Type - I：也称为裸机 Hypervisor。

Type - I 的 Hypervisor 直接运行在硬件之上，没有宿主机操作系统，直接控制硬件资源和客户机。它就像是一个专门为虚拟化而设计的操作系统，将硬件资源进行抽象和管理，然后为虚拟机分配资源。例如，VMware ESXi 就是典型的 Type - I Hypervisor，常用于企业级数据中心，能高效地管理硬件资源，支持多虚拟机同时运行和隔离等功能。常见方案：vmware esxi 、rhev hypervisor、Hyper-v Server

Type - II：也叫宿主型 Hypervisor。

Type - II 的 Hypervisor 运行在一个宿主机操作系统之上，作为宿主机操作系统中的一个应用程序，客户机则是在宿主机操作系统上的一个进程。例如，VMware Workstation 和 VirtualBox 等都是 Type - II Hypervisor，通常用于个人电脑或测试环境，用户可以在自己熟悉的操作系统（如 Windows 或 Linux）上安装这些虚拟化软件，方便地创建和管理虚拟机。常见方案：vmware workstation、Microsoft Hyper-V、VirtualBox Oracle、paralles desktop

##### 特点和场景

**实现特点**

Type - I：由于直接运行在硬件上，没有中间的宿主操作系统层，Type - I Hypervisor 具有较低的系统开销和更高的性能效率，能更充分地利用硬件资源，适合对性能要求较高的生产环境。Type - II：运行在宿主操作系统之上，虚拟机访问硬件资源需要经过宿主操作系统的内核，会带来一定的性能损耗。不过，在一些对性能要求不特别苛刻的场景，如开发测试环境或个人使用场景中，这种性能损耗通常是可以接受的。

**应用场景**

Type - I：适用于企业级的数据中心、云计算平台等需要大规模部署和管理虚拟机的场景，能提供高效、稳定的虚拟化环境，支持多租户、资源池化等功能，满足企业对服务器整合、高可用性和资源灵活调配的需求。Type - II：更适合个人用户、开发人员和测试人员在本地计算机上创建和运行虚拟机，用于学习、开发、测试软件或运行不同的操作系统环境等，具有成本低、易于安装和使用的优点。

##### kvm定位

KVM（Kernel-Based Virtual Machine）属于Type-II虚拟化实现方式。

在Type-II虚拟化中，虚拟机管理程序（如KVM）安装在现有的操作系统之上，这个操作系统被称为宿主操作系统（Host OS）。KVM作为一个Linux内核模块，它依赖于Linux操作系统来管理硬件资源，并为虚拟机提供虚拟化的硬件环境。由于KVM运行在宿主操作系统之上，因此它属于Type-II虚拟化。尽管KVM是Type-II虚拟化实现方式，但它仍然具有高性能和广泛的功能特性。KVM利用Linux内核的调度程序和其他功能来优化虚拟机的性能，并提供了丰富的管理工具和功能，使其成为当前主流的开源服务器虚拟化技术之一。需要注意的是，虽然KVM本身属于Type-II虚拟化，但在某些情况下，通过特定的配置和优化，KVM可以实现接近Type-I虚拟化的性能水平。此外，随着虚拟化技术的不断发展，Type-I和Type-II的界限也在逐渐模糊，一些新的虚拟化解决方案可能结合了两种类型的优点，提供了更加灵活和高效的虚拟化环境。

## 1.2 kvm简介

### 基础知识

#### 官方介绍

**官方介绍**

![原文插图（第 18 页）]({{ '/subjects/KVM/assets/p018-img01.png' | relative_url }})

**关键点：**

全虚拟化的解决方案开源的，被内嵌到linux内核了

**官方地址：**

https://www.linux-kvm.org/page/Main_Page

**2025年官网介绍效果**

![原文插图（第 18 页）]({{ '/subjects/KVM/assets/p018-img02.png' | relative_url }})

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

利用 VT-x/AMD-V 的VMX/AMD-V 模式，Guest OS 运行在非根模式（Rootless Mode），特权指令自动触发虚拟化陷阱（VM Exit），由 KVM 处理后返回结果（VM Entry）。

**内存虚拟化：**

通过EPT/NPT（二级地址转换），直接由硬件管理 Guest OS 的虚拟地址→物理地址映射，无需软件维护影子页表。

**性能优化：**

硬件辅助使 KVM 的虚拟化开销大幅降低，性能接近物理机，远超早期纯软件模拟的全虚拟化方案（如 VMware Workstation 早期版本）。

KVM 是全虚拟化解决方案：从功能上，它支持未修改的 Guest OS 运行。KVM 依赖硬件辅助虚拟化：从实现上，它利用 VT-x/AMD-V 等硬件特性提升性能。

两者的结合使 KVM 兼具兼容性（无需修改 OS）和高性能（接近物理机），成为现代 Linux 服务器虚拟化的主流方案。如果一定要选一个更核心的描述，硬件辅助虚拟化更能体现 KVM 的技术本质，因为离开 VT-x/AMD-V，KVM 将无法工作。

#### 全虚拟化 与 硬件辅助虚拟化冲突么？

**技术比对**

| 维度 | 全虚拟化 | 硬件辅助虚拟化 |
| --- | --- | --- |
| 描述对<br>象 | 虚拟化的功能特性（是否需修改 OS） | 虚拟化的实现方式（是否依赖硬件） |
| 技术演<br>进 | 早期依赖软件模拟（性能差） | 现代虚拟化的必备技术（性能高） |
| 典型产<br>品 | VMware ESXi（早期版本）、<br>VirtualBox | KVM、VMware ESXi（现代版本）、<br>Hyper-V |

硬件辅助是全虚拟化的技术优化，而非替代关系。

纯软件全虚拟化：不依赖硬件扩展，通过二进制翻译模拟特权指令（如早期 VMware）。硬件辅助全虚拟化：利用 VT-x/AMD-V 加速特权指令处理（如 KVM、现代 VMware）。

### 原理解析

#### 原理介绍

**前提**

KVM 本身不执行任何硬件模拟，需要使用一个客户空间的程序通过 /dev/kvm 接口设置一个客户机虚拟服务器的地址空间，向它提供模拟的 I/O，并将它的视频显示映射回宿主的显示屏。目前这个应用程序通常使用 QEMU。

![原文插图（第 20 页）]({{ '/subjects/KVM/assets/p020-img01.png' | relative_url }})

kvm依赖于HVM技术，只能运行在支持硬件虚拟化的CPU上，也就是说CPU支持VT-x或AMD-v，并且只支持x86_64bits系统。只要基于硬件的操作系统内核一旦装载了kvm模块，那么kvm模块就和linux内核组合成了hypervisor，变成了type-I模型的虚拟机。kvm类似于寄生虫，linux内核一旦被寄宿，就没有自主权，跟着kvm一起变成hypervisor的一部分。原来的用户空间就变成了hypervisor的管理控制台运行位置，而kvm以字符设备/dev/kvm的形式作为kvm整个的调用管理接口。kvm创建的虚拟机就是一个进程，ps查看，kill杀死

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

Cpu 支持硬件虚拟化 CPU 不建议超过当前核心数迁移时候，基础环境要一致

#### kvm实现细节

**各执其职**

- KVM：
- 初始化CPU硬件,打开虚拟机模式,负责CPU,内存,中断控制器,时钟. 由内核模块kvm_xxx.ko实现，工
- 作于hypervisor，设备/dev/kvm，是一个字符设备，在用户空间可通过ioctl()系统调用来完成VM创建、
- 启动，为VM分配内存、读写VCPU的寄存器、向VCPU注入中断、时钟等管理功能
- QEMU进程：
- 工作于用户空间，主要用于实现模拟IO设备,如显卡，网卡，硬盘等， qemu-kvm进程：工作于用户空
- 间，用于实现一个虚拟机实例
- Libvirt：
- 提供统一API，守护进程libvirtd和相关工具，如:virsh，virt-manager等

**运行模式**

![原文插图（第 22 页）]({{ '/subjects/KVM/assets/p022-img01.png' | relative_url }})

内核模式：HostOS执行I/O类操作，或其它的特殊指令的操作；称作内核模式用户模式：GuestOS的I/O类操作来宾模式：GuestOS非I/O类操作，称作虚拟机的用户模式更贴切

#### 管理软件

KVM是运行在单机的系统，需要其它软件实现跨主机的统一的管理。常见的虚拟化管理平台如下：

参考资料：http://www.linux-kvm.org/page/Management_Tools

![原文插图（第 22 页）]({{ '/subjects/KVM/assets/p022-img02.png' | relative_url }})

- oVirt
- 功能强大，是Redhat虚拟化管理平台RHEV的开源版本
- http://www.ovirt.org/
- WebVirtMgr
- https://www.webvirtmgr.net
- virt-manager的Web模式的替代品,管理单主机的虚拟机
- OpenStack
- 最主流的开源虚拟化管理平台,基于Python语言开发实现，适合大型企业
- https://www.openstack.org/

Proxmox virtualization environment 简称PVE，是一个开源免费的基于Linux的企业级虚拟化方案，功能不输专业收费的VMware。是一个完整的企业虚拟化开源平台。借助内置的Web界面，您可以轻松管理VM和容器，软件定义的存储和网络，高可用性集群以及单个解决方案上的多个开箱即用工具。VMware vSphere VMware 公司商业化，只用于管理ESXi 的虚拟机，不能管理KVM虚拟机

#### 环境支持

**目前的内核是支持 kvm功能的**

**Rocky系统**

````console
[root@kvm-host ~]# grep -i kvm /boot/config-5.14.0-427.13.1.el9_4.x86_64
CONFIG_KVM_GUEST=y
CONFIG_HAVE_KVM=y
CONFIG_HAVE_KVM_PFNCACHE=y
CONFIG_HAVE_KVM_IRQCHIP=y
CONFIG_HAVE_KVM_IRQFD=y
CONFIG_HAVE_KVM_IRQ_ROUTING=y
CONFIG_HAVE_KVM_DIRTY_RING=y
CONFIG_HAVE_KVM_DIRTY_RING_TSO=y
CONFIG_HAVE_KVM_DIRTY_RING_ACQ_REL=y
CONFIG_HAVE_KVM_EVENTFD=y
CONFIG_KVM_MMIO=y
CONFIG_KVM_ASYNC_PF=y
CONFIG_HAVE_KVM_MSI=y
CONFIG_HAVE_KVM_CPU_RELAX_INTERCEPT=y
CONFIG_KVM_VFIO=y
CONFIG_KVM_GENERIC_DIRTYLOG_READ_PROTECT=y
CONFIG_KVM_COMPAT=y
CONFIG_HAVE_KVM_IRQ_BYPASS=y
CONFIG_HAVE_KVM_NO_POLL=y
CONFIG_KVM_XFER_TO_GUEST_WORK=y
CONFIG_HAVE_KVM_PM_NOTIFIER=y
CONFIG_KVM_GENERIC_HARDWARE_ENABLING=y
CONFIG_KVM_GENERIC_MMU_NOTIFIER=y
CONFIG_KVM_GENERIC_MEMORY_ATTRIBUTES=y
CONFIG_KVM_PRIVATE_MEM=y
CONFIG_KVM_GENERIC_PRIVATE_MEM=y
CONFIG_KVM=m
CONFIG_KVM_SW_PROTECTED_VM=y
CONFIG_KVM_INTEL=m
CONFIG_X86_SGX_KVM=y
CONFIG_KVM_AMD=m
CONFIG_KVM_AMD_SEV=y
CONFIG_KVM_SMM=y
# CONFIG_KVM_XEN is not set
CONFIG_KVM_MAX_NR_VCPUS=4096
CONFIG_PTP_1588_CLOCK_KVM=m
# CONFIG_DRM_I915_GVT_KVMGT is not set
````

````console
[root@kvm-host ~]# tree /lib/modules/5.14.0-
427.13.1.el9_4.x86_64/kernel/arch/x86/kvm/
/lib/modules/5.14.0-427.13.1.el9_4.x86_64/kernel/arch/x86/kvm/
├── kvm-amd.ko.xz
├── kvm-intel.ko.xz
└── kvm.ko.xz
0 directories, 3 files
````

**Ubuntu系统**

````console
root@ubuntu-host:~# grep -i kvm /boot/config-6.11.0-19-generic
CONFIG_KVM_GUEST=y
CONFIG_KVM_COMMON=y
CONFIG_HAVE_KVM_PFNCACHE=y
CONFIG_HAVE_KVM_IRQCHIP=y
CONFIG_HAVE_KVM_IRQ_ROUTING=y
CONFIG_HAVE_KVM_DIRTY_RING=y
CONFIG_HAVE_KVM_DIRTY_RING_TSO=y
CONFIG_HAVE_KVM_DIRTY_RING_ACQ_REL=y
CONFIG_KVM_MMIO=y
CONFIG_KVM_ASYNC_PF=y
CONFIG_HAVE_KVM_MSI=y
CONFIG_HAVE_KVM_READONLY_MEM=y
CONFIG_HAVE_KVM_CPU_RELAX_INTERCEPT=y
CONFIG_KVM_VFIO=y
CONFIG_KVM_GENERIC_DIRTYLOG_READ_PROTECT=y
CONFIG_KVM_GENERIC_PRE_FAULT_MEMORY=y
CONFIG_KVM_COMPAT=y
CONFIG_HAVE_KVM_IRQ_BYPASS=y
CONFIG_HAVE_KVM_NO_POLL=y
CONFIG_KVM_XFER_TO_GUEST_WORK=y
CONFIG_HAVE_KVM_PM_NOTIFIER=y
CONFIG_KVM_GENERIC_HARDWARE_ENABLING=y
CONFIG_KVM_GENERIC_MMU_NOTIFIER=y
CONFIG_KVM_GENERIC_MEMORY_ATTRIBUTES=y
CONFIG_KVM_PRIVATE_MEM=y
CONFIG_KVM_GENERIC_PRIVATE_MEM=y
CONFIG_HAVE_KVM_ARCH_GMEM_PREPARE=y
CONFIG_HAVE_KVM_ARCH_GMEM_INVALIDATE=y
CONFIG_KVM=m
CONFIG_KVM_WERROR=y
CONFIG_KVM_SW_PROTECTED_VM=y
CONFIG_KVM_INTEL=m
CONFIG_KVM_INTEL_PROVE_VE=y
CONFIG_X86_SGX_KVM=y
CONFIG_KVM_AMD=m
CONFIG_KVM_AMD_SEV=y
CONFIG_KVM_SMM=y
CONFIG_KVM_HYPERV=y
CONFIG_KVM_XEN=y
````

````console
# CONFIG_KVM_PROVE_MMU is not set
CONFIG_KVM_EXTERNAL_WRITE_TRACKING=y
CONFIG_KVM_MAX_NR_VCPUS=4096
CONFIG_PTP_1588_CLOCK_KVM=m
CONFIG_DRM_I915_GVT_KVMGT=m
root@ubuntu-host:~# tree /lib/modules/6.11.0-19-generic/kernel/arch/x86/kvm/
/lib/modules/6.11.0-19-generic/kernel/arch/x86/kvm/
├── kvm-amd.ko.zst
├── kvm-intel.ko.zst
└── kvm.ko.zst
1 directory, 3 files
````

## 1.3 部署KVM

### 基础环境

#### 虚拟调整

**前提**

1. 有一台创建好的虚拟机
   - 资源给的多一些
2. 因为我们实验kvm，所以要指定虚拟化引擎，不然的话，无法做虚拟化实验，效果如下勾选虚拟化引擎

![原文插图（第 25 页）]({{ '/subjects/KVM/assets/p025-img01.png' | relative_url }})

#### 异常处理

但是点击 启动虚拟机【无论Rocky还是Ubuntu】之后，会发生如下提示

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img01.png' | relative_url }})

如果出现无法启动，可能是因为开启Hyper-V功能，可以以管理员方式执行下面命令

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img02.png' | relative_url }})

**执行如下命令**

**禁用Hyper-V Hypervisor**

C:\Windows\System32>bcdedit /set hypervisorlaunchtype off 操作成功完成。

![原文插图（第 26 页）]({{ '/subjects/KVM/assets/p026-img03.png' | relative_url }})

重启主机后，重新打开虚拟机即可

#### 验证效果

##### Rocky验证效果

**确保CPU支持HVM**

**inter的CPU效果**

````console
[root@kvm-host ~]# egrep '(vmx|svm)' /proc/cpuinfo
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat pse36 clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc
arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid
tsc_known_freq pni pclmulqdq "vmx" ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe
popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm
3dnowprefetch cpuid_fault ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow ept vpid
ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap
clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves arat vnmi umip pku ospke
gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear flush_l1d
arch_capabilities
...
AMD的CPU效果
[root@kvm-host ~]# egrep '(vmx|svm)' /proc/cpuinfo
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat pse36 clflush mmx fxsr sse sse2 syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm
constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid
tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt aes
xsave avx f16c rdrand hypervisor lahf_lm "svm" extapic cr8_legacy abm sse4a
misalignsse 3dnowprefetch osvw topoext ssbd ibrs ibpb vmmcall fsgsbase bmi1 avx2
smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec
xgetbv1 xsaves clzero wbnoinvd arat npt svm_lock nrip_save vmcb_clean flushbyasid
decodeassists umip pku ospke vaes vpclmulqdq rdpid overflow_recov succor fsrm
注意：
    上面的引号是为了高亮，自己主动添加的
    存在几颗cpu，上面的内容就会显示几行
    Intel CPU 对应 vmx
    AMD CPU 对应 svm
````

**确认支持模块**

**Inter的CPU效果**

````console
[root@kvm-host ~]# lsmod | egrep 'kvm|Module'
Module Size Used by
kvm_intel 442368 0
kvm 1339392 1 kvm_intel
irqbypass 16384 1 kvm
AMD的CPU效果
[root@kvm-host ~]# lsmod | egrep 'kvm|Module'
Module Size Used by
kvm_amd 212992 0
ccp 147456 1 kvm_amd
kvm 1339392 1 kvm_amd
irqbypass 16384 1 kvm
注意：
    如果有信息，就表明我们的虚拟机支持虚拟化。
````

**查看设备文件**

````console
[root@kvm-host ~]# ls /dev/kvm
/dev/kvm
````

##### Ubuntu验证效果

**确保CPU支持HVM**

**Inter CPU效果**

````console
root@ubuntu-host:~# egrep '(vmx|svm)' /proc/cpuinfo
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat pse36 clflush mmx fxsr sse sse2 ss syscall nx pdpe1gb rdtscp lm constant_tsc
arch_perfmon rep_good nopl xtopology tsc_reliable nonstop_tsc cpuid
tsc_known_freq pni pclmulqdq "vmx" ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe
popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm
3dnowprefetch cpuid_fault ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow ept vpid
ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdseed adx smap
clflushopt clwb sha_ni xsaveopt xsavec xgetbv1 xsaves arat vnmi umip pku ospke
gfni vaes vpclmulqdq rdpid movdiri movdir64b fsrm md_clear flush_l1d
arch_capabilities
...
AMD的CPU效果
root@ubuntu-host:~# egrep '(vmx|svm)' /proc/cpuinfo
flags : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
pat pse36 clflush mmx fxsr sse sse2 syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm
constant_tsc rep_good nopl tsc_reliable nonstop_tsc cpuid extd_apicid
tsc_known_freq pni pclmulqdq ssse3 fma cx16 sse4_1 sse4_2 x2apic movbe popcnt aes
xsave avx f16c rdrand hypervisor lahf_lm "svm" extapic cr8_legacy abm sse4a
misalignsse 3dnowprefetch osvw topoext ssbd ibrs ibpb vmmcall fsgsbase bmi1 avx2
smep bmi2 erms invpcid rdseed adx smap clflushopt clwb sha_ni xsaveopt xsavec
xgetbv1 xsaves user_shstk clzero wbnoinvd arat npt svm_lock nrip_save vmcb_clean
flushbyasid decodeassists umip pku ospke vaes vpclmulqdq rdpid overflow_recov
succor fsrm
注意：
    上面的引号是为了高亮，自己主动添加的
    存在几颗cpu，上面的内容就会显示几行
    Intel CPU 对应 vmx
    AMD CPU 对应 svm
````

**确认支持模块**

**Inter CPU效果**

````console
root@ubuntu-host:~# lsmod | egrep 'kvm|Module'
Module Size Used by
kvm_intel 487424 0
kvm 1437696 1 kvm_intel
irqbypass 12288 1 kvm
````

**AMD的CPU效果**

````console
root@ubuntu-host:~# lsmod | egrep 'kvm|Module'
Module Size Used by
kvm_amd 208896 0
ccp 143360 1 kvm_amd
kvm 1404928 1 kvm_amd
irqbypass 12288 1 kvm
注意：
    如果有信息，就表明我们的虚拟机支持虚拟化。
````

**查看设备文件**

````console
root@ubuntu-host:~# ls /dev/kvm
/dev/kvm
````

### 环境部署

#### kvm工具包

**常见工具包**

````text
qemu-kvm:
    为kvm提供底层仿真支持
libvirt-daemon:
    libvirtd守护进程，管理虚拟机
libvirt-client:
    用户端软件，提供客户端管理命令
libvirt-daemon-driver-qemu:
    libvirtd连接qemu的驱动
libvirt:
    使用最多的KVM虚拟化管理工具和应用程序接口，即通过libvirt调用KVM创建虚拟机，
libvirt:
    是KVM通用的访问API，其不但能管理KVM，还能管理VMware、Xen、Hyper-V、virtualBox等虚拟化
方案。
virt-manager:
    图形界面管理工具,其底层也是调用libvirt API来完成对虚拟机的操作，包括虚拟机的创建、删除、启
动、停止以及一些简单的监控功能等。
virt-install:
    虚拟机命令行安装工具
virsh:
    命令行工具是基于 libvirt API 创建的命令行工具，它可以作为图形化的 virt-manager 应用的备
选工具。
    virsh 命令可以被用来创建虚拟化任务管理脚本，如安装、启动和停止虚拟机
virt-viewer:
    通过 VNC 和 SPICE 协议显示虚拟机器图形控制台的最小工具。该工具在其同名软件包中：
virtviewer
cockpit:
    CentOS 和Ubuntu 专门提供的基于Web的虚拟机管理界面
````

#### libvirt

##### 简介

![原文插图（第 30 页）]({{ '/subjects/KVM/assets/p030-img01.png' | relative_url }})

libvirt 程序包是一个与虚拟机监控程序相独立的虚拟化应用程序接口，它可以与操作系统的一系列虚拟化性能进行交互。

**libvirt 程序包提供：**

一个稳定的通用层来安全地管理主机上的虚拟机。一个管理本地系统和连网主机的通用接口。

**功能定位**

在虚拟机监控程序支持的情况下，部署、创建、修改、监测、控制、迁移以及停止虚拟机操作都需要这些 API。尽管 libvirt 可同时访问多个主机，但 API 只限于单节点操作。libvirt 程序包被设计为用来构建高级管理工具和应用程序，例如 virt-manager 与 virsh 命令行管理工具。libvirt 主要的功能是管理单节点主机，并提供 API 来列举、监测和使用管理节点上的可用资源，其中包括CPU、内存、储存、网络和非一致性内存访问（NUMA）分区。管理工具可以位于独立于主机的物理机上，并通过安全协议和主机进行交流。

##### 结构图

![原文插图（第 30 页）]({{ '/subjects/KVM/assets/p030-img02.png' | relative_url }})

#### 镜像准备

**准备课程需要的几个镜像**

Centos7-minial https://mirrors.aliyun.com/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso Rocky9-minial https://mirrors.aliyun.com/rockylinux/9/isos/x86_64/Rocky-9-latest-x86_64-minimal.iso Windows-server 2008 ed2k://|file|cn_windows_server_2008_r2_standard_enterprise_datacenter_and_web_wit h_sp1_vl_build_x64_dvd_617396.iso|3368962048|7C210CAC37A05F459758BCC1F4478F9E|/windows-server 2016 https://download.microsoft.com/download/B/5/F/B5F1A996-B590-45FD-BA99-DE7E745A0882/14393.0.161119-1705.RS1_REFRESH_SERVER_EVAL_X64FRE_ZH-CN.ISO windows-server 2022 https://software-static.download.prss.microsoft.com/pr/download/20348.1.210507-1500.fe_release_amd64fre_SERVER_LOF_PACKAGES_OEM.iso windows-server 2025 https://software-static.download.prss.microsoft.com/dbazure/888969d5-f34g-4e03-ac9d-1f9786c66749/26100.1.240331-1435.ge_release_amd64fre_SERVER_LOF_PACKAGES_OEM.iso

参考资料：https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2025

### Ubuntu安装kvm

#### Ubuntu安装kvm

**安装kvm**

````console
root@ubuntu-host:~# apt install -y qemu-kvm libvirt-daemon-system libvirt-clients
bridge-utils virtinst virt-manager virt-viewer cpu-checker
````

**验证**

**查看虚拟网络**

````console
root@ubuntu-host:~# brctl show
bridge name bridge id STP enabled interfaces
virbr0 8000.52540085ebc4 yes
````

**确认虚拟化效果**

**#如果没有开启CPU虚拟化功能会提示以下信息**

````console
root@ubuntu-host:~# kvm-ok
INFO: Your CPU does not support KVM extensions
KVM acceleration can NOT be used
#添加CPU的虚拟化支持再执行,验证是否支持kvm,只有Ubuntu支持,CentOS 不支持
root@ubuntu-host:~# kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
````

#### Ubuntu安装cockpit

**安装软件**

````console
root@ubuntu-host:~# apt -y install cockpit cockpit-machines
````

默认情况下，该软件禁用了root用户登录

````console
root@ubuntu-host:~# vim /etc/cockpit/disallowed-users
root@ubuntu-host:~# cat /etc/cockpit/disallowed-users
# List of users which are not allowed to login to Cockpit
# root # 注释掉改行，允许root登录
重启主机服务
root@ubuntu-host:~# systemctl restart cockpit
````

**检查服务**

````console
root@ubuntu-host:~# systemctl status cockpit.socket
● cockpit.socket - Cockpit Web Service Socket
     Loaded: loaded (/usr/lib/systemd/system/cockpit.socket; enabled; preset:
enabled)
     Active: active (listening) since Mon 2025-03-24 20:45:45 CST; 11s ago
   Triggers: ● cockpit.service
       Docs: man:cockpit-ws(8)
     Listen: [::]:9090 (Stream)
    Process: 14753 ExecStartPost=/usr/share/cockpit/motd/update-motd localhost
(code=exited, status=0/SUCCESS)
    Process: 14760 ExecStartPost=/bin/ln -snf active.motd /run/cockpit/motd
(code=exited, status=0/SUCCESS)
      Tasks: 0 (limit: 9389)
     Memory: 8.0K (peak: 1.9M)
        CPU: 36ms
     CGroup: /system.slice/cockpit.socket
````

````text
3月 24 20:45:45 ubuntu-host systemd[1]: Starting cockpit.socket - Cockpit Web
Service Socket...
3月 24 20:45:45 ubuntu-host systemd[1]: Listening on cockpit.socket - Cockpit Web
Service Socket.
````

**检查端口**

````console
root@ubuntu-host:~# netstat -tnulp | grep 9090
tcp6 0 0 :::9090 :::* LISTEN
 1/systemd
````

#### Ubuntu查看cockpit

浏览器访问 192.0.2.13:9090

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img01.png' | relative_url }})

**点击高级**

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img02.png' | relative_url }})

点击 继续访问 192.0.2.13(不安全)

![原文插图（第 33 页）]({{ '/subjects/KVM/assets/p033-img03.png' | relative_url }})

输入系统用户root以及配套的密码 EXAMPLE_PASSWORD，如果提示禁止登录的话，需要开启root登录的配置，参考上一节

![原文插图（第 34 页）]({{ '/subjects/KVM/assets/p034-img01.png' | relative_url }})

#### virt-manager工具

注意：该工具依赖于桌面的管理系统，如果操作系统不是桌面版会

**命令行执行**

````console
root@ubuntu-host:~# virt-manager
````

稍等一会，就会出现一个图形化管理工具

![原文插图（第 34 页）]({{ '/subjects/KVM/assets/p034-img02.png' | relative_url }})

### Rocky安装kvm

#### Rocky安装kvm

**准备依赖源**

````console
[root@kvm-host ~]# yum install epel-release
````

**安装软件**

**方法1：**

````console
[root@kvm-host ~]# yum groupinstall "Virtualization Host"
方法2：
[root@kvm-host ~]# yum install qemu-kvm libvirt virt-manager virt-install virt-
viewer bridge-utils
````

**启动服务**

````console
[root@kvm-host ~]# systemctl enable --now libvirtd
````

**确认效果**

````console
[root@kvm-host ~]# brctl show
bridge name bridge id STP enabled interfaces
virbr0 8000.5254006b689d yes
````

**查看路由信息**

````console
root@ubuntu-host:~# route -n
内核 IP 路由表
目标 网关 子网掩码 标志 跃点 引用 使用 接口
0.0.0.0 192.0.2.2 0.0.0.0 UG 100 0 0 eth0
192.0.2.0 0.0.0.0 255.255.255.0 U 100 0 0 eth0
198.18.122.0 0.0.0.0 255.255.255.0 U 0 0 0 virbr0
root@ubuntu-host:~# ps aux | grep -v grep | grep dns
libvirt+ 7465 0.0 0.0 11484 2220 ? S 20:42 0:00
/usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-
ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
root 7466 0.0 0.0 11484 1068 ? S 20:42 0:00
/usr/sbin/dnsmasq --conf-file=/var/lib/libvirt/dnsmasq/default.conf --leasefile-
ro --dhcp-script=/usr/lib/libvirt/libvirt_leaseshelper
结果显示：
    安装完毕软件后，KVM 默认创建了一个 virbr0的虚拟网卡，为虚机网卡提供 NAT 访问外网的功能
    关于该网段的信息是通过dnsmasq服务来提供dns和dhcp服务的
````

#### Rocky安装cockpit

**安装软件**

````console
[root@kvm-host ~]# yum install cockpit cockpit-machines
````

默认情况下，该软件禁用了root用户登录

````console
[root@kvm-host ~]# vim /etc/cockpit/disallowed-users
[root@kvm-host ~]# cat /etc/cockpit/disallowed-users
# List of users which are not allowed to login to Cockpit
# root # 注释掉改行，允许root登录
````

**重启主机服务**

````console
[root@kvm-host ~]# systemctl enable --now cockpit
````

**确认效果**

````console
[root@kvm-host ~]# systemctl status cockpit.service
● cockpit.service - Cockpit Web Service
     Loaded: loaded (/usr/lib/systemd/system/cockpit.service; static)
     Active: active (running) since Mon 2025-03-24 21:06:22 CST; 17s ago
TriggeredBy: ● cockpit.socket
       Docs: man:cockpit-ws(8)
    Process: 7028 ExecStartPre=/usr/libexec/cockpit-certificate-ensure --for-
cockpit-tls (code=exited, status=0/SUCCESS)
   Main PID: 7049 (cockpit-tls)
      Tasks: 1 (limit: 100116)
     Memory: 1.8M
        CPU: 6.231s
     CGroup: /system.slice/cockpit.service
             └─7049 /usr/libexec/cockpit-tls
3月 24 21:06:16 kvm-host systemd[1]: Starting Cockpit Web Service...
3月 24 21:06:22 kvm-host systemd[1]: Started Cockpit Web Service.
````

**确认端口**

````console
[root@kvm-host ~]# netstat -tnulp | grep 9090
tcp6 0 0 :::9090 :::* LISTEN 1/systemd
````

#### Rocky查看cockpit

浏览器访问 192.0.2.12:9090

![原文插图（第 36 页）]({{ '/subjects/KVM/assets/p036-img01.png' | relative_url }})

**点击 高级**

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img01.png' | relative_url }})

点击 继续访问 192.0.2.12(不安全)

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img02.png' | relative_url }})

**输入服务器登录用户名 root以及配套的密码 EXAMPLE_PASSWORD**

![原文插图（第 37 页）]({{ '/subjects/KVM/assets/p037-img03.png' | relative_url }})

#### 创建虚拟机

**上传一个虚拟机镜像**

````console
[root@kvm-host ~]# mkdir /data/images -p
上传文件
[root@kvm-host ~]# ls /data/images/
CentOS-7-x86_64-Minimal-2009.iso
````

**点击左边栏的 虚拟机**

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img01.png' | relative_url }})

点击创建虚拟机，相关配置如图所示

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img02.png' | relative_url }})

注意：关于镜像的选择，需要一层目录一层目录的选择，不会一下子输出出来

**点击 创建并运行**

![原文插图（第 38 页）]({{ '/subjects/KVM/assets/p038-img03.png' | relative_url }})

点击centos7.0 的虚拟机名字

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img01.png' | relative_url }})

**可以看到虚拟机已经开始创建了**

#### 移除虚拟机

点击工作界面 左上角的 虚拟机，回到虚拟机的列表界面

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img02.png' | relative_url }})

**点击关机左侧的三个小点点**

![原文插图（第 39 页）]({{ '/subjects/KVM/assets/p039-img03.png' | relative_url }})

**点击 删除**

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img01.png' | relative_url }})

**确认要删除的关联信息**

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img02.png' | relative_url }})

#### virt-manager工具

**命令行执行**

````console
[root@kvm-host ~]# virt-manager
````

稍等一会，就会出现一个图形化管理工具

![原文插图（第 40 页）]({{ '/subjects/KVM/assets/p040-img03.png' | relative_url }})

注意： 如果rocky没有安装桌面环境的话，执行上面的命令会导致如下问题

````console
[root@kvm-host ~]# virt-manager
[root@kvm-host ~]#
(virt-manager:37183): Gtk-WARNING **: 11:36:38.431: cannot open display:
````

**解决方法：**

````console
[root@kvm-host ~]# yum groupinstall "带 GUI 的服务器"
[root@kvm-host ~]# yum update
[root@kvm-host ~]# reboot
````

#### 网络信息

安装完虚拟工具后,会自动生成一个 virbr0 网卡,类似于Vmware workstation 生成的VMnet8 网卡,充当虚拟机的 NAT 网卡

````console
[root@kvm-host ~]# ifconfig virbr0
virbr0: flags=4099<UP,BROADCAST,MULTICAST> mtu 1500
        inet 198.18.122.1 netmask 255.255.255.0 broadcast 198.18.122.255
        ether 02:00:00:00:00:04 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 0 bytes 0 (0.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
````

改网卡的基本配置文件[配置文件的路径在Rocky和Ubuntu上路径及其效果一样]

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

### 创建虚拟机

#### 打开界面

virt-manager 是一个图形化虚拟机管理工具,方便管理和查看虚拟机

需要提前在Windows上安装X Server的相关软件,比如:Xmanager,xming等才能在Windows显示图形工具。对于mobaxterm来说，其自身已经包含 X Server工具，所以可以直接打开。

**命令行执行**

````console
[root@kvm-host ~]# virt-manager
````

稍等一会，就会出现一个图形化管理工具

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img01.png' | relative_url }})

**点击新建虚拟机**

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img02.png' | relative_url }})

#### 选中镜像文件

点击本地安装介质，然后点击浏览进入到 定位 ISO介质卷位置

![原文插图（第 42 页）]({{ '/subjects/KVM/assets/p042-img03.png' | relative_url }})

选中我们之前说的目录 /data/images ,如果右侧没有CentOS的镜像，可以点击本地浏览的方式找到它

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img01.png' | relative_url }})

#### 定制vm资源配置

选中CentOS镜像后，点击 Choose Volume，就可以看到镜像已经选择完毕了，然后点击 Forward

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img02.png' | relative_url }})

调整虚拟机的资源为2C2G，磁盘空间为20G，然后点击 Forward

![原文插图（第 43 页）]({{ '/subjects/KVM/assets/p043-img03.png' | relative_url }})

#### 安装系统

勾选，在安装前自定义配置后，点击完成，可以看到安装VM前的效果

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img01.png' | relative_url }})

其他的操作，和之前的Rocky安装的步骤一样，等所有的配置做完后，查看安装效果

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img02.png' | relative_url }})

**等待出现 重启主机**

![原文插图（第 44 页）]({{ '/subjects/KVM/assets/p044-img03.png' | relative_url }})

然后点击重启主机后，确认效果

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img01.png' | relative_url }})

#### 查看监控效果

点击virt-manager的管理界面，可以看到运行虚拟机的监控状态

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img02.png' | relative_url }})

如果看不到 cpu使用率的话，可以点击 查看

![原文插图（第 45 页）]({{ '/subjects/KVM/assets/p045-img03.png' | relative_url }})

#### 确认效果

**查看生成的vm映像文件**

**查看镜像文件目录大小**

````console
[root@kvm-host ~]# du -sh /var/lib/libvirt/images/
1.7G /var/lib/libvirt/images/
查看镜像文件的标称容量
[root@kvm-host ~]# ll /var/lib/libvirt/images -h
总用量 1.7G
-rw------- 1 qemu qemu 21G 3月 24 22:44 centos7.0.qcow2
注意：
    此处指定的磁盘会生成一个qcow2的稀疏格式文件,此处可以指定文件最大容量,但实际只占用实际的空间
大小,使用du -sh 文件可以观察到实际大小,使用ls -l 命令看到是此处指定的大小
````

**查看虚拟机保存配置**

````console
[root@kvm-host ~]# ll /etc/libvirt/qemu/
总用量 8
drwx------ 2 root root 6 3月 18 15:55 autostart
-rw------- 1 root root 7119 3月 24 22:34 centos7.0.xml
drwx------ 3 root root 42 3月 24 21:11 networks
````

**查看虚拟机的配置**

````console
[root@kvm-host ~]# cat /etc/libvirt/qemu/centos7.0.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh edit centos7.0
or other application using the libvirt API.
-->
<domain type='kvm'>
  <name>centos7.0</name>
  <uuid>00000000-0000-4000-8000-000000000003</uuid>
  <metadata>
    <libosinfo:libosinfo
xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
      <libosinfo:os id="http://centos.org/centos/7.0"/>
    </libosinfo:libosinfo>
  </metadata>
  <memory unit='KiB'>2097152</memory>
  <currentMemory unit='KiB'>2097152</currentMemory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64' machine='pc-q35-rhel9.4.0'>hvm</type>
    <boot dev='hd'/>
  </os>
````

````xml
  <features>
    <acpi/>
    <apic/>
  </features>
  <cpu mode='host-passthrough' check='none' migratable='on'/>
  <clock offset='utc'>
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled='no'/>
    <suspend-to-disk enabled='no'/>
  </pm>
  <devices>
    <emulator>/usr/libexec/qemu-kvm</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' discard='unmap'/>
      <source file='/var/lib/libvirt/images/centos7.0.qcow2'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <target dev='sda' bus='sata'/>
      <readonly/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <controller type='usb' index='0' model='qemu-xhci' ports='15'>
      <address type='pci' domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
    </controller>
    ... # 大量的controller配置
    <interface type='network'>
      <mac address='02:00:00:00:00:06'/>
      <source network='default'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
    <serial type='pty'>
      <target type='isa-serial' port='0'>
        <model name='isa-serial'/>
      </target>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <channel type='unix'>
      <target type='virtio' name='org.qemu.guest_agent.0'/>
      <address type='virtio-serial' controller='0' bus='0' port='1'/>
    </channel>
    <input type='tablet' bus='usb'>
      <address type='usb' bus='0' port='1'/>
    </input>
````

````xml
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='vnc' port='-1' autoport='yes'>
      <listen type='address'/>
    </graphics>
    <audio id='1' type='none'/>
    <video>
      <model type='vga' vram='16384' heads='1' primary='yes'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
    </video>
    <watchdog model='itco' action='reset'/>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
    </memballoon>
    <rng model='virtio'>
      <backend model='random'>/dev/urandom</backend>
      <address type='pci' domain='0x0000' bus='0x06' slot='0x00' function='0x0'/>
    </rng>
  </devices>
</domain>
[root@kvm-host ~]#
````

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/02-create-vm-from-cli.html' | relative_url }}">下一章：命令创建虚拟机 →</a>
</nav>
