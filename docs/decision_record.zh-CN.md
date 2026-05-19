# CareerPilot Agent 技术决策记录

本文档记录 CareerPilot Agent MVP 阶段的重要技术决策和产品取舍。

它的作用是让项目后续更容易维护，也方便面试时解释：为什么这么设计，而不是只说做了哪些功能。

## DR-001：为什么基于 OpenHarness，而不是从零开始写？

### 决策

CareerPilot 选择基于 OpenHarness 扩展，而不是从零实现一个新的 Agent 框架。

### 原因

OpenHarness 已经提供了 Agent 系统需要的一些基础概念：

- Agent workflow
- Tool-use pattern
- Skill files
- Memory pattern
- CLI entrypoint
- Permission-aware execution
- 可扩展的项目结构

CareerPilot 的重点不是重新造一个通用 Agent 框架，而是在 OpenHarness 之上做求职场景的垂直能力。

### 取舍

这样可以更快做出 MVP，也更容易体现“基于现有 Agent 框架做二次开发”的能力。

代价是 CareerPilot 需要遵守 OpenHarness 的集成边界，后续如果要做原生 tool registry 集成，还需要继续深入 OpenHarness 内部机制。

## DR-002：为什么先用 deterministic tools，而不是完全依赖 LLM？

### 决策

MVP 阶段使用 deterministic Python tools 来实现 JD 分析、简历匹配、项目经历提炼、投递记录管理和面试计划生成。

### 原因

MVP 需要稳定输出，方便：

- Demo 演示
- 单元测试
- 结构化报告
- 重复运行样例
- 调试问题

如果完全依赖 LLM，表达能力会更强，但输出不稳定，测试也更困难。

### 取舍

规则型工具对复杂、非常规输入的理解能力不如 LLM 灵活。

但好处是可以通过 `pytest` 验证，也更像一个工程项目，而不是单纯的 prompt demo。

## DR-003：为什么用本地 JSON memory，而不是数据库？

### 决策

CareerPilot 使用本地 JSON 文件保存投递记录：

    careerpilot/memory/applications.json

### 原因

半月版 MVP 使用 JSON 已经足够，因为：

- 不需要数据库安装和配置。
- 文件容易直接查看。
- Demo 更轻量。
- 适合本地 CLI 工作流。
- 方便后续迁移到数据库或外部存储。

### 取舍

JSON 不适合多人并发、远程访问和复杂查询。

如果后续 CareerPilot 变成 Web 应用或多用户系统，可以再引入 SQLite、PostgreSQL 或其他存储方案。

## DR-004：为什么使用 Markdown Skills？

### 决策

CareerPilot 使用 Markdown 文件描述求职工作流。

当前 Skill 文件包括：

    careerpilot/skills/career-coach.md
    careerpilot/skills/resume-rewriter.md
    careerpilot/skills/interview-prep.md

### 原因

Markdown Skill 方便阅读、修改和 review。

它可以把高层工作流说明和 Python 工具实现分开。

这也符合 OpenHarness 中 skill-based workflow 的思想。

### 取舍

Markdown Skill 本身不等于深度 runtime 集成。

当前 MVP 先把它作为工作流定义，后续再逐步接入 OpenHarness 原生执行机制。

## DR-005：为什么使用 adapter 层接入 OpenHarness？

### 决策

CareerPilot 增加了一个轻量适配器：

    careerpilot/openharness_adapter.py

### 原因

adapter 可以把 OpenHarness 风格的入口和 CareerPilot 内部 Python pipeline 连接起来，同时不需要修改 OpenHarness core agent loop。

这样可以降低 MVP 阶段的开发风险。

同时，CareerPilot 的工具仍然可以独立运行、独立测试。

### 取舍

这种方式不是完整的 OpenHarness native tool registry 集成。

原生集成是后续增强方向。

## DR-006：为什么生成 Markdown demo report？

### 决策

端到端 demo 生成 Markdown 报告：

    examples/careerpilot/demo_report.md

### 原因

Markdown 方便阅读、复制、放进 README，也方便 GitHub 展示。

报告可以包含：

- JD 分析
- 简历匹配分
- 能力缺口
- 项目简历 bullet
- 面试准备计划
- 投递记录摘要

### 取舍

Markdown 不如 JSON 适合机器继续处理。

后续如果要做自动化流水线，可以增加 JSON 输出或 schema-validated report object。

## DR-007：为什么强调简历建议必须人工审核？

### 决策

CareerPilot 把生成的简历建议视为草稿，需要人工审核后才能使用。

### 原因

简历内容有真实性和诚信边界。

Agent 可以帮助用户整理和改写真实经历，但不应该伪造经历、夸大技能或自动生成未经确认的最终投递材料。

### 取舍

这降低了全自动化程度。

但好处是项目更安全，也更符合真实求职场景。

## DR-008：为什么 MVP 阶段就写测试？

### 决策

CareerPilot 在 MVP 阶段就增加了单元测试：

    tests/careerpilot/

### 原因

测试可以让项目更像工程项目，而不是临时脚本。

测试也能保护核心工具逻辑，避免后续改功能时破坏已有输出。

当前测试覆盖 JD 分析、简历匹配、项目经历提炼、投递记录管理和面试计划生成。

### 取舍

写测试会增加短期开发时间。

但它能提高可信度，也方便后续维护。

## DR-009：为什么 MVP 不做 Web 前端？

### 决策

MVP 阶段不做 Web 前端。

### 原因

当前优先级是先验证求职 Agent 的完整工作流。

如果过早做前端，会增加页面设计、路由、部署、状态管理等工作，反而分散核心逻辑开发时间。

### 取舍

MVP 看起来不如 Web 产品直观。

但好处是可以把时间集中在工具设计、工作流质量、文档、测试和 OpenHarness 集成边界上。

## DR-010：下一阶段架构方向是什么？

### 决策

下一阶段应该把 CareerPilot 从 CLI MVP 升级为更完整的 Agent System。

### 计划方向

- OpenHarness 原生 tool registry 集成
- ohmo / IM 渠道接入
- RAG 简历和项目知识库
- 多 Agent 工作流
- Benchmark 和质量评估
- 简历版本管理
- 安全策略和权限边界

### 原因

这些能力可以让 CareerPilot 不只是一个脚本集合，而是更接近真实的 Agent 系统。
