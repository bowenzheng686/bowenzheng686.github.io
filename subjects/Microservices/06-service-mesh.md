---
layout: default
title: "Microservices · Service Mesh"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Microservices Index]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 06 Service Mesh
### 1.6 服务网格 Mesh

从软件层面独力应对微服务架构问题，发展到软、硬一体，合力应对架构问题的时代，此即为“后微服务时代”。

当虚拟化的基础设施从单个服务的容器扩展至由多个容器构成的服务集群、通信网络和存储设施时，软件与硬件的界限便已经模糊。一旦虚拟化的硬件能够跟上软件的灵活性，那些与业务无关的技术性问题便有可能从软件层面剥离，悄无声息地解决于硬件基础设施之内，让软件得以只专注业务，真正“围绕业务能力构建”团队与产品。从软件层面独力应对分布式架构所带来的各种问题，发展到应用代码与基础设施软、硬一体，合力应对架构问题的时代，现在常被媒体冠以“云原生”这个颇为抽象的名字加以宣传。云原生时代与此前微服务时代中追求的目标并没有本质改变，在服务架构演进的历史进程中，可称为“后微服务时代”。

传统 Spring Cloud 与 Kubernetes 提供的解决方案对比

Kubernetes Spring Cloud

弹性伸缩 Autoscaling N/A

服务发现 KubeDNS / CoreDNS Spring Cloud Eureka,Nacos

配置中心 ConfigMap / Secret Spring Cloud Config

服务网关 Ingress Controller Spring Cloud Zuul

负载均衡 Load Balancer Spring Cloud Ribbon

服务安全 RBAC API Spring Cloud Security

跟踪监控 Metrics API / Dashboard Spring Cloud Turbine

降级熔断 N/A Spring Cloud Hystrix

Kubernetes 成为容器战争胜利者标志着后微服务时代的开端，但 Kubernetes 仍然没有能够完美解决全部的分布式问题

“不完美”的意思是，仅从功能上看，单纯的 Kubernetes 反而不如之前的 Spring Cloud 方案。这是因为有一些问题处于应用系统与基础设施的边缘，使得完全在基础设施层面中确实很难精细化地处理。

而 Spring Cloud 的解决方法比较重，学习和交付的成本比较高，需要花更多的精力关注和配置和业务无关的功能实现

为了解决这一类问题，虚拟化的基础设施很快完成了第二次进化，引入了今天被称为“服务网格”（Service Mesh）的“边车代理模式” （Sidecar Proxy）

所谓的“边车”是一种带垮斗的三轮摩托，这个场景里指的具体含义是由系统自动在服务容器（通常是指 Kubernetes 的 Pod）中注入一个通信代理服务器，相当于那个挎斗，以类似网络安全里中间人攻击的方式进行流量劫持，在应用毫无感知的情况下，悄然接管应用所有对外通信。

这个代理除了实现正常的服务间通信外（称为数据平面通信），还接收来自控制器的指令（称为控制平面通信），根据控制平面中的配置， 对数据平面通信的内容进行分析处理，以实现熔断、认证、度量、监控、负载均衡等各种附加功能。这样便实现了既不需要在应用层面加入额外的处理代码，也提供了几乎不亚于程序代码的精细管理能力。

很难从概念上判定清楚一个与应用系统运行于同一资源容器之内的代理服务到底应该算软件还是算基础设施，但它对应用是透明的，不需要改动任何软件代码就可以实现服务治理，这便足够了。

服务网格在 2018 年才火起来，今天它仍然是个新潮的概念，仍然未完全成熟，甚至连 Kubernetes 也还算是个新生事物。相信未来 Kubernetes 将会成为服务器端标准的运行环境，如同现在 Linux 系统服务网格将会成为微服务之间通信交互的主流模式，把“选择什么通信协议”、“怎样调度流量”、“如何认证授权”之类的技术问题隔离于程序代码之外，取代今天 Spring Cloud 全家桶中大部分组件的功能，微服务只需要考虑业务本身的逻辑，这才是最理想的Smart Endpoints解决方案。

业务与技术完全分离，远程与本地完全透明

服务网格 Mesh 的代表技术为Istio,Envoy,Linkerd,Consul Connect,AWS App Mesh等

Kuberetes 结合 ISTIO和Envoy 是实现 Service Mesh的主流方案

服务网格 Mesh 优势

把原本程序员需要关注的安全策略、负载均衡。流量控制、路由选择等基础能力下沉到了底层组件中，并提供了自动恢复的能力，让开发人员只需关注业务本身即可提供各类服务编排,和服务调用的一整套完整解决方案，不仅仅针对JAVA语言写的服务,可以支持任何语言提供了更灵活，可观察和安全的云原生解决方案，可以适应更复杂的应用程序需求结合Kubernetes的相关云原生技术是未来的发展趋势

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/05-microservices.html' | relative_url }}">← Previous: Microservices</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/07-serverless-architecture.html' | relative_url }}">Next: Serverless Architecture →</a>
</nav>
