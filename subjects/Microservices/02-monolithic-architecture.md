---
layout: default
title: "微服务架构 · 单体(巨石)架构"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 02 单体(巨石)架构
### 1.2 单体(巨石)架构

单体应用把商品、订单、支付等业务模块作为**一个可部署单元**交付。它不等于“只能运行在一台机器上”：只要应用状态和依赖允许，同一版本可以部署多个实例，由负载均衡器分流。Java 项目可打包为 JAR 或 WAR，其他语言也有各自的交付形式。

### 单体的优势

- **调用路径短**：模块间主要是进程内调用；同一数据库中的事务通常较容易管理。
- **开发与排错相对直接**：代码、测试和部署入口集中，适合需求尚在探索的团队。
- **运维组件较少**：不必为了通信先部署服务发现、跨服务追踪和复杂的发布协调。

### 何时会遇到压力

如果模块相互读写内部数据、缺乏清晰接口，代码增长后改动范围就难以控制。统一构建与发布也意味着一个模块的变更需要验证整个应用。横向扩容往往复制整个部署单元，难以只给热点功能增加实例；但可先尝试模块化、缓存、异步任务和数据分区，不必立刻拆为微服务。

### 实用判断

先按业务能力划分模块，限制跨模块访问，建立契约测试，并记录构建、发布和故障恢复时间。若独立交付或独立扩容的收益持续超过分布式系统的额外成本，再考虑拆分。维护良好的模块化单体并非“小项目专用”的过渡品。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/01-evolution-of-software-architecture.html' | relative_url }}">← 上一篇：软件架构演变</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/03-model-view-controller-mvc.html' | relative_url }}">下一篇：MVC 模型—视图—控制器 →</a>
</nav>
