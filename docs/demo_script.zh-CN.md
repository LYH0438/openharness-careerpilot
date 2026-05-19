# CareerPilot Agent 演示脚本

本文档用于演示 CareerPilot Agent。

目标是证明 CareerPilot 不只是几个脚本，而是一个围绕 OpenHarness 风格的 skills、tools、memory、结构化输出和测试构建出来的完整求职工作流。

## 1. 演示目标

这个 demo 要证明 CareerPilot 可以输入：

- 一份岗位 JD
- 一份简历
- 一份项目说明

然后生成：

- 结构化 JD 分析
- 简历和岗位的匹配报告
- 缺失技能和优化建议
- 可放进简历的项目 bullet
- 3 天或 7 天面试准备计划
- 本地投递记录
- Markdown demo 报告

## 2. 推荐演示流程

### 第一步：介绍项目

可以这样说：

    CareerPilot Agent 是一个基于 OpenHarness 的个人求职流程智能体。
    它在 OpenHarness 风格的工作流之上，扩展了求职场景的 skills、deterministic tools、本地 memory、结构化报告和测试。

需要强调：

- 它是基于 OpenHarness 扩展的，不是一个完全无关的独立脚本。
- 它聚焦在求职这个明确的垂直场景。
- 它覆盖从 JD 分析到面试准备和投递记录的闭环。

### 第二步：展示项目结构

命令：

    tree -L 3 careerpilot docs examples/careerpilot tests/careerpilot

如果没有安装 `tree`，使用：

    find careerpilot docs examples/careerpilot tests/careerpilot -maxdepth 3 -type f | sort

重点解释这些目录：

- `careerpilot/tools/`：具体工具模块
- `careerpilot/skills/`：Markdown 工作流 Skill
- `careerpilot/memory/`：本地 JSON 投递记录
- `examples/careerpilot/`：样例输入和输出
- `tests/careerpilot/`：单元测试
- `docs/`：架构、集成说明、技术决策、已知问题和演示脚本

### 第三步：展示输入文件

命令：

    cat examples/careerpilot/sample_jd_backend.md

    cat examples/careerpilot/sample_resume.md

    cat examples/careerpilot/sample_project_readme.md

说明：

- JD 提供岗位要求。
- 简历提供用户已有经历证据。
- 项目 README 提供生成简历 bullet 和面试故事的材料。

### 第四步：运行完整 demo

命令：

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

预期结果：

    examples/careerpilot/demo_report.md

### 第五步：展示生成报告

命令：

    cat examples/careerpilot/demo_report.md

重点展示：

- 岗位总结
- 岗位级别
- 核心技能
- 加分技能
- 简历匹配分
- 强匹配项
- 缺失技能
- 简历改写建议
- 项目简历 bullet
- 面试准备计划
- 投递记录摘要

### 第六步：展示本地 memory

命令：

    cat careerpilot/memory/applications.json

说明：

- CareerPilot 会保存本地投递记录。
- 这让它在 MVP 阶段具备最小状态管理能力。
- 当前使用 JSON 是为了简单、可读、方便 demo。

### 第七步：展示 OpenHarness 集成边界

命令：

    python -m careerpilot.openharness_adapter \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

如果当前环境支持，也可以展示 OpenHarness dry-run：

    uv run oh --dry-run -p "Use career-coach skill. Analyze examples/careerpilot/sample_jd_backend.md and compare it with examples/careerpilot/sample_resume.md. Generate a job-fit report using CareerPilot."

说明：

- 当前集成是轻量且显式的。
- CareerPilot 使用 OpenHarness 风格的 skills 和 adapter。
- OpenHarness 原生 tool registry 集成是后续增强方向。

### 第八步：运行测试

命令：

    python -m pytest -q tests/careerpilot

预期结果：

    21 passed

说明：

- 测试让项目不只是 prompt demo。
- 当前测试覆盖 JD 分析、简历匹配、项目经历提炼、投递记录和面试计划。

## 3. 两分钟讲解稿

CareerPilot Agent 是一个基于 OpenHarness 的个人求职流程智能体。它的目标是自动化真实求职流程：分析岗位 JD、对比简历、提炼项目经历、生成面试准备计划，并记录投递状态。

我实现了几个领域工具，包括 JD Analyzer、Resume Matcher、Project Story Extractor、Application Tracker 和 Interview Plan Generator。同时我增加了 Markdown Skills 描述求职工作流，并用本地 JSON memory 保存投递记录。

当前 MVP 通过 Markdown Skills、OpenHarness dry-run 验证和 adapter 模块实现轻量集成。这样既能保持项目稳定，也能和 OpenHarness 的 skills、tools、memory、CLI workflow 等概念对齐。

在工程质量方面，我增加了 `tests/careerpilot` 下的单元测试，目前 CareerPilot 测试全部通过。下一阶段可以继续做 OpenHarness 原生 tool registry 集成、ohmo 聊天渠道接入、RAG 简历知识库、多 Agent 工作流和 benchmark 评估。

## 4. 五分钟讲解结构

更长面试讲解可以按照这个结构：

1. 问题背景：
   手动针对不同 JD 修改简历耗时、重复，而且容易不系统。

2. 为什么使用 OpenHarness：
   OpenHarness 已经提供 Agent 框架相关概念，例如 skills、tools、memory、CLI entrypoints 和 permission-aware workflows。

3. 系统架构：
   CareerPilot 在 OpenHarness 之上增加求职领域层，包括 skills、deterministic tools、本地 memory 和 demo pipeline。

4. 核心工具：
   - JD Analyzer 解析岗位要求。
   - Resume Matcher 生成可解释匹配分。
   - Project Story Extractor 生成简历 bullet 和面试故事。
   - Interview Plan Generator 生成 3 天或 7 天准备计划。
   - Application Tracker 保存本地投递状态。

5. Demo：
   运行 demo 命令，并展示生成的 Markdown 报告。

6. 测试：
   运行 `python -m pytest -q tests/careerpilot`。

7. 当前限制：
   当前集成仍然是轻量级，匹配分是启发式评分，简历建议需要人工审核。

8. 后续计划：
   OpenHarness 原生 tool registry、ohmo 集成、RAG 知识库、多 Agent 工作流、benchmark 评估和安全策略。

## 5. 常见面试问题

### Q1：这个是不是只是 prompt wrapper？

不是。MVP 包含 deterministic Python tools、结构化输出、本地 memory、Markdown skills、端到端 CLI workflow 和单元测试。Prompt 和 Skill 更多是工作流定义，核心逻辑在可测试的 Python 模块中。

### Q2：为什么先用 deterministic tools，而不是完全用 LLM？

MVP 需要稳定输出，方便 demo 和测试。规则型工具让项目更可靠，也更容易 debug。后续可以再叠加 LLM layer，提高语言理解能力。

### Q3：这里 OpenHarness 具体提供了什么？

OpenHarness 提供底层 Agent 框架方向、CLI/dry-run 工作流、skill-based organization，以及 tools 和 memory 等概念。CareerPilot 在这些概念之上扩展求职领域工作流。

### Q4：当前最大的限制是什么？

当前最大限制是 CareerPilot tools 还没有完全注册为 OpenHarness runtime 中的原生工具。现在的集成是通过 skills、dry-run 和 adapter 实现的轻量集成。

### Q5：后续你会怎么改进？

下一步会做 OpenHarness 原生 tool registry 集成、通过 ohmo 接入聊天渠道、加入 RAG 个人知识库、多 Agent 角色拆分、benchmark 评估和更明确的安全策略。
