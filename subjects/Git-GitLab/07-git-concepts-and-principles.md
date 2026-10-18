---
layout: default
title: "Git 与 GitLab 版本控制 · Git 相关概念和原理"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 07 Git 相关概念和原理

先区分工作区、暂存区和提交历史，再理解分支与标签如何引用提交。后文的命令以已初始化的 Git 仓库为前提。

### Git 的区域

Git 的数据存储从物理上分为当前项目目录和当前项目目录下的隐藏子目录.git，分别称为工作区和版本库

Git 版本库逻辑上又分为暂存区和本地仓库

![Git 与 GitLab 版本管理第 31 页插图](assets/img-eb993f01fa111524.webp)

工作区 Workspace：

工作区是你当前正在编辑和修改文件的地方。它是你的项目目录 ，通常是对应于<项目目录>

在这里你可以添加、修改或删除文件。工作区中的文件可以是已被Git跟踪的文件，也可以是未被跟踪的文件。

Git 能识别已跟踪文件在工作区中的未提交修改，但这些修改尚未写入历史，不能作为已提交版本恢复。对新文件执行 `git add` 后，才会将其内容纳入下一次提交候选。

暂存区 Staging Area/Index/Cached：

暂存区（index）保存**下一次提交的内容快照**。执行 `git add` 会更新该快照；它并不是存放所有工作区修改的普通目录，索引元数据通常位于 `.git/index`。

暂存区主要用于临时保存文件少量变更，类似于邮件中的草稿箱

当变更累积到一定阶段，希望生成里程碑式的结果时，会使用commit，将暂存区的变更一次性的批量提交到本地仓库

本地仓库 Local Repository：

用于存储在工作区和暂存区中改过并提交的文件地方，使用 git commit 提交,对应于/<项目目录 >/.git/

每一次commit 会生成一个唯一的ID，通常用于表示一个阶段性的新的版本

`git checkout` 有切换分支和恢复文件等历史用法；新版本 Git 更推荐用 `git switch` 切换分支、`git restore` 恢复文件。它不是 `git commit` 的逆操作。切换分支时若未提交修改可能被覆盖，Git 通常会阻止切换；但显式强制恢复会丢弃修改，所以执行前先用 `git status` 检查并按需提交或暂存。

远程仓库 Remote Repository ：

多个开发人员共同协作提交代码的仓库，即私有 gitlab 服务器或公有云github,gitee网站等

利用远程仓库，可以实现异地备份和远程协作

![Git 与 GitLab 版本管理第 32 页插图](assets/img-e572e430bace45d4.webp)

### Git 提交历史和提交链

![Git 与 GitLab 版本管理第 32 页插图](assets/img-e576dc511efe61bc.webp)

版本库上的commit历史组合起来会形成一个提交链

除了初始commit，每个commit都会都会有一个父commit，也可能会有多个父commit(比如：分支合并)

提交对象只记录父提交，不直接记录“子提交”。从某个提交创建分支只创建新引用；直到新分支上产生提交，历史中才会出现新的后继提交。

这个提交链上的commit还可以使用字符串进行引用

仓库初始化时会创建默认分支引用，名称可能是 `main`、`master` 或自定义名称，不是同时存在 `master/main` 两个分支。

而该提交链也称为版本库的一个分支（Branch），master/main 也是分支的名称标识

`HEAD` 通常指向当前分支，分支再指向其最新提交；处于分离 HEAD 状态时，它直接指向某个提交。

基于HEAD指向的commit，还能够以相对方式引用历史中的提交，例如HEAD~表示前一个提交 git show HEAD命令可以查看HEAD当前所指向的commit的信息

### Git 分支和标签

<https://git-scm.com/book/zh/v2/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%AE%80%E4%BB%8B>

branch 分支

<https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell>

![Git 与 GitLab 版本管理第 33 页插图](assets/img-e576dc511efe61bc.webp)

Git 的分支，其实本质上仅仅是指向提交对象的可变指针

Git 的默认分支名字是 master/main 。 在多次提交操作之后，你其实已经有一个指向最后那个提交对象的 master/main 分支。 master 分支会在每次提交时自动向前移动。

分支是可移动的提交引用，不是整个文件目录的物理副本。不同分支可以独立演进，切换时 Git 根据目标提交更新工作区文件。

![Git 与 GitLab 版本管理第 33 页插图](assets/img-69de3abed1669c70.webp)

假设你准备开发一个新功能，但是需要两周才能完成，第一周你写了50%的代码，如果立刻提交， 由于代码还没写完，不完整的代码库会导致别人不能测试等工作。如果等代码全部写完再一次提交，又存在丢失每天进度的巨大风险。

现在有了分支，就不用担心了。你创建了一个独立的分支，对其他人是透明的,没有影响,他们还继续在原来的分支上正常工作，而你在自己的分支上工作，想提交就提交，直到开发完毕后，再一次性合并到原来的分支上，这样既安全，又不影响别人工作。

tag 标签

<https://git-scm.com/book/en/v2/Git-Basics-Tagging>

给某个状态打个标签用于记录当前状态,相当于里程碑性的提交

tag是git版本库的一个标记，指向某个commit的指针。为某个commit添加一个标签，从而对其完成特殊标记，例如标记特定的版本信息

tag主要用于发布版本的管理，一个版本发布之后，可以为git打上 v1.0.1,v1.0.2 ...这样的类似的标签。

应在完成一个逻辑上完整、可说明的改动时提交；何时推送由团队协作与备份策略决定。发布时可给对应提交创建标签，但标签并非只用于发布。

tag跟branch有点相似，但是本质上和分工上是不同的：

tag 对应某次commit, 是一个点，是不可移动的。

branch 指向一个提交，并随该分支上的新提交向前移动；`HEAD` 指示当前检出的分支，不是每个分支各自拥有一个 HEAD。

所以，两者的区别决定了使用方式，改动代码用 branch ,不改动只查看用 tag。

tag 和 branch 的相互配合使用，有时候起到非常方便的效果

例如：已经发布了 v1.0 v2.0 v3.0 三个版本，这个时候，我突然想不改现有代码的前提下，在 v2.0 的基础上加个新功能，作为 v4.0 发布。就可以检出 v2.0 的代码作为一个 branch ，然后作为开发分支。

常用的版本标记格式

常见格式是 `v主版本.次版本.修订号`，例如 `v1.3.2`。团队也可采用自己的版本约定，但应保持一致并清楚说明兼容性含义。

Git支持使用两种标签：轻量标签（lightweight）与附注标签（annotated）

轻量标签只是指向提交的引用；附注标签是独立对象，可保存创建者、时间和说明，并可签名。

### Git 开发分支流程

分支管理是现代版本控制系统在记录版本和变更记录之外的另一个非常重要的功能

团队于同一个项目上协作时，分支管理是不可或缺的重要功能，因为它

隔离不同开发人员的改动，为每个人提供一个相对独立的空间

隔离团队根据布节奏要实现的代码提交、审核、集成和测试等工作

“如果说多人软件协作项目中有一个灵魂的话，我认为，这个灵魂就是分支策略。可以说，分支策略就是软件协作模式和发布模式的风向标。选择一种符合 DevOps 开发模式的分支策略，对于 DevOps 的实践落地也会大有帮助。” —— 石雪峰

![Git 与 GitLab 版本管理第 35 页插图](assets/img-03801d2d852df9ec.webp)

![Git 与 GitLab 版本管理第 35 页插图](assets/img-f85fe83905c6b24b.webp)

几种常见的分支模型

master：开发、测试和发布都在master分支上完成

简单，但开发、测试和发布彼此影响，仅适用于单feature且无构建过程的场景

master/develop： 在开发分支开发，完成后合并至master分支，并删除develop分支

master 长期分支，记录发布历史

develop 短期分支，完成开发后合并至master分支

develop分支的开发不会影响到master分支的构建过程，但不利于同时开发多个feature；适用于单feature，可从master执行构建的场景

工作流程

```text
~$ git checkout -b develop # from master
~$ git rebase master    #完成开发、测试
~$ git checkout master
~$ git merge develop    #发布
~$ git branch --delete develop
```

master/develop/feature

![Git 与 GitLab 版本管理第 36 页插图](assets/img-6b51b1de9dd1c9e9.webp)

master和develop 都是长期分支

开发人员工作在各自的feature分支上，feature分支经过开发、模块测试后合并到develop分支

develop分支代码经过系统测试，release之后合并到master分支，release是短期分支

多个feature有利于更大规模的合作，但release独立分支中的bug修复变更与develop上的变更可能会导致冲突；因而，适用于多feature，develop在release过程中不会修改的场景

feature短期分支，保存研发人员研发过程

开作流程

```text
git checkout -b feature # from develop，完成开发和特性测试
git checkout develop
git merge feature
git branch --delete feature #完成集成测试和发布
git checkout master
git merge develop
```

master/develop/feature/release

![Git 与 GitLab 版本管理第 37 页插图](assets/img-1e5463388b93813e.webp)

在前一分支模型的基础上，使用单独的release分支进行构建和bug修复

避免了因发布操作而阻塞了develop分支上的变更，但release分支存在的时间越长，导致develop 合并冲突的可能性越大；因此，适用于多feature开发，但develop功能不受release影响的场景

release：短期分支，承载发布过程

工作流程

```text
git checkout -b feature # from develop，完成开发和特性测试
git checkout develop
git merge feature
git branch --delete feature
git checkout -b release # from develop，完成测试、bug修复和发布
git checkout develop
git merge release   #将release合并至develop
git checkout master
git merge release #将release合并至master
git branch --delete release #删除releae分支
```

master/develop/feature/release/hotfix

![Git 与 GitLab 版本管理第 38 页插图](assets/img-44b019dd112fc3b0.webp)

从master单独拉一个短期的hotfix分支进行问题修复

hotfix: 从master拉出来的分支，短期分支

解决了前一模型中hotfix和develop冲突的问题

适用于多feature开发的场景，release不受线上版本hotfix的影响

工作流程

```text
git checkout master
git checkout -b hotfix # 从 master 创建，完成修复和测试
git checkout master
git merge hotfix #合并hotfix分支至master
git checkout develop
git merge hotfix #合并hotfix分支至develop
git branch --delete hotfix #删除hotfix分支
git checkout release # 已存在的 release 分支
git merge develop # 如需同步 develop，先评估发布冻结与冲突风险
git checkout develop
git merge release  # 将 release 分支合并至 develop
git checkout master
git merge release #将releasc分支合并至master
git branch --delete release # 删除 release 分支
```

### Git 分支合并

分支合并，即将多个分支合并成一个分支

利用 git merge   命令将指定的其它分支合并至当前分支

注意：先切换至需要合并的目标分支，再将其它分支合并至当前的目标分支

分支合并存在两种情形

一种是目标分支没有新提交时的快进式合并（Fast-Forward）；另一种是分支已各自演进时，基于共同祖先进行的三路合并（Three-Way Merge）。

快进式合并

![Git 与 GitLab 版本管理第 39 页插图](assets/img-5905edd346540e72.webp)

三路合并

两个分支各自沿着自己的演进路线分别创建了新的提交

合并时需要共同的祖先提交，以及各分支的最新一次提交进行合并

如图，它需要commit3、commit4和commit5参与合并操作

合并时，若某文件存在无法合并的修改，则意味着存在“冲突”的可能，如果冲突，需要用户手动解决冲突后创建提交完成合并

![Git 与 GitLab 版本管理第 39 页插图](assets/img-0610401d5a8e5d41.webp)

### Git 使用远程仓库

![Git 与 GitLab 版本管理第 39 页插图](assets/img-665596b824b6adbd.webp)

通过远程仓库，基于HTTP、SSH 及 Git 多种传输协议可以实现异地备份和远程协作

推送代码至远程仓库的步骤

在某个Git托管服务上注册一个账号，比如：GitHub，Gitee，GitLAB

在托管平台创建仓库后，用 `git remote add origin <远程仓库 URL>` 给本地仓库配置远程地址。

远程仓库，一般默认名称为origin 相关的url在远程库上可以直接获取到

git push 推送本地仓库到远程仓库，git pull 可以拉取远程仓库代码到本地现在仓库中

没有本地仓库的其它主机通过git clone 可以将远程仓库克隆到本地

下列命令中的 `main` 应换成实际分支名；运行前先确认当前仓库和远程地址。

| 任务 | 命令 |
| --- | --- |
| 添加远程 | `git remote add origin <远程仓库 URL>` |
| 查看远程 | `git remote -v` |
| 重命名 / 删除远程 | `git remote rename origin upstream` / `git remote remove origin` |
| 克隆仓库 | `git clone <远程仓库 URL> [目录名]` |
| 抓取远程更新 | `git fetch origin` |
| 抓取指定分支 | `git fetch origin main` |
| 查看远程分支 | `git branch -r` |
| 合并远程跟踪分支 | 在本地 `main` 上执行 `git merge origin/main` |
| 拉取并合并 | `git pull origin main`；概念上相当于先 `fetch` 再 `merge`，实际行为还受配置影响 |
| 推送分支 / 全部分支 / 全部标签 | `git push origin main` / `git push origin --all` / `git push origin --tags` |

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/06-common-software-deployment-models.html' | relative_url }}">← 上一篇：常见的软件部署模式</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/08-installing-git.html' | relative_url }}">下一篇：Git 安装 →</a>
</nav>
