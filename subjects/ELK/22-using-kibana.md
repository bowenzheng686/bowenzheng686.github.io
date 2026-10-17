---
layout: default
title: "ELK Log Analytics · Using Kibana"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to ELK Log Analytics Index]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 22 Using Kibana
### 5.3 使用 Kibana

### 查看和操作Web界面

### Kibana 8.X 开启xpack.security功能连接ES

范例:

```bash
#在ES节点上生成token
[root@ubuntu2204 ~]#/usr/share/elasticsearch/bin/elasticsearch-create-
enrollment-token --scope kibana
eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTAuMC4wLjEwMDo5MjAwIl0sImZnciI6IjdhMzIyMWRhNmFm
OWI1YzUzYzJiMjM3YjJiMjg3MzcwZTBlOGNiOTZkNmJlYjI4MzdkZDFkYzJlNTE4ZDU3OWUiLCJrZXki
OiJRVl90TUpFQkk4OFloVFdtVHFKTDptdmsxNXUtYVI1T3g4bzZ3ZTNYVGdBIn0=
#修改kibana配置文件
[root@ubuntu2204 ~]#grep -Ev "#|^$" /etc/kibana/kibana.yml
server.host: 0.0.0.0                             #修改此行
elasticsearch.hosts: ['https://10.0.0.100:9200'] #修改此行,指向elasticsearch地址
logging.appenders.file.type: file
logging.appenders.file.fileName: /var/log/kibana/kibana.log
logging.appenders.file.layout.type: json
logging.root.appenders: [default, file]
pid.file: /run/kibana/kibana.pid
i18n.locale: zh-CN                              #修改此行
```

```bash
#查看 verification code
[root@ubuntu2204 ~]#systemctl status kibana.service
```

● kibana.service - Kibana

```text
Loaded: loaded (/lib/systemd/system/kibana.service; enabled; vendor preset:
enabled)
Active: active (running) since Thu 2024-08-08 15:37:07 CST; 2min 36s ago
Docs: https://www.elastic.co
Main PID: 3926 (node)
Tasks: 11 (limit: 2193)
Memory: 264.7M
CPU: 10.782s
CGroup: /system.slice/kibana.service
└─3926 /usr/share/kibana/bin/../node/bin/node
/usr/share/kibana/bin/../src/cli/dist
Aug 08 15:37:09 ubuntu2204 kibana[3926]: [2024-08-08T15:37:09.380+08:00][INFO ]
[root] Kibana is starting
Aug 08 15:37:09 ubuntu2204 kibana[3926]: [2024-08-08T15:37:09.446+08:00][INFO ]
[node] Kibana process configured with roles: >
Aug 08 15:37:15 ubuntu2204 kibana[3926]: [2024-08-08T15:37:15.037+08:00][INFO ]
[plugins-service] The following plugins are d>
Aug 08 15:37:15 ubuntu2204 kibana[3926]: [2024-08-08T15:37:15.115+08:00][INFO ]
[http.server.Preboot] http server running at >
Aug 08 15:37:15 ubuntu2204 kibana[3926]: [2024-08-08T15:37:15.445+08:00][INFO ]
[plugins-system.preboot] Setting up [1] plugi>
Aug 08 15:37:15 ubuntu2204 kibana[3926]: [2024-08-08T15:37:15.455+08:00][INFO ]
[preboot] "interactiveSetup" plugin is holdin>
Aug 08 15:37:15 ubuntu2204 kibana[3926]: [2024-08-08T15:37:15.486+08:00][INFO ]
[root] Holding setup until preboot stage is c>
Aug 08 15:37:15 ubuntu2204 kibana[3926]: i Kibana has not been configured.
Aug 08 15:37:15 ubuntu2204 kibana[3926]: Go to http://0.0.0.0:5601/?code=201867
to get started.
Aug 08 15:39:21 ubuntu2204 kibana[3926]: Your verification code is:  201 867
```

```text
#浏览器访问,填写上面的token
http://kibana:5601/
```

![ELK 日志分析第 337 页插图](assets/img-444087d8fb3c9625.png)

![ELK 日志分析第 337 页插图](assets/img-3a195daec793554b.png)

![ELK 日志分析第 338 页插图](assets/img-a126b91880e120bc.png)

```text
#利用elasticsearch的用户密码登录
```

![ELK 日志分析第 338 页插图](assets/img-24f141c085b2f62e.png)

![ELK 日志分析第 339 页插图](assets/img-508fee1d61d765c8.png)

### Kibana 8.X 禁用xpack.security功能连接ES

范例:

```text
#浏览器访问下面链接
http://kabana-server:5601
```

如果出现下面提示，需要删除相关插件或重置浏览器

![ELK 日志分析第 339 页插图](assets/img-56a8d993cee043d1.png)

新版界面

![ELK 日志分析第 340 页插图](assets/img-9bd3eafce1388641.png)

![ELK 日志分析第 340 页插图](assets/img-43650c72b2d657da.png)

![ELK 日志分析第 341 页插图](assets/img-b45f9ab0d96e1372.png)

![ELK 日志分析第 341 页插图](assets/img-2e018019c0a10a08.png)

![ELK 日志分析第 342 页插图](assets/img-5ae32ccfe4431a2c.png)

![ELK 日志分析第 342 页插图](assets/img-8a50193d4d21a55a.png)

![ELK 日志分析第 342 页插图](assets/img-d0ee6c0fe1926293.png)

旧版界面

![ELK 日志分析第 343 页插图](assets/img-45b0fdf48aae7902.png)

```text
#查看状态
http://kabana-server:5601/status
```

![ELK 日志分析第 343 页插图](assets/img-355fecfebb10da74.png)

![ELK 日志分析第 344 页插图](assets/img-481e2fae254bdc0e.png)

### 管理索引

![ELK 日志分析第 344 页插图](assets/img-53bf9b9cf5c832fd.png)

输入以下,再执行

```text
GET _search
```

![ELK 日志分析第 345 页插图](assets/img-fdef032d222b643b.png)

输入下面内容，执行

```text
GET _search { "query":{"match_all":{}}}
```

![ELK 日志分析第 345 页插图](assets/img-ad0ea81ede544721.png)

![ELK 日志分析第 346 页插图](assets/img-79c00d9a429c0ce7.png)

输入下面内容创建索引并执行

```json
POST /index_bowen/_doc/1
{
"username": "bowen",
"age": 18,
"title": "cto"
}
```

![ELK 日志分析第 346 页插图](assets/img-c723a17b0453946c.png)

查看索引

```text
GET /index_bowen/_doc/1
```

![ELK 日志分析第 347 页插图](assets/img-5fcd598e5e1004b4.png)

### 创建索引模式(索引视图)

利用索引创建索引模式(8.X版改名为索引视图)

在logstash 上生成新的索引

```bash
[root@logstash ~]#/usr/share/logstash/bin/logstash -e  'input { file { path =>
"/var/log/dpkg.log" start_position => "beginning" stat_interval => "3" } } output
{ elasticsearch {hosts => ["10.0.0.101:9200"] index => "linux-%{+YYYY.MM.dd}"
}}'
```

添加索引模式(索引视图)

新版界面

![ELK 日志分析第 347 页插图](assets/img-b8dd88d94c6b691d.png)

![ELK 日志分析第 348 页插图](assets/img-ce09c74c7e1a83f1.png)

![ELK 日志分析第 348 页插图](assets/img-d05458be8b9c7d06.png)

![ELK 日志分析第 349 页插图](assets/img-6f3f518dbeaeb250.png)

旧版界面

![ELK 日志分析第 349 页插图](assets/img-05444e95d53581e6.png)

查看之前的索引数据

![ELK 日志分析第 350 页插图](assets/img-07dcbde402ad252b.png)

![ELK 日志分析第 350 页插图](assets/img-16492993271150e3.png)

输入通配符匹配索引

![ELK 日志分析第 351 页插图](assets/img-d5acb81ccdb50818.png)

![ELK 日志分析第 351 页插图](assets/img-dcdc8fb778ff8b31.png)

![ELK 日志分析第 351 页插图](assets/img-3d61b07bc62ec898.png)

![ELK 日志分析第 352 页插图](assets/img-c62f173f88303e63.png)

![ELK 日志分析第 352 页插图](assets/img-59b8f93de8300c34.png)

### Kibana 验证数据

如果默认没有显示柱状的图，可能是最近没有写入新的数据，可以查看较长日期当中的数据或者通过 logstash新写入数据即可

```bash
#安装新包的,生成日志
[root@logstash ~]#apt -y install apache2
```

![ELK 日志分析第 353 页插图](assets/img-4adc5f61fff77508.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/21-installing-and-configuring-kibana.html' | relative_url }}">← Previous: Installing and Configuring Kibana</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/23-securing-kibana-login-with-nginx.html' | relative_url }}">Next: Securing Kibana Login with Nginx →</a>
</nav>
