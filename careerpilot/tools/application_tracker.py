"""Application Tracker Tool for CareerPilot.

This module stores and manages job application records in a local JSON file.
It provides a small persistent memory layer for the CareerPilot Agent.
python -m careerpilot.tools.application_tracker update \
  --company "Example AI" \
  --role "AI Agent Engineer" \
  --status "applied" \
  --next-action "prepare backend system design interview answers" \
  --note "已完成第一版简历投递"
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

DEFAULT_MEMORY_PATH = Path("careerpilot/memory/applications.json")

VALID_STATUSES = {
    "researching",
    "preparing",
    "applied",
    "interview",
    "offer",
    "rejected",
    "archived",
}

ACTIVE_STATUSES = {
    "researching",
    "preparing",
    "applied",
    "interview",
}


@dataclass
class ApplicationRecord:
    company: str
    role: str
    jd_source: str = ""
    status: str = "researching"
    match_score: int | None = None
    next_action: str = ""
    created_at: str = field(default_factory=lambda: date.today().isoformat())
    updated_at: str = field(default_factory=lambda: date.today().isoformat())
    notes: list[str] = field(default_factory=list)


def _validate_status(status: str) -> str:
    normalized = status.strip().lower()
    if normalized not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status: {status}. "
            f"Allowed statuses: {', '.join(sorted(VALID_STATUSES))}"
        )
    return normalized


def _validate_match_score(match_score: int | None) -> int | None:
    if match_score is None:
        return None
    if not 0 <= match_score <= 100:
        raise ValueError("match_score must be between 0 and 100.")
    return match_score


def _normalize_key(value: str) -> str:
    return value.strip().lower()


def load_applications(memory_path: Path | str = DEFAULT_MEMORY_PATH) -> list[dict[str, Any]]:
    path = Path(memory_path)

    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("[]", encoding="utf-8")
        return []

    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            return []
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON file: {path}. "
            "Please check the file format or restore it to an empty list: []."
        ) from exc

    if not isinstance(data, list):
        raise ValueError(f"Invalid application memory format: {path}. Expected a JSON list.")

    return data


def save_applications(
    applications: list[dict[str, Any]],
    memory_path: Path | str = DEFAULT_MEMORY_PATH,
) -> None:
    path = Path(memory_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(applications, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def find_application_index(
    applications: list[dict[str, Any]],
    company: str,
    role: str,
) -> int | None:
    company_key = _normalize_key(company)
    role_key = _normalize_key(role)

    for index, item in enumerate(applications):
        if (
            _normalize_key(str(item.get("company", ""))) == company_key
            and _normalize_key(str(item.get("role", ""))) == role_key
        ):
            return index

    return None


def add_application(
    company: str,
    role: str,
    jd_source: str = "",
    status: str = "researching",
    match_score: int | None = None,
    next_action: str = "",
    notes: list[str] | None = None,
    memory_path: Path | str = DEFAULT_MEMORY_PATH,
) -> dict[str, Any]:
    if not company.strip():
        raise ValueError("company cannot be empty.")
    if not role.strip():
        raise ValueError("role cannot be empty.")

    status = _validate_status(status)
    match_score = _validate_match_score(match_score)

    applications = load_applications(memory_path)

    existing_index = find_application_index(applications, company, role)
    if existing_index is not None:
        raise ValueError(f"Application already exists: {company} - {role}")

    record = ApplicationRecord(
        company=company.strip(),
        role=role.strip(),
        jd_source=jd_source.strip(),
        status=status,
        match_score=match_score,
        next_action=next_action.strip(),
        notes=notes or [],
    )

    record_dict = asdict(record)
    applications.append(record_dict)
    save_applications(applications, memory_path)

    return record_dict


def update_application(
    company: str,
    role: str,
    status: str | None = None,
    match_score: int | None = None,
    next_action: str | None = None,
    note: str | None = None,
    jd_source: str | None = None,
    memory_path: Path | str = DEFAULT_MEMORY_PATH,
) -> dict[str, Any]:
    applications = load_applications(memory_path)
    index = find_application_index(applications, company, role)

    if index is None:
        raise KeyError(f"Application not found: {company} - {role}")

    record = applications[index]

    if status is not None:
        record["status"] = _validate_status(status)

    if match_score is not None:
        record["match_score"] = _validate_match_score(match_score)

    if next_action is not None:
        record["next_action"] = next_action.strip()

    if jd_source is not None:
        record["jd_source"] = jd_source.strip()

    if note:
        record.setdefault("notes", [])
        record["notes"].append(note.strip())

    record["updated_at"] = date.today().isoformat()

    applications[index] = record
    save_applications(applications, memory_path)

    return record


def list_applications(
    status: str | None = None,
    memory_path: Path | str = DEFAULT_MEMORY_PATH,
) -> list[dict[str, Any]]:
    applications = load_applications(memory_path)

    if status is None:
        return applications

    normalized_status = _validate_status(status)
    return [
        item for item in applications
        if str(item.get("status", "")).strip().lower() == normalized_status
    ]


def get_todos(memory_path: Path | str = DEFAULT_MEMORY_PATH) -> list[dict[str, Any]]:
    applications = load_applications(memory_path)

    return [
        item for item in applications
        if str(item.get("status", "")).strip().lower() in ACTIVE_STATUSES
        and str(item.get("next_action", "")).strip()
    ]


def generate_today_tasks(memory_path: Path | str = DEFAULT_MEMORY_PATH) -> list[str]:
    todos = get_todos(memory_path)

    if not todos:
        return ["No pending job-search tasks for today."]

    tasks: list[str] = []

    for item in todos:
        company = item.get("company", "Unknown Company")
        role = item.get("role", "Unknown Role")
        status = item.get("status", "unknown")
        next_action = item.get("next_action", "")
        match_score = item.get("match_score")

        score_part = f" | match score: {match_score}" if match_score is not None else ""
        tasks.append(
            f"[{status}] {company} - {role}{score_part}: {next_action}"
        )

    return tasks


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="CareerPilot Application Tracker")
    parser.add_argument(
        "--memory",
        default=str(DEFAULT_MEMORY_PATH),
        help="Path to applications.json",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new application record")
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--jd-source", default="")
    add_parser.add_argument("--status", default="researching")
    add_parser.add_argument("--match-score", type=int, default=None)
    add_parser.add_argument("--next-action", default="")
    add_parser.add_argument("--note", action="append", default=[])

    update_parser = subparsers.add_parser("update", help="Update an application record")
    update_parser.add_argument("--company", required=True)
    update_parser.add_argument("--role", required=True)
    update_parser.add_argument("--status", default=None)
    update_parser.add_argument("--match-score", type=int, default=None)
    update_parser.add_argument("--next-action", default=None)
    update_parser.add_argument("--jd-source", default=None)
    update_parser.add_argument("--note", default=None)

    list_parser = subparsers.add_parser("list", help="List application records")
    list_parser.add_argument("--status", default=None)

    subparsers.add_parser("todos", help="List active records with next actions")
    subparsers.add_parser("today", help="Generate today's job-search tasks")

    args = parser.parse_args()
    memory_path = Path(args.memory)

    if args.command == "add":
        result = add_application(
            company=args.company,
            role=args.role,
            jd_source=args.jd_source,
            status=args.status,
            match_score=args.match_score,
            next_action=args.next_action,
            notes=args.note,
            memory_path=memory_path,
        )
        _print_json(result)

    elif args.command == "update":
        result = update_application(
            company=args.company,
            role=args.role,
            status=args.status,
            match_score=args.match_score,
            next_action=args.next_action,
            jd_source=args.jd_source,
            note=args.note,
            memory_path=memory_path,
        )
        _print_json(result)

    elif args.command == "list":
        result = list_applications(
            status=args.status,
            memory_path=memory_path,
        )
        _print_json(result)

    elif args.command == "todos":
        result = get_todos(memory_path=memory_path)
        _print_json(result)

    elif args.command == "today":
        for task in generate_today_tasks(memory_path=memory_path):
            print(f"- {task}")


if __name__ == "__main__":
    main()