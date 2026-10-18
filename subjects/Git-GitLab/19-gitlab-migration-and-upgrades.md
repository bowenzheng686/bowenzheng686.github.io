---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 迁移和升级"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 19 GitLab 迁移与升级

**迁移**是把服务与数据移到另一台主机或环境；**升级**是改变 GitLab 软件版本。两件事可以分开进行，合并操作会增加排障难度。通常先在目标环境恢复相同版本并验收，再按照官方升级路径逐步升级。

### 迁移：保持版本不变，先验证恢复

1. 盘点原实例的 GitLab 版本、发行类型、外部数据库与对象存储、域名、证书、Runner 和容器镜像仓库。
2. 备份应用数据，并单独保存 `gitlab.rb`、`gitlab-secrets.json` 与相关证书；验证备份文件可读。
3. 在目标主机安装满足恢复要求的相同 GitLab 版本，先在隔离环境恢复并检查用户、项目、仓库读写和附件。
4. 规划停写窗口、增量差异和 DNS 切换，再开放目标实例；保留可回退的原环境直至验收完成。

### 升级：逐个满足必经版本

GitLab 有特定的“必经升级版本”和后台迁移要求，路径随起点、终点及安装方式变化。不能只凭“先升级到当前大版本最高小版本，再跨大版本”这一固定规则推导。操作前用 [官方升级路径工具](https://docs.gitlab.com/update/upgrade_paths/) 核对每一站，并阅读目标版本发行说明。

每一站应：备份并留出回滚窗口；安装匹配的软件包；执行 `gitlab-ctl reconfigure`；检查 `gitlab-ctl status`、数据库后台迁移和仓库读写；待当前站健康后再进入下一站。若配置项过时，按发行说明迁移设置，而不是只看到服务能启动就继续升级。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/18-gitlab-localization.html' | relative_url }}">← 上一篇：GitLab 汉化</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/20-enabling-https.html' | relative_url }}">下一篇：为 GitLab 启用 HTTPS →</a>
</nav>
