---
layout: default
title: "Docker 容器技术 · 使用 Json 格式文件"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Docker 容器技术目录]({{ '/subjects/Docker/' | relative_url }})

{% raw %}

# 27 使用 Json 格式文件
### 5.10 使用 Json 格式文件

Compose 配置通常写成 YAML。JSON 是 YAML 的子集；使用 JSON 文件时需通过 `-f` 指定，而不是把命令提示符、安装输出和配置内容混在同一个代码块中。下面以一个 Redis 服务说明两种写法。

`compose.yaml`：

```yaml
services:
  redis:
    image: redis:7.2.5-alpine
```

对应的 `compose.json`：

```json
{
  "services": {
    "redis": {
      "image": "redis:7.2.5-alpine"
    }
  }
}
```

现代 Docker Compose 可以输出解析后的 JSON 配置；这与手工维护一份 JSON 文件不是同一回事：

```bash
docker compose -f compose.yaml config --format json > compose.generated.json
docker compose -f compose.json config    # 先验证 JSON 配置
docker compose -f compose.json up -d
docker compose -f compose.json ps
docker compose -f compose.json down
```

`config` 会解析变量并规范化配置，因此输出不保证与原文件逐字相同。不要在同一个项目里同时用 YAML 和 JSON 文件启动两套同名服务；选择一份配置作为维护源即可。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Docker/26-converting-between-docker-run-and-compose.html' | relative_url }}">← 上一篇：docker run 与 Compose 转换</a>
  <a href="{{ '/subjects/Docker/' | relative_url }}">返回 Docker 容器技术目录</a>
  <a href="{{ '/subjects/Docker/28-official-docker-hub.html' | relative_url }}">下一篇：Docker Hub →</a>
</nav>
