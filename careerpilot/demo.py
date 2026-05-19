from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


from careerpilot.tools.jd_analyzer import analyze_jd
from careerpilot.tools.resume_matcher import match_resume, ResumeMatchInput
from careerpilot.tools.project_story_extractor import extract_project_story
from careerpilot.tools.application_tracker import add_application, list_applications


def read_text(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")


def to_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value

    if hasattr(value, "model_dump"):
        return value.model_dump()

    if hasattr(value, "dict"):
        return value.dict()

    raise TypeError(f"Unsupported output type: {type(value)}")


def format_item(item: Any) -> str:
    if isinstance(item, dict):
        # Render common structured objects as readable Markdown instead of raw JSON.
        if {"section", "before", "after"}.issubset(item.keys()):
            return (
                f"**{item.get('section', 'Suggestion')}**\n"
                f"  - Before: {item.get('before', 'N/A')}\n"
                f"  - After: {item.get('after', 'N/A')}"
            )

        if {"company", "role", "status", "match_score", "next_action"}.issubset(item.keys()):
            notes = item.get("notes", [])
            notes_text = ", ".join(notes) if isinstance(notes, list) else str(notes)
            return (
                f"**{item.get('company', 'Unknown Company')} — {item.get('role', 'Unknown Role')}**\n"
                f"  - Status: {item.get('status', 'unknown')}\n"
                f"  - Match Score: {item.get('match_score', 'N/A')}\n"
                f"  - Next Action: {item.get('next_action', 'N/A')}\n"
                f"  - Notes: {notes_text or 'None'}"
            )

        return json.dumps(item, ensure_ascii=False)

    return str(item)


def format_list(items: Any) -> str:
    if not items:
        return "- None"

    if isinstance(items, list):
        rendered_items = []
        for item in items:
            rendered = format_item(item)
            if "\n" in rendered:
                rendered_items.append(f"- {rendered}")
            else:
                rendered_items.append(f"- {rendered}")
        return "\n".join(rendered_items)

    return f"- {format_item(items)}"


def pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def build_interview_plan(
    jd_analysis: Dict[str, Any],
    resume_match: Dict[str, Any],
) -> str:
    focus_topics = resume_match.get("interview_preparation_topics", [])
    missing_skills = resume_match.get("missing_skills", [])
    interview_focus = jd_analysis.get("interview_focus", [])

    day1_topics = focus_topics[:3] or interview_focus[:3]
    day2_topics = missing_skills[:3]
    day3_topics = interview_focus[:3] or focus_topics[:3]

    return f"""
## 3-Day Interview Preparation Plan

### Day 1: Core Role Requirements

{format_list(day1_topics)}

Deliverable:
- Prepare 2 short project stories related to the target role.

### Day 2: Skill Gaps and Weak Evidence

{format_list(day2_topics)}

Deliverable:
- Write one STAR answer for each missing or weak skill.

### Day 3: Mock Interview and Resume Story

{format_list(day3_topics)}

Deliverable:
- Prepare a 2-minute self-introduction and 3 project deep-dive answers.
""".strip()


def build_report(
    jd_path: str,
    resume_path: str,
    project_path: str,
    jd_analysis: Dict[str, Any],
    resume_match: Dict[str, Any],
    project_story: Dict[str, Any],
    applications: List[Dict[str, Any]],
) -> str:
    interview_plan = build_interview_plan(jd_analysis, resume_match)

    interview_story = project_story.get("interview_story", {})
    if not isinstance(interview_story, dict):
        interview_story = {}

    return f"""
# CareerPilot End-to-End Demo Report

## Input Files

- JD: `{jd_path}`
- Resume: `{resume_path}`
- Project README: `{project_path}`

---

# 1. JD Analysis Report

## Role Summary

{jd_analysis.get("role_summary", "N/A")}

## Seniority Level

{jd_analysis.get("seniority_level", "unknown")}

## Core Skills

{format_list(jd_analysis.get("core_skills", []))}

## Nice-to-have Skills

{format_list(jd_analysis.get("nice_to_have_skills", []))}

## Responsibilities

{format_list(jd_analysis.get("responsibilities", []))}

## Keywords for Resume

{format_list(jd_analysis.get("keywords_for_resume", []))}

## Interview Focus

{format_list(jd_analysis.get("interview_focus", []))}

## Risk Notes

{format_list(jd_analysis.get("risk_notes", []))}

---

# 2. Resume Match Report

## Match Score

**{resume_match.get("match_score", "N/A")} / 100**

## Strong Matches

{format_list(resume_match.get("strong_matches", []))}

## Missing Skills

{format_list(resume_match.get("missing_skills", []))}

## Weak Evidence

{format_list(resume_match.get("weak_evidence", []))}

## Resume Keywords to Add

{format_list(resume_match.get("resume_keywords_to_add", []))}

## Rewrite Suggestions

{format_list(resume_match.get("rewrite_suggestions", []))}

## Interview Preparation Topics

{format_list(resume_match.get("interview_preparation_topics", []))}

---

# 3. Project Story Extraction

## One-liner

{project_story.get("one_liner", "N/A")}

## Tech Stack

{format_list(project_story.get("tech_stack", []))}

## Architecture Highlights

{format_list(project_story.get("architecture_highlights", []))}

## Resume Bullets CN

{format_list(project_story.get("resume_bullets_cn", []))}

## Resume Bullets EN

{format_list(project_story.get("resume_bullets_en", []))}

## Interview Story

Problem: {interview_story.get("problem", "N/A")}

Solution: {interview_story.get("solution", "N/A")}

Impact: {interview_story.get("impact", "N/A")}

## Possible Interview Questions

{format_list(project_story.get("possible_interview_questions", []))}

---

# 4. Interview Preparation Plan

{interview_plan}

---

# 5. Application Tracker Summary

{format_list(applications)}

---

# 6. Raw Structured Outputs

## JD Analysis JSON

{pretty_json(jd_analysis)}

## Resume Match JSON

{pretty_json(resume_match)}

## Project Story JSON

{pretty_json(project_story)}

---

# 7. Human Review Notice

This report is generated for drafting and preparation purposes. Please review all resume suggestions manually before using them in real applications.
""".strip()


def run_demo(args: argparse.Namespace) -> None:
    jd_text = read_text(args.jd)
    resume_text = read_text(args.resume)
    project_text = read_text(args.project)

    jd_analysis = to_dict(
        analyze_jd(
            {
                "job_description": jd_text,
                "target_role": args.target_role,
                "language": args.language,
            }
        )
    )

    resume_match = to_dict(
        match_resume(
            ResumeMatchInput(
                resume_text=resume_text,
                jd_analysis=jd_analysis,
                target_role=args.target_role,
            )
        )
    )

    project_story = to_dict(
        extract_project_story(
            project_text,
            args.target_role,
            "resume_and_interview",
        )
    )

    try:
        add_application(
            company=args.company,
            role=args.target_role,
            jd_source=args.jd,
            status="preparing",
            match_score=resume_match.get("match_score", 0),
            next_action="review generated demo report and rewrite project bullets",
            notes=["Generated from CareerPilot Day 7 demo flow."],
        )
    except Exception as exc:
        print(f"[Warning] Failed to add application record: {exc}")

    try:
        applications = list_applications()
    except Exception as exc:
        print(f"[Warning] Failed to list application records: {exc}")
        applications = []

    report = build_report(
        jd_path=args.jd,
        resume_path=args.resume,
        project_path=args.project,
        jd_analysis=jd_analysis,
        resume_match=resume_match,
        project_story=project_story,
        applications=applications,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Demo report generated: {output_path}")
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run CareerPilot end-to-end demo flow."
    )

    parser.add_argument(
        "--jd",
        required=True,
        help="Path to the job description markdown file.",
    )
    parser.add_argument(
        "--resume",
        required=True,
        help="Path to the resume markdown file.",
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Path to the project README markdown file.",
    )
    parser.add_argument(
        "--output",
        default="examples/careerpilot/demo_report.md",
        help="Output report path.",
    )
    parser.add_argument(
        "--target-role",
        default="Backend Engineer",
        help="Target role name.",
    )
    parser.add_argument(
        "--company",
        default="Example AI",
        help="Company name for application tracker.",
    )
    parser.add_argument(
        "--language",
        default="zh-CN",
        help="Output language.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    run_demo(parse_args())
