# CareerPilot Benchmark Evaluation

This report evaluates CareerPilot JD analysis quality using lightweight deterministic metrics.

## Summary

- Cases: 3
- Average keyword recall: 0.4045
- Average schema validity: 0.875
- Average report completeness: 0.875
- Average overall score: 0.7182

## Case Results

| Case | Keyword Recall | Schema Validity | Report Completeness | Overall | Label |
|---|---:|---:|---:|---:|---|
| ai_agent_engineer.md | 0.25 | 0.875 | 0.875 | 0.6667 | fair |
| backend_api_engineer.md | 0.6 | 0.875 | 0.875 | 0.7833 | good |
| ml_platform_engineer.md | 0.3636 | 0.875 | 0.875 | 0.7045 | fair |

## Notes

- Keyword recall is based on expected benchmark keywords.
- Schema validity checks whether required JD analysis fields are present.
- Report completeness currently mirrors schema completeness and can be extended with richer content checks.
- This benchmark is intended for regression tracking, not absolute model quality measurement.
