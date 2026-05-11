---
name: interview-prep
description: Generate interview preparation topics, study plans, project stories, and mock questions based on a JD and resume match report.
---

# Interview Prep Skill

## When to use

Use this skill when the user asks to:

- Prepare for an interview
- Generate a 3-day or 7-day interview plan
- Predict interview questions from a JD
- Prepare project stories
- Practice behavioral or technical answers

## Goal

Create a targeted interview preparation plan based on the target role, JD requirements, resume strengths, and missing skills.

## Inputs

- JD analysis report
- Resume match report
- Target role
- Available preparation days
- Daily available study hours
- User's project experience
- Weak areas or missing skills

## Workflow

1. Identify interview focus areas from the JD.
2. Use resume match results to separate strengths from gaps.
3. Prioritize topics by role relevance and weakness severity.
4. Generate a daily preparation plan.
5. Include concrete deliverables for each day.
6. Generate project story prompts using STAR format.
7. Generate likely technical and behavioral questions.

## Output Format

Return:

- Interview focus summary
- High-priority topics
- 3-day or 7-day preparation plan
- Daily tasks
- Daily deliverables
- Project stories to prepare
- Likely interview questions
- Final review checklist

## Plan Requirements

Each day should include:

- Main topic
- Study tasks
- Practice tasks
- Output deliverable

## Rules

- Keep the plan realistic for the available time.
- Prioritize gaps that are directly related to the JD.
- Do not encourage the user to fake experience.
- When a skill gap exists, suggest honest framing such as "familiar with", "currently learning", or "used in a demo project".
