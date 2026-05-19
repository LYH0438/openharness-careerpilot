# CareerPilot Agent Architecture

## 1. Overview

CareerPilot Agent is a domain-specific job-search agent built on top of OpenHarness.

The goal of this MVP is not to rewrite the OpenHarness runtime. Instead, CareerPilot extends OpenHarness at the application layer with career-focused tools, markdown skills, local memory, structured outputs, tests, and a CLI demo workflow.

The current workflow is:

    Job Description
      -> JD Analysis
      -> Resume Matching
      -> Project Story Extraction
      -> Interview Preparation Plan
      -> Application Tracking
      -> Demo Report

## 2. Design Goals

CareerPilot is designed around five goals:

1. Keep the MVP runnable from the command line.
2. Keep tool outputs structured and testable.
3. Make matching and recommendations explainable.
4. Preserve a clear OpenHarness integration boundary.
5. Avoid overbuilding infrastructure before the workflow is stable.

## 3. System Components

### 3.1 OpenHarness Runtime Layer

OpenHarness provides the base agent framework and development environment.

CareerPilot currently uses or aligns with these OpenHarness capabilities:

| OpenHarness capability | CareerPilot usage |
|---|---|
| CLI / dry-run | Validates prompt assembly and workflow readiness through `oh --dry-run -p` |
| Skills | Uses markdown skills to describe career workflows |
| Tool-use pattern | Implements deterministic Python tools with stable schemas |
| Memory pattern | Stores application state in local JSON memory |
| Permission-aware workflow | Keeps file-based operations explicit and local |
| Testable Python structure | Adds CareerPilot tests under `tests/careerpilot/` |

### 3.2 CareerPilot Skill Layer

CareerPilot defines job-search workflows in markdown skill files:

- `careerpilot/skills/career-coach.md`
- `careerpilot/skills/resume-rewriter.md`
- `careerpilot/skills/interview-prep.md`

The skill layer describes:

- When the workflow should be used.
- What inputs are expected.
- Which tools should be involved.
- What output format should be produced.
- What safety boundaries should be followed.

The skill layer is intentionally separate from Python tool logic. This keeps workflow instructions readable and makes it easier to later connect the workflow to native OpenHarness tool registration.

### 3.3 CareerPilot Tool Layer

CareerPilot currently includes five main tool modules:

| Tool | File | Responsibility |
|---|---|---|
| JD Analyzer | `careerpilot/tools/jd_analyzer.py` | Parses job descriptions into structured role requirements |
| Resume Matcher | `careerpilot/tools/resume_matcher.py` | Compares resume evidence with JD requirements and produces an explainable score |
| Project Story Extractor | `careerpilot/tools/project_story_extractor.py` | Converts project descriptions into resume bullets and interview stories |
| Application Tracker | `careerpilot/tools/application_tracker.py` | Stores and updates local job application records |
| Interview Plan Generator | `careerpilot/tools/interview_plan_generator.py` | Generates 3-day or 7-day preparation plans based on gaps and focus areas |

The tools are deterministic in the MVP. This decision makes the demo stable, the tests reliable, and the output easier to inspect.

### 3.4 Adapter Layer

CareerPilot includes an OpenHarness-facing adapter:

- `careerpilot/openharness_adapter.py`

The adapter exists to provide a stable bridge between OpenHarness-style workflow prompts and the internal CareerPilot Python pipeline.

Current boundary:

- OpenHarness provides CLI prompt entrypoint and dry-run validation.
- CareerPilot provides deterministic tools and report generation.
- The adapter connects the two without changing the OpenHarness core agent loop.

This is a lightweight integration strategy for the MVP. Native OpenHarness tool registry integration is planned for a later iteration.

### 3.5 Demo Layer

The main end-to-end demo entrypoint is:

- `careerpilot/demo.py`

Typical command:

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

The demo reads local example files, runs the tool pipeline, and writes a Markdown report.

### 3.6 Memory Layer

CareerPilot uses local JSON memory for job application tracking:

- `careerpilot/memory/applications.json`

The MVP uses JSON instead of a database because the current goal is local inspectability, demo simplicity, and low setup cost.

The memory layer currently stores:

- Company
- Role
- JD source
- Application status
- Match score
- Next action
- Notes
- Created and updated dates

## 4. Data Flow

The main CareerPilot data flow is:

    User input files
      |
      v
    careerpilot/demo.py or careerpilot/openharness_adapter.py
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
    Markdown demo report and JSON memory update

## 5. Output Design

CareerPilot outputs are designed to be:

1. Structured: tools return stable fields.
2. Explainable: scores and gaps are tied to visible evidence.
3. Human-reviewable: resume suggestions are drafts, not final claims.
4. Testable: fields can be checked through pytest.
5. Demo-friendly: reports are readable as Markdown.

## 6. Testing Strategy

CareerPilot tests live under:

- `tests/careerpilot/`

The tests currently cover:

- JD keyword extraction
- Seniority detection
- Empty input handling
- Resume matching score behavior
- Missing skill detection
- Project bullet generation
- Application tracker add/update/query behavior
- Interview plan generation

Recommended command:

    python -m pytest -q tests/careerpilot

## 7. Current Integration Boundary

The current MVP does not claim full native OpenHarness tool registry integration.

Implemented:

- CareerPilot markdown skills.
- CareerPilot deterministic tools.
- CareerPilot local memory.
- End-to-end demo script.
- OpenHarness adapter command.
- OpenHarness dry-run validation.

Not yet implemented:

- Native OpenHarness tool registry registration.
- Live model-driven CareerPilot tool execution through OpenHarness.
- ohmo / IM channel integration.
- RAG-based resume and project knowledge base.
- Multi-agent workflow.

## 8. Why This Architecture

This architecture keeps the project realistic for a half-month MVP.

The main tradeoff is:

- Stability now: deterministic tools, JSON memory, CLI demo, adapter integration.
- Extensibility later: native tool registry, ohmo integration, RAG knowledge base, multi-agent workflow, benchmark evaluation.

This makes CareerPilot useful as both:

1. A runnable job-search workflow demo.
2. A foundation for a more advanced OpenHarness-based agent system.
