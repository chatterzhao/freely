---
id: C-20260623T022909Z-key: scan-import-fix
phase_state: promoted
promoted_issue_path: docs/issues/I-20260623T022909Z-A/issue.md
source: raw-20260623T022909Z
source_url: https://github.com/chatterzhao/freely/issues/3379
---

# Candidate: Fix task-lifecycle-scan.py import for platform-adapter

## Acceptance Criteria
1. `task-lifecycle-scan.py --project <project> --json` runs without ModuleNotFoundError
2. All three import sites (lines 19, 438, 474) are converted to importlib loading
3. Existing `platform-adapter.py` behavior is preserved (other callers unaffected)

## Promotion Gate
- [x] Code implemented and committed (`2b2f4c77f`)
- [x] Raw issue absorbed into I-20260623T022909Z-A
- [ ] PR created and merged to develop

## Open Questions
None.
