---
layout: default
title: 'Prometheus · 关于文档'
subject_page: true
prometheus_notes: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 关于本文档

文档名称：《云原生监控系统 Prometheus》

使用协议：《知识共享公共许可协议(CCPL)》

## 贡献者

| 贡献者名称 | 贡献度 | 文档变更记录 | 个人主页 |
| --- | --- | --- | --- |
| 马哥（马永亮） | 主编 |  | http://github.com/iKubernetes/ |
| 王晓春 | 作者 | 458 页，版本迭代升级、修订和内容丰富 | http://www.wangxiaochun.com |

## 文档协议

署名要求：使用本系列文档，您必须保留本页中的文档来源信息，具体请参考《知识共享 (Creative Commons) 署名4.0公共许可协议国际版》。

非商业化使用：遵循《知识共享公共许可协议(CCPL)》，并且您不能将本文档用于马哥教育相关业务之外的其他任何商业用途。

您的权利：遵循本协议后，在马哥教育相关业务之外的领域，您将有以下使用权限：

共享 — 允许以非商业性质复制本作品。

改编 — 在原基础上修改、转换或以本作品为基础进行重新编辑并用于个人非商业使用。

## 致谢

本文档中部分素材参考了相关项目的文档，以及通过搜索引擎获得的内容，这里先一并向相关的贡献者表示感谢。

# 云原生监控系统 Prometheus

## 内容概述

- Prometheus 介绍
- Prometheus 部署和配置
- Node Exporter 采集数据
- Pushgateway 采集数据
- PromQL 查询语言
- Grafana 图形化展示
- Prometheus 标签管理
- Prometheus 告警机制
- Prometheus 服务发现
- 各种 Exporter 高级功能
- Prometheus 实现容器监控
- Prometheus 联邦 Federation
- Prometheus 远程存储 VictoriaMetrics
- Kubernetes 集成 Prometheus

## 阅读路线

初学者可先读第 01–04 章，理解监控链路、部署 Prometheus、接入 Node Exporter，再使用 Grafana 查看结果；随后阅读第 07–11 章，掌握 PromQL、标签与记录规则。需要通知时进入告警章节，需要动态目标时进入服务发现章节，最后再结合容器监控、远程存储和 Kubernetes 部署章节实践。每一章的旧版界面截图和历史命令都应与当前软件版本核对，正文会指出影响操作的差异。

{% endraw %}
