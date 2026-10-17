---
layout: default
title: "Prometheus · Grafana 展示与监控"
subject_page: true
prometheus_notes: true
syntax_highlight: true
---

[← 返回 Prometheus 目录]({{ '/subjects/Prometheus/' | relative_url }})

{% raw %}

# 04 Grafana 展示与监控

## 2.4 Grafana 展示 Prometheus 数据

### 2.4.1 Grafana 简介

Grafana是一个开源的度量分析与可视化套件，它基于go语言开发。经常被用作基础设施的时间序列数据和应用程序分析的可视化，应用场景非常多。

Grafana不仅仅支持很多类型的时序数据库数据源，比如Graphite、InfluxDB、Prometheus、Elasticsearch等，虽然每种数据源都有独立的查询语言和能力，但是Grafana的查询编辑器支持所有的数据源，而且能很好的支持每种数据源的特性。

通过该查询编辑器可以对所有数据进行整合，而且还可以在同一个dashboard上进行综合展示。

Grafana最具特色的就是各种各样漂亮的可视化界面，在Grafana提供了各种定制好的，可以直接给各种软件直接使用的展示界面模板

Grafana 默认监听于TCP协议的3000端口，支持集成其他认证服务，且能够通过/metrics输出内建指标

可以在https://grafana.com/dashboards/页面查询到我们想要的各种dashboard模板。

### 2.4.2 Grafana 部署

Grafana官方下载链接
https://grafana.com/grafana/download

在prometheus服务器同时也安装grafana

#### 2.4.2.1 基于包安装
```bash
#下载软件
[root@ubuntu2204 ~]#wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.3.1_amd64.deb
[root@grafana ~]#wget https://dl.grafana.com/enterprise/release/grafana-enterprise_8.2.1_amd64.deb
#从国内镜站下载
[root@grafana ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/grafana/apt/pool/main/g/grafana-enterprise/grafana-enterprise_10.0.0_amd64.deb
[root@grafana ~]#wget
https://mirrors.tuna.tsinghua.edu.cn/grafana/apt/pool/main/g/grafana/grafana_9.0.6_amd64.deb
#安装
#方法1：手动安装依赖包
https://grafana.com/grafana/download
[root@ubuntu2004 ~]#sudo apt-get install -y adduser libfontconfig1 musl
[root@ubuntu2004 ~]#wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.2.0_amd64.deb
[root@ubuntu2004 ~]#sudo dpkg -i grafana-enterprise_11.2.0_amd64.deb
#方法2:可以解决依赖关系
[root@ubuntu2004 ~]#apt update && apt -y install ./grafana-enterprise_8.2.1_amd64.deb
#注意：安装的是本地文件，所以要加文件路径
#方法3:需要解决依赖关系
[root@ubuntu2004 ~]#dpkg -i grafana_9.0.6_amd64.deb
Selecting previously unselected package grafana.
(Reading database ... 76356 files and directories currently installed.)
Preparing to unpack grafana_8.5.9_amd64.deb ...
Unpacking grafana (8.5.9) ...
dpkg: dependency problems prevent configuration of grafana:
 grafana depends on libfontconfig1; however:
  Package libfontconfig1 is not installed.
dpkg: error processing package grafana (--install):
 dependency problems - leaving unconfigured
Processing triggers for systemd (245.4-4ubuntu3.11) ...
Errors were encountered while processing:
 grafana
#提示依赖失败,执行下面修复依赖
[root@ubuntu2004 ~]#apt -y --fix-broken install
#启动服务
[root@ubuntu2004 ~]#systemctl enable --now  grafana-server
[root@ubuntu2004 ~]#systemctl status grafana-server
[root@grafana ~]#
[root@grafana ~]#
#如果安装失败,解决依赖关系
[root@grafana ~]#apt -y --fix-broken install
#查看插件列表(此步可选)
[root@grafana ~]#grafana-cli plugins list-remote
#安装饼状图的插件,如果安装失败,多试几次(此步可选)
[root@grafana ~]#grafana-cli plugins install grafana-piechart-panel
[root@grafana ~]#grafana-cli plugins ls
#安装的插件存放在如下目录中
[root@grafana ~]#ls /var/lib/grafana/plugins/
#启动服务
[root@grafana ~]#systemctl daemon-reload
[root@grafana ~]#systemctl enable --now  grafana-server.service
#检查效果
[root@grafana ~]#systemctl status grafana-server.service
[root@grafana ~]#ss -ntulp|grep grafana
tcp     LISTEN   0  4096           *:3000       *:*      users:(("grafana-
server",pid=35383,fd=8))
#结果显示：当前主机上出现了一个端口3000
```

#### 2.4.2.2 基于docker 安装
https://hub.docker.com/r/grafana/grafana

范例:
```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

### 2.4.3 配置 Prometheus 数据源

#### 2.4.3.1 登录 Grafana Web
```text
#浏览器访问 http://master1.bowen.org:3000/，查看效果
#输入用户名和密码：admin/admin，就会进入到更改密码的页面，查看效果
```

![原 PDF 第 60 页插图](assets/img-6b7dab41a4a4b364.png)

![原 PDF 第 60 页插图](assets/img-fceb50d3fdc253fb.png)

输入更改后的密码后，此处为了方便还用原来的密码admin, 点击"Submit"后，就会进入到首页，查看效果

#### 2.4.3.2 添加 Prometheus 的数据源

添加数据源: 点击 "Add your first data source"

![原 PDF 第 61 页插图](assets/img-fb3d83af4ee45e0d.png)

选择 "Prometheus" 出现添加界面

![原 PDF 第 61 页插图](assets/img-0ed1f587e44caf40.png)

按照如下配置信息，在Settings界面对Prometheus进行配置，效果如下

![原 PDF 第 61 页插图](assets/img-223d96fec118e90c.png)
```text
#输入Prometheus的地址(10.0.0.101:9090或者localhost:9090)，其它没有做任何变动。
```

![原 PDF 第 62 页插图](assets/img-733dd780b08c54b4.png)

其它信息不用设置，点击最下面的"Save & Test" 查看效果

![原 PDF 第 62 页插图](assets/img-92e96c45a208700f.png)

#### 2.4.3.3 使用数据源插件中内置的Dashboard

点Dashboards页签内的import,导入内置的三个模板

![原 PDF 第 62 页插图](assets/img-089cb28d7897e49e.png)

![原 PDF 第 63 页插图](assets/img-d307b3086d112696.png)

查看默认的三个模板

![原 PDF 第 63 页插图](assets/img-397968f03d0acae3.png)

![原 PDF 第 63 页插图](assets/img-1bb8d874b5d24062.png)

注意: 由于没有将grafana纳入到prometheus监控的target,所以以下没有数据

![原 PDF 第 64 页插图](assets/img-f9058baedf2a192e.png)

只要将grafana:3000/metrics加入prometheus的配置文件即可实现下图的正常显示

![原 PDF 第 64 页插图](assets/img-7615108942b3f691.png)

### 2.4.4 导入指定模板展示 Node Exporter 数据

上面内置的模板不太理想,导入指定的网络上比较合适的 Dashboard 模板

#### 2.4.4.1 登录 Grafana 官网查找模板
https://grafana.com/grafana/dashboards/

![原 PDF 第 65 页插图](assets/img-a7af026d70a3b97c.png)

![原 PDF 第 65 页插图](assets/img-0e55473f9abd4c78.png)

![原 PDF 第 66 页插图](assets/img-e3566e7af8e2de2c.png)

#### 2.4.4.2 导入指定模板

导入8919（中文）,1860,11074,13978模板

![原 PDF 第 66 页插图](assets/img-79ac23fc55146a7f.png)
点击"import",将"https://grafana.com/dashboards/8919或1860或11074"添加到如下位置，点 Load
后效果如下

![原 PDF 第 67 页插图](assets/img-fda9df99c75be300.png)
```text
#注意：选择dashboard的时候，一定要选择合适版本,否则会导致无法正常使用
```

然后就会自动将改dashboard资源显示出来，效果如下

![原 PDF 第 67 页插图](assets/img-23350db9ec8c67a6.png)
```text
#注意：一定要选择需要可视化的数据源。
```

在Prometheus Data Source右侧选择刚才配置的Prometheus数据源即可，然后点击"Import",查看效果

![原 PDF 第 67 页插图](assets/img-7ab19293a1bc00c6.png)

结果显示：node_exporter部署完毕后，节点的信息立刻就展示出来了。

如果看不到数据的话

没有安装节点监控 NodePort软件
浏览器的时间与服务器的时间误差超过3s以上  

再次导入1860 模板

![原 PDF 第 68 页插图](assets/img-1a92249b9a6c90fb.png)

## 2.5 监控 Grafana

Grafana 内置了支持Prometheus监控接口

### 2.5.1 配置 Prometheus 监控 Grafana
```yaml
[root@prometheus ~]#vim /usr/local/prometheus/conf/prometheus.yml
.....
  - job_name: 'grafana'  #添加以下行,指定监控的grafan节点,job_name 应该为grafana，通过此名
称实现展示
    static_configs:
    - targets: ['grafana.bowen.org:3000']
......
[root@prometheus ~]#systemctl reload prometheus
```

### 2.5.2 Grafana 展示 Grafana 自身状态

在 Grafana 的数据源 Prometheus  中内置模板 Grafana metrics 中即可展示 Grafana 的状态

![原 PDF 第 69 页插图](assets/img-a2821b0f04993f28.png)

![原 PDF 第 69 页插图](assets/img-a34cc6d93f64a47d.png)

![原 PDF 第 69 页插图](assets/img-7615108942b3f691.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Prometheus/03-node-exporter.html' | relative_url }}">← 上一章：Node Exporter 安装与采集</a>
  <a href="{{ '/subjects/Prometheus/' | relative_url }}">返回 Prometheus 目录</a>
  <a href="{{ '/subjects/Prometheus/05-zookeeper-monitoring.html' | relative_url }}">下一章：Zookeeper 监控 →</a>
</nav>
