---
layout: default
title: "MySQL 性能调优 · 排序与分组的优化边界"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 07 排序与分组的优化边界

## 先看是否能借用索引顺序

`ORDER BY`/`GROUP BY` 能否利用索引顺序，取决于过滤条件、排序列顺序、方向、连接路径和优化器选择。`Using filesort` 是额外排序算法名称，**不代表一定落盘**；排序缓冲不足时才可能产生临时文件。`Using temporary` 也不是固定的性能故障，需要看参与行数、内存/磁盘临时表和总延迟。

```sql
EXPLAIN SELECT name, age FROM employees
WHERE name = 'LiLei' ORDER BY age;
EXPLAIN SELECT name, age FROM employees
WHERE name > 'LiLei' ORDER BY position;
```

排序可采用 `<sort_key, additional_fields>` 或 `<sort_key, rowid>` 两类模式。不应仅凭旧版本的 `max_length_for_sort_data` 阈值调整新版本配置；应以目标版本的 trace、实际行宽和内存使用验证。若过滤后只剩几十行，先过滤再排序可能优于为排序新增宽索引。减少 `SELECT *` 和过大的返回集往往同样重要。[官方参考：ORDER BY 优化](https://dev.mysql.com/doc/refman/8.0/en/order-by-optimization.html)。



## 排序、分组与 filesort 案例

### 常见sql深入优化

### Order by与Group by优化

Case1：

![排序与分组的优化边界配图](assets/index-1-013-ce4ea0fd6946.webp)

分析：

观察 key、key_len 与 Extra 的组合：等值过滤后的索引有序性可能服务排序，但 key_len 本身不能独立证明排序是否由索引完成；仍需检查 Using filesort 与实际计划。

Case 2：

![排序与分组的优化边界配图](assets/index-1-014-22d22be9b8b1.webp)

分析：

从explain的执行结果来看：key_len=74，查询使用了name索引，由于用了position进行排序，跳过了age，出现了Using filesort。

Case 3：

![排序与分组的优化边界配图](assets/index-1-015-1126573e94a8.webp)

分析：

此例的 WHERE 与 ORDER BY 顺序可能复用联合索引；应核对过滤列是否为常量、排序方向及执行计划，不能只凭索引列名下结论。

Case 4：

![排序与分组的优化边界配图](assets/index-1-016-1bf8696d88cb.webp)

分析：

和Case 3中explain的执行结果一样，但是出现了Using filesort，因为索引的创建顺序为name,age,position，但是排序的时候age和position颠倒位置了。

Case 5：

![排序与分组的优化边界配图](assets/index-1-017-a430ee428bc5.webp)

分析：

与 Case 4 对比，此案例的 `age` 等值条件使该列在结果集中可视为常量，原图计划因而没有 `Using filesort`。这说明本次排序可利用索引顺序，并非所有包含常量列的排序都必然如此。

Case 6：

![排序与分组的优化边界配图](assets/index-1-018-1683e922707d.webp)

分析：

混合升降序是否产生 filesort 取决于索引定义和扫描方向。MySQL 8.0 支持真正的降序索引，可为符合定义的混合方向排序提供索引顺序。

Case 7：

![排序与分组的优化边界配图](assets/index-1-019-c8f6c1e20830.webp)

分析：

多个等值条件可能形成多个范围段，是否仍能复用索引顺序要看实际访问方式和排序列；应以执行计划验证。

Case 8：

![排序与分组的优化边界配图](assets/index-1-020-1f18f5737bb9.webp)

### 可以用覆盖索引优化

![排序与分组的优化边界配图](assets/index-1-021-905a9a3719ec.webp)

优化总结：

1、MySQL 可以利用索引顺序，也可以执行 filesort；Using index 通常表示覆盖索引，不是“使用索引完成排序”的专用标志。

2、能否由索引直接满足 ORDER BY，取决于前导列约束、排序方向、索引定义和查询投影。

1) ORDER BY 与索引键顺序一致，且之前的键列满足必要的等值条件时，可能直接按索引顺序输出。

2) WHERE 与 ORDER BY 可共同匹配索引，但范围条件、混合方向或跨表排序可能打断顺序。

3、尽量在索引列上完成排序，遵循索引建立（索引创建的顺序）时的最左前缀法则。

4、出现 Using filesort 不代表一定写磁盘；它表示额外排序，需结合排序行数、内存和临时文件量判断。

5、覆盖索引能减少回表，但增加索引宽度和写入维护成本，应通过读写基线比较。

6、GROUP BY 能否利用索引取决于分组键和访问路径；MySQL 8.0 不保证 GROUP BY 隐式排序。可先用 WHERE 缩小行集，再评估分组与排序成本。

### Using filesort文件排序原理详解

filesort文件排序方式

- 单路排序：是一次性取出满足条件行的所有字段，然后在sort buffer中进行排序；用trace工具可以看到sort_mode信息里显示< sort_key, additional_fields >或者< sort_key, packed_additional_fields >

- 双路排序（又叫回表排序模式）：是首先根据相应的条件取出相应的排序字段和可以直接定位行数据的行 ID，然后在 sort buffer 中进行排序，排序完后需要再次取回其它需要的字段；用trace工具可以看到sort_mode信息里显示< sort_key, rowid >

排序记录可包含排序键及附加列，也可只保留排序键和行标识后再回表。具体模式由目标版本的优化器决定，不应以旧版本 max_length_for_sort_data 的固定阈值推导当前行为。

下面保留原案例的两种 trace 输出，用于辨认 `sort_mode`。其中通过 `max_length_for_sort_data` 切换模式属于 MySQL 5.7 的历史演示；在 MySQL 8.0 上应以当前版本实际 trace 为准，不照搬该参数命令。

![排序与分组的优化边界配图](assets/index-1-022-9375b4f3fca3.webp)

查看下这条sql对应trace结果如下(只展示排序部分)：

```text
mysql> set session optimizer_trace="enabled=on",end_markers_in_json=on;  --开启trace
mysql> select * from employees where name = 'zhuge' order by position;
mysql> select * from information_schema.OPTIMIZER_TRACE;

trace排序部分结果：
"join_execution": {    --Sql执行阶段
        "select#": 1,
        "steps": [
          {
            "filesort_information": [
              {
                "direction": "asc",
                "table": "`employees`",
                "field": "position"
              }
            ] /* filesort_information */,
            "filesort_priority_queue_optimization": {
              "usable": false,
              "cause": "not applicable (no LIMIT)"
            } /* filesort_priority_queue_optimization */,
            "filesort_execution": [
            ] /* filesort_execution */,
            "filesort_summary": {                      --文件排序信息
              "rows": 10000,                           --预计扫描行数
              "examined_rows": 10000,                  --参与排序的行
              "number_of_tmp_files": 3,                --使用临时文件的个数，这个值如果为0代表全部使用的sort_buffer内存排序，否则使用的磁盘文件排序
              "sort_buffer_size": 262056,              --排序缓存的大小，单位Byte
              "sort_mode": "<sort_key, packed_additional_fields>"       --排序方式，这里用的单路排序
            } /* filesort_summary */
          }
        ] /* steps */
      } /* join_execution */


# 以下一组是旧版 MySQL 的历史输出，不作为 MySQL 8.0 的操作步骤。
mysql> set max_length_for_sort_data = 10;
mysql> select * from employees where name = 'zhuge' order by position;
mysql> select * from information_schema.OPTIMIZER_TRACE;

trace排序部分结果：
"join_execution": {
        "select#": 1,
        "steps": [
          {
            "filesort_information": [
              {
                "direction": "asc",
                "table": "`employees`",
                "field": "position"
              }
            ] /* filesort_information */,
            "filesort_priority_queue_optimization": {
              "usable": false,
              "cause": "not applicable (no LIMIT)"
            } /* filesort_priority_queue_optimization */,
            "filesort_execution": [
            ] /* filesort_execution */,
            "filesort_summary": {
              "rows": 10000,
              "examined_rows": 10000,
              "number_of_tmp_files": 2,
              "sort_buffer_size": 262136,
              "sort_mode": "<sort_key, rowid>"         --排序方式，这里用的双路排序
            } /* filesort_summary */
          }
        ] /* steps */
      } /* join_execution */


mysql> set session optimizer_trace="enabled=off";    --关闭trace
```

我们先看单路排序的详细过程：

- 从索引name找到第一个满足 name = ‘zhuge’ 条件的主键 id

- 根据主键 id 取出整行，取出所有字段的值，存入 sort_buffer 中

- 从索引name找到下一个满足 name = ‘zhuge’ 条件的主键 id

- 重复步骤 2、3 直到不满足 name = ‘zhuge’

- 对 sort_buffer 中的数据按照字段 position 进行排序

- 返回结果给客户端

我们再看下双路排序的详细过程：

- 从索引 name 找到第一个满足 name = ‘zhuge’  的主键id

- 根据主键 id 取出整行，把排序字段 position 和主键 id 这两个字段放到 sort buffer 中

- 从索引 name 取下一个满足 name = ‘zhuge’  记录的主键 id

- 重复 3、4 直到不满足 name = ‘zhuge’

- 对 sort_buffer 中的字段 position 和主键 id 按照字段 position 进行排序

- 遍历排序好的 id 和字段 position，按照 id 的值回到原表中取出 所有字段的值返回给客户端

其实对比两个排序模式，单路排序会把所有需要查询的字段都放到 sort buffer 中，而双路排序只会把主键和需要排序的字段放到 sort buffer 中进行排序，然后再通过主键回到原表查询需要的字段。

增大或缩小 sort_buffer_size 都应由实际并发、排序行数、内存峰值和临时文件指标驱动；不能仅因看到 rowid 排序模式就调整旧参数。

查询仅返回必要列、缩小候选行集，并让合适的索引提供过滤或顺序，通常比盲目扩大排序缓冲区更稳妥。

比较不同排序路径时，应记录 sort_mode、examined_rows、临时文件与实际耗时，并在相同数据分布下复测。

sort_buffer_size 属于按需分配的会话级内存预算之一；高并发下要同时估算连接数与其他每连接缓冲区。



{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/06-predicate-index-usage.html' | relative_url }}">← 上一篇：过滤谓词与索引使用</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/08-optimizer-index-choice.html' | relative_url }}">下一篇：优化器选索引与统计信息 →</a>
</nav>
