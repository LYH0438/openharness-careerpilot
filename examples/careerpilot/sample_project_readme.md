# CareerPilot Agent

CareerPilot Agent is a personalized job-search agent built on OpenHarness.

It extends OpenHarness with custom tools, domain skills, local memory, and CLI demo workflows. The project focuses on JD analysis, resume matching, project story extraction, interview preparation planning, and application tracking.

## Tech Stack

- Python
- Pydantic
- OpenHarness
- LLM Tool Calling
- Markdown
- JSON
- pytest
- CLI

## Architecture

User input goes through the OpenHarness CLI or demo script. The Career Skill Router calls domain-specific tools such as JD Analyzer, Resume Matcher, Project Story Extractor, and Application Tracker. Outputs are saved as structured JSON or Markdown reports.

## Goal

The goal is to turn job descriptions, resumes, and project READMEs into actionable career reports, resume bullets, and interview preparation plans.