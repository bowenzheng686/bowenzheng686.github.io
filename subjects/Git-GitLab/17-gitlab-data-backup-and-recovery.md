---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 的数据备份和恢复"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 17 GitLab 数据备份与恢复

备份文件成功生成，不等于灾难发生时一定能恢复。完整方案需要同时保存**应用数据、配置与密钥、外部存储范围**，并在独立实例定期演练。下文以 Linux 软件包安装的 GitLab 为例；容器或 Kubernetes 部署应按相应版本的[官方备份与恢复文档](https://docs.gitlab.com/administration/backup_restore/)调整路径与命令。

### 备份范围与恢复目标

应用备份涵盖数据库、仓库、上传文件等由 GitLab 管理的数据，但通常不包含 `/etc/gitlab/gitlab.rb` 和 `/etc/gitlab/gitlab-secrets.json`。后者关系到加密值解密；即使仓库文件恢复，密钥丢失也可能使 CI 变量、令牌等不可用。若使用对象存储、外部数据库或其他外部服务，还必须核对它们是否纳入单独备份。

先明确两个指标：**RPO** 是可接受的数据丢失时间，决定备份频率；**RTO** 是可接受的恢复时长，决定副本位置、自动化与演练方式。备份副本要放到与 GitLab 实例隔离的受控存储，限制读取权限并验证可读性。

### 创建配置与应用备份

执行前确认备份路径剩余空间、服务状态和当前版本。以下为软件包安装场景的基本命令；不同 GitLab 版本可能采用不同的任务名，应先核对当前版本文档。

```bash
gitlab-ctl status
gitlab-rake gitlab:env:info
gitlab-ctl backup-etc
gitlab-backup create
ls -lh /etc/gitlab/config_backup/
ls -lh /var/opt/gitlab/backups/
```

较旧版本曾用 `gitlab-rake gitlab:backup:create` 创建应用备份。需要自定义路径或保留时间时，在 `/etc/gitlab/gitlab.rb` 配置后执行 `gitlab-ctl reconfigure`；修改前先读当前版本支持的配置项。备份中可能包含源代码、账号信息和密钥，应按敏感数据管理，不能为了方便而设置为所有用户可读。

核对的不只是文件名：检查命令退出状态、日志中每类数据的结果、归档大小是否合理，以及配置备份是否同时包含 `gitlab.rb` 与 `gitlab-secrets.json`。再把两种备份和所依赖的外部数据复制到独立位置。

### 在独立实例做恢复演练

恢复操作会覆盖目标实例数据。先准备与备份匹配的 GitLab 版本和类型、足够的磁盘空间，并备份演练实例自身的数据。不要为了验证备份而删除生产实例中的项目。

下列原课程图片记录隔离实验中删除项目、准备恢复的界面；它们只说明演练场景，不构成生产操作步骤。

![恢复演练的项目示例一](assets/img-035175ab2e0396fd.webp)

![恢复演练的项目示例二](assets/img-cd43800bf0ff7ebb.webp)

![恢复演练的项目示例三](assets/img-1a7bd363bdcd7e79.webp)

恢复前先核对：

1. 备份对应的 GitLab 版本、类型与目标实例满足恢复要求；通常应使用完全一致的版本。
2. 应用备份归档已放在目标实例的备份目录，文件所有者和权限符合 GitLab 要求。
3. `gitlab.rb`、`gitlab-secrets.json` 和外部对象存储等依赖已准备好；演练目标的当前数据已有独立保存。
4. 恢复窗口、用户访问与失败回退方案已经明确。

### 恢复步骤与结果核验

以下是较新软件包版本使用 Puma 和 Sidekiq 的流程骨架。`BACKUP` 值为备份归档文件名去掉 `_gitlab_backup.tar` 后的部分；尖括号不能原样保留。恢复工具可能交互确认覆盖，执行前阅读提示。配置文件和密钥在目标实例的恢复顺序，以当前版本官方文档为准。

```bash
gitlab-ctl stop puma
gitlab-ctl stop sidekiq
gitlab-backup restore BACKUP=<备份 ID>
gitlab-ctl reconfigure
gitlab-ctl restart
gitlab-ctl status
gitlab-rake gitlab:check SANITIZE=true
gitlab-rake gitlab:doctor:secrets
```

旧版可能使用 Unicorn 与 `gitlab-rake gitlab:backup:restore`，这是**历史版本的替代流程**，不应和上面的 Puma 流程混合执行。下面的图片是旧版终端与页面记录，重点观察服务恢复和项目数据，而非照抄其时间戳与组件清单。

![恢复命令的历史终端记录](assets/img-a1ef3d1652d90ae4.webp)

![旧版本恢复记录](assets/img-710dd341e25c70df.webp)

![恢复后项目检查图](assets/img-f515130a78b121da.webp)

**验证应覆盖实际使用链路**：管理员和普通账号登录、项目列表、仓库克隆与推送、附件与制品、CI 变量解密、后台作业，以及邮件或 SSO 等外部集成。网页能打开仅表明 Web 服务启动，不代表数据完整。记录演练用时与发现的缺口，再调整备份频率或范围。

![恢复后访问验证图](assets/img-f2871a71af2ce0ca.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/16-gitlab-project-management.html' | relative_url }}">← 上一篇：GitLab 项目管理</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/18-gitlab-localization.html' | relative_url }}">下一篇：GitLab 汉化 →</a>
</nav>
