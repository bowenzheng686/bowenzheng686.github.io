---
layout: default
title: "MySQL 性能调优 · MySQL 8.0 中与调优相关的能力"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 24 MySQL 8.0 中与调优相关的能力

## 新特性只在合适场景有收益

8.0 提供 `EXPLAIN ANALYZE`、降序索引、不可见索引、直方图、窗口函数、CTE、原子 DDL 等能力；具体起始小版本和限制需按部署版本核对。窗口函数和 CTE 可提升表达能力与可读性，但未必比原查询快，仍需比较计划与中间结果。不可见索引用于评估移除风险，不能代替完整的查询回归。

```sql
SELECT VERSION();
EXPLAIN ANALYZE SELECT * FROM employees WHERE name = 'LiLei';
CREATE INDEX idx_hire_desc_id ON employees(hire_time DESC, id DESC);
ALTER TABLE employees ALTER INDEX idx_hire_desc_id INVISIBLE;
-- 验证后可改回 VISIBLE；不要在尚有依赖时直接删除。
```

MySQL 5.7 的 query cache 配置在 8.0 已不适用；同样，8.0.20 起无索引关联不能继续笼统解释为 Block Nested Loop。评估新能力时，应核对目标版本并做实验。[官方参考：MySQL 8.0 新特性](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html)。



## MySQL 8.0 功能逐项解析

### Mysql 8.0新特性详解

MySQL 8.0 的小版本差异很大；部署前应选定仍受维护的目标版本并逐项验证功能与默认值。

1、新增降序索引

MySQL 5.7 虽接受索引列上的 `DESC` 语法，却未真正保存降序键；8.0 的 InnoDB 可创建降序索引。下列终端输出展示的是两个历史版本的对比，实际优化器选择仍取决于数据与查询条件。

```text
# ====MySQL 5.7演示====
mysql> create table t1(c1 int,c2 int,index idx_c1_c2(c1,c2 desc));
Query OK, 0 rows affected (0.04 sec)

mysql> insert into t1 (c1,c2) values(1, 10),(2,50),(3,50),(4,100),(5,80);
Query OK, 5 rows affected (0.02 sec)

mysql> show create table t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `c1` int(11) DEFAULT NULL,
  `c2` int(11) DEFAULT NULL,
  KEY `idx_c1_c2` (`c1`,`c2`)    --注意这里，c2字段是升序
) ENGINE=InnoDB DEFAULT CHARSET=latin1
1 row in set (0.00 sec)

mysql> explain select * from t1 order by c1,c2 desc;  --5.7也会使用索引，但是Extra字段里有filesort文件排序
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra                       |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |   100.00 | Using index; Using filesort |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
1 row in set, 1 warning (0.01 sec)


# ====MySQL 8.0演示====
mysql> create table t1(c1 int,c2 int,index idx_c1_c2(c1,c2 desc));
Query OK, 0 rows affected (0.02 sec)

mysql> insert into t1 (c1,c2) values(1, 10),(2,50),(3,50),(4,100),(5,80);
Query OK, 5 rows affected (0.02 sec)

mysql> show create table t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `c1` int DEFAULT NULL,
  `c2` int DEFAULT NULL,
  KEY `idx_c1_c2` (`c1`,`c2` DESC)  --注意这里的区别，降序索引生效了
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
1 row in set (0.00 sec)

mysql> explain select * from t1 order by c1,c2 desc;  --Extra字段里没有filesort文件排序，充分利用了降序索引
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |   100.00 | Using index |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)

mysql> explain select * from t1 order by c1 desc,c2;  --Extra字段里有Backward index scan，意思是反向扫描索引;
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+----------------------------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra                            |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+----------------------------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |   100.00 | Backward index scan; Using index |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+----------------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> explain select * from t1 order by c1 desc,c2 desc;  --Extra字段里有filesort文件排序，排序必须按照每个字段定义的排序或按相反顺序才能充分利用索引
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra                       |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |   100.00 | Using index; Using filesort |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> explain select * from t1 order by c1,c2;    --Extra字段里有filesort文件排序，排序必须按照每个字段定义的排序或按相反顺序才能充分利用索引
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra                       |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_c1_c2 | 10      | NULL |    1 |   100.00 | Using index; Using filesort |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-----------------------------+
1 row in set, 1 warning (0.00 sec)
```

2、GROUP BY 不承诺隐式排序

MySQL 8.0 的 GROUP BY 不保证隐式排序；若需要稳定顺序，应显式写 ORDER BY。

```text
# ====MySQL 5.7演示====
mysql> select count(*),c2 from t1 group by c2;
+----------+------+
| count(*) | c2   |
+----------+------+
|        1 |   10 |
|        2 |   50 |
|        1 |   80 |
|        1 |  100 |
+----------+------+
4 rows in set (0.00 sec)


# ====MySQL 8.0演示====
mysql> select count(*),c2 from t1 group by c2;   --8.0版本group by不再默认排序
+----------+------+
| count(*) | c2   |
+----------+------+
|        1 |   10 |
|        2 |   50 |
|        1 |  100 |
|        1 |   80 |
+----------+------+
4 rows in set (0.00 sec)

mysql> select count(*),c2 from t1 group by c2 order by c2;  --8.0版本group by不再默认排序，需要自己加order by
+----------+------+
| count(*) | c2   |
+----------+------+
|        1 |   10 |
|        2 |   50 |
|        1 |   80 |
|        1 |  100 |
+----------+------+
4 rows in set (0.00 sec)
```

3、增加隐藏索引

不可见索引仍由存储引擎维护，默认不被优化器选用；需要测试时可在受控会话启用 use_invisible_indexes，再核对计划。

把待删除索引先设为不可见，可观察查询回退与写入成本；确认没有依赖后再删除，不能把它理解为零成本的“软删除”。

```text
# 创建t2表，里面的c2字段为隐藏索引
mysql> create table t2(c1 int, c2 int, index idx_c1(c1), index idx_c2(c2) invisible);
Query OK, 0 rows affected (0.02 sec)

mysql> show index from t2\G
*************************** 1. row ***************************
        Table: t2
   Non_unique: 1
     Key_name: idx_c1
 Seq_in_index: 1
  Column_name: c1
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: YES
   Index_type: BTREE
      Comment:
Index_comment:
      Visible: YES
   Expression: NULL
*************************** 2. row ***************************
        Table: t2
   Non_unique: 1
     Key_name: idx_c2
 Seq_in_index: 1
  Column_name: c2
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: YES
   Index_type: BTREE
      Comment:
Index_comment:
      Visible: NO   --隐藏索引不可见
   Expression: NULL
2 rows in set (0.00 sec)

mysql> explain select * from t2 where c1=1;
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key    | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | t2    | NULL       | ref  | idx_c1        | idx_c1 | 5       | const |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)

mysql> explain select * from t2 where c2=1;  --隐藏索引c2不会被使用
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | t2    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)

mysql> select @@optimizer_switch\G   --查看各种参数
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on
1 row in set (0.00 sec)

mysql> set session optimizer_switch="use_invisible_indexes=on";  ----在会话级别设置查询优化器可以看到隐藏索引
Query OK, 0 rows affected (0.00 sec)

mysql> select @@optimizer_switch\G
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=on,skip_scan=on,hash_join=on
1 row in set (0.00 sec)

mysql> explain select * from t2 where c2=1;
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key    | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | t2    | NULL       | ref  | idx_c2        | idx_c2 | 5       | const |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)

mysql> alter table t2 alter index idx_c2 visible;
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> alter table t2 alter index idx_c2 invisible;
Query OK, 0 rows affected (0.01 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

4、新增函数索引

MySQL 8.0.13 起支持函数索引；它让特定表达式谓词有机会利用索引，但表达式、字符集和查询写法需匹配。

函数索引基于隐藏生成列实现；它同样占空间并增加写入维护成本。

```text
mysql> create table t3(c1 varchar(10),c2 varchar(10));
Query OK, 0 rows affected (0.02 sec)

mysql> create index idx_c1 on t3(c1);     --创建普通索引
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> create index func_idx on t3((UPPER(c2)));  --创建一个大写的函数索引
Query OK, 0 rows affected (0.03 sec)
Records: 0  Duplicates: 0  Warnings: 0

mysql> show index from t3\G
*************************** 1. row ***************************
        Table: t3
   Non_unique: 1
     Key_name: idx_c1
 Seq_in_index: 1
  Column_name: c1
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: YES
   Index_type: BTREE
      Comment:
Index_comment:
      Visible: YES
   Expression: NULL
*************************** 2. row ***************************
        Table: t3
   Non_unique: 1
     Key_name: func_idx
 Seq_in_index: 1
  Column_name: NULL
    Collation: A
  Cardinality: 0
     Sub_part: NULL
       Packed: NULL
         Null: YES
   Index_type: BTREE
      Comment:
Index_comment:
      Visible: YES
   Expression: upper(`c2`)    --函数表达式
2 rows in set (0.00 sec)

mysql> explain select * from t3 where upper(c1)='ZHUGE';
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | t3    | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    1 |   100.00 | Using where |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-------------+
1 row in set, 1 warning (0.00 sec)

mysql> explain select * from t3 where upper(c2)='ZHUGE';  --使用了函数索引
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------+
| id | select_type | table | partitions | type | possible_keys | key      | key_len | ref   | rows | filtered | Extra |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | t3    | NULL       | ref  | func_idx      | func_idx | 43      | const |    1 |   100.00 | NULL  |
+----+-------------+-------+------------+------+---------------+----------+---------+-------+------+----------+-------+
1 row in set, 1 warning (0.00 sec)
```

5、innodb存储引擎select for update跳过锁等待

FOR SHARE / FOR UPDATE 可配合 NOWAIT 或 SKIP LOCKED 控制锁等待；SKIP LOCKED 会改变结果集，适合队列等允许跳过当前锁定行的场景。

在旧版 MySQL 中，普通 `SELECT ... FOR UPDATE` 遇到冲突锁会等待，直到锁释放或达到 `innodb_lock_wait_timeout`；8.0 提供 `NOWAIT` 与 `SKIP LOCKED` 两种额外语义。

NOWAIT 遇到需等待的行锁时立即报错；SKIP LOCKED 则排除当前被锁的行。两者不能代替业务正确性判断。

库存或任务领取场景可评估 SKIP LOCKED，但必须设计重试、去重与顺序语义，不能把跳过行误认为不存在。

```text
# 先打开一个session1:
mysql> select * from t1;
+------+------+
| c1   | c2   |
+------+------+
|    1 |   10 |
|    2 |   50 |
|    3 |   50 |
|    4 |  100 |
|    5 |   80 |
+------+------+
5 rows in set (0.00 sec)

mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> update t1 set c2 = 60 where c1 = 2;     --锁定第二条记录
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0


# 另外一个session2:
mysql> select * from t1 where c1 = 2 for update;   --等待超时
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction

mysql> select * from t1 where c1 = 2 for update nowait;   --查询立即返回
ERROR 3572 (HY000): Statement aborted because lock(s) could not be acquired immediately and NOWAIT is set.

mysql> select * from t1 for update skip locked;  --查询立即返回，过滤掉了第二行记录
+------+------+
| c1   | c2   |
+------+------+
|    1 |   10 |
|    3 |   50 |
|    4 |  100 |
|    5 |   80 |
+------+------+
4 rows in set (0.00 sec)
```

6、新增innodb_dedicated_server自适应参数

innodb_dedicated_server 可自动设置部分 InnoDB 资源参数，适合专用实例试验；混部环境或显式配置覆盖时应慎用，并核对版本行为。

```text
mysql> show variables like '%innodb_dedicated_server%';   --默认是OFF关闭，修改为ON打开
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| innodb_dedicated_server | OFF   |
+-------------------------+-------+
1 row in set (0.02 sec)
```

7、死锁检查控制

关闭 innodb_deadlock_detect 可能降低热点锁检测开销，但会改变等待与超时行为；必须先确认瓶颈并有监控及回滚方案。

```text
mysql> show variables like '%innodb_deadlock_detect%';  --默认是打开的
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| innodb_deadlock_detect | ON    |
+------------------------+-------+
1 row in set, 1 warning (0.01 sec)
```

8、undo文件不再使用系统表空间

MySQL 8.0 默认使用独立 undo 表空间；具体数量、位置与截断行为应以实例版本为准。

![MySQL 8.0 中与调优相关的能力配图](assets/global-8-002-c9492c54275c.webp)

9、 binlog日志过期时间精确到秒

MySQL 8.0 使用 binlog_expire_logs_seconds 配置保留时长；设置前核对备份、复制延迟与恢复点目标。

10、窗口函数(Window Functions)：也称分析函数

从 MySQL 8.0 开始，新增了一个叫窗口函数的概念，它可以用来实现若干新的查询方式。窗口函数与 SUM()、COUNT() 这种分组聚合函数类似，在聚合函数后面加上over()就变成窗口函数了，在括号里可以加上partition by等分组关键字指定如何分组，窗口函数即便分组也不会将多行查询结果合并为一行，而是将结果放回多行当中，即窗口函数不需要再使用 GROUP BY。

```text
# 创建一张账户余额表
CREATE TABLE `account_channel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '姓名',
  `channel` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '账户渠道',
  `balance` int DEFAULT NULL COMMENT '余额',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB

# 插入一些示例数据
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('1', 'zhuge', 'wx', '100');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('2', 'zhuge', 'alipay', '200');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('3', 'zhuge', 'yinhang', '300');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('4', 'lilei', 'wx', '200');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('5', 'lilei', 'alipay', '100');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('6', 'hanmeimei', 'wx', '500');
INSERT INTO `test`.`account_channel` (`id`, `name`, `channel`, `balance`) VALUES ('6', 'hanmeimei', 'wx', '500');

mysql> select * from account_channel;
+----+-----------+---------+---------+
| id | name      | channel | balance |
+----+-----------+---------+---------+
|  1 | zhuge     | wx      |     100 |
|  2 | zhuge     | alipay  |     200 |
|  3 | zhuge     | yinhang |     300 |
|  4 | lilei     | wx      |     200 |
|  5 | lilei     | alipay  |     100 |
|  6 | hanmeimei | wx      |     500 |
+----+-----------+---------+---------+
6 rows in set (0.00 sec)

mysql> select name,sum(balance) from account_channel group by name;
+-----------+--------------+
| name      | sum(balance) |
+-----------+--------------+
| zhuge     |          600 |
| lilei     |          300 |
| hanmeimei |          500 |
+-----------+--------------+
3 rows in set (0.00 sec)

# 在聚合函数后面加上over()就变成分析函数了，后面可以不用再加group by制定分组，因为在over里已经用partition关键字指明了如何分组计算，这种可以保留原有表数据的结构，不会像分组聚合函数那样每组只返回一条数据
mysql> select name,channel,balance,sum(balance) over(partition by name) as sum_balance from account_channel;
+-----------+---------+---------+-------------+
| name      | channel | balance | sum_balance |
+-----------+---------+---------+-------------+
| hanmeimei | wx      |     500 |         500 |
| lilei     | wx      |     200 |         300 |
| lilei     | alipay  |     100 |         300 |
| zhuge     | wx      |     100 |         600 |
| zhuge     | alipay  |     200 |         600 |
| zhuge     | yinhang |     300 |         600 |
+-----------+---------+---------+-------------+
6 rows in set (0.00 sec)

mysql> select name,channel,balance,sum(balance) over(partition by name order by balance) as sum_balance from account_channel;
+-----------+---------+---------+-------------+
| name      | channel | balance | sum_balance |
+-----------+---------+---------+-------------+
| hanmeimei | wx      |     500 |         500 |
| lilei     | alipay  |     100 |         100 |
| lilei     | wx      |     200 |         300 |
| zhuge     | wx      |     100 |         100 |
| zhuge     | alipay  |     200 |         300 |
| zhuge     | yinhang |     300 |         600 |
+-----------+---------+---------+-------------+
6 rows in set (0.00 sec)


# over()里如果不加条件，则默认使用整个表的数据做运算
mysql> select name,channel,balance,sum(balance) over() as sum_balance from account_channel;
+-----------+---------+---------+-------------+
| name      | channel | balance | sum_balance |
+-----------+---------+---------+-------------+
| zhuge     | wx      |     100 |        1400 |
| zhuge     | alipay  |     200 |        1400 |
| zhuge     | yinhang |     300 |        1400 |
| lilei     | wx      |     200 |        1400 |
| lilei     | alipay  |     100 |        1400 |
| hanmeimei | wx      |     500 |        1400 |
+-----------+---------+---------+-------------+
6 rows in set (0.00 sec)

mysql> select name,channel,balance,avg(balance) over(partition by name) as avg_balance from account_channel;
+-----------+---------+---------+-------------+
| name      | channel | balance | avg_balance |
+-----------+---------+---------+-------------+
| hanmeimei | wx      |     500 |    500.0000 |
| lilei     | wx      |     200 |    150.0000 |
| lilei     | alipay  |     100 |    150.0000 |
| zhuge     | wx      |     100 |    200.0000 |
| zhuge     | alipay  |     200 |    200.0000 |
| zhuge     | yinhang |     300 |    200.0000 |
+-----------+---------+---------+-------------+
6 rows in set (0.00 sec)
```

专用窗口函数：

- 序号函数：ROW_NUMBER()、RANK()、DENSE_RANK()

- 分布函数：PERCENT_RANK()、CUME_DIST()

- 前后函数：LAG()、LEAD()

- 头尾函数：FIRST_VALUE()、LAST_VALUE()

- 其它函数：NTH_VALUE()、NTILE()

```text
# 按 balance 排序展示序号；相同 balance 的行若需稳定次序，应追加 id 作为排序键。
mysql> select name,channel,balance,row_number() over(order by balance) as row_number1 from account_channel;
+-----------+---------+---------+-------------+
| name      | channel | balance | row_number1 |
+-----------+---------+---------+-------------+
| zhuge     | wx      |     100 |           1 |
| lilei     | alipay  |     100 |           2 |
| zhuge     | alipay  |     200 |           3 |
| lilei     | wx      |     200 |           4 |
| zhuge     | yinhang |     300 |           5 |
| hanmeimei | wx      |     500 |           6 |
+-----------+---------+---------+-------------+
6 rows in set (0.00 sec)

# 按照balance字段排序，first_value()选出排第一的余额
mysql> select name,channel,balance,first_value(balance) over(order by balance) as first1 from account_channel;
+-----------+---------+---------+--------+
| name      | channel | balance | first1 |
+-----------+---------+---------+--------+
| zhuge     | wx      |     100 |    100 |
| lilei     | alipay  |     100 |    100 |
| zhuge     | alipay  |     200 |    100 |
| lilei     | wx      |     200 |    100 |
| zhuge     | yinhang |     300 |    100 |
| hanmeimei | wx      |     500 |    100 |
+-----------+---------+---------+--------+
6 rows in set (0.01 sec)
```

12、默认字符集由latin1变为utf8mb4

MySQL 8.0 默认字符集为 utf8mb4；但 utf8 别名在 8.0 中仍可能指向 utf8mb3，建库建表应明确写 utf8mb4。

13、事务性数据字典与系统表调整

MySQL 8.0 将数据字典改为事务性存储，系统表与存储引擎布局也随版本变化；不要假定所有历史 MyISAM 用法都自动等价。

14、元数据存储变动

MySQL 8.0 取消旧版 .frm 元数据文件，采用事务性数据字典；实际目录文件布局受表空间配置与版本影响。

![MySQL 8.0 中与调优相关的能力配图](assets/global-8-003-389a489e02d6.webp)

![MySQL 8.0 中与调优相关的能力配图](assets/global-8-004-cb9ea264fe28.webp)

15、自增变量持久化

旧版 InnoDB 的自增计数器主要由内存维护，正常重启后可能按表中最大值重新初始化；8.0 将计数器变化持久化，通常可避免单纯重启导致的回退。自增值仍不保证连续，回滚、批量插入和故障时机都可能留下缺口，不能把它用作业务流水号的连续性承诺。

```text
# ====MySQL 5.7演示====
mysql> create table t(id int auto_increment primary key,c1 varchar(20));
Query OK, 0 rows affected (0.03 sec)

mysql> insert into t(c1) values('zhuge1'),('zhuge2'),('zhuge3');
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
|  3 | zhuge3 |
+----+--------+
3 rows in set (0.00 sec)

mysql> delete from t where id = 3;
Query OK, 1 row affected (0.01 sec)

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
+----+--------+
2 rows in set (0.00 sec)

mysql> exit;
Bye

# 重启MySQL服务，并重新连接MySQL
mysql> insert into t(c1) values('zhuge4');
Query OK, 1 row affected (0.01 sec)

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
|  3 | zhuge4 |
+----+--------+
3 rows in set (0.00 sec)

mysql> update t set id = 5 where c1 = 'zhuge1';
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  2 | zhuge2 |
|  3 | zhuge4 |
|  5 | zhuge1 |
+----+--------+
3 rows in set (0.00 sec)

mysql> insert into t(c1) values('zhuge5');
Query OK, 1 row affected (0.01 sec)

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  2 | zhuge2 |
|  3 | zhuge4 |
|  4 | zhuge5 |
|  5 | zhuge1 |
+----+--------+
4 rows in set (0.00 sec)

mysql> insert into t(c1) values('zhuge6');
ERROR 1062 (23000): Duplicate entry '5' for key 'PRIMARY'



# ====MySQL 8.0演示====
mysql> create table t(id int auto_increment primary key,c1 varchar(20));
Query OK, 0 rows affected (0.02 sec)

mysql> insert into t(c1) values('zhuge1'),('zhuge2'),('zhuge3');
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
|  3 | zhuge3 |
+----+--------+
3 rows in set (0.00 sec)

mysql> delete from t where id = 3;
Query OK, 1 row affected (0.01 sec)

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
+----+--------+
2 rows in set (0.00 sec)

mysql> exit;
Bye
[root@localhost ~]# service mysqld restart
Shutting down MySQL.... SUCCESS!
Starting MySQL... SUCCESS!

# 重新连接MySQL
mysql> insert into t(c1) values('zhuge4');
Query OK, 1 row affected (0.00 sec)

mysql> select * from t;  --生成的id为4，不是3
+----+--------+
| id | c1     |
+----+--------+
|  1 | zhuge1 |
|  2 | zhuge2 |
|  4 | zhuge4 |
+----+--------+
3 rows in set (0.00 sec)

mysql> update t set id = 5 where c1 = 'zhuge1';
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  2 | zhuge2 |
|  4 | zhuge4 |
|  5 | zhuge1 |
+----+--------+
3 rows in set (0.00 sec)

mysql> insert into t(c1) values('zhuge5');
Query OK, 1 row affected (0.00 sec)

mysql> select * from t;
+----+--------+
| id | c1     |
+----+--------+
|  2 | zhuge2 |
|  4 | zhuge4 |
|  5 | zhuge1 |
|  6 | zhuge5 |
+----+--------+
4 rows in set (0.00 sec)
```

16、DDL原子化

原子 DDL 指单条受支持 DDL 在崩溃后要么完成要么回退，不表示用户可以用 ROLLBACK 撤销已成功执行的 DDL。

MySQL 8.0 的原子 DDL 协调数据字典、存储引擎操作与 binlog；支持范围依语句与存储引擎而定。

```text
# MySQL 5.7
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| account        |
| actor          |
| employee       |
| film           |
| film_actor     |
| leaf_id        |
| t1             |
| test_innodb    |
| test_myisam    |
| test_order_id  |
+----------------+
10 rows in set (0.01 sec)

mysql> drop table t1,t2;  //删除表报错不会回滚，t1表会被删除
ERROR 1051 (42S02): Unknown table 'test.t2'
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| account        |
| actor          |
| employee       |
| film           |
| film_actor     |
| leaf_id        |
| test_innodb    |
| test_myisam    |
| test_order_id  |
+----------------+
9 rows in set (0.00 sec)


# MySQL 8.0
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| account        |
| actor          |
| employee       |
| film           |
| film_actor     |
| leaf_id        |
| t1             |
| test_innodb    |
| test_myisam    |
| test_order_id  |
+----------------+
10 rows in set (0.00 sec)

mysql> drop table t1,t2;  //删除表报错会回滚，t1表依然还在
ERROR 1051 (42S02): Unknown table 'test.t2'
mysql> show tables;
+----------------+
| Tables_in_test |
+----------------+
| account        |
| actor          |
| employee       |
| film           |
| film_actor     |
| leaf_id        |
| t1             |
| test_innodb    |
| test_myisam    |
| test_order_id  |
+----------------+
10 rows in set (0.00 sec)
```

17、参数修改持久化

SET PERSIST 可将受支持的动态全局变量变更写入 mysqld-auto.cnf；需核对权限、生效范围、重启行为和配置优先级。

```sql
SET PERSIST innodb_lock_wait_timeout = 25;
```

服务器会在数据目录的 `mysqld-auto.cnf` 保存持久化变量。下面是便于阅读的 JSON 结构示意；实际内容、权限和配置优先级应以当前版本为准，回滚可用 `RESET PERSIST innodb_lock_wait_timeout` 并恢复运行值。

```json
{
	"Version": 1,
	"mysql_server": {
		"innodb_lock_wait_timeout": {
			"Value": "25",
			"Metadata": {
				"Timestamp": 1675290252103863,
				"User": "root",
				"Host": "localhost"
			}
		}
	}
}
```



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/23-configuration-tradeoffs.html' | relative_url }}">← 上一篇：字段类型与资源预算</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/25-end-to-end-case.html' | relative_url }}">下一篇：端到端案例、验收与回滚 →</a>
</nav>
