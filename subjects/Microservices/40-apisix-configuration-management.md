---
layout: default
title: "微服务架构 · APISIX 配置管理"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回微服务架构目录]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 40 APISIX 配置管理

APISIX 有两类配置，修改方式不同：**进程与部署配置**写在 `conf/config.yaml`，例如监听端口、etcd 端点和 Admin API 的访问边界；**动态资源配置**通过 Admin API、Dashboard 或控制器管理，例如 Route、Upstream 与插件，传统模式下持久化到 etcd。不要把每条路由手工写进自动生成的 `nginx.conf`。

## 静态配置从哪里读取

`conf/config-default.yaml` 是软件附带的默认值，升级时可能变化，不应直接修改。`conf/nginx.conf` 由 APISIX 生成，也不应直接编辑。用户覆盖项写入 `conf/config.yaml`；某些版本支持启动时用 `-c` 指定其他文件，命令和语法应按目标版本检查。

以下以原资料使用的 APISIX 3.x 传统部署为例，展示有效的 YAML 层级。实际字段及默认值要与所安装发行包的 `config-default.yaml` 核对：

```yaml
apisix:
  node_listen: 8000

deployment:
  role: traditional
  role_traditional:
    config_provider: etcd
  etcd:
    host:
      - http://ETCD_HOST:2379
  admin:
    admin_key:
      - name: admin
        key: REPLACE_WITH_STRONG_RANDOM_KEY
        role: admin
```

`node_listen` 改的是**业务代理入口**，不是 Admin API。etcd 地址必须从 APISIX 进程所在网络可达；容器里写 `127.0.0.1:2379` 通常指向 APISIX 容器自己，而不是另一台 etcd 容器。管理密钥应通过安全配置渠道提供，示例中的占位符不可直接上线。

修改文件后先备份旧配置、运行 `apisix test`，再用当前进程管理方式重新加载或重启并查看日志。变更 etcd 端点前应确认新端点健康且保留了现有动态配置；只把 APISIX 指向一个空的 etcd，原有路由不会凭空迁移过去。

## Admin API 的认证和访问范围

Admin API 通常监听 9180，用于创建和修改动态资源。推荐用请求头传密钥，而不是把 key 放在 URL 查询参数里，因为 URL 容易进入代理日志和命令记录：

```bash
curl -H 'X-API-KEY: REPLACE_WITH_STRONG_RANDOM_KEY' \
  http://127.0.0.1:9180/apisix/admin/routes
```

看到 `{"list":[],"total":0}` 表示请求通过认证，但当前没有路由；它并不证明代理入口已经能转发业务请求。实际响应结构会随版本变化。轮换密钥时要同时更新 Dashboard、自动化发布工具等管理客户端，再撤销旧密钥并验证其失效。

原资料将 `admin_listen.ip: 0.0.0.0`、`allow_admin: 0.0.0.0/0`、默认密钥和 `enable_admin_cors: true` 放在一起，会扩大管理面暴露范围。若确需远程管理，应仅允许明确的管理网段，并使用网络策略、TLS、强密钥和审计；Dashboard 也不需要 Admin API 面向所有业务客户端开放。具体 `allow_admin` 与 `admin_listen` 结构应以目标版本配置模板为准。

## 用一条测试路由验证变更

静态配置生效后，检查监听端口和 etcd 连接；再通过 Admin API 创建一个指向已知测试上游的 Route。用业务入口 `http://GATEWAY_HOST:8000/<路径>` 发请求，确认命中上游。这样分别验证了“配置文件能加载”“管理接口能写入”“代理实例已收到动态配置”“业务转发正确”四个环节。下一篇介绍可选 Dashboard，之后再直接操作 Admin API。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/39-installing-apisix.html' | relative_url }}">← 上一篇：APISIX 安装</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/Microservices/41-installing-and-using-apisix-dashboard.html' | relative_url }}">下一篇：APISIX Dashboard 安装与使用 →</a>
</nav>
