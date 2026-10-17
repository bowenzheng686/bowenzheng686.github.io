---
layout: default
title: "ELK Log Analytics · Building Kibana Dashboards"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 25 Building Kibana Dashboards
### 5.6 Kibana 实现 Dashboard 仪表盘

### 先利用可视化功能实现多个图形

![ELK 日志分析第 381 页插图](assets/img-114a1ba168ba79ec.png)

### 创建仪表盘

![ELK 日志分析第 382 页插图](assets/img-4fc54b67452c204c.png)

![ELK 日志分析第 382 页插图](assets/img-b8614ebd75dfbd79.png)

![ELK 日志分析第 382 页插图](assets/img-c5233334857b23f8.png)

![ELK 日志分析第 383 页插图](assets/img-a41dbec5319a3d11.png)

大小和位置都可以调整

![ELK 日志分析第 383 页插图](assets/img-fe1e9f127a0b636f.png)

![ELK 日志分析第 384 页插图](assets/img-f4c25fa11f6fa078.png)

### 共享仪表盘图形

### 方式1: 固定链接

![ELK 日志分析第 384 页插图](assets/img-032d0db807558a13.png)

将复制下来的链接地址粘贴至浏览器地址栏,可以访问上面的图形

![ELK 日志分析第 385 页插图](assets/img-2fdb98872da801f6.png)

### 方式2: 嵌入代码

嵌入代码的共享

![ELK 日志分析第 385 页插图](assets/img-7b615b6adf82e5b8.png)

创建一个html文件,内容如下

```xml
[root@elk-web1 ~]#cat dashboard.html
<html>
<head>
<meta http-equiv=Content-Type content="text/html;charset=utf-8">
<title>kibana仪表盘</title>
</head>
<body>
<img src="http://www.bowen.com/wp-content/uploads/2017/09/logo.png" >
<h1 style="color:red">马哥教育运维ELK项目实战</h1>
<iframe src="http://10.0.0.101:5601/goto/a61616c93be1f64df580ee3f16828173?
embed=true" height="1024" width="1280"></iframe>
</body>
</html>
```

用浏览器打开此文件,可以看到下面显示

![ELK 日志分析第 386 页插图](assets/img-2d752eb0bd8d07dd.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/24-kibana-visualizations.html' | relative_url }}">← Previous: Kibana Visualizations</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/26-collecting-nginx-logs-with-filebeat-and-redis-buffering.html' | relative_url }}">Next: Collecting Nginx Logs with Filebeat and Redis Buffering →</a>
</nav>
