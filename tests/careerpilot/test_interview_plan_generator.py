from careerpilot.tools.interview_plan_generator import (
    InterviewPlanInput,
    format_interview_plan_markdown,
    generate_interview_plan,
)


def sample_input(days: int = 3) -> InterviewPlanInput:
    return InterviewPlanInput(
        target_role="Backend Engineer",
        available_days=days,
        daily_hours=2,
        jd_analysis={
            "core_skills": ["Python", "FastAPI", "PostgreSQL"],
            "interview_focus": [
                "API 设计与后端服务实现",
                "数据库设计、索引和性能优化",
            ],
        },
        resume_match={
            "missing_skills": ["Kubernetes", "CI/CD"],
            "weak_evidence": ["Resume lacks quantified impact."],
            "interview_preparation_topics": [
                "system design",
                "database optimization",
            ],
            "resume_keywords_to_add": ["REST API"],
        },
    )


def test_generate_three_day_plan_has_daily_deliverables():
    result = generate_interview_plan(sample_input(days=3))

    assert result.available_days == 3
    assert len(result.daily_plan) == 3
    assert all(day.deliverables for day in result.daily_plan)
    assert "Kubernetes" in result.priority_topics
    assert result.daily_plan[-1].title == "Mock Interview and Final Review"


def test_generate_seven_day_plan_is_supported():
    result = generate_interview_plan(sample_input(days=7))

    assert result.available_days == 7
    assert len(result.daily_plan) == 7
    assert result.daily_plan[-1].title == "Mock Interview and Final Review"


def test_markdown_output_contains_schedule_and_checklist():
    result = generate_interview_plan(sample_input(days=3))
    markdown = format_interview_plan_markdown(result)

    assert "# Interview Preparation Plan" in markdown
    assert "3 days × 2 hours/day" in markdown
    assert "## Final Checklist" in markdown