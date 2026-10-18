---
layout: default
title: "Git 与 GitLab 版本控制 · Git 安装"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 08 Git 安装

优先使用操作系统包管理器安装 Git，便于获得安全更新；仅在明确需要特定版本时再考虑额外软件源或源码编译。以下终端记录对应旧版系统，版本号只作历史示例。

### Linux 安装 git

<https://git-scm.com/download/linux>

![Git 与 GitLab 版本管理第 41 页插图](assets/img-8cd22be40bbaa9e5.webp)

### 二进制包安装

CentOS和Ubuntu 系统源都带有git版本,可以直接安装

范例: Ubuntu 使系统内置仓库安装 git

```bash
[root@ubuntu2404 ~]#apt update && apt -y install git
[root@ubuntu2404 ~]#git version
git version 2.43.0
```

```bash
[root@ubuntu2204 ~]#apt update && apt -y install git
[root@ubuntu2204 ~]#git version
git version 2.34.1
[root@ubuntu2004 ~]#apt update && apt -y install git
[root@ubuntu2004 ~]#git version
git version 2.25.1
[root@ubuntu1804 ~]#apt update;apt -y install git
[root@ubuntu1804 ~]#git version
git version 2.17.1
```

范例：旧版 Ubuntu 从第三方 PPA 获取较新 Git。PPA 不等于官方仓库，使用前应确认系统版本仍受支持及软件源可信性。

```bash
[root@ubuntu1804 ~]#apt list  git
Listing... Done
git/bionic-security,bionic-updates 1:2.17.1-1ubuntu0.9 amd64 [upgradable from:
1:2.17.1-1ubuntu0.7]
[root@ubuntu1804 ~]#add-apt-repository ppa:git-core/ppa
[root@ubuntu1804 ~]#apt update
[root@ubuntu1804 ~]#apt list git
Listing... Done
git/bionic 1:2.33.0-0ppa1~ubuntu18.04.1 amd64 [upgradable from: 1:2.17.1-
1ubuntu0.7]
N: There are 3 additional versions. Please use the '-a' switch to see them.
[root@ubuntu1804 ~]#apt -y install  git
[root@ubuntu1804 ~]#git version
git version 2.33.0
```

范例: Rocky安装git

```bash
[root@rocky8 ~]#yum -y install git
[root@rocky8 ~]#git version
git version 2.27.0
```

### 源码安装

安装文档

<https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>

![Git 与 GitLab 版本管理第 42 页插图](assets/img-ec840bde0f36eac7.webp)

源码下载

<https://www.kernel.org/pub/software/scm/git>

<https://github.com/git/git/releases>

范例：Ubuntu 编译安装 Git。先安装依赖，以下命令应在取得可信源码并校验版本后执行。

```bash
[root@ubuntu2204 ~]#apt update && apt -y install gcc make dh-autoreconf libcurl4-gnutls-dev libexpat1-dev
[root@ubuntu2204 ~]#git clone https://gitee.com/lbtooth/git.git
[root@ubuntu2204 ~]#cd git
[root@ubuntu2204 git]#make -j "$(nproc)" prefix=/apps/git all
[root@ubuntu2204 git]#make prefix=/apps/git install
[root@ubuntu2204 git]#echo 'PATH=/apps/git/bin/:$PATH' > /etc/profile.d/git.sh
[root@ubuntu2204 git]#. /etc/profile.d/git.sh
[root@ubuntu2204 ~]#git version
git version 2.39.1.388.g2fc9e9ca3c
```

范例: Rocky 8 编译安装git

```bash
[root@rocky8 ~]#yum -y install gcc make openssl-devel curl-devel expat-devel
[root@rocky8 ~]#wget -P /usr/local/src https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.33.0.tar.gz
[root@rocky8 ~]#cd /usr/local/src
[root@rocky8 src]#tar xf git-2.33.0.tar.gz
[root@rocky8 git-2.33.0]#cd git-2.33.0/
[root@rocky8 git-2.33.0]#cat INSTALL
[root@rocky8 git-2.33.0]#make -j "$(nproc)" prefix=/apps/git all
[root@rocky8 git-2.33.0]#make prefix=/apps/git install
[root@rocky8 git-2.33.0]#echo 'export PATH=/apps/git/bin:$PATH' > /etc/profile.d/git.sh
[root@rocky8 git-2.33.0]#. /etc/profile.d/git.sh
[root@rocky8 git-2.33.0]#git version
git version 2.33.0
```

### Windows 安装 git

<https://git-scm.com/downloads>

![Git 与 GitLab 版本管理第 44 页插图](assets/img-9d604d32e50235b2.webp)

![Git 与 GitLab 版本管理第 44 页插图](assets/img-f580c8ba578f70eb.webp)

![Git 与 GitLab 版本管理第 45 页插图](assets/img-3f21453a3b63e2d7.webp)

![Git 与 GitLab 版本管理第 45 页插图](assets/img-62d064e16dea6470.webp)

![Git 与 GitLab 版本管理第 46 页插图](assets/img-5f2c5986b352528d.webp)

![Git 与 GitLab 版本管理第 46 页插图](assets/img-aaa12a719909ce8b.webp)

![Git 与 GitLab 版本管理第 47 页插图](assets/img-686161a33ed0d2fc.webp)

![Git 与 GitLab 版本管理第 47 页插图](assets/img-6a6a8cb663e5af6b.webp)

![Git 与 GitLab 版本管理第 48 页插图](assets/img-50f839fed20b1904.webp)

![Git 与 GitLab 版本管理第 48 页插图](assets/img-0537211e64b09eb6.webp)

![Git 与 GitLab 版本管理第 49 页插图](assets/img-b14e54829a02586e.webp)

![Git 与 GitLab 版本管理第 49 页插图](assets/img-1b70c1d6041a4920.webp)

![Git 与 GitLab 版本管理第 50 页插图](assets/img-6cca07d38090ab93.webp)

![Git 与 GitLab 版本管理第 50 页插图](assets/img-044156045351cd06.webp)

![Git 与 GitLab 版本管理第 51 页插图](assets/img-100539b221de686b.webp)

![Git 与 GitLab 版本管理第 51 页插图](assets/img-a905b6d08a93657e.webp)

![Git 与 GitLab 版本管理第 52 页插图](assets/img-053c5550f2e01731.webp)

![Git 与 GitLab 版本管理第 52 页插图](assets/img-c36a76d28872d306.webp)

注意:

首次提交前配置提交身份：`git config --global user.name "你的姓名"` 和 `git config --global user.email "you@example.com"`。这用于标识提交作者，不等于远程平台的登录凭据。Windows 上若使用凭据管理器保存了 HTTPS 凭据，凭据失效后再更新；SSH 访问则使用密钥，与该 HTTPS 凭据流程不同。

### Mac 安装 git

<https://git-scm.com/download/mac>

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/07-git-concepts-and-principles.html' | relative_url }}">← 上一篇：Git 相关概念和原理</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/09-git-command-syntax.html' | relative_url }}">下一篇：Git 常用语法 →</a>
</nav>
