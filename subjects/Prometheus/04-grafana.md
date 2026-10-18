---
layout: default
title: "Prometheus · 使用 Grafana 展示监控数据"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 04 使用 Grafana 展示监控数据

Prometheus 负责采集、存储和查询时间序列；Grafana 将查询结果组织为面板和仪表盘。**Grafana 不替代 Prometheus 的采集任务**：配置 Grafana 数据源只是让 Grafana 去查询 Prometheus；若要监控 Grafana 本身，还需在 Prometheus 中另加抓取目标。本篇按“部署 → 连接数据源 → 导入仪表盘 → 排查空面板 → 自监控”的顺序完成一次闭环。

## 部署 Grafana

可以按 [Grafana 官方下载页](https://grafana.com/grafana/download) 选择与系统匹配的安装包；原资料列出多个年代的 deb 下载地址和依赖修复日志，版本彼此不一致，不应混装。Ubuntu 上下载**同一版本**的 deb 后，使用 `apt install ./文件名.deb`，让 apt 处理依赖：

```bash
sudo apt update
sudo apt install ./grafana_<版本>_amd64.deb
sudo systemctl enable --now grafana-server
sudo systemctl status grafana-server
ss -lnt | grep ':3000'
```

也可以使用容器。示例把 Grafana 的数据目录放入命名卷，避免删除容器后丢失用户、数据源和仪表盘配置；部署时应固定经过验证的镜像版本，而不是长期依赖浮动的 `latest`。

```bash
docker volume create grafana_data
docker run -d --name grafana --restart unless-stopped \
  -p 3000:3000 -v grafana_data:/var/lib/grafana grafana/grafana:<版本>
docker logs grafana --tail 50
```

两种方式任选其一。浏览器打开 `http://<Grafana 主机地址>:3000/`。新安装实例若使用初始管理员账户，首次登录后应立即修改密码；不要像原资料的演示那样继续沿用 `admin/admin`。正式环境还应通过反向代理配置 HTTPS 和访问控制。

![Grafana 首次登录页面](assets/img-6b7dab41a4a4b364.webp)

![Grafana 修改初始密码](assets/img-fceb50d3fdc253fb.webp)

## 添加 Prometheus 数据源

在 Grafana 中选择 **Connections → Data sources → Add data source → Prometheus**（不同版本菜单名称可能略有变化），填写 Prometheus 的 HTTP 地址，再点击 **Save & test**。地址是从**Grafana 进程所在环境**访问 Prometheus 的地址，而不是浏览器当前电脑的地址：

- 二者安装在同一主机且 Grafana 直接运行于宿主机时，可用 `http://127.0.0.1:9090`。
- Grafana 运行在容器内时，容器里的 `localhost` 指 Grafana 容器本身；应使用可达的宿主机地址，或把两个服务加入同一 Docker 网络后使用服务名。
- 若访问失败，先从 Grafana 所在主机或容器测试 `/api/v1/query?query=up`，再检查防火墙、监听地址与认证。

![Grafana 添加数据源入口](assets/img-fb3d83af4ee45e0d.webp)

![选择 Prometheus 数据源](assets/img-0ed1f587e44caf40.webp)

![配置 Prometheus URL](assets/img-223d96fec118e90c.webp)

![检查数据源其他设置](assets/img-733dd780b08c54b4.webp)

![保存并测试数据源](assets/img-92e96c45a208700f.webp)

连接成功后，可在 Grafana 的 Explore 中先查询 `up`。如果 `up` 有数据，说明数据源与 Prometheus 的查询链路正常；具体仪表盘是否有数据，还取决于相应 Exporter、指标名、标签和时间范围。

## 使用内置仪表盘和导入社区模板

一些数据源或插件带有示例仪表盘。它们只是面板配置，**不会自动生成对应指标**。例如 Grafana 自身指标面板在 Prometheus 尚未抓取 Grafana 的 `/metrics` 前为空，这是符合预期的。

![内置仪表盘导入入口](assets/img-089cb28d7897e49e.webp)

![内置模板导入过程](assets/img-d307b3086d112696.webp)

![内置仪表盘列表](assets/img-397968f03d0acae3.webp)

![内置仪表盘示例](assets/img-1bb8d874b5d24062.webp)

![尚未抓取 Grafana 指标时的空面板](assets/img-f9058baedf2a192e.webp)

![抓取 Grafana 指标后的面板](assets/img-7615108942b3f691.webp)

社区模板可在 [Grafana Dashboards](https://grafana.com/grafana/dashboards/) 查找。原资料以 Node Exporter 的 8919、1860、11074、13978 等编号为例；编号是模板 ID，**不是 Prometheus 查询语句**。导入时先检查模板维护状态、支持的 Grafana/Exporter 版本，再选择刚创建的 Prometheus 数据源。下面截图保留原界面流程。

![Grafana 社区仪表盘搜索](assets/img-a7af026d70a3b97c.webp)

![Node Exporter 模板详情](assets/img-0e55473f9abd4c78.webp)

![仪表盘版本信息](assets/img-e3566e7af8e2de2c.webp)

![导入仪表盘入口](assets/img-79ac23fc55146a7f.webp)

![按模板 ID 加载](assets/img-fda9df99c75be300.webp)

![选择模板数据源](assets/img-23350db9ec8c67a6.webp)

![完成仪表盘导入](assets/img-7ab19293a1bc00c6.webp)

![Node Exporter 指标展示](assets/img-1a92249b9a6c90fb.webp)

如果面板为空，按层排查而不是反复导入模板：先在 Prometheus Targets 页确认 Node Exporter 目标为 UP，再在 Grafana Explore 查询 `up` 和 `node_cpu_seconds_total`，然后检查面板选中的数据源、模板变量、时间范围及指标名是否匹配。主机时钟偏差也可能影响结果，但“相差 3 秒必然无数据”不是通用规则。

## 让 Prometheus 监控 Grafana

Grafana 可暴露 Prometheus 格式的 `/metrics`。确认接口可访问后，在 Prometheus 的 `scrape_configs` 中增加目标；`targets` 必须填写 **Prometheus 所在环境能够访问到的地址**，而不是凭域名猜测。

```yaml
scrape_configs:
  - job_name: grafana
    static_configs:
      - targets: ['grafana.example.local:3000']
```

将该条合并进现有 `prometheus.yml`，不要覆盖其他 job。重载 Prometheus 后，在查询页执行 `up{job="grafana"}`：结果为 1 表示抓取成功，为 0 则结合 Targets 页错误排查路径、网络和 Grafana 指标开关。随后再查看 Grafana 自监控面板，面板和采集链路才算一致。

![Grafana 自监控仪表盘入口](assets/img-a2821b0f04993f28.webp)

![Grafana 自身指标面板](assets/img-a34cc6d93f64a47d.webp)

![Grafana 自身状态展示](assets/img-7615108942b3f691.webp)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/03-node-exporter.html' | relative_url }}">← 上一章：Node Exporter 安装与采集</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/05-zookeeper-monitoring.html' | relative_url }}">下一章：ZooKeeper 监控 →</a>
</nav>
