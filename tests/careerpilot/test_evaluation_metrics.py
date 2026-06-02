from careerpilot.evaluation.metrics import (
    average,
    keyword_recall,
    report_completeness,
    schema_validity,
    score_to_label,
)


def test_keyword_recall_matches_expected_keywords():
    extracted = ["Python", "FastAPI", "PostgreSQL", "REST API"]
    expected = ["Python", "FastAPI", "Docker"]

    assert keyword_recall(extracted, expected) == 0.6667


def test_keyword_recall_returns_one_when_expected_is_empty():
    assert keyword_recall(["Python"], []) == 1.0


def test_keyword_recall_supports_substring_matching():
    extracted = ["REST API design", "Docker-based deployment"]
    expected = ["REST API", "Docker"]

    assert keyword_recall(extracted, expected) == 1.0


def test_schema_validity_returns_partial_score():
    report = {
        "role_summary": "Backend API role",
        "core_skills": ["Python"],
    }
    required = ["role_summary", "core_skills", "responsibilities", "risk_notes"]

    assert schema_validity(report, required) == 0.5


def test_schema_validity_treats_empty_values_as_missing():
    report = {
        "role_summary": "Backend API role",
        "core_skills": [],
        "responsibilities": "",
        "risk_notes": None,
    }
    required = ["role_summary", "core_skills", "responsibilities", "risk_notes"]

    assert schema_validity(report, required) == 0.25


def test_report_completeness_matches_required_fields():
    report = {
        "role_summary": "AI Agent role",
        "core_skills": ["Python", "LLM"],
        "risk_notes": [],
    }
    required = ["role_summary", "core_skills", "risk_notes"]

    assert report_completeness(report, required) == 0.6667


def test_score_to_label():
    assert score_to_label(0.95) == "excellent"
    assert score_to_label(0.8) == "good"
    assert score_to_label(0.65) == "fair"
    assert score_to_label(0.4) == "needs_improvement"


def test_average_empty_list():
    assert average([]) == 0.0


def test_average_values():
    assert average([1.0, 0.5]) == 0.75
