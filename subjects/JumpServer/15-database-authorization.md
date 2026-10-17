---
layout: default
title: "JumpServer Bastion Host · Database Authorization"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← Back to JumpServer Bastion Host Index]({{ '/subjects/JumpServer/' | relative_url }})

{% raw %}

# 15 Database Authorization
### 3.5 数据库授权

注意: JumpServer v2.5 此功能有Bug ,可以选择 V2.4版或者其它版本

### 在后端服务器安装MySQL并创建数据库和用户

范例：容器运行MySQL

```bash
[root@ubuntu2204 ~]#docker run -d --name mysql -p 3306:3306 -e
MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wordpress -e
MYSQL_PASSWORD=123456 registry.cn-beijing.aliyuncs.com/bowenxiaochun/mysql:8.0.29-
oracle
```

范例：Ubuntu 安装 MySQL

```bash
[root@ubuntu2204 ~]#apt -y install mysql-server
[root@ubuntu2204 ~]#sed -i '/127.0.0.1/s/^/#/'
/etc/mysql/mysql.conf.d/mysqld.cnf
[root@ubuntu2204 ~]#vim /etc/mysql/mysql.conf.d/mysqld.cnf
#bind-address           = 127.0.0.1
#mysqlx-bind-address    = 127.0.0.1
[root@ubuntu2204 ~]#systemctl restart mysql
[root@ubuntu2204 ~]#mysql
mysql> create database wordpress;
mysql> create user wordpress@'10.0.0.%' identified by '123456';
mysql> grant all on wordpress.* to wordpress@'10.0.0.%' ;
```

### 创建数据库的系统用户

创建针对数据库的专用系统用户

新版

在账号模版创建

![JumpServer 堡垒机第 80 页插图](assets/img-4c2e7e34e41393cf.png)

### 创建数据库资产（应用）

![JumpServer 堡垒机第 80 页插图](assets/img-7f2959bdf0aa6edc.png)

![JumpServer 堡垒机第 81 页插图](assets/img-6fbc5e8e0079c71f.png)

![JumpServer 堡垒机第 81 页插图](assets/img-6b8d4dbf6766b0f8.png)

### 创建数据库授权规则

数据库应用的授权规则合并到到到资产授权中，需要在资产授权中针对指定资产数据数专门做授权，不支持针对节点授权

![JumpServer 堡垒机第 82 页插图](assets/img-36d6d2da65192c50.png)

### 测试数据库连接

### web 方式连接MySQL资产

![JumpServer 堡垒机第 82 页插图](assets/img-8080e03d35d36c7e.png)

![JumpServer 堡垒机第 83 页插图](assets/img-889cf4be0a6972ec.png)

![JumpServer 堡垒机第 83 页插图](assets/img-ca4f6b5cdd91037d.png)

### 用ssh连接MySQL资产

![JumpServer 堡垒机第 83 页插图](assets/img-fd128c7e95b7068e.png)

![JumpServer 堡垒机第 83 页插图](assets/img-add7d7bfe15c6039.png)

![JumpServer 堡垒机第 84 页插图](assets/img-dd99e6255d92e225.png)

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/JumpServer/14-granting-users-access-to-assets.html' | relative_url }}">← Previous: Granting Users Access to Assets</a>
  <a href="{{ '/subjects/JumpServer/' | relative_url }}">Back to JumpServer Bastion Host Index</a>
  <a href="{{ '/subjects/JumpServer/16-session-management.html' | relative_url }}">Next: Session Management →</a>
</nav>
