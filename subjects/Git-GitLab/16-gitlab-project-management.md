---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 项目管理"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 16 GitLab 项目管理

本章先创建项目，再配置成员权限，最后通过 HTTPS 或 SSH 验证克隆、提交和合并请求。不同版本的页面布局不同，以项目的实际命名空间和默认分支为准。

### 创建项目

### 新建项目

GitLab 项目属于某个命名空间：可以是个人，也可以是组。一个项目通常对应一个代码仓库及其协作设置，是否按服务或模块拆分取决于团队边界与发布方式。

若准备推送已有本地仓库，可创建**空项目**以避免默认 README 产生额外初始提交；若从零开始，直接初始化 README 也可以，但后续推送须先整合远程历史。

![Git 与 GitLab 版本管理第 123 页插图](assets/img-81cd5d119cd7e59e.webp)

新版界面

![Git 与 GitLab 版本管理第 123 页插图](assets/img-2bfb657d07b59dce.webp)

创建项目,指定项目属于组,并选择不进行初始化项目仓库

![Git 与 GitLab 版本管理第 123 页插图](assets/img-b1de0ef7fc45f1a2.webp)

![Git 与 GitLab 版本管理第 124 页插图](assets/img-3753ea26c68fbda0.webp)

命令行指引

您还可以按照以下说明从计算机中上传现有文件。

Git 全局设置

```text
git config --global user.name "Administrator"
git config --global user.email "admin@example.com"
```

创建一个新仓库

```text
git clone http://gitlab.bowen.org/dev/meta.git
cd meta
git switch -c main  # 仅当空仓库克隆后尚未处于 main 时执行
touch README.md
git add README.md
git commit -m "add README"
git push -u origin main
```

推送现有文件夹

```text
cd existing_folder
git init --initial-branch=main
git remote add origin http://gitlab.bowen.org/dev/meta.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

推送现有的 Git 仓库

```text
cd existing_repo
git remote rename origin old-origin
git remote add origin http://gitlab.bowen.org/dev/meta.git
git push -u origin --all
git push -u origin --tags
```

旧版界面

![Git 与 GitLab 版本管理第 125 页插图](assets/img-1827db2fc43e3d2e.webp)

使用管理员创建项目：

![Git 与 GitLab 版本管理第 125 页插图](assets/img-f471758abb22e520.webp)

创建后的项目效果：

![Git 与 GitLab 版本管理第 126 页插图](assets/img-bf0595dc531c68ab.webp)

### 导入项目

新版需要开启导入旧项目到Gitlab功能才支持导入

搜索--管理中心--设置-- 通用--导入和导出设置

![Git 与 GitLab 版本管理第 126 页插图](assets/img-b2bf90d02be422c2.webp)

![Git 与 GitLab 版本管理第 126 页插图](assets/img-161a6fc896d2c2af.webp)

![Git 与 GitLab 版本管理第 127 页插图](assets/img-e7d61b62ae64c06a.webp)

### 将用户添加到组或项目并指定角色

将用户添加到组或项目中,并指定不同的角色,可以获取不同的权限

角色和权限官方帮助

<https://docs.gitlab.com/ce/user/permissions.html>

![Git 与 GitLab 版本管理第 128 页插图](assets/img-83c4038dcceb89bd.webp)

常见角色按权限递增，实际能力还受 GitLab 版本、项目设置和保护分支规则影响：

| 角色 | 常见能力与边界 |
| --- | --- |
| Guest | 参与部分议题和评论；对私有仓库源码的访问受具体权限配置限制。 |
| Reporter | 读取代码和结果，通常不能推送。 |
| Developer | 在允许的分支推送并创建合并请求；受保护分支可能禁止直接推送。 |
| Maintainer | 管理项目设置、成员及发布规则，权限高于普通开发者。 |
| Owner | 主要是组级最高权限，涉及组成员与组设置；不是每个项目都单独有 Owner。 |

在组中添加用户并指定角色

![Git 与 GitLab 版本管理第 129 页插图](assets/img-b3eb7595274ad620.webp)

Developer 通常可以推送非保护分支；对受保护的 `main`/`master` 是否能推送，由具体保护规则决定。不要为了让开发者推送功能分支就授予 Maintainer 权限。

![Git 与 GitLab 版本管理第 129 页插图](assets/img-c66db547bb0bf0f7.webp)

![Git 与 GitLab 版本管理第 129 页插图](assets/img-2c6257f23a86ff20.webp)

或者在项目中添加用户进行角色指定，此方式后续管理不太方便，不建议加用户到项目，建议将用户加入组中

![Git 与 GitLab 版本管理第 130 页插图](assets/img-5df5577942ccb700.webp)

旧版界面

![Git 与 GitLab 版本管理第 130 页插图](assets/img-ad9bac60abf3d149.webp)

![Git 与 GitLab 版本管理第 131 页插图](assets/img-45a595d82e5a902a.webp)

### 使用项目

### 在项目中新建一个测试页面

用上面创建的用户bowen登录，找到项目界面,在项目中新建文件

![Git 与 GitLab 版本管理第 131 页插图](assets/img-51362ca8f4062ba0.webp)

![Git 与 GitLab 版本管理第 132 页插图](assets/img-9c440a3a4e2f8e93.webp)

旧版界面

![Git 与 GitLab 版本管理第 132 页插图](assets/img-cdd375deb4200cf7.webp)

填写 `README.md` 文件内容，说明项目用途、运行方式和协作约定。

![Git 与 GitLab 版本管理第 132 页插图](assets/img-242497ba479e5ce5.webp)

新建项目文件

![Git 与 GitLab 版本管理第 133 页插图](assets/img-de85574f6f94c8d6.webp)

![Git 与 GitLab 版本管理第 133 页插图](assets/img-5eca40737d67c9c9.webp)

### 在linux客户端测试clone和提交项目

![Git 与 GitLab 版本管理第 133 页插图](assets/img-945309aaa0cf9fe0.webp)

命令行指引

您还可以按照以下说明从计算机中上传现有文件。 Git 全局设置

```text
git config --global user.name "Administrator"
git config --global user.email "admin@example.com"
```

创建一个新仓库

```text
git clone http://gitlab.bowen.org/dev/meta.git
cd meta
git switch -c main
touch README.md
git add README.md
git commit -m "add README"
git push -u origin main
```

推送现有文件夹

```text
cd existing_folder
git init --initial-branch=main
git remote add origin http://gitlab.bowen.org/dev/meta.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

推送现有的 Git 仓库

```text
cd existing_repo
git remote rename origin old-origin
git remote add origin http://gitlab.bowen.org/dev/meta.git
git push -u origin --all
git push -u origin --tags
```

根据不同的情况,在另一台主机上执行下面操作

```bash
[root@ubuntu1804 ~]#cd /data
[root@ubuntu1804 data]#ls
lost+found
[root@ubuntu1804 data]#git clone https://gitlab.example.com/testgroup/testproject.git
Cloning into 'testproject'...
Username for 'http://10.0.0.100': bowen
Password for 'http://bowen@10.0.0.100':
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 6 (delta 0), reused 0 (delta 0)
Unpacking objects: 100% (6/6), done.
[root@ubuntu1804 data]#ls -a
.  ..  lost+found  testproject
[root@ubuntu1804 data]#tree testproject/
testproject/
├── index.html
└── README.md
0 directories, 2 files
#设置用户名和邮箱
[root@ubuntu1804 data]#git config --global user.name "bowenxiaochun"
[root@ubuntu1804 data]#git config --global user.email  "root@bowenxiaochun.com"
[root@ubuntu1804 data]#cat ~/.gitconfig
[user]
name = bowenxiaochun
email = root@bowenxiaochun.com
[root@ubuntu1804 data]#vim testproject/
#修改项目文件
[root@ubuntu1804 data]#vim testproject/index.html
[root@ubuntu1804 data]#cat testproject/index.html
<h1>index.html v1 </h1>
<h1>index.html v2 </h1>
[root@ubuntu1804 data]#cd testproject/
[root@ubuntu1804 testproject]#git add .
[root@ubuntu1804 testproject]#git commit -m "v2"
[master 44dbd92] v2
1 file changed, 2 insertions(+), 1 deletion(-)
```

```bash
[root@ubuntu1804 testproject]#git push
Username for 'http://10.0.0.100': bowen
Password for 'http://bowen@10.0.0.100':
Counting objects: 3, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 296 bytes | 296.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0)
To http://10.0.0.100/testgroup/testproject.git
928e057..44dbd92  master -> master
```

### 在 Windows 安装 git 客户端测试clone和提交项目

官网下载链接:

<https://git-scm.com/download/win>

![Git 与 GitLab 版本管理第 136 页插图](assets/img-013051ffec9909e1.webp)

![Git 与 GitLab 版本管理第 136 页插图](assets/img-62fc1105c08c9fe4.webp)

![Git 与 GitLab 版本管理第 136 页插图](assets/img-5a12e56b7528b661.webp)

### Web端验证数据

![Git 与 GitLab 版本管理第 137 页插图](assets/img-a9e9c618635158b1.webp)

![Git 与 GitLab 版本管理第 137 页插图](assets/img-fe32f485a66437b1.webp)

### 实现 ssh 基于key验证的 git 访问

```bash
[root@centos8 ~]#ssh-keygen -t ed25519 -C "you@example.com"
[root@centos8 ~]#cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAA... you@example.com
```

![Git 与 GitLab 版本管理第 138 页插图](assets/img-576db9bcedf76171.webp)

![Git 与 GitLab 版本管理第 138 页插图](assets/img-9b85acac7bc2ee95.webp)

```bash
[root@centos8 ~]#cd /opt
[root@centos8 opt]#ls
[root@centos8 opt]#git clone git@10.0.0.100:testgroup/testproject.git
Cloning into 'testproject'...
The authenticity of host '10.0.0.100 (10.0.0.100)' can't be established.
ECDSA key fingerprint is SHA256:SCZC/wgETlcNAvmd1gaG8Tvb4sR53VzbaX1MHKi9GLY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.0.0.100' (ECDSA) to the list of known hosts.
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 6 (delta 0), reused 0 (delta 0), pack-reused 3
Receiving objects: 100% (6/6), done.
```

### 保护分支

默认master 分支被保护,开发者角色无法对被保护的分支提交代码

也可以将其它分支进行保护,防止指定分支被破环

![Git 与 GitLab 版本管理第 139 页插图](assets/img-a7422ac9511a27ee.webp)

### 合并分支

由于普通开发者无法直接提交代码至master分支

可以先创建其它分支如dev,再提交代码到dev分支

接下来申请将dev 分支合并至master分支

管理者收到请求,经过审核没有问题进行批准合并

最终实现 master 代码的更新

![Git 与 GitLab 版本管理第 140 页插图](assets/img-e7d2662ebb302b72.webp)

![Git 与 GitLab 版本管理第 140 页插图](assets/img-4fc1f1d50cb2c9ea.webp)

![Git 与 GitLab 版本管理第 141 页插图](assets/img-5c272788cc609562.webp)

![Git 与 GitLab 版本管理第 142 页插图](assets/img-daa75e8dee41fcc6.webp)

### Gitlab 协议和格式

GitLab 可以支持http/https或者ssh协议上传和下载文件

http[s] 协议

```text
#格式
http[s]://host[:Port]/group/project.git
#示例
http://gitlab.bowen.org/testgroup/testproject.git
```

ssh 协议

```text
#格式
git@host:group/project.git
#如果使用非标准端口,使用下面格式
ssh://git@host:port/group/project.git
#或者使用下面配置文件实现
~/.ssh/config
Host gitlab.bowen.org
Port 30022
Host *
Port 22
#示例
git@gitlab.bowen.org:testgroup/testproject.git
ssh://git@gitlab.bowen.org:30022/testgroup/testproject.git
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/15-gitlab-user-and-group-management.html' | relative_url }}">← 上一篇：GitLab 用户和组管理</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/17-gitlab-data-backup-and-recovery.html' | relative_url }}">下一篇：GitLab 数据备份与恢复 →</a>
</nav>
