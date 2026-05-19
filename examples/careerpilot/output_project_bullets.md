{
  "one_liner": "基于 OpenHarness 构建的面向 AI Agent Engineer 求职流程智能体",
  "tech_stack": [
    "OpenHarness",
    "Agent",
    "Skill",
    "Memory",
    "CLI",
    "JSON",
    "pytest"
  ],
  "architecture_highlights": [
    "自定义 Tool 抽象，用于封装 JD 分析、简历匹配和项目经历提炼能力",
    "Skill 驱动的领域工作流，将求职流程拆分为可复用步骤",
    "本地 Memory 记录投递状态、用户画像和结构化分析结果",
    "CLI / demo script 支持端到端求职流程演示",
    "使用测试覆盖核心工具逻辑，提升输出稳定性"
  ],
  "resume_bullets_cn": [
    "基于 OpenHarness、Agent、Skill、Memory 构建面向 AI Agent Engineer 的项目经历提炼工具，将项目 README/说明文档结构化转化为中英文简历 bullet、STAR 面试故事和潜在面试问题，提升求职材料复用效率和表达一致性。",
    "设计覆盖项目一句话总结、技术栈、架构亮点、简历表述和面试故事的结构化输出 schema，通过稳定字段支持端到端 demo、单元测试和后续 OpenHarness workflow 编排。",
    "围绕自定义 Tool 抽象实现规则化关键词识别与模板化生成逻辑，将 JD 分析、简历匹配和项目经历提炼能力封装为可测试模块，降低自由生成带来的不稳定风险，使输出结果更适合简历微调、面试复盘和自动化测试。"
  ],
  "resume_bullets_en": [
    "Built a project story extraction tool for AI Agent Engineer workflows using OpenHarness, Agent, Skill, Memory, transforming README-style project descriptions into bilingual resume bullets, STAR interview stories, and likely interview questions to improve reuse and consistency of job-search materials.",
    "Designed a structured output schema covering project summary, tech stack, architecture highlights, resume-ready bullets, and interview narratives, enabling stable end-to-end demos, unit tests, and future OpenHarness workflow integration.",
    "Implemented deterministic keyword extraction and template-based generation around custom tool abstractions, packaging JD analysis, resume matching, and project story extraction into testable modules while making outputs easier to review, test, and tailor for interviews."
  ],
  "interview_story": {
    "problem": "求职过程中，项目经历往往需要针对不同岗位重新组织表达，手动改写耗时且容易遗漏技术亮点。",
    "solution": "围绕 AI Agent Engineer 场景设计 Project Story Extractor，将项目说明结构化解析为技术栈、架构亮点、简历 bullet 和面试故事。",
    "impact": "在 demo 场景中，可以把项目材料快速转化为可复用的简历和面试表达，减少重复整理成本，并提升输出一致性。"
  },
  "possible_interview_questions": [
    "你为什么要把项目经历提炼单独做成一个 Tool？",
    "这个工具和普通 prompt 生成简历 bullet 有什么区别？",
    "你如何保证输出字段稳定，方便后续测试和 workflow 编排？",
    "你在这个项目里具体使用了 OpenHarness 的哪些能力？",
    "Tool schema 设计时，你如何划分输入、输出和异常情况？"
  ]
}
