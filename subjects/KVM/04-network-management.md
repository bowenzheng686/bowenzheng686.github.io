---
layout: default
title: 'KVM 虚拟化 · 网络管理'
subject_page: true
syntax_highlight: true
---

[← 返回 KVM 目录]({{ '/subjects/KVM/' | relative_url }})

# 第 04 章 · 网络管理

虚拟机网络要回答三个问题：来宾如何连接宿主机、地址由谁分配、流量如何到达上游。libvirt 的 NAT 网络适合快速建立独立实验网段；宿主机桥接则让来宾成为上游局域网中的独立节点。两者都依赖宿主机网络和安全策略，不能简单按“实验用 NAT、生产用桥接”划分。

## 4.1 认识默认 NAT 网络

libvirt 常见的 `default` 网络使用 `virbr0`，由宿主机为来宾提供一个虚拟网段，并通过 NAT 转发来宾的外向流量。相同虚拟网络中的来宾通常可相互通信；来自上游网络的入站访问则需要额外的转发或其他访问路径。

先观察本机状态，而不是照抄旧实验的 `virbr0` 地址：

```bash
virsh net-list --all
virsh net-info default
virsh net-dumpxml default
virsh net-dhcp-leases default
ip addr show virbr0
virsh domiflist <虚拟机名>
```

`net-dumpxml` 中的 `<forward mode='nat'/>` 表示出站地址转换；`<ip>` 与 `<dhcp>` 决定来宾网段与租约范围。`virbr0` 是宿主机的虚拟网桥，不是上游物理交换机的桥。网络是否存在、桥名是什么，应以当前 libvirt 配置为准。

## 4.2 自定义 libvirt NAT 网络

新建虚拟网络前先核对网段不与宿主机、VPN、其他虚拟网络和上游网段冲突。下面的 `10.77.0.0/24` 仅作实验示例；实际环境须选择不重叠的地址空间。

把下面内容保存为 `lab-nat.xml`：

```xml
<network>
  <name>lab-nat</name>
  <forward mode='nat'/>
  <bridge name='virbr10' stp='on' delay='0'/>
  <ip address='10.77.0.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.77.0.100' end='10.77.0.199'/>
    </dhcp>
  </ip>
</network>
```

**持久网络**先定义后启动，并按需设置宿主机开机自启：

```bash
virsh net-define lab-nat.xml
virsh net-start lab-nat
virsh net-autostart lab-nat
virsh net-list --all
virsh net-dumpxml lab-nat
```

**临时网络**则用 `virsh net-create lab-nat.xml` 一步启动，不生成持久定义；停止后需要重新创建。它与 `net-define` 是两种选择，不应对同名网络连续执行。若当前虚拟机需要接入新网，用 `virsh edit <虚拟机名>` 在关机状态下把接口的 `<source network='default'/>` 改为 `<source network='lab-nat'/>`，启动后核对 DHCP 租约、来宾 IP、DNS 和上游访问。

停止与删除网络之前，先用 `virsh domiflist <虚拟机名>` 查出依赖它的来宾。`virsh net-destroy lab-nat` 仅停用网络；`virsh net-undefine lab-nat` 删除持久定义。不要把原课程中删除 `default` 网络的演练直接用于仍承载业务的宿主机；运行中的来宾可能仍显示网卡，但已失去相应的网络路径。

## 4.3 宿主机桥接：把来宾接入上游 LAN

桥接与上述 `virbr*` NAT 网络不同：物理网卡成为桥 `br0` 的端口，宿主机的 IP 和默认路由通常配置在 `br0` 上，来宾的虚拟网卡也连接 `br0`。上游交换机端口、Wi-Fi 或云平台 vNIC 可能限制多个 MAC 地址，创建桥之前必须确认可行。

![桥接网络的原课程示意图]({{ '/subjects/KVM/assets/p097-img01.webp' | relative_url }})

### 迁移前的检查与回滚准备

在远程 SSH 会话中直接清空物理网卡地址，会立刻断开连接。应先准备带外控制台或宿主机本地终端，记录当前连接名称、IP、网关、DNS 与路由，并设置可恢复的维护窗口。以下命令只用于**查看**，不会迁移网络：

```bash
nmcli connection show
nmcli device status
ip -br addr
ip route
resolvectl status
```

若使用 NetworkManager，可按当前发行版文档创建桥连接和物理端口连接。下面使用占位符说明需要配置哪些字段，不能把示例 IP、接口名原样复制到真实主机：

```bash
nmcli connection add type bridge ifname br0 con-name br0
nmcli connection modify br0 ipv4.method manual \
  ipv4.addresses <宿主机地址/前缀> \
  ipv4.gateway <上游网关> ipv4.dns <DNS 地址>
nmcli connection add type ethernet ifname <物理网卡> \
  con-name br0-port master br0
```

真正切换时，应在带外控制台上协调停用旧物理网卡连接、启用 `br0` 和 `br0-port`；不要把旧实验中基于 `brctl`、`ifconfig`、临时 `ip route` 的脚本当成持久配置。该脚本在清空物理网卡地址后没有可靠回滚，连接恢复的截图只是一次实验结果，不是对其他环境的保证。

切换后逐项验证：

```bash
nmcli connection show --active
ip -br addr show br0
bridge link
ip route
ping -c 1 <上游网关>
```

预期是宿主机地址位于 `br0`，物理网卡作为端口出现在 `bridge link`，默认路由仍指向**上游网关地址**。若任何检查失败，先通过带外控制台恢复旧连接，再排查 VLAN、上游多 MAC 限制、DNS 和防火墙。不要在失联的 SSH 会话中盲目重试。

### 把虚拟机切换到桥

先导出原虚拟机 XML 并正常关机，然后用 `virsh edit` 修改目标接口。只改变接口类型和来源，保留原来的 MAC、型号和其他设备配置；下列仅是接口片段，不是完整域定义：

```xml
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
```

启动后检查宿主机 `virsh domiflist <虚拟机名>` 与 `bridge link`，再在来宾内检查 IP、默认路由和 DNS。桥接本身不提供 DHCP；来宾要从上游 DHCP 获取地址，或配置上游网段内不冲突的静态地址。旧课程中来宾获得 `192.0.2.x` 地址，只代表其实验 LAN 有相应 DHCP 服务。

![来宾接入桥接网络的原课程示意图]({{ '/subjects/KVM/assets/p106-img01.webp' | relative_url }})

若从桥接退回 NAT，先在关机状态下把接口改回 `<interface type='network'><source network='default'/></interface>`，再启动并检查新的租约；不要仅修改来宾 IP 而忘记恢复 libvirt 网络来源。

### 常见故障的定位顺序

1. **来宾没有地址：** 检查接口是否接到目标网络、DHCP 来自何处、上游是否允许来宾 MAC。
2. **有地址却无法访问上游：** 检查宿主桥端口、VLAN、默认路由与防火墙，再看来宾路由。
3. **能访问 IP 却不能解析域名：** 检查来宾 DNS 和对应网络的 DHCP 配置；不要把它归因于 KVM CPU 虚拟化。
4. **libvirt 报 SELinux 驱动错误：** 核对宿主机 libvirt/SELinux 安装与日志，不要直接删除 `<seclabel>` 绕过预期隔离策略。

网络改动的验证结果应包括宿主机自身连接、来宾与同网段节点通信、DNS 和业务端口，而不仅是一次 `ping` 成功。

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/KVM/03-storage-management.html' | relative_url }}">← 上一章：存储管理</a>
  <a href="{{ '/subjects/KVM/' | relative_url }}">返回 KVM 目录</a>
  <a href="{{ '/subjects/KVM/05-image-management.html' | relative_url }}">下一章：镜像管理 →</a>
</nav>
