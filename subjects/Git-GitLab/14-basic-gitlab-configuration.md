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

安装及初始密码的版本说明可参考 [GitLab Linux package 安装文档](https://docs.gitlab.com/install/package/)；下面以软件包安装的 Omnibus 实例为例。

浏览器访问 `external_url` 对应的地址，优先使用配置正确证书的 HTTPS 域名。若页面无法打开，先核对 DNS、端口与 `gitlab-ctl status`，不要随意改用 IP 绕过域名配置。

首次登录使用管理员账号 `root`。若安装时未显式设置初始密码，GitLab 可能把生成的密码临时写入 `/etc/gitlab/initial_root_password`；该文件会在后续重配置中被移除，且密码修改后其中的值不再有效。不要把文件内容保存到课程笔记或工单。

![Git 与 GitLab 版本管理第 107 页插图](assets/img-90a9eb8780a6b293.webp)

```bash
sudo cat /etc/gitlab/initial_root_password
```

下图是较新版本的登录界面。输入安装时设定的管理员密码，或上述文件中的临时初始密码；若密码已过期或无法登录，按管理员密码重置流程处理。

![Git 与 GitLab 版本管理第 108 页插图](assets/img-07d2d68beea4bb3f.webp)

首次登录后及时设置独立强密码，按实例策略配置双因素认证，并确认管理员邮箱可接收通知。密码策略随版本和实例配置变化，不应只以“至少 8 位”为唯一标准。

![Git 与 GitLab 版本管理第 108 页插图](assets/img-95918d76fefab75f.webp)

完成密码更新后重新登录，确认管理员首页正常打开。

![Git 与 GitLab 版本管理第 109 页插图](assets/img-3573308b805039f8.webp)

下图继续展示当时版本的首页布局；具体菜单位置可能随版本调整。

![Git 与 GitLab 版本管理第 109 页插图](assets/img-2a75f044ead4c229.webp)

旧版安装可能在首次访问时直接显示设置密码页面。它与上面的临时密码文件流程是不同版本的界面，不需要依次执行。

![Git 与 GitLab 版本管理第 110 页插图](assets/img-7007f5ac1bf069cf.webp)

旧版登录页示例如下。

![Git 与 GitLab 版本管理第 110 页插图](assets/img-d5c63bcb09bcc498.webp)

旧版首页示例如下。

![Git 与 GitLab 版本管理第 111 页插图](assets/img-9a593f473b778f96.webp)

### 修改头像

头像无法显示通常只影响界面，不代表仓库服务故障。进入个人资料设置上传受支持的图片即可；若所有用户头像都异常，再检查外部头像服务、代理与网络策略。

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f9376f1902fe0b9e.webp)

![Git 与 GitLab 版本管理第 111 页插图](assets/img-f27f9a5cf22a27ab.webp)

![Git 与 GitLab 版本管理第 112 页插图](assets/img-069c521883ef30bc.webp)

### 关闭账号注册功能

先查看登录页是否有注册入口，再到管理中心核对当前注册策略。

![Git 与 GitLab 版本管理第 112 页插图](assets/img-997d06d5df1fffcd.webp)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-a3b8aef9c6f980ef.webp)

若实例只面向组织内部成员，可由管理员在**管理中心 → 设置 → 通用 → 注册限制**关闭公开注册。确需对外开放注册时，应保留审批、验证和滥用防护措施，而不是机械关闭。

![Git 与 GitLab 版本管理第 113 页插图](assets/img-d198552065266c57.webp)

![Git 与 GitLab 版本管理第 113 页插图](assets/img-badc4e8e570b9688.webp)

保存后退出登录并检查注册入口是否消失；再用普通账户验证已有用户仍可正常登录。关闭注册只阻止自助创建新用户，不会删除现有账号。

![Git 与 GitLab 版本管理第 114 页插图](assets/img-50b36a5dc846a8e1.webp)

旧版界面中的对应选项位置如下；是否关闭注册应由实例面向的人群和账号审批流程决定。

![Git 与 GitLab 版本管理第 114 页插图](assets/img-e4699db892110eca.webp)

更改设置后保存，并确认提示生效。

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f385317c01cb4bb3.webp)

最后用未登录窗口验证注册入口，同时检查现有用户登录。

![Git 与 GitLab 版本管理第 115 页插图](assets/img-f3151643532645c4.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/13-installing-gitlab.html' | relative_url }}">← 上一篇：GitLab 安装</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/15-gitlab-user-and-group-management.html' | relative_url }}">下一篇：GitLab 用户和组管理 →</a>
</nav>
