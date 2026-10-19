---
layout: default
title: "Git 与 GitLab 版本控制 · CICD 流程过程和架构"
subject_page: true
pdf_notes: true
syntax_highlight: true
---

[← 返回Git 与 GitLab 版本控制目录]({{ '/subjects/Git-GitLab/' | relative_url }})

{% raw %}

# 04 CI/CD 流程与架构

上一章区分了 CI、持续交付与持续部署；本章把这些概念放进实际发布流程，比较手动、脚本化和平台化部署。

### 应用部署发展阶段

**开发人员手动部署。** 开发人员自己构建、上传并启动应用。

这种方式适合快速验证，但步骤依赖个人记忆，难以保证不同环境得到相同结果。应至少记录构建版本和启动参数。

**开发与运维交接后手动部署。** 开发交付代码或制品，运维按操作步骤上传并发布。

职责分工更明确，却仍有重复操作、交接信息丢失和人工输入错误的问题；发布清单与可追溯制品能减少歧义。

**脚本和配置管理工具部署。** 运维将重复步骤写入脚本或自动化工具，减少手工差异。

例如用 Shell、Python 或 Ansible 固定安装、配置和启动步骤。脚本同样需要版本管理、测试、权限控制与失败处理，不能因自动化就省略验证。

**平台化部署。** 通过 Web 界面触发经过审批和验证的流水线，而非把“点击一次”视作完整的发布保障。

平台降低重复操作成本，并提供审批、日志与权限边界；代价是维护执行器、凭据和平台本身。Jenkins 是流水线执行平台之一，仍需要团队定义正确的交付流程。

### CICD 流程

![Git 与 GitLab 版本管理第 17 页插图](assets/img-5eddbc6f8cf84c03.webp)

### 传统方式的CICD 流程

![Git 与 GitLab 版本管理第 17 页插图](assets/img-f66c5dedb4fe81ae.webp)

传统流水线中，开发人员把代码推送到 Git 仓库，Jenkins 拉取指定提交，执行构建、测试和打包，再将制品部署到测试环境。验证通过后才发布到生产环境。某一步失败时应停止下游发布、保留日志并从失败阶段或修复后的新提交重新运行，而不是把未经验证的制品继续分发。

### 容器化方式的 CICD 流程

![Git 与 GitLab 版本管理第 18 页插图](assets/img-bf0c44dfef264bac.webp)

容器化流程通常把构建结果制作成带版本标识的镜像，推送到镜像仓库，再用同一镜像部署到测试及生产环境。镜像扫描、配置与密钥管理、部署后健康检查都应纳入流水线。

### Kubernetes 环境的 CICD 流程

![Git 与 GitLab 版本管理第 18 页插图](assets/img-c9c8b47271153d8f.webp)

在 Kubernetes 中，流水线可更新 Deployment 的镜像版本，由控制器滚动替换 Pod。发布是否成功不能只看命令退出码，还要检查就绪探针、滚动状态和业务指标；异常时回滚到上一版本。

### CICD 相关工具

![Git 与 GitLab 版本管理第 18 页插图](assets/img-b8c3ccebaf6f9124.webp)

### 使用 GitLab 实现 CI/CD

![Git 与 GitLab 版本管理第 19 页插图](assets/img-b75189e1db80cb0f.webp)

![Git 与 GitLab 版本管理第 19 页插图](assets/img-0250bdea387bb32c.webp)

GitLab CI/CD 通过仓库中的流水线配置定义作业，并由 Runner 执行。常见阶段包括检查、测试、构建和部署；每一阶段的制品与结果应可追溯到具体提交。

### CICD 基础架构

![Git 与 GitLab 版本管理第 20 页插图](assets/img-5e2a25d9b06add14.webp)

阅读架构图时可沿“代码仓库 → 流水线执行器 → 制品仓库 → 目标环境 → 监控反馈”的路径追踪：代码决定构建来源，制品保持环境间一致，部署策略控制风险，监控将运行结果反馈到下一轮开发。

{% endraw %}

<nav class="article-end" aria-label="章节导航">
  <a href="{{ '/subjects/Git-GitLab/03-continuous-integration-delivery-and-deployment.html' | relative_url }}">← 上一篇：持续集成、持续交付与持续部署（CI/CD）</a>
  <a href="{{ '/subjects/Git-GitLab/' | relative_url }}">返回 Git 与 GitLab 版本控制目录</a>
  <a href="{{ '/subjects/Git-GitLab/05-version-control-systems.html' | relative_url }}">下一篇：版本控制系统（VCS） →</a>
</nav>
