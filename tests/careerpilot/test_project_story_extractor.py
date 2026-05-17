import pytest

from careerpilot.tools.project_story_extractor import extract_project_story


def test_extract_project_story_basic_fields():
    text = """
    CareerPilot Agent is built on OpenHarness using Python, Pydantic,
    custom tools, skills, memory, CLI workflows, JSON outputs, and pytest.
    """

    result = extract_project_story(
        project_text=text,
        target_role="AI Agent Engineer",
    )

    assert result.one_liner
    assert "Python" in result.tech_stack
    assert "OpenHarness" in result.tech_stack
    assert len(result.resume_bullets_cn) >= 1
    assert len(result.resume_bullets_en) >= 1
    assert result.interview_story.problem
    assert len(result.possible_interview_questions) >= 3


def test_extract_project_story_empty_input():
    with pytest.raises(Exception):
        extract_project_story(project_text="")


def test_extract_project_story_scoreless_stable_output():
    text = "A CLI tool that converts project README files into resume bullets."

    result = extract_project_story(
        project_text=text,
        target_role="Backend Engineer",
    )

    assert isinstance(result.tech_stack, list)
    assert isinstance(result.architecture_highlights, list)
    assert isinstance(result.resume_bullets_cn, list)
    assert isinstance(result.resume_bullets_en, list)