---
name: resume-rewriter
description: Rewrite resume sections and project experience for a target job description while preserving truthfulness and evidence.
---

# Resume Rewriter Skill

## When to use

Use this skill when the user asks to:

- Rewrite resume bullets
- Tailor a resume for a specific JD
- Improve project descriptions
- Convert project notes into resume-ready content
- Generate Chinese or English resume bullets

## Goal

Rewrite resume content so that it better matches a target role while remaining truthful, evidence-based, and easy to review.

## Inputs

- Original resume text
- Target job description
- Target role
- Project notes or README
- Preferred language: English, Chinese, or bilingual
- Preferred format: STAR, XYZ, or concise bullet

## Workflow

1. Identify the target role and job requirements.
2. Extract the most relevant skills and responsibilities from the JD.
3. Locate resume sections that support those requirements.
4. Detect weak or vague bullets.
5. Rewrite bullets using action, technology, problem, and impact.
6. Add missing keywords only when supported by evidence.
7. Return before/after suggestions when possible.

## Bullet Templates

Chinese:

基于 [技术/框架] 实现 [功能/系统]，通过 [方法] 解决 [问题]，提升/缩短/支持 [结果]。

English:

Built [system/feature] using [technology], enabling [capability] and improving [metric/result].

## Output Format

Return:

- Summary of rewrite strategy
- Keywords to emphasize
- Before/after bullet suggestions
- Final resume-ready bullets
- Human review checklist

## Rules

- Do not fabricate metrics.
- Do not add technologies the user has not used.
- Do not overstate skill level.
- Prefer measurable impact when evidence exists.
- If no metric exists, use qualitative but concrete impact.
- Mark all generated content as draft content requiring human review.
