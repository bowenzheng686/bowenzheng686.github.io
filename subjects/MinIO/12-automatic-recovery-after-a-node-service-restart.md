---
layout: default
title: "MinIO 对象存储 · 节点服务故障重启后自动恢复"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 12 节点服务故障重启后自动恢复
## 4 MINIO 故障恢复

minio集群有纠删码机制，即使在集群数据盘挂掉一半的情况下，集群中数据也是安全的。

但是如果集群想要正常读写,就需要有N/2+1的节点数才可以正常读写

如果现有minio集群有节点出现故障，就需要更换节点

注意事项

如果更换节点旧节点数据量较大，在节点更换时可以正常使用请先备份原有节点数据到新节点，避免同步的数据过多导致网络带宽被占用如果数据量小，可以不进行备份数据，直接进行更换，节点启动完毕会自动同步数据如果节点挂掉时集群还在读写数据，会导致集群挂掉的节点与其他minio节点数据不同，这里在恢复节点后需修复数据（自动修复，无需人为干预） 最好部署minio集群时使用hosts文件做地址解析，避免更换节点时修改minio配置文件参数更换节点时需要停止minio集群客户端的读写更换的新节点所有配置信息要和旧节点保持一致，包括minio版本，配置文件，hosts解析文件，数据目录位置以及大小

### 4.1 节点服务故障重启后自动恢复

如果在写入数据时,节点服务故障,当节点服务启动后,会自动同步数据

范例:  节点服务故障重启后自动恢复

```bash
#正在写入数据时,将某个节点服务停止
[root@minio2 ~]#systemctl stop minio
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 2/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000

```text
Uptime: offline
Drives: 0/4 OK
```

●  minio3.bowen.org:9000

```bash
Uptime: 14 minutes
Version: 2023-10-16T04:13:43Z
Network: 2/3 OK
Drives: 4/4 OK
Pool: 1
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
3.7 GiB Used, 1 Bucket, 1 Object
1 node offline, 8 drives online, 4 drives offline
#数据写入仍然进行,完成后,可以看到不同节点的数据空间不同
[root@minio1 ~]#df -h /data/
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  8.1G   11G  44% /data
[root@minio2 ~]#df -h /data
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  2.5G   17G  14% /data
[root@minio3 ~]#df -h /data
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G   11G  8.1G  57% /data
#模拟磁盘损坏
[root@minio2 ~]#rm -rf  /data/minio*
[root@minio2 ~]#mkdir /data/minio{1..4}
[root@minio2 ~]#chown -R minio.minio  /data/minio{1..4}
#恢复故障节点的服务
[root@minio2 ~]#systemctl start minio
#多次执行空间查看,可以看到数据在同步中
[root@minio2 ~]#df -h /data/
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  3.2G   16G  18% /data
[root@minio2 ~]#df -h /data/
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  3.4G   16G  19% /data
[root@minio2 ~]#df -h /data/
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  3.9G   15G  21% /data
[root@minio2 ~]#df -h /data/
Filesystem                    Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-minio   20G  8.9G  9.9G  48% /data
#集群状态恢复
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 11 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000

```text
Uptime: 5 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio3.bowen.org:9000

```text
Uptime: 22 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
13 GiB Used, 1 Bucket, 2 Objects
12 drives online, 0 drives offline
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/11-accessing-minio-with-programming-apis.html' | relative_url }}">← Previous: Accessing MinIO with Programming APIs</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">Back to MinIO Object Storage Index</a>
  <a href="{{ '/subjects/MinIO/13-recovering-a-node-after-os-reinstallation.html' | relative_url }}">Next: Recovering a Node After OS Reinstallation →</a>
</nav>
