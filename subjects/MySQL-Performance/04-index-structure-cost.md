---
layout: default
title: "MySQL 性能调优 · 索引结构与访问成本"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 04 索引结构与访问成本

## 从 B+ 树到回表

InnoDB 聚簇索引的叶页承载行记录；二级索引的叶页记录索引列及主键值。用二级索引检索未覆盖的列，通常还要按主键回到聚簇索引，这就是回表。索引覆盖所需列时可以避免相应回表，但更宽的索引增加存储、写入、页分裂和缓存压力。

```sql
-- 同一过滤条件，比较是否需要取回整行
EXPLAIN SELECT * FROM employees WHERE name > 'LiLei';
EXPLAIN SELECT name, age, position FROM employees WHERE name > 'LiLei';
```

覆盖索引案例说明：是否采用索引取决于成本，投影列变化可能改变计划；不保证覆盖索引在每个数据集上都更快。低基数字段也不是“一律不建索引”：它可与其他条件或排序组合，或成为高频查询的一部分。设计时以真实查询、选择性、写入比例和维护成本共同决定。[官方参考：InnoDB 索引类型](https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html)。

对照计划：强制索引时可能出现 `Using index condition`；仅取索引覆盖的列时出现 `Using index`。两图反映特定数据与版本下的执行计划，不代表所有实例的固定结果。



## 示例表、范围扫描与覆盖索引

### 示例表

```sql
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) NOT NULL DEFAULT '' COMMENT '姓名',
  `age` int(11) NOT NULL DEFAULT '0' COMMENT '年龄',
  `position` varchar(20) NOT NULL DEFAULT '' COMMENT '职位',
  `hire_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间',
  PRIMARY KEY (`id`),
  KEY `idx_name_age_position` (`name`,`age`,`position`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='员工记录表';

INSERT INTO employees(name,age,position,hire_time) VALUES('LiLei',22,'manager',NOW());
INSERT INTO employees(name,age,position,hire_time) VALUES('HanMeimei', 23,'dev',NOW());
INSERT INTO employees(name,age,position,hire_time) VALUES('Lucy',23,'dev',NOW());

-- 插入一些示例数据
drop procedure if exists insert_emp;
delimiter ;;
create procedure insert_emp()
begin
  declare i int;
  set i=1;
  while(i<=100000)do
    insert into employees(name,age,position) values(CONCAT('zhuge',i),i,'dev');
    set i=i+1;
  end while;
end;;
delimiter ;
call insert_emp();
```

### 举一个大家不容易理解的综合例子：

1、联合索引首列使用范围条件时，优化器可能选择索引范围扫描，也可能选择全表扫描。

```sql
EXPLAIN SELECT * FROM employees WHERE name > 'LiLei' AND age = 22 AND position ='manager';
```

![索引结构与访问成本配图](assets/index-1-001-c619f9d36f14.webp)

结论：这次执行计划选了全表扫描，原因是符合范围条件的行较多，二级索引回表成本可能高于顺序扫描；不能推广为“首列范围查询不走索引”。

2、强制走索引

```sql
EXPLAIN SELECT * FROM employees force index(idx_name_age_position) WHERE name > 'LiLei' AND age = 22 AND position ='manager';
```

![索引结构与访问成本配图](assets/index-1-002-e746417dbdcb.webp)

结论：虽然使用了强制走索引让联合索引第一个字段范围查找也走索引，扫描的行rows看上去也少了点，但是最终查找效率不一定比全表扫描高，因为回表效率不高

做了一个小实验：

```sql
SELECT * FROM employees WHERE name > 'LiLei';
SELECT * FROM employees FORCE INDEX (idx_name_age_position) WHERE name > 'LiLei';
-- 在同一数据集上分别运行 EXPLAIN ANALYZE，比较实际耗时与读取行数；旧版查询缓存参数不适用于 MySQL 8.0。
```

### 3、覆盖索引优化

```sql
EXPLAIN SELECT name,age,position FROM employees WHERE name > 'LiLei' AND age = 22 AND position ='manager';
```

![索引结构与访问成本配图](assets/index-1-003-a4d707431671.webp)



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/03-plan-validation.html' | relative_url }}">← 上一篇：执行计划验证与优化器判断</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/05-composite-index.html' | relative_url }}">下一篇：联合索引设计与最左前缀 →</a>
</nav>
