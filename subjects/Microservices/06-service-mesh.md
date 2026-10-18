---
layout: default
title: "微服务架构 · 服务网格 Mesh"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 06 服务网格 Mesh
### 1.6 把哪些通信能力下沉到基础设施

服务网格（Service Mesh）面向**服务之间**的通信治理。常见实现把代理与工作负载部署在一起（例如同一 Pod 的 sidecar），或通过节点级、无 sidecar 的数据平面接管部分流量；控制平面下发路由、身份和策略配置，数据平面实际处理请求。它属于软件基础设施，不是硬件功能，也不要求所有服务都使用 Kubernetes。

一个请求从订单服务到库存服务时，代理可执行服务身份认证、加密、路由、超时、重试和指标采集。但代理只看到通信过程，不理解“扣库存”是否可重试、事务如何补偿。**幂等、业务授权和数据一致性仍是应用责任**；错误的自动重试甚至会放大故障。

| 层面 | 典型职责 | 不应误解为 |
| --- | --- | --- |
| Kubernetes | 工作负载调度、服务发现、基础网络与配置对象 | 自带完整的应用级熔断与调用语义 |
| 服务网格 | 服务间身份、流量策略、部分可观测性 | 替代全部网关、业务代码或监控系统 |
| 应用框架 | 业务 API、调用语义与领域容错 | 每项网络策略都必须写入应用 |

引入前先确认是否真的存在跨语言重复治理、大量服务间流量策略或统一身份认证需求。再评估代理资源开销、证书与控制平面可用性、故障排查难度。服务较少时，网关加应用框架可能更容易维护。Istio、Linkerd、Consul Connect 等实现方式和功能边界不同，应以目标版本文档与试点数据判断，而非把网格当作微服务的必经阶段。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/05-microservices.html' | relative_url }}">← 上一篇：微服务</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/07-serverless-architecture.html' | relative_url }}">下一篇：Serverless 架构 →</a>
</nav>
