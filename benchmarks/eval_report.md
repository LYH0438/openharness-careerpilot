# CareerPilot Benchmark Evaluation

This report evaluates CareerPilot JD analysis quality using lightweight deterministic metrics.

## Summary

- Cases: 3
- Average keyword recall: 0.4045
- Average schema validity: 1.0
- Average report completeness: 1.0
- Average overall score: 0.8015

## Case Results

| Case | Keyword Recall | Schema Validity | Report Completeness | Overall | Label |
|---|---:|---:|---:|---:|---|
| ai_agent_engineer.md | 0.25 | 1.0 | 1.0 | 0.75 | good |
| backend_api_engineer.md | 0.6 | 1.0 | 1.0 | 0.8667 | good |
| ml_platform_engineer.md | 0.3636 | 1.0 | 1.0 | 0.7879 | good |

## Notes

- Keyword recall is based on expected benchmark keywords.
- Schema validity checks whether required JD analysis fields are present.
- Report completeness currently mirrors schema completeness and can be extended with richer content checks.
- This benchmark is intended for regression tracking, not absolute model quality measurement.
