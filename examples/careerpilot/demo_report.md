# CareerPilot End-to-End Demo Report

## Input Files

- JD: `examples/careerpilot/sample_jd_backend.md`
- Resume: `examples/careerpilot/sample_resume.md`
- Project README: `examples/careerpilot/sample_project_readme.md`

---

# 1. JD Analysis Report

## Role Summary

Backend Engineer role focused on Python, FastAPI, TypeScript, PostgreSQL.

## Seniority Level

mid

## Core Skills

- Python
- FastAPI
- TypeScript
- PostgreSQL
- Redis
- Docker
- CI/CD
- REST API
- Distributed Systems

## Nice-to-have Skills

- Kubernetes
- AWS
- LLM
- Agent

## Responsibilities

- 设计和维护后端服务
- 开发和维护 API
- 数据库设计与性能优化
- 构建可扩展系统
- 参与部署和 DevOps 流程
- 与跨职能团队协作

## Keywords for Resume

- Python
- FastAPI
- TypeScript
- PostgreSQL
- Redis
- Docker
- CI/CD
- REST API
- Distributed Systems
- Kubernetes
- AWS
- LLM
- Agent
- 设计和维护后端服务
- 开发和维护 API
- 数据库设计与性能优化
- 构建可扩展系统
- 参与部署和 DevOps 流程
- 与跨职能团队协作

## Interview Focus

- API 设计与后端服务实现
- 数据库设计、索引和性能优化
- 部署、云服务和 DevOps 基础
- 系统设计与可扩展架构

## Risk Notes

- 岗位包含明显部署或基础设施要求，简历中需要补充上线、部署或 DevOps 经验。
- 岗位可能关注系统设计能力，需要准备高并发、缓存、数据库扩展等案例。
- 岗位涉及 AI Agent 或 LLM 应用，需要准备工具调用、上下文管理和输出稳定性相关讲法。

---

# 2. Resume Match Report

## Match Score

**68 / 100**

## Strong Matches

- Python
- FastAPI
- PostgreSQL
- Redis
- Docker
- CI/CD
- REST API
- Distributed Systems

## Missing Skills

- TypeScript

## Weak Evidence

- Resume lacks quantified impact. Add measurable results such as latency reduction, API throughput, user scale, test coverage, or time saved.
- Core skill evidence is missing for: TypeScript. Add truthful project evidence instead of only listing them in the skills section.
- Resume does not clearly address responsibilities: 设计和维护后端服务, 开发和维护 API, 数据库设计与性能优化. Rewrite one project bullet to mirror these responsibilities.

## Resume Keywords to Add

- TypeScript
- 设计和维护后端服务
- 开发和维护 API
- 数据库设计与性能优化
- 构建可扩展系统
- 参与部署和 DevOps 流程
- 与跨职能团队协作

## Rewrite Suggestions

- {"section": "Project Experience", "before": "Built a backend system.", "after": "Built a backend-focused service for Backend Engineer roles using Python, FastAPI, PostgreSQL, owning API design, data modeling, and implementation trade-offs; add one measurable result such as request latency, reliability, user scale, or development time saved."}
- {"section": "Skills / Keywords", "before": "Listed general programming skills.", "after": "Add targeted keywords such as TypeScript, 设计和维护后端服务, 开发和维护 API, 数据库设计与性能优化, but only when they are supported by real project or work experience."}
- {"section": "Gap Fix", "before": "Missing JD requirements are not addressed.", "after": "Create or rewrite one bullet to provide evidence for TypeScript; use the format: Built [feature] with [technology], solved [problem], and improved [metric/result]."}
- {"section": "Impact Metrics", "before": "Project bullets describe work without numbers.", "after": "Add at least one quantified result, for example: reduced manual analysis time by X%, processed N records, supported N users, improved test coverage to X%, or shortened workflow time from A to B."}

## Interview Preparation Topics

- API 设计与后端服务实现
- 数据库设计、索引和性能优化
- 部署、云服务和 DevOps 基础
- 系统设计与可扩展架构
- TypeScript
- 设计和维护后端服务
- 开发和维护 API

---

# 3. Project Story Extraction

## One-liner

基于 OpenHarness 构建的面向 Backend Engineer 求职流程智能体

## Tech Stack

- OpenHarness
- Python
- Pydantic
- Agent
- Tool Calling
- Skill
- Memory
- CLI

## Architecture Highlights

- 自定义 Tool 抽象，用于封装 JD 分析、简历匹配和项目经历提炼能力
- Skill 驱动的领域工作流，将求职流程拆分为可复用步骤
- 本地 Memory 记录投递状态、用户画像和结构化分析结果
- CLI / demo script 支持端到端求职流程演示
- 使用测试覆盖核心工具逻辑，提升输出稳定性

## Resume Bullets CN

- 基于 OpenHarness、Python、Pydantic、Agent 构建面向 Backend Engineer 的项目经历提炼工具，将项目 README/说明文档结构化转化为中英文简历 bullet、STAR 面试故事和潜在面试问题，提升求职材料复用效率和表达一致性。
- 设计覆盖项目一句话总结、技术栈、架构亮点、简历表述和面试故事的结构化输出 schema，通过稳定字段支持端到端 demo、单元测试和后续 OpenHarness workflow 编排。
- 围绕自定义 Tool 抽象实现规则化关键词识别与模板化生成逻辑，将 JD 分析、简历匹配和项目经历提炼能力封装为可测试模块，降低自由生成带来的不稳定风险，使输出结果更适合简历微调、面试复盘和自动化测试。

## Resume Bullets EN

- Built a project story extraction tool for Backend Engineer workflows using OpenHarness, Python, Pydantic, Agent, transforming README-style project descriptions into bilingual resume bullets, STAR interview stories, and likely interview questions to improve reuse and consistency of job-search materials.
- Designed a structured output schema covering project summary, tech stack, architecture highlights, resume-ready bullets, and interview narratives, enabling stable end-to-end demos, unit tests, and future OpenHarness workflow integration.
- Implemented deterministic keyword extraction and template-based generation around custom tool abstractions, packaging JD analysis, resume matching, and project story extraction into testable modules while making outputs easier to review, test, and tailor for interviews.

## Interview Story

Problem: 求职过程中，项目经历往往需要针对不同岗位重新组织表达，手动改写耗时且容易遗漏技术亮点。

Solution: 围绕 Backend Engineer 场景设计 Project Story Extractor，将项目说明结构化解析为技术栈、架构亮点、简历 bullet 和面试故事。

Impact: 在 demo 场景中，可以把项目材料快速转化为可复用的简历和面试表达，减少重复整理成本，并提升输出一致性。

## Possible Interview Questions

- 你为什么要把项目经历提炼单独做成一个 Tool？
- 这个工具和普通 prompt 生成简历 bullet 有什么区别？
- 你如何保证输出字段稳定，方便后续测试和 workflow 编排？
- 你在这个项目里具体使用了 OpenHarness 的哪些能力？
- 为什么使用 Pydantic 定义输入输出 schema？
- Tool schema 设计时，你如何划分输入、输出和异常情况？

---

# 4. Interview Preparation Plan

# Interview Preparation Plan

Target role: **Backend Engineer**
Schedule: **7 days × 2 hours/day**

## Priority Topics
- API 设计与后端服务实现
- 数据库设计、索引和性能优化
- 部署、云服务和 DevOps 基础
- 系统设计与可扩展架构
- TypeScript
- 设计和维护后端服务
- 开发和维护 API
- Python
- FastAPI
- PostgreSQL
- 数据库设计与性能优化
- 补强薄弱证据与量化结果

## Day 1: Backend API Fundamentals

Focus:
- API 设计与后端服务实现

Tasks:
- 复习 REST API 设计、认证授权、错误处理、分页和幂等性。
- 整理一个你在项目中设计或维护 API 的案例，说明输入、输出、边界和失败处理。
- 准备 2 个英文回答：API design trade-off 和 backend service ownership。

Deliverables:
- 2 个 API 设计面试回答
- 1 个后端服务 STAR 项目故事

## Day 2: Database and Performance

Focus:
- 数据库设计、索引和性能优化

Tasks:
- 复习索引、事务、慢查询、连接池和缓存的基础概念。
- 把项目中的数据库使用场景改写成一个性能优化或数据建模故事。
- 准备解释：什么时候加索引、什么时候用缓存、如何排查慢查询。

Deliverables:
- 1 个数据库优化 STAR 故事
- 3 个数据库高频问题的要点答案

## Day 3: Deployment, Cloud, and DevOps

Focus:
- 部署、云服务和 DevOps 基础

Tasks:
- 复习 Docker 镜像、容器运行、环境变量、日志和基础部署流程。
- 整理你项目中可诚实描述的部署、测试或 CI/CD 经验。
- 准备说明你如何让一个服务从本地脚本变成可运行 demo。

Deliverables:
- 1 个部署或 CI/CD 项目回答
- 1 份可加入简历的 DevOps 证据 bullet 草稿

## Day 4: System Design and Scalability

Focus:
- 系统设计与可扩展架构

Tasks:
- 复习容量估算、API 边界、数据存储、缓存、异步任务和故障处理。
- 用 CareerPilot demo 画出一个简单系统设计讲法：输入、工具、报告、memory。
- 准备回答：如何从单脚本演进到多 Agent 或 RAG 系统。

Deliverables:
- 1 个系统设计口述大纲
- 1 张文字版架构图或流程图

## Day 5: Role Requirement Deep Dive: TypeScript

Focus:
- TypeScript

Tasks:
- 复习 JD 中与 `TypeScript` 相关的基础概念、常见问题和项目使用场景。
- 把该主题映射到你的简历证据：项目、课程、工具或真实经历。
- 准备一个 60-90 秒回答，说明你如何学习或实践过该主题。

Deliverables:
- 1 个围绕 `TypeScript` 的面试回答
- 1 条可人工审核的简历补充建议

## Day 6: Backend API Fundamentals

Focus:
- 设计和维护后端服务

Tasks:
- 复习 REST API 设计、认证授权、错误处理、分页和幂等性。
- 整理一个你在项目中设计或维护 API 的案例，说明输入、输出、边界和失败处理。
- 准备 2 个英文回答：API design trade-off 和 backend service ownership。

Deliverables:
- 2 个 API 设计面试回答
- 1 个后端服务 STAR 项目故事

## Day 7: Mock Interview and Final Review

Focus:
- API 设计与后端服务实现
- 数据库设计、索引和性能优化
- 部署、云服务和 DevOps 基础
- 系统设计与可扩展架构

Tasks:
- 进行一轮 30-45 分钟模拟面试：自我介绍、项目深挖、技术基础、行为问题。
- 检查每个高优先级主题是否都有一个真实项目证据或诚实的学习计划。
- 复盘回答中过度夸大、缺少数字、缺少技术细节的地方。

Deliverables:
- 1 份 2 分钟英文自我介绍
- 3 个项目深挖答案
- 1 份最后修改清单

## Final Checklist
- 每个 JD 核心技能至少对应一个简历或项目证据。
- 每个缺失技能都有诚实表述：补项目证据、写 familiar，或放入学习计划。
- 至少准备 3 个 STAR 项目故事：后端实现、问题排查、结果影响。
- 所有简历修改都需要人工审核，不能编造经历或夸大熟练度。

> Human review required: This interview plan is generated for preparation purposes. Verify every resume claim and project story before using it in real applications.

---

# 5. Application Tracker Summary

- {"company": "Example AI", "role": "AI Agent Engineer", "jd_source": "examples/careerpilot/sample_jd_backend.md", "status": "applied", "match_score": 78, "next_action": "prepare backend system design interview answers", "created_at": "2026-05-17", "updated_at": "2026-05-17", "notes": ["需要补充 MCP 和多 Agent 相关表述", "已完成第一版简历投递"]}
- {"company": "Example AI", "role": "Backend Engineer", "jd_source": "examples/careerpilot/sample_jd_backend.md", "status": "preparing", "match_score": 68, "next_action": "review generated demo report and rewrite project bullets", "created_at": "2026-05-17", "updated_at": "2026-05-17", "notes": ["Generated from CareerPilot Day 7 demo flow."]}

---

# 6. Raw Structured Outputs

## JD Analysis JSON

{
  "role_summary": "Backend Engineer role focused on Python, FastAPI, TypeScript, PostgreSQL.",
  "seniority_level": "mid",
  "core_skills": [
    "Python",
    "FastAPI",
    "TypeScript",
    "PostgreSQL",
    "Redis",
    "Docker",
    "CI/CD",
    "REST API",
    "Distributed Systems"
  ],
  "nice_to_have_skills": [
    "Kubernetes",
    "AWS",
    "LLM",
    "Agent"
  ],
  "responsibilities": [
    "设计和维护后端服务",
    "开发和维护 API",
    "数据库设计与性能优化",
    "构建可扩展系统",
    "参与部署和 DevOps 流程",
    "与跨职能团队协作"
  ],
  "keywords_for_resume": [
    "Python",
    "FastAPI",
    "TypeScript",
    "PostgreSQL",
    "Redis",
    "Docker",
    "CI/CD",
    "REST API",
    "Distributed Systems",
    "Kubernetes",
    "AWS",
    "LLM",
    "Agent",
    "设计和维护后端服务",
    "开发和维护 API",
    "数据库设计与性能优化",
    "构建可扩展系统",
    "参与部署和 DevOps 流程",
    "与跨职能团队协作"
  ],
  "interview_focus": [
    "API 设计与后端服务实现",
    "数据库设计、索引和性能优化",
    "部署、云服务和 DevOps 基础",
    "系统设计与可扩展架构"
  ],
  "risk_notes": [
    "岗位包含明显部署或基础设施要求，简历中需要补充上线、部署或 DevOps 经验。",
    "岗位可能关注系统设计能力，需要准备高并发、缓存、数据库扩展等案例。",
    "岗位涉及 AI Agent 或 LLM 应用，需要准备工具调用、上下文管理和输出稳定性相关讲法。"
  ]
}

## Resume Match JSON

{
  "match_score": 68,
  "strong_matches": [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "Redis",
    "Docker",
    "CI/CD",
    "REST API",
    "Distributed Systems"
  ],
  "missing_skills": [
    "TypeScript"
  ],
  "weak_evidence": [
    "Resume lacks quantified impact. Add measurable results such as latency reduction, API throughput, user scale, test coverage, or time saved.",
    "Core skill evidence is missing for: TypeScript. Add truthful project evidence instead of only listing them in the skills section.",
    "Resume does not clearly address responsibilities: 设计和维护后端服务, 开发和维护 API, 数据库设计与性能优化. Rewrite one project bullet to mirror these responsibilities."
  ],
  "resume_keywords_to_add": [
    "TypeScript",
    "设计和维护后端服务",
    "开发和维护 API",
    "数据库设计与性能优化",
    "构建可扩展系统",
    "参与部署和 DevOps 流程",
    "与跨职能团队协作"
  ],
  "rewrite_suggestions": [
    {
      "section": "Project Experience",
      "before": "Built a backend system.",
      "after": "Built a backend-focused service for Backend Engineer roles using Python, FastAPI, PostgreSQL, owning API design, data modeling, and implementation trade-offs; add one measurable result such as request latency, reliability, user scale, or development time saved."
    },
    {
      "section": "Skills / Keywords",
      "before": "Listed general programming skills.",
      "after": "Add targeted keywords such as TypeScript, 设计和维护后端服务, 开发和维护 API, 数据库设计与性能优化, but only when they are supported by real project or work experience."
    },
    {
      "section": "Gap Fix",
      "before": "Missing JD requirements are not addressed.",
      "after": "Create or rewrite one bullet to provide evidence for TypeScript; use the format: Built [feature] with [technology], solved [problem], and improved [metric/result]."
    },
    {
      "section": "Impact Metrics",
      "before": "Project bullets describe work without numbers.",
      "after": "Add at least one quantified result, for example: reduced manual analysis time by X%, processed N records, supported N users, improved test coverage to X%, or shortened workflow time from A to B."
    }
  ],
  "interview_preparation_topics": [
    "API 设计与后端服务实现",
    "数据库设计、索引和性能优化",
    "部署、云服务和 DevOps 基础",
    "系统设计与可扩展架构",
    "TypeScript",
    "设计和维护后端服务",
    "开发和维护 API"
  ]
}

## Project Story JSON

{
  "one_liner": "基于 OpenHarness 构建的面向 Backend Engineer 求职流程智能体",
  "tech_stack": [
    "OpenHarness",
    "Python",
    "Pydantic",
    "Agent",
    "Tool Calling",
    "Skill",
    "Memory",
    "CLI"
  ],
  "architecture_highlights": [
    "自定义 Tool 抽象，用于封装 JD 分析、简历匹配和项目经历提炼能力",
    "Skill 驱动的领域工作流，将求职流程拆分为可复用步骤",
    "本地 Memory 记录投递状态、用户画像和结构化分析结果",
    "CLI / demo script 支持端到端求职流程演示",
    "使用测试覆盖核心工具逻辑，提升输出稳定性"
  ],
  "resume_bullets_cn": [
    "基于 OpenHarness、Python、Pydantic、Agent 构建面向 Backend Engineer 的项目经历提炼工具，将项目 README/说明文档结构化转化为中英文简历 bullet、STAR 面试故事和潜在面试问题，提升求职材料复用效率和表达一致性。",
    "设计覆盖项目一句话总结、技术栈、架构亮点、简历表述和面试故事的结构化输出 schema，通过稳定字段支持端到端 demo、单元测试和后续 OpenHarness workflow 编排。",
    "围绕自定义 Tool 抽象实现规则化关键词识别与模板化生成逻辑，将 JD 分析、简历匹配和项目经历提炼能力封装为可测试模块，降低自由生成带来的不稳定风险，使输出结果更适合简历微调、面试复盘和自动化测试。"
  ],
  "resume_bullets_en": [
    "Built a project story extraction tool for Backend Engineer workflows using OpenHarness, Python, Pydantic, Agent, transforming README-style project descriptions into bilingual resume bullets, STAR interview stories, and likely interview questions to improve reuse and consistency of job-search materials.",
    "Designed a structured output schema covering project summary, tech stack, architecture highlights, resume-ready bullets, and interview narratives, enabling stable end-to-end demos, unit tests, and future OpenHarness workflow integration.",
    "Implemented deterministic keyword extraction and template-based generation around custom tool abstractions, packaging JD analysis, resume matching, and project story extraction into testable modules while making outputs easier to review, test, and tailor for interviews."
  ],
  "interview_story": {
    "problem": "求职过程中，项目经历往往需要针对不同岗位重新组织表达，手动改写耗时且容易遗漏技术亮点。",
    "solution": "围绕 Backend Engineer 场景设计 Project Story Extractor，将项目说明结构化解析为技术栈、架构亮点、简历 bullet 和面试故事。",
    "impact": "在 demo 场景中，可以把项目材料快速转化为可复用的简历和面试表达，减少重复整理成本，并提升输出一致性。"
  },
  "possible_interview_questions": [
    "你为什么要把项目经历提炼单独做成一个 Tool？",
    "这个工具和普通 prompt 生成简历 bullet 有什么区别？",
    "你如何保证输出字段稳定，方便后续测试和 workflow 编排？",
    "你在这个项目里具体使用了 OpenHarness 的哪些能力？",
    "为什么使用 Pydantic 定义输入输出 schema？",
    "Tool schema 设计时，你如何划分输入、输出和异常情况？"
  ]
}

## Interview Plan JSON

{
  "target_role": "Backend Engineer",
  "available_days": 7,
  "daily_hours": 2.0,
  "priority_topics": [
    "API 设计与后端服务实现",
    "数据库设计、索引和性能优化",
    "部署、云服务和 DevOps 基础",
    "系统设计与可扩展架构",
    "TypeScript",
    "设计和维护后端服务",
    "开发和维护 API",
    "Python",
    "FastAPI",
    "PostgreSQL",
    "数据库设计与性能优化",
    "补强薄弱证据与量化结果"
  ],
  "daily_plan": [
    {
      "day": 1,
      "title": "Backend API Fundamentals",
      "focus": [
        "API 设计与后端服务实现"
      ],
      "tasks": [
        "复习 REST API 设计、认证授权、错误处理、分页和幂等性。",
        "整理一个你在项目中设计或维护 API 的案例，说明输入、输出、边界和失败处理。",
        "准备 2 个英文回答：API design trade-off 和 backend service ownership。"
      ],
      "deliverables": [
        "2 个 API 设计面试回答",
        "1 个后端服务 STAR 项目故事"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 2,
      "title": "Database and Performance",
      "focus": [
        "数据库设计、索引和性能优化"
      ],
      "tasks": [
        "复习索引、事务、慢查询、连接池和缓存的基础概念。",
        "把项目中的数据库使用场景改写成一个性能优化或数据建模故事。",
        "准备解释：什么时候加索引、什么时候用缓存、如何排查慢查询。"
      ],
      "deliverables": [
        "1 个数据库优化 STAR 故事",
        "3 个数据库高频问题的要点答案"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 3,
      "title": "Deployment, Cloud, and DevOps",
      "focus": [
        "部署、云服务和 DevOps 基础"
      ],
      "tasks": [
        "复习 Docker 镜像、容器运行、环境变量、日志和基础部署流程。",
        "整理你项目中可诚实描述的部署、测试或 CI/CD 经验。",
        "准备说明你如何让一个服务从本地脚本变成可运行 demo。"
      ],
      "deliverables": [
        "1 个部署或 CI/CD 项目回答",
        "1 份可加入简历的 DevOps 证据 bullet 草稿"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 4,
      "title": "System Design and Scalability",
      "focus": [
        "系统设计与可扩展架构"
      ],
      "tasks": [
        "复习容量估算、API 边界、数据存储、缓存、异步任务和故障处理。",
        "用 CareerPilot demo 画出一个简单系统设计讲法：输入、工具、报告、memory。",
        "准备回答：如何从单脚本演进到多 Agent 或 RAG 系统。"
      ],
      "deliverables": [
        "1 个系统设计口述大纲",
        "1 张文字版架构图或流程图"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 5,
      "title": "Role Requirement Deep Dive: TypeScript",
      "focus": [
        "TypeScript"
      ],
      "tasks": [
        "复习 JD 中与 `TypeScript` 相关的基础概念、常见问题和项目使用场景。",
        "把该主题映射到你的简历证据：项目、课程、工具或真实经历。",
        "准备一个 60-90 秒回答，说明你如何学习或实践过该主题。"
      ],
      "deliverables": [
        "1 个围绕 `TypeScript` 的面试回答",
        "1 条可人工审核的简历补充建议"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 6,
      "title": "Backend API Fundamentals",
      "focus": [
        "设计和维护后端服务"
      ],
      "tasks": [
        "复习 REST API 设计、认证授权、错误处理、分页和幂等性。",
        "整理一个你在项目中设计或维护 API 的案例，说明输入、输出、边界和失败处理。",
        "准备 2 个英文回答：API design trade-off 和 backend service ownership。"
      ],
      "deliverables": [
        "2 个 API 设计面试回答",
        "1 个后端服务 STAR 项目故事"
      ],
      "estimated_hours": 2.0
    },
    {
      "day": 7,
      "title": "Mock Interview and Final Review",
      "focus": [
        "API 设计与后端服务实现",
        "数据库设计、索引和性能优化",
        "部署、云服务和 DevOps 基础",
        "系统设计与可扩展架构"
      ],
      "tasks": [
        "进行一轮 30-45 分钟模拟面试：自我介绍、项目深挖、技术基础、行为问题。",
        "检查每个高优先级主题是否都有一个真实项目证据或诚实的学习计划。",
        "复盘回答中过度夸大、缺少数字、缺少技术细节的地方。"
      ],
      "deliverables": [
        "1 份 2 分钟英文自我介绍",
        "3 个项目深挖答案",
        "1 份最后修改清单"
      ],
      "estimated_hours": 2.0
    }
  ],
  "final_checklist": [
    "每个 JD 核心技能至少对应一个简历或项目证据。",
    "每个缺失技能都有诚实表述：补项目证据、写 familiar，或放入学习计划。",
    "至少准备 3 个 STAR 项目故事：后端实现、问题排查、结果影响。",
    "所有简历修改都需要人工审核，不能编造经历或夸大熟练度。"
  ],
  "human_review_notice": "This interview plan is generated for preparation purposes. Verify every resume claim and project story before using it in real applications."
}

---

# 7. Human Review Notice

This report is generated for drafting and preparation purposes.
Please review all resume suggestions manually before using them in real applications.