---
layout: default
title: "MinIO 对象存储 · 系统重装后的节点恢复"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 13 系统重装后的节点恢复

节点故障后重装操作系统，比单纯重启服务多了身份、网络、挂载与数据路径恢复。先判断**原数据盘是否完好**：若仍可读取，优先保留并重新挂载；若盘已损坏，则属于驱动器替换和数据修复流程。不要在未知故障原因时格式化旧盘，也不要把空目录当作原盘直接启动。

## 恢复前的检查

通过健康节点的管理入口确认故障范围：

```bash
mc admin info minio-cluster
mc admin heal minio-cluster --dry-run
```

记录原节点的主机名、MinIO 版本、完整端点列表、环境变量文件、服务单元、证书、数据盘序列号和挂载映射，并确认独立备份可用。`mc admin info` 报告一个节点离线只说明当前通信失败；网络、服务或磁盘都可能是原因。故障期间集群是否还能读写取决于实际纠删码集合与仲裁，不能由节点总数推算。

## 原数据盘仍然完好

重装系统后，先安装与集群兼容的 MinIO 版本，恢复服务账户、配置文件与证书。将原数据盘**按原挂载点逐一挂载**，核对文件系统、所有权和读写权限，再恢复服务。尤其要保持 `MINIO_VOLUMES` 的端点表达式与原集群一致，不能临时增减驱动器或更换路径顺序。

```bash
findmnt /data/minio1
findmnt /data/minio2
findmnt /data/minio3
findmnt /data/minio4
systemctl cat minio.service
sudo systemctl start minio.service
sudo journalctl -u minio.service -n 100 --no-pager
```

如果新主机 IP 与旧 IP 不同，优先维护稳定的 DNS 名称，并检查各节点能解析到新地址；使用 `/etc/hosts` 时必须在相关节点上保持一致。更新负载均衡后端地址，并检验网络策略。但**不应无差别重启整个健康集群**：原案例在修复一台故障节点时重启所有节点，会扩大故障窗口，并可能使仍有仲裁的集群暂时不可用。

## 原数据盘已经丢失

替换盘的数量、所属纠删码集合及当前在线分片决定集群能否完成修复。先核对当前版本的驱动器替换指南与数据备份，再为每个失效盘准备与原路径对应的独立新盘；不要用同一块新盘上的多个目录冒充多个驱动器。恢复服务后，MinIO 可在满足条件时对新盘进行修复，但不能保证“节点一上线所有对象立即恢复”。如果丢失量超过可恢复范围，必须从备份或其他副本恢复。

## 验证修复结果

服务启动只表示进程在运行，不能作为数据恢复成功的终点。依次检查：

1. `mc admin info minio-cluster` 中各节点、驱动器和网络状态与预期拓扑相符。
2. `mc admin heal minio-cluster --dry-run` 与服务日志不再显示持续增加的修复失败；必要时依据当前版本文档启动修复并等待完成。
3. 故障前和故障期间上传的测试对象可通过不同入口读取，内容校验一致。
4. 监控、备份任务和负载均衡健康检查恢复正常。

原资料中的输出一处写新节点 `Drives: 0/4 OK`，同一段末尾又写 `12 drives online`，两者互相矛盾；实际操作必须以新的完整健康输出为准。底层 `tree` 出现 `xl.meta` 只能证明目录中有元数据，不能证明对象已完整、可读取。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/12-automatic-recovery-after-a-node-service-restart.html' | relative_url }}">← 上一篇：节点服务重启后的恢复</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/14-scaling-out.html' | relative_url }}">下一篇：扩容 →</a>
</nav>
