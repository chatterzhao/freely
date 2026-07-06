- issue_id: I-20260505T1210Z-A-C
- issue_path: docs/B2-docs/ibm/issue-state-refactor/raw-20260505T121000Zissues/I-20260505T1210Z-A-C.md
- phase_state: in_dev
- candidate_path: docs/B1-docs/raw-20260505T121000Z/candidates.md

Changes:
- governance-merge-gate: G1/G2/G3 consistency gates + S3 schema validation

Previous:
- I-20260505T1210Z-A: scan constants + migration (merged)
- I-20260505T1210Z-A-B: issue-sync platform_state fix (merged)

Migration (2026-05-05):
- bin/migrate-issue-phase-state: executed — 190 files migrated
- raw: status → phase_state, platform_state added
- I-*: status removed, platform_state added
- 2 raw: phase_state promoted → absorbed (illegal value fix)
