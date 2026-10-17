---
layout: default
title: "Microservices · Monolithic Architecture"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Microservices Index]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 02 Monolithic Architecture
### 1.2 单体(巨石)架构

传统架构（单机系统），一个项目一个工程：比如:商品、订单、支付、库存、登录、注册等等，统一部署，一个进程 all in one的架构方式，把所有的功能单元放在一个应用里。然后把整个应用部署到一台服务器上。如果负载能力不行，将整个应用进行水平复制，进行扩展，然后通过负载均衡实现访问。 Java实现：JSP、Servlet，打包成一个jar、war部署易于开发和测试:也十分方便部署;当需要扩展时，只需要将war复制多份，然后放到多个服务器 上，再做个负载均衡就可以了。 复杂性高，在业务规模和团队规模发展的一定阶段，多个模块耦合在一起，代码结构混乱，使得团队成员无人理解整个代码逻辑。 导致代码质量低，复杂性进一步增加。进一步导致重复代码越积越多。代码难以被修改和重构可靠性差，如果某个功能模块出问题，有可能引起整个应用的崩溃。修改Bug后，某模块功能修改或升级后，需要停掉整个服务，重新整体重新打包、部署这个应用war包，功能模块相互之间耦合度高,相互影响,不适合当今互联网业务功能的快速迭代。 交付效率低，构建和部署耗时长，编译耗时变长，开发调试将大部分时间花在重新编译上，难以定位问题，开发效率低。 伸缩性(scalable)差,单体只能按整体横向扩展，无法分模块垂直扩展。 总结: 架构简单,部署方便,打包编译部署升级效率低下,各功能耦合度高,扩展困难,扩缩容不灵活,适合小型简单项目

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/01-evolution-of-software-architecture.html' | relative_url }}">← Previous: Evolution of Software Architecture</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/03-model-view-controller-mvc.html' | relative_url }}">Next: Model-View-Controller (MVC) →</a>
</nav>
