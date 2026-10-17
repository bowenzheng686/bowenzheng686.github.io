---
layout: default
title: "ELK Log Analytics · Kibana Visualizations"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 24 Kibana Visualizations
### 5.5.Kibana 可视化画图功能

https://www.elastic.co/guide/cn/kibana/current/introduction.html

Kibana支持多种图形展示功能，需要日志是json格式的支持，具体如下：

### lens 可视化

![ELK 日志分析第 355 页插图](assets/img-68e3559bca965efe.png)

![ELK 日志分析第 356 页插图](assets/img-ee292623a544c05a.png)

### 垂直条形图

显示访问次数最多的客户端IP

8.X

![ELK 日志分析第 356 页插图](assets/img-a85c916d14244df9.png)

7.X

![ELK 日志分析第 357 页插图](assets/img-c6cc86dbcd3d234c.png)

![ELK 日志分析第 357 页插图](assets/img-81fc10f470bd21c6.png)

![ELK 日志分析第 357 页插图](assets/img-7c46b4e7ab3f9339.png)

![ELK 日志分析第 358 页插图](assets/img-2f8fc53bd49e3dd5.png)

![ELK 日志分析第 358 页插图](assets/img-c526326cec2700ca.png)

### 水平条形图

8,X

![ELK 日志分析第 359 页插图](assets/img-534ed2bbda7a439b.png)

7.X

![ELK 日志分析第 359 页插图](assets/img-a2f682a072eacfc6.png)

![ELK 日志分析第 360 页插图](assets/img-9b4269acf432e8bc.png)

![ELK 日志分析第 360 页插图](assets/img-34cadb65d0afaca8.png)

### Markdown

![ELK 日志分析第 361 页插图](assets/img-bd06ae96a811366c.png)

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

![ELK 日志分析第 361 页插图](assets/img-0fedc670bb9c3957.png)

![ELK 日志分析第 362 页插图](assets/img-e4baa49d9e6908ee.png)

### 仪表盘图

8.X

![ELK 日志分析第 362 页插图](assets/img-9d48667803b3094b.png)

7.X

![ELK 日志分析第 363 页插图](assets/img-7754e79fd06866d1.png)

![ELK 日志分析第 363 页插图](assets/img-159f4d92b89611db.png)

![ELK 日志分析第 363 页插图](assets/img-8c49bc3123e74bfa.png)

![ELK 日志分析第 364 页插图](assets/img-262d2da31e41a391.png)

![ELK 日志分析第 364 页插图](assets/img-c26194c118b6a80e.png)

### 热力图

8.X 版

使用内置的样例数据实现 一天中的全球用户的访问热度

先导入样例数据

![ELK 日志分析第 365 页插图](assets/img-0df818b3f11dfbf6.png)

![ELK 日志分析第 365 页插图](assets/img-c649ea103fd11660.png)

创建图形

![ELK 日志分析第 366 页插图](assets/img-c3e9e58f0f657da2.png)

![ELK 日志分析第 366 页插图](assets/img-f32139ddfc787c94.png)

![ELK 日志分析第 367 页插图](assets/img-75c65bbd63787351.png)

![ELK 日志分析第 367 页插图](assets/img-45db77d4fb157875.png)

![ELK 日志分析第 368 页插图](assets/img-234cbabcb329c307.png)

![ELK 日志分析第 368 页插图](assets/img-9496df00ba98c0ba.png)

![ELK 日志分析第 369 页插图](assets/img-390ede9bb960b54f.png)

![ELK 日志分析第 369 页插图](assets/img-7a5152d4b8f835e8.png)

![ELK 日志分析第 370 页插图](assets/img-517395cbfdc44eb3.png)

7.X版

![ELK 日志分析第 370 页插图](assets/img-9a07b84e7be5e6b7.png)

![ELK 日志分析第 370 页插图](assets/img-13693316208f0092.png)

![ELK 日志分析第 371 页插图](assets/img-2e4dd26d0b7e0bdf.png)

![ELK 日志分析第 371 页插图](assets/img-36401a1e7d68bb31.png)

### 面积图

8.X

![ELK 日志分析第 372 页插图](assets/img-136dc6b2033c4074.png)

7.X

![ELK 日志分析第 372 页插图](assets/img-0cc9d27e2c74fc2a.png)

![ELK 日志分析第 373 页插图](assets/img-193960fd82544b9c.png)

![ELK 日志分析第 373 页插图](assets/img-305b7617526d6f8d.png)

![ELK 日志分析第 374 页插图](assets/img-bbcd404a26fe15ac.png)

### 饼状图

![ELK 日志分析第 374 页插图](assets/img-033f47d9b024dce3.png)

![ELK 日志分析第 375 页插图](assets/img-193960fd82544b9c.png)

![ELK 日志分析第 375 页插图](assets/img-9a63c03769a3e410.png)

![ELK 日志分析第 376 页插图](assets/img-bea150f3c4fe4950.png)

### 数据表 Datatable

![ELK 日志分析第 377 页插图](assets/img-ca4e10d82f2a5c6c.png)

可以讲结果导出，再通过excel查看

### 线图 Line Chart

8.X

![ELK 日志分析第 378 页插图](assets/img-970c5cdacd2d03f5.png)

![ELK 日志分析第 378 页插图](assets/img-8adac7594329a086.png)

7.X

![ELK 日志分析第 379 页插图](assets/img-0931a6d9e72a10f8.png)

保存折线图

### 标签云图

![ELK 日志分析第 380 页插图](assets/img-8bfe743dc074e2af.png)

![ELK 日志分析第 380 页插图](assets/img-c0689ebf34439cf5.png)

### 地图

![ELK 日志分析第 381 页插图](assets/img-8ce6117e52f601c1.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/23-securing-kibana-login-with-nginx.html' | relative_url }}">← Previous: Securing Kibana Login with Nginx</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/25-building-kibana-dashboards.html' | relative_url }}">Next: Building Kibana Dashboards →</a>
</nav>
