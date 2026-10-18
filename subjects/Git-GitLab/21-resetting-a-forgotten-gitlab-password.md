---
layout: default
title: "Git 与 GitLab 版本控制 · 重置 GitLab 忘记的密码"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 21 重置遗忘的 GitLab 管理员密码

此操作针对**自管理 GitLab 实例**的管理员账户。先确认当前实例、备份和操作权限；密码重置会影响现有登录会话与自动化凭据，完成后应通知相关负责人更新依赖。

官方说明

<https://docs.gitlab.com/ee/security/reset_user_password.html#reset-the-root-password>

优先按当前安装版本的官方文档使用交互式重置命令：

```bash
sudo gitlab-rake "gitlab:password:reset[root]"
```

命令会提示输入新密码，避免把明文密码写进终端历史或教程。若版本不支持该任务，再依据官方文档使用 Rails 控制台。下列旧版控制台输出只演示查找用户和保存逻辑；密码值请在实际会话中输入独立强密码，不要复用示例。

```bash
[root@gitlab ~]#gitlab-rails console -e production
#此步可能比较慢,需要等一段时间
--------------------------------------------------------------------------------
Ruby:         ruby 2.7.5p203 (2021-11-24 revision f69aeb8314) [x86_64-linux]
GitLab:       15.1.2 (ea7455c8292) FOSS
GitLab Shell: 14.7.4
PostgreSQL:   13.6
------------------------------------------------------------[ booted in 23.59s ]
Loading production environment (Rails 6.1.4.7)
#输入下面指令
#方法1
irb(main):001:0> user = User.find_by_username 'root'
#方法2
irb(main):001:0> user = User.where(id: 1).first
=> #<User id:1 @root>
#更改密码并确认密码
irb(main):002:0> new_password = '<本次新设的强密码>'
irb(main):003:0> user.password = new_password
irb(main):004:0> user.password_confirmation = new_password
#保存
irb(main):005:0> user.save!
=> true
#退出控制台
irb(main):006:0> quit
#验证用新密码登录，注意：要使用external_url对应的URL登录才可以
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/20-enabling-https.html' | relative_url }}">← 上一篇：为 GitLab 启用 HTTPS</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/22-common-interview-questions.html' | relative_url }}">下一篇：常见面试题 →</a>
</nav>
