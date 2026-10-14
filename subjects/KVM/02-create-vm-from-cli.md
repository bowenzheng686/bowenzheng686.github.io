---
layout: default
title: 'KVM 虚拟化 · 命令创建虚拟机'
subject_page: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 02 章 · 命令创建虚拟机

> 公开版已将实验密码、主机标识和网络地址替换为示例值；正文图片已恢复，截图中的敏感区域已做本地像素覆盖。执行命令前请按实际环境调整。

## 2.1 常见命令

### 基础知识

**工具体系**

![原文插图（第 48 页）]({{ '/subjects/KVM/assets/p048-img01.png' | relative_url }})

**虚拟机的管理有两套管理工具：**

qemu：linux内核支持的专用kvm管理工具 qemu-kvm 结合虚拟化软件qemv管理kvm虚拟机的集成工具集

````bash
    qemu-img 虚拟磁盘的管理工具
````

libvirt：通用的虚拟化技术管理工具

````bash
    virt-install 虚拟机专用创建工具
    virsh 操作虚拟环境的一个命令行管理工具，支持远程管理操作
    virt-manager 管理虚拟机的图形化的桌面用户接口
````

我们的学习过程中创建虚拟机选用virt-install，管理虚拟机使用virsh，磁盘用qemu-img。

### 配置结构

安装完毕kvm之后，会形成一个专用的目录结构

````bash
[root@kvm-host ~]# ls /etc/libvirt/
hooks libxl-sanlock.conf qemu-sanlock.conf
libvirt-admin.conf lxc.conf secrets
libvirt.conf nwfilter storage
libvirtd.conf qemu virtlockd.conf
libxl.conf qemu.conf virtlogd.conf
libxl-lockd.conf qemu-lockd.conf virt-login-shell.conf
注意：
    qemu目录是我们创建虚拟机后，保存虚拟机配置文件的目录
````

### 命令解读

虽然使用 virt-manager 可以方便的管理虚拟机,但如果需要批量进行虚拟机的创建管理,命令行工具virt-install 更加方便和适合

**virt-install命令解读**

````bash
[root@kvm-host ~]# virt-install --help
usage: virt-install --name NAME --memory MB STORAGE INSTALL [options]
从指定安装源创建新虚拟机。
optional arguments:
  -h, --help show this help message and exit
  --version show program's version number and exit
  --connect URI 通过 libvirt URI 连接到虚拟机管理程序
通用选项:
  -n NAME, --name NAME 客户机实例名称
  --memory MEMORY 配置客户机内存分配。示例：
                        --memory 1024 (in MiB)
                        --memory memory=1024,currentMemory=512
  --vcpus VCPUS 为客户机配置的 vCPU 数。示例：
                        --vcpus 5
                        --vcpus 5,maxvcpus=10,cpuset=1-4,6,8
                        --vcpus sockets=2,cores=4,threads=2
  --cpu CPU CPU 型号和功能。示例：
                        --cpu coreduo,+x2apic
                        --cpu host-passthrough
````

````text
                        --cpu host
  --metadata METADATA 配置客户机元数据。例如：
                        --metadata name=foo,title="My pretty title",uuid=...
                        --metadata description="My nice long description"
  --xml XML 在最终 XML 上执行原始 XML XPath 选项。 示例：
                        --xml ./cpu/@mode=host-passthrough
                        --xml ./devices/disk[2]/serial=new-serial
                        --xml xpath.delete=./clock
安装方法选项:
  --cdrom CDROM 光驱安装介质
  -l LOCATION, --location LOCATION
                        发行版安装 URL，例如：https://host/path。请参见手册页获取有关特
定发行的示例。
  --pxe 使用 PXE 协议从网络引导
  --import 在已有的磁盘镜像中构建客户机
  -x EXTRA_ARGS, --extra-args EXTRA_ARGS
                        将附加参数添加到由 --location 引导的内核中
  --initrd-inject INITRD_INJECT
                        添加指定文件到由 --location 指定的 initrd 根中
  --unattended [UNATTENDED]
                        执行无人值守安装
  --install INSTALL 指定细粒度的安装选项
  --reinstall DOMAIN 重新安装现有的虚拟系统。仅应用安装选项，忽略所有其他虚拟系统配置选
项。
  --cloud-init [CLOUD_INIT]
                        执行云映像安装，配置 cloud-init
  --boot BOOT 配置客户机引导设置。例如：
                        --boot hd,cdrom,menu=on
                        --boot init=/sbin/init (针对容器)
  --idmap IDMAP 为 LXC 容器启用用户名称空间。示例：
                        --idmap uid.start=0,uid.target=1000,uid.count=10
操作系统选项:
  --os-variant OS_VARIANT, --osinfo OS_VARIANT
                        要安装到客户机中的操作系统。
                        This is used for deciding optimal defaults like VirtIO.
                        Example values: fedora29, rhel7.0, win10, ...
                        Use '--osinfo list' to see a full list.
设备选项:
  --disk DISK 指定存储的各种选项。例如：
                        --disk size=10 (在默认位置创建 10GiB 镜像)
                        --disk /my/existing/disk,cache=none
                        --disk device=cdrom,bus=scsi
                        --disk=?
  -w NETWORK, --network NETWORK
                        配置客户机网络接口。例如：
                        --network bridge=mybr0
                        --network network=my_libvirt_virtual_net
                        --network network=mynet,model=virtio,mac=00:11...
                        --network none
                        --network help
  --graphics GRAPHICS 配置客户机显示设定。示例：
                        --graphics spice
                        --graphics vnc,port=5901,listen=0.0.0.0
````

````text
                        --graphics none
  --controller CONTROLLER
                        Configure a guest controller device. Ex:
                        --controller type=usb,model=qemu-xhci
                        --controller type=scsi,model=virtio-scsi
  --input INPUT 配置客户机输入设备。例如：
                        --input tablet
                        --input keyboard,bus=usb
  --serial SERIAL 配置客户机串口设备
  --parallel PARALLEL 配置客户机并口设备
  --channel CHANNEL 配置客户机通信通道
  --console CONSOLE 配置文本控制台连接主机与客户机
  --hostdev HOSTDEV 配置物理 USB/PCI 等主机设备与客户机共享
  --filesystem FILESYSTEM
                        传递主机目录到客户机。例如：
                        --filesystem /my/source/dir,/dir/in/guest
                        --filesystem template_name,/,type=template
  --sound [SOUND] 配置客户机声音设备仿真
  --audio AUDIO Configure host audio backend for sound devices
  --watchdog WATCHDOG 配置客户机看门狗设备
  --video VIDEO 配置客户机视频硬件。
  --smartcard SMARTCARD
                        配置客户机智能卡设备。例如：
                        --smartcard mode=passthrough
  --redirdev REDIRDEV 配置客户机重定向设备。例如：
                        --redirdev usb,type=tcp,server=198.51.100.1:4000
  --memballoon MEMBALLOON
                        配置客户机 memballoon 设备。例如：
                        --memballoon model=virtio
  --tpm TPM 配置客户机 TPM 设备。例如：
                        --tpm /dev/tpm
  --rng RNG 配置客户机 RNG 设备。示例：
                        --rng /dev/urandom
  --panic PANIC 配置客户机 panic 设备。例如：
                        --panic default
  --shmem SHMEM Configure a guest shared memory device. Ex:
                        --shmem name=shmem0
  --memdev MEMDEV 配置客户机内存设备。示例：
                        --memdev dimm,target.size=1024
  --vsock VSOCK 配置客户机 vsock 套接字。示例：
                        --vsock cid.auto=yes
                        --vsock cid.address=7
  --iommu IOMMU 配置 IOMMU 设备。示例：
                        --iommu model=intel,driver.aw_bits=48
客户机配置选项:
  --iothreads IOTHREADS
                        设定域 <iothreads> 和 <iothreadids> 配置。
  --seclabel SECLABEL, --security SECLABEL
                        设定域 seclabel 配置。
  --keywrap KEYWRAP 设定客户机以执行 S390 加密密钥管理操作。
  --cputune CPUTUNE 调整域进程的 CPU 参数。
  --numatune NUMATUNE 为域进程调整 NUMA 策略。
  --memtune MEMTUNE 为域进程调整内存策略。
  --blkiotune BLKIOTUNE
                        为域进程调整 blkio 策略。
````

````text
  --memorybacking MEMORYBACKING
                        为域进程设置内存后备策略。例如：
                        --memorybacking hugepages=on
  --features FEATURES 设定域 <features> XML。示例：
                        --features acpi=off
                        --features apic=on,apic.eoi=on
  --clock CLOCK 设置域 <clock> XML。例如：
                        --clock offset=localtime,rtc_tickpolicy=catchup
  --pm PM 配置 虚拟系统 电源管理功能
  --events EVENTS 配置 虚拟系统 生命周期管理策略
  --resource RESOURCE 配置 虚拟系统 资源分区(cgroups)
  --sysinfo SYSINFO 配置 SMBIOS 系统信息。示例：
                        --sysinfo host
                        --sysinfo bios.vendor=MyVendor,bios.version=1.2.3,...
  --qemu-commandline QEMU_COMMANDLINE
                        将参数直接传递给 QEMU 模拟器。示例：
                        --qemu-commandline='-display gtk,gl=on'
                        --qemu-commandline env=DISPLAY=:0.1
  --launchSecurity LAUNCHSECURITY, --launchsecurity LAUNCHSECURITY
                        Configure VM launch security (e.g. SEV memory
encryption). Ex:
                        --launchSecurity sev
虚拟化平台选项:
  -v, --hvm 这个客户机应该是一个全虚拟化客户机
  -p, --paravirt 这个客户机应该是一个半虚拟化客户机
  --container 这个客户机应该是一个容器客户机
  --virt-type VIRT_TYPE
                        要使用的虚拟机管理程序名称 (kvm, qemu, xen, ...)
  --arch ARCH 模拟 CPU 架构
  --machine MACHINE 机器类型为仿真类型
其它选项:
  --autostart 主机启动时自动启动域。
  --transient 创建一个临时域。
  --destroy-on-exit 关闭控制台查看器后，强制关闭域电源。
  --wait [WAIT] 请等待数分钟以便完成安装。
  --autoconsole AUTOCONSOLE
                        配置客户机控制台自动连接。示例：
                        --autoconsole text
                        --autoconsole graphical
                        --autoconsole none
  --noautoconsole 不要自动尝试连接到客户端控制台
  --noreboot 安装完成后不启动客户机。
  --print-xml [XMLONLY]
                        打印生成的 XML 域，而不是创建客户机。
  --dry-run 运行安装程序，但不创建设备或定义客户机。
  --check CHECK 启用或禁用验证检查。例如：
                        --check path_in_use=off
                        --check all=off
  -q, --quiet 抑制非错误输出
  -d, --debug 输入故障排除信息
使用 '--option=?' 或 '--option help' 来查看可用的子选项
请参考 man 手册，以便了解示例和完整的选项语法。
````

## 2.2 初始化

### 基础知识

#### 创建磁盘

需求：要创建虚拟机，就需要给他提供一个虚拟的磁盘，我们就在/opt目录下创建一个10G大小的raw格式的虚拟磁盘CentOS-7-x86_64.raw

**查看子命令帮助：**

**用此工具创建的磁盘文件显示和实际占用的空间都是很小的**

````bash
qemu-img create -f 磁盘格式 容量
````

命令格式：qemu-img create -f 磁盘格式 磁盘名称 磁盘大小

````bash
[root@kvm-host ~]# qemu-img create -f raw /opt/CentOS-7-x86_64.raw 10G
Formatting '/opt/CentOS-7-x86_64.raw', fmt=raw size=10737418240
````

**执行效果：**

````bash
[root@kvm-host ~]# ls -lh /opt/
总用量 1.0M
-rw-r--r-- 1 root root 10G 3月 24 22:59 CentOS-7-x86_64.raw
````

#### 创建虚拟机

使用virt-install命令，基于我们提供的系统镜像和虚拟磁盘来创建一个虚拟机，另外在创建虚拟机之前，提前打开vnc客户端，在创建虚拟机的时候，通过vnc来连接虚拟机，对其进行配置和查看进度。

````bash
[root@kvm-host ~]# virt-install --virt-type kvm --name CentOS-7-x86_64 --memory
1024 --cdrom=/data/images/CentOS-7-x86_64-Minimal-2009.iso --disk=/opt/CentOS-7-
x86_64.raw --network network=default --graphics vnc,listen=0.0.0.0 --
noautoconsole
参数解析：
    --virt-type kvm 指定创建的虚拟机基于的虚拟化技术
    --name CentOS-7-x86_64 指定创建虚拟机的名字，推荐"简洁"
    --ram 1024 指定创建虚拟机的内存大小
    --cdrom=XX.iso 指定创建虚拟机使用的系统镜像
    --disk path=XX.raw 指定创建虚拟机使用的虚拟磁盘
    --network network=default 指定创建虚拟机使用的网络类型
    --graphics vnc,listen=0.0.0.0 指定访问虚拟机使用的客户端配置信息
    --noautoconsole 禁用配置的客户端自动连接虚拟机
````

#### 连接虚拟机

**打开vnc-viewer软件**

![原文插图（第 54 页）]({{ '/subjects/KVM/assets/p054-img01.png' | relative_url }})

只需要输入一个 192.0.2.12【kvm的主机地址】 即可

![原文插图（第 54 页）]({{ '/subjects/KVM/assets/p054-img02.png' | relative_url }})

通过vnc客户端连接到安装界面,kvm虚拟机的默认端口从5900开始

双击 192.0.2.12 连接

![原文插图（第 55 页）]({{ '/subjects/KVM/assets/p055-img01.png' | relative_url }})

#### 系统安装

**网卡配置**

- 选择安装Centos条目
- 光标移动到“Install Centos7 ...”，
- 通过给内核传递参数，配置网卡
- 按Tab键，编辑配置，在末尾追加 net.ifnames=0 biosdevname=0，编辑完毕后，直接按Enter

![原文插图（第 55 页）]({{ '/subjects/KVM/assets/p055-img02.png' | relative_url }})

接下来跟安装普通系统的步骤一致，毕竟是测试，所以注意以下几项：

**网卡打开：**

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img01.png' | relative_url }})

安装软件：最小化

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img02.png' | relative_url }})

检查安装源：(默认)

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img03.png' | relative_url }})

设置最简单密码：EXAMPLE_PASSWORD

![原文插图（第 56 页）]({{ '/subjects/KVM/assets/p056-img04.png' | relative_url }})

等待系统安装完毕后，点击reboot，重启虚拟机

### 简单操作

#### 连接虚拟机

vnc中虚拟机是不会重启的，需要在宿主机系统中，使用命令开启虚拟机

命令格式：virsh start 虚拟机名称

````bash
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
注意：
    每次关闭虚拟机后，再次开启虚拟机，虚拟机的id都会自动的变化
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
````

**vnc连接登录**

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img01.png' | relative_url }})

**查看ip地址**

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img02.png' | relative_url }})

**查看路由信息**

![原文插图（第 57 页）]({{ '/subjects/KVM/assets/p057-img03.png' | relative_url }})

可以看到：操作方式是跟正常操作linux系统的方式是一致的。

#### 宿主机检查

**宿主机检查网络**

**宿主机检查网络**

````bash
[root@kvm-host ~]# ifconfig
...
virbr0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet 198.18.122.1 netmask 255.255.255.0 broadcast 198.18.122.255
        ether 02:00:00:00:00:04 txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 1 bytes 125 (125.0 B)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
vnet0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST> mtu 1500
        inet6 fe80::fc54:ff:fee8:440d prefixlen 64 scopeid 0x20<link>
        ether 02:00:00:00:00:0a txqueuelen 1000 (Ethernet)
        RX packets 0 bytes 0 (0.0 B)
        RX errors 0 dropped 0 overruns 0 frame 0
        TX packets 105 bytes 6792 (6.6 KiB)
        TX errors 0 dropped 0 overruns 0 carrier 0 collisions 0
效果：
    虚拟机启动后，当前系统中，多出来了一个网卡vnet0，这个vnet网卡没有ipv4的地址
````

**宿主机检查进程**

**宿主机检查进程**

````bash
[root@kvm-host ~]# ps aux | grep CentOS
qemu 2607 14.3 2.8 2844772 462116 ? Sl 13:35 0:27
/usr/libexec/qemu-kvm -name guest=CentOS-7-x86_64,debug-threads=on -S -object
{"qom-
type":"secret","id":"masterKey0","format":"raw","file":"/var/lib/libvirt/qemu/dom
ain-1-CentOS-7-x86_64/master-key.aes"} -machine pc-q35-rhel9.4.0,usb=off,dump-
guest-core=off,memory-backend=pc.ram,hpet=off,acpi=on -accel kvm -cpu
host,migratable=on -m size=1048576k -object ...} -sandbox
on,obsolete=deny,elevateprivileges=deny,spawn=deny,resourcecontrol=deny -msg
timestamp=on
效果：
    虚拟机，本质上就是在宿主机系统上的一个kvm进程，管理虚拟机跟管理进程基本一样
注意：
    我的libvirtd服务即使停止了，它不会影响虚拟机的正常运行
    但是就不能使用virsh来管理虚拟机了
````

#### 配置解析

##### 配置目录

**虚拟机配置**

````bash
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

##### 配置文件

**虚拟机配置文件**

````bash
[root@kvm-host ~]# cat /etc/libvirt/qemu/CentOS-7-x86_64.xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh edit CentOS-7-x86_64 提示我们只能用virsh edit进行编辑这个文件
````

````xml
or other application using the libvirt API.
-->
<domain type='kvm'> # domain完全指虚拟机系统。type一项指明了使用的是哪种虚拟
化技术
  下面几项是虚拟机的全局配置信息：
虚拟机名称和uuid信息
  <name>CentOS-7-x86_64</name> # 名字不允许包含空格
  <uuid>00000000-0000-4000-8000-000000000002</uuid>
内存信息
  <memory unit='KiB'>1048576</memory>
  <currentMemory unit='KiB'>1048576</currentMemory>
cpu信息
  <vcpu placement='static'>1</vcpu>
  <os>
<type arch='x86_64' machine='pc-i440fx-rhel7.0.0'>hvm</type>
# type 表示全虚拟化还是半虚拟化，hvm表示全虚拟化
<boot dev='hd'/> # 表示虚拟机从哪里开机
# boot 怎么启动的，如"fd"表示从文件启动, "hd"从硬盘启动, "cdrom"从光驱启动 和 "network"从
网络启动
#可以重复多行，指定不同的值，作为一个启动设备列表。
#The dev attribute takes one of the values "fd", "hd", "cdrom" or "network"
  </os>
  <features> # 表示硬件资源(处理器)特性
    <acpi/>
    <apic/>
  </features>
  <cpu mode='custom' match='exact'>
    <model fallback='allow'>SandyBridge</model>
  </cpu>
时钟信息
  <clock offset='utc'> # utc表示时间模式，localtime表示使用本地时间
    <timer name='rtc' tickpolicy='catchup'/>
    <timer name='pit' tickpolicy='delay'/>
    <timer name='hpet' present='no'/>
  </clock>
突发事件处理机制
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
注意：
    突发事件处理定义了当发生poweroff时，直接destroy虚拟机。当虚拟机reboot、crash的时候，会
自动采用重启操作，还可以自定义
虚拟机管理配置(内存和磁盘)
  <pm>
    <suspend-to-mem enabled='no'/>
    <suspend-to-disk enabled='no'/>
  </pm>
虚拟机设备信息
注意：
    在虚拟化技术或者云计算中，都使用image一词来表示虚拟磁盘
  <devices> #在<device></device>中的都是虚拟外设
    模拟器信息
<emulator>/usr/libexec/qemu-kvm</emulator>
虚拟机磁盘信息
````

````xml
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/opt/CentOS-7-x86_64.raw'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <target dev='hda' bus='ide'/>
      <readonly/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
</disk>
虚拟机控制器配置信息
    <controller type='usb' index='0' model='ich9-ehci1'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
    </controller>
    ...
    <controller type='virtio-serial' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
</controller>
虚拟机网络接口配置信息
    <interface type='network'>
      <mac address='02:00:00:00:00:05'/>
      <source network='default'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
# 虚拟机的网卡的mac地址，前面的52:54:00地址是固定的，后面的三项是随机的。
虚拟机串口配置信息，可以不用更改
    <serial type='pty'>
      <target port='0'/>
</serial>
虚拟机终端配置信息
    <console type='pty'>
      <target type='serial' port='0'/>
</console>
虚拟机渠道配置信息
    <channel type='unix'>
      <target type='virtio' name='org.qemu.guest_agent.0'/>
      <address type='virtio-serial' controller='0' bus='0' port='1'/>
</channel>
虚拟机输入输出设备信息
    <input type='tablet' bus='usb'>
      <address type='usb' bus='0' port='1'/>
    </input>
    <input type='mouse' bus='ps2'/>
<input type='keyboard' bus='ps2'/>
# vnc方式登录，端口号自动分配 可以通过virsh vncdisplay来查询[vncdisplay domainId]
虚拟机图形设备信息
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
</graphics>
虚拟机声音设备信息
    <video>
````

````xml
      <model type='cirrus' vram='16384' heads='1' primary='yes'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
</video>
虚拟机存储信息
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
    </memballoon>
  </devices>
</domain>
# 虚拟机网络文件
````

注意：配置文件中展示的所有信息，都可以在ps aux 中的进程中一一找到对应的配置项

##### 网络配置

**网络配置文件**

````bash
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

### 基础功能

#### 检查

**命令解析**

````bash
virsh list 列出所有活动的虚拟机
virsh list --all 列出所有活动和不活的的虚拟机
virsh list --transient 列出所有临时的虚拟机
virsh list --persistent 列出所有永久的虚拟机
````

**示例效果**

**查看所有运行中的虚拟机**

````bash
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
查看所有的虚拟机，无论运行与否
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
注意：
    虚拟机的每次重启，虚拟机的id都会自动的变化，因为虚拟机的运行本质上是操作系统的一个进程而已
````

#### 创建

##### 方法解读

创建虚拟机的方式除了初始方法，还有一种经常使用的方法--使用配置文件，而使用配置文件的话，会有

**两种创建的方式：**

**临时创建**
- 借助于现成的配置文件和之前创建的虚拟机数据，创建一个新虚拟机，他会自动清除
- 步骤：配置文件-创建虚拟机-查看
- 命令：virsh create file_name.xml

**正规创建**
- 借助于现成的配置文件在虚拟机管理程序中注册一个新的虚拟机，他不会自动清除
- 步骤：配置文件-注册虚拟机-开启虚拟机-查看
- 命令：virsh define file_name.xml

**关键点：**

尽量拷贝一个完整的虚拟机配置文件，然后修改配置文件中的名字，这个配置文件名称和配置文件中的 name属性要一致，且名字唯一

##### 临时创建

**拷贝文件**

````bash
[root@kvm-host ~]# cd /etc/libvirt/qemu
[root@kvm-host qemu]# cp CentOS-7-x86_64.xml CentOS-7-x86_64-1.xml
[root@kvm-host qemu]# ls
autostart CentOS-7-x86_64-1.xml CentOS-7-x86_64.xml networks
````

**修改配置文件**

````bash
[root@kvm-host qemu]# vim CentOS-7-x86_64-1.xml
    ...
  9 <name>CentOS-7-x86_64-1</name>
 10 <uuid>00000000-0000-4000-8000-00000000000b</uuid>
    ...
    注意：
        主要修改的地方就是：虚拟机的名字，uuid
        虚拟磁盘不需要修改，如果要修改的话，一个新建的虚拟磁盘里面因为没有boot文件，就会报错
        网卡什么的尽量不要更改，更改后即使可以，但是启动不成功
````

因为一个运行中的vm是占用硬件磁盘的，所以会导致资源冲突

````bash
[root@kvm-host qemu]# virsh create /etc/libvirt/qemu/CentOS-7-x86_64-1.xml
错误： 从 /etc/libvirt/qemu/CentOS-7-x86_64-1.xml 创建域失败
错误： 内部错误：连接监控的过程中进程退出: 2025-03-25T05:46:06.860047Z qemu-kvm: -device
{"driver":"virtio-blk-pci","bus":"pci.4","addr":"0x0","drive":"libvirt-2-
storage","id":"virtio-disk0","bootindex":1}: Failed to get "write" lock
Is another process using the image [/opt/CentOS-7-x86_64.raw]?
````

为了避免资源冲突，我们将另外一个虚拟机关闭

````bash
[root@kvm-host qemu]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
[root@kvm-host qemu]# virsh list
 Id 名称 状态
-------------------
````

创建新的虚拟机,而且虚拟机处于运行状态

````bash
[root@kvm-host qemu]# virsh create /etc/libvirt/qemu/CentOS-7-x86_64-1.xml
从 CentOS-7-x86_64-1 创建的域 '/etc/libvirt/qemu/CentOS-7-x86_64-1.xml'
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
--------------------------------
 3 CentOS-7-x86_64-1 运行
 - CentOS-7-x86_64 关闭
可以看到：
    新建的虚拟机已经成功了，而且启动的非常快 - 原因是系统盘是没有变的
````

1.2.2.3.2.3永久创建

**配置文件**

````bash
[root@kvm-host qemu]# cp CentOS-7-x86_64.xml CentOS-7-x86_64-2.xml
````

**编辑虚拟机配置**

````bash
[root@kvm-host qemu]# vim CentOS-7-x86_64-2.xml
...
<domain type='kvm'>
  <name>CentOS-7-x86_64-2</name>
  <uuid>00000000-0000-4000-8000-000000000005</uuid>
  ...
````

关闭虚拟机,刚才临时创建的虚拟机，找不到记录了

````bash
[root@kvm-host qemu]# virsh shutdown CentOS-7-x86_64-1
域 'CentOS-7-x86_64-1' 正在关闭
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
------------------------------
 - CentOS-7-x86_64 关闭
````

**注册虚拟机**

````bash
[root@kvm-host qemu]# virsh define /etc/libvirt/qemu/CentOS-7-x86_64-2.xml
从 CentOS-7-x86_64-2 定义的域 '/etc/libvirt/qemu/CentOS-7-x86_64-2.xml'
查看效果
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-2 关闭
````

**开启虚拟机**

````bash
[root@kvm-host qemu]# virsh start CentOS-7-x86_64-2
域 'CentOS-7-x86_64-2' 已启动
确认效果
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
--------------------------------
 4 CentOS-7-x86_64-2 运行
 - CentOS-7-x86_64 关闭
注意：
    由于多个虚拟机使用同一个磁盘文件，所以，同一时间点内，只允许启动1个虚拟机
````

##### 登录

当我们虚拟机过多的时候，如果想用vnc来连接的话，就不够了，但我还想用vnc怎么办？

**思路：**

执行 'virsh domdisplay 虚拟机名称' 来获取虚拟机的地址信息

**启动虚拟机**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
启动虚拟机
[root@kvm-host ~]# virsh start CentOS-7-x86_64
域 'CentOS-7-x86_64' 已启动
````

**查看运行的地址**

````bash
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
[root@kvm-host ~]# virsh domdisplay CentOS-7-x86_64
vnc://localhost:0
注意：
    :后面的数字n代表虚拟机启动的端口号，特指vnc端口号5900+n
````

**vnc查看连接方式：**

![原文插图（第 66 页）]({{ '/subjects/KVM/assets/p066-img01.png' | relative_url }})

##### console登录

**需求**

- 虽然我们可以使用vnc等方式连接到虚拟机中进行各种操作，但是，对于有些简单操作，使用vnc比较麻
- 烦，所以我们这里学一种轻巧的登录虚拟机的方法：console
- 注意：
- 默认情况下，新安装的虚拟机，是无法通过virsh console 命令连入虚拟机中的，这时我们需要
- 开启虚拟机的console功能。我们可以通过 grubby 来配置grub信息

使用vnc登录到虚拟机，添加ttyS0的许可，然后重启虚拟机

````bash
grubby --update-kernel=ALL --args="console=ttyS0"
reboot
````

重启主机后，确认效果

````bash
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
````

**思路**

**命令帮助：**

````bash
    virsh console --help
命令格式：
    virsh console 虚拟机名称
````

**使用console登录虚拟机**

````bash
[root@kvm-host ~]# virsh console CentOS-7-x86_64
连接到域 'CentOS-7-x86_64'
转义字符是 ^] (Ctrl + ]) # 此处按Enter进入到登录界面
CentOS Linux 7 (Core)
Kernel 3.10.0-1160.el7.x86_64 on an x86_64
localhost login: root
密码：
Last login: Tue Mar 25 20:28:50 on tty1
[root@localhost ~]# id
uid=0(root) gid=0(root) 组=0(root) 环境=unconfined_u:unconfined_r:unconfined_t:s0-
s0:c0.c1023
````

**按 ctrl+] 组合键退出virsh console**

````bash
[root@localhost ~]# # 按 ctrl+] 组合键退出
[root@kvm-host ~]#
````

### 其他功能

#### 挂起

**命令解读**

查看帮助：virsh suspend --help 命令格式：virsh suspend vmhost_name

**挂起实践**

**查看效果**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 1 CentOS-7-x86_64 运行
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
````

**挂起虚拟机**

````bash
[root@kvm-host ~]# virsh suspend CentOS-7-x86_64
域 'CentOS-7-x86_64' 已挂起
````

**查看效果**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
----------------------------------
 1 CentOS-7-x86_64 已暂停
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
````

查看vnc效果，vnc的画面没有任何动的痕迹了 -- vnc界面卡死了，但是虚拟机并没有关机

![原文插图（第 68 页）]({{ '/subjects/KVM/assets/p068-img01.png' | relative_url }})

#### 恢复

**命令解读**

查看帮助：virsh resume --help 命令格式：virsh resume vmhost_name

**恢复虚拟机**

````bash
[root@kvm-host ~]# virsh resume CentOS-7-x86_64
域 'CentOS-7-x86_64' 已恢复
````

**查看效果**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 1 CentOS-7-x86_64 运行
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
````

可以看到：vnc界面里面恢复了，而且可以进行操作

![原文插图（第 69 页）]({{ '/subjects/KVM/assets/p069-img01.png' | relative_url }})

#### 关闭实践

**需求**

虚拟机运行时间太长了，向休息一下，那就关闭咯

**方法**

````bash
virsh shutdown 虚拟机名称
注意：
    shutdown方法依赖于acpid服务，Acpid是一个用户空间的服务进程，它充当linux内核与应用程序之
间通信的接口，负责将kernel中的电源管理事件转发给应用程序。所以要保证我们的操作系统有acpid服务。
````

**acpid服务**

对于ubuntu来说，它会自动安装相关软件并运行该服务对于centos来说，它需要手工安装并启动

````bash
[root@kvm-host ~]# yum install acpid -y
[root@kvm-host ~]# systemctl start acpid
[root@kvm-host ~]# systemctl enable acpid
````

**关闭虚拟机**

````bash
[root@kvm-host ~]# virsh shutdown CentOS-7-x86_64
域 'CentOS-7-x86_64' 正在关闭
````

稍等5秒钟后，才会生效

````bash
[root@kvm-host ~]# virsh list
 Id 名称 状态
-------------------
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
````

使用shutdown关闭的时候，一定要避免资源冲突，特别是基于同一个配置文件创建出来的虚拟机。如果出现这种情况的话，shutdown不管用，使用kill方式关闭或者强制删除方法，示例如下：

**关闭虚拟机**

````bash
   ps aux | grep CentOS
   kill 6589
检查
   virsh list --all
````

#### 强制关闭

**功能简介**

将一个运行中的虚拟机强制关闭。命令格式：virsh destroy 虚拟机名称

**已关闭的虚拟机无法再次被关闭**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
[root@kvm-host ~]# virsh destroy CentOS-7-x86_64-1
错误： 销毁域 'CentOS-7-x86_64-1' 失败
错误： 所需操作无效：域没有在运行
````

**准备运行的虚拟机**

````bash
[root@kvm-host ~]# virsh start CentOS-7-x86_64-1
域 'CentOS-7-x86_64-1' 已启动
[root@kvm-host ~]# virsh list
 Id 名称 状态
--------------------------------
 1 CentOS-7-x86_64-1 运行
````

**强制关闭运行中的虚拟机**

````bash
[root@kvm-host ~]# virsh destroy CentOS-7-x86_64-1
域 'CentOS-7-x86_64-1' 已销毁
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
````

#### 删除实践

正常删除,不影响虚拟机的当前运行状态的删除

删除其配置文件，virsh状态表中存在，关闭虚拟机后，状态表中亦删除命令格式：virsh undefine 虚拟机名称

**删除虚拟机**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-2 关闭
[root@kvm-host ~]# virsh undefine CentOS-7-x86_64-2
domain 'CentOS-7-x86_64-2' 已被解除定义
````

**检查效果**

````bash
[root@kvm-host ~]# virsh list --all
 Id 名称 状态
--------------------------------
 - CentOS-7-x86_64 关闭
 - CentOS-7-x86_64-1 关闭
[root@kvm-host ~]# ls /etc/libvirt/qemu
autostart CentOS-7-x86_64-1.xml CentOS-7-x86_64.xml networks
````

注意：正则运行中的虚拟机会在关闭虚拟机的时候，彻底消失。

### 开机自启动

#### 基础知识

**简介**

默认情况下，创建好的kvm虚拟机不会随宿主机开启而启动，特殊的工作场景中，为了简便工作，我们会将其设置成开机自启动功能。

**命令**

**开启自启动命令格式：**

帮助：virsh autostart --help 开启：virsh autostart 虚拟机名称关闭：virsh autostart --disable 虚拟机名称

**注意：**

开机自启动的操作，仅限于被注册的虚拟机，临时虚拟机没有该功能。

#### 开启自启动

**检查配置文件目录效果**

````bash
[root@kvm-host ~]# ls /etc/libvirt/qemu
autostart CentOS-7-x86_64-1.xml CentOS-7-x86_64.xml networks
````

**设置开机自启动**

````bash
[root@kvm-host ~]# virsh autostart CentOS-7-x86_64
域 'CentOS-7-x86_64' 标记为自动启动
````

**确认效果**

**方法1：**

````bash
[root@kvm-host ~]# tree /etc/libvirt/qemu
/etc/libvirt/qemu
├── autostart # 多了一个autostart目录
│ └── CentOS-7-x86_64.xml -> /etc/libvirt/qemu/CentOS-7-x86_64.xml
├── CentOS-7-x86_64-1.xml
├── CentOS-7-x86_64.xml
└── networks
    ├── autostart
    │ └── default.xml -> ../default.xml
    └── default.xml
3 directories, 5 files
方法2：
[root@kvm-host ~]# virsh list --autostart --all
 Id 名称 状态
------------------------------
 - CentOS-7-x86_64 关闭
````

**重启主机后确认效果**

````bash
[root@kvm-host ~]# reboot
Remote side unexpectedly closed network connection
─────────────────────────────────────────────────────────────────────────────────
───
Session stopped
    - Press <return> to exit tab
    - Press R to restart session
    - Press S to save terminal output to file
登录后确认效果
Last login: Tue Mar 25 20:23:42 2025 from 192.0.2.1
[root@kvm-host ~]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行 # 确实是开机自启动了
````

#### 取消开机自启动

**取消开机自启动**

````bash
[root@kvm-host ~]# virsh autostart --disable CentOS-7-x86_64
域 'CentOS-7-x86_64' 未标记为自动启动
````

**确认目录效果**

````bash
[root@kvm-host ~]# tree /etc/libvirt/qemu
/etc/libvirt/qemu
├── autostart
├── CentOS-7-x86_64-1.xml
├── CentOS-7-x86_64.xml
└── networks
    ├── autostart
    │ └── default.xml -> ../default.xml
    └── default.xml
3 directories, 4 files
````

**确认状态**

````bash
[root@kvm-host ~]# virsh list --no-autostart --all
 Id 名称 状态
--------------------------------
 1 CentOS-7-x86_64 运行
 - CentOS-7-x86_64-1 关闭
````

### 备份编辑

#### 基础知识

**需求**

手工修改虚拟机的配置，限制太多。学习虚拟机配置文件的专用的操作功能。

**基本操作**

- 备份
- 作用：文件内容的版本保存
- 格式：virsh dumpxml 虚拟主机名 > backup_vmhost.file
- 注意：备份文件如果想在本机使用的话，需要vim修改一下主机名和uuid，才可以
- 编辑
- 作用：文件内容的编辑动作
- 格式：virsh edit 虚拟主机名
- 注意：备份的虚拟机文件如果想要使用virsh edit编辑的话，必须要保证该文件已经注册到虚拟机管理
- 设备中了

#### 备份实践

**查看效果**

````bash
[root@kvm-host ~]# cd /etc/libvirt/qemu
[root@kvm-host qemu]# ls
autostart CentOS-7-x86_64-1.xml CentOS-7-x86_64.xml networks
````

**备份文件**

````bash
[root@kvm-host qemu]# virsh dumpxml CentOS-7-x86_64 > CentOS-backup.xml
[root@kvm-host qemu]# ls
autostart CentOS-7-x86_64-1.xml CentOS-7-x86_64.xml CentOS-backup.xml
 networks
````

备份文件如果想在本机使用的话，需要vim修改一下主机名和uuid

````bash
[root@kvm-host qemu]# vim CentOS-backup.xml
<domain type='kvm' id='1'>
  <name>CentOS-7-x86_64-bak</name>
  <uuid>00000000-0000-4000-8000-000000000004</uuid>
    ...
注意：仅仅修改name和uuid即可
````

**创建虚拟机**

````bash
[root@kvm-host qemu]# virsh define CentOS-backup.xml
从 CentOS-7-x86_64-bak 定义的域 'CentOS-backup.xml'
````

**查看效果**

````bash
[root@kvm-host qemu]# virsh list --all
 Id 名称 状态
----------------------------------
 - CentOS-7-x86_64 运行
 - CentOS-7-x86_64-1 关闭
 - CentOS-7-x86_64-bak 关闭
可以看到：
    创建的虚拟机默认情况下是关闭状态的。
````

#### 编辑实践

为了避免资源抢占，这里将所有的虚拟机关闭

````bash
[root@kvm-host qemu]# virsh list
 Id 名称 状态
------------------------------
 1 CentOS-7-x86_64 运行
[root@kvm-host qemu]# virsh shutdown 1
域 '1' 正在关闭
````

**编辑虚拟机**

````bash
[root@kvm-host qemu]# virsh edit CentOS-7-x86_64-bak
域'CentOS-7-x86_64-bak' XML 配置已被编辑。
原内容：
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
修改后内容：
    <graphics type='vnc' port='8888' listen='0.0.0.0' passwd='EXAMPLE_PASSWORD'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
````

**确认效果**

````bash
[root@kvm-host qemu]# virsh start CentOS-7-x86_64-bak
域 'CentOS-7-x86_64-bak' 已启动
[root@kvm-host ~]# virsh domdisplay CentOS-7-x86_64-bak
vnc://localhost:2988
关于vnc的连接，可以是 192.0.2.12:8888，不可以是192.0.2.12:2988
````

上面测试的信息是给 vnc 连接时候登录用的，不是给 virsh console 连接用的，因为virsh console 不走 vnc。

![原文插图（第 76 页）]({{ '/subjects/KVM/assets/p076-img01.png' | relative_url }})

**点击输入密码后的效果**

![原文插图（第 77 页）]({{ '/subjects/KVM/assets/p077-img01.png' | relative_url }})

## 2.3 其他内容

### 基础信息

**查看virsh默认支持的虚拟机操作系统**

````bash
[root@kvm-host ~]# virt-install --osinfo list | wc -l
848
````

**查看支持的win系列的操作系统**

````bash
[root@kvm-host ~]# virt-install --osinfo list |grep win
win98
win95
win11
win10
win8
win8.1
win7
win3.1
win2.1
win2.0
win2k
win2k22
win2k19
win2k16
win2k12
win2k12r2
win2k8
win2k8r2
win2k3
win2k3r2
win1.0
winme
winnt4.0
winnt3.51
winnt3.5
winnt3.1
winvista
winxp
````

### 无需磁盘创建VM

无需事先创建磁盘文件，直接创建虚拟机

**确认支持的系统版本**

````bash
[root@kvm-host ~]# virt-install --osinfo list |grep centos7
centos7, centos7.0
````

**创建虚拟机**

````bash
[root@kvm-host ~]# virt-install --virt-type kvm --os-variant=centos7 --name
centos7 --ram 1024 --vcpus 1 --cdrom=/data/images/CentOS-7-x86_64-Minimal-
2009.iso --disk path=/opt/CentOS-7-x86_64.qcow2,size=10,format=qcow2,bus=virtio -
-network network=default --graphics vnc,listen=0.0.0.0 --noautoconsole
````

**确认效果**

````bash
[root@kvm-host ~]# virsh list
 Id 名称 状态
----------------------------------
 4 CentOS-7-x86_64-bak 运行
 5 centos7 运行
````

### 桥接方式创建VM

注意：使用桥接方式创建vm，需要提前保证是存在桥接网卡的，否则下面的命令无法执行

````bash
[root@kvm-host ~]# virt-install --virt-type kvm --os-variant=centos7 --name
centos7-bridge --ram 1024 --vcpus 1 --cdrom=/data/images/CentOS-7-x86_64-Minimal-
2009.iso --disk path=/opt/CentOS-7-x86_64.qcow2,size=10,format=qcow2,bus=virtio -
-network network=bridge:virbr1,model=virtio --graphics vnc,listen=0.0.0.0 --
noautoconsole
````

### 克隆VM

**打开virt-manager**

````bash
[root@kvm-host ~]# virt-manager
````

clone的方式，仅限于关闭的主机场景

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img01.png' | relative_url }})

**对第一个主机进行克隆操作**

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img02.png' | relative_url }})

查看克隆后效果，克隆后的主机，和之前的主机运行效果一样，而且使用的不是同一个磁盘

![原文插图（第 79 页）]({{ '/subjects/KVM/assets/p079-img03.png' | relative_url }})

# 2 核心知识

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/01-virtualization-basics.html' | relative_url }}">← 上一章：虚拟化基础</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/03-storage-management.html' | relative_url }}">下一章：存储管理 →</a>
</nav>
