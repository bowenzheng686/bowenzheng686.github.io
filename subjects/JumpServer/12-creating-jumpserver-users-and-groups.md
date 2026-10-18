---
layout: default
title: "JumpServer 堡垒机 · 创建JumpServer用户和组"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 12 创建 JumpServer 用户和组

本篇创建的是**登录 JumpServer 的人员身份**及用户组，不是目标 Linux／Windows 主机上的账号。资产账号与两者的关联将在下一篇处理。

原资料区分系统管理员、普通用户和系统审计员。管理员维护平台配置与授权，普通用户在获授权范围内访问资产，审计员查看会话与操作记录。具体角色名称和权限边界应以当前版本为准；新增人员时优先授予普通用户角色。

### 创建用户

![JumpServer 堡垒机第 50 页插图](assets/img-5f1446e0576a97c5.webp)

填写用户名、姓名和可接收邀请的邮箱。邮箱通常要唯一，且应属于该人员；创建后确认邀请或重置邮件能送达。

![JumpServer 堡垒机第 51 页插图](assets/img-7f9f160f4c79602b.webp)

按相同步骤创建第二位测试用户，便于之后验证组授权是否按预期生效；不要共用一个登录账号。

![JumpServer 堡垒机第 52 页插图](assets/img-6a41bbf7ea710ca2.webp)

![JumpServer 堡垒机第 52 页插图](assets/img-fa39ad668acc75ab.webp)

### 创建组并将用户加入组中

![JumpServer 堡垒机第 53 页插图](assets/img-ac9fb39d1a099ddd.webp)

创建 development 组并添加相关用户。组是批量授权的对象，后续把组与资产关联时，所有成员都可能继承访问权限。

![JumpServer 堡垒机第 53 页插图](assets/img-b637f015cd0237fd.webp)

另建 test 组，让测试人员与开发人员的授权边界保持清晰。若一人同时属于两个组，应复核其有效权限是否超出岗位需要。

![JumpServer 堡垒机第 53 页插图](assets/img-914b082a70badf4a.webp)

在组列表核对成员和名称，再进行资产授权；创建组本身不会让用户自动拥有资产访问权。

![JumpServer 堡垒机第 54 页插图](assets/img-0266b9a879f844b0.webp)

### 使用新用户登录

![JumpServer 堡垒机第 54 页插图](assets/img-dc6c93399144e611.webp)

新用户首次登录后可完善个人信息并设置独立密码。用普通用户身份查看可见资产，确认没有意外继承管理员权限。

![JumpServer 堡垒机第 55 页插图](assets/img-999817425077a599.webp)

![JumpServer 堡垒机第 55 页插图](assets/img-d319ce7fbdb28ff5.webp)

### 禁用和启用用户

当人员暂时不应登录时，可禁用其平台账号。禁用后应验证新登录被拒绝，并按当前版本行为检查已有会话是否需要单独终止。

![JumpServer 堡垒机第 56 页插图](assets/img-5cd4b31f2f7e406a.webp)

![JumpServer 堡垒机第 56 页插图](assets/img-70dfca0ec5985d3e.webp)

重新启用前，先核对其所属组和资产授权仍然适用；重新启用不应默认恢复已过期的临时权限。

![JumpServer 堡垒机第 56 页插图](assets/img-86c4d190caae37d3.webp)

![JumpServer 堡垒机第 56 页插图](assets/img-aa9d187cbd6f77f8.webp)

### 启用用户多因子认证功能

多因素认证（MFA）在密码之外增加第二个验证因素，例如验证器应用生成的动态码。启用前应准备设备丢失时的恢复流程；只要求输入两次相同类型的密码并不构成真正的多因素认证。

### 开启MFA

可在用户设置中为指定人员开启 MFA；先用测试账号绑定，再推广到管理员和其他人员。不要在截图或文档中公开绑定二维码或恢复码。

![JumpServer 堡垒机第 57 页插图](assets/img-5a48b93bd339777f.webp)

![JumpServer 堡垒机第 57 页插图](assets/img-b2b71df2c6351a12.webp)

### 绑定手机APP

![JumpServer 堡垒机第 58 页插图](assets/img-3d8cb8b2d2d3a519.webp)

![JumpServer 堡垒机第 58 页插图](assets/img-9289cf52ee24e03d.webp)

在受信任的应用商店安装兼容的验证器，扫描当前用户的绑定二维码并用动态码确认。绑定完成后，应保存必要的恢复信息，而非只依赖一台手机。

![JumpServer 堡垒机第 58 页插图](assets/img-1cb73282068baa38.webp)

![JumpServer 堡垒机第 59 页插图](assets/img-721e94ee3b985de8.webp)

### 重新登录验证

![JumpServer 堡垒机第 59 页插图](assets/img-43bbab88aef08b1a.webp)

![JumpServer 堡垒机第 59 页插图](assets/img-bc9539834a2b3446.webp)

![JumpServer 堡垒机第 60 页插图](assets/img-f8c380af78aca92d.webp)

### 创建系统审计员

系统审计员负责在授权范围内查看会话、命令及录像记录，不应因此自动获得资产登录权限。创建后使用该账号登录，验证它能看到所需审计资料，同时不能修改平台配置。

![JumpServer 堡垒机第 60 页插图](assets/img-3ade01b3d46b2fff.webp)

最后使用审计员账号重新登录，按下图核对审计页面是否可见，以及普通资产操作是否仍受授权限制。

![JumpServer 堡垒机第 61 页插图](assets/img-c47894b1795022e3.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/11-initial-login-and-configuration.html' | relative_url }}">← 上一篇：首次登录与配置</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">返回 JumpServer 专题目录</a>
  <a href="{{ '/subjects/JumpServer/13-creating-assets-and-linking-privileged-and-regular-users.html' | relative_url }}">下一篇：创建资产与关联账号 →</a>
</nav>
