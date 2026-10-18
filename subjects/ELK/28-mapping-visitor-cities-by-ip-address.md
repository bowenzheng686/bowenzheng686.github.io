---
layout: default
title: "ELK 日志分析 · 通过坐标地图统计网站访问用户的 IP 所在城市"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回ELK 日志分析目录]({{ '/subjects/ELK/' | relative_url }})

{% raw %}

# 28 通过坐标地图统计网站访问用户的 IP 所在城市
### 6.3 通过坐标地图统计网站访问用户的 IP 所在城市

注意: 7.X 前地图功能要求必须使用 logstash 开头的索引名称,8.X无此要求

### 下载并解压地址数据文件（可选）

先获取IP数据库两种方式

官方网站 elasticsearch和logstash包内置

官方网站链接

<https://www.maxmind.com/>

早期直接下载,现在必须注册登录后,在用户帐户页面下载

![ELK 日志分析第 410 页插图](assets/img-0814861dc8acf164.png)

<https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en>

![ELK 日志分析第 410 页插图](assets/img-8fdfb44e3930ff77.png)

![ELK 日志分析第 411 页插图](assets/img-b86f4d4bfb7a56fc.png)

```bash
[root@es-node1 ~]#wget
'https://download.maxmind.com/app/geoip_download_by_token?edition_id=GeoLite2-
City&date=20210202&suffix=tar.gz&token=v2.local.BgAHbu3hNj12U4MC0BNR1IEHJmykzhP3
eNMAtADgDcjcwc4AI4uShA3KLgabS1tian8XFMNpsULdUSlkyiJcJvl0rKQ3zvrAuDBLRIUGwml6_ewl
R24scqvtUK79oQ1HG0YmhSPHiPJsJsi93K-_8Jz4b5HFkCFSbnfvlTfes6j7MlLW01tks4SGviCb1u-
6r-8_8A' -O GeoLite2-City_`date +%Y%M%d`.tar.gz
[root@logstash1 ~]#ll -h GeoLite2-City_20210202.tar.gz
-rw-r--r-- 1 root root 29M Feb  9 23:03 GeoLite2-City_20210202.tar.gz
[root@logstash1 ~]#tar xf GeoLite2-City_20210202.tar.gz  -C /etc/logstash/
[root@logstash1 ~]#ln -s /etc/logstash/GeoLite2-City_20210202/
/etc/logstash/GeoLite2-City
[root@logstash1 ~]#ll -h /etc/logstash/GeoLite2-City/GeoLite2-City.mmdb
-rw-r--r-- 1 root root 59M Feb  3 00:01 /etc/logstash/GeoLite2-City/GeoLite2-
City.mmdb
```

范例：elasticsearch和logstash 包内置数据库

```bash
#8.X elasticsearch 不在内置数据库
[root@ubuntu2204 ~]#dpkg -L elasticsearch |grep -i GeoLite2
#8.X logstash 包仍内置数据库
[root@ubuntu2204 ~]#dpkg -L logstash |grep GeoLite2-City.mmdb|xargs ls -lh
-rw-r--r-- 1 root root 60M  1月 24 18:42
/usr/share/logstash/vendor/bundle/jruby/2.6.0/gems/logstash-filter-geoip-7.2.12-
java/vendor/GeoLite2-City.mmdb
```

```bash
[root@ubuntu1804 ~]#dpkg -L elasticsearch |grep GeoLite2-City.mmdb|xargs ls -lh
-rw-r--r-- 1 root root 60M Mar 26  2020 /usr/share/elasticsearch/modules/ingest-
geoip/GeoLite2-City.mmdb
[root@ubuntu1804 ~]#dpkg -L logstash |grep GeoLite2-City.mmdb|xargs ls -lh
-rw-r--r-- 1 logstash logstash 59M Mar 26  2020
/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-filter-geoip-6.0.3-
java/vendor/GeoLite2-City.mmdb
```

### 配置 Filebeat 配置文件

```bash
[root@centos8 ~]#cat /etc/filebeat/filebeat.yml
filebeat.inputs:
- type: log
enabled: true
paths:
- /var/log/nginx/access_json.log
json.keys_under_root: true
json.overwrite_keys: true
tags: ["nginx-access"]
- type: log
enabled: true
paths:
- /var/log/nginx/error.log
tags: ["nginx-error"]
- type: log
enabled: true
paths:
- /var/log/syslog
tags: ["syslog"]
output.kafka:
hosts: ["10.0.0.201:9092", "10.0.0.202:9092", "10.0.0.203:9092"]
topic: filebeat-log
partition.round_robin:
reachable_only: true
required_acks: 1
compression: gzip
max_message_bytes: 1000000
```

### 配置 Logstash 使用地址库

地理位置字段geoip.coordinates的数据类型早期为浮点数，从8.X开始变为geo_point类型的字段。

<https://www.elastic.co/guide/en/elasticsearch/reference/master/geo-point.html>

范例：

```bash
#使用Logstash内置的地图库
#8.X,此步可选
[root@ubuntu2204 ~]#cp
/usr/share/logstash/vendor/bundle/jruby/2.6.0/gems/logstash-filter-geoip-7.2.12-
java/vendor/GeoLite2-City.mmdb /etc/logstash/conf.d/
[root@ubuntu2204 ~]#ll -h /etc/logstash/conf.d/GeoLite2-City.mmdb
-rw-r--r-- 1 root root 60M  2月 19 10:58 /etc/logstash/conf.d/GeoLite2-City.mmdb
#7.X
[root@ubuntu1804 ~]#cp
/usr/share/logstash/vendor/bundle/jruby/2.5.0/gems/logstash-filter-geoip-6.0.3-
java/vendor/GeoLite2-City.mmdb /etc/logstash/conf.d/
[root@ubuntu1804 ~]#ls -lh /etc/logstash/conf.d/
total 59M
-rw-r--r-- 1 root root  59M Aug 27 08:50 GeoLite2-City.mmdb
-rw-r--r-- 1 root root 1.2K Aug 27 10:59 kafka-to-es.conf
#修改logstash配置
[root@logstash ~]#vim /etc/logstash/conf.d/kafka-to-es.conf
input {
kafka {
bootstrap_servers => "10.0.0.201:9092,10.0.0.202:9092,10.0.0.203:9092"
topics => "filebeat-log"
codec => "json"
}
}
filter {
if "nginx-access" in [tags] {
geoip {
source => "clientip"      #日志必须是json格式,且有一个clientip的key
target => "geoip"
database => "/usr/share/logstash/vendor/bundle/jruby/3.1.0/gems/logstash-
filter-geoip-7.3.0-java/vendor/GeoLite2-City.mmdb" #8.15.0 必选项
#database => "/etc/logstash/conf.d/GeoLite2-City.mmdb"    #指定数据库文件,可选
add_field => ["[geoip][coordinates]","%{[geoip][geo][location][lon]}"]
#8.X添加经纬度字段包括经度
add_field => ["[geoip][coordinates]","%{[geoip][geo][location][lat]}"]
#8.X添加经纬度字段包括纬度
#add_field => ["[geoip][coordinates]", "%{[geoip][longitude]}"] #7,X添加经纬
度字段包括经度
#add_field => ["[geoip][coordinates]", "%{[geoip][latitude]}"]  #7,X添加经纬
度字段包括纬度
}
#转换经纬度为浮点数，注意：8X必须做，7.X 可不做此步
mutate {
convert => [ "[geoip][coordinates]", "float"]
}
}
}
output {
#stdout {}   #调试使用
if "nginx-access" in [tags] {
elasticsearch {
hosts => ["10.0.0.101:9200","10.0.0.102:9200","10.0.0.103:9200"]
index => "logstash-kafka-nginx-accesslog-%{+YYYY.MM.dd}"
#注意: 7.X之前版本地图功能要求必须使用 logstash 开头的索引名称
}
}
if "nginx-error" in [tags] {
elasticsearch {
hosts => ["10.0.0.101:9200","10.0.0.102:9200","10.0.0.103:9200"]
index => "logstash-kafka-nginx-errorlog-%{+YYYY.MM.dd}"
}
}
if "syslog" in [tags] {
elasticsearch {
hosts => ["10.0.0.101:9200","10.0.0.102:9200","10.0.0.103:9200"]
index => "logstash-kafka-syslog-%{+YYYY.MM.dd}"
}
}
}
[root@logstash ~]#/usr/share/logstash/bin/logstash -f
/etc/logstash/conf.d/redis-to-es.conf  -t
[root@logstash ~]#systemctl restart logstash.service
```

### 写入 Nginx 的访问日志数据

```bash
[root@elk-web1 ~]#tail -n 1000 json.log  >>
/data/nginx/logs/nginx.access_json.log
```

### Head 插件确认索引成功

![ELK 日志分析第 414 页插图](assets/img-0eaffd9486e28382.png)

![ELK 日志分析第 414 页插图](assets/img-eee7d856c2bb5118.png)

### Kibana 创建索引模式(数据视图)

8.X

![ELK 日志分析第 415 页插图](assets/img-142edcfb2fd5594e.png)

![ELK 日志分析第 415 页插图](assets/img-4a271f5b4e5fe3bd.png)

7.X

![ELK 日志分析第 416 页插图](assets/img-49d4f55811ee8c5f.png)

![ELK 日志分析第 416 页插图](assets/img-99eac9efed087def.png)

确认出现geoip 相关字段

![ELK 日志分析第 416 页插图](assets/img-030d8d7334513f3c.png)

![ELK 日志分析第 417 页插图](assets/img-6dc3819562eac53c.png)

![ELK 日志分析第 417 页插图](assets/img-c7f7ca396b674530.png)

### Kibana 创建地图数据

对于区域地图、坐标地图、Coordinate Map之类的图形展示，新版的Kibana已经将其整合到了一个统一的功能模块 Map. 通过左侧边栏的 analytics的Maps中来创建图形

### 查看 Kibana 样例地图

![ELK 日志分析第 418 页插图](assets/img-b629d9d9f5bf1871.png)

![ELK 日志分析第 418 页插图](assets/img-f02db73677737b8c.png)

查看内置的数据视图

![ELK 日志分析第 419 页插图](assets/img-f7e23359ee9c6501.png)

![ELK 日志分析第 419 页插图](assets/img-b76850ced8376441.png)

![ELK 日志分析第 420 页插图](assets/img-83b0832596c5e4d3.png)

![ELK 日志分析第 420 页插图](assets/img-453775ffda43b886.png)

![ELK 日志分析第 421 页插图](assets/img-0b8a62716d41d693.png)

![ELK 日志分析第 421 页插图](assets/img-bfc17f6bda438b91.png)

![ELK 日志分析第 422 页插图](assets/img-5b4cbbe0ce081e50.png)

换一种风格显示

![ELK 日志分析第 422 页插图](assets/img-e22760f0d3eaa9a2.png)

### 创建地图

```text
7.x支持 float格式，8.x支持geo_point类型。
```

6.3.7.2.1 8.X 实现

![ELK 日志分析第 423 页插图](assets/img-deed0f11582200bc.png)

![ELK 日志分析第 423 页插图](assets/img-7aaf6eee66d3ab2a.png)

默认的地理位置字段的类型导致出现下面的错误

![ELK 日志分析第 424 页插图](assets/img-93996a6243d11f59.png)

说明

ES8 要求地图数据类型geo_point类型，在logstash的地址信息的格式使用mutate（支持的数据类型： integer，integer_eu，float，float_eu，string，boolean）可以转换成 float类型而不支持geo_point类型，所以需要转换一下logstash在传递信息到es时候的模板信息，将地址信息转换成geo_point类型即可

解决方案：

获取模板修改模板使用模板

在开发工具执行下面指令，获取模版设置，复制mappings块中的所有内容

```text
# 查看生成的索引信息
GET /nginxaccess-2021.04.19
GET /logstash-kafka-nginx-accesslog-2022.03.02
#复制mappings开始的行到settings行之前结束,并最后再加一个 }
```

![ELK 日志分析第 425 页插图](assets/img-7006c753b4871a16.png)

执行下面操作生成索引模板，将上面的mappings部分内容复制到下面，只修改"coordinates": {  "type": "geo_point" } 部分

```json
PUT /_template/template_nginx_accesslog   #模板名称可以自定义
{
"index_patterns" : [
"nginxaccess-*"                      #8.X数据视图对应的索引模式，匹配索引名称的模
式
#"logstash-kafka-nginx-accesslog-*"  #8.X数据视图对应的索引模式，匹配索引名称的模
式
],
"order" : 0,
"aliases" : { },
"mappings": {                 #复制mappings开始的行到settings行之前结束,并最后再加一
个 }
"properties": {
.......
"geoip": {
"properties": {
"coordinates": {
"type": "geo_point",      #只修改此行,原值为float改为geo_point
.......
}
#必须要先删除旧的索引数据,上面修改才能生效
```

![ELK 日志分析第 426 页插图](assets/img-be0b46e82c260fcf.png)

查看生成的索引模板

![ELK 日志分析第 426 页插图](assets/img-9506605a81247dc7.png)

必须先删除旧有索引重新生成数据才能生效

```bash
#数据量不足可以多执行几次
[root@ubuntu2204 ~]#cat   access_json.log-20220304 >>
/var/log/nginx/access_json.log
```

确认类型是否修改

![ELK 日志分析第 427 页插图](assets/img-36a06e8b42559149.png)

![ELK 日志分析第 427 页插图](assets/img-0e942d4cb79d1645.png)

![ELK 日志分析第 427 页插图](assets/img-6e74d91e1ce803b9.png)

重新创建图形

![ELK 日志分析第 428 页插图](assets/img-e7be2096a02a16fc.png)

![ELK 日志分析第 428 页插图](assets/img-935cea5de5f8300e.png)

![ELK 日志分析第 429 页插图](assets/img-3dc418d5ccb1fc5a.png)

![ELK 日志分析第 429 页插图](assets/img-431e07971aa8ae55.png)

生成热图

![ELK 日志分析第 430 页插图](assets/img-a893ddd74c330b79.png)

![ELK 日志分析第 430 页插图](assets/img-6f21ac8e377df428.png)

![ELK 日志分析第 431 页插图](assets/img-0585d21b47588474.png)

![ELK 日志分析第 431 页插图](assets/img-b9465ec235fe4d20.png)

6.3.7.2.2 7.X 实现

![ELK 日志分析第 432 页插图](assets/img-137c3d3fd9ee937b.png)

![ELK 日志分析第 432 页插图](assets/img-9eee030c16fc9e03.png)

![ELK 日志分析第 433 页插图](assets/img-a361a1bfd67e6414.png)

![ELK 日志分析第 433 页插图](assets/img-8ce6117e52f601c1.png)

![ELK 日志分析第 434 页插图](assets/img-ad21227f04684a5b.png)

将默认地图更换成成中文地图

```text
7.X 默认是英文的地图，如果希望是是中文地图的话，可以通过配置文件修改地图的引用地址即可
#将地图更换成高德地图，在kibana的配置文件中，添加如下配置
grep map /etc/kibana/kibana.yml
map.tilemap.url: 'http://webrd02.is.autonavi.com/appmaptile?
lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'
#重启服务
systemctl restart kibana.service
```

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/ELK/27-collecting-nginx-logs-with-filebeat-and-kafka-buffering.html' | relative_url }}">← Previous: Collecting Nginx Logs with Filebeat and Kafka Buffering</a>
  <a href="{{ '/subjects/ELK/' | relative_url }}">Back to ELK Log Analytics Index</a>
  <a href="{{ '/subjects/ELK/29-writing-collected-logs-to-mysql-with-logstash.html' | relative_url }}">Next: Writing Collected Logs to MySQL with Logstash →</a>
</nav>
