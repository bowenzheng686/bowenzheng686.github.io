---
layout: default
title: "Git and GitLab Version Control · Resetting a Forgotten GitLab Password"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Git and GitLab Version Control Index]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 21 Resetting a Forgotten GitLab Password
### 3.10 重置 GitLab 忘记的密码

官方说明

<https://docs.gitlab.com/ee/security/reset_user_password.html#reset-the-root-password>

范例:

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
irb(main):002:0> user.password="bowen@123"
=> "bowen@123"
irb(main):003:0> user.password_confirmation="bowen@123"
=> "bowen@123"
#保存
irb(main):004:0> user.save
=> true
#退出控制台
irb(main):005:0> quit
#验证用新密码登录，注意：要使用external_url对应的URL登录才可以
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/20-enabling-https.html' | relative_url }}">← Previous: Enabling HTTPS</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">Back to Git and GitLab Version Control Index</a>
  <a href="{{ '/subjects/Git-GitLab/22-common-interview-questions.html' | relative_url }}">Next: Common Interview Questions →</a>
</nav>
