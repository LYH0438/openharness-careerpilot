# CareerPilot Day 2 学习笔记：如何设计 Skill 文件

## 1. 今天完成了什么

Day 2 的核心任务是为 CareerPilot Agent 设计 3 个领域 Skill：

```text
careerpilot/skills/career-coach.md
careerpilot/skills/resume-rewriter.md
careerpilot/skills/interview-prep.md
这 3 个文件不是普通说明文档，而是给 Agent 使用的“领域工作流说明”。

它们的作用是告诉 Agent：

什么时候使用这个能力
输入可能有哪些
应该输出什么
应该按照什么步骤思考和执行
有哪些边界不能越过

当前 3 个 Skill 的职责如下：

career-coach
  CareerPilot 的总入口 Skill，负责完整求职流程：
  JD 分析 -> 简历匹配 -> 项目经历重写 -> 面试准备 -> 投递记录。

resume-rewriter
  简历改写 Skill，负责根据目标岗位优化简历 bullet、项目经历和关键词表达。

interview-prep
  面试准备 Skill，负责根据 JD 和简历缺口生成 3 天或 7 天准备计划、项目故事和模拟问题。
2. 什么是 Skill

在 OpenHarness / Agent 项目中，Skill 可以理解为：

一份用 Markdown 写成的领域工作流说明，让 Agent 在特定场景下知道如何完成任务。

Skill 不是 Python 函数，也不是具体工具调用。

它更像是：

Prompt + Workflow + Domain Rules + Safety Boundary

普通 prompt 通常只是一段临时指令，例如：

帮我优化简历。

而 Skill 是可复用的工作流，例如：

当用户要求简历优化时：
1. 先识别目标岗位。
2. 再解析 JD 关键词。
3. 再找简历中的证据。
4. 然后生成 before/after 修改建议。
5. 最后提醒用户人工审核，不能编造经历。

所以 Skill 的价值是：
它把一次性的聊天提示，变成了可复用、可解释、可维护的 Agent 行为规范。

3. Skill 和 Tool 的区别

CareerPilot 中会同时有 Skill 和 Tool。

二者区别如下：

对比项	Skill	Tool
本质	Markdown 工作流说明	Python 可执行代码
作用	告诉 Agent 怎么做	真正执行某个具体任务
示例	career-coach.md	jd_analyzer.py
是否直接运行	不直接运行	可以被调用执行
适合表达	流程、规则、边界、输出风格	解析、计算、文件读写、JSON 处理
面试讲法	领域工作流抽象	工具调用能力实现

在 CareerPilot 中，比较理想的结构是：

Skill 负责规划和编排：
  career-coach.md

Tool 负责具体执行：
  jd_analyzer.py
  resume_matcher.py
  project_story_extractor.py
  application_tracker.py

例如：

用户输入 JD 和简历
   |
   v
career-coach Skill 判断任务流程
   |
   +--> 调用 JD Analyzer Tool
   +--> 调用 Resume Matcher Tool
   +--> 调用 Interview Prep 逻辑
   |
   v
生成最终求职报告
4. 一个 Skill 文件的基本结构

一个 Skill Markdown 一般包含两部分：

---
name: skill-name
description: What this skill does.
---

# Skill Title

## When to use

## Goal

## Inputs

## Workflow

## Output Format

## Rules / Safety Boundaries
4.1 Frontmatter

文件最上面的部分叫 frontmatter：

---
name: career-coach
description: Analyze job descriptions, match resumes, rewrite project experience, generate interview preparation plans, and manage job application workflow.
---

它的作用是让框架或 Agent 快速理解这个 Skill 是什么。

其中：

name
  Skill 的唯一名称，应该短、清楚、可被引用。

description
  Skill 的一句话说明，应该描述能力边界和适用场景。

为什么这里用英文？

主要原因：

很多 Agent 框架和模型对英文 skill description 的检索效果更稳定。
后续如果接入 OpenHarness skill discovery，英文描述更适合做匹配。
项目放到简历和 GitHub 时，英文说明更通用。

但 Skill 正文完全可以写成中英双语。后续可以优化成 bilingual version。

5. 如何写好一个 Skill

写 Skill 时不要只写“你是一个简历助手”。

差的写法：

你是一个简历优化专家，请帮用户优化简历。

这个太泛，不像工程项目。

好的 Skill 应该写清楚：

1. 什么时候使用
2. 输入是什么
3. 目标是什么
4. 按什么步骤做
5. 输出什么格式
6. 有什么禁止事项

例如 resume-rewriter 的核心逻辑应该是：

When to use:
  用户要求重写简历、优化 bullet、针对 JD 修改简历时使用。

Inputs:
  原始简历、目标 JD、目标岗位、项目说明、输出语言。

Workflow:
  先提取 JD 要求，再定位简历证据，再重写 bullet。

Rules:
  不编造经历，不添加没有用过的技术，不伪造指标。

这才是一个可复用的 Skill。

6. 为什么 CareerPilot 需要 3 个 Skill

如果只写一个大 Skill，所有事情都塞进 career-coach.md，会导致职责不清晰。

所以 Day 2 拆成了 3 个 Skill：

career-coach
  负责总流程。

resume-rewriter
  负责简历重写。

interview-prep
  负责面试准备。

这种拆法有几个好处：

职责清楚。
后续更容易接入对应 Tool。
面试时更容易讲架构。
可以逐步扩展成多 Agent 工作流。
不同 Skill 可以单独测试和优化。
7. career-coach.md 学习笔记
7.1 它的定位

career-coach.md 是 CareerPilot 的主 Skill。

它不是只做简历修改，而是负责完整求职流程：

JD 分析
  -> 简历匹配
  -> 项目经历重写
  -> 面试准备
  -> 投递状态记录
7.2 为什么它是主 Skill

因为用户通常不会一开始说：

请调用 jd_analyzer.py。

用户更可能说：

这是一个后端岗位 JD，帮我看看我适不适合。

这时 Agent 需要先理解用户想完成的是一个求职分析任务，然后选择正确流程。

career-coach.md 就是用来定义这个总流程的。

7.3 它的核心内容

它主要包含：

When to use:
  JD 分析、简历匹配、项目经历重写、面试准备、投递管理。

Inputs:
  岗位、公司、JD、简历、项目 README、用户画像、投递状态。

Outputs:
  JD 分析报告、简历匹配报告、缺口分析、简历关键词、项目 bullet、面试计划。

Workflow:
  先理解岗位，再分析 JD，再匹配简历，再生成改写建议和面试计划。

Safety:
  不自动投递、不填写敏感信息、不编造经历、不擅自改文件。
7.4 面试讲法

可以这样讲：

我把 CareerPilot 的主流程抽象成了 career-coach Skill。它不是一个简单 prompt，而是一个可复用的求职工作流定义。它规定了从 JD 分析、简历匹配、项目经历重写，到面试准备和投递记录的完整流程。这样 Agent 在面对不同求职请求时，不是随机回答，而是按照固定的领域流程执行。

8. resume-rewriter.md 学习笔记
8.1 它的定位

resume-rewriter.md 专门负责简历内容优化。

它的重点不是“写得更好听”，而是：

根据目标 JD，把已有经历改写得更匹配，同时不编造事实。
8.2 为什么单独拆出来

简历重写是一个高风险任务，因为很容易出现：

- 编造不存在的技术
- 夸大项目影响
- 伪造量化指标
- 把学习经历写成生产经验

所以它需要单独的规则和边界。

8.3 它的核心内容
When to use:
  用户要求优化简历、改写 bullet、针对 JD 定制简历时。

Inputs:
  原简历、目标 JD、目标岗位、项目 README、语言偏好。

Workflow:
  提取 JD 要求 -> 找简历证据 -> 识别弱 bullet -> 重写 -> 人工审核。

Output:
  改写策略、关键词、before/after、最终 bullet、人工审核 checklist。

Rules:
  不编造指标，不添加没用过的技术，不夸大熟练度。
8.4 Bullet 模板

中文模板：

基于 [技术/框架] 实现 [功能/系统]，通过 [方法] 解决 [问题]，提升/缩短/支持 [结果]。

英文模板：

Built [system/feature] using [technology], enabling [capability] and improving [metric/result].
8.5 面试讲法

可以这样讲：

我把简历重写单独拆成了 resume-rewriter Skill，因为简历生成涉及事实准确性和诚信边界。这个 Skill 要求 Agent 先从 JD 中提取目标能力，再从用户简历或项目说明中寻找证据，只有有证据支持的内容才能写入 bullet。同时它要求所有生成内容都作为 draft，需要人工审核，避免 Agent 编造经历或指标。

9. interview-prep.md 学习笔记
9.1 它的定位

interview-prep.md 负责根据 JD 和简历缺口生成面试准备计划。

它关注的是：

用户应该复习什么？
应该准备哪些项目故事？
可能被问哪些问题？
每天应该产出什么？
9.2 为什么需要它

CareerPilot 的目标不是只帮用户改简历，而是形成求职闭环。

如果只做 JD 分析和简历匹配，流程还不完整。

面试准备计划可以把“缺口分析”变成“行动计划”。

例如：

缺少 Docker / CI/CD 经验
  -> 面试计划中安排一天复习部署流程
  -> 准备一个 honest framing 的回答
9.3 它的核心内容
When to use:
  用户要求准备面试、生成 3 天或 7 天计划、预测面试题时。

Inputs:
  JD 分析报告、简历匹配报告、目标岗位、可用天数、每天学习时间。

Workflow:
  找面试重点 -> 区分强项和短板 -> 按优先级排计划 -> 生成每日任务和产出。

Output:
  面试重点、优先复习主题、每日计划、项目故事、模拟问题、最终 checklist。

Rules:
  计划要现实，优先补 JD 强相关短板，不鼓励伪造经验。
9.4 面试讲法

可以这样讲：

interview-prep Skill 的作用是把前面 JD Analyzer 和 Resume Matcher 的结果转化成具体行动。它会根据岗位要求和简历缺口生成 3 天或 7 天计划，每天包含学习任务、练习任务和明确产出物。这样 CareerPilot 不只是分析工具，而是能帮助用户完成从岗位理解到面试准备的闭环。

10. 为什么 Skill 要写规则和禁止事项

Agent 项目不是只要能输出内容就可以，还要有边界。

CareerPilot 涉及求职和简历，所以必须特别注意：

不能编造经历。
不能自动投递真实岗位。
不能随便填写敏感信息。
不能把不熟悉的技能写成熟练掌握。
不能擅自修改用户文件。

这些规则体现的是 Agent 的安全性和可信度。

面试时可以强调：

我在 Skill 中显式写了 safety boundaries，因为求职智能体涉及简历真实性和个人信息。相比普通 prompt demo，我更关注可控性、可解释性和 human-in-the-loop。

11. Skill 文件为什么目前还没有被 OpenHarness 自动发现

Day 2 中我们把 Skill 文件放在：

careerpilot/skills/

但是 dry-run 结果显示 OpenHarness 当前只发现了默认 Skills，没有发现 career-coach。

这是正常的。

原因是：

Day 2 目标：
  写出 CareerPilot 的领域 Skill 草稿。

Day 8 目标：
  研究 OpenHarness Skill 加载路径，并把 CareerPilot Skill 接入 OpenHarness discovery。

所以当前阶段不要求 OpenHarness 自动加载这 3 个 Skill。

后续 Day 8 要解决的问题是：

1. OpenHarness 默认从哪些目录加载 Skill？
2. 是否需要复制到 .claude/skills 或其他默认目录？
3. 是否需要通过 plugin 或配置注册？
4. 如何用 oh -p 触发 career-coach workflow？
12. 我后续如何自己写一个 Skill

可以按这个模板写：

---
name: skill-name
description: One sentence explaining when and why this skill should be used.
---

# Skill Title

## When to use

Use this skill when the user asks to:

- ...
- ...
- ...

## Goal

Explain the final outcome this skill should help produce.

## Inputs

- Input 1
- Input 2
- Input 3

## Workflow

1. Step one.
2. Step two.
3. Step three.
4. Step four.

## Output Format

Return:

- Section 1
- Section 2
- Section 3

## Rules

- Do not ...
- Always ...
- Prefer ...

写 Skill 时可以问自己 6 个问题：

1. 这个 Skill 解决什么问题？
2. 用户什么情况下会触发它？
3. 它需要哪些输入？
4. 它应该输出什么？
5. 它应该按什么步骤做？
6. 它绝对不能做什么？

如果这 6 个问题都回答清楚，这个 Skill 就比较像工程项目里的工作流，而不是普通 prompt。

13. 这 3 个 Skill 在项目架构中的位置

CareerPilot 半月版的架构可以理解为：

User Input
   |
   v
OpenHarness CLI
   |
   v
CareerPilot Skills
   |
   +--> career-coach
   |      负责总流程编排
   |
   +--> resume-rewriter
   |      负责简历优化逻辑
   |
   +--> interview-prep
          负责面试准备计划
   |
   v
CareerPilot Tools
   |
   +--> jd_analyzer.py
   +--> resume_matcher.py
   +--> project_story_extractor.py
   +--> application_tracker.py
   |
   v
Structured Report / Memory Update

Day 2 只完成了 Skill 层。

Day 3 开始进入 Tool 层。

14. 面试时可以怎么讲 Day 2
30 秒版本

我在 Day 2 主要做了 CareerPilot 的 Skill 设计，把求职场景拆成了 3 个可复用工作流：career-coach 作为总入口，负责 JD 分析到面试准备的完整流程；resume-rewriter 专注简历重写，并加入不编造经历的安全边界；interview-prep 负责根据 JD 和简历缺口生成准备计划。这些 Skill 是后续 Tool 调用和 Agent 编排的上层逻辑。

1 分钟版本

CareerPilot 不是一个简单的 prompt 工具，所以我先用 Markdown Skill 把领域工作流沉淀下来。career-coach 定义完整求职流程，包括 JD 分析、简历匹配、项目经历重写、面试准备和投递记录；resume-rewriter 定义简历 bullet 改写规则，强调必须基于证据，不能编造指标和技术；interview-prep 把岗位要求和简历缺口转化成 3 天或 7 天行动计划。这样做的好处是，Agent 的行为不是随机聊天，而是有明确流程、输入输出和安全边界。

2 分钟版本

Day 2 我没有直接写 Python 工具，而是先做 Skill 层设计。原因是 Agent 项目需要先明确任务边界和工作流，否则后面工具会变成零散函数。我的设计是把 CareerPilot 拆成 3 个 Skill。第一个是 career-coach，它是总入口，负责从 JD 到简历匹配、项目故事、面试准备和投递状态的闭环。第二个是 resume-rewriter，它专注简历定制，要求先从 JD 提取关键词，再从简历中寻找证据，只能基于已有事实生成 bullet。第三个是 interview-prep，它根据岗位要求和简历短板生成准备计划，每天都有学习任务、练习任务和产出物。这个设计体现了 Skill 和 Tool 的分层：Skill 负责领域流程，Tool 负责具体执行。后续我会用 jd_analyzer.py、resume_matcher.py 等工具承接这些 Skill 中定义的步骤。

15. 今日复盘

今天我学到：

1. Skill 是 Agent 的领域工作流说明，不是普通文档。
2. 一个好的 Skill 必须包含使用场景、输入、输出、流程和边界。
3. Skill 负责告诉 Agent 怎么做，Tool 负责真正执行。
4. CareerPilot 的 3 个 Skill 分别覆盖总流程、简历重写和面试准备。
5. 简历相关 Agent 必须特别注意真实性和人工审核。
6. 当前 Skill 还没有接入 OpenHarness discovery，这是 Day 8 的任务。

下一步 Day 3：

实现 JD Analyzer Tool：
careerpilot/tools/jd_analyzer.py

