---
layout: default
title: "JumpServer 堡垒机 · 创建JumpServer用户和组"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 12 创建JumpServer用户和组
### 3.2 创建JumpServer用户和组

JumpServer 支持三种登录用户角色

系统管理员普通用户系统审计员

### 创建用户

![JumpServer 堡垒机第 50 页插图](assets/img-5f1446e0576a97c5.png)

填写用户信息,注意: 邮箱地址不能重复

![JumpServer 堡垒机第 51 页插图](assets/img-7f9f160f4c79602b.png)

相同方法再创建xiaoming用户

![JumpServer 堡垒机第 52 页插图](assets/img-6a41bbf7ea710ca2.png)

![JumpServer 堡垒机第 52 页插图](assets/img-fa39ad668acc75ab.png)

### 创建组并将用户加入组中

![JumpServer 堡垒机第 53 页插图](assets/img-ac9fb39d1a099ddd.png)

创建development组,并将前面创建的用户加入组中

![JumpServer 堡垒机第 53 页插图](assets/img-b637f015cd0237fd.png)

创建test组,将入用户

![JumpServer 堡垒机第 53 页插图](assets/img-914b082a70badf4a.png)

查看创建的组

![JumpServer 堡垒机第 54 页插图](assets/img-0266b9a879f844b0.png)

### 使用新用户登录

![JumpServer 堡垒机第 54 页插图](assets/img-dc6c93399144e611.png)

首次登录完善个人信息

![JumpServer 堡垒机第 55 页插图](assets/img-999817425077a599.png)

![JumpServer 堡垒机第 55 页插图](assets/img-d319ce7fbdb28ff5.png)

### 禁用和启用用户

禁用用户

![JumpServer 堡垒机第 56 页插图](assets/img-5cd4b31f2f7e406a.png)

![JumpServer 堡垒机第 56 页插图](assets/img-70dfca0ec5985d3e.png)

启用用户

![JumpServer 堡垒机第 56 页插图](assets/img-86c4d190caae37d3.png)

![JumpServer 堡垒机第 56 页插图](assets/img-aa9d187cbd6f77f8.png)

### 启用用户多因子认证功能

多因子认证Multi-Factor Authentication (MFA) 是一种简单有效的最佳安全实践方法，用户要通过两种以上的认证机制之后，才能得到授权，使用计算机资源

JumpServer 启用 MFA 后，用户登录网站时，系统将要求输入用户名和密码（第一安全要素），然后要求输入来自其 MFA 设备的动态验证码（第二安全要素），双因素的安全认证将为您的账户提供更高的安全保护

### 开启MFA

在用户列表中,对指定用户更新配置

![JumpServer 堡垒机第 57 页插图](assets/img-5a48b93bd339777f.png)

![JumpServer 堡垒机第 57 页插图](assets/img-b2b71df2c6351a12.png)

### 绑定手机APP

![JumpServer 堡垒机第 58 页插图](assets/img-3d8cb8b2d2d3a519.png)

![JumpServer 堡垒机第 58 页插图](assets/img-9289cf52ee24e03d.png)

按下图下载APP并安装

![JumpServer 堡垒机第 58 页插图](assets/img-1cb73282068baa38.png)

![JumpServer 堡垒机第 59 页插图](assets/img-721e94ee3b985de8.png)

### 重新登录验证

![JumpServer 堡垒机第 59 页插图](assets/img-43bbab88aef08b1a.png)

![JumpServer 堡垒机第 59 页插图](assets/img-bc9539834a2b3446.png)

![JumpServer 堡垒机第 60 页插图](assets/img-f8c380af78aca92d.png)

### 创建系统审计员

系统审计员即查看录像带的人(M42期宽宽语录)

![JumpServer 堡垒机第 60 页插图](assets/img-3ade01b3d46b2fff.png)

使用审计员用户登录

![JumpServer 堡垒机第 61 页插图](assets/img-c47894b1795022e3.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/11-initial-login-and-configuration.html' | relative_url }}">← Previous: Initial Login and Configuration</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">Back to JumpServer Bastion Host Index</a>
  <a href="{{ '/subjects/JumpServer/13-creating-assets-and-linking-privileged-and-regular-users.html' | relative_url }}">Next: Creating Assets and Linking Privileged and Regular Users →</a>
</nav>
