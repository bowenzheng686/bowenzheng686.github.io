---
layout: default
title: "Prometheus · 微信告警"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 14 微信告警

## 5.7 微信告警

### 5.7.1 微信告警说明

微信是我们日常使用的通信工具，而且通信的效率非常的高，下面介绍微信的告警方式。

就目前来说，使用微信告警的方式主要有以下三种：

用个人号发送告警 - 一般需要借助于专属的开发工具来实现
用公众号发送告警 -  借助于软件本身的机制来实现。  
用企业号发送告警 -  借助于软件本身的机制来实现。此为推荐方式  

对于公众号发送告警。但是很多个人公众号并没有开启了相关功能，无法测试很多功能，所以我们在测试微信公众号之前，可以采用官方的测试接口来实现告警功能。

微信公众号测试的接口地址:
https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

企业微信目前更为便利和普遍,如下采用企业微信实现告警

企业微信接口
```text
#获取认证token
https://qyapi.weixin.qq.com/cgi-bin/gettoken
#发送告警信息
https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="企业微信token"
#帮助手册：
获取认证：https://developer.work.weixin.qq.com/document/10013
发送消息：https://developer.work.weixin.qq.com/document/path/90236
```

实现步骤

企业微信后台配置

创建企业微信、自定义告警部门
创建企业应用认证信息  
Alertmanager配置告警通知人和告警模板  
Prometheus配置告警规则  

### 5.7.2 微信告警案例

#### 5.7.2.1 企业微信配置

5.7.2.1.1 注册企业微信

微信告警首先得注册一个企业微信，然后才能实现微信告警。

浏览器访问下面链接,注册企业微信
https://work.weixin.qq.com/

使用个人微信扫码登录后，定制自己的企业信息

注意：注册一个企业，没有任何限制，无需认证

![原 PDF 第 182 页插图](assets/img-2adb974da4747095.png)

![原 PDF 第 183 页插图](assets/img-1c92a9633a2535d3.png)

![原 PDF 第 184 页插图](assets/img-932e37134cb993b3.png)

用浏览器进入管理后台

![原 PDF 第 184 页插图](assets/img-12c041a01e7c31b7.png)

或者安装企业微信的PC端登录

![原 PDF 第 185 页插图](assets/img-676b49e382870882.png)
```text
查看到企业ID的值为 ww644a0d95807e476b
```

![原 PDF 第 185 页插图](assets/img-d865c02932d96206.png)

5.7.2.1.2 创建部门和人员

5.7.2.1.2.1 创建部门

![原 PDF 第 186 页插图](assets/img-e391701f36db7500.png)
```text
注意: 创建的部门的部门ID为2
```

![原 PDF 第 186 页插图](assets/img-12eda2398f14fdbd.png)

5.7.2.1.2.2 部门加入人员

方法1: 直接微信邀请,让相关人员自行扫码加入

![原 PDF 第 187 页插图](assets/img-c898a28e033a782e.png)

方法2 手动添加人员

![原 PDF 第 187 页插图](assets/img-03e05ed9dea58c5a.png)

![原 PDF 第 188 页插图](assets/img-fb47c04e06098162.png)

5.7.2.1.3 创建微信应用

![原 PDF 第 188 页插图](assets/img-ffb9ed12372d870b.png)

上传Logo和指定应用名称,并选择范围

![原 PDF 第 189 页插图](assets/img-96fa11f378cf1d01.png)

注意记下以下信息：
应用的 AgentId值1000004
应用的 Secret的值qYgLlipdHtZidsd8qAZaTKKkGkzIyWxuQSeQOk9Si0M

![原 PDF 第 189 页插图](assets/img-ffe62d9cfa53bdb7.png)

5.7.2.1.4 测试发送微信消息

可以给加入的员工发送微信消息

![原 PDF 第 190 页插图](assets/img-b179f217e6585b1d.png)

![原 PDF 第 190 页插图](assets/img-5ffb0a01e10cb161.png)

![原 PDF 第 190 页插图](assets/img-ada55959690465c4.png)

员工个人微信可以收到以下信息

![原 PDF 第 191 页插图](assets/img-675bb8b7fad96b4c.png)

#### 5.7.2.2 微信告警消息命令

官方微信教程
https://developer.work.weixin.qq.com/document/path/90487
https://work.weixin.qq.com/api/doc/90000/90003/90487

![原 PDF 第 191 页插图](assets/img-fc2aa31cffa22f78.png)

官方微信API参考文档
https://developer.work.weixin.qq.com/document/path/91039
https://work.weixin.qq.com/api/doc/90000/90135/91039

![原 PDF 第 191 页插图](assets/img-439db912f02aa924.png)

总结相关信息如下
查看到企业ID的值: ww644a0d95807e476b
部门ID的值: 2
应用的 AgentId的值: 1000004
应用的 Secret的值:qYgLlipdHtZidsd8qAZaTKKkGkzIyWxuQSeQOk9Si0M

5.7.2.2.1 获取 Token
```bash
#获取通信token格式：
curl -H "Content-Type: application/json" -d '{"corpid":"企业id", "corpsecret": "应用
secret"}' https://qyapi.weixin.qq.com/cgi-bin/gettoken
```

范例: 获取 Token
```bash
#示例：
[root@prometheus ~]#curl -H "Content-Type: application/json" -d
'{"corpid":"ww644a0d95807e476b", "corpsecret":
"qYgLlipdHtZidsd8qAZaTKKkGkzIyWxuQSeQOk9Si0M"}' https://qyapi.weixin.qq.com/cgi-bin/gettoken
#返回token
{"errcode":0,"errmsg":"ok","access_token":"NMaWPA8xfYmcN5v8so7TdqsBwym78Vs53X5OsOy69-
Q6Kv3GGXGU_V-8keGaArYkurIXrKMJGrdFbhYy-QqmKsr5x61-wv6yXZy0kiooXE-
QfbDoNRumBSjiJg0AqkEOeBqaT1dc8_DryE-RGVD39J4Iu61TU3HWsyZVkGuRTU6ejM-
qauflSOuy5cbDSONNXi9zUPwUmlg4XkAobrLgOw","expires_in":7200}
```

5.7.2.2.2 命令发送测试信息
```bash
#发送信息信息要求Json格式如下：
    Data = {
         "toparty": 部门id,
         "msgtype": "text",
         "agentid": Agentid,
         "text": {"content": "消息内容主题"},
         "safe": "0"
    }
#格式：
curl -H "Content-Type: application/json" -d '{"toparty": "部门id",
"msgtype":"text","agentid": "agentid", "text":{"content":"告警内容"}, "safe": "安全级
别"}' https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="企业微信token"
```

范例:
```bash
#利用上面的token发送信息,注意:token有时间期限
[root@prometheus ~]#curl -H "Content-Type: application/json" -d '{"toparty": "2",
"msgtype":"text","agentid": "1000004", "text":{"content":"PromAlert - prometheus 告警
测试"}, "safe": "0"}' https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="TOKEN"
#返回成功提示
{"errcode":0,"errmsg":"ok","msgid":"MESSAGE_ID"}
```

手机微信收到下面信息

![原 PDF 第 193 页插图](assets/img-832f98f89553aca9.png)

5.7.2.2.3 发送微信告警脚本

发送微信可以使用各种语言,下面使用shell脚本实现
```bash
cat wechat.sh
#!/bin/bash
#
#FileName:          wechat.sh
#Description:       Send message from wechat for prometheus monitor
CorpID="CORPID"
Secret="SECRET"
agentid=1000004  #改为 AgentId 在创建的应用那里看
PartyID=2  #通讯录中的部门ID
GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CorpID&corpsecret=$Secret"
Token=$(curl -s -G $GURL |awk -F\": '{print $4}'|awk -F\" '{print $2}')
#echo $Token
PURL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$Token"
function body(){
        local userid=$1  #发送的用户位于$1的字符串
        local partyid=$PartyID
        local msg=$(echo "$@" | cut -d" " -f2-)
        printf '{\n'
        printf '\t"touser": "'"$userid"\"",\n"
        printf '\t"toparty": "'"$PartyID"\"",\n"
        printf '\t"msgtype": "text",\n'
        printf '\t"agentid": "'"$agentid"\"",\n"
        printf '\t"text": {\n'
        printf '\t\t"content": "'"$msg"\""\n"
        printf '\t},\n'
        printf '\t"safe":"0"\n'
        printf '}\n'
}
curl --data-ascii "$(body $*)" $PURL
#添加执行权限
chmod +x wechat.sh
#发送测试微信，其中bowen为企业微信的帐号，并且不区分大小写
./wechat.sh bowen 微信告警测试标题 微信告警测试信息内容
{"errcode":0,"errmsg":"ok","msgid":"TGvhsTpDOJtMR4-
VhJqudSvxsnPPPXmSuXbb2iXiXw9Hk43lbS1TQ19-MDvEMZmCE02GJL9zRlG49u-hQHaXJg"}
```

在手机企业微信APP中可以收到下面提示

![原 PDF 第 194 页插图](assets/img-25e1b35a3b7f76f6.png)

#### 5.7.2.3 Alertmanager 配置

5.7.2.3.1 定制告警的配置信息
```yaml
cat /usr/local/alertmanager/conf/alertmanager.yml
# 全局配置
global:
  resolve_timeout: 5m
  #邮件信息
  smtp_smarthost: 'smtp.qq.com:25'
  smtp_from: '29308620@qq.com'
  smtp_auth_username: '29308620@qq.com'
  smtp_auth_password: 'dgezyimkdswwbhea'
  smtp_hello: 'qq.com'
  smtp_require_tls: false
  #必须项
  wechat_api_corp_id: 'ww644a0d95807e476b'
  #此处的微信信息可省略,下面wechat_configs 也提供了相关信息
  wechat_api_url: 'https://qyapi.weixin.qq.com/cgi-bin/'
  wechat_api_secret: 'qYgLlipdHtZidsd8qAZaTKKkGkzIyWxuQSeQOk9Si0M'
# 模板配置
templates:
  - '../tmpl/*.tmpl'
# 路由配置,分级告警,critical级才发微信告警,一般只发邮件告警
route:
  group_by: ['instance', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 10s
  receiver: 'email'
  routes:
  - receiver: 'wechat'  #新版写法
    matchers:
    - severity = "critical"
  #- match:                   #旧版写法
  #    severity: critical
  #  receiver: 'wechat'
# 收信人员
receivers:
- name: 'email'
  email_configs:
  - to: 'root@bowen.com'
    send_resolved: true
    html: '{{ template "test.html" . }}'
    headers: { Subject: "[WARN] 报警邮件"}
#在下面添加微信配置文件
- name: 'wechat'
  wechat_configs:
  - to_party: '2'
    #to_user: '@all' #支持给企业内所有人发送
    agent_id: '1000004'
    #api_secret: 'qYgLlipdHtZidsd8qAZaTKKkGkzIyWxuQSeQOk9Si0M'
    send_resolved: true
    message: '{{ template "wechat.default.message" . }}'
#上面的配置，关键的信息必须准确，否则无法实现告警
group_wait       #初次发送告警延时
group_interval   #距离第一次发送告警，等待多久再次发送告警
repeat_interval  #告警重发时间
#重启alertmanager服务
systemctl restart alertmanager
systemctl status alertmanager
```

5.7.2.3.2 定制告警的模板配置信息
```bash
# vim /usr/local/alertmanager/tmpl/wechat.tmpl
{{ define "wechat.default.message" }}
{{- if gt (len .Alerts.Firing) 0 -}}
{{- range $index, $alert := .Alerts -}}
{{- if eq $index 0 }}
========= 监控报警 =========
告警状态：{{   .Status }}
告警级别：{{ .Labels.severity }}
告警类型：{{ $alert.Labels.alertname }}
故障主机: {{ $alert.Labels.instance }}
告警主题: {{ $alert.Annotations.summary }}
告警详情: {{ $alert.Annotations.message }}{{ $alert.Annotations.description}};
触发阀值：{{ .Annotations.value }}
故障时间: {{ ($alert.StartsAt.Add 28800e9).Format "2006-01-02 15:04:05" }}  #注意:此为
golang的时间Format,表示123456
========= = end = =========
{{- end }}
{{- end }}
{{- end }}
{{- if gt (len .Alerts.Resolved) 0 -}}
{{- range $index, $alert := .Alerts -}}
{{- if eq $index 0 }}
========= 异常恢复 =========
告警类型：{{ .Labels.alertname }}
告警状态：{{   .Status }}
告警主题: {{ $alert.Annotations.summary }}
告警详情: {{ $alert.Annotations.message }}{{ $alert.Annotations.description}};
故障时间: {{ ($alert.StartsAt.Add 28800e9).Format "2006-01-02 15:04:05" }}
恢复时间: {{ ($alert.EndsAt.Add 28800e9).Format "2006-01-02 15:04:05" }}
{{- if gt (len $alert.Labels.instance) 0 }}
实例信息: {{ $alert.Labels.instance }}
{{- end }}
========= = end = =========
{{- end }}
{{- end }}
{{- end }}
{{- end }}
#重启alertmanager服务
systemctl reload alertmanager
systemctl status alertmanager
#检查效果
ss -tnulp | grep alert
udp     UNCONN   0  0                      *:9094                 *:*
users:(("alertmanager",pid=31732,fd=7))
tcp     LISTEN   0  4096                   *:9093                 *:*
users:(("alertmanager",pid=31732,fd=8))
tcp     LISTEN   0  4096                   *:9094                 *:*
users:(("alertmanager",pid=31732,fd=3))
```

#### 5.7.2.4 Prometheus 集成配置

5.7.2.4.1 定制告警规则
```yaml
#创建告警规则文件
vim /usr/local/prometheus/rules/prometheus_alert_route.yml
groups:
- name: flask_web
  rules:
  - alert: InstanceDown
    expr: up{job="my_metric"} == 0
    for: 10s
    labels:
      severity: critical  #指定告警级别
    annotations:
      summary: "Instance {{ $labels.instance  }} 停止工作"
      description: "{{ $labels.instance  }} job {{ $labels.job  }} 已经停止1分钟以上"
      value: "{{$value}}"
- name: flask_QPS
  rules:
  - alert: InstanceQPSIsHight
    expr: increase(request_count_total{job="my_metric"}[1m]) > 500
    for: 10s
    labels:
      severity: warning
    annotations:
      summary: "Instance {{ $labels.instance  }} QPS 持续过高"
      description: "{{ $labels.instance  }} job {{ $labels.job  }} QPS 持续过高"
      value: "{{$value}}"
```

5.7.2.4.2 修改 Prometheus 配置文件
```yaml
#在prometheus里面，配置告警规则文件生效
grep -Ev '^.*#|^$' /usr/local/prometheus/conf/prometheus.yml
global:
alerting:
  alertmanagers:
    - static_configs:
         - targets:
             - 10.0.0.100:9093
rule_files:
  - "../rules/*.yml"
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: 'node_exporter'
    static_configs:
    - targets: ['10.0.0.104:9100','10.0.0.105:9100','10.0.0.106:9100']
      labels: {app: 'k8s-node'}
  - job_name: 'my_metric'
    static_configs:
    - targets: ['10.0.0.101:8000']
      labels: {app: 'flask_web'}
#重启服务
systemctl restart prometheus
systemctl status prometheus
#检查效果
ss  -tnulp | grep prometheus
tcp     LISTEN   0  4096                   *:9090                 *:*
users:(("prometheus",pid=57535,fd=8))
```

#### 5.7.2.5 验证结果

5.7.2.5.1 停止和恢复 flask_web服务

![原 PDF 第 198 页插图](assets/img-79d42c0e93e9486e.png)

查看prometheus的告警动作

![原 PDF 第 198 页插图](assets/img-4486a5b40adbb3b8.png)

![原 PDF 第 198 页插图](assets/img-7acbd513a0feb0cf.png)

查看企业微信的告警信息

![原 PDF 第 199 页插图](assets/img-a325b1e76cbfdf8f.png)

恢复 flask_web服务,可以看到微信信息如下

![原 PDF 第 200 页插图](assets/img-3acf9cc943f8aeb9.png)

![原 PDF 第 201 页插图](assets/img-3acf9cc943f8aeb9.png)

5.7.2.5.2 高并发访问只触发邮件告警
```bash
#运行下面脚本触发高并发访问
cat curl_metrics.sh
#!/bin/bash
URL=http://127.0.0.1:8001/metrics
while true;do
    curl_num=$(($RANDOM%50+1))
    sleep_num=$(($RANDOM%5+1))
    for c_num in `seq $curl_num`;do
         curl -s $URL &> /dev/null
    done
    #sleep $sleep_num
done
bash curl_metrics.sh
```

![原 PDF 第 201 页插图](assets/img-2bb18830c07957c0.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/13-alert-templates-routing.html' | relative_url }}">← 上一章：告警模板、路由与抑制</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/15-dingtalk-alerting.html' | relative_url }}">下一章：钉钉告警 →</a>
</nav>
