"""Evaluation metrics for CareerPilot benchmark reports.

This module provides lightweight deterministic metrics for CareerPilot v0.2.
The goal is not to create a perfect academic benchmark, but to make the agent
outputs inspectable, regression-testable, and easier to compare across cases.
"""

from __future__ import annotations

from typing import Any


def normalize_text(text: str) -> str:
    """Normalize text for simple keyword matching."""
    return text.lower().replace("-", " ").replace("_", " ")


def keyword_recall(extracted_keywords: list[str], expected_keywords: list[str]) -> float:
    """Calculate recall of expected keywords found in extracted keywords.

    Recall = matched expected keywords / all expected keywords.

    The matching is intentionally simple and deterministic. It uses normalized
    substring matching so terms such as "REST API" can match longer extracted
    phrases like "REST API design".
    """
    if not expected_keywords:
        return 1.0

    extracted_text = normalize_text(" ".join(str(item) for item in extracted_keywords))
    matched = 0

    for keyword in expected_keywords:
        if normalize_text(str(keyword)) in extracted_text:
            matched += 1

    return round(matched / len(expected_keywords), 4)


def schema_validity(report: dict[str, Any], required_fields: list[str]) -> float:
    """Return field presence score for required report fields.

    A field counts as present when:
    - the key exists in the report
    - the value is not None
    - the value is not an empty string
    - the value is not an empty list

    Empty dictionaries are considered missing as well.
    """
    if not required_fields:
        return 1.0

    missing_values = (None, "", [], {})
    present = 0

    for field in required_fields:
        if field in report and report[field] not in missing_values:
            present += 1

    return round(present / len(required_fields), 4)


def report_completeness(report: dict[str, Any], required_fields: list[str]) -> float:
    """Return report completeness score.

    Currently this mirrors schema_validity. It is kept as a separate metric so
    future versions can add richer content checks without changing the public
    metric interface.
    """
    return schema_validity(report, required_fields)


def average(values: list[float]) -> float:
    """Return the rounded average for a list of numeric values."""
    if not values:
        return 0.0

    return round(sum(values) / len(values), 4)


def score_to_label(score: float) -> str:
    """Convert a numeric score into a readable quality label."""
    if score >= 0.9:
        return "excellent"
    if score >= 0.75:
        return "good"
    if score >= 0.6:
        return "fair"
    return "needs_improvement"
