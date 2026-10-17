---
layout: default
title: "Prometheus · 钉钉告警"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 15 钉钉告警

## 5.8 钉钉告警

Prometheus 不直接支持钉钉告警, 但对于prometheus来说，它所支持的告警机制非常多，尤其还支持通过webhook，从而可以实现市面上大部分的实时动态的告警平台。

Alertmanager 的 webhook 集成了钉钉报警，钉钉机器人对文件格式有严格要求，所以必须通过特定的格式转换，才能发送给钉钉的机器人。

在这里使用开源工具 prometheus-webhook-dingtalk 来进行prometheus和dingtalk的环境集成。

Github链接
https://github.com/timonwong/prometheus-webhook-dingtalk

工作原理

![原 PDF 第 202 页插图](assets/img-35a65713ef0e5b39.png)

群机器人是钉钉群的高级扩展功能，通过选择机器人，并对通知群进行设置，就可以自动将机器人消息自动推送到钉钉群中，特别的高级智能化,由于机器人是将消息推送到群，需要预先建立好一个群实现

为了完成钉钉的告警实践，遵循以下的步骤

配置  PC 端钉钉机器人
测试钉钉环境  

### 5.8.1 钉钉环境

#### 5.8.1.1 安装钉钉和创建企业

因为手机端无法进行添加机器人的相关操作，所以需要提前在电脑上下载安装钉钉的 PC 版本

下载安装钉钉

![原 PDF 第 202 页插图](assets/img-33ff4a55b5d2fd6f.png)

注册并登录钉钉后,创建专属的团队组织

点击右上角的内容，点击"创建企业/组织/团队"

![原 PDF 第 202 页插图](assets/img-f24742f37e7d3d13.png)

按照顺序一次填写手机号信息

![原 PDF 第 203 页插图](assets/img-730981f775ad6746.png)

点击下一步，完善信息

![原 PDF 第 203 页插图](assets/img-2f5dada0d37971e6.png)

点击下一步后，企业创建成功

![原 PDF 第 204 页插图](assets/img-fa1052c347b80941.png)

#### 5.8.1.2 创建钉钉的告警群

点击右上角的"+", 选择"发起群聊"

![原 PDF 第 204 页插图](assets/img-bac2b67055577888.png)

创建项目群或者管理群等类型中的一种，我们这里选择创建项目群

![原 PDF 第 204 页插图](assets/img-e5f42b94a25f2cb9.png)

![原 PDF 第 205 页插图](assets/img-efc7c98419363319.png)

创建后效果

![原 PDF 第 205 页插图](assets/img-498090a2c7b92f09.png)

![原 PDF 第 205 页插图](assets/img-75329fd456fe98d5.png)

#### 5.8.1.3 告警群中添加和配置机器人

群设置  ---  智能群助手 --- 添加机器人 --- 自定义通过webhook接入自定义服务

![原 PDF 第 206 页插图](assets/img-ede4b869a00ddb59.png)

![原 PDF 第 207 页插图](assets/img-869a5990f17e25c4.png)

![原 PDF 第 208 页插图](assets/img-121957e37b65c9d1.png)

选择添加机器人后，选择 "自定义通过webhook接入自定义服务"

![原 PDF 第 208 页插图](assets/img-29891bb30c837d7f.png)

创建机器人后，定制特有的关键字信息，便于后续接收信息

![原 PDF 第 209 页插图](assets/img-0ac43947f3dbf2b8.png)

指定机器人名字并设置安全设置

![原 PDF 第 209 页插图](assets/img-e3465d69b784f68b.png)

![原 PDF 第 210 页插图](assets/img-7542dc3ef5e5e636.png)
```text
注意：一定要记住分配的webhook地址：
https://oapi.dingtalk.com/robot/send?access_token=TOKEN
记住告警的错误关键字:PromAlert
```

#### 5.8.1.4 钉钉测试

5.8.1.4.1 只采用关键字的测试效果
```bash
WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?
access_token=TOKEN"
curl -H "Content-Type: application/json" -d '{"msgtype":"text","text":
{"content":"PromAlert - prometheus 告警测试"}}' ${WEBHOOK_URL}
#返回信息
{"errcode":0,"errmsg":"ok"}
#注意：只有包含定制的告警关键字的信息才会被发送成功。否则会提示下面错误,这里面测试的时候，没有开启加签
{"errcode":310000, errmsg":"description:关键词不还配;solution:请联系群管理员查看此机器人的关
键词，并在发送的信息中包含此关键词;"}
```

可以看到钉钉收到如下信息

![原 PDF 第 211 页插图](assets/img-414eae248ce107ad.png)

范例: Python 测试代码
```python
[root@ubuntu2204 ~]#cat dingding_send.py
#!/usr/bin/python3
import json
import requests
def send_msg(url,content):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        "msgtype": "text",
        "text": {
          "content": content
        },
       }
    r = requests.post(url,headers=headers,data = json.dumps(data))
    print(r.text)
    return r.text
if __name__ == '__main__':
    #下面为钉钉机器人的webhook地址
    url = 'https://oapi.dingtalk.com/robot/send?
access_token=TOKEN'
    content = 'PromAlert测试消息'
    send_msg(url,content)
```

5.8.1.4.2 采用关键字和加签的测试效果

在机器人的安全设置,选择"加签",复制加签信息

![原 PDF 第 212 页插图](assets/img-4a95339d3322298a.png)
```text
记录加签的信息:SEC2233b6ab300289ea5ede5b1a859d01bc7ea8a0ee3eaa1145b15b38b12dbd5558
```

如果采用了加签，这就要求，不仅仅要满足关键字的内容，还需要满足数据全流程认证加密的要求才可以正常发送

加签验证的注意事项
```python
加签校验的特点在于： 基于时间戳的会话认证，所以我们要基于加签的信息，生成配套的时间戳和base64的秘钥生
成，最后与我们的token生成标准的url地址
https://oapi.dingtalk.com/robot/send?access_token=钉钉token&timestamp=时间戳信息&sign=
生成的秘钥
#定制生成的python脚本
vim create_sign.py
#!/usr/bin/python3
import time, hmac, hashlib, base64
import urllib.parse
# 生成时间戳
timestamp = str(round(time.time() * 1000))
# 传递当前的加签内容
secret = 'SEC2233b6ab300289ea5ede5b1a859d01bc7ea8a0ee3eaa1145b15b38b12dbd5558'
# 对加签内容进行编码
secret_enc = secret.encode('utf-8')
# 对基础内容进行格式化定制,并进行编码
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
# 基于编码后的进入进行digest摘要认证加密
hmac_code = hmac.new(secret_enc, string_to_sign_enc,
digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
# 打印会话相关的时间戳和认证信息
print("Timestamp:",timestamp)
print("Sign: ",sign)
#运行脚本显示如下效果
python3 create_sign.py
Timestamp: 1650114717313
Sign:  KAHQEy%2BV7mbs5oaEuXX%2FlBaimtGEQar5un2YgeYv7Dw%3D
```

加签情况下测试发送信息
```bash
WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=TOKEN&timestamp=1650114717313&sign=KAHQEy%2BV7mbs5oaEuXX%2FlBaimtGEQar5un2YgeYv7Dw%3D"
curl -H 'Content-Type: application/json' -d '
{
    "msgtype": "markdown",
    "markdown": {
         "title": "PromAlert 告警信息",
         "text": "##  问题详情 \n### 问题级别: 严重\n### 问题类型: MySQL 服务\n### 查询时间:
2022-02-22"
    }
}'   ${WEBHOOK_URL}
#返回结果
{"errcode":0,"errmsg":"ok"}
#钉钉收到如下信息
```

![原 PDF 第 213 页插图](assets/img-6a405eaeab2f24c1.png)

### 5.8.2 钉钉告警实现

![原 PDF 第 213 页插图](assets/img-eb25fd5b8b61e885.png)

Prometheus 不直接支持钉钉告警,在这里使用开源工具 prometheus-webhook-dingtalk 来进行Prometheus 和 dingtalk的环境集成。

注意: 以下环境假设 Prometheus 已经实现告警规则和相关功能
```yaml
cat /usr/local/prometheus/conf/prometheus.yml
......
alerting:
  alertmanagers:
    - static_configs:
         - targets:
             - 10.0.0.101:9093
......
rule_files:
  - "../rules/*.yml"  #指定规则文件路径
.....
  - job_name: 'my_metric'
    static_configs:
    - targets: ['10.0.0.101:8000']
      labels: {app: 'flask_web'}
```

#### 5.8.2.1 prometheus-webhook-dingtalk 软件部署
https://github.com/timonwong/prometheus-webhook-dingtalk

范例：二进制安装
```bash
#下载软件
wget https://github.com/timonwong/prometheus-webhook-dingtalk/releases/download/v2.1.0/prometheus-webhook-dingtalk-2.1.0.linux-amd64.tar.gz
wget https://github.com/timonwong/prometheus-webhook-dingtalk/releases/download/v2.0.0/prometheus-webhook-dingtalk-2.0.0.linux-amd64.tar.gz
#解压文件
tar xf prometheus-webhook-dingtalk-2.0.0.linux-amd64.tar.gz -C /usr/local/
ln -s /usr/local/prometheus-webhook-dingtalk-2.0.0.linux-amd64/ /usr/local/dingtalk
#准备文件和目录
cd /usr/local/dingtalk
mkdir bin conf
mv prometheus-webhook-dingtalk bin/
cp config.example.yml conf/config.yml
#编辑 config.yml 相关信息
vim /usr/local/dingtalk/conf/config.yml
targets:
  webhook1:
    url: https://oapi.dingtalk.com/robot/send?access_token=TOKEN
    # secret for signature
    secret: TOKEN
#查看命令帮助
/usr/local/dingtalk/bin/prometheus-webhook-dingtalk --help
usage: prometheus-webhook-dingtalk [<flags>]
Flags:
  -h, --help                    Show context-sensitive help (also try --help-long and
--help-man).
      --web.listen-address=":8060"
                                The address to listen on for web interface.
      --web.enable-ui           Enable Web UI mounted on /ui path
      --web.enable-lifecycle    Enable reload via HTTP request.
      --config.file=config.yml  Path to the configuration file.
      --log.level=info          Only log messages with the given severity or above.
One of: [debug, info, warn, error]
      --log.format=logfmt       Output format of log messages. One of: [logfmt, json]
      --version                 Show application version.
#尝试命令启动后，测试效果
/usr/local/dingtalk/bin/prometheus-webhook-dingtalk --
config.file=/usr/local/dingtalk/conf/config.yml --web.listen-address=0.0.0.0:8060
#/usr/local/dingtalk/bin/prometheus-webhook-dingtalk --web.listen-
address="0.0.0.0:8060"
--ding.profile="alertname=https://oapi.dingtalk.com/robot/send?
access_token=TOKEN"
#检查端口
ss -tnulp | egrep 'Pro|8060'
Netid   State    Recv-Q   Send-Q     Local Address:Port      Peer Address:Port
Process
tcp     LISTEN   0  4096                   *:8060                 *:*
users:(("prometheus-webh",pid=281635,fd=3))
#测试发送信息,注意:需要取消钉钉中安全设置中的自定义关键字,只保留加签才能成功,否则提示"Unable to
talk to DingTalk"发送失败
curl "http://10.0.0.100:8060/dingtalk/webhook1/send" -H 'Content-Type:
application/json' -d '
{
    "msgtype": "markdown",
    "markdown": {
         "title": "PromAlert 告警信息",
         "text": "##  问题详情 \n### 问题级别: 严重\n### 问题类型: MySQL 服务\n### 查询时间:
2022-02-22"
    }
}'
#返回结果
OK
#如果钉钉中安全设置中有自定义关键字,prometheus-webhook-dingtalk会提示下面错误
msg="Failed to send notification to DingTalk" respCode=310000 respMsg="keywords not
in content
#准备servcie文件
[root@ubuntu2204 ~]#cat  /lib/systemd/system/dingtalk.service
[Unit]
Description=alertmanager project
After=network.target
[Service]
Type=simple
ExecStart=/usr/local/dingtalk/bin/prometheus-webhook-dingtalk --
config.file=/usr/local/dingtalk/conf/config.yml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
User=prometheus
Group=prometheus
[Install]
WantedBy=multi-user.target
[root@ubuntu2204 ~]#chown -R prometheus: /usr/local/dingtalk/
[root@ubuntu2204 ~]#systemctl  enable --now dingtalk.service
```

范例：容器方式启动
```bash
[root@ubuntu2204 ~]#cat docker-compose.yml
version: '3.6'
networks:
  monitoring:
    driver: bridge
    ipam:
      config:
         - subnet: 172.31.0.0/24
services:
  alertmanager:
    image: prom/alertmanager:v0.24.0
    volumes:
      - ./alertmanager/:/etc/alertmanager/
    networks:
      - monitoring
    ports:
      - 9093:9093
    command:
      - '--config.file=/etc/alertmanager/config.yml'
      - '--storage.path=/alertmanager'
      - '--log.level=debug'
  prometheus-webhook-dingtalk:
    image: timonwong/prometheus-webhook-dingtalk:v2.1.0
    volumes:
      - ./dingtalk/:/etc/prometheus-webhook-dingtalk/
    #command:
      #- --config.file=config.yml
      #- --config.file=/etc/prometheus-webhook-dingtalk/config-with-template.yml
    networks:
      - monitoring
    ports:
      - 8060:8060
[root@ubuntu2204 ~]#cat dingtalk/confg.yml
## Request timeout
# timeout: 5s
## Customizable templates path
# templates:
#   - contrib/templates/legacy/template.tmpl
## You can also override default template using `default_message`
## The following example to use the 'legacy' template from v0.3.0
#default_message:
#  title: '{{ template "legacy.title" . }}'
#  text: '{{ template "legacy.content" . }}'
## Targets, previously was known as "profiles"
targets:
  webhook1:
    url: https://oapi.dingtalk.com/robot/send?access_token=TOKEN
    # secret for signature
    secret: TOKEN
```

#### 5.8.2.2 Alertmanager 配置
```yaml
# vim /usr/local/alertmanager/conf/alertmanager.yml
global:
  ...
# 模板配置
templates:
  - '../tmpl/*.tmpl'
# 路由配置,添加下面内容
route:
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 10s
  receiver: 'dingtalk'
# 收信人员
receivers:
- name: 'dingtalk'
  webhook_configs:
  - url: 'http://10.0.0.100:8060/dingtalk/webhook1/send'
    send_resolved: true
#重启alertmanager服务
amtool check-config /usr/local/alertmanager/conf/alertmanager.yml
Checking '/usr/local/alertmanager/conf/alertmanager.yml'  SUCCESS
Found:
 - global config
 - route
 - 1 inhibit rules
 - 5 receivers
 - 1 templates
  SUCCESS
systemctl reload alertmanager
systemctl status alertmanager
#注意:当前此配置不支持钉钉中安全设置中有自定义关键字,只适用于加签
```

关闭flask_web服务触发故障后查看dingding的告警效果

![原 PDF 第 218 页插图](assets/img-b1659a38c3f8c978.png)

![原 PDF 第 218 页插图](assets/img-0c94ee0eea5b3927.png)

![原 PDF 第 218 页插图](assets/img-234ce5379b5cdca3.png)

重启flask-web应用,可以收到恢复信息

![原 PDF 第 219 页插图](assets/img-592d643e2dc93b9c.png)

#### 5.8.2.3 定制钉钉告警模板文件

5.8.2.3.1 确保钉钉中安全设置中有自定义关键字和加签

![原 PDF 第 219 页插图](assets/img-ae952b845e7f708d.png)

5.8.2.3.2 准备两个图片的外链接

图片用于在告警模板中显示,图片可以放在自已的网站或者利用云服务(比如: 七牛云)的对象存储功能实现
http://www.bowen.com/testdir/images/OK.png
http://www.bowen.com/testdir/images/ERROR.png

5.8.2.3.3 配置告警模板
```text
#创建告警模板
vim /usr/local/dingtalk/contrib/templates/dingtalk.tmpl
{{ define "__subject" }}[{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{
.Alerts.Firing | len }}{{ end }}] {{ .GroupLabels.SortedPairs.Values | join " " }} {{
if gt (len .CommonLabels) (len .GroupLabels) }}({{ with .CommonLabels.Remove
.GroupLabels.Names }}{{ .Values | join " " }}{{ end }}){{ end }}{{ end }}
{{ define "__alertmanagerURL" }}{{ .ExternalURL }}/#/alerts?receiver={{ .Receiver }}
{{ end }}
{{ define "__text_alert_list" }}{{ range . }}
**Labels**
{{ range .Labels.SortedPairs }}> - {{ .Name }}: {{ .Value | markdown | html }}
{{ end }}
**Annotations**
{{ range .Annotations.SortedPairs }}> - {{ .Name }}: {{ .Value | markdown | html }}
{{ end }}
**Source:** [{{ .GeneratorURL }}]({{ .GeneratorURL }})
{{ end }}{{ end }}
{{ define "___text_alert_list" }}{{ range . }}
---
**告警主题:** {{ .Labels.alertname | upper }}
**告警级别:** {{ .Labels.severity | upper }}
**触发时间:** {{ dateInZone "2006-01-02 15:04:05" (.StartsAt) "Asia/Shanghai" }}
**事件信息:** {{ range .Annotations.SortedPairs }} {{ .Value | markdown | html }}
{{ end }}
**事件标签:**
{{ range .Labels.SortedPairs }}{{ if and (ne (.Name) "severity") (ne (.Name)
"summary") (ne (.Name) "team") }}> - {{ .Name }}: {{ .Value | markdown | html }}
{{ end }}{{ end }}
{{ end }}
{{ end }}
{{ define "___text_alertresovle_list" }}{{ range . }}
---
**告警主题:** {{ .Labels.alertname | upper }}
**告警级别:** {{ .Labels.severity | upper }}
**触发时间:** {{ dateInZone "2006-01-02 15:04:05" (.StartsAt) "Asia/Shanghai" }}
**结束时间:** {{ dateInZone "2006-01-02 15:04:05" (.EndsAt) "Asia/Shanghai" }}
**事件信息:** {{ range .Annotations.SortedPairs }} {{ .Value | markdown | html }}
{{ end }}
**事件标签:**
{{ range .Labels.SortedPairs }}{{ if and (ne (.Name) "severity") (ne (.Name)
"summary") (ne (.Name) "team") }}> - {{ .Name }}: {{ .Value | markdown | html }}
{{ end }}{{ end }}
{{ end }}
{{ end }}
{{/* Default */}}
{{ define "_default.title" }}{{ template "__subject" . }}{{ end }}
{{ define "_default.content" }} [{{ .Status | toUpper }}{{ if eq .Status "firing" }}:
{{ .Alerts.Firing | len }}{{ end }}\] **[{{ index .GroupLabels "alertname" }}]({{
template "__alertmanagerURL" . }})**
{{ if gt (len .Alerts.Firing) 0 -}}
![警报 图标](http://www.bowen.com/testdir/images/ERROR.png)
**========PromAlert 告警触发========**
{{ template "___text_alert_list" .Alerts.Firing }}
{{- end }}
{{ if gt (len .Alerts.Resolved) 0 -}}
![恢复图标](http://www.bowen.com/testdir/images/OK.png)
**========PromAlert 告警恢复========**
{{ template "___text_alertresovle_list" .Alerts.Resolved }}
{{- end }}
{{- end }}
{{/* Legacy */}}
{{ define "legacy.title" }}{{ template "__subject" . }}{{ end }}
{{ define "legacy.content" }} [{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{
.Alerts.Firing | len }}{{ end }}\] **[{{ index .GroupLabels "alertname" }}]({{
template "__alertmanagerURL" . }})**
{{ template "__text_alert_list" .Alerts.Firing }}
{{- end }}
{{/* Following names for compatibility */}}
{{ define "_ding.link.title" }}{{ template "_default.title" . }}{{ end }}
{{ define "_ding.link.content" }}{{ template "_default.content" . }}{{ end }}
#模板语言解析
添加图标格式： ![警报 图标](http://fqdn/url/图片文件名)
该图片地址必须是全网都能够访问的一个地址
日期时间不要乱改，这是golang语言的时间格式
```

#### 5.8.2.4 应用告警模板
```text
vim /usr/local/dingtalk/conf/config.yml
......
#添加下面五行
templates:
  - '/usr/local/dingtalk/contrib/templates/dingtalk.tmpl'
default_message:
  title: '{{ template "_ding.link.title" . }}'
  text: '{{ template "_ding.link.content" . }}'
.......
targets:
  webhook1:
    url: https://oapi.dingtalk.com/robot/send?access_token=TOKEN
    # secret for signature
    secret: TOKEN
#重启dingtalk服务
/usr/local/dingtalk/bin/prometheus-webhook-dingtalk --
config.file=/usr/local/dingtalk/conf/config.yml --web.listen-address=0.0.0.0:8060
#显示以下信息
level=info ts=2022-04-16T14:29:51.822Z caller=entry.go:26 component=web
http_scheme=http http_proto=HTTP/1.1 http_method=POST remote_addr=10.0.0.101:54204
user_agent=Alertmanager/0.23.0 uri=http://10.0.0.100:8060/dingtalk/webhook1/send
resp_status=200 resp_bytes_length=2 resp_elapsed_ms=586.517974 msg="request complete"
```

#### 5.8.2.5 测试验证

尝试关闭web服务和重启web服务，查看自定义告警文件信息

![原 PDF 第 222 页插图](assets/img-5749912f9f265b64.png)

恢复web服务和重启web服务，查看自定义告警文件信息

![原 PDF 第 223 页插图](assets/img-49ae1e38d1aa3c1b.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/14-wechat-alerting.html' | relative_url }}">← 上一章：微信告警</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/16-alertmanager-ha.html' | relative_url }}">下一章：Alertmanager 高可用与其他应用 →</a>
</nav>
