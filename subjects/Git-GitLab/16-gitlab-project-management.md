---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 项目管理"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 16 GitLab 项目管理

本章先创建项目，再配置成员权限，最后通过 HTTPS 或 SSH 验证克隆、提交和合并请求。不同版本的页面布局不同，以项目的实际命名空间和默认分支为准。

### 创建项目

GitLab 项目属于某个命名空间：可以是个人，也可以是组。一个项目通常对应一个代码仓库及其协作设置，是否按服务或模块拆分取决于团队边界与发布方式。

若准备推送已有本地仓库，可创建**空项目**以避免默认 README 产生额外初始提交；若从零开始，直接初始化 README 也可以，但后续推送须先整合远程历史。

![Git 与 GitLab 版本管理第 123 页插图](assets/img-81cd5d119cd7e59e.webp)

下图展示较新版本中的项目创建入口。

![Git 与 GitLab 版本管理第 123 页插图](assets/img-2bfb657d07b59dce.webp)

本例把项目放在组命名空间下，并选择空仓库，以便上传已有本地历史。

![Git 与 GitLab 版本管理第 123 页插图](assets/img-b1de0ef7fc45f1a2.webp)

![Git 与 GitLab 版本管理第 124 页插图](assets/img-3753ea26c68fbda0.webp)

项目创建页会给出克隆、新文件夹初始化和已有仓库迁移三种指引。它们是**三选一**，不是连续执行的步骤。若已有 Git 仓库，只需要核对目标地址、分支和权限后添加远端并推送；若是普通文件夹，先初始化、提交，再关联远端。实际命令放在本章后面的客户端操作中。

下面三张图是旧版创建流程，用于识别命名空间、可见性和结果页面，不必与新版流程重复操作。

![Git 与 GitLab 版本管理第 125 页插图](assets/img-1827db2fc43e3d2e.webp)

旧版的创建表单如下。

![Git 与 GitLab 版本管理第 125 页插图](assets/img-f471758abb22e520.webp)

创建后先确认项目 URL、默认分支和可见性符合预期。

![Git 与 GitLab 版本管理第 126 页插图](assets/img-bf0595dc531c68ab.webp)

### 导入项目

如果迁移现有托管平台项目，可使用 GitLab 导入器；管理员可能需要先在**管理中心 → 设置 → 通用 → 导入和导出**启用相应来源。导入能力因版本与实例策略而异，迁移后还应核对分支、标签、议题、成员与 CI 设置，而不是仅确认页面出现。

![Git 与 GitLab 版本管理第 126 页插图](assets/img-b2bf90d02be422c2.webp)

![Git 与 GitLab 版本管理第 126 页插图](assets/img-161a6fc896d2c2af.webp)

![Git 与 GitLab 版本管理第 127 页插图](assets/img-e7d61b62ae64c06a.webp)

### 将用户添加到组或项目并指定角色

项目成员可以从组继承，也可以直接添加到项目。权限详情以 [GitLab 角色与权限文档](https://docs.gitlab.com/user/permissions/) 和实例配置为准。

![Git 与 GitLab 版本管理第 128 页插图](assets/img-83c4038dcceb89bd.webp)

常见角色按权限递增，实际能力还受 GitLab 版本、项目设置和保护分支规则影响：

| 角色 | 常见能力与边界 |
| --- | --- |
| Guest | 参与部分议题和评论；对私有仓库源码的访问受具体权限配置限制。 |
| Reporter | 读取代码和结果，通常不能推送。 |
| Developer | 在允许的分支推送并创建合并请求；受保护分支可能禁止直接推送。 |
| Maintainer | 管理项目设置、成员及发布规则，权限高于普通开发者。 |
| Owner | 主要是组级最高权限，涉及组成员与组设置；不是每个项目都单独有 Owner。 |

多个项目共享同一团队时，优先在组中管理成员，以减少逐个项目授权的重复工作。

![Git 与 GitLab 版本管理第 129 页插图](assets/img-b3eb7595274ad620.webp)

Developer 通常可以推送非保护分支；对受保护的 `main`/`master` 是否能推送，由具体保护规则决定。不要为了让开发者推送功能分支就授予 Maintainer 权限。

![Git 与 GitLab 版本管理第 129 页插图](assets/img-c66db547bb0bf0f7.webp)

![Git 与 GitLab 版本管理第 129 页插图](assets/img-2c6257f23a86ff20.webp)

项目直邀适合只需访问单个项目的协作者；组级授权便于统一管理，但也会将权限传播到组内其他项目。应选择最小必要范围，而不是一概避免项目直邀。

![Git 与 GitLab 版本管理第 130 页插图](assets/img-5df5577942ccb700.webp)

以下两张图是旧版成员管理界面，对应的角色含义仍需按当前版本核对。

![Git 与 GitLab 版本管理第 130 页插图](assets/img-ad9bac60abf3d149.webp)

![Git 与 GitLab 版本管理第 131 页插图](assets/img-45a595d82e5a902a.webp)

### 在 Web 界面创建文件

用具有相应权限的成员登录项目，在仓库页面新建 `README.md` 或测试文件。若默认分支受到保护，界面可能引导创建新分支和合并请求，而非允许直接提交。

![Git 与 GitLab 版本管理第 131 页插图](assets/img-51362ca8f4062ba0.webp)

![Git 与 GitLab 版本管理第 132 页插图](assets/img-9c440a3a4e2f8e93.webp)

旧版的文件创建界面如下。

![Git 与 GitLab 版本管理第 132 页插图](assets/img-cdd375deb4200cf7.webp)

填写 `README.md` 文件内容，说明项目用途、运行方式和协作约定。

![Git 与 GitLab 版本管理第 132 页插图](assets/img-242497ba479e5ce5.webp)

提交后回到仓库文件列表，确认文件位于预期分支。

![Git 与 GitLab 版本管理第 133 页插图](assets/img-de85574f6f94c8d6.webp)

![Git 与 GitLab 版本管理第 133 页插图](assets/img-5eca40737d67c9c9.webp)

### 在 Linux 客户端克隆与提交

![Git 与 GitLab 版本管理第 133 页插图](assets/img-945309aaa0cf9fe0.webp)

上面的 Web 示例已有远端提交，因此客户端应先**克隆**，不要再用 `git init` 和强制推送覆盖历史。用项目页面提供的 HTTPS 地址替换占位符：

```bash
git clone <项目 HTTPS URL>
cd <项目目录>
git config user.name "你的姓名"
git config user.email "you@example.com"
git switch -c feature/readme
# 编辑 README.md 后检查并提交
git status
git add README.md
git commit -m "完善项目说明"
git push -u origin feature/readme
```

如果项目尚是空仓库且本地已有提交，则在**现有本地仓库**中用 `git remote add origin <项目 URL>`、`git push -u origin <当前分支>`；不要把这些命令混进克隆流程。HTTPS 推送通常使用访问令牌或凭据管理器，不能将账号密码或令牌写进仓库文件。

### 在 Windows 客户端验证

从 [Git for Windows 官方页面](https://git-scm.com/download/win)安装客户端；命令工作流与 Linux 一致。安装后用 `git --version` 检查，再克隆项目并确认凭据配置，而不是照搬旧截图中的用户名或远端地址。

![Git 与 GitLab 版本管理第 136 页插图](assets/img-013051ffec9909e1.webp)

![Git 与 GitLab 版本管理第 136 页插图](assets/img-62fc1105c08c9fe4.webp)

![Git 与 GitLab 版本管理第 136 页插图](assets/img-5a12e56b7528b661.webp)

### 在 Web 端核对结果

客户端推送后刷新项目页面，检查分支、提交、文件和作者信息。若目标是受保护分支，还应确认合并请求与流水线检查状态。

![Git 与 GitLab 版本管理第 137 页插图](assets/img-a9e9c618635158b1.webp)

![Git 与 GitLab 版本管理第 137 页插图](assets/img-fe32f485a66437b1.webp)

### 使用 SSH 密钥访问

SSH 是 HTTPS 之外的另一种传输方式。生成密钥后，仅把**公钥**添加到 GitLab 个人设置；私钥留在本机。首次连接时，先核对服务器主机指纹与管理员发布的指纹一致，再接受提示。

```bash
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAA... you@example.com
```

![Git 与 GitLab 版本管理第 138 页插图](assets/img-576db9bcedf76171.webp)

![Git 与 GitLab 版本管理第 138 页插图](assets/img-9b85acac7bc2ee95.webp)

```bash
ssh -T git@<GitLab 主机>
git clone git@<GitLab 主机>:<组>/<项目>.git
```

### 保护分支

默认分支是否受保护、哪些角色可以推送或合并，取决于项目当前规则；不能假定所有版本都默认保护 `master`。建议限制主分支直接推送，要求通过合并请求、审查和必要的流水线检查。保护的是分支引用和操作权限，不会替代仓库备份。

![Git 与 GitLab 版本管理第 139 页插图](assets/img-a7422ac9511a27ee.webp)

### 合并分支

开发者将功能分支推送到远端后发起 Merge Request，选择目标分支并说明改动、测试结果和回滚影响。审查者核对差异与流水线，确认通过后按项目策略合并；若未通过，应在原分支修正并重新验证。合并后检查目标分支的新提交，而非只看到“已合并”状态就结束。

![Git 与 GitLab 版本管理第 140 页插图](assets/img-e7d2662ebb302b72.webp)

![Git 与 GitLab 版本管理第 140 页插图](assets/img-4fc1f1d50cb2c9ea.webp)

![Git 与 GitLab 版本管理第 141 页插图](assets/img-5c272788cc609562.webp)

![Git 与 GitLab 版本管理第 142 页插图](assets/img-daa75e8dee41fcc6.webp)

### Gitlab 协议和格式

GitLab 通常提供 HTTPS 与 SSH 两种仓库地址，实际协议与端口以项目的“克隆”菜单为准。优先使用配置正确证书的 HTTPS；内网测试时也不应把明文 HTTP 当成默认生产方案。

HTTPS 地址格式：

```text
#格式
http[s]://host[:Port]/group/project.git
#示例
https://gitlab.example.com/testgroup/testproject.git
```

SSH 地址格式：

```text
#格式
git@host:group/project.git
#非标准端口使用 ssh:// 格式
ssh://git@host:port/group/project.git
#示例
git@gitlab.example.com:testgroup/testproject.git
ssh://git@gitlab.example.com:30022/testgroup/testproject.git
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/15-gitlab-user-and-group-management.html' | relative_url }}">← 上一篇：GitLab 用户和组管理</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/17-gitlab-data-backup-and-recovery.html' | relative_url }}">下一篇：GitLab 数据备份与恢复 →</a>
</nav>
