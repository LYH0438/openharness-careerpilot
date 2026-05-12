import pytest

from careerpilot.tools.jd_analyzer import JDAnalysisInput, SeniorityLevel, analyze_jd


def test_analyze_backend_jd_extracts_core_skills():
    jd = """
    We are looking for a Backend Engineer with 3+ years of experience.
    Build REST API services using Python, FastAPI, PostgreSQL, Redis and Docker.
    Kubernetes and AWS are nice to have.
    """

    result = analyze_jd(
        JDAnalysisInput(
            job_description=jd,
            target_role="Backend Engineer",
            language="zh-CN",
        )
    )

    assert result.seniority_level == SeniorityLevel.mid
    assert "Python" in result.core_skills
    assert "FastAPI" in result.core_skills
    assert "PostgreSQL" in result.core_skills
    assert "REST API" in result.core_skills
    assert "Kubernetes" in result.nice_to_have_skills
    assert "AWS" in result.nice_to_have_skills
    assert result.interview_focus


def test_empty_jd_raises_error():
    with pytest.raises(Exception):
        analyze_jd(
            {
                "job_description": "",
                "target_role": "Backend Engineer",
                "language": "zh-CN",
            }
        )


def test_ai_agent_jd_extracts_agent_keywords():
    jd = """
    We are hiring an AI Agent Engineer to build LLM applications.
    The role involves tool calling, RAG pipelines, agent workflows, and Python services.
    Docker is preferred.
    """

    result = analyze_jd(
        {
            "job_description": jd,
            "target_role": "AI Agent Engineer",
            "language": "zh-CN",
        }
    )

    all_skills = result.core_skills + result.nice_to_have_skills

    assert "Python" in all_skills
    assert "LLM" in all_skills
    assert "Agent" in all_skills
    assert "RAG" in all_skills
    assert any("LLM" in item or "Agent" in item for item in result.interview_focus)