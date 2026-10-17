---
layout: default
title: "Docker Container Technology · Container Live Migration with CRIU"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Docker Container Technology Index]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 07 Container Live Migration with CRIU
### 1.7 基于CRIU实现容器热迁移（了解）

### 容器热迁移说明

### 容器热迁移

<https://docs.docker.com/reference/cli/docker/checkpoint/>

Docker容器热迁移是指在不停止或中断容器的情况下，将正在运行的Docker容器从一个主机迁移到另一个主机的过程。此过程确保了服务的高可用性，特别适用于负载均衡和故障转移场景。

Docker容器热迁移广泛应用于各种需要高可用性、负载均衡和故障转移的场景，如云计算平台、微服务架构、在线服务系统等。通过容器热迁移，可以在不中断服务的情况下实现容器的迁移和扩展，提高系统的灵活性和可靠性。

### CRIU 说明

<https://criu.org/Main_Page>

CRIU(Checkpoint/Restore In Userspace)是一款 Linux 软件。它可以冻结正在运行的容器（或单个应用程序）并将其状态检查点到磁盘。保存的数据可用于恢复应用程序并完全按照冻结期间的方式运行它。 使用此功能，现在可以进行应用程序或容器实时迁移、快照、远程调试和许多其他操作。 CRIU 最初是 Virtuozzo 的一个项目，并在社区的巨大帮助下发展壮大。它目前被 OpenVZ、LXC/LXD、 Docker、Podman 和其他软件使用（集成到其中），并打包用于许多 Linux 发行版。

### Docker 基于 CRIU 实现热迁移说明

<https://docs.docker.com/reference/cli/docker/checkpoint/#using-checkpoint-and-restore>

A new top level command docker checkpoint is introduced, with three subcommands:

docker checkpoint create (creates a new checkpoint) docker checkpoint ls (lists existing checkpoints) docker checkpoint rm (deletes an existing checkpoint)

Additionally, a --checkpoint flag is added to the docker container start command.

The options for docker checkpoint create :

```text
解释Usage:  docker checkpoint create [OPTIONS] CONTAINER CHECKPOINT
Create a checkpoint from a running container
--leave-running=false    Leave the container running after checkpoint
--checkpoint-dir         Use a custom checkpoint storage directory
```

And to restore a container:

```text
Usage:  docker start --checkpoint CHECKPOINT_ID [OTHER OPTIONS] CONTAINER
```

Example of using checkpoint and restore on a container:

```bash
$ docker run  --name cr -d busybox /bin/sh -c 'i=0; while true; do echo $i;
i=$(expr $i + 1); sleep 1; done'
abc0123
$ docker checkpoint create cr checkpoint1
# <later>
$ docker start --checkpoint checkpoint1 cr
abc0123
# 该选项的作用是 禁用容器的 seccomp 过滤器，允许容器中的进程自由调用任何系统调用。
换句话说，容器将不受 seccomp 的限制，可以执行所有系统调用，类似于在宿主机上运行的进程。
```

### Docker 基于 CRIU 实现热迁移步骤

1. 创建检查点：

```text
docker checkpoint create <container_name> <checkpoint_name>
```

2. 导出检查点：

将检查点文件导出到另一个主机。

```text
Docker 的检查点文件通常存储在
/var/lib/docker/containers/<container_id>/checkpoints/ 目录下。每个检查点会生成一
组文件，包括元数据文件和内存快照文件
rsync -avz
/var/lib/docker/containers/<container_id>/checkpoints/checkpoint1/
user@target_host:/path/to/destination/
scp -r /var/lib/docker/containers/<container_id>/checkpoints/checkpoint1/
user@target_host:/path/to/destination/
```

3. 在目标主机上恢复容器：

```text
docker start --checkpoint=<checkpoint_name> <container_name>
```

### 容器热迁移案例

### 环境准备

安装 criu 安装 docker 配置 docker 支持CRIU

1.7.2.1.1 Ubuntu

```bash
#Ubuntu24.04默认没有criu包,需要添加安装源
[root@ubuntu2404 ~]#add-apt-repository ppa:criu/ppa -y && apt update && apt -y
install criu docker.io
[root@ubuntu2404 ~]#criu check
Can't check shutdown state of inet socket
Looks good.
[root@ubuntu2404 ~]#criu -V
Version: 4.0
[root@ubuntu2404 ~]#criu check
Looks good.
[root@ubuntu2404 ~]#criu -V
Version: 4.1
```

```bash
#Ubuntu22.04默认有criu包
[root@ubuntu2204 ~]#apt update && apt install -y  docker.io criu
[root@ubuntu2204 ~]#criu --version
Version: 3.16.1
[root@ubuntu2204 ~]#criu check
Looks good.
[root@ubuntu2204 ~]#docker version
Client:
Version:           26.1.3
API version:       1.45
Go version:        go1.22.2
Git commit:        26.1.3-0ubuntu1~22.04.1
Built:             Mon Oct 14 21:24:40 2024
OS/Arch:           linux/amd64
Context:           default
Server:
Engine:
Version:          26.1.3
API version:      1.45 (minimum version 1.24)
Go version:       go1.22.2
Git commit:       26.1.3-0ubuntu1~22.04.1
Built:            Mon Oct 14 21:24:40 2024
OS/Arch:          linux/amd64
Experimental:     false
containerd:
Version:          1.7.24
GitCommit:
runc:
Version:          1.1.12-0ubuntu2~22.04.1
GitCommit:
docker-init:
Version:          0.19.0
GitCommit:
```

```bash
#默认没有开启checkpoint的实验性功能
[root@ubuntu2404 ~]#docker checkpoint
docker checkpoint is only supported on a Docker daemon with experimental features
enabled
```

```json
#启动CRIU功能
[root@ubuntu2404 ~]#cat > /etc/docker/daemon.json <<EOF
{
"registry-mirrors": [
"https://docker.1ms.run",
"https://docker.xuanyuan.me"
],
"experimental": true
}
EOF
[root@ubuntu2404 ~]#systemctl restart docker
[root@ubuntu2404 ~]#docker checkpoint
Usage:  docker checkpoint COMMAND
Manage checkpoints
Commands:
create      Create a checkpoint from a running container
ls          List checkpoints for a container
rm          Remove a checkpoint
Run 'docker checkpoint COMMAND --help' for more information on a command.
```

1.7.2.1.2 RockyLinux

```bash
#在所有相关的主机上安装相关工具
[root@rocky9 ~]#yum -y install criu
[root@rocky9 ~]#criu --version
Version: 3.18
[root@rocky9 ~]#yum install -y yum-utils device-mapper-persistent-data lvm2
[root@rocky9 ~]#yum-config-manager --add-repo http://mirrors.aliyun.com/docker-
ce/linux/centos/docker-ce.repo
[root@rocky9 ~]#yum -y install docker-ce
[root@rocky9 ~]#systemctl enable --now docker
[root@rocky9 ~]#systemctl restart docker
#默认没有开启checkpoint功能
[root@rocky9 ~]#docker checkpoint
docker checkpoint is only supported on a Docker daemon with experimental features
enabled
[root@rocky9 ~]#echo "{\"experimental\": true}" >> /etc/docker/daemon.json
```

```bash
[root@rocky9 ~]#systemctl restart docker
#确认支持并查看相关用法
[root@rocky9 ~]#docker checkpoint
Usage:  docker checkpoint COMMAND
Manage checkpoints
Commands:
create      Create a checkpoint from a running container
ls          List checkpoints for a container
rm          Remove a checkpoint
Run 'docker checkpoint COMMAND --help' for more information on a command.
```

```bash
[root@rocky9 ~]#docker checkpoint create --help
Usage:  docker checkpoint create [OPTIONS] CONTAINER CHECKPOINT
Create a checkpoint from a running container
Options:
--checkpoint-dir string   Use a custom checkpoint storage directory
--leave-running           Leave the container running after checkpoint
```

```bash
[root@rocky9 ~]#docker start --help |grep checkpoint
--checkpoint string       Restore from this checkpoint
--checkpoint-dir string   Use a custom checkpoint storage directory
```

### 启动运行一个需要热迁移的容器

```bash
#创建测试容器
[root@rocky9 ~]#docker run  --restart always --name cr -d registry.cn-
beijing.aliyuncs.com/bowenxiaochun/busybox:1.32.0 /bin/sh -c 'i=0; while true; do
echo $i `date +%F_%T` ; i=$(expr $i + 1); sleep 1; done'
[root@rocky9 ~]#docker logs -f  cr
0 2025-06-25_02:38:10
1 2025-06-25_02:38:11
2 2025-06-25_02:38:12
3 2025-06-25_02:38:13
4 2025-06-25_02:38:14
5 2025-06-25_02:38:15
6 2025-06-25_02:38:16
```

### 备份

```bash
#创建checkpoint快照
#方法1:checkpoint数据指定生成文件所在目录
[root@ubuntu2404 ~]#docker checkpoint create --checkpoint-dir /srv/ cr
checkpoint1
#创建checkpoint后,容器会自动退出
[root@ubuntu2404 ~]#docker ps -l
CONTAINER ID   IMAGE
COMMAND                  CREATED              STATUS                        PORTS
NAMES
806663a7e3c3   registry.cn-beijing.aliyuncs.com/bowenxiaochun/busybox:1.32.0
"/bin/sh -c 'i=0; wh…"   About a minute ago   Exited (137) 50 seconds ago
cr
[root@ubuntu2404 ~]#ls /srv
checkpoint1
[root@ubuntu2404 ~]#ls /srv/checkpoint1/
cgroup.img        files.img      ipcns-var-11.img    pages-1.img
tmpfs-dev-51.tar.gz.img  utsns-12.img
core-1.img        fs-1.img       mm-1.img            pages-2.img
tmpfs-dev-52.tar.gz.img
core-26.img       fs-26.img      mm-26.img           pstree.img
tmpfs-dev-53.tar.gz.img
descriptors.json  ids-1.img      mountpoints-13.img  seccomp.img
tmpfs-dev-54.tar.gz.img
fdinfo-2.img      ids-26.img     pagemap-1.img       timens-0.img
tmpfs-dev-55.tar.gz.img
fdinfo-3.img      inventory.img  pagemap-26.img      tmpfs-dev-48.tar.gz.img
tmpfs-dev-56.tar.gz.img
[root@ubuntu2404 ~]#du -sh /srv/checkpoint1/
240K    /srv/checkpoint1/
```

```bash
[root@ubuntu2404 ~]#docker checkpoint ls cr
#需要指定路径才能看到checkpoint
[root@ubuntu2404 ~]#docker checkpoint ls cr --checkpoint-dir /srv/
CHECKPOINT NAME
checkpoint1
#方法2: checkpoint数据保存在默认路
径/var/lib/docker/containers/<container_id>/checkpoints/
[root@rocky9 ~]#docker checkpoint create cr checkpoint1
checkpoint1
#查看checkpoint文件
[root@rocky9 ~]#tree
/var/lib/docker/containers/806663a7e3c38362a7678e9d618cee6ac668a3337800e1daa9587
3ba71333f03/checkpoints/
/var/lib/docker/containers/806663a7e3c38362a7678e9d618cee6ac668a3337800e1daa9587
3ba71333f03/checkpoints/
└── checkpoint1
├── cgroup.img
├── core-1.img
├── core-84.img
├── descriptors.json
├── fdinfo-2.img
├── fdinfo-3.img
├── files.img
├── fs-1.img
├── fs-84.img
├── ids-1.img
├── ids-84.img
├── inventory.img
├── ipcns-var-11.img
├── mm-1.img
├── mm-84.img
├── mountpoints-13.img
├── pagemap-1.img
├── pagemap-84.img
├── pages-1.img
├── pages-2.img
├── pstree.img
├── seccomp.img
├── timens-0.img
├── tmpfs-dev-48.tar.gz.img
├── tmpfs-dev-51.tar.gz.img
├── tmpfs-dev-52.tar.gz.img
├── tmpfs-dev-53.tar.gz.img
├── tmpfs-dev-54.tar.gz.img
├── tmpfs-dev-55.tar.gz.img
├── tmpfs-dev-56.tar.gz.img
└── utsns-12.img
1 directory, 31 files
```

```bash
#创建checkpoint后,容器会自动退出
[root@rocky9 ~]#docker ps -l
CONTAINER ID   IMAGE
COMMAND                  CREATED              STATUS                        PORTS
NAMES
806663a7e3c3   registry.cn-beijing.aliyuncs.com/bowenxiaochun/busybox:1.32.0
"/bin/sh -c 'i=0; wh…"   About a minute ago   Exited (137) 50 seconds ago
cr
#确认创建checkpoint
[root@rocky9 ~]#docker checkpoint ls cr
CHECKPOINT NAME
checkpoint1
```

```bash
[root@ubuntu2404 ~]#docker logs  cr
0 2025-01-16_10:12:11
1 2025-01-16_10:12:12
2 2025-01-16_10:12:13
3 2025-01-16_10:12:14
4 2025-01-16_10:12:15
5 2025-01-16_10:12:16
6 2025-01-16_10:12:17
7 2025-01-16_10:12:18
```

```bash
#删除checkpoint
[root@rocky9 ~]#docker checkpoint rm cr  checkpoint1
```

### 还原

```bash
#在第二台主机上准备环境,按1.7.2.1小节
#用相同的命令创建和前面主机同样的容器,注意:只创建不运行
[root@ubuntu2404 ~]#docker create --restart always --name cr  registry.cn-
beijing.aliyuncs.com/bowenxiaochun/busybox:1.32.0 /bin/sh -c 'i=0; while true; do
echo $i `date +%F_%T` ; i=$(expr $i + 1); sleep 1; done'
[root@ubuntu2404 ~]#docker ps -l
CONTAINER ID   IMAGE
COMMAND                  CREATED              STATUS
PORTS     NAMES
e765a315dfd4   registry.cn-beijing.aliyuncs.com/bowenxiaochun/busybox:1.32.0
"/bin/sh -c 'i=0; wh…"   About a minute ago   Exited (137) About a minute ago
cr
```

```bash
#当前没有checkpoint
[root@ubuntu2404 ~]#docker checkpoint ls cr
CHECKPOINT NAME
#查看容器ID
[root@ubuntu2404 ~]#docker inspect --format "{{.ID}}" cr
e765a315dfd4b11b2ce9affd4cf80263054a3de2b4baaac1492ffa5c378a5a84
#查看当前容器目录为空
[root@ubuntu2404 ~]#ls
/var/lib/docker/containers/e765a315dfd4b11b2ce9affd4cf80263054a3de2b4baaac1492ff
a5c378a5a84/checkpoints/
[root@ubuntu2404 ~]#
```

```bash
#将第一台主机的checkpoint文件复制到需要恢复的目标主机相应的目录下
[root@ubuntu2404 ~]#cd
/var/lib/docker/containers/e765a315dfd4b11b2ce9affd4cf80263054a3de2b4baaac1492ff
a5c378a5a84/checkpoints/
[root@ubuntu2404 checkpoints]#rsync -av 10.0.0.101:/srv/checkpoint1/ .
```

```bash
#目标主机上确认文件复制完成
[root@ubuntu2404 ~]#ls
/var/lib/docker/containers/e765a315dfd4b11b2ce9affd4cf80263054a3de2b4baaac1492ff
a5c378a5a84/checkpoints/
checkpoint1
#查看checkpoint出现
[root@ubuntu2404 ~]#docker checkpoint ls cr
CHECKPOINT NAME
checkpoint1
#恢复容器
[root@ubuntu2404 ~]#docker start --checkpoint checkpoint1 cr
#观察日志说明容器是接着上前面的继续执行
[root@ubuntu2404 ~]#docker logs -f cr
8 2025-01-16_10:15:47
9 2025-01-16_10:15:48
10 2025-01-16_10:15:49
11 2025-01-16_10:15:50
12 2025-01-16_10:15:51
13 2025-01-16_10:15:52
14 2025-01-16_10:15:53
15 2025-01-16_10:15:54
16 2025-01-16_10:15:55
17 2025-01-16_10:15:56
18 2025-01-16_10:15:57
19 2025-01-16_10:15:58
20 2025-01-16_10:15:59
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/06-docker-run-parameters.html' | relative_url }}">← Previous: Docker Run Parameters</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">Back to Docker Container Technology Index</a>
  <a href="{{ '/subjects/Docker/08-docker-image-fundamentals.html' | relative_url }}">Next: Docker Image Fundamentals →</a>
</nav>
