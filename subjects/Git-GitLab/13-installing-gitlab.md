---
layout: default
title: "Git 与 GitLab 版本控制 · GitLab 安装"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 13 GitLab 安装

GitLab 有不同发行版本和订阅层级。本篇旧实验使用 GitLab CE 软件包；实际安装前应以目标 GitLab 版本的官方安装说明核对操作系统、数据库、内存和升级路径，不能直接照搬旧版包名。

### 安装方法

Gitlab 服务的安装文档：

<https://docs.gitlab.com/install/>

安装方式包括 Linux 软件包、容器和 Kubernetes Helm Chart；下面先以单机 Linux 包为主线。其他方式的维护与备份策略不同，不应混用命令。

<https://docs.gitlab.com/ee/install/install_methods.html>

| 方式 | 适用场景 |
| --- | --- |
| Linux 软件包（Omnibus） | 单机或自管理部署，打包 Web、数据库和后台服务。 |
| Docker 容器 | 已有容器运维能力，需持久化配置、日志和数据目录。 |
| Kubernetes Helm Chart | 集群化部署，需额外规划存储、Ingress、证书和升级。 |
| 源码安装 | 特殊平台或开发场景，维护成本较高。 |

### 安装 GitLab 要求

Gitlab硬件和软件的环境要求：

<https://docs.gitlab.com/ce/install/requirements.html>

硬件配置要求较高：

实验环境可能需要数 GiB 内存；生产容量应根据 GitLab 版本、用户数、仓库量、CI 作业和监控组件单独规划。原文中的“2 核、8 GiB、10 GiB 磁盘”不是通用最低规格，尤其磁盘应为仓库增长和备份保留预留空间。

注意:如果内存较低,可以会导致Gitlab有些服务无法启动,建议4G以上内存

![Git 与 GitLab 版本管理第 94 页插图](assets/img-df7afd80c9545aad.webp)

数据库要求:

从GitLab 12.1 开始Linux包安装不再支持MySQL,只支持PostgreSQL

![Git 与 GitLab 版本管理第 94 页插图](assets/img-f56b96c7d7609111.webp)

### 安装前准备

### Ubuntu 系统环境安装前准备

配置ubuntu 仓库

旧实验以 Ubuntu 18.04 的 `bionic` 软件源为例，该系统已过常规支持期。不要把下面源列表复制到其他 Ubuntu 版本；新部署应使用受支持发行版与其匹配的软件源。

旧版 Ubuntu 软件源示例中的发行代号和行内换行均不可直接执行。准备新环境时，先检查 `cat /etc/os-release`，再按该版本的官方说明配置软件源；安装包必须与系统发行版和架构匹配。

### RHEL 系统环境安装前准备

先设置可解析的主机名、时间同步、存储和必要端口策略。**安装 GitLab 不要求关闭防火墙或 SELinux**；应按官方文档开放所需端口并保持安全机制启用。以下旧实验中的 `disable firewalld` 和 `SELINUX=disabled` 不适合作为推荐步骤。

```bash
[root@centos ~]# hostnamectl set-hostname gitlab.example.com
[root@centos ~]# getent hosts gitlab.example.com
```

### GitLab 安装

gitlab 安装有多种方式,下面选择包安装方式

<https://docs.gitlab.com/ce/install/>

![Git 与 GitLab 版本管理第 96 页插图](assets/img-92c8ba7cec97243f.webp)

### 安装 GitLab

官方gitlab 包下载链接

<https://packages.gitlab.com/gitlab>

![Git 与 GitLab 版本管理第 96 页插图](assets/img-4704661e557575f8.webp)

GitLab-CE 安装包官方下载地址：

<https://packages.gitlab.com/gitlab/gitlab-ce>

yum源清华大学下载地址：

<https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/>

CentOS 的yum源

![Git 与 GitLab 版本管理第 97 页插图](assets/img-e8843e73f4236029.webp)

Ubuntu 的deb源

<https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu/pool/>

![Git 与 GitLab 版本管理第 97 页插图](assets/img-1e396d27d8dd917e.webp)

范例：Ubuntu 国内镜像下载并安装 GitLab

```bash
#新版下载和安装
[root@ubuntu2204 ~]#wget 'https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu/pool/jammy/main/g/gitlab-ce/gitlab-ce_17.3.1-ce.0_amd64.deb'
#旧版
[root@ubuntu1804 ~]#wget 'https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu/pool/bionic/main/g/gitlab-ce/gitlab-ce_14.1.0-ce.0_amd64.deb'
#方法1
[root@ubuntu1804 ~]#dpkg -i gitlab-ce_14.1.0-ce.0_amd64.deb
#方法2
[root@ubuntu2204 ~]#apt install ./gitlab-ce_17.3.1-ce.0_amd64.deb
#旧版下载和安装
[root@ubuntu1804 ~]#wget 'https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/ubuntu/pool/bionic/main/g/gitlab-ce/gitlab-ce_11.11.8-ce.0_amd64.deb'
[root@ubuntu1804 ~]#dpkg -i gitlab-ce_11.11.8-ce.0_amd64.deb
```

![Git 与 GitLab 版本管理第 98 页插图](assets/img-8947a774be4c2287.webp)

### 修改 GitLab 配置

gitlab相关的目录：

```text
/etc/gitlab #配置文件目录，重要
/var/opt/gitlab #数据目录,源代码就存放在此目录,重要
/var/log/gitlab #日志目录
/run/gitlab #运行目录,存放很多的数据库文件
/opt/gitlab #安装目录
```

范例： gitlab 初始化配置

```bash
[root@ubuntu1804 ~]#vim /etc/gitlab/gitlab.rb
[root@ubuntu1804 ~]#grep '^external_url' /etc/gitlab/gitlab.rb
external_url 'https://gitlab.example.com'   # 与证书和 DNS 保持一致
#可选,实现邮件通知设置,增加下面行(可以和上面行写在一起)
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.qq.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "29308620@qq.com"
gitlab_rails['smtp_password'] = "授权码"
gitlab_rails['smtp_domain'] = "qq.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = true
gitlab_rails['gitlab_email_from'] = "29308620@qq.com"
#可选
nginx['listen_port']=8080  #修改nginx代理监听的端口
gitlab_sshd['enable']=true  #是否启用sshd服务
gitlab_sshd['listen_address']='0.0.0.0:2222'#ssh协议端口,地址
ssh://git@gitlab.bowen.org:2222/example/app.git
#新版中增加下面行,给root用户指定初始密码才能登录，或者设置环境变量GITLAB_ROOT_PASSWORD实现初
始密码
#注意:密码至少8位并且复杂度要求才是有效密码
# 初始密码交由安装流程的受控机制管理，不把固定明文密码写进示例配置。
#名称解析
[root@ubuntu1804 ~]#vim /etc/hosts
192.0.2.100 gitlab.example.com
```

由于 Gitlab 主机功能是代码托管，默认有些额外的组件比较消耗资源，如果暂时不使用可以考虑关闭

范例:  将不需要使用的组件都设定为false

```text
vim /etc/gitlab/gitlab.rb
prometheus['enable'] = false
prometheus['monitor_kubernetes'] =false
alertmanager['enable'] = false
node_exporter['enable'] = false
redis_exporter['enable'] = false
postgres_exporter['enable'] = false
gitlab_exporter['enable'] = false
prometheus_monitoring['enable'] =false
grafana['enable'] = false
```

### 初始化和启动服务

执行配置reconfigure并启动服务：

```bash
#每次修改完配置文件都需要执行此操作
[root@ubuntu1804 ~]#gitlab-ctl reconfigure
```

![Git 与 GitLab 版本管理第 100 页插图](assets/img-b7efcc2d8430b44b.webp)

### 验证 GitLab 启动完成

```bash
#新版服务
[root@ubuntu1804 ~]#gitlab-ctl status
run: alertmanager: (pid 12495) 73s; run: log: (pid 12138) 144s
run: gitaly: (pid 12374) 76s; run: log: (pid 11439) 257s
run: gitlab-exporter: (pid 12388) 76s; run: log: (pid 11915) 163s
run: gitlab-workhorse: (pid 12349) 77s; run: log: (pid 11840) 181s
run: grafana: (pid 12514) 73s; run: log: (pid 12286) 96s
run: logrotate: (pid 11357) 270s; run: log: (pid 11365) 269s
run: nginx: (pid 11846) 177s; run: log: (pid 11860) 176s
run: node-exporter: (pid 12363) 76s; run: log: (pid 11898) 170s
run: postgres-exporter: (pid 12507) 73s; run: log: (pid 12164) 140s
run: postgresql: (pid 11570) 252s; run: log: (pid 11585) 249s
run: prometheus: (pid 12397) 75s; run: log: (pid 11960) 152s
run: puma: (pid 11754) 196s; run: log: (pid 11762) 193s
run: redis: (pid 11387) 264s; run: log: (pid 11395) 263s
run: redis-exporter: (pid 12390) 75s; run: log: (pid 11936) 157s
run: sidekiq: (pid 11772) 190s; run: log: (pid 11786) 187s
```

```bash
#旧版服务
[root@ubuntu1804 ~]#gitlab-ctl status
run: alertmanager: (pid 29801) 117s; run: log: (pid 29411) 135s
run: gitaly: (pid 29575) 120s; run: log: (pid 28084) 222s
run: gitlab-monitor: (pid 29659) 119s; run: log: (pid 29196) 151s
run: gitlab-workhorse: (pid 29616) 120s; run: log: (pid 28848) 173s
run: logrotate: (pid 28923) 166s; run: log: (pid 29008) 163s
run: nginx: (pid 28851) 172s; run: log: (pid 28902) 169s
run: node-exporter: (pid 29638) 119s; run: log: (pid 29107) 157s
run: postgres-exporter: (pid 29817) 116s; run: log: (pid 29479) 131s
run: postgresql: (pid 28231) 217s; run: log: (pid 28266) 214s
run: prometheus: (pid 29767) 118s; run: log: (pid 29335) 139s
run: redis: (pid 27937) 229s; run: log: (pid 27974) 227s
run: redis-exporter: (pid 29668) 118s; run: log: (pid 29258) 145s
run: sidekiq: (pid 28742) 180s; run: log: (pid 28797) 177s
run: unicorn: (pid 28653) 186s; run: log: (pid 28698) 183s
```

### 验证端口及状态

80端口是在初始化gitlib的时候启动的，因此如果之前有程序占用了相关端口,就会导致初始化失败或无法访问

```bash
[root@ubuntu1804 ~]#lsof -i :80
COMMAND   PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   28851       root    7u  IPv4  88801      0t0  TCP *:http (LISTEN)
nginx   28852 gitlab-www    7u  IPv4  88801      0t0  TCP *:http (LISTEN)
nginx   28853 gitlab-www    7u  IPv4  88801      0t0  TCP *:http (LISTEN)
```

### Gitlab的常用命令

GitLab除了使用Web界面进行管理，还提供了各组件的统一命令为gitlab-ctl，此外还有一些各组件专用的命令，如gitlab-pgsql、 gitlab-rails和gitlab-rake等

```text
#客户端命令行操作行
gitlab-ctl
gitlab-ctl check-config #检查配置
gitlab-ctl show-config  #查看配置
gitlab-ctl reconfigure  #修改过配置后需要执行重新配置
gitlab-ctl stop         #停止gitlab
gitlab-ctl start        #启动gitlab
gitlab-ctl restart      #重启gitlab
gitlab-ctl status       #查看组件运行状态
gitlab-ctl tail         #查看所有日志
gitlab-ctl tail nginx   #查看某个组件的日志
gitlab-ctl service-list #列出服务
#其它命令
gitlab-rails #用于启动控制台进行特殊操作，如修改管理员密码、打开数据库控制台( gitlab-rails
dbconsole)等
gitlab-psql #数据库命令行
gitlab-rake #数据备份恢复等数据操作
```

范例：

```bash
[root@ubuntu1804 ~]#gitlab-psql
psql (9.6.11)
Type "help" for help.
gitlabhq_production=# help
You are using psql, the command-line interface to PostgreSQL.
Type:  \copyright for distribution terms
\h for help with SQL commands
\? for help with psql commands
\g or terminate with semicolon to execute query
\q to quit
gitlabhq_production=# \db
List of tablespaces
Name    |    Owner    | Location
------------+-------------+----------
pg_default | gitlab-psql |
pg_global  | gitlab-psql |
(2 rows)
```

```bash
gitlabhq_production-# \q
[root@ubuntu1804 ~]#
```

范例: 查看服务列表

```bash
[root@gitlab ~]#gitlab-ctl service-list
alertmanager*
gitaly*
gitlab-exporter*
gitlab-workhorse*
grafana*
logrotate*
nginx*
node-exporter*
postgres-exporter*
postgresql*
prometheus*
puma*
redis*
redis-exporter*
sidekiq*
```

### 为什么不直接运行旧版一键安装脚本

原稿脚本把 Ubuntu 18.04 的包路径、固定管理员密码和邮件授权码写死，还含有换行损坏的 URL 与 Shell 语句，无法可靠安装当前版本。安装流程应按下列顺序逐步执行并检查结果：

1. 核对系统支持矩阵、资源容量、DNS 与证书。
2. 从官方渠道配置与系统版本匹配的软件源，选择受支持的 GitLab 版本并安装。
3. 在 `/etc/gitlab/gitlab.rb` 配置 `external_url`，谨慎设置邮件、Registry 等可选组件。
4. 执行 `gitlab-ctl reconfigure`，再用 `gitlab-ctl status` 和浏览器访问检查核心服务。
5. 配置备份、升级窗口和日志监控；记录管理员初始凭据的安全交付方式。

不要在安装日志或教程中输出实际密码，也不要只凭 `gitlab-ctl status` 的退出码判断 Web、SSH 和仓库读写功能都正常。

### 基于 Docker 安装 GitLab

<https://docs.gitlab.com/ee/install/docker.html>

<https://hub.docker.com/r/gitlab/gitlab-ce>

![Git 与 GitLab 版本管理第 104 页插图](assets/img-3afc265bab354579.webp)

```text
https://docs.gitlab.com/ee/install/docker/configuration.html#pre-configure-
docker-container
sudo docker run --detach \
--hostname gitlab.example.com \
--env GITLAB_OMNIBUS_CONFIG="external_url 'http://gitlab.example.com';
gitlab_rails['lfs_enabled'] = true;" \
--publish 443:443 --publish 80:80 --publish 22:22 \
--name gitlab \
--restart always \
--volume $GITLAB_HOME/config:/etc/gitlab \
--volume $GITLAB_HOME/logs:/var/log/gitlab \
--volume $GITLAB_HOME/data:/var/opt/gitlab \
--shm-size 256m \
gitlab/gitlab-ce:<version>-ce.0
```

范例:基于Docker 部署

```bash
docker pull gitlab/gitlab-ce:17.0.1-ce.0
export GITLAB_HOME=/srv/gitlab
sudo docker run --detach \
--hostname gitlab.example.com \
--publish 443:443 --publish 80:80 --publish 22:22 \
--name gitlab \
--restart always \
--volume $GITLAB_HOME/config:/etc/gitlab \
--volume $GITLAB_HOME/logs:/var/log/gitlab \
--volume $GITLAB_HOME/data:/var/opt/gitlab \
--shm-size 256m \
gitlab/gitlab-ce:17.0.1-ce.0
#gitlab/gitlab-ce:latest
```

### 基于 Kubernetes 安装 GitLab

Kubernetes 安装不等于把单机命令直接复制进集群。应根据 [GitLab 官方 Helm Chart 文档](https://docs.gitlab.com/charts/) 核对与目标 Kubernetes 版本兼容的 Chart，并规划持久卷、Ingress、TLS 证书、外部域名、备份和升级。原稿中旧版 Operator 的多行 URL 与 YAML 缩进均已失效，不再作为可执行示例。

验证时至少检查 Chart/Pod 状态、Web 登录、SSH/HTTPS 克隆与推送，以及备份恢复演练；某个控制器显示 `Ready` 并不代表整个服务可交付。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/12-introduction-to-gitlab.html' | relative_url }}">← 上一篇：GitLab 介绍</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/14-basic-gitlab-configuration.html' | relative_url }}">下一篇：GitLab 基本配置 →</a>
</nav>
