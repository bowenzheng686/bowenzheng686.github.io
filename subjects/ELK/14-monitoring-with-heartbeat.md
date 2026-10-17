---
layout: default
title: "ELK Log Analytics · Monitoring with Heartbeat"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 14 Monitoring with Heartbeat
### 3.2 利用 Heartbeat 监控

heartbeat 用来定时探测服务是否正常运行。支持也支持TLS、身份验证和代理

官方heartbeat配置文档

<https://www.elastic.co/guide/en/beats/heartbeat/current/configuring-howto-heartbeat.html>

### 下载并安装

注意：安装前建议先修改主机名，确保每个主机名称唯一

```bash
[root@ubuntu2404 ~]#hostnamectl set-hostname web01.bowen.org
[root@ubuntu2404 ~]#exit
```

下载链接

<https://www.elastic.co/cn/downloads/beats/heartbeat>

<https://mirrors.tuna.tsinghua.edu.cn/elasticstack/8.x/apt/pool/main/h/heartbeat-elastic/>

<https://mirrors.tuna.tsinghua.edu.cn/elasticstack/7.x/apt/pool/main/h/heartbeat-elastic/>

```bash
#新版
[root@elk-web2 ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/elasticstack/8.x/apt/pool/main/h/heartbeat-
elastic/heartbeat-8.6.1-amd64.deb
#旧版
[root@elk-web2 ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/elasticstack/7.x/apt/pool/main/h/heartbeat-
elastic/heartbeat-7.6.2-amd64.deb
#安装
[root@elk-web2 ~]#dpkg -i heartbeat-7.6.2-amd64.deb
#准备需要监控的服务httpd
[root@elk-web2 ~]#apt -y install apache2
```

### 修改配置

官方参考

```text
https://www.elastic.co/guide/en/beats/heartbeat/current/configuration-heartbeat-
options.html
#官方示例 heartbeat.yml
heartbeat.monitors:
- type: icmp
id: ping-myhost
name: My Host Ping
hosts: ["myhost"]
schedule: '*/5 * * * * * *'  #相当于'@every 5s'
- type: tcp
id: myhost-tcp-echo
name: My Host TCP Echo
hosts: ["myhost:777"]  # default TCP Echo Protocol
#check.send: "Check"
#check.receive: "Check"
schedule: '@every 5s'
- type: http
id: service-status
name: Service Status
service.name: my-apm-service-name
hosts: ["http://localhost:80/service/status"]
check.response.status: [200] #默认值
schedule: '@every 5s'
heartbeat.scheduler:
limit: 10
```

时间格式: 注意可以支持秒级精度

```text
https://github.com/gorhill/cronexpr#implementation
Field name     Mandatory?   Allowed values    Allowed special characters
----------     ----------   --------------    --------------------------
Seconds        No           0-59              * / , -
Minutes        Yes          0-59              * / , -
Hours          Yes          0-23              * / , -
Day of month   Yes          1-31              * / , - L W
Month          Yes          1-12 or JAN-DEC   * / , -
Day of week    Yes          0-6 or SUN-SAT    * / , - L #
Year           No           1970–2099         * / , -
```

范例:

```bash
[root@elk-web2 ~]#vim /etc/heartbeat/heartbeat.yml
# Configure monitors inline
heartbeat.monitors:
- type: http
enabled: true                 #修改此行false为true
# List or urls to query
urls: ["http://localhost:80/test.html"]  #修改此行，指向需要监控的服务器的地址和端口
# Configure task schedule
schedule: '@every 10s'
# Total test connection and data exchange timeout
timeout: 6s
#添加下面内容，包括 tcp 和 icmp
- type: tcp
id: myhost-tcp-echo
name: My Host TCP Echo
hosts: ["10.0.0.205:80"]  # default TCP Echo Protocol
schedule: '@every 5s'
- type: icmp                   #添加下面5行，用于监控ICMP
id: ping-myhost
name: My Host Ping
hosts: ["10.0.0.100"]
schedule: '*/5 * * * * * *'
setup.kibana:
# Kibana Host
# Scheme and port can be left out and will be set to the default (http and
5601)
# In case you specify and additional path, the scheme is required:
http://localhost:5601/path
# IPv6 addresses should always be defined as: https://[2001:db8::1]:5601
host: "10.0.0.101:5601 #指向kibana服务器地址和端口,可选
#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
# Array of hosts to connect to.
hosts: ["10.0.0.101:"]  #修改此行，指向ELK集群服务器地址和端口
```

### 启动服务

```bash
[root@elk-web2 ~]#systemctl enable --now  heartbeat-elastic.service
```

### head 插件查看索引

新版索引

索引名：.ds-heartbeat-<版本号>-年月日

![ELK 日志分析第 129 页插图](assets/img-2be1bdf3f8ecab80.png)

旧版索引

heartbeat-<版本号>-年月日

![ELK 日志分析第 129 页插图](assets/img-daa558028147aef6.png)

### 通过 Kibana 查看收集的性能指标

通过Kibana 可以看到主机的状态

8.X 版

Observability---运行时间--监测 Uptime Monitors

![ELK 日志分析第 130 页插图](assets/img-467cc0e62e7782a1.png)

![ELK 日志分析第 130 页插图](assets/img-ac24feef5c2869ad.png)

![ELK 日志分析第 131 页插图](assets/img-667460f78cdecf68.png)

旧版

![ELK 日志分析第 131 页插图](assets/img-1f07180e522a6f1c.png)

![ELK 日志分析第 132 页插图](assets/img-9cebfa8c57459c35.png)

![ELK 日志分析第 132 页插图](assets/img-b68fa6ad3287762a.png)

![ELK 日志分析第 132 页插图](assets/img-d8786fd1c8c0d5f2.png)

![ELK 日志分析第 133 页插图](assets/img-b0894fd8a8e7f7df.png)

![ELK 日志分析第 133 页插图](assets/img-5e51199e9d55eba8.png)

### 停止监控的服务再观察 Kibana

Down 机后Refresh ，可以看到下面的橙色

```bash
[root@elk-web2 ~]#systemctl stop apache2
```

新版

![ELK 日志分析第 134 页插图](assets/img-413f74e264578f52.png)

![ELK 日志分析第 134 页插图](assets/img-9fec3b22f3146f80.png)

旧版

![ELK 日志分析第 135 页插图](assets/img-8db2743e73a652cc.png)

![ELK 日志分析第 135 页插图](assets/img-b9de4f872c9a0604.png)

![ELK 日志分析第 135 页插图](assets/img-328f4b9f09e9b3c6.png)

![ELK 日志分析第 136 页插图](assets/img-c71e7377ec321dd0.png)

![ELK 日志分析第 136 页插图](assets/img-e65848409a9281b3.png)

### 利用 Kibana 将 Heartbeat 的数据进行可视化

旧版

![ELK 日志分析第 137 页插图](assets/img-522ca9aad573d7b9.png)

![ELK 日志分析第 137 页插图](assets/img-8aa0263fd71ccd14.png)

![ELK 日志分析第 137 页插图](assets/img-8cd2dc3b94de0145.png)

![ELK 日志分析第 138 页插图](assets/img-8d48e4b506167800.png)

![ELK 日志分析第 138 页插图](assets/img-60e23ade6a3c4ee5.png)

![ELK 日志分析第 138 页插图](assets/img-6f34d0fc3b4e2d70.png)

![ELK 日志分析第 139 页插图](assets/img-e691ea7af64b6786.png)

![ELK 日志分析第 139 页插图](assets/img-e02e79bd1fdceebf.png)

![ELK 日志分析第 139 页插图](assets/img-60111d812b64ae94.png)

![ELK 日志分析第 140 页插图](assets/img-b56184a2be554574.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/13-monitoring-performance-with-metricbeat.html' | relative_url }}">← Previous: Monitoring Performance with Metricbeat</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/15-collecting-logs-with-filebeat.html' | relative_url }}">Next: Collecting Logs with Filebeat →</a>
</nav>
