---
layout: default
title: "Git 与 GitLab 版本控制 · Git 常用语法"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 09 Git 常用语法
### 2.3 Git 常用语法

使用 git 命令添加代码,提交等管理代码操作

### Git 用法说明

官方文档:

<https://git-scm.com/docs>

<https://git-scm.com/book/zh/v2>

![Git 与 GitLab 版本管理第 53 页插图](assets/img-0cf22fd127fa17c6.webp)

区域间文件操作

![Git 与 GitLab 版本管理第 53 页插图](assets/img-2bc00c18e07eea77.webp)

git 的命令应按工作流理解，而不是记忆一张混合了参数、注释和换行的长清单。下面各行都是独立命令；尖括号表示需要替换的值，不要原样输入。

| 阶段 | 常用命令 | 作用 |
| --- | --- | --- |
| 创建仓库 | `git init -b main` / `git clone <仓库 URL>` | 初始化本地仓库，或克隆已有远程仓库。 |
| 设置身份 | `git config --global user.name "你的姓名"` / `git config --global user.email "you@example.com"` | 设置提交作者信息；不是远程登录凭据。 |
| 查看状态 | `git status` / `git diff` / `git diff --staged` | 分别检查工作树、未暂存差异和已暂存差异。 |
| 暂存并提交 | `git add <路径>` / `git commit -m "说明"` | 选择要提交的内容并生成提交。`git commit -am` 不包括未跟踪的新文件。 |
| 撤销暂存 | `git restore --staged <路径>` | 从暂存区移除变更，保留工作区文件。 |
| 丢弃工作区修改 | `git restore <路径>` | 将已跟踪文件恢复为暂存区版本；未提交的修改会丢失。 |
| 查看历史 | `git log --oneline --graph --all` / `git show <提交>` | 阅读提交图和具体差异。 |
| 新建并切换分支 | `git switch -c <分支名>` / `git switch <分支名>` | 隔离开发和切换工作线。 |
| 合并 | 在目标分支执行 `git merge <来源分支>` | 把来源分支的变更带入当前分支。 |
| 标记发布 | `git tag -a v1.0.0 -m "发布说明"` | 给当前提交创建附注标签。 |
| 关联远程 | `git remote add origin <仓库 URL>` / `git remote -v` | 添加并检查远程地址；并不在平台上创建仓库。 |
| 同步 | `git fetch origin` / `git pull --ff-only origin main` / `git push -u origin main` | 先抓取、按策略整合、再推送。`pull` 的行为还受配置影响。 |

**容易混淆的操作：** `git rm <路径>` 会删除工作区文件并暂存删除；`git rm --cached <路径>` 只停止跟踪，不删除工作区文件。`git reset --hard <提交>` 会丢弃未提交修改并移动当前分支，不适合直接处理已共享历史；已推送的错误提交通常用 `git revert <提交>` 生成抵消提交。

### 自定义提交日志

`git log --oneline --graph --all` 足够用于日常追踪。需要自定义输出时，可用：

```bash
git log --graph --pretty=format:'%h %ad %an %s' --date=short
```

上例依次显示短提交 ID、作者日期、作者姓名和标题。常用占位符如下，更多格式以 `git help log` 中的 PRETTY FORMATS 为准。

| 占位符 | 含义 | 占位符 | 含义 |
| --- | --- | --- | --- |
| `%H` / `%h` | 完整 / 缩短的提交 ID | `%P` / `%p` | 完整 / 缩短的父提交 ID |
| `%an` / `%ae` | 作者姓名 / 邮箱 | `%cn` / `%ce` | 提交者姓名 / 邮箱 |
| `%ad` / `%ar` | 作者日期 / 相对时间 | `%cd` / `%cr` | 提交者日期 / 相对时间 |
| `%s` / `%b` | 提交标题 / 正文 | `%d` | 分支和标签等引用名 |
| `%n` / `%%` | 换行 / 字面百分号 | `%C(...)` / `%Creset` | 设置 / 重置输出颜色 |

### Git 案例

### 创建项目并初始化配置

```bash
[root@gitlab ~]#mkdir /data/testproject/
[root@gitlab ~]#cd /data/testproject/
#初始化
[root@gitlab testproject]#git init
[root@gitlab testproject]#ls -a
.  ..   .git
[root@gitlab testproject]#tree .git
.git
├── branches                #分支
├── config                  #git config命令设置的配置信息
├── description             #被git web(Github的原型)用来显示对仓库的描述
├── HEAD                    #当前分支的标识符号，一般指向refs/heads目录下的分支文件
├── hooks                   #触发器规则的文件，俗称"钩子文件"
│   ├── applypatch-msg.sample
│   ├── commit-msg.sample
│   ├── fsmonitor-watchman.sample
├── info                    #一些特殊文件设置目录，比如忽略文件设置，.gitignore是互补的
│   └── exclude
├── objects                 #存放git对象，git 核心的文件目录
│   ├── info
│   └── pack
└── refs                    #各个提交对象的标识(SHA-1)文件
├── heads               #分支相关信息的目录
└── tags                #标签相关信息的目录
9 directories, 17 files
# 提交前设置作者身份；示例名称和邮箱需替换为自己的信息。
#选项--system 表示针对所有用户的配置,保存在/etc/gitconfig文件中
#选项--global 表示当前用户环境,保存在~/.gitconfig文件中,推荐使用
#选项--local  表示只针对当前目录(项目)的配置,保存在当前目录的.git/config文件中，此为默认值，
可省略
#优先级:local > global > system
#配置文件使用ini格式，存在一至多个[section]，各配置参数可以section为前缀引用
#列出已有配置：git config -l | --list
#用户名，另外还可以使用author.name标记作者，以及使用committer.name标记提交者
[root@gitlab ~]#git config --global user.name bowenxiaochun
#用户的邮箱，还可以使用author.email标记作者邮箱和使用committer.email标记提交者邮箱
[root@gitlab ~]#git config --global user.email you@example.com
#为color.diff和color.grep设定默认值,true或auto表示启用语法着色功能,false或never表示关闭语
法着色功能
[root@gitlab ~]#git config --global color.ui true
#配置git默认使用的文本编辑器,也可由环境变量GIT_EDITOR指定，且此变量的优先级更高
[root@gitlab ~]#git config --global core.editor vim
#system级和global优先级比较
[root@gitlab ~]#git config  --system user.name bowen
#查看system,global和local的配置
[root@gitlab ~]#git config -l
user.name=bowenxiaochun             #global级优先级高于system
user.email=you@example.com
core.editor=vim
core.ui=true
[root@gitlab ~]#cat .gitconfig
[user]
name = bowenxiaochun
email = you@example.com
#只查看global配置
[root@gitlab ~]#git config -l --global
#交互编辑配置
[root@gitlab ~]#git config --global -e
#删除配置
[root@gitlab ~]#git config --unset --system user.name
```

### 添加暂存区并提交数据

```bash
[root@gitlab testproject]#touch a.txt
[root@gitlab testproject]#git add a.txt
[root@gitlab testproject]#git commit -m 'add a.txt'
```

注意:

`git status` 会区分“尚未暂存”和“已暂存”的变更。终端颜色会受配置影响，因此不要只凭红绿判断，应阅读状态标题及 `git diff` / `git diff --staged` 的内容。

![Git 与 GitLab 版本管理第 60 页插图](assets/img-d7818a44bdd480c4.webp)

下图展示了已暂存变更的状态；提交前再核对 `git diff --staged`，确认没有误加入文件。

![Git 与 GitLab 版本管理第 60 页插图](assets/img-eb1a5903b7d34bd5.webp)

### 设置忽略文件

`.gitignore` 告诉 Git 不要自动加入**尚未跟踪**且匹配规则的文件；已跟踪文件不会因新增忽略规则而停止跟踪。必要时先从索引中移除，再提交该变更。

生产中有如下几类文件可能需要忽略

常见忽略对象包括构建产物、编辑器临时文件、本地缓存和含本机配置的文件。但不要把项目所需的图片或可共享的配置一概忽略；密钥更不应先提交再依赖 `.gitignore` 补救。

范例: 忽略指定文件

```bash
[root@gitlab testproject]#cat .gitignore
/bin
/target
.classpath
.project
.settings
*.h
!test.h
*.py[cx]
# Java class files
*.class
# vim swap file
*.swp
# Executable files
*.exe
# Object and archive files
# Can use regular expression, e.g., [oa] matches either o or a *.[oa]
# temp sub-directory (ended with a directory separator)
temp/
```

```bash
#注意:无须提交此文件.gitignore 就可以立即生效忽略，但为了保存此文件，还是最终需要提交此文件到
本地仓库中
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git commit -m '设置忽略'
```

范例:

```bash
[root@ubuntu2204 ~]#cat RuoYi-Vue/.gitignore
######################################################################
# Build Tools
.gradle
/build/
!gradle/wrapper/gradle-wrapper.jar
target/
!.mvn/wrapper/maven-wrapper.jar
######################################################################
# IDE
### STS ###
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
### IntelliJ IDEA ###
.idea
*.iws
*.iml
*.ipr
### JRebel ###
rebel.xml
### NetBeans ###
nbproject/private/
build/*
nbbuild/
dist/
nbdist/
.nb-gradle/
######################################################################
# Others
*.log
*.xml.versionsBackup
*.swp
!*/build/*.java
!*/build/*.html
!*/build/*.xml
```

### 将文件加入暂存区再取消添加

```bash
[root@gitlab testproject]#touch f1.txt
[root@gitlab testproject]#git status
On branch master
No commits yet
Untracked files:
(use "git add <file>..." to include in what will be committed)
f1.txt
nothing added to commit but untracked files present (use "git add" to track)
[root@gitlab testproject]#git add f1.txt
#查看暂存区文件
[root@gitlab testproject]#git ls-files
f1.txt
[root@gitlab testproject]#git status
On branch master
No commits yet
Changes to be committed:
(use "git rm --cached <file>..." to unstage)
new file:   f1.txt
#从暂存区删除
#方法1
[root@gitlab testproject]#git rm --cached f1.txt
#方法2
[root@gitlab testproject]#git restore --staged f1.txt  # 与上一种方法择一，不要连续执行
#确认是否从暂存区删除
[root@gitlab testproject]#git status
On branch master
No commits yet
Untracked files:
(use "git add <file>..." to include in what will be committed)
f1.txt
nothing added to commit but untracked files present (use "git add" to track)
#确认暂存区文件不存在
[root@gitlab testproject]#git ls-files
[root@gitlab testproject]#
```

### 查看暂存区的文件内容

```bash
[root@rocky8 testproject]#echo testdata > test.txt
[root@rocky8 testproject]#git add .
#查看暂存区的文件
[root@rocky8 testproject]#git ls-files -s
100644 4871fd52755be519c29ae719f385bd5f2863627c 0   test.txt
[root@rocky8 testproject]#file .git/objects/48/71fd52755be519c29ae719f385bd5f2863627c
.git/objects/48/71fd52755be519c29ae719f385bd5f2863627c: VAX COFF executable -
version 20741
[root@rocky8 testproject]#git cat-file -t 4871fd52755be519c29ae719f385bd5f2863627c
blob
[root@rocky8 testproject]#git cat-file -p 4871fd52755be519c29ae719f385bd5f2863627c
testdata
```

### 利用暂存区恢复误删除的工作区文件

```bash
[root@gitlab testproject]#touch test.txt
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git ls-files
README.md
b.txt
test.txt
[root@gitlab testproject]#rm -f test.txt
[root@gitlab testproject]#ls
README.md
#从暂存区复制文件到工作目录，两种方式
[root@gitlab testproject]#git restore test.txt
[root@gitlab testproject]#git checkout -- test.txt  # 旧写法，与上一行择一
[root@gitlab testproject]#ls
README.md  test.txt
```

### 同时删除工作区和暂存区

```bash
[root@gitlab testproject]#touch f2.txt
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git ls-files
f1.txt
f2.txt
[root@gitlab testproject]#ls
f1.txt  f2.txt
#同时删除工作区和暂存区文件
[root@gitlab testproject]#git rm -f f2.txt
rm 'f2.txt'
[root@gitlab testproject]#ls
f1.txt
[root@gitlab testproject]#git ls-files
f1.txt
```

### 回滚工作区的文件为暂存区中版本

```bash
[root@gitlab testproject]#echo v1 > f1.txt
[root@gitlab testproject]#git status
On branch master
No commits yet
Untracked files:
(use "git add <file>..." to include in what will be committed)
f1.txt
nothing added to commit but untracked files present (use "git add" to track)
[root@gitlab testproject]#git add .
[root@gitlab testproject]#echo v2 > f1.txt
[root@gitlab testproject]#git status
On branch master
No commits yet
Changes to be committed:
(use "git rm --cached <file>..." to unstage)
new file:   f1.txt
Changes not staged for commit:
(use "git add <file>..." to update what will be committed)
(use "git checkout -- <file>..." to discard changes in working directory)
modified:   f1.txt
#回滚工作区的文件为暂存区中版本
[root@gitlab testproject]#git checkout -- f1.txt
[root@gitlab testproject]#cat f1.txt
v1
```

### 多次提交后回滚至指定提交的版本

2.3.2.9.1 git reset

git reset 官方说明

<https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%87%8D%E7%BD%AE%E6%8F%AD%E5%AF%86>

<https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified>

`git reset` 移动当前分支引用（分离 HEAD 状态下则移动 HEAD），并按选项决定是否重置索引与工作区。它不会“删除”提交对象，但原分支上的历史可能暂时不可见，可用 `git reflog` 找回。对已共享的分支通常不要直接改写历史。

```text
--soft  #工作目录和暂存区都不会被改变，只是本地仓库中的文件回滚到指定的版本，仅移动HEAD和
master指针的指向，不会重置暂存区或工作区
--mixed #默认选项。回滚暂存区和本地仓库，但工作目录不受影响
--hard  #本地仓库,暂存区和工作目录都回滚到指定的提交,该选项非常危险
```

![Git 与 GitLab 版本管理第 65 页插图](assets/img-1671afbf70c0e39a.webp)

回滚前的状态

![Git 与 GitLab 版本管理第 65 页插图](assets/img-c9f16bf381e53287.webp)

git reset --soft HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 66 页插图](assets/img-a5f4a5a99aa15353.webp)

git reset --mixed HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 67 页插图](assets/img-945e9f5e58cb0bcc.webp)

git reset --hard HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 68 页插图](assets/img-d8490e8f90160431.webp)

```bash
[root@gitlab testproject]#cat f1.txt
v1
[root@gitlab testproject]#git commit -m v1
[master (root-commit) 0cc266f] v1
1 file changed, 1 insertion(+)
create mode 100644 f1.txt
[root@gitlab testproject]#git status
On branch master
nothing to commit, working tree clean
[root@gitlab testproject]#echo v2 > f1.txt
[root@gitlab testproject]#git status
On branch master
Changes not staged for commit:
(use "git add <file>..." to update what will be committed)
(use "git checkout -- <file>..." to discard changes in working directory)
modified:   f1.txt
no changes added to commit (use "git add" and/or "git commit -a")
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git commit -m v2
[master 6fd0263] v2
1 file changed, 1 insertion(+), 1 deletion(-)
[root@gitlab testproject]#cat f1.txt
v2
[root@gitlab testproject]#git log
commit 6fd026348697f81baee6a1e3cb8032e39c5b073d (HEAD -> master)
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 10:00:27 2021 +0800
v2
commit 0cc266fec574873d01aa2e1c4d82bc9da3d6f61d
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 09:59:48 2021 +0800
v1
[root@gitlab testproject]#git reset --hard HEAD^
HEAD is now at 0cc266f v1
[root@gitlab testproject]#cat f1.txt
v1
[root@gitlab testproject]#git log
commit 0cc266fec574873d01aa2e1c4d82bc9da3d6f61d (HEAD -> master)
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 09:59:48 2021 +0800
v1
[root@gitlab testproject]#echo v2 > f1.txt
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git commit -m v2
[master 4a07d95] v2
1 file changed, 1 insertion(+), 1 deletion(-)
[root@gitlab testproject]#echo v3 > f1.txt
[root@gitlab testproject]#git add .
[root@gitlab testproject]#git commit -m v3
[master 0169b85] v3
1 file changed, 1 insertion(+), 1 deletion(-)
[root@gitlab testproject]#git log
commit 0169b85667f3f157659c88260facc36e201f7271 (HEAD -> master)
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 10:04:06 2021 +0800
v3
commit 4a07d953fcc779d9d0b05a7fd86f90259863c821
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 10:03:47 2021 +0800
v2
commit 0cc266fec574873d01aa2e1c4d82bc9da3d6f61d
Author: bowenxiaochun <root@bowenxiaochun.com>
Date:   Fri Sep 10 09:59:48 2021 +0800
v1
[root@gitlab testproject]#cat f1.txt
v3
#指定回滚至指定版本
[root@gitlab testproject]#git reset --hard 0cc266
HEAD is now at 0cc266f v1
[root@gitlab testproject]#cat f1.txt
v1
#无法查看到被回退前的历史版本
[root@gitlab testproject]#git log
#查看到被回退前的历史版本
[root@gitlab testproject]#git reflog
bf08d86 (HEAD -> master) HEAD@{0}: reset: moving to bf08d86aad95859e010a2cede7f
fd1592e HEAD@{1}: revert: Revert "chore: remove docker image scanning (#515)"
aa6581d: reset: moving to HEAD
```

范例:  回滚至指定CommitID 对应的版本

```bash
[root@ubuntu2204 ~]#git clone https://github.com/apache/apisix-docker.git
[root@ubuntu2204 ~]#cd apisix-docker/
[root@ubuntu2204 apisix-docker]#grep dashboard example/docker-compose.yml
- "./grafana_conf/dashboards:/var/lib/grafana/dashboards"
#查看commitid
[root@ubuntu2204 apisix-docker]#git log
commit aa6581dbbfa4e26dcf3f233e4a65f62ee4472d18 (HEAD -> master,
origin/release/apisix-3.7.0, origin/master, origin/HEAD)
Author: AlinsRan <alinsran@apache.org>
Date:   Thu Nov 23 18:02:03 2023 +0800
feat: release APISIX 3.7.0 (#521)
commit 8e3bf6f1ad0e9e1d4e3fca97bf3419cc24fbf690
Author: Gallardot <gallardot@apache.org>
Date:   Wed Nov 22 17:19:34 2023 +0800
doc: fix typo (#520)
commit 2f226c7b606b06f4b5a35a782d482998f21cd640
Author: Liu Wei <monkeydluffy6017@gmail.com>
Date:   Wed Nov 8 14:19:03 2023 +0800
feat: remove apisix-dashboard (#518)             #删除dashboard
commit 5720e8a520a34d7bf31a188576f4f3ea6ca07983
Author: Liu Wei <monkeydluffy6017@gmail.com>
Date:   Tue Nov 7 16:11:53 2023 +0800
feat: remove apisix-dashboard (#516)            #删除dashboard
commit bf08d86aad95859e010a2cede7f5c697a3f71e2e     #使用带有dashboard的版本
Author: Abhishek Choudhary <shreemaan.abhishek@gmail.com>
Date:   Mon Oct 16 14:05:48 2023 +0545
chore: remove docker image scanning (#515)
commit abab1e88077b869753029c2caf17d2210199c262
Author: Abhishek Choudhary <shreemaan.abhishek@gmail.com>
Date:   Fri Oct 13 09:00:20 2023 +0545
chore: remove centos based docker images (#512)
......
#回滚至指定commitid的版本
[root@ubuntu2204 apisix-docker]#git reset --hard bf08d86aad95859e0
#确认回滚成功
[root@ubuntu2204 apisix-docker]#grep dashboard example/docker-compose.yml
apisix-dashboard:
image: apache/apisix-dashboard:3.0.1-alpine
- ./dashboard_conf/conf.yaml:/usr/local/apisix-dashboard/conf/conf.yaml
- "./grafana_conf/dashboards:/var/lib/grafana/dashboards"
#查看日志
[root@ubuntu2204 apisix-docker]#git log
commit bf08d86aad95859e010a2cede7f5c697a3f71e2e (HEAD -> master)
Author: Abhishek Choudhary <shreemaan.abhishek@gmail.com>
Date:   Mon Oct 16 14:05:48 2023 +0545
chore: remove docker image scanning (#515)
commit abab1e88077b869753029c2caf17d2210199c262
Author: Abhishek Choudhary <shreemaan.abhishek@gmail.com>
Date:   Fri Oct 13 09:00:20 2023 +0545
chore: remove centos based docker images (#512)
commit 96e5b047b6ccf6a07d35506dbbb72db189491900
Author: Abhishek Choudhary <shreemaan.abhishek@gmail.com>
Date:   Sun Oct 8 08:03:47 2023 +0545
chore: remove unnecessary dependencies (#514)
commit 6ab8becc1482b30a9a88efe9099d62f3e1c709f4
Author: bowen Zhe <377762305@qq.com>
Date:   Sat Oct 7 14:30:06 2023 +0800
fix: update docker-compose-arm64 yaml (#475)
.......
```

2.3.2.9.2 git revert

如果我们修改了某些内容，已经commit到本地仓库，并且push到远程仓库了，这种情况下想把本地和远程仓库都回退到某个版本，该怎么做呢？

前面用git reset只是在本地仓库中回退版本，而远程仓库的版本不会变化，这样，即使本地reset了，但如果再次git pull，那么，远程仓库的内容又会和本地之前版本的内容进行merge，造成回退失败。

对于已经把代码push到远程仓库，你退回本地代码其实也想同时退回线上代码，回滚到某个指定的版本，线上线下代码保持一致。git revert用于撤销某次操作，此次操作之前和之后的commit和history都会保留，即用一个新提交来消除一个历史提交所做的任何修改。

revert之后你的本地代码会回滚到指定的历史版本，然后再git push。

![Git 与 GitLab 版本管理第 72 页插图](assets/img-20157a531a17674a.webp)

![Git 与 GitLab 版本管理第 73 页插图](assets/img-20157a531a17674a.webp)

git revert 用法

```text
git revert HEAD            #撤销前一次commit,会交互式打开文本编辑器提示输入提交信息
git revert HEAD --no-edit  #非交互式撤销前一次提交
git revert HEAD^  #撤销前前一次commit
git revert <commitid> #撤销指定的版本，撤销也会作为一次提交进行保存
```

reset和revert区别

```text
git revert是用一次新的commit来回滚之前的commit，git reset是直接删除指定的commit。
git reset是把HEAD向后移动了一下，而git revert是HEAD继续前进，只是新的commit的内容跟要
revert的内容正好相反，能够抵消要被revert的内容。
```

### 创建分支和合并分支

各种分支模型

![Git 与 GitLab 版本管理第 73 页插图](assets/img-dcf0b8bd4064fe61.webp)

```bash
#查看分支,默认只有master分支
[root@gitlab testproject]#git branch
* master
[root@gitlab testproject]#echo master data v1.0 > f1.txt
[root@gitlab testproject]#echo f2.txt > f2.txt
[root@gitlab testproject]#git commit -am 'add tow files'
#只创建分支不切换
[root@gitlab testproject]#git branch dev
#切换分支
[root@gitlab testproject]#git checkout  dev
#创建并切换新分支dev
[root@gitlab testproject]#git checkout -b dev
#查看分支
[root@gitlab testproject]#git branch
* dev
master
[root@gitlab testproject]#ls
f1.txt  f2.txt
[root@gitlab testproject]#cat f1.txt
master data v1.0
[root@gitlab testproject]#cat f2.txt
f2.txt
[root@gitlab testproject]#echo dev data v1.0 > f1.txt
[root@gitlab testproject]#git commit -am 'modify f1.txt'
#切换回原分支,修改数据
[root@gitlab testproject]#git checkout  master
[root@gitlab testproject]#echo f1.txt master data v2.0 > f1.txt
[root@gitlab testproject]#git commit -am "f1.txt v2.0"
[root@gitlab testproject]#git log  --pretty --oneline --graph --all
#效果如下
[root@ubuntu2204 myai]#git log  --pretty --oneline --graph --all
* 5fda12d (HEAD -> hotfix) hotfix v1.0
| * f08a4d3 (dev) dev v2.0
| * 92cb984 dev v1.0
|/
* 0806dbb (master) add syslog
* 8638e13 Revert "revert.go v3.0"
* e3083a2 revert.go v3.0
* df9d9a4 revert.go v2.0
* c18b0e0 revert.go v1.0
* 12ed600 world.go v2.0
* caf2c0d world.go v1.0
* e9f873e add bowen.java
* be16fce create .gitignore
* 3445c7f new feature
* 2931df4 myai init
```

```bash
# 以下两个分支都修改了 f1.txt，因此是可能发生冲突的三路合并，不是快进式合并。
[root@gitlab testproject]#git checkout dev
#合并master分支到当前分支dev
#交互式合并
[root@gitlab testproject]#git merge master
#或者非交互式
[root@gitlab testproject]#git merge master -m "merge master"  # 与上一行择一
[root@gitlab testproject]#cat f1.txt
<<<<<<< HEAD
f1.txt dev data v1.0
=======
f1.txt master data v2.0
>>>>>>> master
#合并分支效果如下
[root@ubuntu2204 myai]#git log  --pretty --oneline --graph --all
* fc2b988 (master, hotfix) hotfix v2.0
* 5fda12d hotfix v1.0
| * f08a4d3 (HEAD -> dev) dev v2.0
| * 92cb984 dev v1.0
|/
* 0806dbb add syslog
* 8638e13 Revert "revert.go v3.0"
* e3083a2 revert.go v3.0
* df9d9a4 revert.go v2.0
* c18b0e0 revert.go v1.0
* 12ed600 world.go v2.0
* caf2c0d world.go v1.0
* e9f873e add bowen.java
* be16fce create .gitignore
* 3445c7f new feature
* 2931df4 myai init
```

```bash
#三路合并：平行分支(有多次独立的提交的多个分支)中因为不同分支中同一个文件内容不同,会出现冲突,需
要手动解决冲突,并重新add和commit
[root@gitlab testproject]#git merge master
Auto-merging f1.txt
CONFLICT (content): Merge conflict in f1.txt
Automatic merge failed; fix conflicts and then commit the result.
自动合并 f1.txt
冲突（内容）：合并冲突于 f1.txt
自动合并失败，修正冲突然后提交修正的结果
```

```bash
#提示合并冲突，查看文件冲突的信息，提示git merge --abort 取消合并或者修改冲突在的文件来解决冲
突
[root@gitlab testproject]#git status
#修改文件，自行解决冲突
[root@gitlab testproject]#vim f1.txt
[root@gitlab testproject]#cat f1.txt
f1.txt dev data v1.0
f1.txt master data v2.0
[root@gitlab testproject]#git add f1.txt
[root@gitlab testproject]#git commit -m 'merge master'
[root@gitlab testproject]#git log --pretty=oneline  --graph --all
#合并效果如下
[root@ubuntu2204 myai]#git log  --pretty --oneline --graph --all
*   c2d6615 (HEAD -> master) merge dev2.0
|\
| * f08a4d3 (dev) dev v2.0
| * 92cb984 dev v1.0
* | fc2b988 (hotfix) hotfix v2.0
* | 5fda12d hotfix v1.0
|/
* 0806dbb add syslog
* 8638e13 Revert "revert.go v3.0"
* e3083a2 revert.go v3.0
* df9d9a4 revert.go v2.0
* c18b0e0 revert.go v1.0
* 12ed600 world.go v2.0
* caf2c0d world.go v1.0
* e9f873e add bowen.java
* be16fce create .gitignore
* 3445c7f new feature
* 2931df4 myai init
```

### 修改分支名称

```bash
[root@gitlab testproject]#git branch
dev
* master
[root@gitlab testproject]#git checkout dev
Switched to branch 'dev'
#修改当前分支名称为devel
[root@gitlab testproject]#git branch -M devel
[root@gitlab testproject]#git branch
* devel
master
```

### 当前状态打 tag 并利用 tag 回滚

```bash
[root@gitlab testproject]#echo v1.0 > a.txt;git add .;git commit -m v1.0
[main 0fba09a] v1.0
1 file changed, 1 insertion(+)
[root@gitlab testproject]#git tag v1.0
[root@gitlab testproject]#git tag
v1.0
[root@gitlab testproject]#echo v2.0 > a.txt;git add .;git commit -m v2.0
[main f0153a6] v2.0
1 file changed, 1 insertion(+), 1 deletion(-)
[root@gitlab testproject]#git tag v2.0
[root@gitlab testproject]#git tag
v1.0
v2.0
[root@gitlab testproject]#git show v1.0
commit 0fba09a8319f4c671be711f863ae12d44fd451a9 (tag: v1.0)
Author: bowenxiaochun <29308620@qq.com>
Date:   Tue Feb 02 23:11:02 2020 +0800
v1.0
diff --git a/a.txt b/a.txt
index e69de29..6b3126c 100644
--- a/a.txt
+++ b/a.txt
@@ -0,0 +1 @@
+v1.0
[root@gitlab testproject]#git reset --hard v1.0
HEAD is now at 0fba09a v1.0
[root@gitlab testproject]#cat a.txt
v1.0
```

### 本地代码提交给公有云仓库码云

国内公有云仓库

<https://gitee.com/>

注意: 新建仓库时,选择不初始化仓库

![Git 与 GitLab 版本管理第 77 页插图](assets/img-45ed136d66627554.webp)

```bash
#在本机创建项目
[root@centos8 ~]#mkdir -p /data/myapp && cd /data/myapp
[root@centos8 myapp]#git init
[root@centos8 myapp]#git config --global user.name "bowenxiaochun"
[root@centos8 myapp]#git config --global user.email "29308620@qq.com"
[root@centos8 myapp]#echo Hello,git > hello.txt
[root@centos8 myapp]#git add .
[root@centos8 myapp]#git commit -m "v1.0"
#先注册并登录码云,创建名称为myapp的未初始化的空仓库后,可以执行下面操作建立本地仓库和远程码云的
联系
[root@centos8 myapp]#git remote add origin https://gitee.com/lbtooth/myapp.git
# 先确认当前分支名；以下示例将 main 推送为远程 master
[root@centos8 myapp]#git branch --show-current
[root@centos8 myapp]#git push -u origin main:master
Username for 'https://gitee.com': bowenxiaochun
Password for 'https://lbtooth@gitee.com': <访问令牌或平台要求的凭据>
[root@centos8 myapp]#git remote
origin
[root@centos8 myapp]#git remote -v
origin  https://gitee.com/lbtooth/myapp.git (fetch)
origin  https://gitee.com/lbtooth/myapp.git (push)
#和码云同步至本地
[root@centos8 myapp]#git pull origin master
#再次提交
[root@centos8 myapp]#echo Hello2,git >> hello.txt
[root@centos8 myapp]#git add .
[root@centos8 myapp]#git commit -m "v2.0"
#查看日志
[root@centos8 myapp]#git log --oneline
#push到远程仓库，再次查看日志
[root@centos8 myapp]#git push -u origin main:master
[root@centos8 myapp]#git log --oneline
#删除关联
[root@centos8 myapp]#git remote remove origin
[root@centos8 myapp]#git remote -v
#从远程仓库拉取代码
[root@ubuntu2204 myapp]#git remote -v
origin  https://gitee.com/lbtooth/myapp.git (fetch)
origin  https://gitee.com/lbtooth/myapp.git (push)
[root@ubuntu2204 myapp]#git pull
#默认只能看到当前分支
[root@ubuntu2204 myapp]#git branch
* master
#查看所有分支，包括远程分支
[root@ubuntu2204 myapp]#git branch -a
* master
remotes/origin/HEAD -> origin/master
remotes/origin/devel
remotes/origin/hotfix
remotes/origin/master
#切换至指定分支
[root@ubuntu2204 myapp]#git checkout devel
Branch devel set up to track remote branch devel from origin.
Switched to a new branch 'devel'
#可以看到分支在本地生成，并可以看到分支里的文件
[root@ubuntu2204 myapp]#git branch
* devel
master
```

### 访问远程仓库时的网络诊断

远程访问失败时，先用 `git remote -v` 核对仓库地址，再确认 DNS、HTTPS/SSH 连通性和所需权限。不要把访问令牌嵌入 URL 或命令行：它可能留在终端历史、进程列表或日志中。

如果所在网络需要组织提供的代理，可按网络管理员给出的地址配置 Git，例如：

```bash
git config --global http.proxy http://<代理主机>:<端口>
git config --global --get http.proxy
# 不再需要时撤销
git config --global --unset http.proxy
```

第三方镜像或下载中转站可能不完整、不同步，也可能改变信任边界。特别是私有仓库和安装包，优先使用受信任的官方地址，并核验来源与校验值。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/08-installing-git.html' | relative_url }}">← 上一篇：Git 安装</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/10-public-cloud-repositories.html' | relative_url }}">下一篇：公有云仓库 →</a>
</nav>
