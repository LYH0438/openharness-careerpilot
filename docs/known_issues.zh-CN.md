# CareerPilot Agent 已知问题与后续改进

本文档记录 CareerPilot Agent MVP 阶段的当前限制和后续改进方向。

它的目的不是削弱项目价值，而是让项目边界更清楚，方便后续继续开发，也方便面试时解释当前版本和未来版本的区别。

## 1. OpenHarness 集成仍然是轻量级

### 当前状态

CareerPilot 当前通过以下方式和 OpenHarness 对齐：

- Markdown skill files
- OpenHarness dry-run 验证
- 轻量 adapter 模块
- CLI demo 工作流

### 当前限制

CareerPilot 的工具还没有注册为 OpenHarness 原生 tool registry 中的工具。

当前集成可以说明项目遵循 OpenHarness 的 skills、tools、memory 和 workflow 思路，但还不是完整的 OpenHarness runtime tool invocation。

### 后续改进

后续版本可以继续研究 OpenHarness tool registry 或 plugin 机制，把 CareerPilot 工具注册为原生工具。

## 2. 匹配分是启发式评分

### 当前状态

Resume Matcher 使用 deterministic matching logic 生成匹配分。

它主要考虑：

- 核心技能覆盖
- 缺失技能
- 简历证据
- 岗位职责
- 面试重点

### 当前限制

这个分数适合 demo 和解释，但没有用真实招聘结果做验证。

它不能被理解为“拿到面试的概率”。

### 后续改进

后续可以建立轻量 benchmark，用多组 JD 和简历评估：

- 关键词召回率
- 缺失技能判断准确度
- 报告完整性
- schema 稳定性
- 建议可执行性

## 3. 规则型 parser 的语言理解能力有限

### 当前状态

CareerPilot MVP 为了稳定性，主要使用规则型、确定性的解析逻辑。

### 当前限制

这种方式对标准样例比较稳定，但对复杂、不规范或很长的 JD，可能无法理解所有隐含要求。

例如：

- 隐含的资历要求
- 软技能要求
- 行业背景要求
- 模糊描述
- 格式混乱的岗位文本

### 后续改进

后续可以增加可选的 LLM analysis layer，同时保留 deterministic tools 作为 schema validator 和 fallback。

## 4. 简历建议必须人工审核

### 当前状态

CareerPilot 可以生成简历 bullet、改写建议和面试故事。

### 当前限制

生成内容可能不够具体，或者表达强度超过用户真实经历。

CareerPilot 不能用来伪造经历，也不能夸大技能熟练度。

### 后续改进

后续可以在报告中加入更明确的安全提示和 human-review 提醒。

## 5. 本地 JSON memory 不是生产级存储

### 当前状态

投递记录保存在：

    careerpilot/memory/applications.json

### 当前限制

本地 JSON 简单、可读，但不适合：

- 多用户
- 并发写入
- 远程访问
- 高级筛选
- 长期生产环境

### 后续改进

如果 CareerPilot 后续变成 Web 应用或多人使用工具，可以考虑引入 SQLite、PostgreSQL 或其他存储方案。

## 6. 还没有 RAG 知识库

### 当前状态

当前 demo 读取一份 JD、一份简历和一份项目说明。

### 当前限制

系统还不能从更大的个人资料库中自动检索：

- 多版本简历
- 多个项目文档
- 过往面试记录
- 历史投递结果
- 公司相关笔记

### 后续改进

后续可以加入 RAG-style knowledge layer，根据目标岗位自动选择最相关的项目经历和简历证据。

## 7. 还没有多 Agent 工作流

### 当前状态

CareerPilot 当前是单一 workflow 调用多个工具。

### 当前限制

它还没有把不同职责拆分成多个专门 Agent。

### 后续改进

后续可以引入以下角色：

- JDAnalystAgent
- ResumeStrategistAgent
- ProjectStoryAgent
- InterviewCoachAgent
- ApplicationOpsAgent

然后把多个 Agent 的输出聚合成最终报告。

## 8. 还没有聊天或 IM 渠道

### 当前状态

CareerPilot 当前通过本地命令和 demo script 运行。

### 当前限制

它还不能通过 Telegram、Slack、飞书、Discord 等聊天工具使用。

### 后续改进

后续可以通过 ohmo 或类似 gateway，把求职工作流接入聊天界面。

## 9. Demo 输入样例仍然较小

### 当前状态

`examples/careerpilot/` 下的样例故意保持较小，方便学习和演示。

### 当前限制

小样例适合展示流程，但不能充分覆盖真实世界中复杂、混乱、多样的 JD 和简历。

### 后续改进

后续可以增加更多样例和 benchmark case，例如：

- Backend Engineer
- AI Agent Engineer
- ML Engineer
- Platform Engineer
- Junior / Senior 不同级别岗位

## 10. 输出质量仍需要评估体系

### 当前状态

当前输出是可读、可测试的，但质量主要依赖人工检查。

### 当前限制

系统还没有自动判断一条 bullet 是否足够具体、真实、有结果导向。

### 后续改进

后续可以增加质量评估规则，例如：

- bullet 是否包含动作、技术和影响
- 建议是否对应 JD 缺口
- 是否避免夸大或编造
- 面试计划是否具体且有时间安排
