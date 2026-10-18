---
layout: default
title: "JumpServer 堡垒机 · 授权用户使用资产"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 14 授权用户使用资产

前两章分别建立了人员、用户组、资产和资产账号。现在要把它们通过授权规则关联起来：**谁**可以在**何时**以**哪个资产账号**访问**哪些资产**。授权不是创建资产账号的同义词。

![JumpServer 堡垒机第 69 页插图](assets/img-c9131b169b45885f.webp)

### 创建资产授权规则

在授权规则中选择用户或组、资产或节点、允许使用的资产账号，并按需要限定有效时间与动作。先对一台测试资产授予最小范围，验证后再批量扩大。某些版本可在授权或账号推送流程中创建目标主机账号，但必须查看任务结果；如果目标主机已有账号，避免误以为规则会替它重新创建。

SSH 用于终端连接；SFTP 用于文件传输，应仅在业务需要且目标资产支持时开放。下图依次展示较新版本的规则界面及选择过程。

![JumpServer 堡垒机第 69 页插图](assets/img-a996e4cb611bd57f.webp)

![JumpServer 堡垒机第 70 页插图](assets/img-a62d25f56b64d45f.webp)

![JumpServer 堡垒机第 70 页插图](assets/img-3f565a6368257e0b.webp)

以下是旧版界面，操作概念相同，但菜单与字段位置不同。不要把两套截图的点击顺序混用。

![JumpServer 堡垒机第 71 页插图](assets/img-6eb0f4fdae7272ef.webp)

![JumpServer 堡垒机第 71 页插图](assets/img-a9aaea6624cd4604.webp)

![JumpServer 堡垒机第 72 页插图](assets/img-a5e468933b2011c2.webp)

![JumpServer 堡垒机第 72 页插图](assets/img-b4c665f5b19273f8.webp)

![JumpServer 堡垒机第 72 页插图](assets/img-dafad510419e478a.webp)

![JumpServer 堡垒机第 73 页插图](assets/img-b103529f8c6f72c9.webp)

![JumpServer 堡垒机第 73 页插图](assets/img-091fc085d471fb83.webp)

![JumpServer 堡垒机第 73 页插图](assets/img-3121960469f05224.webp)

如需不同环境或不同角色的权限，分别建立规则并检查重叠范围。例如开发组可访问开发环境，并不意味着应通过另一条节点规则意外获得生产权限。

![JumpServer 堡垒机第 74 页插图](assets/img-a35c47994eab11a4.webp)

![JumpServer 堡垒机第 74 页插图](assets/img-750e25c603fed1c9.webp)

### 测试登录访问后端服务器

![JumpServer 堡垒机第 75 页插图](assets/img-5e3779e1c221ef9f.webp)

![JumpServer 堡垒机第 75 页插图](assets/img-4fe85db009a7f1d0.webp)

用普通测试用户登录，确认只看到预期资产。连接后执行只读测试命令，检查会话归属、使用的资产账号及审计记录；不要只以“终端打开了”作为验收。

![JumpServer 堡垒机第 75 页插图](assets/img-97c72c2321b7ce5c.webp)

原截图中的 Web 终端入口可能随版本调整，核心验收仍是授权范围和会话记录是否正确。

![JumpServer 堡垒机第 76 页插图](assets/img-ecd1b67711046233.webp)

### 测试上传和下载文件

文件传输可通过当前版本支持的 Web 界面或 SFTP 客户端进行。使用 SFTP 客户端时，应确认连接的是 JumpServer 的 SFTP 接入端口，而不是目标主机的 SSH 端口，并用非敏感测试文件验证上传、下载和审计记录。

![JumpServer 堡垒机第 76 页插图](assets/img-7b73cace09b30462.webp)

![JumpServer 堡垒机第 76 页插图](assets/img-3613403a5712a6ea.webp)

![JumpServer 堡垒机第 77 页插图](assets/img-27b2f6b25c5f149b.webp)

![JumpServer 堡垒机第 77 页插图](assets/img-fb680e27ba5df3b0.webp)

![JumpServer 堡垒机第 78 页插图](assets/img-6b9c0a882b8b21e5.webp)

![JumpServer 堡垒机第 78 页插图](assets/img-bdef2bf8e2d8e501.webp)

### ssh连接JumpServer

除 Web 终端外，也可用 SSH 客户端连接 JumpServer 的接入端口。下面的用户名是**平台登录用户**，后续还要在菜单中选择获授权的资产：

```text
ssh -p 2222 jumpserver_user@jumpserver
```

![JumpServer 堡垒机第 79 页插图](assets/img-61e7e2e686031c9f.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/13-creating-assets-and-linking-privileged-and-regular-users.html' | relative_url }}">← 上一篇：创建资产与关联账号</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">返回 JumpServer 专题目录</a>
  <a href="{{ '/subjects/JumpServer/15-database-authorization.html' | relative_url }}">下一篇：数据库授权 →</a>
</nav>
