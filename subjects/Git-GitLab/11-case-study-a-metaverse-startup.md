---
layout: default
title: "Git 与 GitLab 版本控制 · 综合案例: 元宇宙创业史"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 11 综合案例：从个人开发到团队协作

假设一个小团队从单人开发的页面项目起步，后来需要并行开发、在多台电脑上协作，最终发布可追溯版本。这个案例按项目成长顺序串联前几章的 Git 概念；命令中的 URL 和分支名是示意，执行前先查看 `git status`、`git branch -a` 与 `git remote -v`。

### 第一阶段：个人项目留下可信的提交

开发者先初始化仓库，明确提交身份，再把一个完整、可运行的改动作为提交。`git add .` 可能误纳入临时文件，因此提交前应检查暂存差异。

```bash
mkdir meta-project && cd meta-project
git init -b main
git config user.name "你的姓名"
git config user.email "you@example.com"
printf '<h1>项目首页</h1>\n' > index.html
git add index.html
git diff --staged
git commit -m "建立项目首页"
git log --oneline --graph
```

后续新增功能时，先修改文件，再检查、暂存和提交。若仅想查看旧提交，可用 `git show <提交 ID>`；不必为了“回看历史”执行 `git reset --hard`。`reset --hard` 会改变当前分支并丢弃未提交修改，只应在明确需要放弃本地历史时使用。

### 第二阶段：用分支隔离新功能

团队希望开发一个新特性，而当前版本仍需稳定运行。开发者从 `main` 创建短期功能分支，完成并测试后再合并，避免把半成品直接推向主分支。

```bash
git switch main
git switch -c feature/ar
# 编辑 index.html，完成相关测试
git add index.html
git commit -m "增加 AR 展示入口"
git switch main
git merge feature/ar
git branch -d feature/ar
```

最后两行只有在功能已审核、通过测试且无需继续开发时才执行。若两边修改同一位置，合并可能冲突，需要读懂双方意图、解决冲突并重新测试；Git 不会自动判断业务上哪一版正确。

### 第三阶段：把仓库共享到远端

团队在托管平台创建**空仓库**。如果平台已生成 README 等初始提交，应先整合远端历史，而不是强制覆盖。下列原课程图片展示当时的创建页面与结果页面，按钮和套餐信息以当前平台为准。

![远程仓库创建示例一](assets/img-45ed136d66627554.webp)

![远程仓库创建示例二](assets/img-d205504ed56a6a32.webp)

```bash
git remote add origin <远端仓库 URL>
git remote -v
git push -u origin main
```

`origin` 是远端名称，只需添加一次。后续如仓库地址变更，使用 `git remote set-url origin <新 URL>`。普通协作通常只推送需要共享的分支，不必无条件 `git push --all`；公开敏感或实验分支前先审查内容。

![远程仓库查看提交的历史界面](assets/img-15c43c484409ec40.webp)

### 第四阶段：另一台电脑继续开发

新电脑只需克隆一次。克隆会配置 `origin` 并获取远端历史；之后在同一目录内用 `fetch` 或 `pull` 更新，不要每天重新克隆。

```bash
git clone <远端仓库 URL>
cd meta-project
git branch -a
git switch -c feature/search
# 编辑文件并完成测试
git add <文件>
git commit -m "增加搜索入口"
git push -u origin feature/search
```

在另一台电脑接着处理同一功能分支时，先取得远端更新，再修改：

```bash
git fetch origin
git switch --track origin/feature/search  # 本机尚无该分支时
git pull --ff-only origin feature/search
```

若本机已有该分支，直接 `git switch feature/search` 即可。`--ff-only` 避免在没有明确决定合并策略时意外产生合并提交；若两台机器都提交了不同改动，需要先理解差异，再按团队策略合并或变基。

### 第五阶段：审查、发布和修复

功能完成后推送分支，在平台发起合并请求。审查者检查代码与自动化测试，再将其合入受保护的 `main`。发布时给通过验证的提交创建标签：

```bash
git switch main
git pull --ff-only origin main
git tag -a v1.0.0 -m "首个正式版本"
git push origin v1.0.0
```

标签是指向某个提交的名称，不是文件快照的额外副本。若线上版本出错，应先判断是回滚发布制品、创建修复提交，还是对某个共享提交执行 `git revert`；不要对已共享的 `main` 直接 `reset --hard` 后强制推送。

### 认证方式与最小风险

HTTPS 可以结合凭据管理器和平台访问令牌；SSH 则使用公私钥。令牌不要写入远端 URL、脚本或提交历史。使用 SSH 时只把 `~/.ssh/id_ed25519.pub` 的**公钥**加入平台，私钥留在本机，并核对首次连接的主机指纹。认证方式改变的是传输凭据，不改变分支、提交和审查流程。

至此，一个项目从单机历史发展为多人协作仓库。可靠性来自小而清楚的提交、受审查的合并、可追溯的标签和明确的发布验证，而不是单纯把代码推送到云端。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/10-public-cloud-repositories.html' | relative_url }}">← 上一篇：公有云仓库</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/12-introduction-to-gitlab.html' | relative_url }}">下一篇：GitLab 介绍 →</a>
</nav>
