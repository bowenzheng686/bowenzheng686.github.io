---
layout: default
title: "Prometheus · 自定义指标与 Grafana 面板"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 09 自定义指标与 Grafana 面板

前两章介绍了 PromQL 的选择与运算，本章把它应用到自己的服务：**在代码中记录请求指标 → 暴露 `/metrics` → 让 Prometheus 抓取 → 用 PromQL 得到请求速率和耗时 → 在 Grafana 画图**。原资料把“业务请求地址”和“指标地址”都叫 `/metrics`，且使用两个端口，容易误以为访问指标端点会产生业务请求；下面改成一个服务端口、两个清楚的路径。

## 何时编写自定义指标

应用若已有官方客户端库，优先在应用内部埋点；无法修改的第三方服务可用 Exporter 转换已有状态；短时批处理任务再考虑 Pushgateway。自定义指标要有稳定名称、明确单位和有限的标签维度。不要按单个用户或请求 ID 打标签，也不要用循环疯狂请求来“制造监控数据”；验证时发送几次正常请求即可。

## Python：为 Web 请求埋点

下面用 Flask 与 `prometheus-client` 做一个可运行的教学例子。开发环境先建虚拟环境，再安装依赖；原资料同时列出 apt、pip、多个 virtualenv 工具和不同系统版本的配置，这些是互斥的安装路径，不必全部执行。

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install flask prometheus-client
```

保存为 `app.py`：

```python
from flask import Flask, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

app = Flask(__name__)
REQUESTS = Counter(
    "demo_http_requests_total",
    "已处理的示例业务请求",
    ["route"],
)
DURATION = Histogram(
    "demo_http_request_duration_seconds",
    "示例业务请求耗时（秒）",
    ["route"],
)

@app.get("/")
def index():
    with DURATION.labels(route="home").time():
        REQUESTS.labels(route="home").inc()
        return "demo ok\n"

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)
```

```bash
flask --app app run --host 127.0.0.1 --port 8000
# 另一个终端
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/metrics
```

访问 `/` 会增加 `demo_http_requests_total{route="home"}`，并更新 Histogram 的 `_bucket`、`_sum`、`_count`。访问 `/metrics` 只读取指标，不增加业务请求计数。Flask 自带服务器适合此处练习，正式部署需使用适当的应用服务器，并确认多进程指标收集方式。指标名是否出现、值是否增长，比照抄旧截图中的具体数值更重要。

## 接入 Prometheus 并验证查询

将目标加入现有 `prometheus.yml` 的 `scrape_configs`，地址必须是 **Prometheus 所在环境能访问到的服务地址**。如果 Prometheus 与 Flask 不在同一主机，就不能写 `127.0.0.1:8000`；如果 Flask 只监听回环地址，也不能被远程主机抓取。

```yaml
scrape_configs:
  - job_name: demo-python
    static_configs:
      - targets: ['demo-host.example.local:8000']
        labels:
          app: demo
```

先运行 `promtool check config /path/to/prometheus.yml`，再重载 Prometheus。Targets 页面应显示目标 UP；在表达式页先查 `demo_http_requests_total`，再查 `rate(demo_http_requests_total[5m])`。速率函数需要窗口内至少两个样本，刚启动或请求太少时没有结果不代表配置损坏。

![Prometheus 中的自定义目标](assets/img-64da83e43135e395.webp)

![请求计数器的原始值](assets/img-06460a1e84de6e76.webp)

![请求计数随访问增长](assets/img-65df8c582110b231.webp)

![请求速率查询](assets/img-4c26ab8feab5ee72.webp)

![短时速率查询](assets/img-fdf1d18975c2d8eb.webp)

## Go：相同链路的另一种实现

Go 客户端也可在业务处理器里更新指标，再由 `promhttp.Handler()` 暴露 `/metrics`。原资料的 Go 示例只有默认的 Go 运行时指标，没有自定义业务指标；下面补上计数器，使两个语言案例能对应比较。

```go
package main

import (
    "log"
    "net/http"

    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var requests = prometheus.NewCounter(prometheus.CounterOpts{
    Name: "demo_go_requests_total",
    Help: "已处理的 Go 示例请求总数",
})

func main() {
    prometheus.MustRegister(requests)
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        requests.Inc()
        _, _ = w.Write([]byte("demo ok\n"))
    })
    http.Handle("/metrics", promhttp.Handler())
    log.Fatal(http.ListenAndServe(":9527", nil))
}
```

初始化 Go module、安装依赖后运行，再分别访问 `http://127.0.0.1:9527/` 和 `/metrics`。若要由 Prometheus 抓取，同样添加一个可达的 `host:9527` 目标；Go 运行时指标出现只说明客户端库正常，自定义的 `demo_go_requests_total` 增长才说明业务埋点生效。

## 在 Grafana 中设计四个面板

Grafana 的数据源应已指向 Prometheus（第 04 章）。创建仪表盘并添加时间序列面板前，先在 Prometheus 表达式页验证每条 PromQL。下面四个问题分别对应四种查询，避免把“QPS”和“每分钟请求数”混为一谈：

| 需要展示 | PromQL | 单位 |
| --- | --- | --- |
| 每秒请求速率（QPS） | `sum by (instance) (rate(demo_http_requests_total[5m]))` | req/s |
| 最近一分钟请求增量 | `sum by (instance) (increase(demo_http_requests_total[1m]))` | requests |
| 最近五分钟平均耗时 | `sum by (instance) (rate(demo_http_request_duration_seconds_sum[5m])) / sum by (instance) (rate(demo_http_request_duration_seconds_count[5m]))` | s |
| 最近五分钟 P95 耗时 | `histogram_quantile(0.95, sum by (instance, le) (rate(demo_http_request_duration_seconds_bucket[5m])))` | s |

原资料直接用累计 `_sum / _count` 得到“启动以来平均耗时”，与面板期待的“最近一段时间”不同；这里对二者分别求速率。图例可以使用 `{{instance}}`，但图例变量与 Grafana 面板的 **Instant** 查询开关没有因果关系；时间序列面板一般使用范围查询。选择数据源、时间范围和单位后再保存面板。

以下截图展示原教程的旧版 Grafana 界面。当前版本的菜单名称、编辑器布局可能不同，但“数据源 → 查询 → 可视化 → 单位/图例 → 保存”的顺序不变。

![Grafana 面板类型选择](assets/img-8fe817b0efebe9aa.webp)

![Grafana 可视化插件入口](assets/img-e0f2ffc0d6213b72.webp)

![已有仪表盘概览](assets/img-e95908681accc393.webp)

![面板菜单入口](assets/img-d1811b35e70fbc3e.webp)

![面板详情视图](assets/img-b22f44a2f3063858.webp)

![Explore 查询视图](assets/img-037c2879280e487e.webp)

![面板编辑视图](assets/img-5344930aca9a29ca.webp)

![编辑 PromQL 查询](assets/img-cba0687b0b391a8b.webp)

![图表样式配置](assets/img-e2d605da6e1b7dd8.webp)

![面板一般设置](assets/img-2b2d36e17e71b37b.webp)

### 按查询、单位和时间范围逐项验证

先添加一个面板，选择 Prometheus 数据源并粘贴 QPS 查询。确认图上有曲线后，再设置标题、图例 `{{instance}}`、单位 `req/s`。下方原图依次对应创建、选择数据源和输入查询的过程。

![新建仪表盘面板](assets/img-9e50b28b07c5a3fd.webp)

![选择 Prometheus 数据源](assets/img-ce8e262420771b45.webp)

![输入 PromQL 并预览](assets/img-3c327479507b7c78.webp)

曲线样式、坐标轴和图例属于呈现层，不会修正错误的 PromQL；先确认查询结果与单位，再调整这些选项。保存第一个面板后，以同样流程添加请求增量、平均耗时和 P95 面板。

![时间序列样式](assets/img-bfb0c9c0be347c0c.webp)

![坐标轴配置](assets/img-137a6bdec4c05693.webp)

![图例配置](assets/img-6f7774b38aecbf6c.webp)

![面板标题设置](assets/img-fa5074284c54a559.webp)

![保存面板](assets/img-c41860aab15aac09.webp)

![首个面板显示结果](assets/img-034de707f993c9b4.webp)

![添加其他面板](assets/img-a880f0564f52a8f1.webp)

![请求速率面板配置](assets/img-d0c05d1b40bdf34d.webp)

![请求增量面板配置](assets/img-dd6ae8b7e4f72292.webp)

![平均耗时面板配置](assets/img-c49b0aa889a5db41.webp)

![耗时面板的查询设置](assets/img-060193846ed3cd0c.webp)

![第四个面板配置](assets/img-4c84826a07be6a7d.webp)

![组合后的仪表盘](assets/img-06e1fd1a609b72d8.webp)

![仪表盘展示示例一](assets/img-669c9bacef62ad70.webp)

![仪表盘展示示例二](assets/img-34429b5887fe2795.webp)

若曲线为空，按顺序检查：业务请求是否确实发生、`/metrics` 是否暴露相应序列、Prometheus Target 是否 UP、PromQL 是否在表达式页有结果、Grafana 面板时间范围与数据源是否正确。这样可以明确问题出在埋点、采集、查询还是展示，而不是反复调整图形外观。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/08-promql-operators.html' | relative_url }}">← 上一章：PromQL 运算符、聚合与函数</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/10-label-management.html' | relative_url }}">下一章：标签与重标记 →</a>
</nav>
