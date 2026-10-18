---
layout: default
title: "JumpServer 堡垒机 · 会话管理"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回JumpServer 堡垒机目录]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 16 会话管理
### 3.6 会话管理

会话管理可以实现查看当前在线的会话命令记录、历史会话过去的执行过的命令,也可以强制将用户踢出

![JumpServer 堡垒机第 84 页插图](assets/img-3f3f7b77bccb8e48.jpeg)

### 查看在线会话

![JumpServer 堡垒机第 84 页插图](assets/img-dc2a45e85629c21e.png)

![JumpServer 堡垒机第 85 页插图](assets/img-75e2526523de1fa7.png)

### 查看历史会话

### 在线回放

![JumpServer 堡垒机第 85 页插图](assets/img-928864d109062c4b.png)

![JumpServer 堡垒机第 86 页插图](assets/img-7748d6294d666a5d.png)

### 离线查看录像

可以将历史会话过程下载再播放,但需要下载相关的播放器

注意：JumpServer-v2.19.1版的录像无法打开

<https://github.com/jumpserver/VideoPlayer/releases>

![JumpServer 堡垒机第 86 页插图](assets/img-132668c25f921df1.png)

![JumpServer 堡垒机第 87 页插图](assets/img-e68881708511ea52.png)

![JumpServer 堡垒机第 87 页插图](assets/img-4e8ccd3a8821d021.png)

![JumpServer 堡垒机第 87 页插图](assets/img-15e5fc1f539982c7.png)

![JumpServer 堡垒机第 88 页插图](assets/img-34f20b7f427eec87.png)

![JumpServer 堡垒机第 88 页插图](assets/img-6f0d99776cc2db88.png)

### 查看命令历史

![JumpServer 堡垒机第 89 页插图](assets/img-b89df4b77d1c16b9.png)

### 终端管理

可以在线监控用户正在进行的操作过程,甚至可以强制中断用户的连接,将其踢出会话

![JumpServer 堡垒机第 89 页插图](assets/img-8bd8453d7b54aace.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/15-database-authorization.html' | relative_url }}">← Previous: Database Authorization</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">Back to JumpServer Bastion Host Index</a>
  <a href="{{ '/subjects/JumpServer/17-command-filters.html' | relative_url }}">Next: Command Filters →</a>
</nav>
