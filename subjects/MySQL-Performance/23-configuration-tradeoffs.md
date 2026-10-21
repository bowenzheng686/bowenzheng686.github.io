---
layout: default
title: "MySQL 性能调优 · 字段类型与资源预算"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 23 字段类型与资源预算

## 连接、内存、日志不能分别拍脑袋

`max_connections` 决定允许的并发连接上限，但上调它不能解决慢查询导致的连接堆积；应用连接池、活跃线程数、CPU、每连接内存和操作系统文件描述符要一起评估。`innodb_buffer_pool_size` 应按实例是否独占、工作集和其他内存消耗定；排序/连接缓冲及临时表可能按会话或执行路径增加，不能简单把各缓冲值乘以连接数当作精确占用，也不能忽略极端并发风险。

```sql
SHOW VARIABLES WHERE Variable_name IN (
  'max_connections','innodb_buffer_pool_size',
  'innodb_redo_log_capacity','tmp_table_size','sort_buffer_size'
);
SHOW GLOBAL STATUS LIKE 'Max_used_connections';
```

固定内存比例、连接数公式和默认值可能随版本变化；应按“查看当前值 → 找到瓶颈 → 估算资源 → 单变量试验 → 回滚”。参数变更需注明作用域、动态生效性、重启需求和持久化方式。[官方参考：系统变量](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html)。



## 字段类型与数据布局

字段类型选择

在MySQL中，选择正确的数据类型，对于性能至关重要。一般应该遵循下面两步：

（1）确定合适的大类型：数字、字符串、时间、二进制；

（2）确定具体的类型：有无符号、取值范围、变长定长等。

选择较小的合适类型可节省存储和索引空间；是否允许 NULL 应由业务语义决定，不能一律设为 NOT NULL。

### 1、数值类型

| 类型 | 存储字节 | 有符号范围 | 无符号范围 | 用途 |
| --- | --- | --- | --- | --- |
| TINYINT | 1 | -128～127 | 0～255 | 小整数 |
| SMALLINT | 2 | -32768～32767 | 0～65535 | 小整数 |
| MEDIUMINT | 3 | -8388608～8388607 | 0～16777215 | 中整数 |
| INT | 4 | -2147483648～2147483647 | 0～4294967295 | 常用整数 |
| BIGINT | 8 | -9223372036854775808～9223372036854775807 | 0～18446744073709551615 | 大整数 |
| FLOAT / DOUBLE | 4 / 8 | 近似浮点 | 近似浮点 | 不宜直接存精确金额 |
| DECIMAL(M,D) | 依精度而定 | 依定义而定 | 依定义而定 | 十进制精确数值 |

#### 优化建议

- 如果整形数据没有负数，如ID号，建议指定为UNSIGNED无符号类型，容量可以扩大一倍。

- ENUM、SET、BIT 与整数类型的语义不同，应按值域、可迁移性和查询方式选择，不能一概用 TINYINT 替换。

- MySQL 8.0 已弃用整数显示宽度；建表时优先使用 INT 等类型本身，而不是依赖 INT(10) 的显示格式。

- DECIMAL最适合保存准确度要求高，而且用于计算的数据，比如价格。但是在使用DECIMAL类型的时候，注意长度设置。

- 金额等需要精确十进制运算的数据优先考虑 `DECIMAL`；若采用最小货币单位的整数建模，要明确单位、范围、舍入和跨系统换算规则。

- 整数适合计数、标识和离散值，`AUTO_INCREMENT` 只适用于整数列；类型仍应先满足业务语义和数值范围。

### 2、日期和时间

| 类型 | 存储 | 主要语义 | 注意事项 |
| --- | --- | --- | --- |
| DATE | 3 字节 | 日期 | 不含时分秒 |
| TIME | 3 字节起 | 时间或时长 | 可指定小数秒精度 |
| YEAR | 1 字节 | 年份 | 适用范围以版本为准 |
| DATETIME | 5 字节起 | 日期时间 | 不做会话时区转换 |
| TIMESTAMP | 4 字节起 | 时间点 | 按会话时区转换，范围受限 |

#### 优化建议

- MySQL 的 TIME、DATETIME、TIMESTAMP 可指定 0—6 位小数秒精度，不限于整秒。

- 建议用DATE数据类型来保存日期。MySQL中默认的日期格式是yyyy-mm-dd。

- 用MySQL的内建类型DATE、TIME、DATETIME来存储时间，而不是使用字符串。

- `TIMESTAMP` 和 `DATETIME` 都可在受支持版本中使用 `CURRENT_TIMESTAMP` 默认值；它记录的是服务器求值时间，需核对会话时区及列定义。

- TIMESTAMP是UTC时间戳，与时区相关。

- `DATETIME` 表示不随会话时区自动转换的日期时间值；不要把其内部存储等同于 `YYYYMMDD HH:MM:SS` 整数。跨时区业务应明确写入约定。

- `TIMESTAMP` 的可表示范围较窄且按时区转换，`DATETIME` 范围更广且不自动转换；取舍应由时间语义、范围及迁移需求决定，而不是固定偏好。

- Unix 时间戳存为整数便于跨系统交换与数值计算，但会失去部分内建日期类型的可读性和函数便利；要统一秒/毫秒单位、时区显示规则与有效范围。

### 3、字符串

| 类型 | 容量与语义 | 建模要点 |
| --- | --- | --- |
| CHAR | 定长，长度按字符定义 | 适合长度稳定的短文本 |
| VARCHAR | 变长，受行大小和字符集约束 | 适合长度变化较大的文本 |
| TINYTEXT / TINYBLOB | 最多 255 字节 | TEXT 受字符集影响，BLOB 存二进制 |
| TEXT / BLOB | 最多 65535 字节 | 大字段读取与索引设计需单独评估 |
| MEDIUMTEXT / MEDIUMBLOB | 最多 16777215 字节 | 关注行外存储和 I/O |
| LONGTEXT / LONGBLOB | 理论上限约 4 GiB | 实际还受包大小和资源限制 |

#### 优化建议

- 字符串的长度相差较大用VARCHAR；字符串短，且所有值都接近一个长度用CHAR。

- CHAR和VARCHAR适用于包括人名、邮政编码、电话号码和不超过255个字符长度的任意字母数字组合。那些要用来计算的数字不要用VARCHAR类型保存，因为可能会导致一些与计算相关的问题。换句话说，可能影响到计算的准确性和完整性。

- 尽量少用BLOB和TEXT，如果实在要用可以考虑将BLOB和TEXT字段单独存一张表，用id关联。

- BLOB系列存储二进制字符串，与字符集无关。TEXT系列存储非二进制字符串，与字符集相关。

- BLOB/TEXT 的默认值能力随版本和表达式语法变化；设计时先核对目标版本与迁移工具支持。

### PS：INT显示宽度

旧版整数显示宽度影响部分展示行为，不影响数值范围；MySQL 8.0 中不应把它当作建模参数。

```sql
CREATE TABLE `user`(
    `id` TINYINT(2) UNSIGNED
);
```

TINYINT UNSIGNED 的数值范围是 0—255，显示宽度不改变范围。写入 500 在严格 SQL 模式下会报错；不要假设自动截断。

ZEROFILL 仅改变旧版本的显示填充，并隐含 UNSIGNED；MySQL 8.0 已弃用该机制，格式化应放在应用层。

```sql
`id` TINYINT(2) UNSIGNED ZEROFILL
```

显示为 05 或 00005 不改变实际存储数值，但不要为新系统依赖 ZEROFILL。

整数类型的可存范围由 TINYINT、INT 等类型及有无符号决定，与括号中的旧式显示宽度无关。

## 实例参数与资源预算

补充一点配置文件my.ini或my.cnf的全局参数：

以下以 32 核、64 GiB 内存、SSD 实例为预算示例；参数值不是直接可套用的生产推荐。

- CPU：32核

- 内存：64G

- DISK：2T SSD

下面参数都是服务端参数，默认在配置文件的 [mysqld] 标签下

```ini
max_connections=3000
```

连接的创建和销毁消耗内存、线程和文件描述符。并发数表示同一时刻在处理的请求或连接数，QPS 表示每秒查询数；两者有关联但不是同一个指标，还要同时看请求耗时与连接池使用率。

连接内存不是固定的最小/最大两档；排序、连接、网络缓冲等按需分配。应以峰值连接数和每连接实际内存估算总预算。

3000 个连接的理论上限不能简单按 256 KiB 或 64 MiB 相乘；需要考虑活动连接比例、每连接缓冲、线程栈及操作系统余量。

buffer pool、连接与系统缓存共享内存预算。若总内存承诺超过可用内存，可能触发交换和延迟抖动；先从连接池与负载观测入手。

```ini
max_user_connections=2980
```

`max_user_connections` 限制的是单个账号允许的并发连接数，不会从 `max_connections` 中自动预留管理连接。若要保障故障时的管理入口，应另外评估管理员权限、额外连接及运维通道。

```ini
back_log=300
```

back_log 控制等待建立连接的请求队列上限，实际队列还受操作系统参数和流量突发影响；它不是已建立连接的等待队列。

```ini
wait_timeout=300
```

wait_timeout 影响非交互式空闲连接的关闭时间；与连接池保活策略配合设置，默认值以实例为准。

```ini
interactive_timeout=300
```

interactive_timeout 影响交互式客户端会话；具体生效值应查看当前实例与会话。

```ini
innodb_thread_concurrency=64
```

innodb_thread_concurrency 默认常为 0（不限制）；不应按 CPU 核数机械设置，只有确认 InnoDB 内部并发控制是瓶颈时才试验。

```ini
innodb_buffer_pool_size=40G
```

innodb_buffer_pool_size 应结合专用/混部、工作集、操作系统页缓存及其他内存开销确定，不套固定 60%—70% 比例。

```ini
innodb_lock_wait_timeout=10
```

innodb_lock_wait_timeout 设定锁等待超时；过低会增加失败重试，过高会延长请求尾延迟，应配合事务与死锁排查。

```ini
innodb_flush_log_at_trx_commit=1
```

该配置应与 binlog 刷盘策略、故障恢复目标一起评估。

```ini
sync_binlog=1
```

该配置应与 redo 刷盘策略和复制一致性一起评估。

```ini
sort_buffer_size=4M
```

sort_buffer_size 控制单次排序的内存预算；增加它不保证 ORDER BY 或 GROUP BY 更快，应先检查索引、排序行数与临时文件。

`sort_buffer_size` 是会话级设置，排序操作需要时才使用相关缓冲；实际分配方式与版本、排序路径有关，不应假定每条连接建立时或第一次排序时都一次性占满配置值。

sort_buffer_size 按需要分配，不能简单以所有连接数乘该值作为实占内存；但高并发排序可能显著推高峰值。

```ini
join_buffer_size=4M
```

join_buffer_size 属于连接执行的内存预算之一，其使用和分配取决于查询计划；应先考虑关联列索引。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/22-instance-observability.html' | relative_url }}">← 上一篇：实例级观测与调优顺序</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/24-mysql-8-features.html' | relative_url }}">下一篇：MySQL 8.0 中与调优相关的能力 →</a>
</nav>
