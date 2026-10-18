---
layout: default
title: "MinIO 对象存储 · 节点服务重启后的恢复"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 12 节点服务重启后的恢复

本节只讨论**原有磁盘与数据仍在、MinIO 进程暂时停止后重启**的情形。操作系统重装、磁盘被更换或数据路径丢失属于不同故障，见下一章。把进程重启与磁盘损坏混为一谈，会让恢复步骤变得危险。

## 故障期间会发生什么

分布式集群使用纠删码和读写仲裁，但“半数盘在线就一定安全、半数加一节点就能读写”不是普适规则。能否继续读写取决于纠删码集合、校验分片数、故障位置与对象状态。即使服务仍能接受请求，也应把离线节点视为故障窗口，尽快恢复，并持续关注集群健康。

当某节点服务停止时，`mc admin info` 会报告该节点或其磁盘离线。其他节点的请求能否成功，由当时的仲裁决定。故障期间写入成功的对象在节点恢复后可能需要后台修复；修复速度受数据量、磁盘和网络吞吐影响，不等同于“服务一启动就立即同步完全部数据”。

## 恢复原节点

首先确认故障原因：进程异常、网络中断、磁盘未挂载、权限变化和存储损坏的处理方式不同。**不要为演示“自动恢复”而删除 `/data/minio*`**；原资料把 `rm -rf` 当作磁盘故障模拟，会直接销毁分片与元数据，不属于安全的服务重启实验。

在原节点上检查数据路径和服务状态：

```bash
systemctl status minio.service
findmnt /data/minio1
findmnt /data/minio2
findmnt /data/minio3
findmnt /data/minio4
journalctl -u minio.service -n 100 --no-pager
```

若仅是服务停止且挂载、数据和配置仍完好，保持原端点列表、凭据与版本不变，启动服务：

```bash
sudo systemctl start minio.service
sudo systemctl status minio.service
```

集群侧使用管理别名检查状态：

```bash
mc admin info minio-cluster
mc admin heal minio-cluster --dry-run
```

`mc admin info` 应逐步显示节点与预期驱动器恢复在线。`mc admin heal --dry-run` 可查看待修复情况；不同版本的后台扫描与手动修复命令有差异，实际操作前先查看 `mc admin heal --help`。不能只用各节点的 `df -h` 数字是否相等判断修复完成，因为纠删码分片与文件系统开销本来就可能不同。

最后通过 API 验证故障前、故障期间写入的样本对象均可读取，并持续观察修复队列、错误日志与集群指标。若仍有离线磁盘，先处理挂载或硬件问题，不要通过新建空目录掩盖故障。正式环境的故障演练应有独立备份、可回滚方案和明确的维护窗口。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/11-accessing-minio-with-programming-apis.html' | relative_url }}">← 上一篇：编程接口访问</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/13-recovering-a-node-after-os-reinstallation.html' | relative_url }}">下一篇：系统重装后的节点恢复 →</a>
</nav>
