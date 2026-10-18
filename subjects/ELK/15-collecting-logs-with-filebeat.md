---
layout: default
title: "ELK 日志分析 · 利用 Filebeat 收集日志"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 15 利用 Filebeat 收集日志

Filebeat 是安装在日志来源附近的轻量采集器：输入读取文件、容器日志或标准输入，处理器补充字段，内部队列缓冲事件，输出发送给 Elasticsearch、Logstash、Redis 或 Kafka。它不等同于 Logstash 的复杂转换能力，也没有“必定只占 10 MB 内存”的保证。内存使用受输入数量、队列与流量影响，应实测。一个 Filebeat 进程可以有多个输入，但只能启用**一种输出类型**；要分发到不同目标，可在该输出下配置多个主机，或交给下游 Logstash 路由。


<details>
<summary>Filebeat 输入、harvester 与输出流程（3 张）</summary>

![Filebeat 输入、harvester 与输出流程 · 图 1](assets/img-6cc4d9fa3db435b4.webp)

![Filebeat 输入、harvester 与输出流程 · 图 2](assets/img-85b1465e3563dc56.webp)

![Filebeat 输入、harvester 与输出流程 · 图 3](assets/img-955a779dbd3415dd.webp)

</details>


## 1. 安装与配置原则

先选择与目标 Elastic Stack 兼容的 Filebeat 版本，按[官方安装文档](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html)安装并验证版本。DEB 包通常把配置放在 `/etc/filebeat/filebeat.yml`，把读取进度放在 `/var/lib/filebeat`。Docker/Kubernetes 运行时要挂载日志路径、持久化 registry 并按目标集群配置认证；原文粘贴的 Kubernetes 清单缩进已损坏且含明文示例密码，应按相应版本的官方清单取得原件，而非复制那段截断文本。

```bash
sudo dpkg -i filebeat-VERSION-amd64.deb
filebeat version
sudo filebeat test config -c /etc/filebeat/filebeat.yml
sudo filebeat test output -c /etc/filebeat/filebeat.yml
sudo systemctl enable --now filebeat
sudo journalctl -u filebeat -n 50 --no-pager
```

配置是 YAML，列表项目与子字段必须正确缩进。新部署优先使用 `filestream`，每个输入给唯一 `id`；历史 7.x 的 `log` 输入及其 `json.keys_under_root`、`multiline.*` 选项不能直接搬进 `filestream`。文件识别、轮转及 registry 格式随版本和输入类型变化，**不要手工删除 registry 来“修复”未采集问题**，否则可能造成重读或丢读。

## 2. 从标准输入认识事件结构

先用 console 输出查看 Filebeat 如何把一行文本变成事件。配置保存为 `/etc/filebeat/stdin.yml`，用独立的 `path.data` 调试，避免与 systemd 服务争用同一个 registry。

```yaml
filebeat.inputs:
  - type: stdin
    enabled: true
    tags: ["demo-stdin"]
    fields:
      project: "demo"
output.console:
  pretty: true
```

```bash
sudo filebeat test config -c /etc/filebeat/stdin.yml
sudo filebeat -e -c /etc/filebeat/stdin.yml --path.data /tmp/filebeat-stdin-demo
```

输入 `hello` 后，`message` 是原始文本；`@timestamp`、`agent.name`、`host.name`、`tags`、`fields.project` 是采集器添加或配置的元数据。输入看似 JSON 的一行，若没有解析器，仍只是 `message` 字符串。测试本地文件输出时，可以把上面的 `output.console` 换成下面的**唯一**输出，读取生成的 NDJSON 行即可；文件名可能带日期后缀，按实际版本查看。

```yaml
output.file:
  path: "/tmp"
  filename: "filebeat-demo"
```

## 3. 从日志文件读取：文本与 NDJSON

普通文本按行读取；一行一个 JSON 对象的日志才适合 `ndjson` parser。下例的 `id` 必须在同一 Filebeat 进程内唯一。

```yaml
filebeat.inputs:
  - type: filestream
    id: app-text
    enabled: true
    paths: ["/var/log/app/app.log"]
    tags: ["app-text"]
  - type: filestream
    id: app-json
    enabled: true
    paths: ["/var/log/app/events.ndjson"]
    parsers:
      - ndjson:
          target: ""
          add_error_key: true
    tags: ["app-json"]
output.console:
  pretty: true
```

先用 `filebeat test config` 检查缩进，再向实际被监控文件**追加**新行。Filebeat 会记录已读位置；编辑旧内容、复制已处理文件或改变文件身份时的行为，取决于输入的文件标识与轮转设置，原文“大小不变就会全部重读”的说法并不可靠。若测试文件太小且当前 filestream 使用内容指纹识别，可先写足够内容，或按版本文档调整识别配置。

## 4. 输出到 Elasticsearch 并在 Kibana 查看

把上例的 console 输出替换为 Elasticsearch 输出，只保留一个 `output.*`。8.x/9.x 默认安全配置通常需要 HTTPS、CA 与凭据；旧版无认证 HTTP 示例仅适合相应实验环境。

```yaml
output.elasticsearch:
  hosts: ["https://ES_HOST:9200"]
  username: "${ES_USER}"
  password: "${ES_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/certs/http_ca.crt"]
```

配置通过后，观察 Filebeat 日志和 Elasticsearch 中的 `filebeat-*` 数据流或索引。在 Kibana 创建匹配的数据视图并选 `@timestamp`，再到 Discover 设置合适的时间范围。截图展示了 7.x 与 8.x 界面差异；排查顺序是**输入有新行 → Filebeat 发布成功 → 索引/数据流存在 → 数据视图匹配 → 时间范围正确**。


<details>
<summary>系统日志索引与 Kibana 查询界面（7 张）</summary>

![系统日志索引与 Kibana 查询界面 · 图 1](assets/img-55b5fc6c3f072982.webp)

![系统日志索引与 Kibana 查询界面 · 图 2](assets/img-2811d9e68f55df85.webp)

![系统日志索引与 Kibana 查询界面 · 图 3](assets/img-94daf68a03fb0704.webp)

![系统日志索引与 Kibana 查询界面 · 图 4](assets/img-44db5f43b964201a.webp)

![系统日志索引与 Kibana 查询界面 · 图 5](assets/img-395936554fbde359.webp)

![系统日志索引与 Kibana 查询界面 · 图 6](assets/img-82080fb740a6f301.webp)

![系统日志索引与 Kibana 查询界面 · 图 7](assets/img-19a9b700fbee3b04.webp)

</details>


### 自定义索引名称

原文把关闭 ILM、自定义索引、模板和 8.x 数据流命名混在一起，容易误以为配置 `index` 就一定生成 `.ds-自定义名-*`。实际结果取决于当前版本、ILM/数据流和索引模板。确需经典自定义索引时，要成套配置索引名、生命周期策略和模板匹配，先在测试集群确认写入结果，不要为了修改分片而删除已有业务索引。下面是**关闭 Filebeat 默认 ILM 的经典索引示意**：

```yaml
output.elasticsearch:
  hosts: ["https://ES_HOST:9200"]
  username: "${ES_USER}"
  password: "${ES_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/certs/http_ca.crt"]
  index: "app-%{[agent.version]}-%{+yyyy.MM.dd}"
setup.ilm.enabled: false
setup.template.name: "app"
setup.template.pattern: "app-*"
setup.template.settings:
  index.number_of_shards: 1
  index.number_of_replicas: 1
```

验证时看实际索引名、模板生效情况和分片设置。单节点配 1 个副本可能使状态为 yellow；已有索引不会因更改新模板而自动重建。


<details>
<summary>自定义索引在不同版本中的显示（6 张）</summary>

![自定义索引在不同版本中的显示 · 图 1](assets/img-30cf2a9d346c7189.webp)

![自定义索引在不同版本中的显示 · 图 2](assets/img-4ed08f74bc201e0b.webp)

![自定义索引在不同版本中的显示 · 图 3](assets/img-a8d24b48071d53d2.webp)

![自定义索引在不同版本中的显示 · 图 4](assets/img-ea3ef8071e26598a.webp)

![自定义索引在不同版本中的显示 · 图 5](assets/img-91dd4a914c32db9b.webp)

![自定义索引在不同版本中的显示 · 图 6](assets/img-714dc48db37f9e10.webp)

</details>


## 5. Nginx：区分访问日志与错误日志

Nginx 访问日志若输出为每行合法 JSON，后续可按 `status`、`uri`、`clientip` 等字段分析；错误日志通常保留文本。配置 `log_format ... escape=json` 后，先用 `nginx -t` 检查并用 `python3 -m json.tool` 验证实际一行日志。**不要为了产生错误日志而注释站点的 `try_files`**，这会改变请求行为。

以下单个 Filebeat 配置给两路输入打标签，并按标签路由到不同经典索引。标签用于表示日志来源，不应在多个输入里重复读取同一物理文件。多台 Nginx 可使用相同索引规则，通过 `agent.name` 或 `host.name` 区分来源。

```yaml
filebeat.inputs:
  - type: filestream
    id: nginx-access
    paths: ["/var/log/nginx/access_json.log"]
    parsers:
      - ndjson:
          target: ""
          add_error_key: true
    tags: ["nginx-access"]
  - type: filestream
    id: nginx-error
    paths: ["/var/log/nginx/error.log"]
    tags: ["nginx-error"]

output.elasticsearch:
  hosts: ["https://ES_HOST:9200"]
  username: "${ES_USER}"
  password: "${ES_PASSWORD}"
  ssl.certificate_authorities: ["/etc/filebeat/certs/http_ca.crt"]
  indices:
    - index: "nginx-access-%{+yyyy.MM.dd}"
      when.contains:
        tags: "nginx-access"
    - index: "nginx-error-%{+yyyy.MM.dd}"
      when.contains:
        tags: "nginx-error"
setup.ilm.enabled: false
setup.template.name: "nginx"
setup.template.pattern: "nginx-*"
```

原示例中 `%{+yyy.MM.dd}` 少了一个 `y`；按日期生成索引时应使用 `yyyy.MM.dd`。访问日志里的 `@timestamp` 若与 Filebeat 元数据冲突，应明确决定使用日志时间还是采集时间并验证结果，不要无意识覆盖。按状态码分流时，先解析 JSON，再对真正的 `status` 字段条件判断；对原始文本用 `include_lines: ['404']` 可能误匹配 URL、字节数或用户代理，不等于 HTTP 404。


<details>
<summary>Nginx 访问与错误日志的数据视图（7 张）</summary>

![Nginx 访问与错误日志的数据视图 · 图 1](assets/img-6d495a13bc08045e.webp)

![Nginx 访问与错误日志的数据视图 · 图 2](assets/img-1112591e4a1c9338.webp)

![Nginx 访问与错误日志的数据视图 · 图 3](assets/img-fe2009ff0479b2fa.webp)

![Nginx 访问与错误日志的数据视图 · 图 4](assets/img-faf253acea89940a.webp)

![Nginx 访问与错误日志的数据视图 · 图 5](assets/img-c1ed5ec2727aa022.webp)

![Nginx 访问与错误日志的数据视图 · 图 6](assets/img-9359ed56aef1b4f4.webp)

![Nginx 访问与错误日志的数据视图 · 图 7](assets/img-96cdf2fe536616cd.webp)

</details>


## 6. Tomcat：访问日志与多行异常

Tomcat 访问日志可用 AccessLogValve 产生结构化字段，但原文 `server.xml` 的 `pattern` 被换行和 HTML 实体截断，不能直接粘贴。先在当前 Tomcat 版本的文档中确认 Valve 的 JSON 转义能力与占位符，再对生成的一整行做 JSON 解析验证。若日志仍是普通文本，不要启用 `ndjson` 强行解析。

Tomcat 包安装与二进制安装的路径不同，先用 `systemctl status tomcat*`、`ls /var/log/tomcat*` 或实际 `CATALINA_BASE` 核对。访问日志和 Catalina 错误日志用**不同输入**：前者逐行解析，后者可能包含跨多行的 Java 异常，需要在采集端合并后再发送到 Elasticsearch。以下示例把 Catalina 的日期时间行视为新事件起点；应先对真实日志抽样，确认其格式确实如此。

```yaml
filebeat.inputs:
  - type: filestream
    id: tomcat-access
    paths: ["/var/log/tomcat10/localhost_access_log.*.txt"]
    parsers:
      - ndjson:
          target: ""
          add_error_key: true
    tags: ["tomcat-access"]
  - type: filestream
    id: tomcat-catalina
    paths: ["/var/log/tomcat10/catalina*.log"]
    parsers:
      - multiline:
          type: pattern
          pattern: '^[0-3][0-9]-[A-Za-z]{3}-[0-9]{4} '
          negate: true
          match: after
          max_lines: 500
    tags: ["tomcat-error"]
```

这条模式匹配原日志中 `03-Dec-2022 ...` 一类的头行，不适用于每种 Tomcat 日志格式。旧 `log` 输入使用 `multiline.pattern` 等字段，不能与上面 `filestream.parsers` 混在同一输入里。若单条异常超过 `max_lines` 或长期没有下一条头行，应关注截断与 `timeout`；在 Kibana 中检查一条异常的堆栈是否完整，而不是只看索引出现。


<details>
<summary>Tomcat 访问与错误日志的索引、数据视图和字段（14 张）</summary>

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 1](assets/img-baefc730365ace20.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 2](assets/img-c0579a4e2023329d.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 3](assets/img-0aa3b3763bc0635a.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 4](assets/img-e3e183aa9173524a.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 5](assets/img-47b6af2cc52ea2f1.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 6](assets/img-fa0222d98eee1167.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 7](assets/img-b46b8f831ea4703d.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 8](assets/img-efce0c1e612bf673.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 9](assets/img-6b2ec85fd69637b2.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 10](assets/img-266c994d77af40fb.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 11](assets/img-1fdadb5813607a6d.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 12](assets/img-a1341c2988cbf8eb.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 13](assets/img-5e1ce878ca1d9309.webp)

![Tomcat 访问与错误日志的索引、数据视图和字段 · 图 14](assets/img-4bdfd05b71141337.webp)

</details>



<details>
<summary>多行异常与 Kibana 中的合并结果（5 张）</summary>

![多行异常与 Kibana 中的合并结果 · 图 1](assets/img-38b2cac0814a3109.webp)

![多行异常与 Kibana 中的合并结果 · 图 2](assets/img-2c9fd8fb15d1f180.webp)

![多行异常与 Kibana 中的合并结果 · 图 3](assets/img-6c9792f07ebabd2d.webp)

![多行异常与 Kibana 中的合并结果 · 图 4](assets/img-09413af0c5a55fb8.webp)

![多行异常与 Kibana 中的合并结果 · 图 5](assets/img-51aa0205ce3c936b.webp)

</details>


## 7. Redis、Kafka 与 Logstash 输出的选择

这三种输出**互为替代**，不能同时放在同一个 Filebeat 配置里。Redis List 可缓冲突发流量，但受内存限制并需监控队列长度；Kafka 更适合较高吞吐与较强持久化需求；Logstash Beats input 则用于集中转换。后续专题分别展开 Redis 和 Kafka 的完整链路。

```yaml
# 选择 Redis 时启用这一段，并移除其他 output.*：
output.redis:
  hosts: ["REDIS_HOST:6379"]
  password: "${REDIS_PASSWORD}"
  db: 0
  key: "filebeat"
  datatype: list
```

Redis 应仅绑定内网、配置认证和容量告警，不能照旧示例绑定 `0.0.0.0` 后匿名访问；检查指定 `LLEN filebeat` 即可，不要用 `KEYS *` 扫描全库。

```yaml
# 选择 Kafka 时启用这一段，并移除其他 output.*：
output.kafka:
  hosts: ["KAFKA_HOST_1:9092", "KAFKA_HOST_2:9092"]
  topic: "filebeat-log"
  required_acks: 1
  compression: gzip
```

`required_acks` 与 Kafka broker 的副本、`min.insync.replicas` 共同决定交付保证；不是简单把值设为 `-1` 就必然零丢失。验证时检查 Filebeat 发布结果、Topic 与消费者偏移。

```yaml
# 选择 Logstash 时启用这一段，并移除其他 output.*：
output.logstash:
  hosts: ["LOGSTASH_1:5044", "LOGSTASH_2:5044"]
  loadbalance: true
```

Logstash 需先启用 Beats input 并监听 5044；`loadbalance: true` 会把事件分散到可用的 Logstash 节点，不表示每条事件同时复制给全部节点。按目的地切换输出前，先停止旧服务、检查配置与目标连通性，再生成新日志验证完整链路。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/14-monitoring-with-heartbeat.html' | relative_url }}">← 上一篇：使用 Heartbeat 监控</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/16-introduction-to-logstash.html' | relative_url }}">下一篇：Logstash 简介 →</a>
</nav>
