---
layout: default
title: "Git and GitLab Version Control · GitLab Migration and Upgrades"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Git and GitLab Version Control Index]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 19 GitLab Migration and Upgrades
### 3.8 GitLab 迁移和升级

在生产中升级往往伴随着服务器的迁移,比如从本地机房迁移到云环境中,而实现升级

迁移流程

在原GitLab主机上备份配置文件和数据在目标主机上安装相同的版本的GitLab软件还原配置和数据本质上就是备份和恢复的过程

升级流程

如果新主机，需要先安装原版本，并还原配置和数据

不能直接跳过中间的版本直接升级,选择最近的大版本进行升级

比如:12.1想升级到13.0,先升级到12.X最高版,再升级到13.0

下载新版本的安装包,直接安装包

安装包时可能会提示出错,原因是版本升级后有些配置项会过时,根据提示修改配置即可

重新配置: gitlab-ctl reconfigure

重启服务: gitlab-ctl restart

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/18-gitlab-localization.html' | relative_url }}">← Previous: GitLab Localization</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">Back to Git and GitLab Version Control Index</a>
  <a href="{{ '/subjects/Git-GitLab/20-enabling-https.html' | relative_url }}">Next: Enabling HTTPS →</a>
</nav>
