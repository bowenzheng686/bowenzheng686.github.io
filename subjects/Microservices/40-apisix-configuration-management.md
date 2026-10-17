---
layout: default
title: "Microservices · APISIX Configuration Management"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to Microservices Index]({{ '/subjects/Microservices/' | relative_url }})

{% raw %}

# 40 APISIX Configuration Management
### 8.3 APISIX 配置管理

### APISIX 配置文件

<https://apisix.apache.org/docs/apisix/installation-guide/#next-steps>

配置 APISIX 方法

By directly changing your configuration file ( conf/config.yaml ).

By using the --config or the -c flag to pass the path to your configuration file while starting APISIX.

```text
apisix start -c <path to config file>
```

APISIX将使用此配置文件中的配置信息，如果未配置任何配置，则将回退到默认配置。

注意

```text
APISIX's default configuration can be found in `conf/config-default.yaml` file and it should not be modified.
It is bound to the source code and the configuration should only be changed by the methods mentioned above.
The `conf/nginx.conf` file is automatically generated and should not be modified.
APISIX 的默认配置可以在 `conf/config-default.yaml` 文件中找到，不应修改。 它与源代码绑定，只能通过上述方法更改配置。
`conf/nginx.conf` 文件是自动生成的，不应修改。
```

范例: 包安装默认配置文件

```bash
[root@ubuntu2204 ~]#cat /usr/local/apisix/conf/config.yaml
#
#Licensed to the Apache Software Foundation (ASF) under one or more
#contributor license agreements.  See the NOTICE file distributed with
#this work for additional information regarding copyright ownership.
#The ASF licenses this file to You under the Apache License, Version 2.0
#(the "License"); you may not use this file except in compliance with
#the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
#
#If you want to set the specified configuration value, you can set the new
#in this file. For example if you want to specify the etcd address:
#
#deployment:
# role: traditional
# role_traditional:
#   config_provider: etcd
# etcd:
#   host:
#     - http://127.0.0.1:2379
#
#To configure via environment variables, you can use `${{VAR}}` syntax. For instance:
#
#deployment:
# role: traditional
# role_traditional:
#   config_provider: etcd
# etcd:
#   host:
#     - http://${{ETCD_HOST}}:2379
#
#And then run `export ETCD_HOST=$your_host` before `make init`.
#
#If the configured environment variable can't be found, an error will be thrown.
#
#Also, If you want to use default value when the environment variable not set,
#Use `${{VAR:=default_value}}` instead. For instance:
#
#deployment:
# role: traditional
# role_traditional:
#   config_provider: etcd
# etcd:
#   host:
#     - http://${{ETCD_HOST:=localhost}}:2379
#
#This will find environment variable `ETCD_HOST` first, and if it's not exist it will use `localhost` as
default value.
#
deployment:
role: traditional
role_traditional:
config_provider: etcd
admin:
admin_key:
- name: admin
key: edd1c9f034335f136f87ad84b625c8f1  # using fixed API token has security risk, please update it
when you deploy to production environment
role: admin
#测试访问,默认不允许远程访问，只允许本地访问
[root@ubuntu2204 ~]#curl http://127.0.0.1:9180/apisix/admin/routes?api_key=edd1c9f034335f136f87ad84b625c8f1 -i
HTTP/1.1 200 OK
Date: Thu, 02 Nov 2023 07:56:33 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
Server: APISIX/3.2.2
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: *
Access-Control-Max-Age: 3600
X-API-VERSION: v3
{"list":[],"total":0}
```

### 修改配置

范例: 将客户端访问的默认侦听端口9080配置为“8000”

```bash
#conf/config.yaml
[root@ubuntu2204 ~]#vim /usr/local/apisix/conf/config.yaml
#修改下面行
apisix:
node_listen: 8000
......
[root@ubuntu2204 ~]#systemctl restart apisix.service
[root@ubuntu2204 ~]#ss -nltp|grep openresty
LISTEN 0      511          0.0.0.0:9180       0.0.0.0:*    users:(("openresty",pid=12121,fd=7),
("openresty",pid=12120,fd=7),("openresty",pid=12119,fd=7))
LISTEN 0      511          0.0.0.0:8000       0.0.0.0:*    users:(("openresty",pid=12121,fd=13),
("openresty",pid=12119,fd=13))
LISTEN 0      511          0.0.0.0:8000       0.0.0.0:*    users:(("openresty",pid=12120,fd=9),
("openresty",pid=12119,fd=9))
LISTEN 0      511        127.0.0.1:9090       0.0.0.0:*    users:(("openresty",pid=12121,fd=6),
("openresty",pid=12120,fd=6),("openresty",pid=12119,fd=6))
LISTEN 0      511        127.0.0.1:9091       0.0.0.0:*    users:(("openresty",pid=12124,fd=26))
LISTEN 0      511          0.0.0.0:9443       0.0.0.0:*    users:(("openresty",pid=12121,fd=15),
("openresty",pid=12119,fd=15))
LISTEN 0      511          0.0.0.0:9443       0.0.0.0:*    users:(("openresty",pid=12120,fd=11),
("openresty",pid=12119,fd=11))
LISTEN 0      511             [::]:8000          [::]:*    users:(("openresty",pid=12120,fd=10),
("openresty",pid=12119,fd=10))
LISTEN 0      511             [::]:8000          [::]:*    users:(("openresty",pid=12121,fd=14),
("openresty",pid=12119,fd=14))
LISTEN 0      511             [::]:9443          [::]:*    users:(("openresty",pid=12120,fd=12),
("openresty",pid=12119,fd=12))
LISTEN 0      511             [::]:9443          [::]:*    users:(("openresty",pid=12121,fd=16),
("openresty",pid=12119,fd=16))
```

范例:  修改 etcd地址更改为http://etcd.bowen.org:2379

```bash
#conf/config.yaml
[root@ubuntu2204 ~]#vim /usr/local/apisix/conf/config.yaml
apisix:
node_listen: 8000
deployment:
role: traditional
role_traditional:
config_provider: etcd
etcd:
host:
- "http://etcd.bowen.org:2379"
[root@ubuntu2204 ~]#systemctl restart apisix.service
```

范例:  更改 Admin API key

基于安全原因，需要更改默认的 Admin API key

```bash
https://apisix.apache.org/docs/apisix/installation-guide/#updating-admin-api-key
[root@ubuntu2204 ~]#vim /usr/local/apisix/conf/config.yaml
......
deployment:
admin:
admin_key
-
name: "admin"
key: newsupersecurekey  #修改此行
#key: edd1c9f034335f136f87ad84b625c8f1
role: admin
#重启生效
[root@ubuntu2204 ~]#systemctl restart apisix.service
#验证访问
[root@ubuntu2204 ~]#curl -i http://127.0.0.1:9180/apisix/admin/routes -H"X-API-KEY: newsupersecurekey"
[root@ubuntu2204 ~]#curl -i http://127.0.0.1:9180/apisix/admin/routes?api_key=newsupersecurekey
HTTP/1.1 200 OK
Date: Tue, 05 Dec 2023 11:00:21 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
Server: APISIX/3.6.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: *
Access-Control-Max-Age: 3600
X-API-VERSION: v3
{"list":[],"total":0}
```

范例：打开远程管理功能

```bash
[root@ubuntu2204 ~]#vim /usr/local/apisix/conf/config.yaml
......
deployment:
role: traditional
role_traditional:
config_provider: etcd
admin:
admin_listen:
port: 9180
ip: 0.0.0.0
admin_api_version: v3
admin_key:
- role: admin
#key: ogeBAJkDCqJZuDGZUABZRIBVQFvgqCSk #3.13.0默认key
#key: KSUifDhEpsKLBhqvEpeKpQziNQVQwjie #新版默认key
#key: ejMqSewssdcYOkDcCSxwFKxjvGkQHCsV #新版默认key
#key: KIrRjALJLNAEMamUbcjmfLxguNkYAfZK #新版默认key
key: edd1c9f034335f136f87ad84b625c8f1  #旧版默认key
name: admin
admin_key_required: true
enable_admin_cors: true
allow_admin:
- 127.0.0.0/24
- 10.0.0.0/24  #添加此行
- 0.0.0.0/0    #任意远程主机都可以访问
#重启生效
[root@ubuntu2204 ~]#systemctl restart apisix.service
#测试远程访问API
[root@ubuntu2204 ~]#curl http://10.0.0.100:9180/apisix/admin/routes?api_key=edd1c9f034335f136f87ad84b625c8f1 -
i
HTTP/1.1 200 OK
Date: Mon, 16 Dec 2024 03:45:00 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
Server: APISIX/3.11.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Access-Control-Expose-Headers: *
Access-Control-Max-Age: 3600
X-API-VERSION: v3
{"list":[],"total":0}
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Microservices/39-installing-apisix.html' | relative_url }}">← Previous: Installing APISIX</a>
  <a href="{{ '/subjects/Microservices/' | relative_url }}">Back to Microservices Index</a>
  <a href="{{ '/subjects/Microservices/41-installing-and-using-apisix-dashboard.html' | relative_url }}">Next: Installing and Using APISIX Dashboard →</a>
</nav>
