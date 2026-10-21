---
layout: default
title: "MySQL 性能调优 · 数据页、Buffer Pool 与读写路径"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 18 数据页、Buffer Pool 与读写路径

## 先理解缓存，再讨论内存参数

MySQL Server 层解析与优化 SQL，InnoDB 存储引擎管理索引页、行记录和事务。MySQL 8.0 已移除 query cache；分析架构时应区分 Server 层与 InnoDB 的缓存和读写职责。Buffer Pool 缓存数据页与索引页，修改后的页成为脏页；刷盘由后台机制协调，而不是每条更新都立即随机写回数据文件。

```sql
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_read%';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_pages_dirty';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';
```

缓存命中率要结合工作集、扫描模式和 I/O 延迟看，不能单凭一个高百分比断言没有瓶颈。固定“内存占比 60–70%”不是普适配置建议。[官方参考：Buffer Pool](https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html)。



## 从 SQL 到存储引擎的访问路径

### MySQL的内部组件结构

![数据页、Buffer Pool 与读写路径配图](assets/innodb-logs-001-8b037d012a4e.webp)

大体来说，MySQL 可以分为 Server 层和存储引擎层两部分。

### Server层

Server 层包括连接管理、SQL 解析、优化、执行等跨存储引擎能力。旧版本的查询缓存已在 MySQL 8.0 移除，不属于当前查询路径。

### 存储引擎层

存储引擎层负责数据的存储和提取。其架构模式是插件式的，支持 InnoDB、MyISAM、Memory 等多个存储引擎。现在最常用的存储引擎是 InnoDB，它从 MySQL 5.5.5 版本开始成为了默认存储引擎。也就是说如果我们在create table时不指定表的存储引擎类型,默认会给你设置存储引擎为InnoDB。

沿着连接器、解析器、优化器与执行器的顺序看一次查询，再进入 InnoDB 的数据页与日志机制。

#### 连接器

我们知道由于MySQL是开源的，他有非常多种类的客户端：navicat,mysql front,jdbc,SQLyog等非常丰富的客户端，包括各种编程语言实现的客户端连接程序，这些客户端要向mysql发起通信都必须先跟Server端建立通信连接，而建立连接的工作就是有连接器完成的。

第一步，你会先连接到这个数据库上，这时候接待你的就是连接器。连接器负责跟客户端建立连接、获取权限、维持和管理连接。连接命令一般是这么写的：

```bash
mysql -h HOST -u USER -p -P 3306
# 密码通过交互输入，避免写在命令行参数中。
```

连接命令中的 mysql 是客户端工具，用来跟服务端建立连接。在完成经典的 TCP 握手后，连接器就要开始认证你的身份，这个时候用的就是你输入的用户名和密码。

- 用户名或密码不匹配时，客户端会收到认证错误；认证成功后，服务器按账号与权限规则处理后续请求。权限缓存及重检时机因权限类型而异，不能概括为整个连接期只读取一次权限。

修改全局权限、数据库权限或表列权限后，对现有连接的生效时机可能不同；应按具体 `GRANT`、`REVOKE` 与版本验证。重要权限变更还应检查并清理不再需要的现有会话。

#### 查询缓存的版本边界

MySQL 8.0 已移除旧 query cache。查询性能分析应关注 Buffer Pool、执行计划、应用缓存与实际 I/O，而不是旧参数 query_cache_type。

#### 分析器

MySQL 8.0 解析 SQL 后生成内部语法结构；随后优化器比较可用访问路径，最后由执行器调用存储引擎。旧版查询缓存不参与此流程。

分析器先会做“词法分析”。你输入的是由多个字符串和空格组成的一条 SQL 语句，MySQL 需要识别出里面的字符串分别是什么，代表什么。

MySQL 从你输入的"select"这个关键字识别出来，这是一个查询语句。它也要把字符串“T”识别成“表名 T”，把字符串“ID”识别成“列 ID”。

做完了这些识别以后，就要做“语法分析”。根据词法分析的结果，语法分析器会根据语法规则，判断你输入的这个 SQL 语句是否满足 MySQL 语法。

如果你的语句不对，就会收到“You have an error in your SQL syntax”的错误提醒，比如下面这个语句 from 写成了 "rom"。

```sql
select * fro test where id=1;
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'fro test where id=1' at line 1
```

### 下图是分析器对sql的分析过程步骤：

![数据页、Buffer Pool 与读写路径配图](assets/innodb-logs-002-472114e5c688.webp)

SQL语句经过分析器分析之后，会生成一个这样的语法树

![数据页、Buffer Pool 与读写路径配图](assets/innodb-logs-003-4ba32ab7d2d9.webp)

至此我们分析器的工作任务也基本圆满了。接下来进入到优化器

#### 优化器

经过了分析器，MySQL 就知道你要做什么了。在开始执行之前，还要先经过优化器的处理。

优化器是在表里面有多个索引的时候，决定使用哪个索引；或者在一个语句有多表关联（join）的时候，决定各个表的连接顺序；以及一些mysql自己内部的优化机制。

#### 执行器

执行前还要进行权限检查；权限检查点与具体语句和版本有关，不应以旧版查询缓存的特例解释当前行为。

```sql
select * from test where id=10;
```

如果有权限，就打开表继续执行。打开表的时候，执行器就会根据表的引擎定义，去使用这个引擎提供的接口。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/17-lock-waits-deadlocks.html' | relative_url }}">← 上一篇：锁等待、死锁与排障</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/19-redo-undo.html' | relative_url }}">下一篇：redo、undo 与提交耐久性 →</a>
</nav>
