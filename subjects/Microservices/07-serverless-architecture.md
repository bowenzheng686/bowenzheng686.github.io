---
layout: default
title: "微服务架构 · 无服务架构 Serverless"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 07 Serverless 架构
### 1.7 “无服务器”不等于没有服务器

Serverless 指开发团队把一部分服务器容量规划、运行时维护和弹性伸缩交给平台，而不是应用不再使用服务器。常见形式包括函数即服务（FaaS）和托管数据库、消息、对象存储等后端即服务（BaaS）。它与微服务是不同维度：一个微服务可以部署为容器，也可以由云函数实现。

以“上传图片后生成缩略图”为例：对象存储产生事件，触发函数读取原图、生成缩略图并写回存储。开发者主要维护函数逻辑、权限和事件契约；平台负责实例启动与扩缩。但仍需设计失败重试、幂等、消息积压、可观测性与费用上限。

### 适合与不适合的条件

- **适合试点**：事件驱动任务、请求量波动明显、任务执行时间可控，且希望减少长期维护空闲服务器的工作。
- **需要验证**：长连接、持续高负载、严格尾延迟、强依赖本地状态或特殊运行环境。平台对并发、执行时长、网络访问和冷启动的限制因产品而异，不能一概断言“无限算力”或固定的冷启动毫秒数。
- **成本比较**：低流量时按使用量计费可能划算；持续高负载时也可能比常驻服务更贵。结合真实流量、存储、出网和日志费用测算，而非只看函数调用费。

Serverless 能减少部分基础设施操作，不会替团队承担业务可靠性、数据安全和跨组件故障处理。Kubernetes、Knative 或云厂商函数产品都能承载部分场景，但不是唯一实现路径；先用一个可独立回退的业务事件试点，再决定是否扩大使用。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/06-service-mesh.html' | relative_url }}">← 上一篇：服务网格 Mesh</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/08-microservices-vs-monoliths.html' | relative_url }}">下一篇：微服务还是单体 →</a>
</nav>
