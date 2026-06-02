# CareerPilot Agent v0.2 Roadmap

> Status: planned after `v0.1-careerpilot-mvp`  
> Target version: `v0.2-careerpilot-agent-system`  
> Suggested duration: 8-12 days, standard plan 10 days  
> Core theme: upgrade CareerPilot from a runnable MVP into an evidence-based, traceable, evaluable, and safety-aware agent system.

---

## 1. Background

CareerPilot Agent v0.1 has completed the minimum job-search workflow:

```text
JD -> JD Analysis -> Resume Matching -> Project Bullet Rewriting -> Interview Plan -> Application Tracking
```

The v0.1 release is already suitable for resume use and project demonstration. The next version should not simply add more features. The goal of v0.2 is to improve system quality and interview value by adding evaluation, evidence, traceability, multi-role workflow design, and safety boundaries.

The original post-v0.1 enhancement plan included a larger 15-day scope:

```text
- ohmo / Telegram / Slack / Feishu integration
- RAG resume knowledge base
- Multi-agent collaboration
- Benchmark and quality evaluation
- GitHub project understanding
- Resume version management and diff
- Safety and compliance boundaries
```

The current v0.2 is a focused subset of that larger enhancement plan. It keeps the highest engineering-value items and moves more product-heavy or integration-heavy items to v0.3.

---

## 2. v0.2 Positioning

### Version Name

```text
CareerPilot Agent v0.2 — Evidence-based Multi-role Agent System
```

### One-sentence Goal

Upgrade CareerPilot from a CLI-based job-search MVP into an evidence-based multi-role agent system with benchmark evaluation, traceable intermediate outputs, lightweight retrieval, and human-review safety boundaries.

### What v0.2 Should Prove

```text
v0.1 proved:
I can build a complete domain-specific agent workflow on top of OpenHarness.

v0.2 should prove:
I can make that workflow evaluable, evidence-based, traceable, modular, and safer.
```

---

## 3. v0.2 Scope

### In Scope

v0.2 should include the following core capabilities:

```text
1. Benchmark / Evaluation
2. Evidence Matrix / Lightweight RAG
3. Multi-role Agent Workflow
4. Agent Trace
5. Safety Policy / Human Review Boundary
6. README and architecture updates
7. v0.2 release notes
```

### Out of Scope

The following items are intentionally deferred to v0.3:

```text
1. ohmo / Telegram / Slack / Feishu integration
2. GitHub repository automatic analyzer
3. Resume version management and diff
4. Full embedding-based RAG
5. Complex multi-agent runtime
6. Automated real-job application submission
```

Reason for deferral:

```text
- They are valuable, but not necessary for v0.2.
- They can significantly increase configuration, integration, and debugging cost.
- v0.2 should stay focused on engineering quality and interview explainability.
```

---

## 4. v0.2 Core Milestones

## M1. Benchmark / Evaluation

### Goal

Make CareerPilot measurable instead of only demonstrable.

### Motivation

Without evaluation, the project can look like a prompt wrapper. A benchmark layer shows that outputs can be checked, compared, and regression-tested.

### Planned Files

```text
careerpilot/
  evaluation/
    __init__.py
    metrics.py
    eval_runner.py

benchmarks/
  jds/
    backend_api_engineer.md
    ai_agent_engineer.md
    ml_platform_engineer.md
  resumes/
    backend_resume.md
    ai_agent_resume.md
  expected_keywords.json
  eval_report.md
```

### Metrics

```text
keyword_recall
schema_validity
report_completeness
overall_score
score_label
```

### Example CLI

```bash
python -m careerpilot.evaluation.eval_runner
```

### Expected Output

```text
benchmarks/eval_report.md
```

### Acceptance Criteria

```text
- At least 3 benchmark JD samples exist.
- Expected keyword annotations exist.
- Evaluation runner generates a Markdown report.
- Metrics are deterministic and locally runnable.
- Tests cover metric behavior.
```

---

## M2. Evidence Matrix / Lightweight RAG

### Goal

Make resume recommendations evidence-based.

### Motivation

The agent should not simply say “add this skill” or “highlight this project.” It should show where the recommendation comes from and whether the evidence is strong, weak, or missing.

### Planned Files

```text
careerpilot/
  knowledge/
    resumes/
      resume_backend.md
      resume_ai_agent.md
    projects/
      careerpilot_project.md
      backend_project.md
    interviews/
      sample_interview_notes.md

  tools/
    evidence_matrix_generator.py

examples/
  careerpilot/
    evidence_matrix.md
```

### Workflow

```text
JD requirement
  -> retrieve relevant resume/project/interview evidence
  -> score evidence strength
  -> generate recommendation
  -> render evidence matrix
```

### Evidence Matrix Format

```markdown
| JD Requirement | My Evidence | Source | Strength | Recommendation |
|---|---|---|---:|---|
| Python backend | FastAPI backend project | project doc | 5/5 | Keep as core project |
| Agent tool use | CareerPilot custom tools | project doc | 5/5 | Put in first project |
| Kubernetes | Only familiar, no project evidence | skills section | 2/5 | Mention as familiar, do not overclaim |
```

### Acceptance Criteria

```text
- Evidence matrix can be generated from local knowledge documents.
- Each recommendation has a source.
- Missing or weak evidence is explicitly marked.
- The output discourages exaggeration.
```

---

## M3. Multi-role Agent Workflow

### Goal

Upgrade the v0.1 single workflow into a modular multi-role agent workflow.

### Motivation

v0.1 is an end-to-end pipeline. v0.2 should expose clearer agent roles, intermediate results, and aggregation logic.

### Planned Files

```text
careerpilot/
  agents/
    __init__.py
    base.py
    jd_analyst.py
    resume_strategist.py
    project_story_agent.py
    interview_coach.py
    report_aggregator.py

examples/
  careerpilot/
    agent_trace.md
    demo_report_v0.2.md
```

### Agent Roles

```text
JDAnalystAgent
  Parses the job description into responsibilities, core skills, keywords, seniority, and interview focus.

ResumeStrategistAgent
  Compares resume evidence against JD requirements and proposes targeted resume strategy.

ProjectStoryAgent
  Converts project descriptions into resume-ready bullets and interview stories.

InterviewCoachAgent
  Generates preparation topics and daily plans based on gaps.

ReportAggregator
  Combines intermediate outputs into a final career report.
```

### Workflow

```text
User JD + Resume + Project Docs
  -> JDAnalystAgent
  -> ResumeStrategistAgent
  -> ProjectStoryAgent
  -> InterviewCoachAgent
  -> ReportAggregator
  -> Final v0.2 Career Report
```

### Agent Trace Requirements

The workflow should save intermediate outputs:

```text
examples/careerpilot/agent_trace.md
```

The trace should include:

```text
- agent name
- input summary
- output summary
- key decisions
- warnings or missing evidence
```

### Acceptance Criteria

```text
- Multi-role workflow runs end-to-end.
- Each agent has a clear input and output contract.
- Agent trace is generated.
- Final report includes evidence-aware recommendations.
```

---

## M4. Safety Policy / Human Review Boundary

### Goal

Add explicit safety and integrity boundaries for resume generation and application workflows.

### Motivation

CareerPilot operates in a high-integrity domain. It should not fabricate experience, exaggerate skills, or automatically apply to jobs without user review.

### Planned Files

```text
careerpilot/
  policies/
    resume_safety.md
    tool_permissions.md
```

### Safety Rules

```text
1. Do not fabricate work experience, education, projects, or achievements.
2. Do not exaggerate skill proficiency beyond the provided evidence.
3. Do not automatically submit real job applications.
4. Do not automatically fill sensitive personal information.
5. Mark weak or missing evidence clearly.
6. Require human review before resume submission.
7. Restrict file writes to the project workspace.
8. Require confirmation before sensitive shell or file operations.
```

### Required Disclaimer

```text
Human review required: This resume suggestion is generated for drafting purposes. Verify accuracy before submission.
```

### Acceptance Criteria

```text
- Safety policy documents exist.
- Demo report includes human-review disclaimer.
- Evidence matrix distinguishes strong, weak, and missing evidence.
- README documents the safety boundary.
```

---

## 5. Recommended 10-day Schedule

## Day 16-17: Benchmark / Evaluation

```text
- Create benchmark JD and resume samples.
- Add expected keyword annotations.
- Implement metrics.py.
- Implement eval_runner.py.
- Generate eval_report.md.
- Add tests for evaluation metrics.
```

Deliverables:

```text
careerpilot/evaluation/
benchmarks/
benchmarks/eval_report.md
tests/careerpilot/test_evaluation_metrics.py
```

---

## Day 18-19: Evidence Matrix / Lightweight RAG

```text
- Create knowledge directory.
- Add resume, project, and interview-note samples.
- Implement simple keyword retrieval.
- Implement evidence matrix generation.
- Add evidence_matrix.md example.
```

Deliverables:

```text
careerpilot/knowledge/
careerpilot/tools/evidence_matrix_generator.py
examples/careerpilot/evidence_matrix.md
```

---

## Day 20-22: Multi-role Agent Workflow

```text
- Create agents directory.
- Implement JDAnalystAgent.
- Implement ResumeStrategistAgent.
- Implement ProjectStoryAgent.
- Implement InterviewCoachAgent.
- Implement ReportAggregator.
- Save intermediate trace outputs.
- Generate demo_report_v0.2.md.
```

Deliverables:

```text
careerpilot/agents/
examples/careerpilot/agent_trace.md
examples/careerpilot/demo_report_v0.2.md
```

---

## Day 23: Safety Policy

```text
- Add resume_safety.md.
- Add tool_permissions.md.
- Add human-review disclaimer to reports.
- Update known issues or limitations.
```

Deliverables:

```text
careerpilot/policies/resume_safety.md
careerpilot/policies/tool_permissions.md
```

---

## Day 24-25: Documentation and Release

```text
- Update README.
- Update README.zh-CN if needed.
- Update architecture.md.
- Add v0.1 vs v0.2 comparison.
- Run full tests.
- Generate release notes.
- Tag release.
```

Deliverables:

```text
README.md
README.zh-CN.md
docs/architecture.md
docs/known_issues.md
RELEASE_NOTES_v0.2.md
```

Suggested tag:

```text
v0.2-careerpilot-agent-system
```

---

## 6. v0.1 vs v0.2 Comparison

| Dimension | v0.1 MVP | v0.2 Agent System |
|---|---|---|
| Main goal | Runnable job-search workflow | Evaluable and evidence-based agent system |
| Workflow | Single end-to-end demo flow | Multi-role agent workflow |
| Evaluation | Unit tests | Benchmark metrics and evaluation report |
| Evidence | Resume/JD comparison | Evidence matrix with source references |
| Output | Markdown/JSON report | Final report + evidence matrix + trace |
| Traceability | Limited demo output | Agent trace with intermediate decisions |
| Safety | Basic known issues | Explicit safety policy and human-review boundary |
| Resume value | Shows domain workflow implementation | Shows system design, evaluation, and agent safety |

---

## 7. v0.2 Final Acceptance Checklist

```text
- [ ] Benchmark dataset exists.
- [ ] Evaluation runner works locally.
- [ ] eval_report.md is generated.
- [ ] Evaluation metrics have tests.
- [ ] Knowledge documents exist.
- [ ] Evidence matrix generator works.
- [ ] evidence_matrix.md is generated.
- [ ] Multi-role agents are implemented.
- [ ] agent_trace.md is generated.
- [ ] demo_report_v0.2.md is generated.
- [ ] Safety policy documents exist.
- [ ] Human-review disclaimer appears in generated reports.
- [ ] README includes v0.1 vs v0.2 comparison.
- [ ] Architecture docs are updated.
- [ ] Full test suite passes.
- [ ] v0.2 release notes are written.
- [ ] GitHub release tag is created.
```

---

## 8. Suggested v0.2 Resume Bullet

### English

```text
Extended CareerPilot from a CLI-based MVP into an evidence-based multi-role agent system with benchmark evaluation, traceable intermediate outputs, lightweight retrieval, and human-review safety boundaries for resume tailoring workflows.
```

### Chinese

```text
将 CareerPilot 从 CLI 求职流程 MVP 扩展为具备 Benchmark 评估、证据矩阵、多角色工作流、Agent Trace 与人工审核安全边界的智能体系统，提升简历定制建议的可解释性、可追踪性与工程可信度。
```

---

## 9. v0.3 Direction

v0.3 should focus on productization and richer integrations after v0.2 has established the system foundation.

### v0.3 Candidate Features

```text
1. ohmo / Telegram / Slack / Feishu integration
2. GitHub/local repository analyzer
3. Resume version management
4. Resume diff report
5. Embedding-based RAG
6. More realistic application memory
7. Optional chat-based workflow
```

### v0.3 Priority Recommendation

```text
P0: ohmo or one chat-channel integration
P1: GitHub/local repository analyzer
P1: Resume version management and diff report
P2: Embedding-based RAG
P2: More advanced multi-agent coordination
```

### v0.3 Target Positioning

```text
CareerPilot Agent v0.3 — Productized Personal Career Agent
```

### v0.3 Goal

Turn CareerPilot from a local agent system into a more product-like personal career assistant that can interact through chat channels, understand local or GitHub projects, manage tailored resume versions, and preserve richer application history.

### Deferred Risks

```text
- IM channel configuration may take longer than expected.
- GitHub repo analysis can become broad and should avoid hallucinating nonexistent modules.
- Resume versioning must avoid overwriting the base resume.
- Embedding-based RAG adds dependency and reproducibility complexity.
```

---

## 10. Implementation Policy

v0.2 should follow these constraints:

```text
- Prefer deterministic, locally runnable logic before adding external services.
- Keep all generated examples committed under examples/careerpilot/.
- Keep benchmark data small but representative.
- Maintain backward compatibility with v0.1 demo commands where possible.
- Avoid expanding scope during v0.2 implementation.
- Push after each stable milestone.
- Update docs and dev_log after each milestone.
```

---

## 11. Recommended Next Step

Start with M1 Benchmark / Evaluation because it gives the highest immediate engineering value and creates a foundation for future regression testing.

First implementation target:

```bash
python -m careerpilot.evaluation.eval_runner
```

Expected artifact:

```text
benchmarks/eval_report.md
```
