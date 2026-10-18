---
layout: default
title: "MinIO 对象存储 · 备份与恢复概述"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MinIO 对象存储目录]({{ '/subjects/MinIO/' | relative_url }})

{% raw %}

# 16 备份与恢复概述

MinIO 的纠删码用于应对一定范围内的盘或节点故障，**不是独立备份**：误删除、错误覆盖、凭据泄露、整站故障和错误配置都可能同时影响在线数据。本章介绍用 `rclone` 通过 S3 API 复制对象的基本流程；跨站点复制、对象锁和版本化等更完整的方案，应按恢复目标另行设计。

## 先定义恢复目标与范围

备份前明确 RPO（可接受的数据丢失时间）和 RTO（恢复服务所需时间），列出要保护的桶、对象、版本、元数据、访问策略、用户与访问密钥、生命周期规则，以及应用依赖。`rclone` 复制普通对象可以用于数据级备份，**不能默认完整保留桶配置、所有历史版本或 MinIO 管理身份**。

备份空间应根据对象的**逻辑数据量**、版本保留、增长、压缩和保留周期估算，并预留校验与恢复余量。原资料以“集群原始盘总容量的一半”估算备份空间并不可靠：纠删码开销、实际使用率和历史版本都会改变所需容量。数据量越大，越需要可持续的备份设计，而不是因为集群已有高可用就放弃备份。

## rclone 是什么

`rclone` 是支持多种云存储和本地文件系统的命令行工具，常用于复制、同步、检查和迁移。对 MinIO 使用 S3 后端，连接的是 **API 地址**，不是 Console 端口。它的几个动词差异需要先分清：

| 命令 | 作用 | 备份时的关注点 |
| --- | --- | --- |
| `rclone copy` | 将源对象复制到目标，不因源缺失而删除目标已有文件 | 适合作为初次和增量复制的基础。 |
| `rclone sync` | 使目标与源尽量一致，目标多余内容可能被删除 | 误删可能传播到“备份”，先预演并配置保留策略。 |
| `rclone check` | 对比源与目标的对象集合及可用校验信息 | 是传输验收的一部分，不能替代恢复演练。 |
| `rclone size` | 统计对象数与逻辑大小 | 用于估算容量，非底层原始磁盘占用。 |

## 安装与配置

可通过系统包管理器安装 `rclone`，再运行 `rclone version` 确认版本。交互式 `rclone config` 会询问后端类型，选择 `s3` 和 MinIO 提供商，填写 API Endpoint、专用 Access Key 与 Secret Key。不要用根账户执行日常备份；为备份身份授予所需桶的读取权限，恢复身份则另授写入权限。

```bash
sudo apt install rclone
rclone version
rclone config
rclone lsd minio:
```

配置文件通常位于 `~/.config/rclone/rclone.conf`，其中可能包含可用凭据。应限制权限并使用环境变量、密钥管理系统或加密配置方式管理密钥。原示例手写配置将 `env_auth` 错拼为 `evn_auth`，并直接展示密钥，均不宜沿用。若按文件配置，最小结构如下，真实密钥不要写进教程或仓库：

```ini
[minio]
type = s3
provider = Minio
env_auth = false
access_key_id = ACCESS_KEY
secret_access_key = SECRET_KEY
endpoint = http://minio.example.internal:9000
```

S3 签名、TLS、区域与路径式访问设置应按部署实际情况核对；`rclone lsd minio:` 能列出桶，仅证明基本连接与列举权限可用。

## 一次对象级备份与恢复

下面以 `mybucket` 为例，将对象复制到另一故障域的备份目录。先确保目录有足够空间，备份机本身受访问控制和监控保护。

```bash
rclone size minio:mybucket
rclone copy minio:mybucket /backup/minio/mybucket --progress --transfers 8
rclone check minio:mybucket /backup/minio/mybucket
```

后续运行 `copy` 会跳过可判断为未变化的对象，但如果源中对象被删除，目标旧文件仍会保留；这只是保留旧文件，不等于可追溯的版本化备份。应建立周期性快照或带时间戳的备份集，并记录任务退出码、对象数量、错误日志和恢复点。`--checksum` 依赖服务端可用的校验信息；多段上传等情况下不能把 ETag 一律当作普通 MD5。限速 `--bwlimit`、并发 `--transfers` 等参数按负载测试后调整。

恢复时先选择**独立测试桶或测试集群**验证，避免直接覆盖正在使用的生产桶：

```bash
rclone copy /backup/minio/mybucket restore:mybucket-test --progress
rclone check /backup/minio/mybucket restore:mybucket-test
```

然后由应用验证样本对象的读取、内容与元数据，并单独恢复桶策略、用户和其他未包含在对象复制中的配置。实际灾难恢复还应演练访问入口切换和回滚。下一章继续展示操作示例与常见陷阱。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MinIO/15-scaling-in.html' | relative_url }}">← 上一篇：缩容</a>
  <a href="{{ '/subjects/MinIO/' | relative_url }}">返回 MinIO 对象存储目录</a>
  <a href="{{ '/subjects/MinIO/17-backup-and-restore-examples.html' | relative_url }}">下一篇：备份与恢复示例 →</a>
</nav>
