---
layout: default
title: "MinIO Object Storage · Backup and Restore Overview"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to MinIO Object Storage Index]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 16 Backup and Restore Overview
## 6 MINIO 备份还原

### 6.1 备份还原说明

### rclone 工具介绍

Rclone，即"rsync for cloud storage"，号称云存储的瑞士军刀

Rclone是一款专业的用于管理和同步云储存数据的开源命令行工具。通过该工具，用户不仅可以在各类型云盘之间拷贝、同步数据，还能支持资源占用低，速度快，稳定性好等一系列优点。

rclone 由Golang编写，旨在提供在不同平台的文件系统和多种类型的对象存储产品之间的数据同步功能。

rclone支持超过40种不同的云存储服务，如 Amazon S3、Google Drive、Dropbox、Microsoft OneDrive、Google Cloud Storage等，它提供了多种文件传输方式，包括复制、同步、移动和删除文件，并支持文件加密和压缩。 此外，rclone还支持分块上传和下载，允许传输过程中断后恢复，以及文件的校验和合并。它的主要优势在于灵活性和可扩展性，可以用于备份、文件同步、数据迁移等多种场景，并在Windows、macOS、 Linux、FreeBSD、NetBSD等平台上均可运行。

Rclone 具有强大的云等同于 unix 命令 rsync、cp、mv、mount、ls、ncdu、tree、rm 和 cat。Rclone 熟悉的语法包括 shell 管道支持和--dry-run保护。它在命令行、脚本或通过其API 使用。

Rclone多种文件传输协议，支持SFTP，HTTP，WebDAV，FTP和DLNA。Rclone是一个成熟的开源软件，最初受rsync的启发并采用Golang编写。其文档和社区也都非常好，提供广泛和友好的使用用例。

rclone的配置简单，可以通过命令行或配置文件进行设置，它提供了丰富的命令行功能，使得操作云存储非常方便。此外，rclone还提供mount操作，允许将远端对象存储挂载到本地文件系统进行访问。

使用rclone工具进行数据同步，把minio集群bucket的对象数据同步到备份服务器

Rclone 配置

配置可以直接添加配置文件的方式或者通过进入交互式配置会话命令一步步的完成配置。

默认配置完成的后配置文件都保存在：~/.config/rclone/rclone.conf 目录下。

```text
[tencent-cos] # 自定义的配置名称
type = s3  # 存储类型，参考官方文档所有支持的类型
provider = TencentCOS  # 提供商，参考官方文档或者全部
env_auth = false   # 不通过环境变量配置认证
access_key_id = AKxxxxxxxx  # 腾讯云后台生成的密钥key
secret_access_key = Secretxxxxxxx # 腾讯云后台生成的密钥secret
endpoint = cos.ap-chengdu.myqcloud.com # 腾讯云cos所在的地区，看你所在存储桶的公网地址
```

Rclone 语法

```text
#基本格式
rclone [功能选项] <源> <目标> [参数] [参数]
# 本地同步到网盘
rclone [功能选项] <本地路径> <配置名称:路径> [参数] [参数]
# 网盘同步到本地
rclone [功能选项] <配置名称:路径> <本地路径> [参数] [参数]
# 网盘同步到网盘
rclone [功能选项] <配置名称:路径> <配置名称:路径> [参数] [参数]
# [参数]为可选项
#示例：
#同步本地/data/file的文件夹内容到tencent-cos存储下的/backup文件夹中,并且排
除/root/excludes.txt中指定的文件内容
rclone sync /data/file tencent-cos:/backup --exclude-from
'/root/backup_file.txt'
# 两个网盘文件同步
rclone copy 配置网盘名称1:网盘路径 配置网盘名称2:网盘路径
```

Rclone 命令列表

使用 rclone --help 可查看所有命令，这里只列出常用的命令

命令说明

rclone copy 复制

rclone

移动，如果要在移动后删除空源目录，加上 --delete-empty-src-dirs 参数,会删除源

move

文件类似于MV命令

rclone mount 挂载

rclone sync 同步：将源目录同步到目标目录，只更改目标目录

rclone size 查看网盘文件占用大小

rclone delete 删除路径下的文件内容

rclone mkdir 创建目录

rclone rmdir 删除目录

rclone rmdirs 删除指定环境下的空目录。如果加上 --leave-root 参数，则不会删除根目录

rclone check 检查源和目的地址数据是否匹配

rclone ls 列出指定路径下的所有的文件以及文件大小和路径

rclone lsl 比上面多一个显示上传时间

rclone lsd 列出指定路径下的目录

rclone lsf 列出指定路径下的目录和文件

范例: 安装和配置 rclone

```bash
#准备rclone的配置文件
[root@ubuntu2404 ~]#apt list rclone
Listing... Done
rclone/noble-security,noble-updates,noble-updates,noble-security 1.60.1+dfsg-
3ubuntu0.24.04.2 amd64
N: There is 1 additional version. Please use the '-a' switch to see it
[root@ubuntu2404 ~]#apt update && apt -y install rclone
[root@ubuntu2404 ~]#rclone version
rclone v1.60.1-DEV
- os/version: ubuntu 24.04 (64 bit)
- os/kernel: 6.8.0-48-generic (x86_64)
- os/type: linux
- os/arch: amd64
- go/version: go1.22.2
- go/linking: dynamic
- go/tags: none
```

```bash
[root@ubuntu2404 ~]#apt update && apt -y install rclone
#实现自动补全
#方法1
[root@ubuntu2404 ~]#echo 'source <(rclone completion bash)' >> ~/.bashrc;exit
#方法2
[root@ubuntu2404 ~]#rclone  completion bash > /etc/bash_completion.d/rclone;exit
#创建配置
#方式1：通过提示自动生成配置
[root@ubuntu2404 ~]#rclone config
Current remotes:
Name                 Type
====                 ====
minio                s3
minio-cluster        s3
e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q>n
```

```bash
#方法2：手动准备配置文件
[root@ubuntu2204 ~]#mkdir  -p .config/rclone
[root@ubuntu2204 ~]#cat >  .config/rclone/rclone.conf <<EOF
[minio]
type = s3
provider = Minio
evn_auth = false
#access_key_id = admin
#secret_access_key = 12345678
access_key_id = eesdfHZp7ab0SUZCIFWq
secret_access_key = sznccI8iITaQMp9ZzJYmv7H0w8ompCAPF9jvFtpE
region = beijing-1
endpoint = http://minio.bowen.org:9000
EOF
#验证配置
[root@ubuntu2204 ~]#rclone lsd minio:
-1 2023-10-17 18:10:16        -1 mybucket
```

### 备份还原过程

注意事项

备份服务器要求存储空间至少满足minio集群存储空间的一半

比如:  minio集群存储空间一共48T,则备份服务器需要24T的空间来备份数据

第一次进行全量同步，之后进行增量同步

可以使用md5校验来确定是否同步数据，根据自身需求选择，md5校验会cpu消耗较高，但是确定对象文件是否改变要比其他方式更准确

建议在业务负载较低时执行备份

如果数据量大时不建议进行备份，因为本身minio集群已经实现高可用

具体备份还原流程

```bash
#方式1：通过提示自动生成配置
[root@ubuntu2404 ~]#rclone config
Current remotes:
Name                 Type
====                 ====
minio                s3
minio-cluster        s3
e) Edit existing remote
n) New remote
d) Delete remote
r) Rename remote
c) Copy remote
s) Set configuration password
q) Quit config
e/n/d/r/c/s/q>n
```

```bash
#方法2：手动准备配置文件
[root@minio01 ~]# vim ~/.config/rclone/rclone.conf
[minio] #minio集群名称
type = s3
provider = Minio
evn_auth = false
access_key_id = admin
secret_access_key = 12345678
region = beijing-1
endpoint = http://minio.bowen.org:9000
#验证配置命令
rclone lsd <minio集群名称>:
#备份命令
#全量备份
rclone sync <minio集群名称>:/<bucket名称> <备份目录> -vP
#增量备份,使用md5判断文件是否需要重新同步
rclone sync <minio集群名称>:/<bucket名称> <备份目录>  -vP --checksum
#备份选项
--transfers=N - 并行文件数，默认为4，根据内存，以及带宽调整
--buffer-size=SIZE 加速 sync命令，使用内存缓存大小
--bwlimit UP:DOWN 上传下载限速b|k|M|G,在业务需要时可根据需求设置
--checksum 通过md5判断文件是否有需要同步，消耗cpu比较高
--update --use-server-modtime 通过mtime判断文件是否需要同步,Skip files that are newer
on the destination
#推荐同步备份数据命令
rclone sync <minio集群名称>:/<bucket名称> <备份目录> --transfers=8 --update -v -P
#推荐恢复备份数据命令
rclone sync <备份目录> <minio集群名称>:/<bucket名称> --transfers=8 --update -v --
logfile=rclone.log
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/15-scaling-in.html' | relative_url }}">← Previous: Scaling In</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">Back to MinIO Object Storage Index</a>
  <a href="{{ '/subjects/MinIO/17-backup-and-restore-examples.html' | relative_url }}">Next: Backup and Restore Examples →</a>
</nav>
