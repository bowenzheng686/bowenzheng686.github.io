---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 基本配置"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 14 GitLab 基本配置
### 3.3 GitLab 基本配置

### 首次登录 GitLab Web 界面修改密码

新版gitlab密码初始化官方帮助链接

<https://docs.gitlab.com/omnibus/installation/index.html>

浏览器访问http://gitlab服务器IP/

在新版gitlab中第一次登录的界面发生变化,取消重设密码界面,需要直接输入用户和密码才能登录

默认用户为root，其密码是随机生成

![Git 与 GitLab 版本管理第 107 页插图](assets/img-90a9eb8780a6b293.png)

```bash
#如果没有在配置文件中对密码做初始化设置,可以从以下文件找到初始密码
[root@ubuntu1804 ~]#cat /etc/gitlab/initial_root_password
# WARNING: This value is valid only in the following conditions
#          1. If provided manually (either via `GITLAB_ROOT_PASSWORD` environment
variable or via `gitlab_rails['initial_root_password']` setting in `gitlab.rb`,
it was provided before database was seeded for the first time (usually, the first
reconfigure run).
#          2. Password hasn't been changed manually, either via UI or via command
line.
#
#          If the password shown here doesn't work, you must reset the admin
password following
https://docs.gitlab.com/ee/security/reset_user_password.html#reset-your-root-
password.
Password: t2c31Eqz4035tmrbAJFl/itm8aSkEHu87xGzluzsj/w=
# NOTE: This file will be automatically deleted in the first reconfigure run
after 24 hours.
```

新版登录界面,用root用户和配置文件中指定的密码或以上文件中的初始密码登录

![Git 与 GitLab 版本管理第 108 页插图](assets/img-07d2d68beea4bb3f.png)

新版登录后,也可以再次修改密码,注意:密码至少8位

![Git 与 GitLab 版本管理第 108 页插图](assets/img-95918d76fefab75f.png)

使用用户 root 和上面设置的密码登录

新版界面

![Git 与 GitLab 版本管理第 109 页插图](assets/img-3573308b805039f8.png)

新版登录首页

![Git 与 GitLab 版本管理第 109 页插图](assets/img-2a75f044ead4c229.png)

以下是旧版的首次登录web页面，必须先设置密码，密码要求最少8位

![Git 与 GitLab 版本管理第 110 页插图](assets/img-7007f5ac1bf069cf.png)

旧版界面

![Git 与 GitLab 版本管理第 110 页插图](assets/img-d5c63bcb09bcc498.png)

旧版登录首页

![Git 与 GitLab 版本管理第 111 页插图](assets/img-9a593f473b778f96.png)

### 修改头像

登录gitlab后可能看到用户的头像不能正常显示,可以修改为自定义的头像

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f9376f1902fe0b9e.png)

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f27f9a5cf22a27ab.png)

![Git 与 GitLab 版本管理第 112 页插图](assets/img-069c521883ef30bc.png)

### 关闭账号注册功能

新版用户注册界面

![Git 与 GitLab 版本管理第 112 页插图](assets/img-997d06d5df1fffcd.png)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-a3b8aef9c6f980ef.png)

关闭注册功能,先用root用户登录

![Git 与 GitLab 版本管理第 113 页插图](assets/img-d198552065266c57.png)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-badc4e8e570b9688.png)

Save Changes 后,再重新登录观察到注册界面不再显示

![Git 与 GitLab 版本管理第 114 页插图](assets/img-50b36a5dc846a8e1.png)

旧版中默认情况下也可以直接注册账号，基于安全目的，一般都会关闭此功能

![Git 与 GitLab 版本管理第 114 页插图](assets/img-e4699db892110eca.png)

取消账户注册功能之后点save changes

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f385317c01cb4bb3.png)

重新登录，验证是否还有注册选项

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f3151643532645c4.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/13-installing-gitlab.html' | relative_url }}">← Previous: Installing GitLab</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">Back to Git and GitLab Version Control Index</a>
  <a href="{{ '/subjects/Git-GitLab/15-gitlab-user-and-group-management.html' | relative_url }}">Next: GitLab User and Group Management →</a>
</nav>
