from __future__ import annotations

import argparse
from argparse import Namespace
from pathlib import Path

from careerpilot.demo import run_demo


def run_job_fit_report(
    jd: str,
    resume: str,
    project: str,
    output: str = "examples/careerpilot/demo_report.md",
    target_role: str = "Backend Engineer",
    company: str = "Example AI",
    language: str = "zh-CN",
) -> str:
    """
    OpenHarness-facing adapter for the CareerPilot end-to-end workflow.

    This function provides a stable Python entrypoint that can be called by:
    - OpenHarness shell/tool execution
    - future tool registry integration
    - local CLI demos

    It delegates the actual workflow execution to careerpilot.demo.run_demo.
    """
    args = Namespace(
        jd=jd,
        resume=resume,
        project=project,
        output=output,
        target_role=target_role,
        company=company,
        language=language,
    )

    run_demo(args)
    return str(Path(output))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="OpenHarness adapter for CareerPilot job-fit report generation."
    )

    parser.add_argument("--jd", required=True, help="Path to job description file.")
    parser.add_argument("--resume", required=True, help="Path to resume file.")
    parser.add_argument("--project", required=True, help="Path to project README file.")
    parser.add_argument(
        "--output",
        default="examples/careerpilot/demo_report.md",
        help="Path to generated Markdown report.",
    )
    parser.add_argument(
        "--target-role",
        default="Backend Engineer",
        help="Target role name.",
    )
    parser.add_argument(
        "--company",
        default="Example AI",
        help="Company name for application tracking.",
    )
    parser.add_argument(
        "--language",
        default="zh-CN",
        help="Output language.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = run_job_fit_report(
        jd=args.jd,
        resume=args.resume,
        project=args.project,
        output=args.output,
        target_role=args.target_role,
        company=args.company,
        language=args.language,
    )
    print(f"CareerPilot report generated via OpenHarness adapter: {output}")


if __name__ == "__main__":
    main()
