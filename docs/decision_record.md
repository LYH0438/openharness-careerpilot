# CareerPilot Agent Decision Record

This document records important technical and product decisions made during the CareerPilot Agent MVP.

The goal is to make the project easier to review, maintain, and explain in interviews.

## DR-001: Why build CareerPilot on OpenHarness instead of from scratch?

### Decision

CareerPilot is built on top of OpenHarness instead of creating a new agent framework from scratch.

### Reason

OpenHarness already provides the base concepts needed for an agent system:

- Agent workflow
- Tool-use pattern
- Skill files
- Memory pattern
- CLI entrypoint
- Permission-aware execution
- Extensible project structure

CareerPilot focuses on domain specialization for job-search workflows instead of rebuilding generic agent infrastructure.

### Tradeoff

This decision makes the MVP faster to build and easier to connect with an existing agent framework.

The tradeoff is that CareerPilot needs to respect OpenHarness boundaries and may require additional work later to complete native tool registry integration.

## DR-002: Why start with deterministic tools instead of LLM-only tools?

### Decision

The MVP uses deterministic Python tools for JD analysis, resume matching, project story extraction, application tracking, and interview plan generation.

### Reason

The MVP needs stable outputs for:

- Demo reliability
- Unit testing
- Structured reports
- Repeatable examples
- Easier debugging

LLM-only output would be more flexible, but it would also be harder to test and more likely to produce inconsistent results.

### Tradeoff

Deterministic tools may be less flexible than an LLM in understanding unusual inputs.

The benefit is that the MVP can be tested with `pytest` and explained as an engineering project, not only as a prompt demo.

## DR-003: Why use local JSON memory instead of a database?

### Decision

CareerPilot stores application records in a local JSON file:

    careerpilot/memory/applications.json

### Reason

For the half-month MVP, local JSON is enough because:

- It requires no database setup.
- It is easy to inspect.
- It is easy to version in examples.
- It keeps the demo lightweight.
- It matches the current local CLI workflow.

### Tradeoff

JSON memory is not suitable for concurrent users, remote access, or complex querying.

A database can be introduced later if CareerPilot grows into a multi-user or web-based product.

## DR-004: Why use Markdown skills?

### Decision

CareerPilot uses Markdown skill files to describe career workflows.

Current skill files include:

    careerpilot/skills/career-coach.md
    careerpilot/skills/resume-rewriter.md
    careerpilot/skills/interview-prep.md

### Reason

Markdown skills make the workflow readable and easy to review.

They separate high-level task instructions from Python implementation details.

This also aligns CareerPilot with OpenHarness concepts such as skill-based workflow routing.

### Tradeoff

Markdown skills do not automatically guarantee deep runtime integration.

The MVP uses them as workflow definitions first, while deeper OpenHarness-native execution can be added later.

## DR-005: Why use an adapter layer for OpenHarness integration?

### Decision

CareerPilot includes a lightweight adapter:

    careerpilot/openharness_adapter.py

### Reason

The adapter gives CareerPilot a stable bridge to OpenHarness-style workflows without modifying the OpenHarness core agent loop.

This keeps the MVP lower risk.

The adapter allows the project to demonstrate OpenHarness alignment while keeping CareerPilot tools independently runnable and testable.

### Tradeoff

This is not the same as full native OpenHarness tool registry integration.

The native integration remains a future enhancement.

## DR-006: Why generate Markdown demo reports?

### Decision

The end-to-end demo generates a Markdown report:

    examples/careerpilot/demo_report.md

### Reason

Markdown is easy to read, easy to copy into documentation, and easy to show in GitHub.

It also helps the project serve both technical and career-oriented use cases.

The report can include:

- JD analysis
- Resume match score
- Missing skills
- Project resume bullets
- Interview preparation plan
- Application tracking summary

### Tradeoff

Markdown is not ideal for structured downstream processing.

For future automation, JSON outputs or schema-validated report objects can be added.

## DR-007: Why keep resume suggestions human-reviewable?

### Decision

CareerPilot treats generated resume suggestions as drafts that require human review.

### Reason

Resume content has an honesty and accuracy boundary.

The agent should help rewrite and organize real experience, but it should not fabricate experience, exaggerate skills, or produce final claims without review.

### Tradeoff

This reduces full automation.

The benefit is that it keeps the project safer and more realistic for real job-search use.

## DR-008: Why prioritize tests during the MVP?

### Decision

CareerPilot includes unit tests under:

    tests/careerpilot/

### Reason

Tests make the project more credible as a software engineering project.

They also protect the deterministic tool logic when new features are added.

Current tests cover the core pipeline, including JD analysis, resume matching, project story extraction, application tracking, and interview plan generation.

### Tradeoff

Writing tests takes additional time during a short MVP schedule.

The benefit is higher confidence and easier maintenance.

## DR-009: Why not build a web frontend in the MVP?

### Decision

The MVP does not include a web frontend.

### Reason

The current priority is to prove the job-search agent workflow first.

A frontend would add design, routing, deployment, and state management work before the core agent logic is fully mature.

### Tradeoff

The MVP is less product-like visually.

The benefit is that more time can be spent on tool design, workflow quality, documentation, tests, and OpenHarness alignment.

## DR-010: What is the next architectural direction?

### Decision

The next phase should improve CareerPilot from a CLI MVP into a more complete agent system.

### Planned directions

- Native OpenHarness tool registry integration
- ohmo / IM channel integration
- RAG-based resume and project knowledge base
- Multi-agent workflow
- Benchmark and quality evaluation
- Resume version management
- Safety and permission policies

### Reason

These improvements would make CareerPilot more realistic as an agent system and less like a standalone script collection.
