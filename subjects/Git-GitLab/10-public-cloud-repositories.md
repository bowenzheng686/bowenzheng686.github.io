---
layout: default
title: "Git 与 GitLab 版本控制 · 公有云仓库"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 10 公有云仓库

git 创建本地仓库后,可以将本地仓库和远程仓库进行同步.实现网络共享和备份

远程仓库可以分为公有云仓库和私有仓库

“公有云托管”和“仓库是否公开”是两个维度：GitHub、Gitee 等云服务也能托管私有仓库；GitLab 既可自建，也有云端服务。选择时应看访问控制、合规要求、可用性和备份策略。

### 使用 github

<https://github.com/>

范例：在平台创建空仓库后，将本地 Git 仓库关联到远程。下方旧终端记录中的仓库地址和 `master` 分支只作示例，实际操作应替换为自己的地址与分支名。

![Git 与 GitLab 版本管理第 80 页插图](assets/img-81c9f40c134b1cb4.webp)

```bash
[root@gitlab testproject]#git remote add origin git@github.com:lbtooth/hello-world.git
[root@gitlab testproject]#git remote
origin
[root@gitlab testproject]#git remote  -v
origin  git@github.com:lbtooth/hello-world.git (fetch)
origin  git@github.com:lbtooth/hello-world.git (push)
[root@gitlab testproject]#git push -u origin master
The authenticity of host 'github.com (52.74.223.119)' can't be established.
RSA key fingerprint is SHA256:nThbg6kXUpJWGl7E1IGOCspRomTxdCARLviKw6E5SY8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'github.com,52.74.223.119' (RSA) to the list of known
hosts.
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.
[root@gitlab testproject]#ssh-keygen -t ed25519 -C "you@example.com"
[root@gitlab testproject]#cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAA... you@example.com
```

![Git 与 GitLab 版本管理第 81 页插图](assets/img-f9e732589ac3f546.webp)

上例首次推送因没有配置可用 SSH 公钥而失败。先核对远程主机指纹，再把生成的**公钥**添加到代码托管平台；私钥始终留在本机。完成后重新执行 `git push -u origin master`，下方输出才代表推送成功。

```bash
[root@gitlab testproject]#git push -u origin master
Counting objects: 11, done.
Delta compression using up to 2 threads.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (11/11), 825 bytes | 825.00 KiB/s, done.
Total 11 (delta 0), reused 0 (delta 0)
To github.com:lbtooth/hello-world.git
* [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```

### 使用 gitee

范例: 国内码云创建仓库

![Git 与 GitLab 版本管理第 82 页插图](assets/img-ae533e6e94314082.webp)

![Git 与 GitLab 版本管理第 83 页插图](assets/img-5130a14b27114a1c.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/09-git-command-syntax.html' | relative_url }}">← 上一篇：Git 常用语法</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/11-case-study-a-metaverse-startup.html' | relative_url }}">下一篇：综合案例：从个人开发到团队协作 →</a>
</nav>
