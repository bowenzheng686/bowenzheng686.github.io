---
layout: default
title: "微服务架构 · Spring Cloud Gateway 开发"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 36 Spring Cloud Gateway 开发

本篇先建立一条**固定地址**路由，确认 Gateway 自身工作，再把目标改成服务发现地址。这样遇到 404 或 503 时，能分清是路径匹配、过滤器还是注册中心的问题。

## 1. 选择兼容依赖

在已有 Spring Boot 项目中引入与当前 Spring Cloud 发布列车兼容的 Gateway starter。下例是原资料使用的 WebFlux Gateway 依赖形式；若所选版本已调整 starter 名称，应按该版本官方文档确认，不要混用 MVC Gateway 和 WebFlux Gateway 的配置。

```xml
<dependency>
  <groupId>org.springframework.cloud</groupId>
  <artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

依赖版本由项目的 Spring Cloud BOM 管理。若要使用 `lb://`，还需服务发现适配及 Spring Cloud LoadBalancer；不需要先连接 Nacos 才能验证固定地址路由。

## 2. 写一条可观察的路由

假设后端在 `127.0.0.1:9201` 提供 `GET /ping`，网关监听 8080。配置文件 `src/main/resources/application.yml` 应保留如下层级：

```yaml
server:
  port: 8080

spring:
  application:
    name: gateway-demo
  cloud:
    gateway:
      routes:
        - id: backend-api
          uri: http://127.0.0.1:9201
          predicates:
            - Path=/api/**
          filters:
            - StripPrefix=1
```

先直接访问 `http://127.0.0.1:9201/ping`，再访问 `http://127.0.0.1:8080/api/ping`。两者应落到同一后端接口；如果网关返回 404，检查 Path 断言和后端路径；若返回连接错误，检查目标服务是否运行。原资料中的 YAML 全部丢失缩进，直接复制将无法加载。

## 3. 启动类与验证

```java
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GatewayDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayDemoApplication.class, args);
    }
}
```

这是 Java 源码，不应标注为 JSON。启动日志出现应用运行只证明网关进程已起来；仍需发起请求验证路由。若要切换成服务发现，把 `uri` 改为 `lb://myapp-api`，确认注册中心有健康的 `myapp-api` 实例、网关拥有相应依赖，并验证客户端到注册中心的连接。下一篇展示多条路由和业务项目中的注意点。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/35-spring-cloud-gateway-core-concepts.html' | relative_url }}">← 上一篇：Spring Cloud Gateway 核心概念</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/Microservices/37-spring-cloud-gateway-practical-examples.html' | relative_url }}">下一篇：Spring Cloud Gateway 实战案例 →</a>
</nav>
