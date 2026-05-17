from pathlib import Path

from careerpilot.tools.resume_matcher import ResumeMatchInput, match_resume


resume_text = Path("examples/sample_resume.md").read_text(encoding="utf-8")

jd_analysis = {
    "role_summary": "Backend Engineer role focused on API development, database design, and production service reliability.",
    "seniority_level": "junior/mid",
    "core_skills": ["Python", "FastAPI", "PostgreSQL", "REST API"],
    "nice_to_have_skills": ["Kubernetes", "AWS", "CI/CD"],
    "responsibilities": ["design backend services", "maintain API", "database optimization"],
    "keywords_for_resume": ["RESTful API", "Docker", "PostgreSQL indexing", "CI/CD", "distributed systems"],
    "interview_focus": ["system design", "database optimization", "API performance"],
    "risk_notes": ["Resume should add more deployment and CI/CD evidence."]
}

result = match_resume(
    ResumeMatchInput(
        resume_text=resume_text,
        jd_analysis=jd_analysis,
        target_role="Backend Engineer",
    )
)

Path("examples/output_resume_match.md").write_text(
    "# Resume Match Output\n\n```json\n"
    + result.model_dump_json(indent=2)
    + "\n```\n",
    encoding="utf-8",
)

print("Generated examples/output_resume_match.md")