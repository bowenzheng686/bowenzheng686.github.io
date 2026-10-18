---
layout: default
title: "ELK 日志分析 · Kibana 可视化画图功能"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 24 Kibana 可视化画图功能
### 5.5 Kibana 可视化功能

https://www.elastic.co/guide/cn/kibana/current/introduction.html

Kibana 可基于 Elasticsearch 中可检索的字段创建图表，并不要求原始日志文件本身一定是 JSON；关键在于采集后字段已正确解析、映射类型适合聚合，且数据视图与时间范围正确。以下截图跨越不同 Kibana 版本，操作入口可能变化，阅读时重点理解每种图表要回答的问题。

### lens 可视化

Lens 适合从数据视图中拖拽字段，快速尝试维度和指标。开始前先确认目标字段是可聚合的数值、关键字或日期类型，再保存图表供仪表板复用。

![ELK 日志分析第 355 页插图](assets/img-68e3559bca965efe.webp)

![ELK 日志分析第 356 页插图](assets/img-ee292623a544c05a.webp)

### 垂直条形图

垂直条形图适合比较各客户端 IP 的访问次数：横轴使用 IP 分组，纵轴用文档计数。若字段被映射为 `text`，应选择可聚合的 `keyword` 子字段；同时注意高基数 IP 排行的查询成本。

下图为 8.x 版本界面：

![ELK 日志分析第 356 页插图](assets/img-a85c916d14244df9.webp)

下列截图为 7.x 版本的配置与结果：

![ELK 日志分析第 357 页插图](assets/img-c6cc86dbcd3d234c.webp)

![ELK 日志分析第 357 页插图](assets/img-81fc10f470bd21c6.webp)

![ELK 日志分析第 357 页插图](assets/img-7c46b4e7ab3f9339.webp)

![ELK 日志分析第 358 页插图](assets/img-2f8fc53bd49e3dd5.webp)

![ELK 日志分析第 358 页插图](assets/img-c526326cec2700ca.webp)

### 水平条形图

水平条形图与垂直条形图使用相同的聚合思路，更适合展示较长的类别名称或前 N 名排行。

8.x 版本界面：

![ELK 日志分析第 359 页插图](assets/img-534ed2bbda7a439b.webp)

7.x 版本界面：

![ELK 日志分析第 359 页插图](assets/img-a2f682a072eacfc6.webp)

![ELK 日志分析第 360 页插图](assets/img-9b4269acf432e8bc.webp)

![ELK 日志分析第 360 页插图](assets/img-34cadb65d0afaca8.webp)

### Markdown

Markdown 面板用于给仪表板添加标题、说明或操作提示，不应把它当作实时数据表。以下仅是静态排版示例：

![ELK 日志分析第 361 页插图](assets/img-bd06ae96a811366c.webp)

```text
## 工作安排
| 时间  |姓名| 联系电话     |
| ---- | ---- | ---- |
| 周一 | user1 | 1234567890 |
| 周二 | user2 | 1234567890 |
| 周三 | user3 | 1234567890 |
| 周四 | user4 | 1234567890 |
| 周五 | user5 | 1234567890 |
| 周六 | user6 | 1234567890 |
| 周日 | user7 | 1234567890 |
```

![ELK 日志分析第 361 页插图](assets/img-0fedc670bb9c3957.webp)

![ELK 日志分析第 362 页插图](assets/img-e4baa49d9e6908ee.webp)

### 仪表盘图

仪表盘式图形适合显示单个数值相对于目标值的进度，例如当前错误率与告警阈值。使用前先定义单位和阈值，避免颜色看起来“危险”却没有业务含义。

8.x 版本界面：

![ELK 日志分析第 362 页插图](assets/img-9d48667803b3094b.webp)

7.x 版本界面：

![ELK 日志分析第 363 页插图](assets/img-7754e79fd06866d1.webp)

![ELK 日志分析第 363 页插图](assets/img-159f4d92b89611db.webp)

![ELK 日志分析第 363 页插图](assets/img-8c49bc3123e74bfa.webp)

![ELK 日志分析第 364 页插图](assets/img-262d2da31e41a391.webp)

![ELK 日志分析第 364 页插图](assets/img-c26194c118b6a80e.webp)

### 热力图

热力图用颜色表示两个维度组合下的数量或强度，例如小时与星期几组成的访问量矩阵。下列 8.x 截图使用内置示例数据；先导入示例数据，再选择合适的时间字段和指标，不能把示例的地理分布直接解释为真实业务流量。

导入示例数据：

![ELK 日志分析第 365 页插图](assets/img-0df818b3f11dfbf6.webp)

![ELK 日志分析第 365 页插图](assets/img-c649ea103fd11660.webp)

选择数据视图、行列维度与颜色指标，创建图形：

![ELK 日志分析第 366 页插图](assets/img-c3e9e58f0f657da2.webp)

![ELK 日志分析第 366 页插图](assets/img-f32139ddfc787c94.webp)

![ELK 日志分析第 367 页插图](assets/img-75c65bbd63787351.webp)

![ELK 日志分析第 367 页插图](assets/img-45db77d4fb157875.webp)

![ELK 日志分析第 368 页插图](assets/img-234cbabcb329c307.webp)

![ELK 日志分析第 368 页插图](assets/img-9496df00ba98c0ba.webp)

![ELK 日志分析第 369 页插图](assets/img-390ede9bb960b54f.webp)

![ELK 日志分析第 369 页插图](assets/img-7a5152d4b8f835e8.webp)

![ELK 日志分析第 370 页插图](assets/img-517395cbfdc44eb3.webp)

下面是 7.x 的对应界面：

![ELK 日志分析第 370 页插图](assets/img-9a07b84e7be5e6b7.webp)

![ELK 日志分析第 370 页插图](assets/img-13693316208f0092.webp)

![ELK 日志分析第 371 页插图](assets/img-2e4dd26d0b7e0bdf.webp)

![ELK 日志分析第 371 页插图](assets/img-36401a1e7d68bb31.webp)

### 面积图

面积图突出随时间变化的累计量或趋势；多序列堆叠时需说明各序列是否可以相加，否则容易误读总量。

8.x 版本界面：

![ELK 日志分析第 372 页插图](assets/img-136dc6b2033c4074.webp)

7.x 版本界面：

![ELK 日志分析第 372 页插图](assets/img-0cc9d27e2c74fc2a.webp)

![ELK 日志分析第 373 页插图](assets/img-193960fd82544b9c.webp)

![ELK 日志分析第 373 页插图](assets/img-305b7617526d6f8d.webp)

![ELK 日志分析第 374 页插图](assets/img-bbcd404a26fe15ac.webp)

### 饼状图

饼图适合少量类别的占比比较。类别过多或差距较小时改用条形图，并让读者能看到分母与时间范围。

![ELK 日志分析第 374 页插图](assets/img-033f47d9b024dce3.webp)

![ELK 日志分析第 375 页插图](assets/img-193960fd82544b9c.webp)

![ELK 日志分析第 375 页插图](assets/img-9a63c03769a3e410.webp)

![ELK 日志分析第 376 页插图](assets/img-bea150f3c4fe4950.webp)

### 数据表 Datatable

数据表适合列出分组统计的精确数值，与上面的图形互补。

![ELK 日志分析第 377 页插图](assets/img-ca4e10d82f2a5c6c.webp)

如需进一步分析，可使用当前版本提供的导出功能；导出权限、行数限制和字段脱敏策略应事先确认。

### 线图 Line Chart

折线图适合对比一段时间内的指标趋势。选择合理的时间粒度，避免把采样间隔变化误解为业务突增。

8.x 版本界面：

![ELK 日志分析第 378 页插图](assets/img-970c5cdacd2d03f5.webp)

![ELK 日志分析第 378 页插图](assets/img-8adac7594329a086.webp)

7.x 版本界面：

![ELK 日志分析第 379 页插图](assets/img-0931a6d9e72a10f8.webp)

保存图表时使用能说明指标、维度和时间粒度的名称，后续才容易在仪表板中复用。

### 标签云图

标签云可快速展示高频词或类别，但字体大小不利于精确比较；需要排序和具体数值时应切换到条形图或数据表。

![ELK 日志分析第 380 页插图](assets/img-8bfe743dc074e2af.webp)

![ELK 日志分析第 380 页插图](assets/img-c0689ebf34439cf5.webp)

### 地图

地图依赖地理字段（如 `geo_point`）及正确的 IP 地理位置解析。没有地理字段时，单纯把字符串 IP 放进地图不会产生可靠位置。

![ELK 日志分析第 381 页插图](assets/img-8ce6117e52f601c1.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/23-securing-kibana-login-with-nginx.html' | relative_url }}">← 上一篇：通过 Nginx 实现 Kibana 登录安全认证</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/25-building-kibana-dashboards.html' | relative_url }}">下一篇：Kibana 实现 Dashboard 仪表盘 →</a>
</nav>
