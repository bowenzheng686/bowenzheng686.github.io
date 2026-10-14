---
layout: default
title: KVM 虚拟化
subject_page: true
---

# KVM 虚拟化

从虚拟化基础和 KVM 部署开始，依次学习命令行创建虚拟机、存储、网络、镜像与资源管理，最后理解实现原理和 Windows 虚拟机的部署。原笔记按知识主题拆分为 8 章。公开版保留正文与命令示例，已替换实验密码、主机标识和网络地址，并省略原始截图。

## 基础与部署

<ol>
  <li><a href="{{ '/subjects/KVM/01-virtualization-basics.html' | relative_url }}">虚拟化基础</a>：虚拟化分类、KVM 原理、宿主机环境与部署。</li>
  <li><a href="{{ '/subjects/KVM/02-create-vm-from-cli.html' | relative_url }}">命令创建虚拟机</a>：virt-install、virsh、虚拟机生命周期与克隆。</li>
</ol>

## 核心管理

<ol start="3">
  <li><a href="{{ '/subjects/KVM/03-storage-management.html' | relative_url }}">存储管理</a>：存储池、存储卷和磁盘操作。</li>
  <li><a href="{{ '/subjects/KVM/04-network-management.html' | relative_url }}">网络管理</a>：虚拟网络、网桥与网络配置。</li>
  <li><a href="{{ '/subjects/KVM/05-image-management.html' | relative_url }}">镜像管理</a>：镜像格式与镜像操作。</li>
  <li><a href="{{ '/subjects/KVM/06-resource-management.html' | relative_url }}">资源管理</a>：CPU、内存及相关资源配置。</li>
</ol>

## 原理与拓展

<ol start="7">
  <li><a href="{{ '/subjects/KVM/07-virtualization-principles.html' | relative_url }}">虚拟化原理</a>：CPU、内存、I/O 与网络虚拟化。</li>
  <li><a href="{{ '/subjects/KVM/08-create-windows-vm.html' | relative_url }}">创建 Windows 虚拟机</a>：VirtIO 驱动与安装实践。</li>
</ol>
