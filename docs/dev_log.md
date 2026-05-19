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

## 2026-05-17 Day 6：Application Tracker 与本地 Memory 实现

### 今日目标

Day 6 的目标是为 CareerPilot Agent 增加最小可用的状态管理能力，使智能体不只能够生成岗位分析、简历匹配和项目经历改写结果，还能够记录真实求职流程中的投递状态、下一步动作和备注信息。

本日重点实现：

- 使用本地 JSON 文件作为轻量级 memory。
- 支持新增岗位申请记录。
- 支持更新投递状态。
- 支持查询待办事项。
- 支持生成今日求职任务清单。
- 增加基础异常处理和单元测试。

该模块对应半月计划中的 Day 6：Application Tracker，用于补齐 CareerPilot 的求职闭环状态管理能力。:contentReference[oaicite:0]{index=0}

---

### 完成内容

#### 1. 新增本地 Memory 文件

新增目录和文件：

```text
careerpilot/memory/applications.json
````

该文件用于保存用户的投递记录，初始内容为：

```json
[]
```

它作为 CareerPilot 的最小持久化 memory，用于记录公司、岗位、状态、匹配分、下一步动作和备注。

---

#### 2. 实现 Application Tracker Tool

新增文件：

```text
careerpilot/tools/application_tracker.py
```

实现了以下核心能力：

* `load_applications`

  * 读取本地 JSON memory。
  * 如果文件不存在，自动创建空列表文件。
  * 如果 JSON 格式错误，返回可读错误信息。

* `save_applications`

  * 将投递记录写回 JSON 文件。
  * 使用 `ensure_ascii=False`，保证中文内容可读。

* `add_application`

  * 新增投递记录。
  * 支持公司、岗位、JD 来源、状态、匹配分、下一步动作和备注。
  * 使用 `company + role` 判断重复记录。

* `update_application`

  * 更新已有投递记录。
  * 支持更新状态、匹配分、下一步动作、JD 来源和备注。
  * 每次更新自动刷新 `updated_at`。

* `list_applications`

  * 查询全部投递记录。
  * 支持按状态筛选。

* `get_todos`

  * 查询仍处于活跃状态、且存在下一步动作的记录。

* `generate_today_tasks`

  * 根据当前活跃投递记录生成今日求职任务清单。

---

#### 3. 定义投递状态枚举

当前支持的状态包括：

```text
researching -> preparing -> applied -> interview -> offer -> rejected -> archived
```

其中活跃状态定义为：

```text
researching
preparing
applied
interview
```

这些状态会被用于生成待办事项和今日任务清单。

---

#### 4. 增加 CLI 调用方式

`application_tracker.py` 支持通过命令行直接调用，方便本地 demo 和后续端到端流程集成。

新增记录示例：

```bash
python -m careerpilot.tools.application_tracker add \
  --company "Example AI" \
  --role "AI Agent Engineer" \
  --jd-source "examples/careerpilot/sample_jd_backend.md" \
  --status "preparing" \
  --match-score 78 \
  --next-action "rewrite project bullets" \
  --note "需要补充 MCP 和多 Agent 相关表述"
```

更新状态示例：

```bash
python -m careerpilot.tools.application_tracker update \
  --company "Example AI" \
  --role "AI Agent Engineer" \
  --status "applied" \
  --next-action "prepare backend system design interview answers" \
  --note "已完成第一版简历投递"
```

查询全部记录：

```bash
python -m careerpilot.tools.application_tracker list
```

生成今日任务：

```bash
python -m careerpilot.tools.application_tracker today
```

---

### 测试内容

新增测试文件：

```text
tests/careerpilot/test_application_tracker.py
```

覆盖了以下场景：

1. 新增投递记录。
2. 拒绝重复投递记录。
3. 更新状态和备注。
4. 按状态筛选记录。
5. 查询 active 状态下的待办事项。
6. 生成今日任务清单。
7. 文件不存在时自动创建 memory 文件。
8. JSON 格式错误时抛出可读错误。
9. 非法状态会被拒绝。
10. 非法匹配分会被拒绝。

测试命令：

```bash
python -m pytest -q tests/careerpilot/test_application_tracker.py
```

测试结果：

```text
10 passed
```

同时运行 CareerPilot 当前测试：

```bash
python -m pytest -q tests/careerpilot
```

结果正常。

---

### 今日验收结果

Day 6 的两个核心验收命令均已正常通过：

```bash
python -m pytest -q tests/careerpilot/test_application_tracker.py
```

```bash
python -m careerpilot.tools.application_tracker today
```

说明 Application Tracker 已经具备基本可用能力：

* 可以保存投递记录。
* 可以读取投递记录。
* 可以更新投递状态。
* 可以生成今日任务。
* 可以通过单元测试验证核心逻辑。

---

### 技术决策

#### 1. 使用 JSON 文件而不是数据库

半月版优先保证项目可运行、可解释、可演示，因此暂时不引入 SQLite、PostgreSQL 或 ORM。

选择 JSON 的原因：

* 实现成本低。
* 文件内容可直接查看。
* 方便 demo。
* 适合本地个人智能体的最小 memory。
* 后续可以平滑升级为 SQLite 或向量数据库。

---

#### 2. 使用 `company + role` 判断重复记录

当前版本没有引入唯一 ID，因此用公司名和岗位名共同判断一条投递记录是否重复。

优点：

* 简单直接。
* 符合当前 demo 场景。
* 方便用户理解。

后续如果支持同一公司多个岗位、多轮投递或历史归档，可以改为自动生成 application id。

---

#### 3. 限制 `match_score` 在 0 到 100 之间

`match_score` 来自 Resume Matcher 的输出。为了避免后续报告或排序逻辑出现异常，Application Tracker 中也做了范围校验。

当前规则：

```text
0 <= match_score <= 100
```

非法分数会直接抛出错误。

---

#### 4. 将 active 状态单独抽象出来

为了生成今日任务，需要判断哪些投递记录仍然需要用户跟进。

当前 active 状态包括：

```text
researching
preparing
applied
interview
```

这些状态代表用户仍然需要执行下一步动作。

非 active 状态包括：

```text
offer
rejected
archived
```

这些状态默认不进入今日任务清单。

---

### 遇到的问题与解决方式

#### 问题 1：本地 memory 文件可能不存在

如果用户第一次运行工具，`careerpilot/memory/applications.json` 可能还不存在。

解决方式：

* 在 `load_applications` 中检测文件是否存在。
* 如果不存在，自动创建父目录。
* 写入空 JSON 列表 `[]`。

---

#### 问题 2：JSON 文件可能被手动改坏

由于 memory 文件是本地 JSON，用户可能手动编辑时破坏格式。

解决方式：

* 捕获 `json.JSONDecodeError`。
* 抛出可读错误。
* 提示可以将文件恢复为空列表 `[]`。

---

#### 问题 3：重复记录可能导致状态混乱

如果同一家公司同一岗位被重复新增，后续更新时可能不知道应该更新哪一条。

解决方式：

* 新增时检查 `company + role`。
* 如果已存在，则拒绝新增。
* 后续可以扩展为支持 application id。

---

#### 问题 4：非法状态可能破坏流程

如果状态随意填写，例如 `waiting`、`done`、`pending`，后续统计和待办生成会变得不稳定。

解决方式：

* 定义固定状态枚举。
* 所有新增和更新操作都必须经过状态校验。

---

### 今日产出文件

新增或修改的文件包括：

```text
careerpilot/tools/application_tracker.py
careerpilot/memory/applications.json
tests/careerpilot/test_application_tracker.py
docs/dev_log.md
```

---

### 当前项目进度

截至 Day 6，CareerPilot 已经完成以下核心模块：

* Day 2：CareerPilot Skills 草稿。
* Day 3：JD Analyzer Tool。
* Day 4：Resume Matcher Tool。
* Day 5：Project Story Extractor。
* Day 6：Application Tracker 与本地 Memory。

目前项目已经具备从岗位分析、简历匹配、项目经历提炼到投递状态记录的基础模块。

下一步需要在 Day 7 将这些工具串联起来，形成端到端 demo flow。

---

### 面试可讲点

今天完成的 Application Tracker 可以作为项目中的 memory 模块来讲。

可以这样表达：

> 我在 CareerPilot 中实现了一个轻量级 Application Tracker，用本地 JSON 文件作为最小 memory，保存公司、岗位、投递状态、匹配分、下一步动作和备注。这个模块让智能体不只是一次性生成建议，而是可以持续跟踪用户的求职流程。为了保证 demo 稳定性，我增加了状态枚举、重复记录检查、JSON 异常处理和单元测试。

英文版本：

> I implemented a lightweight Application Tracker as the local memory layer of CareerPilot. It stores company, role, application status, match score, next action, and notes in a JSON file. This allows the agent to track the user's job-search workflow over time instead of only generating one-off recommendations. I also added status validation, duplicate detection, JSON error handling, and unit tests to make the module reliable for demos.

---

### 明日计划：Day 7

Day 7 的目标是打通端到端 Demo Flow。

计划新增：

```text
careerpilot/demo.py
examples/careerpilot/demo_report.md
docs/demo_script.md
```

目标命令：

```bash
python -m careerpilot.demo \
  --jd examples/careerpilot/sample_jd_backend.md \
  --resume examples/careerpilot/sample_resume.md \
  --project examples/careerpilot/sample_project_readme.md \
  --output examples/careerpilot/demo_report.md
```

预期输出完整 Markdown 报告，包含：

* JD 分析结果。
* 简历匹配结果。
* 项目经历重写结果。
* 面试准备建议。
* 投递状态记录。

## 2026-05-17 Day 7

### 今日目标
- 打通 CareerPilot 端到端 demo flow
- 将 JD Analyzer、Resume Matcher、Project Story Extractor 和 Application Tracker 串联起来
- 生成完整 Markdown demo report

### 完成内容
- 新增 `careerpilot/demo.py`
- 支持通过命令行传入 JD、简历和项目 README
- 自动生成 `examples/careerpilot/demo_report.md`
- 报告包含 JD 分析、简历匹配、项目经历提炼、3 天面试准备计划和投递记录摘要
- 新增 `docs/demo_script.md` 记录演示命令和讲解流程

### 技术决策
- 使用独立 demo 脚本先打通 MVP 闭环
- 输出 Markdown，方便 README 展示、面试演示和人工审核
- Application Tracker 继续使用本地 JSON，保持轻量可读

### 遇到问题
- `demo.py` 初版调用工具函数时与现有函数签名不一致
- 通过对齐 `analyze_jd`、`match_resume` 和 `extract_project_story` 的实际参数结构修复
- 后续 Day 8 再进一步研究 OpenHarness 原生运行方式和 skill/tool 接入边界

### 明日计划
- 研究 OpenHarness skill/tool 接入方式
- 让 CareerPilot 不只是独立 Python demo，而是能体现 OpenHarness workflow 扩展


## 2026-05-19 Day 8

### 今日目标
- 接入 OpenHarness 运行方式
- 让 CareerPilot 不只是独立 Python demo，而是具备 OpenHarness-facing workflow 入口
- 记录当前集成边界和后续 native tool registry 计划

### 完成内容
- 新增 `careerpilot/openharness_adapter.py`
- 为 CareerPilot end-to-end workflow 提供稳定 Python adapter
- 更新 `careerpilot/skills/career-coach.md`，补充 OpenHarness CLI 集成说明
- 新增 `docs/openharness_integration.md`
- 运行 `uv run oh --dry-run -p ...` 验证 OpenHarness dry-run 可用
- 验证 `python -m careerpilot.openharness_adapter` 可以生成 demo report

### 验证结果
- OpenHarness dry-run readiness: ready
- Auth validation: configured
- API client: ok
- Static discovery succeeded
- Built-in tools discovered: 39
- Skills discovered: 10
- CareerPilot adapter 可以生成 `examples/careerpilot/demo_report.md`
- `python -m py_compile careerpilot/openharness_adapter.py` 通过
- `python -m pytest -q tests/careerpilot` 通过

### 技术决策
- Day 8 采用轻量 adapter 方案，而不是直接修改 OpenHarness core
- 保持 CareerPilot 工具为 deterministic Python modules，降低 demo 风险
- 通过 Skill + Adapter + CLI 体现当前 OpenHarness 集成边界
- 将 native OpenHarness tool registry registration 作为后续增强任务

### 遇到问题
- OpenHarness dry-run 成功，但 likely skill match 中没有直接高亮 `career-coach`
- 当前版本先记录为 lightweight integration，后续再研究原生 tool registry 或 plugin 接入

### 明日计划
- Day 9 完善测试与异常处理
- 覆盖空输入、文件不存在、JSON 异常、重复投递记录等情况
