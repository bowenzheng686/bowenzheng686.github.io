---
layout: default
title: "MySQL 性能调优 · 联合索引设计与最左前缀"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 05 联合索引设计与最左前缀

## 用查询形态决定列顺序

联合索引 `(name, age, position)` 可支持从 `name` 开始的查找；等值列后接范围列时，后续列通常难以继续缩小连续扫描区间，但仍可能用于覆盖或索引条件下推。排序能否利用索引要单独核对计划。不能把“范围后面的列完全没有作用”写成绝对规则，也不能为了凑最左前缀而注入无意义的 `IN` 条件。

```sql
EXPLAIN SELECT id FROM employees
WHERE name = 'LiLei' AND age = 22;
EXPLAIN SELECT id FROM employees
WHERE name LIKE 'Li%' AND age = 22 AND position = 'manager';
```

优先盘点高频 SQL，再评估等值过滤、范围、`ORDER BY`、返回列与更新成本。例如，社交搜索中 `(province, city, sex, age)` 与 `(sex, score)` 服务不同查询路径；是否保留两个索引要看查询比例和写入代价。为“最近七天活跃”增设派生布尔列会引入持续维护和时间边界问题，不能只凭索引命中率决定。对于长字符串前缀索引，还要验证区分度，且完整排序通常不能仅靠截断前缀完成。[官方参考：多列索引](https://dev.mysql.com/doc/refman/8.0/en/multiple-column-indexes.html)。



## 索引设计原则与组合索引案例

### 索引设计原则

1、先盘点高频 SQL，再确定索引

不知大家一般是怎么给数据表建立索引的，是建完表马上就建立索引吗？

表建成时可先保证主键、唯一约束等正确性索引；业务查询稳定后，再依据实际 WHERE、JOIN、ORDER BY 与写入负载补充或调整性能索引。

2、联合索引尽量覆盖条件

比如可以设计一个或者两三个联合索引(尽量少建单值索引)，让每一个联合索引都尽量去包含sql语句里的where、order by、group by的字段，还要确保这些联合索引的字段顺序尽量满足sql查询的最左前缀原则。

3、低基数字段不能单独决定索引是否有用

索引基数是指这个字段在表里总共有多少个不同的值，比如一张表总共100万行记录，其中有个性别字段，其值不是男就是女，那么该字段的基数就是2。

低基数字段单独过滤时可能选择性不足，但它在联合索引中仍可能服务其他等值条件、排序或覆盖查询；不能一律排除。

索引选择还要考虑数据倾斜、组合选择性、查询频率、回表与写入维护成本。

4、长字符串我们可以采用前缀索引

尽量对字段类型较小的列设计索引，比如说什么tinyint之类的，因为字段类型较小的话，占用磁盘空间也会比较小，此时你在搜索的时候性能也会比较好一点。

当然，这个所谓的字段类型小一点的列，也不是绝对的，很多时候你就是要针对varchar(255)这种字段建立索引，哪怕多占用一些磁盘空间也是有必要的。

对于这种varchar(255)的大字段可能会比较占用磁盘空间，可以稍微优化下，比如针对这个字段的前20个字符建立索引，就是说，对这个字段里的每个值的前20个字符放在索引树里，类似于 KEY index(name(20),age,position)。

此时你在where条件里搜索的时候，如果是根据name字段来搜索，那么此时就会先到索引树里根据name字段的前20个字符去搜索，定位到之后前20个字符的前缀匹配的部分数据之后，再回到聚簇索引提取出来完整的name字段值进行比对。

但是假如你要是order by name，那么此时你的name因为在索引树里仅仅包含了前20个字符，所以这个排序是没法用上索引的， group by也是同理。所以这里大家要对前缀索引有一个了解。

5、where与order by冲突时优先where

在where和order by出现索引设计冲突时，到底是针对where去设计索引，还是针对order by设计索引？到底是让where去用上索引，还是让order by用上索引?

一般这种时候往往都是让where条件去使用索引来快速筛选出来一部分指定的数据，接着再进行排序。

因为大多数情况基于索引进行where筛选往往可以最快速度筛选出你要的少部分数据，然后做排序的成本可能会小很多。

### 6、基于慢sql查询做优化

可以根据监控后台的一些慢sql，针对这些慢sql查询做特定的索引优化。

索引设计实战

以社交场景APP来举例，我们一般会去搜索一些好友，这里面就涉及到对用户信息的筛选，这里肯定就是对用户user表搜索了，这个表一般来说数据量会比较大，我们先不考虑分库分表的情况，比如，我们一般会筛选地区(省市)，性别，年龄，身高，爱好之类的，有的APP可能用户还有评分，比如用户的受欢迎程度评分，我们可能还会根据评分来排序等等。

对于后台程序来说除了过滤用户的各种条件，还需要分页之类的处理，可能会生成类似sql语句执行：

select xx from user where xx=xx and xx=xx order by xx limit xx,xx

如何设计索引？若用户经常按省、市筛选，再按性别过滤，`(province, city, sex)` 值得纳入候选；但是否保留仍要看组合选择性、排序需求、写入成本及真实查询计划。单列基数较低并不能直接否定或肯定这个联合索引。

例如查询按省、市与年龄过滤，而索引为 (province, city, sex, age)：缺少 sex 的等值约束会影响 age 的连续定位能力。可比较不同列序或另建索引；不要仅为凑齐索引而加入覆盖全部性别的 IN 条件。

爱好字段若为多值关系，通常不适合简单放进用户表的单列索引；应先确定数据模型与查询路径，再评估复合索引或关联表。

假设可能还有一个筛选条件，比如要筛选最近一周登录过的用户，一般大家肯定希望跟活跃用户交友了，这样能尽快收到反馈，对应后台sql可能是这样：

where  province=xx and city=xx and sex in ('female','male') and age>=xx and age<=xx and latest_login_time>= xx

最近七天登录是随时间滚动的条件。若使用派生布尔列，必须维护失效边界和更新成本；也可针对 login_time 与其他过滤列测试不同索引方案，不能直接断言某一宽索引必然有效。

组合索引能否显著减少候选行依赖数据分布与谓词选择性；排序和分页还需单独评估，不能假定总是落入磁盘 filesort。

不过有时可能用户会这么来查询，就查下受欢迎度较高的女性，比如sql：where  sex = 'female'  order by score limit xx,xx，那么上面那个索引是很难用上的，不能把太多的字段以及太多的值都用 in 语句拼接到sql里的，那怎么办了？其实我们可以再设计一个辅助的联合索引，比如 (sex,score)，这样就能满足查询要求了。

索引组合应覆盖主要查询模式，但数量和列序应由实际 workload、写入代价及回归测试决定，不设“一两个索引覆盖 80% 查询”的固定目标。

![联合索引设计与最左前缀配图](assets/index-1-023-49cbb5dafe5d.webp)



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/04-index-structure-cost.html' | relative_url }}">← 上一篇：索引结构与访问成本</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/06-predicate-index-usage.html' | relative_url }}">下一篇：过滤谓词与索引使用 →</a>
</nav>
