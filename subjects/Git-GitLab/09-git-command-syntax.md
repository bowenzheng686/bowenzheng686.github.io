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

![Git 与 GitLab 版本管理第 53 页插图](assets/img-0cf22fd127fa17c6.png)

区域间文件操作

![Git 与 GitLab 版本管理第 53 页插图](assets/img-2bc00c18e07eea77.png)

git 命令常见用法

```text
#查看git及子命令的帮助
git help <子命令> #不加<子命令>是查看git命令的帮助
git <子命令> --help #不加<子命令>是查看git命令的帮助
man git-<子命令>
git version  #查看版本
git init       #本地仓库初始化
git init --initial-branch=main  #初始化主分支为main，默认为master,注意:此为新版用法
git init --bare #创建无工作区的祼仓库,适用于充当远程仓库,一般对应的目录以.git为后缀
git clone <repository_url>  [workdir]      #克隆url指定的项目的所有分支和标签对应文件到
指定目录（默认为当前目录）,并在本地创建此项目的git仓库，默认只显示master分支，而不晃示其它支
支，但可以执行git checkout 分支，即可查看到其它分支的文件
git clone -b develop <repository_url>      #克隆url指定的项目,并切换到develop分支
git clone -b tag <repository_url>          #克隆url指定的项目，并切换到指定的tag
git config --global user.name "bowenxiaochun" #设置当前用户的git全局用户名,和下面两项都
存放在~/.gitconfig文件中
git config --global user.email "29308620@qq.com" #设置全局邮箱
git config --global color.ui true   #让Git显示颜色，会让命令输出看起来更醒目
git config --global core.editor vim #git默认的编辑器为nano，不常用，需要修改为vim
git config --global --list|-l  #列出用户全局设置,默认保存在~/.gitconfig文件中
git config --global -e #交互编辑配置
#文件操作
git add index.html / . #添加指定文件、目录或当前目录下所有数据到暂存区
git mv file_oldname file_newname    #将已经进入版本仓库的文件改名，注意：不支持在工作区没
有存入暂存区的新创建的文件
git rm --cached file   #只删除暂存区的文件,不删除工作区文件,相当于git add 反操作，和git
restore --staged 功能相同
git rm  file           #从删除工作目录和暂存区删除文件
git checkout file      #从暂存区复制文件到工作目录
git restore --staged <file>     #新版EXPERIMENTAL命令,撤销add到暂存区的文件回到工作区，
重新成为untracked状态
git restore <file>     #撤消已跟踪但尚未加入暂存区中的文件变更，撤消了工作区中文件的所有新的
更改
git restore -s <commitid> <pathspec>  #从某个提交中恢复文件
#示例：从前一次提交中恢复README.md文件：git
restore -s HEAD~ READEME.md
#查看文件列表和内容
git ls-files           #查看暂存区文件,选项-s显示mode bits, object name and stage
number,-o显示untracked文件
git cat-file -p <blogid>  #查看仓库对象的内容,仓库对象存放在.git/objects目录下
#查看文件变化
git diff [<path>...]                            #对比工作区和暂存区的区别
git diff --staged|cached  [<path>...]           #对比暂存区和本地仓库的前一次提交的区别
git diff --cached <commit> [<path>...]          #对比暂存区与指定的提交
git diff [<commit>] [--] [<path>...]            #对比工作区和指定提交的文件的区别
git diff <commit>...<commit> [--] [<path>...]   #提交和提交之间的文件的区别
#提交
git commit -m  “comment“         #提交文件到工作区
git commit -am "comment"         #添加所有修改(不包括新文件)到暂存区并提交,相当于git add
+ git commit
git commit --amend --no-edit     #重新覆盖上次的提交
git commit --amend -m "comment"  #重新提交,覆盖上次的提交
git show [HEAD]                   #查看最近一次提交的详细信息,即查看HEAD当前所指向的
commit的信息
#查看日志
git status #查看工作区的状态
git log #查看提交日志
git log --oneline #查看提交日志的简要信息，一个提交一行，只显示commit id的前七位
git log --oneline -N  #查看最近N条commit日志
git log  --pretty=oneline #查看提交日志的简要信息，一个提交一行，显示commit id 全部位
git log  --pretty=raw     #查看提交信息，包括对应的tree对象，父提交，作者等
git log --stats #查看提交的文件的统计信息
git log -p [commit_id] #查看指定提交和之前提交的变化详细信息
git log --author="<author-name-pattern>" #查看指定作者的提交
git log <file-pattern> #查看指定文件的提交
git log origin/main  #查看远程仓库的日志
git reflog  #查看分支或其它引用在本地仓库的完整历史记录
#回滚提交，本质上是将HEAD和master引用移到指定的commit上，是否基于指定的commit连同重置暂存区
和工作区则取决于使用的选项
git reset --hard|soft|minxed HEAD^^ #git版本回滚， HEAD为当前版本，加一个^为上一个，^^
为上上一个版本，也可以将^换成~
git reset --hard|soft|minxed HEAD~n #回滚前n个版本，0表示当前commit，~或者~1表示前一个
commit,即相当于HEAD^
git reset --hard|soft|minxed 5ae4b06 #回退到指定id的版本,使用 git reflog 获取每次提交
的ID
git reset --hard|soft|minxed v1.0    #支持tag,此处的v1.0为tag
#分支管理
git branch #查看分支及当前所处的分支
git branch -av #查看所有本地和远程分支
git branch <分支名> #创建分支<分支名>
git branch <分支名> <commit_id> #基于指定提交创建新分支
git branch -d <分支名>  #删除分支
git branch -m dev develop #修改分支名dev为develop
git branch -M main #修改当前分支名称为main
git branch -r      #列出所有远程分支
#切换分支
git checkout <分支名>    #切换到已有的分支，HEAD也会自动指向目标分支上的最新提交
git checkout <tag>     #切换至指定标签，检出到标签，会导致分离头指针，且新创建的提交也将处于
分离的状态
git checkout -b <分支名> #创建并切换到一个新分支
git checkout -b <分支名> origin/<分支名> #利用服务器远程仓库的分支，同步在本地创建分支
git checkout [<commit>]-- <file> ...  #找回在工作区删除的已存入暂存区或提交的文件
git merge master -m  <message>  #将master分支合并至当前分支,无选项-m, 则为交互式输入信息
git merge orgin/<branch_name>   #将远程分支合并到本地当前分支，通常应该将存在映射关系（通
常为同一个分支名称）的分支进行合并
git merge --abort     #取消合并
git switch <branchname>    #切换分支.是Git 2.23 版本引入的新命令,git switch 是一个只专
注于分支切换的命令，而 git checkout 则是一个历史更久,有更多的用途。除了切换分支外，git
checkout 还可以用于还原文件、切换到特定的提交、创建新的分支等更通用的命令
git switch -c <new-branch>      #切抽并创建分支,相当于git branch <new-branch> && git
switch <new-branch>
#标签
git tag <tagname>                          #当前commit创建轻量标签
git tag <tagname>  <commit_id>             #将指定commit创建轻量标签
git tag -a <tagname>  -m <message>         #将当前commit创建附注标签
git tag -a <tagname>  -m <message> <commit_id>  #将指定commit创建附注标签
git tag -d <tagname>                    #删除标签
git reset --hard <tagname>              #回滚到指定标签
git tag                                 #查看标签
git tag -l [<pattern>]                  #查看指定模式的标签
git show <tagname>                      #查看指定标签详细信息
#远程仓库
git remote -v #查看远程仓库
git remote show <remote_name> #查看远程仓库详细信息，<remote_name>默认origin
git remote add <remote_name> <url> #创建远程仓库，<remote_name> 默认为origin
git remote add origin git@gitlab.example.com:testgroup/testproject.git #建立远程仓
库和本地origin关联
git remote rename origin new-origin  #修改默认远程仓库名称origin为新的名称new-origin
git remote remove|rm origin #删除远程仓库的关联
#和远程仓库推和位
git push #将本地仓库提交代码到远程服务器
git push <remote_name> <branch_name> #推送指定分支到指定的远程仓库
git push origin master #将本地master分支推送到远程的 master 分支,和当前分支是否为master
分支无关
git push origin dev    #将本地dev分支推送到远程的dev分支,如果远程没有dev会自动创建,和当前
分支是否为dev分支无关
git push -u|--set-upstream origin master #将本地master分支推送到远程仓库master,-u表示
以后可用git push 代替此命令
git push origin main:dev #将本地main分支推送至远程dev分支
git push origin :dev #将空分支推送到远程dev,即删除远程dev分支
git push <remote_name> --all #推送本地仓库的的所有有分支到远程
git push -u origin --all     #推送所有分支
git push origin <tagname>       #推送本地仓库指定的tag到远程
git push origin --tag <tagname> #推送本地仓库指定的tag到远程
git push <remote_name> --tags          #将本地仓库所有的tag都推送到远程,默认不会推送标签
git push --delete origin <tagname> #删除远程仓库的标签
git pull               #从远程服务器获取所有分支的代码到本地仓库,并自动合并到本地仓库和工作
区
git pull <remote_name> #拉取并合并远程分支变更到当前分支，相当于git fetch <remote_name>
和git merge <remote_name>
git pull origin dev    #从远程服务器指定的分支dev拉取代码到本地仓库,并自动合并到本地仓库和
工作区
git fetch <remote_name> #获取远程仓库所有分支上的变更
git fetch <remote_name>   <branch_name> #获取远程仓库指定分支上的变更，但不合并
git fetch origin master #从远程仓库origin的master分支获取最新版本到本地仓库,但不合并至工
作区，需要手动完成合并
#忽略文件，实现不跟踪指定文件
vim .gitignore #定义忽略文件，即不放在仓库的文件
```

git log 显示日志格式

```text
git log --graph --pretty=format:'参数'
```

参数说明

参数说明

%H commit hash

%h commit short hash

%T tree hash

%t tree short hash

%P parent hash

%p parent short hash

%an 作者名字

%aN .mailmap 中对应的作者名字

%ae 作者邮箱

%aE .mailmap 中对应的作者邮箱

%ad –date=制定的日期格式

%aD RFC2822 日期格式

%ar 日期格式，例如：1 day ago

%at UNIX timestamp 日期格式

%ai ISO 8601 日期格式

%cn 提交者名字

%cN .mailmap 对应的提交的名字

%ce 提交者邮箱

%cE .mailmap 对应的提交者的邮箱

%cd –data=制定的提交日期的格式

%cD RFC2822 提交日期的格式

%cr 提交日期的格式，例如：1day ago

%ct UNIX timestamp 提交日期的格式

%ci ISO 8601 提交日期的格式

%d ref 名称

%e encoding

%s commit 信息标题

%f 过滤 commit 信息的标题使之可以作为文件名

%b commit 信息内容

%N commit notes 参数说明

%gD reflog selector, e.g., refs/stash@{1}

%gd shortened reflog selector, e.g., stash@{1}

%gs reflog subject

%Cred 切换至红色

%Cgreen 切换至绿色

%Cblue 切换至蓝色

%Creset 重设颜色

%C(color) 制定颜色，as described in color.branch.* config option

%m left right or boundary mark

%n 换行

%% a raw %

%x00 print a byte from a hex code

%w([[,[,]]]) switch line wrapping, like the -w option of git-shortlog(1).

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
#设置git，提交commit之前需要先配置git的基本信息
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
[root@gitlab ~]#git config --global user.email root@bowenxiaochun.com
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
user.email=root@bowenxiaochun.com
core.editor=vim
core.ui=true
[root@gitlab ~]#cat .gitconfig
[user]
name = bowenxiaochun
email = 29308620@qq.com
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

如果工作区和暂存区数据不一致,会显示红色的提示

![Git 与 GitLab 版本管理第 60 页插图](assets/img-d7818a44bdd480c4.png)

如果暂存区和本地仓库数据不一致,会显示绿色的提示

![Git 与 GitLab 版本管理第 60 页插图](assets/img-eb1a5903b7d34bd5.png)

### 设置忽略文件

配置.gitignore文件让 Git 不再管理当前目录下的某些文件。

生产中有如下几类文件可能需要忽略

程序运行时产生的临时文件程序连接数据库这一类的配置文件程序本地开发使用的图片文件其它不想被共享的文件

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
*.py[c|x]
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
[root@gitlab testproject]#git restore --staged f1.txt
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
[root@rocky8 testproject]#file
.git/objects/48/71fd52755be519c29ae719f385bd5f2863627c
.git/objects/48/71fd52755be519c29ae719f385bd5f2863627c: VAX COFF executable -
version 20741
[root@rocky8 testproject]#git cat-file -t
4871fd52755be519c29ae719f385bd5f2863627
blob
[root@rocky8 testproject]#git cat-file -p
4871fd52755be519c29ae719f385bd5f2863627c
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
[root@gitlab testproject]#git checkout test.txt
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

git reset 是对本地仓库的项目进行回滚操作的命令，它主要有如下三个参数

```text
--soft  #工作目录和暂存区都不会被改变，只是本地仓库中的文件回滚到指定的版本，仅移动HEAD和
master指针的指向，不会重置暂存区或工作区
--mixed #默认选项。回滚暂存区和本地仓库，但工作目录不受影响
--hard  #本地仓库,暂存区和工作目录都回滚到指定的提交,该选项非常危险
```

![Git 与 GitLab 版本管理第 65 页插图](assets/img-1671afbf70c0e39a.png)

回滚前的状态

![Git 与 GitLab 版本管理第 65 页插图](assets/img-c9f16bf381e53287.png)

git reset --soft HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 66 页插图](assets/img-a5f4a5a99aa15353.png)

git reset --mixed HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 67 页插图](assets/img-945e9f5e58cb0bcc.png)

git reset --hard HEAD~ 执行的效果

![Git 与 GitLab 版本管理第 68 页插图](assets/img-d8490e8f90160431.png)

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

![Git 与 GitLab 版本管理第 72 页插图](assets/img-20157a531a17674a.jpeg)

![Git 与 GitLab 版本管理第 73 页插图](assets/img-20157a531a17674a.jpeg)

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

![Git 与 GitLab 版本管理第 73 页插图](assets/img-dcf0b8bd4064fe61.png)

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
#快进式合并：切换分支至dev分支，此分支为被合并的目标分支
[root@gitlab testproject]#git checkout dev
#合并master分支到当前分支dev
#交互式合并
[root@gitlab testproject]#git merge master
#或者非交互式
[root@gitlab testproject]#git merge master -m "merge master"
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
[root@gitlab testproject]#git commit -am 'merge master'
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

![Git 与 GitLab 版本管理第 77 页插图](assets/img-45ed136d66627554.png)

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
#将本地main分支推送至码云的master分支
[root@centos8 myapp]#git push -u origin main:master
Username for 'https://gitee.com': bowenxiaochun
Password for 'https://lbtooth@gitee.com': 123456
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
[root@centos8 myapp]#git log --online
#push到远程仓库，再次查看日志
[root@centos8 myapp]#git push -u origin main:master
[root@centos8 myapp]#git log --online
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

### github 代理

github 从国内访问可能会失败,可以利用代理访问

2.3.2.14.1 代理1

```text
将 https://github.com/ 修改为 https://githubfast.com/，其它不变，再下载
```

范例

```bash
[root@ubuntu2204 ~]#wget
https://github.com/stilleshan/dockerfiles/archive/master.zip
Connecting to github.com (github.com)|20.205.243.166|:443... failed: Connection
refused.
#修改链接地址为githubfast
[root@ubuntu2204 ~]#wget
https://githubfast.com/stilleshan/dockerfiles/archive/master.zip
--2025-04-10 20:54:01--
https://githubfast.com/stilleshan/dockerfiles/archive/master.zip
HTTP request sent, awaiting response... 200 OK
Length: unspecified [application/zip]
Saving to: ‘master.zip’
master.zip                           [        <=>                      ]   2.76M
1.87MB/s    in 1.5s
```

2.3.2.14.2 代理2

<https://ghproxy.com/>

![Git 与 GitLab 版本管理第 79 页插图](assets/img-3df53f464157ceca.png)

```bash
#访问格式
git clone
https://mirror.ghproxy.com/https://github.com/your_name/your_private_repo
#git clone 私有仓库
git clone
https://user:your_token@mirror.ghproxy.com/https://github.com/your_name/your_pri
vate_repo
#wget & curl
wget
https://mirror.ghproxy.com/https://github.com/stilleshan/dockerfiles/archive/mas
ter.zip
wget
https://mirror.ghproxy.com/https://raw.githubusercontent.com/stilleshan/dockerfi
les/main/README.md
curl -O
https://mirror.ghproxy.com/https://github.com/stilleshan/dockerfiles/archive/mas
ter.zip
curl -O
https://mirror.ghproxy.com/https://raw.githubusercontent.com/stilleshan/dockerfi
les/main/README.md
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/08-installing-git.html' | relative_url }}">← Previous: Installing Git</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">Back to Git and GitLab Version Control Index</a>
  <a href="{{ '/subjects/Git-GitLab/10-public-cloud-repositories.html' | relative_url }}">Next: Public Cloud Repositories →</a>
</nav>
