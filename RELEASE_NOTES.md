# v0.1-careerpilot-mvp

CareerPilot Agent v0.1 is a half-month MVP built on top of OpenHarness. It focuses on a complete job-search workflow: JD analysis, resume matching, project story extraction, interview preparation planning, and local application tracking.

## Added

- Career Coach Skill for job-search workflow orchestration.
- JD Analyzer Tool with structured requirement extraction.
- Resume Matcher Tool with explainable match scoring.
- Project Story Extractor for resume bullets and interview stories.
- Interview Plan Generator for 3-day and 7-day preparation plans.
- Local Application Tracker using JSON memory.
- End-to-end demo report generation.
- English and Chinese README documentation.
- Architecture, demo script, decision record, known issues, and development log documents.
- Unit tests for core CareerPilot tools.

## OpenHarness Integration

- Added CareerPilot domain skills under the project workspace.
- Added a lightweight OpenHarness adapter to expose CareerPilot workflow information.
- Verified dry-run level workflow checks through the OpenHarness `oh` entrypoint.
- Current v0.1 integration focuses on skills, workflow documentation, CLI execution, and project-level tool modules.

## Known Issues

- The current OpenHarness integration is at dry-run and adapter level; deeper native tool registry integration is planned for v0.2.
- The matching score is heuristic and designed for explainability, not benchmarked accuracy.
- Resume rewriting output still requires human review before real job applications.
- IM gateway integration through ohmo, Telegram, Slack, or Feishu is planned for v0.2.
- Current application memory uses local JSON files instead of a database.

## Demo

Run the end-to-end demo:

    python -m careerpilot.demo \
      --jd examples/careerpilot/sample_jd_backend.md \
      --resume examples/careerpilot/sample_resume.md \
      --project examples/careerpilot/sample_project_readme.md \
      --output examples/careerpilot/demo_report.md \
      --target-role "Backend Engineer" \
      --company "Example AI" \
      --prep-days 7 \
      --daily-hours 2

Run tests:

    python -m pytest -q tests/careerpilot

## Resume Bullet

Built CareerPilot Agent, a personalized job-search agent on top of OpenHarness, by extending custom tools, domain skills, local memory, structured outputs, and an end-to-end CLI workflow. Implemented JD parsing, resume-job matching, project story extraction, interview preparation planning, and application tracking with explainable scoring and test coverage.
