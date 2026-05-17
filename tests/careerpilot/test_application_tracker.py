import json

import pytest

from careerpilot.tools.application_tracker import (
    add_application,
    generate_today_tasks,
    get_todos,
    list_applications,
    load_applications,
    update_application,
)


def test_add_application_creates_record(tmp_path):
    memory_path = tmp_path / "applications.json"

    record = add_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="preparing",
        match_score=78,
        next_action="rewrite project bullets",
        notes=["Need to emphasize OpenHarness tools."],
        memory_path=memory_path,
    )

    assert record["company"] == "Example AI"
    assert record["role"] == "AI Agent Engineer"
    assert record["status"] == "preparing"
    assert record["match_score"] == 78

    saved = json.loads(memory_path.read_text(encoding="utf-8"))
    assert len(saved) == 1


def test_add_application_rejects_duplicate(tmp_path):
    memory_path = tmp_path / "applications.json"

    add_application(
        company="Example AI",
        role="AI Agent Engineer",
        memory_path=memory_path,
    )

    with pytest.raises(ValueError, match="already exists"):
        add_application(
            company="Example AI",
            role="AI Agent Engineer",
            memory_path=memory_path,
        )


def test_update_application_changes_status_and_note(tmp_path):
    memory_path = tmp_path / "applications.json"

    add_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="preparing",
        memory_path=memory_path,
    )

    updated = update_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="applied",
        next_action="prepare interview stories",
        note="Submitted tailored resume.",
        memory_path=memory_path,
    )

    assert updated["status"] == "applied"
    assert updated["next_action"] == "prepare interview stories"
    assert "Submitted tailored resume." in updated["notes"]


def test_list_applications_filters_by_status(tmp_path):
    memory_path = tmp_path / "applications.json"

    add_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="preparing",
        memory_path=memory_path,
    )

    add_application(
        company="Old Corp",
        role="Backend Engineer",
        status="rejected",
        memory_path=memory_path,
    )

    preparing = list_applications(status="preparing", memory_path=memory_path)

    assert len(preparing) == 1
    assert preparing[0]["company"] == "Example AI"


def test_get_todos_returns_active_records_with_next_action(tmp_path):
    memory_path = tmp_path / "applications.json"

    add_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="preparing",
        next_action="rewrite project bullets",
        memory_path=memory_path,
    )

    add_application(
        company="Closed Corp",
        role="Backend Engineer",
        status="rejected",
        next_action="no action",
        memory_path=memory_path,
    )

    todos = get_todos(memory_path=memory_path)

    assert len(todos) == 1
    assert todos[0]["company"] == "Example AI"


def test_generate_today_tasks(tmp_path):
    memory_path = tmp_path / "applications.json"

    add_application(
        company="Example AI",
        role="AI Agent Engineer",
        status="interview",
        match_score=82,
        next_action="prepare system design questions",
        memory_path=memory_path,
    )

    tasks = generate_today_tasks(memory_path=memory_path)

    assert len(tasks) == 1
    assert "Example AI" in tasks[0]
    assert "prepare system design questions" in tasks[0]


def test_missing_file_returns_empty_list(tmp_path):
    memory_path = tmp_path / "missing" / "applications.json"

    applications = load_applications(memory_path)

    assert applications == []
    assert memory_path.exists()


def test_invalid_json_raises_readable_error(tmp_path):
    memory_path = tmp_path / "applications.json"
    memory_path.write_text("{bad json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON file"):
        load_applications(memory_path)


def test_invalid_status_is_rejected(tmp_path):
    memory_path = tmp_path / "applications.json"

    with pytest.raises(ValueError, match="Invalid status"):
        add_application(
            company="Example AI",
            role="AI Agent Engineer",
            status="waiting",
            memory_path=memory_path,
        )


def test_invalid_match_score_is_rejected(tmp_path):
    memory_path = tmp_path / "applications.json"

    with pytest.raises(ValueError, match="match_score must be between 0 and 100"):
        add_application(
            company="Example AI",
            role="AI Agent Engineer",
            match_score=120,
            memory_path=memory_path,
        )