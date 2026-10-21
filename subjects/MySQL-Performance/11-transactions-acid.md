---
layout: default
title: "MySQL 性能调优 · 事务、ACID 与提交边界"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回 MySQL 性能调优目录]({{ '/subjects/MySQL-Performance/' | relative_url }})

{% raw %}

# 11 事务、ACID 与提交边界

## 原子性不等于“写一条反向 SQL”

事务把一组操作定义成提交或回滚的工作单元。原资料对 ACID 的框架可保留，但应修正机制表述：undo 记录用于回滚与一致性读，并非简单保存“完全相反的一句 SQL”；redo 支撑崩溃恢复，耐久性还受刷盘配置与硬件故障模型影响；隔离由锁与 MVCC 等共同实现；一致性还依赖约束和应用业务规则。

下面用余额表说明事务边界。演示库先执行：

```sql
CREATE TABLE accounts (
  id BIGINT PRIMARY KEY,
  balance DECIMAL(12,2) NOT NULL
) ENGINE=InnoDB;
INSERT INTO accounts VALUES (1, 1000.00), (2, 1000.00);

START TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
-- 任一步失败，应由应用显式 ROLLBACK，并处理重试与幂等。
```

`autocommit=1` 下每条独立 DML 默认各自成为事务；显式事务需明确异常路径，不要在持锁期间做外部 RPC 或等待人工输入。DDL 的提交行为与普通 DML 不同，不应混入这个转账事务。下一篇讨论并发下“看见什么”。[官方参考：事务](https://dev.mysql.com/doc/refman/8.0/en/commit.html)。
示例仅用于观察原子提交；真实转账还需余额不足检查、请求幂等和失败重试策略。

---

原始资料：[有道云笔记](https://note.youdao.com/noteshare?id=9cdb35f4b463f3db296c57f5120bcf5d&sub=DA9C05A19FCE4B4EA56272006036698F)。

[原资料图像归档](source-figures.html)。

{% endraw %}
<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/MySQL-Performance/10-joins-subqueries-count.html' | relative_url }}">← 上一篇：关联、子查询与计数</a>
  <a href="{{ '/subjects/MySQL-Performance/' | relative_url }}">返回专题目录</a>
  <a href="{{ '/subjects/MySQL-Performance/12-isolation-anomalies.html' | relative_url }}">下一篇：隔离级别与并发异常 →</a>
</nav>
