---
layout: default
title: "ELK 日志分析 · 使用 Kibana"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 22 使用 Kibana
### 5.3 使用 Kibana

### 5.3.1 首次连接与登录

Kibana 8.x 及更新版本在启用 Elasticsearch 安全功能时，通常可通过 enrollment 流程完成首次连接。在 Elasticsearch 节点生成短时有效的 Kibana enrollment token，并在 Kibana 节点的交互向导中输入；**不要把令牌贴进教程、日志或公开仓库**。

```bash
# 在 Elasticsearch 节点生成一次性令牌
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana

# 在 Kibana 节点检查启动与首次配置提示
sudo systemctl status kibana --no-pager
sudo journalctl -u kibana -n 50 --no-pager
```

在浏览器访问实际的 Kibana 地址，按界面提示完成 enrollment 和验证，再用具备相应权限的 Elasticsearch 用户登录。`0.0.0.0` 是监听地址，不是供浏览器访问的主机名；若从其他机器访问，应配置受控入口及 HTTPS。具体向导与命令随版本变化，使用当前版本文档核对。

![ELK 日志分析第 337 页插图](assets/img-444087d8fb3c9625.webp)

![ELK 日志分析第 337 页插图](assets/img-3a195daec793554b.webp)

![ELK 日志分析第 338 页插图](assets/img-a126b91880e120bc.webp)

完成连接后，用已配置的用户账号登录，并确认 Kibana 显示的是预期的 Elasticsearch 集群。

![ELK 日志分析第 338 页插图](assets/img-24f141c085b2f62e.webp)

![ELK 日志分析第 339 页插图](assets/img-508fee1d61d765c8.webp)

### 5.3.2 对照不同版本的界面

下面截图来自多个版本，菜单与图标可能不同。遇到提示时先核对浏览器访问地址、Kibana 日志以及 Elasticsearch 连接状态，不应把“禁用安全功能”当成解决登录问题的默认步骤。

![ELK 日志分析第 339 页插图](assets/img-56a8d993cee043d1.webp)

新版界面示例：

![ELK 日志分析第 340 页插图](assets/img-9bd3eafce1388641.webp)

![ELK 日志分析第 340 页插图](assets/img-43650c72b2d657da.webp)

![ELK 日志分析第 341 页插图](assets/img-b45f9ab0d96e1372.webp)

![ELK 日志分析第 341 页插图](assets/img-2e018019c0a10a08.webp)

![ELK 日志分析第 342 页插图](assets/img-5ae32ccfe4431a2c.webp)

![ELK 日志分析第 342 页插图](assets/img-8a50193d4d21a55a.webp)

![ELK 日志分析第 342 页插图](assets/img-d0ee6c0fe1926293.webp)

旧版界面示例：

![ELK 日志分析第 343 页插图](assets/img-45b0fdf48aae7902.webp)

查看服务状态时，可访问实际 Kibana 主机上的 `/status` 路径；页面是否可见仍受当前认证和权限控制。

![ELK 日志分析第 343 页插图](assets/img-355fecfebb10da74.webp)

![ELK 日志分析第 344 页插图](assets/img-481e2fae254bdc0e.webp)

### 5.3.3 使用 Dev Tools 验证索引

Dev Tools 的 Console 用于向 Elasticsearch 发送 API 请求。如果 `demo-readers` 尚不存在，先执行本节后面的写入示例，再回到查询命令；不要在生产集群上用无条件的 `_search` 扫描所有索引。

![ELK 日志分析第 344 页插图](assets/img-53bf9b9cf5c832fd.webp)

先查询目标索引的少量文档：

```text
GET /demo-readers/_search?size=5
```

![ELK 日志分析第 345 页插图](assets/img-fdef032d222b643b.webp)

也可以明确写出查询条件：

```text
GET /demo-readers/_search
{
  "query": { "match_all": {} },
  "size": 5
}
```

![ELK 日志分析第 345 页插图](assets/img-ad0ea81ede544721.webp)

![ELK 日志分析第 346 页插图](assets/img-79c00d9a429c0ce7.webp)

若演示索引尚不存在，可以先写入一条文档，再查询。写入会由 Elasticsearch 按当前设置创建索引；正式业务应预先设计映射与模板。

```json
PUT /demo-readers/_doc/1
{
  "username": "example",
  "age": 18,
  "title": "engineer"
}
```

![ELK 日志分析第 346 页插图](assets/img-c723a17b0453946c.webp)

按 ID 读取刚写入的文档：

```text
GET /demo-readers/_doc/1
```

![ELK 日志分析第 347 页插图](assets/img-5fcd598e5e1004b4.webp)

### 5.3.4 创建数据视图

Kibana 较新版本把“索引模式”称为“数据视图”。有了 `demo-readers` 索引后，可创建匹配 `demo-readers*` 的数据视图。该演示文档没有时间字段，创建时应选择“不使用时间筛选器”；日志类数据若有 `@timestamp`，则应选正确的时间字段。

新版界面示例：

![ELK 日志分析第 347 页插图](assets/img-b8dd88d94c6b691d.webp)

![ELK 日志分析第 348 页插图](assets/img-ce09c74c7e1a83f1.webp)

![ELK 日志分析第 348 页插图](assets/img-d05458be8b9c7d06.webp)

![ELK 日志分析第 349 页插图](assets/img-6f3f518dbeaeb250.webp)

旧版“索引模式”界面示例：

![ELK 日志分析第 349 页插图](assets/img-05444e95d53581e6.webp)

创建数据视图后，在 Discover 中选择它，并核对时间范围和筛选条件，再查看已写入的文档。

![ELK 日志分析第 350 页插图](assets/img-07dcbde402ad252b.webp)

![ELK 日志分析第 350 页插图](assets/img-16492993271150e3.webp)

数据视图可使用通配符匹配一组有相同字段结构的索引；不要用过宽的 `*` 将无关数据混在一起。

![ELK 日志分析第 351 页插图](assets/img-d5acb81ccdb50818.webp)

![ELK 日志分析第 351 页插图](assets/img-dcdc8fb778ff8b31.webp)

![ELK 日志分析第 351 页插图](assets/img-3d61b07bc62ec898.webp)

![ELK 日志分析第 352 页插图](assets/img-c62f173f88303e63.webp)

![ELK 日志分析第 352 页插图](assets/img-59b8f93de8300c34.webp)

### 5.3.5 排查“看不到数据”

若 Discover 没有显示柱状图或文档，先确认 Elasticsearch 中是否确有数据、当前数据视图是否匹配索引、时间字段与查询时间范围是否正确，再检查用户权限。本文的 `demo-readers` 无时间字段，因而不应期待按时间生成的直方图；不必通过安装无关软件来制造日志。

![ELK 日志分析第 353 页插图](assets/img-4adc5f61fff77508.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/21-installing-and-configuring-kibana.html' | relative_url }}">← 上一篇：安装并配置 Kibana</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/23-securing-kibana-login-with-nginx.html' | relative_url }}">下一篇：通过 Nginx 实现 Kibana 登录安全认证 →</a>
</nav>
