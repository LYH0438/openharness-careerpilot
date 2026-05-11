---
name: career-coach
description: Analyze job descriptions, match resumes, rewrite project experience, generate interview preparation plans, and manage job application workflow.
---

# Career Coach Skill

## When to use

Use this skill when the user asks about:

- Job description analysis
- Resume tailoring
- Resume and JD matching
- Project experience rewriting
- Interview preparation
- Job application tracking
- CareerPilot Agent workflow

## Goal

Help the user complete a job-search workflow from job description understanding to resume optimization, project storytelling, interview preparation, and application status tracking.

## Inputs

The skill may use the following inputs:

- Target role
- Company name
- Job description text
- Resume text
- Project README or project notes
- User career profile
- Application status or next action

## Outputs

The skill should produce structured and actionable outputs:

- JD analysis report
- Resume match report
- Missing skills and evidence gaps
- Resume keywords to add
- Project resume bullets in Chinese and English
- Interview preparation topics
- 3-day or 7-day preparation plan
- Application tracking update when requested

## Workflow

1. Identify the target role, company, and user goal.
2. Parse the JD into core skills, responsibilities, seniority level, keywords, and interview focus.
3. Compare the JD requirements with the user's resume.
4. Identify strong matches, missing skills, weak evidence, and resume keywords to add.
5. Rewrite relevant project experience using clear impact-oriented bullets.
6. Generate an interview preparation plan based on the JD and resume gaps.
7. Save or update application status only when the user explicitly asks.

## Output Principles

- Prefer structured Markdown or JSON-like sections.
- Make suggestions specific and actionable.
- Do not exaggerate the user's experience.
- Do not invent projects, employers, metrics, or skills.
- Always mark resume suggestions as drafts requiring human review.
- Explain match scores with visible reasoning.
- Keep the workflow focused on job search and career preparation.

## Safety and Boundaries

Do not:

- Auto-apply to real jobs.
- Fill sensitive personal information without user confirmation.
- Fabricate work experience or credentials.
- Claim expertise not supported by the resume or project evidence.
- Modify files unless the user explicitly asks.
