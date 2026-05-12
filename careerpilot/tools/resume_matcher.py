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
    return text.lower()


def _coverage(items: list[str], resume_text: str) -> tuple[list[str], list[str], float]:
    if not items:
        return [], [], 1.0

    normalized_resume = _normalize(resume_text)
    matched = [item for item in items if _normalize(item) in normalized_resume]
    missing = [item for item in items if item not in matched]
    score = len(matched) / len(items)

    return matched, missing, score


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

    missing_skills = missing_core_skills + [
        skill for skill in nice_to_have if _normalize(skill) not in _normalize(data.resume_text)
    ]

    weak_evidence = []
    if project_score < 0.5:
        weak_evidence.append("Project experience lacks concrete implementation evidence.")
    if not any(char.isdigit() for char in data.resume_text):
        weak_evidence.append("Resume lacks quantified impact or measurable results.")
    if missing_responsibilities:
        weak_evidence.append(
            "Resume does not clearly address responsibilities: "
            + ", ".join(missing_responsibilities[:3])
        )

    resume_keywords_to_add = [
        keyword for keyword in keywords
        if _normalize(keyword) not in _normalize(data.resume_text)
    ]

    rewrite_suggestions = [
        RewriteSuggestion(
            section="Project Experience",
            before="Built a backend system.",
            after=(
                f"Built a {data.target_role}-oriented backend service using "
                f"{', '.join(matched_skills[:3]) or 'relevant technologies'}, "
                "with clear ownership, technical decisions, and measurable impact."
            ),
        )
    ]

    interview_topics = list(dict.fromkeys(
        interview_focus + missing_skills[:3] + missing_responsibilities[:2]
    ))

    return ResumeMatchOutput(
        match_score=match_score,
        strong_matches=matched_skills + matched_responsibilities,
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