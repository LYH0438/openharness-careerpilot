"""Run CareerPilot benchmark evaluation.

This runner evaluates JD analysis quality using deterministic checks:
- keyword recall
- output schema validity
- report completeness

It is intentionally lightweight so it can run locally without external services.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from careerpilot.evaluation.metrics import (
    average,
    keyword_recall,
    report_completeness,
    schema_validity,
    score_to_label,
)


ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = ROOT / "benchmarks"
JDS_DIR = BENCHMARK_DIR / "jds"
EXPECTED_KEYWORDS_PATH = BENCHMARK_DIR / "expected_keywords.json"
EVAL_REPORT_PATH = BENCHMARK_DIR / "eval_report.md"


JD_REQUIRED_FIELDS = [
    "role_summary",
    "seniority_level",
    "core_skills",
    "responsibilities",
    "keywords_for_resume",
    "interview_focus",
    "risk_notes",
]

JD_OPTIONAL_FIELDS = [
    "nice_to_have_skills",
]


def _load_json(path: Path) -> dict[str, Any]:
    """Load JSON from a UTF-8 encoded file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_text(path: Path) -> str:
    """Load text from a UTF-8 encoded file."""
    return path.read_text(encoding="utf-8")


def _normalize_result(result: Any) -> dict[str, Any]:
    """Normalize analyzer output into a dictionary."""
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if hasattr(result, "dict"):
        return result.dict()
    if isinstance(result, dict):
        return result

    raise TypeError(f"Unsupported JD analyzer result type: {type(result)!r}")


def _run_jd_analyzer(jd_text: str, target_role: str = "Software Engineer") -> dict[str, Any]:
    """Call CareerPilot JD analyzer.

    The current CareerPilot JD analyzer uses a payload-style API:

        analyze_jd(payload: JDAnalysisInput | dict) -> JDAnalysisOutput

    This wrapper keeps the evaluation runner isolated from tool-level schema
    details and normalizes the output into a dictionary.
    """
    import careerpilot.tools.jd_analyzer as jd_analyzer

    payload = {
        "job_description": jd_text,
        "target_role": target_role,
        "language": "en",
    }

    if hasattr(jd_analyzer, "analyze_jd"):
        result = jd_analyzer.analyze_jd(payload)
        return _normalize_result(result)

    if hasattr(jd_analyzer, "analyze_job_description"):
        result = jd_analyzer.analyze_job_description(payload)
        return _normalize_result(result)

    if hasattr(jd_analyzer, "JDAnalyzer"):
        analyzer = jd_analyzer.JDAnalyzer()
        result = analyzer.analyze(payload)
        return _normalize_result(result)

    raise RuntimeError(
        "Cannot find a supported JD analyzer entrypoint. "
        "Expected analyze_jd, analyze_job_description, or JDAnalyzer.analyze."
    )

def _collect_extracted_keywords(report: dict[str, Any]) -> list[str]:
    """Collect keyword-like strings from a JD analysis report."""
    keywords: list[str] = []

    for field in [
        "core_skills",
        "nice_to_have_skills",
        "keywords_for_resume",
        "responsibilities",
        "interview_focus",
    ]:
        value = report.get(field, [])
        if isinstance(value, list):
            keywords.extend(str(item) for item in value)
        elif isinstance(value, str):
            keywords.append(value)

    return keywords


def evaluate_jd_case(jd_path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one JD benchmark case."""
    jd_text = _load_text(jd_path)
    target_role = jd_path.stem.replace("_", " ").title()
    report = _run_jd_analyzer(jd_text, target_role=target_role)

    expected_core = expected.get("core_keywords", [])
    expected_nice = expected.get("nice_to_have_keywords", [])
    expected_all = expected_core + expected_nice

    extracted_keywords = _collect_extracted_keywords(report)

    kw_recall = keyword_recall(extracted_keywords, expected_all)
    schema_score = schema_validity(report, JD_REQUIRED_FIELDS)
    completeness = report_completeness(report, JD_REQUIRED_FIELDS)
    overall = average([kw_recall, schema_score, completeness])

    return {
        "case": jd_path.name,
        "keyword_recall": kw_recall,
        "schema_validity": schema_score,
        "report_completeness": completeness,
        "overall": overall,
        "label": score_to_label(overall),
        "extracted_keywords": extracted_keywords,
    }


def run_evaluation() -> dict[str, Any]:
    """Run evaluation for all benchmark JD cases."""
    expected_keywords = _load_json(EXPECTED_KEYWORDS_PATH)

    case_results = []
    for jd_path in sorted(JDS_DIR.glob("*.md")):
        expected = expected_keywords.get(jd_path.name, {})
        case_results.append(evaluate_jd_case(jd_path, expected))

    summary = {
        "cases": len(case_results),
        "avg_keyword_recall": average([case["keyword_recall"] for case in case_results]),
        "avg_schema_validity": average([case["schema_validity"] for case in case_results]),
        "avg_report_completeness": average([case["report_completeness"] for case in case_results]),
        "avg_overall": average([case["overall"] for case in case_results]),
    }

    return {
        "summary": summary,
        "cases": case_results,
    }


def write_markdown_report(
    evaluation: dict[str, Any],
    output_path: Path = EVAL_REPORT_PATH,
) -> None:
    """Write evaluation result as a Markdown report."""
    summary = evaluation["summary"]
    cases = evaluation["cases"]

    lines = [
        "# CareerPilot Benchmark Evaluation",
        "",
        "This report evaluates CareerPilot JD analysis quality using lightweight deterministic metrics.",
        "",
        "## Summary",
        "",
        f"- Cases: {summary['cases']}",
        f"- Average keyword recall: {summary['avg_keyword_recall']}",
        f"- Average schema validity: {summary['avg_schema_validity']}",
        f"- Average report completeness: {summary['avg_report_completeness']}",
        f"- Average overall score: {summary['avg_overall']}",
        "",
        "## Case Results",
        "",
        "| Case | Keyword Recall | Schema Validity | Report Completeness | Overall | Label |",
        "|---|---:|---:|---:|---:|---|",
    ]

    for case in cases:
        lines.append(
            f"| {case['case']} | {case['keyword_recall']} | "
            f"{case['schema_validity']} | {case['report_completeness']} | "
            f"{case['overall']} | {case['label']} |"
        )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Keyword recall is based on expected benchmark keywords.",
            "- Schema validity checks whether required JD analysis fields are present.",
            "- Report completeness currently mirrors schema completeness and can be extended with richer content checks.",
            "- This benchmark is intended for regression tracking, not absolute model quality measurement.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """CLI entrypoint."""
    evaluation = run_evaluation()
    write_markdown_report(evaluation)

    print(json.dumps(evaluation["summary"], indent=2, ensure_ascii=False))
    print(f"Wrote benchmark report to {EVAL_REPORT_PATH}")


if __name__ == "__main__":
    main()
