---
layout: default
title: "ELK 日志分析 · 通过坐标地图统计网站访问用户的 IP 所在城市"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 28 通过坐标地图统计网站访问用户的 IP 所在城市
### 6.3 通过坐标地图统计网站访问用户的 IP 所在城市

本例在上一章 Filebeat → Kafka → Logstash → Elasticsearch 链路的访问日志上增加 GeoIP 富化，然后在 Kibana Maps 中按大致城市位置展示访问来源。**IP 地理位置只是数据库估计**，并非用户真实位置；NAT、代理、移动网络与 VPN 都可能造成偏差。地图能否使用，关键是 Elasticsearch 中位置字段映射为 `geo_point`，而不是索引名称是否以 `logstash` 开头。

### 6.3.1 选择 IP 数据库

Logstash 的 GeoIP 插件可使用其支持的数据库管理方式；是否自带数据库、更新策略和许可证要求会随版本变化，应查看[插件文档](https://www.elastic.co/guide/en/logstash/current/plugins-filters-geoip.html)。若自行下载 MaxMind GeoLite2，需遵守其账号、许可和更新要求，并把数据库文件放在 Logstash 服务用户可读取的位置。旧资料中的带令牌下载 URL 不应复制或继续使用，令牌可能泄露账号权限。

![ELK 日志分析第 410 页插图](assets/img-0814861dc8acf164.webp)

![ELK 日志分析第 410 页插图](assets/img-8fdfb44e3930ff77.webp)

![ELK 日志分析第 411 页插图](assets/img-b86f4d4bfb7a56fc.webp)

### 6.3.2 确认日志中有客户端 IP

先检查 Nginx JSON 日志是否包含有效的客户端 IP 字段，例如 `clientip`。如果 Nginx 在反向代理之后，应先建立可信代理链，避免把代理 IP 当成用户 IP；不要盲目信任客户端自行传入的 `X-Forwarded-For`。Filebeat/Kafka 输入与上一章一致，这里只展示新增的 Logstash 过滤步骤。

### 6.3.3 在 Logstash 中富化位置

将下面过滤段加入现有 Logstash 管道；示例假定事件标签为 `nginx-access`，`clientip` 是一个可解析的 IP 字符串：

```text
filter {
  if "nginx-access" in [tags] and [clientip] {
    geoip {
      source => "clientip"
      target => "[client]"
      ecs_compatibility => "v8"
    }
  }
}
```

在 ECS 模式下，GeoIP 可生成 `[client][geo][location]` 等字段。若使用自定义 MMDB 文件，再按当前插件文档增加 `database` 路径；不要复制旧示例里带 JRuby gem 版本号的安装目录。也不必把经纬度手工拼成 float 数组，再期望 Kibana 自动识别为地理点。

### 6.3.4 先定义映射，再写入新数据

为匹配 `logs-nginx-access-*` 的新索引定义位置字段类型。在 Kibana Dev Tools 执行：

```http
PUT /_index_template/nginx-access-geo
{
  "index_patterns": ["logs-nginx-access-*"],
  "template": {
    "mappings": {
      "properties": {
        "client": {
          "properties": {
            "geo": {
              "properties": {
                "location": { "type": "geo_point" }
              }
            }
          }
        }
      }
    }
  }
}
```

模板只作用于之后创建的匹配索引，**不会修改已有索引字段类型**。如历史索引映射错误，应规划新索引与 reindex，并验证数据后再切换数据视图；不应为了“让地图显示”直接删除原索引。写入新文档后检查 `client.geo.location` 的映射和值，确认 GeoIP 解析失败记录没有被误用。

### 6.3.5 验证索引与数据视图

先在 Elasticsearch 查看新索引的映射和几条实际文档，确认 `client.geo.location` 是 `geo_point` 且有可用坐标。原截图使用 Head 插件展示索引；当前版本也可用 Kibana Dev Tools 或 API 完成检查。

```http
GET /logs-nginx-access-*/_mapping/field/client.geo.location
GET /logs-nginx-access-*/_search?size=3
```

![ELK 日志分析第 414 页插图](assets/img-0eaffd9486e28382.webp)

![ELK 日志分析第 414 页插图](assets/img-eee7d856c2bb5118.webp)

在 Kibana 创建匹配 `logs-nginx-access-*` 的数据视图，并选择真实日志时间字段（通常是 `@timestamp`）。查看字段列表时，不只确认出现了字段名，还应检查 `client.geo.location` 的类型与最近文档的坐标值。以下截图同时包含旧版“索引模式”和新版“数据视图”界面，菜单名称可能变化。

![ELK 日志分析第 415 页插图](assets/img-142edcfb2fd5594e.webp)

![ELK 日志分析第 415 页插图](assets/img-4a271f5b4e5fe3bd.webp)

![ELK 日志分析第 416 页插图](assets/img-49d4f55811ee8c5f.webp)

![ELK 日志分析第 416 页插图](assets/img-99eac9efed087def.webp)

![ELK 日志分析第 416 页插图](assets/img-030d8d7334513f3c.webp)

![ELK 日志分析第 417 页插图](assets/img-6dc3819562eac53c.webp)

![ELK 日志分析第 417 页插图](assets/img-c7f7ca396b674530.webp)

### 6.3.6 在 Maps 中选择图层

Kibana Maps 可用地理点图层展示访问来源，也可按网格聚合生成热度图。先从 Kibana 自带示例地图熟悉底图、图层和时间筛选，再换成自己的访问日志数据视图；示例数据中的位置不代表真实访问者。

![ELK 日志分析第 418 页插图](assets/img-b629d9d9f5bf1871.webp)

![ELK 日志分析第 418 页插图](assets/img-f02db73677737b8c.webp)

![ELK 日志分析第 419 页插图](assets/img-f7e23359ee9c6501.webp)

![ELK 日志分析第 419 页插图](assets/img-b76850ced8376441.webp)

![ELK 日志分析第 420 页插图](assets/img-83b0832596c5e4d3.webp)

![ELK 日志分析第 420 页插图](assets/img-453775ffda43b886.webp)

![ELK 日志分析第 421 页插图](assets/img-0b8a62716d41d693.webp)

![ELK 日志分析第 421 页插图](assets/img-bfc17f6bda438b91.webp)

![ELK 日志分析第 422 页插图](assets/img-5b4cbbe0ce081e50.webp)

![ELK 日志分析第 422 页插图](assets/img-e22760f0d3eaa9a2.webp)

### 6.3.7 用访问日志创建地图

选择访问日志数据视图、`client.geo.location` 作为位置字段，再按访问次数设置点大小或热度。地图为空时按顺序检查：时间范围是否覆盖新日志、字段是否为 `geo_point`、GeoIP 解析是否成功、所选数据视图是否匹配新索引。下方 8.x 截图里出现的映射错误，是旧资料先写入 float 坐标、后修改模板造成的历史问题；前文先建模板再写数据即可避免它。不要为了修正映射直接删除原索引。

![ELK 日志分析第 423 页插图](assets/img-deed0f11582200bc.webp)

![ELK 日志分析第 423 页插图](assets/img-7aaf6eee66d3ab2a.webp)

![ELK 日志分析第 424 页插图](assets/img-93996a6243d11f59.webp)

![ELK 日志分析第 425 页插图](assets/img-7006c753b4871a16.webp)

![ELK 日志分析第 426 页插图](assets/img-be0b46e82c260fcf.webp)

![ELK 日志分析第 426 页插图](assets/img-9506605a81247dc7.webp)

![ELK 日志分析第 427 页插图](assets/img-36a06e8b42559149.webp)

![ELK 日志分析第 427 页插图](assets/img-0e942d4cb79d1645.webp)

![ELK 日志分析第 427 页插图](assets/img-6e74d91e1ce803b9.webp)

![ELK 日志分析第 428 页插图](assets/img-e7be2096a02a16fc.webp)

![ELK 日志分析第 428 页插图](assets/img-935cea5de5f8300e.webp)

![ELK 日志分析第 429 页插图](assets/img-3dc418d5ccb1fc5a.webp)

![ELK 日志分析第 429 页插图](assets/img-431e07971aa8ae55.webp)

![ELK 日志分析第 430 页插图](assets/img-a893ddd74c330b79.webp)

![ELK 日志分析第 430 页插图](assets/img-6f21ac8e377df428.webp)

![ELK 日志分析第 431 页插图](assets/img-0585d21b47588474.webp)

![ELK 日志分析第 431 页插图](assets/img-b9465ec235fe4d20.webp)

下面的 7.x 截图用于对照旧界面。无论界面版本，地图图层仍需要 Elasticsearch 可识别的地理字段；“7.x 只支持 float、8.x 才支持 geo_point”并不准确。

![ELK 日志分析第 432 页插图](assets/img-137c3d3fd9ee937b.webp)

![ELK 日志分析第 432 页插图](assets/img-9eee030c16fc9e03.webp)

![ELK 日志分析第 433 页插图](assets/img-a361a1bfd67e6414.webp)

![ELK 日志分析第 433 页插图](assets/img-8ce6117e52f601c1.webp)

![ELK 日志分析第 434 页插图](assets/img-ad21227f04684a5b.webp)

地图底图使用的瓦片服务与 IP 定位数据库是两回事。若要更换底图语言或供应商，应核对当前 Kibana Maps 的配置文档、服务条款、网络可达性和 HTTPS 支持，不要直接复制旧版 HTTP 瓦片 URL。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/27-collecting-nginx-logs-with-filebeat-and-kafka-buffering.html' | relative_url }}">← 上一篇：Filebeat 收集Nginx日志并写入 Kafka 缓存发送至 Elasticsearch</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/29-writing-collected-logs-to-mysql-with-logstash.html' | relative_url }}">下一篇：Logstash收集日志写入 MySQL 数据库 →</a>
</nav>
