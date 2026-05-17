# CareerPilot Agent Dev Log

## 2026-05-11 Day 1

### 今日目标
- 跑通 OpenHarness CLI。
- 配置模型 provider。
- 阅读 OpenHarness 核心目录结构。
- 建立 CareerPilot 开发分支。
- 画出第一版架构理解图。

### 完成内容
- [x] 使用 WSL + uv 搭建开发环境。
- [x] 成功执行 `uv run oh --help`。
- [x] 完成 OpenAI-compatible provider 配置。
- [x] 使用 DeepSeek `deepseek-v4-flash` 作为轻量开发模型。
- [x] 修复 WSL 到 DeepSeek API 的网络连通性问题。
- [x] 成功执行 `uv run oh -p "Say hello in one sentence."`。
- [x] 成功执行 `uv run oh -p "Explain this repository in 5 bullet points"`。
- [x] 成功执行 `uv run oh --dry-run -p "Explain this repository in 5 bullet points"`。
- [x] 成功执行 `uv run pytest -q`。
- [x] 测试结果：`1049 passed, 6 skipped`。

### 遇到问题
- WSL 初始环境缺少 pip，已通过安装基础 Python 工具和 uv 解决。
- 首次模型调用出现 `API error: Request timed out`。
- 排查发现 WSL 未正常访问 HTTPS 外网，`curl https://api.deepseek.com`、GitHub、Baidu 均超时。
- 启动 VPN 后，`curl -I https://api.deepseek.com` 返回 `HTTP/2 401`，说明网络连通，401 是未携带 API key 的正常响应。
- 首次运行 `uv run pytest -q` 报错：`Failed to spawn: pytest, Permission denied (os error 13)`。
- 使用 `uv run python -m pytest -q` 验证后发现缺少 `pytest`。
- 安装 `pytest` 后继续缺少 `pytest_asyncio`。
- 通过 `uv add --dev pytest` 和 `uv add --dev pytest-asyncio` 补齐测试依赖后，测试通过。

### 技术决策
- 使用 WSL + uv 管理项目环境。
- 不使用 conda 作为主项目环境，避免和 uv/pyproject 工作流混用。
- 使用 DeepSeek `deepseek-v4-flash` 作为 Day 1 轻量模型。
- CareerPilot 半月版先作为 OpenHarness 上层扩展模块开发，不改底层 agent loop。
- 对 OpenHarness 的修改先集中在上层 `careerpilot/` 模块、skills、docs 和 examples 中。

### 当前配置记录
```text
profile: openrouter
provider: deepseek
api_format: openai
model: deepseek-v4-flash
base_url: https://api.deepseek.com
User Prompt
   |
   v
oh CLI / TUI
   |
   v
OpenHarness Runtime
   |
   +--> Model Provider
   +--> Tools
   +--> Skills
   +--> Memory
   +--> Permissions / Plugins / MCP
   |
   v
Response / Tool Execution Result
uv run oh -p "Explain this repository in 5 bullet points"
# success

uv run oh --dry-run -p "Explain this repository in 5 bullet points"
# success

uv run pytest -q
# 1049 passed, 6 skipped
明日计划
新建 careerpilot/skills/。
编写 career-coach.md。
编写 resume-rewriter.md。
编写 interview-prep.md。

## 2026-05-12 Day 2

### 今日目标
- 定义 CareerPilot 的核心 Skill 工作流。
- 新建 `careerpilot/skills/career-coach.md`。
- 新建 `careerpilot/skills/resume-rewriter.md`。
- 新建 `careerpilot/skills/interview-prep.md`。
- 明确每个 Skill 的使用场景、输入、输出、流程和边界。

### 完成内容
- [x] 创建 `careerpilot/skills/` 目录。
- [x] 创建 `career-coach.md`，定义 CareerPilot 求职智能体总工作流。
- [x] 创建 `resume-rewriter.md`，定义简历重写和 JD 定制流程。
- [x] 创建 `interview-prep.md`，定义面试准备计划生成流程。
- [x] 检查 3 个 Skill 文件的 frontmatter 和基础内容。

### Skill 设计说明

```text
career-coach
  总入口 Skill，负责完整求职流程：
  JD 分析 -> 简历匹配 -> 项目经历重写 -> 面试准备 -> 投递记录。

resume-rewriter
  简历改写 Skill，负责根据目标岗位重写简历 bullet、项目经历和关键词表达。

interview-prep
  面试准备 Skill，负责根据 JD 和简历缺口生成 3 天或 7 天准备计划、项目故事和模拟问题。

技术决策
Skill 先使用 Markdown 文件定义，便于和 OpenHarness 的 Skill 机制对齐。
Day 2 只沉淀领域工作流，不实现 Python Tool。
Skill 输出强调结构化、可解释和可人工审核。
Resume 相关输出必须避免夸大经历，所有生成内容都作为 draft。
Application tracking 只在用户明确要求时写入，避免默认修改状态文件。
遇到问题
追加 Day 2 日志时，曾在 EOF 结束后误把 Markdown 内容粘贴到 shell，导致出现 command not found。
通过 Python 脚本重新整理 docs/dev_log.md，删除残缺 Day 2 段落并追加干净版本。
明日计划
实现 careerpilot/tools/jd_analyzer.py。
准备 examples/sample_jd_backend.md。
准备 examples/output_jd_analysis.json。
为 JD Analyzer 编写基础测试。


### Day 2 额外检查
- 执行 `uv run oh --dry-run -p "Use career-coach skill to explain the CareerPilot workflow."`
- dry-run 结果：`level: ready`
- Provider 配置正常：`provider: deepseek`，`api_format: openai`，`model: deepseek-v4-flash`
- 当前 OpenHarness discovery 发现默认 Skills 数量为 10，尚未发现 `careerpilot/skills/` 下的 CareerPilot Skills。
- 结论：这是预期结果。Day 2 只完成 Skill 草稿，Skill discovery 集成放到 Day 8。
## 2026-05-12 Day 3 - JD Analyzer Tool

### 今日目标

今天的目标是实现 CareerPilot Agent 的第一个核心自定义工具：`JD Analyzer Tool`。

该工具用于接收一段岗位 JD 文本，并输出结构化岗位分析结果，包括：

- 岗位一句话总结
- 岗位等级判断：junior / mid / senior / unknown
- 核心技能要求
- 加分技能要求
- 岗位职责
- 简历关键词
- 面试关注点
- 风险提示

Day 3 的重点不是追求语义理解完全准确，而是先建立一个稳定、可测试、可复用的工具模块，为 Day 4 的 Resume Matcher Tool 提供输入基础。

---

### 完成内容

#### 1. 新增 JD Analyzer 工具

新增文件：

```text
careerpilot/tools/jd_analyzer.py

实现内容包括：

使用 Pydantic 定义输入 schema：JDAnalysisInput
使用 Pydantic 定义输出 schema：JDAnalysisOutput
定义岗位等级枚举：SeniorityLevel
实现 deterministic parser 版本的 JD 分析逻辑
支持从 JD 中抽取技术关键词
支持推断岗位 seniority level
支持抽取职责类别
支持区分 core skills 和 nice-to-have skills
支持生成 interview focus 和 risk notes
支持通过 python -m careerpilot.tools.jd_analyzer 直接运行

主要输出字段：

{
  "role_summary": "...",
  "seniority_level": "...",
  "core_skills": [],
  "nice_to_have_skills": [],
  "responsibilities": [],
  "keywords_for_resume": [],
  "interview_focus": [],
  "risk_notes": []
}
2. 新增样例 JD 和样例输出

由于当前项目是在 OpenHarness fork 内开发，为避免和 OpenHarness 原有 examples 混在一起，最终采用项目级子目录：

examples/careerpilot/

新增文件：

examples/careerpilot/sample_jd_backend.md
examples/careerpilot/output_jd_analysis.json

其中：

sample_jd_backend.md 保存后端工程师岗位 JD 样例
output_jd_analysis.json 保存 JD Analyzer 的结构化输出结果

生成样例输出命令：

python -m careerpilot.tools.jd_analyzer > examples/careerpilot/output_jd_analysis.json

JSON 格式校验命令：

python -m json.tool examples/careerpilot/output_jd_analysis.json > /tmp/jd_check.json

校验结果：通过，输出 JSON 格式合法。

3. 新增单元测试

新增文件：

tests/careerpilot/test_jd_analyzer.py

测试覆盖内容：

后端岗位 JD 的核心技能抽取
岗位等级识别
nice-to-have 技能识别
空 JD 输入异常处理
AI Agent / LLM / RAG 相关关键词抽取

测试命令：

python -m pytest -q tests/careerpilot/test_jd_analyzer.py

最终测试结果：

3 passed in 0.02s
今日最终文件结构

Day 3 完成后，新增或更新的核心文件如下：

careerpilot/
  __init__.py
  tools/
    __init__.py
    jd_analyzer.py

examples/
  careerpilot/
    sample_jd_backend.md
    output_jd_analysis.json

tests/
  careerpilot/
    test_jd_analyzer.py
关键技术实现
1. Deterministic Parser

Day 3 暂时没有直接接入 LLM，而是先实现规则解析版本。

原因：

输出稳定，方便测试
demo 不容易因为模型输出漂移而失败
下游 Resume Matcher 可以依赖固定 schema
后续可以在规则解析基础上加入 LLM refinement

当前实现基于关键词表和规则进行抽取，例如：

技术关键词：Python、FastAPI、PostgreSQL、Redis、Docker、Kubernetes、AWS、REST API、LLM、Agent、RAG
职责关键词：后端服务、API、数据库、部署、协作、分布式系统
等级关键词：junior、mid、senior、3+ years、5+ years 等
2. Pydantic Schema

使用 Pydantic 定义输入输出结构，保证工具输出字段稳定。

输入 schema：

class JDAnalysisInput(BaseModel):
    job_description: str
    target_role: Optional[str] = "Unknown Role"
    language: Optional[str] = "zh-CN"

输出 schema：

class JDAnalysisOutput(BaseModel):
    role_summary: str
    seniority_level: SeniorityLevel
    core_skills: List[str]
    nice_to_have_skills: List[str]
    responsibilities: List[str]
    keywords_for_resume: List[str]
    interview_focus: List[str]
    risk_notes: List[str]

这个设计方便后续 Resume Matcher Tool 直接复用 JD Analyzer 的输出结果。

3. Nice-to-have 分类逻辑优化

最初版本使用技能前后固定长度上下文判断是否包含 nice to have、preferred、plus 等标记。

问题：

当 JD 中出现一句 Kubernetes and AWS are nice to have.
前面同一段落中的 Python、FastAPI、PostgreSQL、Redis、Docker 也可能被误判为 nice-to-have
导致 core_skills 为空，测试失败

修复方式：

改为按行和句子切分 JD
判断每个技能所在的具体 segment 是否属于 nice-to-have
如果一个技能同时出现在核心要求和 nice-to-have 中，优先归为 core skill
支持 Nice to have: 这种 section header

修复后结果：

core: ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'REST API']
nice: ['Kubernetes', 'AWS']
level: SeniorityLevel.mid
遇到的问题与解决方案
问题 1：f-string 语法错误

运行命令时出现错误：

SyntaxError: f-string expression part cannot include a backslash

原因：

return f" {text.lower().replace('\\n', ' ')} "

Python 3.10 不允许 f-string 表达式中直接包含反斜杠。

解决方案：

def _normalize_text(text: str) -> str:
    normalized = text.lower().replace("\n", " ")
    return f" {normalized} "
问题 2：样例文件路径不一致

最初代码读取路径：

examples/careerpilot/sample_jd_backend.md

但文件实际放在：

careerpilot/examples/sample_jd_backend.md

导致错误：

FileNotFoundError: [Errno 2] No such file or directory

解决方案：

将样例统一移动到项目级 examples 子目录：

examples/careerpilot/

并删除错误遗留目录：

rm -rf careerpilot/examples

最终采用的运行方式：

python -m careerpilot.tools.jd_analyzer > examples/careerpilot/output_jd_analysis.json
问题 3：pytest 中 core_skills 为空

测试失败信息：

AssertionError: assert 'Python' in []

排查过程：

先用 debug 脚本确认 _find_skills() 是否正常工作。

debug 结果显示：

skills: ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'REST API']
core: []
nice: ['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'Kubernetes', 'AWS', 'REST API']
level: SeniorityLevel.mid

结论：

技能抽取本身是正常的
问题出在 _split_core_and_nice_to_have()
nice-to-have 判断范围太宽，导致所有技能都被归入 nice-to-have

解决方案：

重写 nice-to-have 分类逻辑，按句子和 section 判断，而不是用固定字符窗口。

修复后测试通过：

3 passed in 0.02s
今日验证命令

今天最终通过的关键命令如下：

python -m careerpilot.tools.jd_analyzer
python -m careerpilot.tools.jd_analyzer > examples/careerpilot/output_jd_analysis.json
python -m json.tool examples/careerpilot/output_jd_analysis.json > /tmp/jd_check.json
python -m pytest -q tests/careerpilot/test_jd_analyzer.py

最终测试结果：

3 passed in 0.02s
Git 提交记录

今日相关提交：

7298147 Add CareerPilot JD analyzer tool

同时也提交了学习笔记：

b5ce0e8 Add skill learning notes

当前分支：

feature/careerpilot-agent

最近提交记录：

b5ce0e8 Add skill learning notes
7298147 Add CareerPilot JD analyzer tool
9bbd1cf docs: record CareerPilot skill dry-run check
63b6983 feat: add CareerPilot skill drafts
1929ad8 feat(ohmo): add agent-turn cron delivery (#247)
技术决策记录
决策 1：Day 3 先不用 LLM

虽然后续可以加入 LLM 结构化输出，但 Day 3 先使用 deterministic parser。

原因：

半月版优先保证稳定可演示
单元测试更容易写
输出 schema 更可控
后续 Resume Matcher 可以直接依赖当前输出
决策 2：CareerPilot examples 使用 examples/careerpilot/

由于当前项目是在 OpenHarness 仓库中扩展，OpenHarness 原项目已有自己的 examples/ 目录。

因此 CareerPilot 的样例统一放在：

examples/careerpilot/

而不是：

careerpilot/examples/

这样可以让样例属于整个项目的 demo assets，同时避免和 OpenHarness 原有 examples 混淆。

决策 3：测试路径使用 tests/careerpilot/

为了避免和 OpenHarness 原有测试混在一起，CareerPilot 的测试统一放在：

tests/careerpilot/

这样后续可以单独运行 CareerPilot 测试：

python -m pytest -q tests/careerpilot/
当前限制

当前 JD Analyzer 仍然是规则解析版本，存在以下限制：

复杂 JD 的隐含要求可能无法识别
技能词表需要持续扩充
同义词和上下文理解能力有限
对中文 JD 的覆盖还需要加强
nice-to-have 判断已经改进，但仍可能在复杂格式下误判
当前正式样例文件只有一个，后续可以补充 AI Agent JD 或 ML Engineer JD 样例

这些限制可以在后续版本中通过 LLM refinement、更多样例和 benchmark 来改进。

今日收获

今天完成了 CareerPilot 的第一个真正可运行工具模块。

主要收获：

明确了 Tool schema 设计方式
完成了 Pydantic 输入输出建模
理解了 deterministic parser 在 demo 和测试中的价值
解决了 Python 模块路径和样例路径问题
通过 pytest 建立了最小测试闭环
为 Day 4 Resume Matcher 提供了稳定输入基础
明日计划：Day 4 Resume Matcher Tool

明天开始实现：

careerpilot/tools/resume_matcher.py
examples/careerpilot/sample_resume.md
examples/careerpilot/output_resume_match.json
tests/careerpilot/test_resume_matcher.py

Day 4 目标：

输入简历文本和 JD Analyzer 输出
计算简历与岗位的匹配分
输出 strong matches
输出 missing skills
输出 weak evidence
输出 resume keywords to add
输出 rewrite suggestions
输出 interview preparation topics

评分逻辑初步采用可解释规则：

match_score = 技术关键词覆盖 * 0.45
            + 项目证据覆盖 * 0.35
            + 岗位职责覆盖 * 0.20

Day 4 的重点是让 JD Analyzer 的输出真正进入下游流程，形成：

JD -> JD Analysis -> Resume Matching

这是 CareerPilot 求职闭环的第二步。

## Day 4：Resume Matcher Tool

### 今日目标
实现简历与 JD 分析结果的匹配工具。

### 完成内容
- 新建 `careerpilot/tools/resume_matcher.py`
- 定义 `ResumeMatchInput`、`ResumeMatchOutput`、`RewriteSuggestion`
- 实现基于关键词覆盖、项目证据覆盖、职责覆盖的可解释匹配分
- 新建 `tests/test_resume_matcher.py`
- 测试通过：`2 passed`
- 新建 `examples/sample_resume.md`
- 生成 `examples/careerpilot/output_resume_match.md`

### 验收结果
- 可以输出 `match_score`
- 可以识别 `strong_matches`
- 可以识别 `missing_skills`
- 可以生成 `rewrite_suggestions`
- 可以生成 `interview_preparation_topics`

### 备注
当前版本是 deterministic matcher，不依赖 LLM。后续可接入模型增强 rewrite quality，但保留 schema validation 和规则评分逻辑。
## 2026-05-17 Day 5

### 今日目标
- 实现 Project Story Extractor。
- 将项目 README / 项目说明转化为简历项目经历、面试故事和潜在面试问题。
- 保证输出结构稳定，便于后续 demo、测试和 README 展示。

### 完成内容
- 新增 `careerpilot/tools/project_story_extractor.py`。
- 使用 Pydantic 定义输入输出结构：
  - `ProjectStoryInput`
  - `ProjectStoryOutput`
  - `InterviewStory`
- 实现规则版项目经历提炼逻辑：
  - 提取项目一句话总结 `one_liner`
  - 识别技术栈 `tech_stack`
  - 生成架构亮点 `architecture_highlights`
  - 生成中文简历 bullet `resume_bullets_cn`
  - 生成英文简历 bullet `resume_bullets_en`
  - 生成面试故事 `interview_story`
  - 生成可能面试问题 `possible_interview_questions`
- 新增样例项目说明文件：
  - `examples/sample_project_readme.md`
- 新增输出样例文件：
  - `examples/output_project_bullets.md`
- 新增测试文件：
  - `tests/test_project_story_extractor.py`
- 验证 `project_story_extractor.py` 可以独立运行并输出结构化 JSON。

### 验证结果
执行命令：

```bash
python careerpilot/tools/project_story_extractor.py
运行成功，输出包含以下核心字段：

one_liner
tech_stack
architecture_highlights
resume_bullets_cn
resume_bullets_en
interview_story
possible_interview_questions

其中中文 bullet、英文 bullet、面试故事和面试问题均正常生成，满足 Day 5 验收标准。
技术决策
当前版本优先使用规则化关键词识别和模板化生成，而不是直接依赖 LLM。
原因：
输出更稳定，方便单元测试。
demo 时不依赖模型 API，降低运行失败风险。
后续可以在规则版基础上接入 LLM 作为增强层。
使用 Pydantic schema 固定输入输出字段，便于后续接入 OpenHarness workflow 和端到端 demo。
遇到问题
当前技术栈识别依赖关键词匹配，如果输入样例中没有显式写出 Python、Pydantic 等关键词，输出中可能不会出现这些技术。
后续可以通过改进样例 README 或扩展关键词映射表，让识别结果更完整。
面试讲法

今天实现的是 CareerPilot 的 Project Story Extractor。它的作用是把项目 README 或项目说明转化成可以直接用于简历和面试表达的结构化内容。相比直接让模型自由生成，我先用 Pydantic 固定 schema，再用规则和模板生成稳定输出，这样可以保证结果可测试、可复现，也方便后续接入 OpenHarness 的工具调用和端到端求职流程。
简历 bullet 草稿

中文：

实现 Project Story Extractor 工具，基于 Pydantic schema 和规则化关键词识别，将项目 README 自动转化为中英文简历 bullet、架构亮点、STAR 面试故事和潜在面试问题，提升项目经历包装效率与输出稳定性。

英文：

Implemented a Project Story Extractor with Pydantic schemas and deterministic keyword extraction, converting README-style project descriptions into bilingual resume bullets, architecture highlights, STAR-style interview stories, and likely interview questions.
明日计划
实现 Application Tracker。
使用本地 JSON 文件保存投递记录。
支持新增申请、更新状态、查询待办和生成今日求职任务清单。

