# CareerPilot Agent 架构说明

## 1. 总览

CareerPilot Agent 是一个基于 OpenHarness 扩展的求职流程智能体。

本项目的目标不是重写 OpenHarness 的底层运行框架，而是在 OpenHarness 之上增加一个垂直领域应用层，用于完成 JD 分析、简历匹配、项目经历提炼、面试准备计划和投递记录管理。

当前 MVP 的核心流程是：

    岗位 JD
      -> JD 分析
      -> 简历匹配
      -> 项目经历提炼
      -> 面试准备计划
      -> 投递记录管理
      -> Demo 报告

## 2. 设计目标

CareerPilot 的架构设计围绕以下几个目标：

1. 保证半月版可以通过命令行稳定运行。
2. 工具输出尽量结构化，方便测试和后续扩展。
3. 简历匹配和修改建议要可解释，而不是只给一个模糊结论。
4. 明确 CareerPilot 和 OpenHarness 的集成边界。
5. 在工作流稳定之前，不提前引入过重的数据库、前端或复杂多 Agent 系统。

## 3. 系统分层

### 3.1 OpenHarness 运行层

OpenHarness 提供基础 Agent 框架和运行环境。

CareerPilot 当前使用或对齐了 OpenHarness 的这些能力：

| OpenHarness 能力 | CareerPilot 中的使用方式 |
|---|---|
| CLI / dry-run | 使用 `oh --dry-run -p` 验证 prompt 组装和工作流可用性 |
| Skills | 使用 Markdown Skill 描述求职工作流 |
| Tool-use 思路 | 实现稳定的 Python 工具模块 |
| Memory 思路 | 使用本地 JSON 保存投递状态 |
| 权限边界 | 文件读写限制在本地项目目录中 |
| Python 测试结构 | 在 `tests/careerpilot/` 中增加单元测试 |

### 3.2 Skill 工作流层

CareerPilot 使用 Markdown 文件定义求职场景的工作流：

    careerpilot/skills/career-coach.md
    careerpilot/skills/resume-rewriter.md
    careerpilot/skills/interview-prep.md

Skill 层主要描述：

1. 什么时候应该使用这个工作流。
2. 需要哪些输入。
3. 应该调用哪些工具。
4. 输出应该长什么样。
5. 哪些事情不能做，例如不能伪造经历、不能夸大技能熟练度。

Skill 层和 Python 工具逻辑是分开的。这样做的好处是：工作流说明更容易阅读，也方便后续接入 OpenHarness 原生 tool registry。

### 3.3 Tool 工具层

CareerPilot 当前有五个主要工具模块：

| 工具 | 文件 | 作用 |
|---|---|---|
| JD Analyzer | `careerpilot/tools/jd_analyzer.py` | 把岗位描述解析为结构化岗位要求 |
| Resume Matcher | `careerpilot/tools/resume_matcher.py` | 对比简历和 JD，输出匹配分、强匹配、缺失技能和修改建议 |
| Project Story Extractor | `careerpilot/tools/project_story_extractor.py` | 把项目说明改写为中英文简历 bullet 和面试故事 |
| Application Tracker | `careerpilot/tools/application_tracker.py` | 保存和更新本地投递记录 |
| Interview Plan Generator | `careerpilot/tools/interview_plan_generator.py` | 根据岗位重点和简历短板生成 3 天或 7 天面试准备计划 |

当前 MVP 中，这些工具主要采用 deterministic parser，也就是规则型、稳定型逻辑。

这样设计的原因是：

1. Demo 更稳定。
2. 测试更容易通过。
3. 输出字段更可控。
4. 后续如果接入 LLM，也可以保留这些字段作为 schema 和 fallback。

### 3.4 Adapter 适配层

CareerPilot 当前包含一个面向 OpenHarness 的适配器：

    careerpilot/openharness_adapter.py

这个适配器的作用是把 OpenHarness 风格的入口和 CareerPilot 内部 Python pipeline 连接起来。

当前边界是：

    OpenHarness:
      - 提供 CLI / dry-run / Skill 工作流入口

    CareerPilot:
      - 提供具体求职工具
      - 生成结构化分析结果
      - 生成 demo report
      - 保存本地 memory

这是一种轻量集成方式。

当前 MVP 不直接修改 OpenHarness core agent loop，也还没有完全接入 OpenHarness 原生 tool registry。这样可以降低前期开发风险，先保证 CareerPilot 的业务闭环跑通。

### 3.5 Demo 演示层

端到端 demo 的主要入口是：

    careerpilot/demo.py

典型运行命令是：

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

这个 demo 会读取本地样例文件，然后依次运行：

    JD Analyzer
      -> Resume Matcher
      -> Project Story Extractor
      -> Interview Plan Generator
      -> Application Tracker

最后输出一个 Markdown 格式的 demo report。

### 3.6 Memory 记忆层

CareerPilot 当前使用本地 JSON 文件保存投递记录：

    careerpilot/memory/applications.json

当前没有使用数据库，原因是半月版更重视：

1. 本地可运行。
2. 文件容易检查。
3. Demo 成本低。
4. 不增加额外依赖。
5. 方便后续迁移到数据库或外部存储。

当前 memory 中保存的信息包括：

    company
    role
    jd_source
    status
    match_score
    next_action
    notes
    created_at
    updated_at

## 4. 主流程数据流

CareerPilot 当前主流程可以理解为：

    用户输入文件
      |
      v
    careerpilot/demo.py 或 careerpilot/openharness_adapter.py
      |
      v
    JD Analyzer
      |
      v
    Resume Matcher
      |
      v
    Project Story Extractor
      |
      v
    Interview Plan Generator
      |
      v
    Application Tracker
      |
      v
    Markdown 报告 + JSON 投递记录

## 5. 输出设计

CareerPilot 的输出设计重点是：

1. 结构化：工具返回稳定字段，方便测试和后续自动化。
2. 可解释：匹配分、缺失技能、修改建议都尽量能追溯到 JD 或简历内容。
3. 可人工审核：简历建议只是草稿，不直接当作真实投递材料。
4. 可测试：核心字段可以通过 pytest 验证。
5. 适合演示：最终报告使用 Markdown，方便截图、阅读和放进 README。

## 6. 测试策略

CareerPilot 的测试位于：

    tests/careerpilot/

当前测试覆盖：

1. JD 关键词提取。
2. 岗位级别判断。
3. 空输入处理。
4. 简历匹配分计算。
5. 缺失技能识别。
6. 项目 bullet 生成。
7. 投递记录新增、更新和查询。
8. 面试准备计划生成。

推荐测试命令：

    python -m pytest -q tests/careerpilot

## 7. 当前 OpenHarness 集成边界

当前 MVP 不声称已经完成 OpenHarness 原生 tool registry 的深度集成。

已经完成：

1. CareerPilot Markdown Skills。
2. CareerPilot deterministic tools。
3. CareerPilot local memory。
4. 端到端 demo script。
5. OpenHarness adapter。
6. OpenHarness dry-run 验证。

尚未完成：

1. OpenHarness 原生 tool registry 注册。
2. 通过 OpenHarness live agent loop 直接执行 CareerPilot tools。
3. ohmo / IM 渠道接入。
4. RAG 简历和项目知识库。
5. 多 Agent 工作流。

## 8. 为什么这样设计

这个架构更适合半月版 MVP。

当前取舍是：

    现在优先稳定：
      - deterministic tools
      - JSON memory
      - CLI demo
      - adapter integration
      - pytest coverage

    后续再增强：
      - native tool registry
      - ohmo / IM integration
      - RAG knowledge base
      - multi-agent workflow
      - benchmark evaluation

这样做可以让 CareerPilot 同时具备两个价值：

1. 现在是一个可运行、可演示的求职工作流工具。
2. 后续可以继续扩展成更完整的 OpenHarness-based agent system。
