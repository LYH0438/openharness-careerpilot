# CareerPilot Demo Script

## Goal

This demo shows the end-to-end CareerPilot workflow:

JD -> JD Analysis -> Resume Matching -> Project Story Extraction -> Interview Preparation Plan -> Application Tracking

## Command

```bash
python -m careerpilot.demo \
  --jd examples/careerpilot/sample_jd_backend.md \
  --resume examples/careerpilot/sample_resume.md \
  --project examples/careerpilot/sample_project_readme.md \
  --output examples/careerpilot/demo_report.md
Expected Output

The command generates:

examples/careerpilot/demo_report.md

The report contains:

JD analysis report
Resume match report
Project story extraction result
3-day interview preparation plan
Application tracker summary
Demo Talking Points

CareerPilot is an end-to-end job-search workflow built on top of OpenHarness-style tool and skill design.

The workflow uses separate tools for different responsibilities:

JD Analyzer extracts structured role requirements.
Resume Matcher compares the resume against the JD.
Project Story Extractor turns project descriptions into resume-ready bullets.
Application Tracker stores local application state.

The output is a Markdown report that can be reviewed, copied into README, or used as a demo artifact.
