---
layout: default
title: 首页
---

# 你好，我是 Bowenzheng686

欢迎来到我的个人主页。

这里记录我的技术学习、项目实践与日常思考。

## 关于我

这里可以填写你的个人介绍，例如正在学习的内容、
感兴趣的技术方向，以及希望分享的项目。

## 我的 GitHub

[访问我的 GitHub 主页](https://github.com/bowenzheng686)

## 最新文章

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url | relative_url }}) · {{ post.date | date: "%Y-%m-%d" }}
{% else %}
第一篇文章正在准备中。
{% endfor %}
