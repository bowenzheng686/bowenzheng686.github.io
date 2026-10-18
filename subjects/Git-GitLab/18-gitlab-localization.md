---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 汉化"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 18 GitLab 汉化
### 3.7 GitLab 汉化

gitlab 默认是英文界面，可以汉化为中文界面，有三种汉化方式

### 官方内置的配置实现汉化

GitLab 自带中文语言支持，但汉化的不彻底，可以通过下面配置修改语言显示

![Git 与 GitLab 版本管理第 151 页插图](assets/img-16f0b4c92a65d704.webp)

查看效果

![Git 与 GitLab 版本管理第 151 页插图](assets/img-1b6191ad71aabe5e.webp)

### 在界面中选择中文

GitLab 已内置中文界面。登录后进入个人头像菜单中的 **Preferences / 偏好设置**，在语言选项中选择简体中文并保存，刷新页面核对菜单、项目页与设置页。部分术语可能仍保留英文，这是产品翻译覆盖度或版本差异，不代表设置失败。

![Git 与 GitLab 版本管理第 153 页插图](assets/img-a853186aeddba5f9.webp)

原稿中替换 `/opt/gitlab/embedded/service/gitlab-rails` 或给它打旧版汉化补丁的做法，会修改软件包管理的应用文件，并可能在升级后失效。现代 GitLab 优先使用内置语言，不再把第三方补丁作为推荐步骤。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/17-gitlab-data-backup-and-recovery.html' | relative_url }}">← 上一篇：GitLab 数据备份与恢复</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/19-gitlab-migration-and-upgrades.html' | relative_url }}">下一篇：GitLab 迁移与升级 →</a>
</nav>
