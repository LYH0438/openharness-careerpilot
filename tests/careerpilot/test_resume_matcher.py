from careerpilot.tools.resume_matcher import ResumeMatchInput, match_resume


def test_match_resume_returns_valid_score():
    data = ResumeMatchInput(
        resume_text="Built Python API service with PostgreSQL database.",
        target_role="Backend Engineer",
        jd_analysis={
            "core_skills": ["Python", "FastAPI", "PostgreSQL"],
            "nice_to_have_skills": ["Kubernetes"],
            "responsibilities": ["API"],
            "keywords_for_resume": ["REST API", "CI/CD"],
            "interview_focus": ["system design"],
        },
    )

    result = match_resume(data)

    assert 0 <= result.match_score <= 100
    assert "Python" in result.strong_matches
    assert "FastAPI" in result.missing_skills
    assert "Kubernetes" in result.missing_skills


def test_empty_resume_raises_error():
    data = ResumeMatchInput(
        resume_text="",
        target_role="Backend Engineer",
        jd_analysis={"core_skills": ["Python"]},
    )

    try:
        match_resume(data)
        assert False
    except ValueError as exc:
        assert "resume_text cannot be empty" in str(exc)