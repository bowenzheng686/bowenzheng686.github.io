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

安装完成后，应依次完成首次登录、管理员密码更新与账号注册策略检查。界面位置会随版本变化，以下截图主要帮助识别操作目标，而非保证按钮名称始终相同。

### 首次登录 GitLab Web 界面修改密码

新版gitlab密码初始化官方帮助链接

<https://docs.gitlab.com/omnibus/installation/index.html>

浏览器访问 `external_url` 对应的地址，优先使用配置正确证书的 HTTPS 域名。若页面无法打开，先核对 DNS、端口与 `gitlab-ctl status`，不要随意改用 IP 绕过域名配置。

在新版gitlab中第一次登录的界面发生变化,取消重设密码界面,需要直接输入用户和密码才能登录

默认用户为root，其密码是随机生成

![Git 与 GitLab 版本管理第 107 页插图](assets/img-90a9eb8780a6b293.webp)

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
Password: <安装时生成的一次性初始密码>
# NOTE: This file will be automatically deleted in the first reconfigure run
after 24 hours.
```

新版登录界面,用root用户和配置文件中指定的密码或以上文件中的初始密码登录

![Git 与 GitLab 版本管理第 108 页插图](assets/img-07d2d68beea4bb3f.webp)

首次登录后及时设置独立强密码，按实例策略配置双因素认证，并确认管理员邮箱可接收通知。密码策略随版本和实例配置变化，不应只以“至少 8 位”为唯一标准。

![Git 与 GitLab 版本管理第 108 页插图](assets/img-95918d76fefab75f.webp)

使用用户 root 和上面设置的密码登录

新版界面

![Git 与 GitLab 版本管理第 109 页插图](assets/img-3573308b805039f8.webp)

新版登录首页

![Git 与 GitLab 版本管理第 109 页插图](assets/img-2a75f044ead4c229.webp)

以下是旧版的首次登录web页面，必须先设置密码，密码要求最少8位

![Git 与 GitLab 版本管理第 110 页插图](assets/img-7007f5ac1bf069cf.webp)

旧版界面

![Git 与 GitLab 版本管理第 110 页插图](assets/img-d5c63bcb09bcc498.webp)

旧版登录首页

![Git 与 GitLab 版本管理第 111 页插图](assets/img-9a593f473b778f96.webp)

### 修改头像

头像无法显示通常只影响界面，不代表仓库服务故障。进入个人资料设置上传受支持的图片即可；若所有用户头像都异常，再检查外部头像服务、代理与网络策略。

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f9376f1902fe0b9e.webp)

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f27f9a5cf22a27ab.webp)

![Git 与 GitLab 版本管理第 112 页插图](assets/img-069c521883ef30bc.webp)

### 关闭账号注册功能

新版用户注册界面

![Git 与 GitLab 版本管理第 112 页插图](assets/img-997d06d5df1fffcd.webp)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-a3b8aef9c6f980ef.webp)

若实例只面向组织内部成员，可由管理员在**管理中心 → 设置 → 通用 → 注册限制**关闭公开注册。确需对外开放注册时，应保留审批、验证和滥用防护措施，而不是机械关闭。

![Git 与 GitLab 版本管理第 113 页插图](assets/img-d198552065266c57.webp)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-badc4e8e570b9688.webp)

保存后退出登录并检查注册入口是否消失；再用普通账户验证已有用户仍可正常登录。关闭注册只阻止自助创建新用户，不会删除现有账号。

![Git 与 GitLab 版本管理第 114 页插图](assets/img-50b36a5dc846a8e1.webp)

旧版中默认情况下也可以直接注册账号，基于安全目的，一般都会关闭此功能

![Git 与 GitLab 版本管理第 114 页插图](assets/img-e4699db892110eca.webp)

取消账户注册功能之后点save changes

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f385317c01cb4bb3.webp)

重新登录，验证是否还有注册选项

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f3151643532645c4.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/13-installing-gitlab.html' | relative_url }}">← 上一篇：GitLab 安装</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/15-gitlab-user-and-group-management.html' | relative_url }}">下一篇：GitLab 用户和组管理 →</a>
</nav>
