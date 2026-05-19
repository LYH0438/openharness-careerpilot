from __future__ import annotations

from pydantic import BaseModel, Field


class RewriteSuggestion(BaseModel):
    section: str
    before: str
    after: str


class ResumeMatchInput(BaseModel):
    resume_text: str
    jd_analysis: dict
    target_role: str = "Unknown"


class ResumeMatchOutput(BaseModel):
    match_score: int = Field(ge=0, le=100)
    strong_matches: list[str]
    missing_skills: list[str]
    weak_evidence: list[str]
    resume_keywords_to_add: list[str]
    rewrite_suggestions: list[RewriteSuggestion]
    interview_preparation_topics: list[str]


def _normalize(text: str) -> str:
    return text.lower().replace("-", " ").replace("_", " ")


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def _coverage(items: list[str], resume_text: str) -> tuple[list[str], list[str], float]:
    if not items:
        return [], [], 1.0

    normalized_resume = _normalize(resume_text)
    matched = [item for item in items if _normalize(item) in normalized_resume]
    missing = [item for item in items if item not in matched]
    score = len(matched) / len(items)

    return matched, missing, score


def _build_weak_evidence(
    project_score: float,
    resume_text: str,
    missing_core_skills: list[str],
    missing_responsibilities: list[str],
) -> list[str]:
    weak_evidence: list[str] = []

    if project_score < 0.5:
        weak_evidence.append(
            "Project experience lacks concrete implementation evidence. Add bullets that mention what you built, which technology you used, and what result it produced."
        )

    if not any(char.isdigit() for char in resume_text):
        weak_evidence.append(
            "Resume lacks quantified impact. Add measurable results such as latency reduction, API throughput, user scale, test coverage, or time saved."
        )

    if missing_core_skills:
        weak_evidence.append(
            "Core skill evidence is missing for: "
            + ", ".join(missing_core_skills[:4])
            + ". Add truthful project evidence instead of only listing them in the skills section."
        )

    if missing_responsibilities:
        weak_evidence.append(
            "Resume does not clearly address responsibilities: "
            + ", ".join(missing_responsibilities[:3])
            + ". Rewrite one project bullet to mirror these responsibilities."
        )

    return weak_evidence


def _build_rewrite_suggestions(
    target_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    resume_keywords_to_add: list[str],
    resume_text: str,
) -> list[RewriteSuggestion]:
    skill_phrase = ", ".join(matched_skills[:3]) or "relevant backend technologies"
    missing_phrase = ", ".join(missing_skills[:3]) or "the most important JD keywords"
    keyword_phrase = ", ".join(resume_keywords_to_add[:4]) or "role-specific keywords"

    suggestions = [
        RewriteSuggestion(
            section="Project Experience",
            before="Built a backend system.",
            after=(
                f"Built a backend-focused service for {target_role} roles using {skill_phrase}, "
                "owning API design, data modeling, and implementation trade-offs; "
                "add one measurable result such as request latency, reliability, user scale, or development time saved."
            ),
        ),
        RewriteSuggestion(
            section="Skills / Keywords",
            before="Listed general programming skills.",
            after=(
                f"Add targeted keywords such as {keyword_phrase}, but only when they are supported by real project or work experience."
            ),
        ),
        RewriteSuggestion(
            section="Gap Fix",
            before="Missing JD requirements are not addressed.",
            after=(
                f"Create or rewrite one bullet to provide evidence for {missing_phrase}; "
                "use the format: Built [feature] with [technology], solved [problem], and improved [metric/result]."
            ),
        ),
    ]

    if not any(char.isdigit() for char in resume_text):
        suggestions.append(
            RewriteSuggestion(
                section="Impact Metrics",
                before="Project bullets describe work without numbers.",
                after=(
                    "Add at least one quantified result, for example: reduced manual analysis time by X%, "
                    "processed N records, supported N users, improved test coverage to X%, or shortened workflow time from A to B."
                ),
            )
        )

    return suggestions


def match_resume(data: ResumeMatchInput) -> ResumeMatchOutput:
    if not data.resume_text.strip():
        raise ValueError("resume_text cannot be empty")

    core_skills = data.jd_analysis.get("core_skills", [])
    nice_to_have = data.jd_analysis.get("nice_to_have_skills", [])
    responsibilities = data.jd_analysis.get("responsibilities", [])
    keywords = data.jd_analysis.get("keywords_for_resume", [])
    interview_focus = data.jd_analysis.get("interview_focus", [])

    matched_skills, missing_core_skills, skill_score = _coverage(
        core_skills, data.resume_text
    )

    matched_responsibilities, missing_responsibilities, responsibility_score = _coverage(
        responsibilities, data.resume_text
    )

    project_evidence_terms = [
        "project",
        "built",
        "developed",
        "implemented",
        "designed",
        "optimized",
        "deployed",
        "api",
        "database",
        "service",
    ]

    _, _, project_score = _coverage(project_evidence_terms, data.resume_text)

    raw_score = (
        skill_score * 0.45
        + project_score * 0.35
        + responsibility_score * 0.20
    )
    match_score = max(0, min(100, round(raw_score * 100)))

    missing_nice_to_have = [
        skill for skill in nice_to_have
        if _normalize(skill) not in _normalize(data.resume_text)
    ]

    missing_skills = _dedupe(missing_core_skills + missing_nice_to_have)

    resume_keywords_to_add = [
        keyword for keyword in keywords
        if _normalize(keyword) not in _normalize(data.resume_text)
    ]

    weak_evidence = _build_weak_evidence(
        project_score=project_score,
        resume_text=data.resume_text,
        missing_core_skills=missing_core_skills,
        missing_responsibilities=missing_responsibilities,
    )

    rewrite_suggestions = _build_rewrite_suggestions(
        target_role=data.target_role,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        resume_keywords_to_add=resume_keywords_to_add,
        resume_text=data.resume_text,
    )

    interview_topics = _dedupe(
        interview_focus
        + missing_skills[:3]
        + missing_responsibilities[:2]
        + resume_keywords_to_add[:2]
    )

    return ResumeMatchOutput(
        match_score=match_score,
        strong_matches=_dedupe(matched_skills + matched_responsibilities),
        missing_skills=missing_skills,
        weak_evidence=weak_evidence,
        resume_keywords_to_add=resume_keywords_to_add,
        rewrite_suggestions=rewrite_suggestions,
        interview_preparation_topics=interview_topics,
    )


if __name__ == "__main__":
    sample = ResumeMatchInput(
        resume_text="Built Python API service with PostgreSQL database.",
        target_role="Backend Engineer",
        jd_analysis={
            "core_skills": ["Python", "FastAPI", "PostgreSQL"],
            "nice_to_have_skills": ["Kubernetes", "AWS"],
            "responsibilities": ["design backend services", "maintain API"],
            "keywords_for_resume": ["REST API", "CI/CD", "distributed systems"],
            "interview_focus": ["system design", "database optimization"],
        },
    )

    print(match_resume(sample).model_dump_json(indent=2))
