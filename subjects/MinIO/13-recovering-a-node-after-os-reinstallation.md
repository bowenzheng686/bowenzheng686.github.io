---
layout: default
title: "MinIO Object Storage · Recovering a Node After OS Reinstallation"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to MinIO Object Storage Index]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 13 Recovering a Node After OS Reinstallation
### 4.2 节点故障重新安装系统恢复故障

范例:  3节点集群中一个节点彻底故障并重新安装进行恢复

```bash
#发现一台节点出故障
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 3 hours
Version: 2023-10-16T04:13:43Z
Network: 2/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000  #故障节点

```text
Uptime: offline
Drives: 0/4 OK
```

●  minio3.bowen.org:9000

```text
Uptime: 3 hours
Version: 2023-10-16T04:13:43Z
Network: 2/3 OK
Drives: 4/4 OK
Pool: 1
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
2.6 MiB Used, 1 Bucket, 4 Objects
1 node offline, 8 drives online, 4 drives offline
```

```bash
#在所有节点上修改/etc/hosts文件中用新节点的IP替代故障节点的IP
[root@minio1 ~]#vim /etc/hosts
10.0.0.101 minio1.bowen.org
10.0.0.104 minio2.bowen.org  #原主机名保留,更新节点的IP
10.0.0.103 minio3.bowen.org
```

```bash
[root@minio1 ~]#for i  in {2..3};do scp /etc/hosts minio$i.bowen.org:/etc/;done
#修改反向代理配置,替换故障节点的地址为新节点
过程略
#安装一台新的节点,参考2.3.2.1小节:范例: 二进制安装MinIO 实现3节点4磁盘的分布式集群部署
过程略
#在所有节点上重启服务
[root@minio1 ~]#systemctl restart minio.service
#验证节点恢复
[root@ubuntu2204 ~]#mc admin  info minio-cluster
```

●  minio1.bowen.org:9000

```text
Uptime: 9 seconds
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
```

●  minio2.bowen.org:9000

```text
Uptime: 9 seconds
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 0/4 OK
Pool: 1
```

●  minio3.bowen.org:9000

```bash
Uptime: 9 seconds
Version: 2023-10-16T04:13:43Z
Network: 3/3 OK
Drives: 4/4 OK
Pool: 1
Pools:
1st, Erasure sets: 1, Drives per erasure set: 12
13 GiB Used, 1 Bucket, 2 Objects
12 drives online, 0 drives offline
#在新节点上发现数据恢复
[root@ubuntu2204-107 ~]#tree /data/
/data/
├── lost+found
├── minio1
│   └── mybucket
│       ├── example-object1.txt
│       │   └── xl.meta
│       ├── example-object2.txt
│       │   └── xl.meta
│       └── example-object3.txt
│           └── xl.meta
├── minio2
│   └── mybucket
│       ├── example-object1.txt
│       │   └── xl.meta
│       ├── example-object2.txt
│       │   └── xl.meta
│       └── example-object3.txt
│           └── xl.meta
├── minio3
│   └── mybucket
│       ├── example-object1.txt
│       │   └── xl.meta
│       ├── example-object2.txt
│       │   └── xl.meta
│       └── example-object3.txt
│           └── xl.meta
└── minio4
└── mybucket
├── example-object1.txt
│   └── xl.meta
├── example-object2.txt
│   └── xl.meta
└── example-object3.txt
└── xl.meta
21 directories, 12 files
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/12-automatic-recovery-after-a-node-service-restart.html' | relative_url }}">← Previous: Automatic Recovery After a Node Service Restart</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">Back to MinIO Object Storage Index</a>
  <a href="{{ '/subjects/MinIO/14-scaling-out.html' | relative_url }}">Next: Scaling Out →</a>
</nav>
