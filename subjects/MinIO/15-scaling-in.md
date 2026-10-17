---
layout: default
title: "MinIO Object Storage · Scaling In"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to MinIO Object Storage Index]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 15 Scaling In
### 5.2 缩容

如果MinIO不是基于LVM的存储，缩容相当于重新部署集群

缩容前所有节点的数据备份,再在配置中删除上面的添加的节点,只保留部分节点,重启服务后,再恢复数据

注意：缩容需要重建数据和Access Key 信息

```bash
#查看当前状态
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000

```text
Uptime: 30 seconds
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 1
```

●  minio3.bowen.org:9000

```text
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 1
```

●  minio4.bowen.org:9000

```text
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 2
```

●  minio5.bowen.org:9000

```text
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 2
```

●  minio6.bowen.org:9000

```bash
Uptime: 3 minutes
Version: 2023-10-16T04:13:43Z
Network: 6/6 OK
Drives: 4/4 OK
Pool: 2
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
2nd, Erasure sets: 1, Drives per erasure set: 12
3.9 MiB Used, 1 Bucket, 6 Objects
24 drives online, 0 drives offline
#备份数据
略
#在所有节点修改配置
[root@minio1 ~]#vim /etc/default/minio
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=12345678
#MINIO_VOLUMES='http://minio{1...3}.bowen.org:9000/data/minio{1...4}
http://minio{4...6}.bowen.org:9000/data/minio{1...4}'
MINIO_VOLUMES='http://minio{1...3}.bowen.org:9000/data/minio{1...4}' #只保留部分节点
MINIO_OPTS='--console-address :9001'
MINIO_PROMETHEUS_AUTH_TYPE="public"
#关闭删除的节点服务,在集群剩余的所有节点上重启服务
[root@minio1 ~]#systemctl restart minio
#可看集群状态缩容成功
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 4 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000

```text
Uptime: 4 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio3.bowen.org:9000

```text
Uptime: 4 minutes
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
0 B Used, 1 Bucket, 0 Objects
12 drives online, 0 drives offline
#还原数据
略
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/14-scaling-out.html' | relative_url }}">← Previous: Scaling Out</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">Back to MinIO Object Storage Index</a>
  <a href="{{ '/subjects/MinIO/16-backup-and-restore-overview.html' | relative_url }}">Next: Backup and Restore Overview →</a>
</nav>
