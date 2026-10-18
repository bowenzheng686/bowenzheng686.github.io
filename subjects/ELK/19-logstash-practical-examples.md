---
layout: default
title: "ELK 日志分析 · Logstash 实战案例"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 19 Logstash 实战案例

前一篇介绍了输入、过滤和输出插件；本篇把它们串成七条实际数据链路。每个案例先确认**日志源确实产生了新事件**，再检查 Logstash 输入、字段转换、Elasticsearch 索引与 Kibana 时间范围。示例中的地址、证书和路径需按环境替换，不同版本的插件参数也要以已安装版本为准。不要把多个独立案例的 `.conf` 同时放在同一管道目录中运行，以免重复采集或将事件送到意外的输出。

## 1. 单文件：dpkg 日志进入 Elasticsearch

这个最小案例用 `/var/log/dpkg.log` 说明 File input 的读取进度。Logstash 服务用户必须有读取日志和写入 sincedb 的权限；`start_position => "beginning"` 只影响此前未被 sincedb 记录的文件。与原文不同，测试时不必卸载 Apache 之类的软件来制造事件，可观察已有日志或在隔离测试文件中追加一行。

```ruby
input {
  file {
    path => "/var/log/dpkg.log"
    start_position => "beginning"
    sincedb_path => "/var/lib/logstash/dpkg.sincedb"
    tags => ["dpkg"]
  }
}
output {
  if "dpkg" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "dpkg-%{+YYYY.MM.dd}"
    }
  }
}
```

```bash
sudo -u logstash /usr/share/logstash/bin/logstash --path.settings /etc/logstash \
  -f /etc/logstash/conf.d/dpkg-to-es.conf --config.test_and_exit
sudo systemctl restart logstash
sudo journalctl -u logstash -n 80 --no-pager
```

`Configuration OK` 只确认基本语法，并不证明能读取文件或写入 Elasticsearch。之后检查 `dpkg-*` 索引/文档以及 Kibana 中匹配的数据视图。


<details>
<summary>单文件索引与 Kibana 验证（2 张）</summary>

![单文件索引与 Kibana 验证 · 图 1](assets/img-7ea0f3a7bf364e0b.webp)

![单文件索引与 Kibana 验证 · 图 2](assets/img-efa76fa08e107fed.webp)

</details>


## 2. 多文件：系统日志与 Tomcat 访问日志分流

先确认 Tomcat 实际安装方式：包安装可能写入 `/var/log/tomcat9` 或 `/var/log/tomcat10`，归档安装通常在 `CATALINA_BASE/logs`。Logstash 可以同时读取不同文件，再按标签输出到不同索引。原文多次将 `type` 当作唯一来源标记；它只是事件字段，标签更明确，也不会与旧版 Elasticsearch 文档映射类型混淆。

```ruby
input {
  file {
    path => "/var/log/syslog"
    tags => ["system"]
    sincedb_path => "/var/lib/logstash/system.sincedb"
  }
  file {
    path => "/var/log/tomcat10/localhost_access_log.*.txt"
    tags => ["tomcat-access"]
    sincedb_path => "/var/lib/logstash/tomcat-access.sincedb"
  }
}
output {
  if "system" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "system-%{+YYYY.MM.dd}"
    }
  } else if "tomcat-access" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "tomcat-access-%{+YYYY.MM.dd}"
    }
  }
}
```

若日志报 `EACCES`，检查目录的遍历权限、文件读取权限与服务用户身份，通过日志组或适当 ACL 授予最小读取权限。**不要把 Logstash 改为 root，也不要修改发行包的 systemd 单元以绕过权限。**产生一条系统或 Tomcat 新日志后，分别核对两个索引的文档数。


<details>
<summary>多文件与 Tomcat 索引的历史界面（10 张）</summary>

![多文件与 Tomcat 索引的历史界面 · 图 1](assets/img-f48890d617b4c135.webp)

![多文件与 Tomcat 索引的历史界面 · 图 2](assets/img-23f8cb53e93f71c9.webp)

![多文件与 Tomcat 索引的历史界面 · 图 3](assets/img-60e7f783c2a3ec4f.webp)

![多文件与 Tomcat 索引的历史界面 · 图 4](assets/img-04010b5e9988df43.webp)

![多文件与 Tomcat 索引的历史界面 · 图 5](assets/img-43aa8ab79d465d25.webp)

![多文件与 Tomcat 索引的历史界面 · 图 6](assets/img-f33c620966384bcd.webp)

![多文件与 Tomcat 索引的历史界面 · 图 7](assets/img-3c01371a6233fc80.webp)

![多文件与 Tomcat 索引的历史界面 · 图 8](assets/img-7c6a53da4c839b76.webp)

![多文件与 Tomcat 索引的历史界面 · 图 9](assets/img-472bd00b8f43656f.webp)

![多文件与 Tomcat 索引的历史界面 · 图 10](assets/img-4b7221c9e026c83f.webp)

</details>


## 3. Tomcat JSON 访问日志与 Java 多行异常

访问日志若要作为 JSON 解析，必须让 Tomcat 实际输出**每行一个合法 JSON 对象**。原文 AccessLogValve 的 `pattern` 被 PDF 换行破坏，而且请求头中可能出现引号等需要转义的字符；先按当前 Tomcat 版本的 AccessLogValve 文档配置，再用 `python3 -m json.tool` 验证抽样行，不能因为界面显示花括号就断定格式正确。验证之后才可在 File input 上用 `codec => json`。原文用 Python `eval(line)` 读取访问日志既不能可靠解析 JSON，也会执行输入内容；应使用 `json.loads(line)`。

```python
import json
from collections import Counter

counts = Counter()
with open("/var/log/tomcat10/access_json.log", encoding="utf-8") as source:
    for line in source:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        counts[str(event.get("status"))] += 1
print("200:", counts["200"], "404:", counts["404"])
```

Catalina 或应用异常通常由一行时间/级别头和多行堆栈组成。要在**靠近源头的位置**合并：直接用 Logstash File input 时可用 multiline codec；若 Filebeat 先采集，则应在 Filebeat 输入端合并，不要等到多个流在 Logstash Beats input 混合后才处理。模式须以真实日志样本为准，下面匹配以 `03-Dec-2022 ...` 开头的 Tomcat 日志：

```ruby
input {
  file {
    path => "/var/log/tomcat10/catalina*.log"
    tags => ["tomcat-error"]
    codec => multiline {
      pattern => "^[0-3][0-9]-[A-Za-z]{3}-[0-9]{4} "
      negate => true
      what => "previous"
      auto_flush_interval => 5
    }
  }
}
```

`negate => true` 表示不匹配新事件头的行拼接到前一条；`auto_flush_interval` 使末尾事件不必无限等下一条头。检查 `message` 中一条异常是否包含完整堆栈，并为超长异常设置容量上限。不要把 `^[` 当成所有 Java 日志通用起点。


<details>
<summary>Tomcat JSON、索引与多行异常验证（19 张）</summary>

![Tomcat JSON、索引与多行异常验证 · 图 1](assets/img-db9341ae65e9bf08.webp)

![Tomcat JSON、索引与多行异常验证 · 图 2](assets/img-b966e2579e1853e5.webp)

![Tomcat JSON、索引与多行异常验证 · 图 3](assets/img-df744a9066817497.webp)

![Tomcat JSON、索引与多行异常验证 · 图 4](assets/img-5509cdcb8822feb1.webp)

![Tomcat JSON、索引与多行异常验证 · 图 5](assets/img-171d454fd1c0c632.webp)

![Tomcat JSON、索引与多行异常验证 · 图 6](assets/img-20e85f6e47e621f1.webp)

![Tomcat JSON、索引与多行异常验证 · 图 7](assets/img-8db4b8053d87d514.webp)

![Tomcat JSON、索引与多行异常验证 · 图 8](assets/img-fb7d6e99fece8290.webp)

![Tomcat JSON、索引与多行异常验证 · 图 9](assets/img-c06bd38df54c5772.webp)

![Tomcat JSON、索引与多行异常验证 · 图 10](assets/img-d0f042e00a34a7eb.webp)

![Tomcat JSON、索引与多行异常验证 · 图 11](assets/img-ae69174b646ee473.webp)

![Tomcat JSON、索引与多行异常验证 · 图 12](assets/img-deaf3ed1de8fbad4.webp)

![Tomcat JSON、索引与多行异常验证 · 图 13](assets/img-ff054e856e1060eb.webp)

![Tomcat JSON、索引与多行异常验证 · 图 14](assets/img-f4cf8f4cea618c95.webp)

![Tomcat JSON、索引与多行异常验证 · 图 15](assets/img-c776eea26a0c5edb.webp)

![Tomcat JSON、索引与多行异常验证 · 图 16](assets/img-22f22f944a5fc795.webp)

![Tomcat JSON、索引与多行异常验证 · 图 17](assets/img-3bbcd28b05734cc8.webp)

![Tomcat JSON、索引与多行异常验证 · 图 18](assets/img-d410812a2d0718ad.webp)

![Tomcat JSON、索引与多行异常验证 · 图 19](assets/img-2bf072ac9fc5a4ee.webp)

</details>


## 4. Nginx：JSON 访问日志和文本错误日志

在 Nginx 中用 `log_format ... escape=json` 生成结构化访问日志，再用 `nginx -t` 与 `tail -n 1 ... | python3 -m json.tool` 验证一整行。错误日志通常仍是文本。Logstash File input 分别读取，访问日志才使用 JSON codec：

```ruby
input {
  file {
    path => "/var/log/nginx/access_json.log"
    codec => json
    tags => ["nginx-access"]
  }
  file {
    path => "/var/log/nginx/error.log"
    tags => ["nginx-error"]
  }
}
output {
  if "nginx-access" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "nginx-access-%{+YYYY.MM.dd}"
    }
  } else if "nginx-error" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "nginx-error-%{+YYYY.MM.dd}"
    }
  }
}
```

原文说新版索引名“不能以 nginx 或 tomcat 开头”，并无普遍的 Elasticsearch 命名禁令；如果某环境写入失败，应检查已有模板、数据流、权限和错误日志，而不是随意改前缀。数据视图应分别匹配实际索引，并选择正确的 `@timestamp`。


<details>
<summary>Nginx 访问和错误日志的索引、数据视图（8 张）</summary>

![Nginx 访问和错误日志的索引、数据视图 · 图 1](assets/img-3e6a068cfc843374.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 2](assets/img-072be65b5da191cd.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 3](assets/img-fc4d0be4e7c31dc9.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 4](assets/img-1452b67420615110.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 5](assets/img-e6b477af5e829834.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 6](assets/img-2bc1ad009ddb44b6.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 7](assets/img-c6be5c91b7da99d1.webp)

![Nginx 访问和错误日志的索引、数据视图 · 图 8](assets/img-d05ce262cb71f2b7.webp)

</details>


## 5. TCP/UDP：先确认消息边界，再入库

TCP input 接受网络流，通常按行界定事件；UDP datagram 可能丢失或乱序，不适合要求可靠交付的日志。测试时先用 `stdout` 输出并限制监听地址，明确来源发送的是文本还是一行一个 JSON；对纯文本强行设置 JSON codec 会产生 `_jsonparsefailure`。

```ruby
input {
  tcp {
    host => "127.0.0.1"
    port => 9527
    codec => json_lines
    tags => ["tcp-demo"]
  }
}
output { stdout { codec => rubydebug } }
```

```bash
printf '%s\n' '{"name":"示例","age":28}' | nc 127.0.0.1 9527
```

确认字段后再把输出换成 Elasticsearch；如需跨主机发送，绑定内网地址、限制来源并配置适合的 TLS。Shell 的 `/dev/tcp/HOST/PORT` 是 Bash 功能，不是 Linux 中真实存在的普通设备文件；它只是另一个发送方式，不能替代协议校验。


<details>
<summary>TCP 输入及 Kibana 中的事件（4 张）</summary>

![TCP 输入及 Kibana 中的事件 · 图 1](assets/img-e972e89f250793d2.webp)

![TCP 输入及 Kibana 中的事件 · 图 2](assets/img-7682d73253f7a1f6.webp)

![TCP 输入及 Kibana 中的事件 · 图 3](assets/img-aab4ca1445858897.webp)

![TCP 输入及 Kibana 中的事件 · 图 4](assets/img-f99a9937b8a06ba8.webp)

</details>


## 6. HAProxy → rsyslog → Logstash

HAProxy 把日志交给本机 syslog，rsyslog 根据 `local6` facility 转发，Logstash 的 syslog input 解析协议头并写入 Elasticsearch。三个配置要对齐：**HAProxy facility、rsyslog 选择器、Logstash 接收地址/端口**。与原文不同，不必为了让 Logstash 监听特权端口 514 而以 root 运行；改用 5514，或由前端代理/系统能力完成端口转发。

在 HAProxy 的 `global` 段按当前发行版选择可用的本地 syslog 地址，例如：

```haproxy
global
    log /dev/log local6
```

rsyslog 的转发规则（`@@` 表示 TCP；`@` 是 UDP）：

```conf
local6.* @@LOGSTASH_HOST:5514
```

Logstash 端配置 TCP/UDP syslog input 并按标签分流，相关 TLS 与网络限制按插件版本和部署环境设置：

```ruby
input {
  syslog {
    host => "LOGSTASH_PRIVATE_IP"
    port => 5514
    tags => ["haproxy"]
  }
}
output {
  if "haproxy" in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "haproxy-%{+YYYY.MM.dd}"
    }
  }
}
```

先 `rsyslogd -N1` 验证配置，再重启 rsyslog；用 `logger -p local6.info` 产生测试日志。若无数据，按 HAProxy 本地日志、rsyslog 转发、Logstash 监听/解析、Elasticsearch 索引逐段检查，不应先重启整台主机。原案例中的 HAProxy 状态页使用弱口令并绑定全部地址，实际部署还需访问控制。


<details>
<summary>HAProxy、rsyslog 与 Kibana 验证（10 张）</summary>

![HAProxy、rsyslog 与 Kibana 验证 · 图 1](assets/img-204e12105a3b37b1.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 2](assets/img-682467fc4dc8ff7a.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 3](assets/img-f7f5a1b60a760bee.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 4](assets/img-7f7187296e49c980.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 5](assets/img-d3009db81c58bf8a.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 6](assets/img-d078a02b8208543c.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 7](assets/img-07a3d71657e8e4b6.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 8](assets/img-dca57eda610c224e.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 9](assets/img-76150a52f4176aa7.webp)

![HAProxy、rsyslog 与 Kibana 验证 · 图 10](assets/img-93854c6225d95475.webp)

</details>


## 7. 商城应用日志：提取业务动作并做可视化

原始行如 `[INFO] 2018-06-28 08:08:12 [www.mall.com] - DAU|9136|加入收藏|2018-06-28 01:05:02`。它同时包含日志写入时间和业务动作时间：若要分析用户行为，应明确选择后者写入 `@timestamp`。原文直接按 `|` 切开后，把第一段中的整段前缀当作字段而未解析，容易让读者误解 `DAU`、用户 ID 和动作的边界。以下用 Grok 一次提取：

```ruby
input { beats { port => 5044 } }
filter {
  grok {
    match => {
      "message" => "^\[%{LOGLEVEL:level}\] %{TIMESTAMP_ISO8601:recorded_at} \[%{DATA:site}\] - %{WORD:metric}\|%{NUMBER:user_id:int}\|%{DATA:action}\|%{TIMESTAMP_ISO8601:action_time}$"
    }
    tag_on_failure => ["_mall_parse_failure"]
  }
  if "_mall_parse_failure" not in [tags] {
    date {
      match => ["action_time", "yyyy-MM-dd HH:mm:ss"]
      timezone => "Asia/Shanghai"
      target => "@timestamp"
    }
  }
}
output {
  if "_mall_parse_failure" not in [tags] {
    elasticsearch {
      hosts => ["https://ES_HOST:9200"]
      user => "${ES_USER}"
      password => "${ES_PASSWORD}"
      ssl_certificate_authorities => ["/etc/logstash/certs/http_ca.crt"]
      index => "mall-app-%{+YYYY.MM.dd}"
    }
  } else {
    stdout { codec => rubydebug }
  }
}
```

先用单行样本确认 `user_id` 是数字、`action` 是“加入收藏”等文本、`@timestamp` 转为 UTC 后对应原本的北京时间。Kibana 的数据视图匹配 `mall-app-*`；**历史样本在 2018 年**，Discover 默认“最近 15 分钟”不会显示，需要切换到对应日期。动作次数可用 `action.keyword` 的 Terms 聚合；若要计算真正的日活用户，不能把事件条数当 DAU，还需按日期对 `user_id` 做去重计数。先保存各图表，再组合为仪表盘。


<details>
<summary>商城日志字段、可视化与最终仪表盘（23 张）</summary>

![商城日志字段、可视化与最终仪表盘 · 图 1](assets/img-fb155ac9bb4847e4.webp)

![商城日志字段、可视化与最终仪表盘 · 图 2](assets/img-29f662470adddc8b.webp)

![商城日志字段、可视化与最终仪表盘 · 图 3](assets/img-d726f2f4c5089603.webp)

![商城日志字段、可视化与最终仪表盘 · 图 4](assets/img-258266fcbf7caf2e.webp)

![商城日志字段、可视化与最终仪表盘 · 图 5](assets/img-9931a68897d12c64.webp)

![商城日志字段、可视化与最终仪表盘 · 图 6](assets/img-30d57a94bdc9274c.webp)

![商城日志字段、可视化与最终仪表盘 · 图 7](assets/img-19070f5a04953c7f.webp)

![商城日志字段、可视化与最终仪表盘 · 图 8](assets/img-e4bd67e849fe7308.webp)

![商城日志字段、可视化与最终仪表盘 · 图 9](assets/img-95187504b73862b5.webp)

![商城日志字段、可视化与最终仪表盘 · 图 10](assets/img-279313fa03d86241.webp)

![商城日志字段、可视化与最终仪表盘 · 图 11](assets/img-14f7228127f75968.webp)

![商城日志字段、可视化与最终仪表盘 · 图 12](assets/img-0e63022ca00752d7.webp)

![商城日志字段、可视化与最终仪表盘 · 图 13](assets/img-ba0e0e0576902f1b.webp)

![商城日志字段、可视化与最终仪表盘 · 图 14](assets/img-5a579ea1260dfdbf.webp)

![商城日志字段、可视化与最终仪表盘 · 图 15](assets/img-291ce64543e65308.webp)

![商城日志字段、可视化与最终仪表盘 · 图 16](assets/img-a1c208cbb8789c72.webp)

![商城日志字段、可视化与最终仪表盘 · 图 17](assets/img-20e111424cd2968e.webp)

![商城日志字段、可视化与最终仪表盘 · 图 18](assets/img-3d64bbcc779e9979.webp)

![商城日志字段、可视化与最终仪表盘 · 图 19](assets/img-3e8869cfe06477c5.webp)

![商城日志字段、可视化与最终仪表盘 · 图 20](assets/img-d5967d182e8059b7.webp)

![商城日志字段、可视化与最终仪表盘 · 图 21](assets/img-e55e69cc4d22639f.webp)

![商城日志字段、可视化与最终仪表盘 · 图 22](assets/img-adee6cd88d785a4e.webp)

![商城日志字段、可视化与最终仪表盘 · 图 23](assets/img-10e885b220253d34.webp)

</details>


{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/18-using-logstash.html' | relative_url }}">← 上一篇：使用 Logstash</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">返回 ELK 日志分析目录</a>
  <a href="{{ '/subjects/ELK/20-introduction-to-kibana.html' | relative_url }}">下一篇：Kibana 简介 →</a>
</nav>
