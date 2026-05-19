# CareerPilot Agent Demo Script

This document provides a repeatable demo script for presenting CareerPilot Agent.

The goal is to show that CareerPilot is not only a collection of scripts, but a complete job-search workflow built around OpenHarness-style skills, tools, memory, structured outputs, and tests.

## 1. Demo Goal

The demo should prove that CareerPilot can take:

- A job description
- A resume
- A project description

And generate:

- A structured JD analysis
- A resume-job match report
- Missing skills and improvement suggestions
- Resume-ready project bullets
- A 3-day or 7-day interview preparation plan
- A local application tracking record
- A Markdown demo report

## 2. Recommended Demo Flow

### Step 1: Introduce the project

Say:

    CareerPilot Agent is a personalized job-search agent built on top of OpenHarness.
    It extends the OpenHarness-style workflow with career-focused skills, deterministic tools, local memory, structured reports, and tests.

Key points to mention:

- It is built as an OpenHarness extension, not a standalone unrelated script.
- It focuses on a concrete vertical workflow: job search.
- It covers the full loop from JD analysis to interview preparation and application tracking.

### Step 2: Show the project structure

Command:

    tree -L 3 careerpilot docs examples/careerpilot tests/careerpilot

If `tree` is not installed, use:

    find careerpilot docs examples/careerpilot tests/careerpilot -maxdepth 3 -type f | sort

Important directories to explain:

- `careerpilot/tools/`: deterministic tool modules
- `careerpilot/skills/`: markdown workflow skills
- `careerpilot/memory/`: local JSON application memory
- `examples/careerpilot/`: sample inputs and outputs
- `tests/careerpilot/`: unit tests
- `docs/`: architecture, integration notes, decisions, known issues, and demo script

### Step 3: Show the input files

Commands:

    cat examples/careerpilot/sample_jd_backend.md

    cat examples/careerpilot/sample_resume.md

    cat examples/careerpilot/sample_project_readme.md

Explain:

- The JD provides target role requirements.
- The resume provides user evidence.
- The project README provides material for resume bullets and interview stories.

### Step 4: Run the full demo

Command:

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

Expected result:

    examples/careerpilot/demo_report.md

### Step 5: Show the generated report

Command:

    cat examples/careerpilot/demo_report.md

Sections to highlight:

- Role summary
- Seniority level
- Core skills
- Nice-to-have skills
- Resume match score
- Strong matches
- Missing skills
- Rewrite suggestions
- Project resume bullets
- Interview preparation plan
- Application tracking summary

### Step 6: Show application memory

Command:

    cat careerpilot/memory/applications.json

Explain:

- CareerPilot stores local application records.
- This makes the agent stateful at the MVP level.
- The current storage is JSON for simplicity and inspectability.

### Step 7: Show OpenHarness integration boundary

Command:

    python -m careerpilot.openharness_adapter \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

Also show the OpenHarness dry-run command if available:

    uv run oh --dry-run -p "Use career-coach skill. Analyze examples/careerpilot/sample_jd_backend.md and compare it with examples/careerpilot/sample_resume.md. Generate a job-fit report using CareerPilot."

Explain:

- Current integration is lightweight and explicit.
- CareerPilot uses OpenHarness-style skills and a bridge adapter.
- Native OpenHarness tool registry integration is planned as a future improvement.

### Step 8: Run tests

Command:

    python -m pytest -q tests/careerpilot

Expected result:

    21 passed

Explain:

- Tests make the project more than a prompt demo.
- Core parsing, matching, project story extraction, application tracking, and interview planning logic are covered.

## 3. Two-Minute Presentation Script

CareerPilot Agent is a personalized job-search agent built on top of OpenHarness. The goal is to automate a real job-search workflow: analyze a job description, compare it with a resume, extract project stories, generate interview preparation plans, and track the application state.

I implemented the domain layer with several deterministic tools: a JD Analyzer, Resume Matcher, Project Story Extractor, Application Tracker, and Interview Plan Generator. I also added markdown skills to describe career workflows and local JSON memory to persist application records.

The current MVP uses a lightweight OpenHarness integration through markdown skills, dry-run validation, and an adapter module. This keeps the project stable while still aligning with OpenHarness concepts like skills, tools, memory, and CLI workflows.

For engineering quality, I added unit tests under `tests/careerpilot`, and the current CareerPilot test suite passes. The next phase would be native OpenHarness tool registration, ohmo chat integration, RAG-based resume knowledge, multi-agent workflow, and benchmark evaluation.

## 4. Five-Minute Presentation Structure

Use this structure for a longer interview explanation:

1. Problem:
   Manual resume tailoring is slow, repetitive, and inconsistent.

2. Why OpenHarness:
   OpenHarness already provides agent framework concepts such as skills, tools, memory, CLI entrypoints, and permission-aware workflows.

3. Architecture:
   CareerPilot adds a job-search domain layer on top of OpenHarness through skills, deterministic tools, local memory, and a demo pipeline.

4. Core tools:
   - JD Analyzer extracts role requirements.
   - Resume Matcher produces explainable match scoring.
   - Project Story Extractor generates resume bullets and interview stories.
   - Interview Plan Generator creates 3-day or 7-day prep plans.
   - Application Tracker stores local job application state.

5. Demo:
   Run the demo command and show the generated Markdown report.

6. Testing:
   Run `python -m pytest -q tests/careerpilot`.

7. Limitations:
   Current integration is lightweight, matching is heuristic, and resume suggestions require human review.

8. Next steps:
   Native OpenHarness tool registry, ohmo integration, RAG knowledge base, multi-agent workflow, benchmark evaluation, and safety policies.

## 5. Common Interview Questions

### Q1: Is this just a prompt wrapper?

No. The MVP includes deterministic Python tools, structured outputs, local memory, markdown skills, an end-to-end CLI workflow, and unit tests. The project uses prompts and skills as workflow definitions, but the core logic is implemented as testable modules.

### Q2: Why use deterministic tools instead of only LLM calls?

The MVP needs stable outputs for demo and testing. Deterministic tools make the project reliable and easier to debug. Later, an LLM layer can be added on top for richer language understanding.

### Q3: What exactly does OpenHarness provide here?

OpenHarness provides the base agent framework direction, CLI/dry-run workflow, skill-based organization, and concepts such as tools and memory. CareerPilot extends these concepts with a job-search domain workflow.

### Q4: What is the biggest limitation right now?

The biggest limitation is that CareerPilot tools are not yet fully registered as native OpenHarness runtime tools. Current integration is lightweight through skills, dry-run, and an adapter module.

### Q5: How would you improve it next?

The next improvements are native OpenHarness tool registration, chat integration through ohmo, RAG-based personal knowledge retrieval, multi-agent role separation, benchmark evaluation, and stronger safety policies.
