---
layout: default
title: "Microservices · Model-View-Controller (MVC)"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Microservices Index]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 03 Model-View-Controller (MVC)
### 1.3 MVC

JAVA的 MVC

MVC是模型(Model)、视图(View)、控制器(Controller)的简写，是一种软件设计规范。是将业务逻辑、数据、显示分离的方法来组织代码。 MVC主要作用是降低了视图与业务逻辑间的双向偶合。

MVC不是一种设计模式，MVC是一种架构模式。当然不同的MVC存在差异。

MVC 采用template技术实现前端展示，前端和后端最终编译和整合为一个单体应用，和前后端分离方式分为两个独立项目是不同的。

Model（模型）：数据模型，提供要展示的数据，因此包含数据和行为，可以认为是领域模型或JavaBean组件（包含数据和行为），不过现在一般都分离开来：Value Object（数据Dao） 和 服务层（行为Service）。也就是模型提供了模型数据查询和模型数据的状态更新等功能，包括数据和业务。 View（视图）：负责进行模型的展示，一般就是我们见到的用户界面，客户想看到的东西。可通过JSP实现 Controller（控制器）：接收用户请求，委托给模型进行处理（状态改变），处理完毕后把返回的模型数据返回给视图，由视图负责展示。也就是说控制器做了个调度员的工作。最终表现为Servlet

Python的 MTV

M: Model 数据模型，负责与数据库交互， T：Template 模板展示，负责呈现内容到浏览器，一般为.html文件 V:  view 流程逻辑，负责接收请求，相当于处理中枢，获取数据（来自用户） ，经过处理后选择合适的结果返回给用户。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/02-monolithic-architecture.html' | relative_url }}">← Previous: Monolithic Architecture</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/04-service-oriented-architecture-soa.html' | relative_url }}">Next: Service-Oriented Architecture (SOA) →</a>
</nav>
