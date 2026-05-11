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

