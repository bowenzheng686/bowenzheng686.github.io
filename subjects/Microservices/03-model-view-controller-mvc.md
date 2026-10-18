---
layout: default
title: "微服务架构 · MVC 模型—视图—控制器"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 03 MVC 模型—视图—控制器
### 1.3 MVC

MVC（Model–View–Controller）将输入处理、业务数据和展示组织成不同职责。它描述的是**应用内部**的代码结构，不决定应用必须是单体，也不要求视图一定由服务端模板渲染。前后端分离的后端接口仍可采用 MVC 组织方式。

以“查看订单”为例，请求先进入 **Controller**：校验输入、调用应用服务并选择响应形式；**Model** 承载订单数据和相关业务规则，实际项目常进一步分为领域对象、服务与持久化层；**View** 负责将结果呈现给用户，可以是 HTML 模板，也可以是供前端使用的 JSON 表示。DAO 与 Value Object 分别负责数据访问和值表达，并不是 Model 的同义词。

在 Java Web 项目中，Spring MVC 的 Controller 处理路由和请求，视图可以采用 Thymeleaf 模板或 JSON 响应。Django 常用 **MTV** 术语：Model 管理数据，Template 负责展示，View 接收请求并准备响应；Django View 在职责上更接近 MVC 的 Controller。

下一篇 SOA 讨论**系统之间**的服务边界；MVC 讨论**应用内部**的职责分工。两者不在同一个层面，也不是先后替代关系。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/02-monolithic-architecture.html' | relative_url }}">← 上一篇：单体(巨石)架构</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回微服务架构目录</a>
  <a href="{{ '/subjects/Microservices/04-service-oriented-architecture-soa.html' | relative_url }}">下一篇：SOA 面向服务架构 →</a>
</nav>
