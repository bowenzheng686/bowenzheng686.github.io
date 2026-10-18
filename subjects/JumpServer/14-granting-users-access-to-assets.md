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
### 3.4 授权用户使用资产

![JumpServer 堡垒机第 69 页插图](assets/img-c9131b169b45885f.png)

### 创建资产授权规则

通过资产授权规则, 为JumpServer用户分配可以访问的资产及使用的系统用户的普通用户

新版

执行完成后，自动在后端服务器生成系统用户的普通用户

注意:需要指定SSH和SFTP协议(用于上传下载文件)

![JumpServer 堡垒机第 69 页插图](assets/img-a996e4cb611bd57f.png)

![JumpServer 堡垒机第 70 页插图](assets/img-a62d25f56b64d45f.png)

![JumpServer 堡垒机第 70 页插图](assets/img-3f565a6368257e0b.png)

旧版

![JumpServer 堡垒机第 71 页插图](assets/img-6eb0f4fdae7272ef.png)

![JumpServer 堡垒机第 71 页插图](assets/img-a9aaea6624cd4604.png)

![JumpServer 堡垒机第 72 页插图](assets/img-a5e468933b2011c2.png)

![JumpServer 堡垒机第 72 页插图](assets/img-b4c665f5b19273f8.png)

![JumpServer 堡垒机第 72 页插图](assets/img-dafad510419e478a.png)

![JumpServer 堡垒机第 73 页插图](assets/img-b103529f8c6f72c9.png)

![JumpServer 堡垒机第 73 页插图](assets/img-091fc085d471fb83.png)

![JumpServer 堡垒机第 73 页插图](assets/img-3121960469f05224.png)

同样再创建授权规则

![JumpServer 堡垒机第 74 页插图](assets/img-a35c47994eab11a4.png)

![JumpServer 堡垒机第 74 页插图](assets/img-750e25c603fed1c9.png)

### 测试登录访问后端服务器

![JumpServer 堡垒机第 75 页插图](assets/img-5e3779e1c221ef9f.png)

![JumpServer 堡垒机第 75 页插图](assets/img-4fe85db009a7f1d0.png)

选中主机后,输入命令,再执行

![JumpServer 堡垒机第 75 页插图](assets/img-97c72c2321b7ce5c.png)

点右上角的web终端,可以打开终端界面

![JumpServer 堡垒机第 76 页插图](assets/img-ecd1b67711046233.png)

### 测试上传和下载文件

可以通过web方式或者通过filezilla等工具直接连接jumpserver的2222端口都可以实现文件的上传下载

![JumpServer 堡垒机第 76 页插图](assets/img-7b73cace09b30462.png)

![JumpServer 堡垒机第 76 页插图](assets/img-3613403a5712a6ea.png)

![JumpServer 堡垒机第 77 页插图](assets/img-27b2f6b25c5f149b.png)

![JumpServer 堡垒机第 77 页插图](assets/img-fb680e27ba5df3b0.png)

![JumpServer 堡垒机第 78 页插图](assets/img-6b9c0a882b8b21e5.png)

![JumpServer 堡垒机第 78 页插图](assets/img-bdef2bf8e2d8e501.png)

### ssh连接JumpServer

JumpServer 还支持用户通过ssh连接其2222/tcp端口进行访问

连接方式:

```text
ssh -p 2222 jumpserver_user@jumpserver
```

![JumpServer 堡垒机第 79 页插图](assets/img-61e7e2e686031c9f.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/13-creating-assets-and-linking-privileged-and-regular-users.html' | relative_url }}">← Previous: Creating Assets and Linking Privileged and Regular Users</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">Back to JumpServer Bastion Host Index</a>
  <a href="{{ '/subjects/JumpServer/15-database-authorization.html' | relative_url }}">Next: Database Authorization →</a>
</nav>
