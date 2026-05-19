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

## 2026-05-19 Day 9

### 今日目标

- 完善 CareerPilot 核心工具的测试覆盖。
- 验证异常处理和输出稳定性。
- 确认 CareerPilot 新增模块不会破坏 OpenHarness 原有测试。

### 完成内容

- 确认 `tests/careerpilot/` 下已经包含 4 个核心测试文件：
  - `test_application_tracker.py`
  - `test_jd_analyzer.py`
  - `test_project_story_extractor.py`
  - `test_resume_matcher.py`

- 运行 CareerPilot 专属测试集，全部通过。
- 运行 OpenHarness 全仓库测试集，全部通过。
- 验证 CareerPilot 的工具、测试和 OpenHarness 集成没有引入回归问题。
- 当前测试结果说明 CareerPilot 已经具备较好的基础工程稳定性，可以继续进入 README 和项目包装阶段。

### 验收结果

CareerPilot 专属测试命令：

```bash
python -m pytest -q tests/careerpilot
```

运行结果：

```text
..................                                                                                                           [100%]
18 passed in 0.05s
```

OpenHarness 全仓库测试命令：

```bash
python -m pytest -q
```

运行结果：

```text
............................................................................................................................ [ 11%]
............................................................................................................................ [ 23%]
............................................................................................................................ [ 34%]
............................................................................................................................ [ 46%]
.......................................................................................s.................................... [ 57%]
............................................................................................................................ [ 69%]
............................................................................................................................ [ 80%]
............................................................................................................................ [ 92%]
........................................s......ss..ss............................                                            [100%]
1067 passed, 6 skipped in 23.88s
```

### 技术决策

- 将 CareerPilot 的核心工具视为可测试模块，而不是一次性 demo 脚本。
- 使用 pytest 验证 JD 分析、简历匹配、项目经历提炼和投递记录管理的基础行为。
- 保持工具输出结构稳定，方便后续 README 展示、demo 报告生成和面试讲解。
- 在进入 README 包装前，先通过 CareerPilot 局部测试和 OpenHarness 全量测试，确保项目集成没有破坏原仓库行为。
- 当前阶段继续保持轻量实现，不引入复杂数据库或额外服务，优先保证半月版 MVP 可运行、可解释、可测试。

### 今日总结

Day 9 主要完成了 CareerPilot 的工程稳定性验证。当前 `tests/careerpilot/` 下已经覆盖 4 个核心工具模块，并且 CareerPilot 专属测试集通过 `18 passed`。同时，OpenHarness 全仓库测试也通过 `1067 passed, 6 skipped`，说明新增的 CareerPilot 模块没有影响原项目功能。

这一天的价值在于把 CareerPilot 从“能运行的功能 demo”进一步推进为“有测试保护的工程项目”。后续在 README、简历和面试展示中，可以强调项目不仅实现了 JD 分析、简历匹配、项目提炼和投递记录管理，也具备基础测试和回归验证。

### 明日计划

- 开始 Day 10：README 第一版。
- 在 README 中补充项目定位、核心功能、架构图、快速开始、demo 命令、测试命令和后续路线图。
- 将 CareerPilot 包装成一个招聘方可以快速理解的 OpenHarness 垂直场景智能体项目。
## 2026-05-19 Day 11

### 今日目标
- 优化 CareerPilot 输出质量，让报告更像真实求职工具，而不是模板生成器。
- 优化 Project Story Extractor 的中英文简历 bullet，使其更接近 STAR / XYZ 表达。
- 优化 Resume Matcher 的缺口建议和简历改写建议，使输出更具体、可执行。
- 优化 demo report 的 Markdown 展示格式，减少原始 JSON 对阅读体验的影响。

### 完成内容
- 优化了 `careerpilot/tools/project_story_extractor.py`：
  - 调整技术栈排序逻辑，使 `OpenHarness`、`Python`、`Pydantic`、`Agent`、`Skill`、`Memory` 等核心技术优先展示。
  - 改进中文简历 bullet，使其包含动作、技术、结构化输出和结果价值。
  - 改进英文简历 bullet，使其更适合放入英文简历或面试材料。
  - 修复了 `_build_resume_bullets_en` 重复定义导致新版英文 bullet 被旧逻辑覆盖的问题。

- 优化了 `careerpilot/tools/resume_matcher.py`：
  - 增强 `weak_evidence` 输出，使其能指出缺少量化结果、缺少核心技能证据、缺少岗位职责映射等问题。
  - 增强 `rewrite_suggestions` 输出，使其包含 Project Experience、Skills / Keywords、Gap Fix、Impact Metrics 等具体建议。
  - 将简历建议从泛泛描述改为更接近真实求职场景的可执行建议。
  - 保持原有 `ResumeMatchOutput` 结构不变，避免破坏现有测试和 demo workflow。

- 优化了 `careerpilot/demo.py`：
  - 改进 `format_item` 和 `format_list` 的 Markdown 渲染逻辑。
  - 将 `rewrite_suggestions` 从原始 JSON 行改成更易读的 Markdown 子项。
  - 将 `Application Tracker Summary` 从原始 JSON 行改成公司、岗位、状态、匹配分、下一步动作和备注的展示格式。

- 重新生成了示例输出：
  - `examples/careerpilot/output_project_bullets.md`
  - `examples/careerpilot/demo_report.md`

### 验证结果
- Project Story Extractor 测试通过：3 passed in 0.02s
- Resume Matcher 测试通过：2 passed in 0.02s
- CareerPilot 全量测试通过：18 passed in 0.05s

### 输出质量改进
- `output_project_bullets.md` 现在包含更清晰的中英文简历 bullet：
  - 中文 bullet 强调 OpenHarness、Agent、Skill、Memory、结构化输出和可测试模块。
  - 英文 bullet 强调 project story extraction、structured schema、deterministic keyword extraction 和 testable modules。

- `demo_report.md` 现在更适合展示：
  - JD Analysis、Resume Match、Project Story、Interview Plan 和 Application Tracker 形成完整闭环。
  - Rewrite Suggestions 已经从 JSON 改为可读 Markdown。
  - Application Tracker Summary 已经从 JSON 改为简洁状态摘要。
  - Human Review Notice 保留，强调简历建议需要人工审核，避免生成内容被直接当作事实使用。

### 技术决策
- 继续保持规则化、确定性输出，而不是引入不稳定的自由生成逻辑。
- 优先提升 demo report 的可读性和简历 bullet 的可复用性。
- 不改变已有输入输出 schema，保证测试和后续 OpenHarness workflow 集成稳定。
- 将“输出质量优化”控制在工具层和 demo 渲染层，避免影响 Application Tracker 等已稳定模块。

### 遇到问题
- `project_story_extractor.py` 中存在重复定义的 `_build_resume_bullets_en`，导致前一次优化没有完全生效。
- 初版英文 bullet 中混入中文 architecture highlight，导致英文输出不自然。
- 初版 demo report 中 `rewrite_suggestions` 和 application records 以原始 JSON 形式展示，不适合 README 或面试演示截图。

### 解决方式
- 删除重复的英文 bullet 函数定义。
- 将第三条中英文 bullet 改为固定的、自然的 Tool abstraction 表达。
- 在 `demo.py` 中针对 rewrite suggestion 和 application record 增加 Markdown 渲染逻辑。
- 重新生成 demo report 并运行全量测试确认没有回归。

### 明日计划
- Day 12：增加或强化 3 天 / 7 天面试准备计划能力。
- 让面试计划与 JD 分析、简历缺口、弱证据更加相关。
- 考虑新增独立的 `interview_plan_generator.py`，或者在现有 demo flow 中增强 interview preparation 输出。
- 继续保持可测试、可解释、可展示的实现方式。

### 可复用材料
- 中文简历 bullet 草稿：
  - 基于 OpenHarness、Python、Pydantic、Agent 构建面向求职场景的 CareerPilot Agent，扩展 JD 分析、简历匹配、项目经历提炼和投递状态追踪工具，实现从岗位分析到面试准备的端到端自动化闭环。
  - 设计结构化输出 schema 和规则化生成逻辑，将岗位关键词、能力缺口、项目亮点和面试准备项转化为可测试、可复用的求职报告，提升输出稳定性和面试展示价值。
  - 优化 demo report 的 Markdown 渲染和人审提示机制，使智能体输出不仅可被程序消费，也能直接用于 README 展示、简历微调和面试复盘。

- 英文简历 bullet 草稿：
  - Built CareerPilot Agent on top of OpenHarness with custom tools for JD analysis, resume matching, project story extraction, and application tracking, enabling an end-to-end job-search workflow from role analysis to interview preparation.
  - Designed structured output schemas and deterministic generation logic to convert job requirements, skill gaps, project highlights, and interview topics into testable and reusable career reports.
  - Improved Markdown report rendering and human-review safeguards, making agent outputs suitable for README demos, resume tailoring, and interview preparation workflows.

## 2026-05-19 Day 12：增加 3 天 / 7 天面试准备计划

### 今日目标

今天的目标是补齐 CareerPilot Agent 求职闭环中的“面试准备计划”模块，让系统不仅能分析 JD、匹配简历、提炼项目经历，还能根据岗位要求和简历短板生成可执行的 3 天或 7 天面试准备计划。

### 完成内容

- 新增 `careerpilot/tools/interview_plan_generator.py`。
- 新增结构化输入模型 `InterviewPlanInput`。
- 新增每日计划模型 `InterviewDay`。
- 新增结构化输出模型 `InterviewPlanOutput`。
- 实现 `generate_interview_plan()`，根据 JD 分析结果和简历匹配结果生成准备计划。
- 实现 `format_interview_plan_markdown()`，将结构化计划转换为 Markdown 报告。
- 支持 `available_days` 参数，可以生成 3 天、7 天或其他 1-14 天范围内的计划。
- 支持 `daily_hours` 参数，可以根据每天可投入时间输出计划。
- 更新 `careerpilot/demo.py`，将原先 demo 内部的临时面试计划逻辑替换为正式工具调用。
- 新增 `tests/careerpilot/test_interview_plan_generator.py`。
- 新增 `examples/careerpilot/output_interview_plan.md`。
- 更新 `examples/careerpilot/demo_report.md`，端到端报告现在包含 7 天面试准备计划。

### 关键实现

本次将面试计划从 demo 脚本中的固定模板升级为独立 Tool。

输入包括：

    {
      "jd_analysis": "JD Analyzer 的结构化输出",
      "resume_match": "Resume Matcher 的结构化输出",
      "available_days": 7,
      "daily_hours": 2,
      "target_role": "Backend Engineer"
    }

输出包括：

    {
      "target_role": "Backend Engineer",
      "available_days": 7,
      "daily_hours": 2,
      "priority_topics": [],
      "daily_plan": [],
      "final_checklist": [],
      "human_review_notice": ""
    }

计划生成逻辑优先参考以下字段：

- `resume_match.interview_preparation_topics`
- `resume_match.missing_skills`
- `resume_match.weak_evidence`
- `jd_analysis.interview_focus`
- `jd_analysis.core_skills`
- `resume_match.resume_keywords_to_add`

这样可以保证面试准备计划不是泛泛模板，而是和 JD 要求、简历缺口、项目证据弱点强相关。

### 设计决策

#### 1. 为什么单独新增 `interview_plan_generator.py`

之前 demo 中已有一个简单的 3 天面试计划，但它只是 demo helper，不能被测试、复用或单独运行。

本次将其抽象为独立 Tool，原因是：

- 便于单元测试。
- 便于未来接入 OpenHarness tool registry。
- 便于 demo、CLI、IM gateway 或多 Agent 工作流复用。
- 更符合 CareerPilot 的模块化设计：JD Analyzer、Resume Matcher、Project Story Extractor、Interview Plan Generator、Application Tracker 各自负责一个清晰能力。

#### 2. 为什么使用规则生成而不是直接依赖 LLM

半月版优先保证稳定可演示，因此本模块继续采用 deterministic rule-based generator。

好处是：

- 输出稳定。
- 测试容易。
- demo 不依赖外部模型调用。
- 面试时可以清楚解释生成逻辑。
- 避免 LLM 输出字段不稳定导致 demo report 崩溃。

#### 3. 为什么保留 human review notice

面试准备和简历修改都涉及真实经历表达，因此输出中继续保留人工审核提醒。

这是为了避免：

- 编造不存在的项目经历。
- 夸大技能熟练度。
- 把学习计划写成真实工作经验。
- 在真实投递中直接使用未经审核的内容。

### 测试结果

新增测试通过：

    python -m pytest -q tests/careerpilot/test_interview_plan_generator.py

结果：

    ... [100%]
    3 passed in 0.03s

CareerPilot 全量测试通过：

    python -m pytest -q tests/careerpilot

结果：

    ..................... [100%]
    21 passed in 0.06s

### Demo 验证

生成独立面试计划输出：

    python -m careerpilot.tools.interview_plan_generator > examples/careerpilot/output_interview_plan.md

生成 7 天端到端 demo report：

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

输出结果：

    [Warning] Failed to add application record: Application already exists: Example AI - Backend Engineer
    Demo report generated: examples/careerpilot/demo_report.md

其中 warning 是正常现象，因为 Application Tracker 已经存在 `Example AI - Backend Engineer` 记录，重复记录保护生效，没有影响 demo report 生成。

### Demo Report 检查

使用以下命令检查报告内容：

    grep -n "Interview Preparation Plan" examples/careerpilot/demo_report.md
    grep -n "Day 7" examples/careerpilot/demo_report.md
    grep -n "Final Checklist" examples/careerpilot/demo_report.md

结果显示：

    198:# 4. Interview Preparation Plan
    200:# Interview Preparation Plan
    303:## Day 7: Mock Interview and Final Review
    321:## Final Checklist

说明端到端报告中已经包含：

- Interview Preparation Plan
- 7 天准备计划
- Day 7 模拟面试和最终复盘
- Final Checklist

### 今日产出文件

    careerpilot/tools/interview_plan_generator.py
    tests/careerpilot/test_interview_plan_generator.py
    careerpilot/demo.py
    examples/careerpilot/output_interview_plan.md
    examples/careerpilot/demo_report.md
    docs/dev_log.md

### 当前项目状态

Day 12 后，CareerPilot Agent 的 MVP 闭环已经进一步完整：

    JD -> JD 分析 -> 简历匹配 -> 项目经历提炼 -> 面试准备计划 -> 投递记录 -> Demo Report

相比 Day 7 的 demo flow，当前版本的面试准备计划已经从固定模板升级为可复用、可测试、结构化的正式模块。

### 遇到的问题

#### 问题 1：Application Tracker 重复记录 warning

运行 demo 时出现：

    [Warning] Failed to add application record: Application already exists: Example AI - Backend Engineer

原因是之前 Day 7 已经写入过同一个公司和岗位的记录。

当前处理方式：

- 保留 warning。
- 不影响 demo report 生成。
- 不在 Day 12 中强行修改 memory 行为。

后续可以在 Day 13 或 Day 14 中考虑优化：

- demo 运行时允许更新已有记录。
- 或增加 `--allow-update-application` 参数。
- 或在 report 中显示“已有记录未重复添加”。

#### 问题 2：`demo_report.md` 中 application tracker 仍显示 Day 7 的旧 next_action

当前报告里仍能看到旧记录：

    "next_action": "review generated demo report and rewrite project bullets"
    "notes": ["Generated from CareerPilot Day 7 demo flow."]

这不是 Day 12 功能错误，而是 Application Tracker 去重后没有覆盖旧记录导致的。

后续计划：

- 在文档中说明这是当前 MVP 的 known issue。
- 后续增加 update existing application 的能力。

### 技术收获

今天主要完成了从“demo 内部逻辑”到“正式 Tool 模块”的升级。

这体现了几个工程能力：

- 用 Pydantic schema 固定输入输出结构。
- 用 deterministic rules 保证 demo 稳定。
- 用 pytest 覆盖新增模块。
- 将业务逻辑从 demo script 中拆出，提升复用性。
- 将 JD 分析、简历匹配和面试计划串成完整求职闭环。
- 保留 human-in-the-loop，避免求职材料生成中的事实风险。

### 可用于面试讲解的总结

Day 12 我把 CareerPilot 的面试准备计划从 demo 中的固定模板升级成了独立工具。这个工具读取 JD Analyzer 和 Resume Matcher 的结构化输出，优先根据岗位面试重点、缺失技能、弱证据和关键词缺口生成 3 天或 7 天计划。每一天都会输出 focus、tasks、deliverables 和 estimated_hours，并且最后有 final checklist 和 human review notice。这样 CareerPilot 不只是给出分析报告，还能把岗位差距转化为可执行的面试准备行动。

### 明日计划

Day 13 进入文档补齐阶段，重点是让项目更容易被回看、复盘和面试展示。

计划补充：

- `docs/architecture.md`
- `docs/decision_record.md`
- `docs/demo_script.md`
- `docs/known_issues.md`

其中 `known_issues.md` 可以记录 Application Tracker 重复记录 warning 和当前 MVP 的边界。

## 2026-05-19 Day 13

### 今日目标

补充 CareerPilot Agent 的开发文档和设计溯源记录，让项目不仅能运行，也能在后续复盘和面试中讲清楚架构、取舍、限制和演示流程。

### 完成内容

1. 新增英文架构文档：

   - `docs/architecture.md`

   该文档说明了 CareerPilot 的整体架构，包括 OpenHarness runtime layer、Skill layer、Tool layer、Adapter layer、Demo layer 和 Memory layer。

2. 新增中文架构文档：

   - `docs/architecture.zh-CN.md`

   中文版本用于后续自己复盘和面试准备，内容与英文架构文档保持一致。

3. 新增英文技术决策记录：

   - `docs/decision_record.md`

   记录了 MVP 阶段的关键技术决策，包括为什么基于 OpenHarness、为什么使用 deterministic tools、为什么使用 JSON memory、为什么先采用 adapter 集成方式等。

4. 新增中文技术决策记录：

   - `docs/decision_record.zh-CN.md`

   中文版本方便后续回看，也方便整理面试回答。

5. 新增英文已知问题文档：

   - `docs/known_issues.md`

   记录当前 MVP 的限制，例如 OpenHarness 集成仍然是轻量级、匹配分是启发式评分、没有 RAG 知识库、没有多 Agent 工作流等。

6. 新增中文已知问题文档：

   - `docs/known_issues.zh-CN.md`

   中文版本用于明确当前项目边界和后续增强方向。

7. 重写英文演示脚本：

   - `docs/demo_script.md`

   将原有简单演示说明升级为正式 demo script，包含演示目标、演示步骤、两分钟讲解稿、五分钟讲解结构和常见面试问题。

8. 新增中文演示脚本：

   - `docs/demo_script.zh-CN.md`

   中文版本用于自己练习演示和面试讲解。

### 技术决策

1. Day 13 不新增功能代码，重点补齐文档体系。
2. 架构文档明确说明当前 CareerPilot 是 OpenHarness 之上的垂直领域扩展，而不是重写 OpenHarness core。
3. 决策记录明确当前 MVP 使用 deterministic tools 的原因：稳定、可测试、可解释。
4. 已知问题文档主动说明当前限制，避免项目被误解为已经完成生产级集成。
5. Demo script 同时提供英文和中文版本，方便 GitHub 展示和个人复盘。

### 验证结果

运行 CareerPilot 测试：

    python -m pytest -q tests/careerpilot

结果：

    21 passed

说明 Day 13 的文档修改没有影响现有功能和测试。

### 当前项目状态

新增或修改的文档包括：

    docs/architecture.md
    docs/architecture.zh-CN.md
    docs/decision_record.md
    docs/decision_record.zh-CN.md
    docs/demo_script.md
    docs/demo_script.zh-CN.md
    docs/known_issues.md
    docs/known_issues.zh-CN.md
    docs/dev_log.md

### 明日计划

Day 14 将进入最终整理与演示准备阶段，重点包括：

1. 清理代码和无用文件。
2. 跑完整 demo。
3. 跑完整测试。
4. 更新 README 中的文档链接。
5. 准备 2 分钟演示脚本。
6. 准备简历项目描述。
7. 准备 v0.1-careerpilot-mvp tag。

## 2026-05-19 Day 14

### 今日目标

- 完成 CareerPilot v0.1 MVP 的最终整理与演示准备。
- 重新验证端到端 demo、测试、OpenHarness dry-run 和核心文档。
- 为后续打 tag 和发布 v0.1 做准备。

### 完成内容

- 确认当前分支为 `feature/careerpilot-agent`，并且本地与远程 `origin/feature/careerpilot-agent` 保持同步。
- 重新运行端到端 demo，成功生成 `examples/careerpilot/demo_report.md`。
- 验证 demo report 覆盖 JD 分析、简历匹配、项目经历提炼和 7 天面试准备计划。
- 运行 CareerPilot 专属测试，`tests/careerpilot` 共 21 个测试全部通过。
- 运行 OpenHarness dry-run 检查，确认配置、prompt assembly、API client、skill/tool discovery 等静态检查处于 ready 状态。
- 检查 `careerpilot/skills` 下的三个 Markdown Skill 文件：`career-coach.md`、`resume-rewriter.md`、`interview-prep.md`。
- 检查 README 是否覆盖项目定位、架构、Quick Start、Demo、OpenHarness dry-run、测试说明、Roadmap 和简历描述。
- 检查 `docs/openharness_integration.md`，确认当前 MVP 的 OpenHarness 集成边界已经写清楚。

### 验证命令

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

    python -m pytest -q tests/careerpilot

    uv run oh --dry-run -p "Use career-coach skill. Analyze examples/careerpilot/sample_jd_backend.md and compare it with examples/careerpilot/sample_resume.md. Generate a job-fit report using CareerPilot."

### 验证结果

- Demo report generated: `examples/careerpilot/demo_report.md`
- CareerPilot tests: 21 passed
- OpenHarness dry-run readiness: ready
- Git working tree: clean before Day14 log update

### 技术决策

- v0.1 继续保持 lightweight integration：OpenHarness 负责 CLI prompt entrypoint、skill/workflow context 和 dry-run readiness validation；CareerPilot 通过 Python 模块和 `openharness_adapter` 暴露稳定的端到端 workflow。
- 暂不在 v0.1 中强行实现 native OpenHarness tool registry registration，避免在 MVP 收尾阶段引入不稳定改动。
- README 和集成文档中明确说明当前边界，避免把 dry-run 集成夸大为完整原生工具注册。

### 遇到问题

- 重新运行 demo 时出现 `Application already exists: Example AI - Backend Engineer` warning。
- 该 warning 来自 Application Tracker 的重复记录保护，不影响 demo report 生成，也不影响测试结果。
- 后续可以考虑在 demo 命令中增加 `--skip-tracker` 或 `--update-existing-application` 参数，让重复运行 demo 时输出更干净。

### 当前状态

- CareerPilot v0.1 MVP 已经具备可演示状态。
- 核心功能、测试、文档和 OpenHarness dry-run 均已验证。
- 下一步是准备 release note、2 分钟演示稿、简历项目描述，并打 tag：`v0.1-careerpilot-mvp`。

### 明日计划

- Day 15 作为 buffer day，修复最后发现的问题。
- 准备 GitHub release note。
- 根据需要补充 demo 截图或录屏。
- 发布 v0.1 MVP。

## 2026-05-19 Day 15 Final Release

### 今日目标

- 完成 CareerPilot Agent v0.1 半月版最终发布。
- 确认测试、demo、tag、release note 和 GitHub Release 状态。
- 将项目整理为可演示、可复盘、可写进简历的 MVP 版本。

### 完成内容

- 重新运行 CareerPilot 专属测试，结果为 21 passed。
- 重新运行端到端 demo，成功生成 `examples/careerpilot/demo_report.md`。
- 确认当前开发分支为 `feature/careerpilot-agent`。
- 确认远程分支已推送到 GitHub。
- 确认版本 tag `v0.1-careerpilot-mvp` 已存在。
- 新增根目录 `RELEASE_NOTES.md`，用于 GitHub Release 页面展示。
- 在 GitHub 发布 v0.1 release。

### GitHub Release

Release 页面：

https://github.com/LYH0438/openharness-careerpilot/releases

### 当前 v0.1 状态

CareerPilot Agent v0.1 已完成半月版 MVP 闭环：

- JD Analyzer：岗位描述结构化分析。
- Resume Matcher：简历与岗位匹配分析。
- Project Story Extractor：项目经历提炼与中英文 bullet 生成。
- Interview Plan Generator：3 天 / 7 天面试准备计划。
- Application Tracker：本地 JSON 投递记录管理。
- Career Skills：通过 Markdown Skill 固化求职工作流。
- OpenHarness Integration：完成 dry-run、skill-guided workflow 和轻量 adapter 集成。
- Demo Report：一条命令生成端到端求职分析报告。
- Tests：核心工具测试通过。

### Known Issues

- 当前 OpenHarness 集成仍以 dry-run、skill 和 adapter 为主，尚未完成深度原生 tool registry 接入。
- 匹配分是启发式评分，重点是可解释和可测试，尚未做 benchmark。
- 简历生成内容仍需要人工审核，不能自动投递或夸大经历。
- 当前 memory 使用本地 JSON，不适合多用户或生产并发场景。
- IM 渠道、RAG、多 Agent、benchmark 和安全策略计划放入 v0.2。

### 阶段总结

v0.1 的目标不是做一个完整求职平台，而是基于 OpenHarness 做出一个可以运行、可以演示、可以解释架构、可以写进简历的垂直领域智能体 MVP。

当前版本已经形成从岗位 JD 到简历匹配、项目经历优化、面试准备和投递记录的最小闭环。后续 v0.2 可以继续围绕 ohmo / IM 接入、RAG 简历知识库、多 Agent 协作、benchmark 评估和安全边界增强项目复杂度。

### 简历 Bullet

中文：

基于 OpenHarness 二次开发 CareerPilot Agent 求职流程智能体，扩展 JD 解析、简历匹配、项目经历提炼、面试准备计划和投递状态追踪等自定义工具；通过 Markdown Skill 固化求职工作流，结合本地 JSON Memory、结构化输出、可解释评分逻辑和 pytest 测试，形成从岗位分析到简历优化和面试准备的端到端 CLI Demo。

英文：

Built CareerPilot Agent, a personalized job-search agent on top of OpenHarness, by extending custom tools, domain skills, local memory, structured outputs, and an end-to-end CLI workflow. Implemented JD parsing, resume-job matching, project story extraction, interview preparation planning, and application tracking with explainable scoring and test coverage.

### 下一阶段计划

- Day16 起进入 v0.2 增强阶段。
- 优先考虑 ohmo / Telegram / Slack / Feishu 等 IM 渠道接入。
- 增加 RAG 简历知识库和岗位-经历证据矩阵。
- 拆分多 Agent / 多角色求职工作流。
- 增加 benchmark 和 schema validation 评估报告。
- 增加安全策略和 human-in-the-loop 边界。
