---
layout: default
title: "Microservices · Developing with Spring Cloud Gateway"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Microservices Index]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 36 Developing with Spring Cloud Gateway
### 7.3 Spring Cloud Gateway 开发

### 添加依赖

在pom.xml中添加下面的依赖

```xml
<!-- spring cloud gateway 依赖 -->
<dependency>
<groupId>org.springframework.cloud</groupId>
<artifactId>spring-cloud-starter-gateway</artifactId>
</dependency>
```

### 修改resources/application.yml 配置文件

修改resources/application.yml 配置文件,配置路由规则

```text
server:
port: 8080
spring:
application:
name: gateway-demo
cloud:
gateway:
routes:
# 系统模块
- id: gateway-system
#uri: http://localhost:9201/
uri: lb://myapp-api
predicates:
- Path=/api/**
filters:
- StripPrefix=1  #从请求路径中删除第一个前缀。
```

### 创建网关启动类

```json
@SpringBootApplication
public class GatewayDemoApplication
{
public static void main(String[] args)
{
SpringApplication.run(GatewayDemoApplication.class, args);
System.out.println("网关启动成功");
}
}
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/35-spring-cloud-gateway-core-concepts.html' | relative_url }}">← Previous: Spring Cloud Gateway Core Concepts</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/37-spring-cloud-gateway-practical-examples.html' | relative_url }}">Next: Spring Cloud Gateway Practical Examples →</a>
</nav>
