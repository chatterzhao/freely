---
local_id: I-20260503T0901Z-timezone-standardize
kind: linked
status: in_dev
phase_state: in_dev
source_candidate: docs/pre-brainstorms/20260503-0901--timezone-standardize/candidates.md
promoted_from: raw-20260503-0901
platform_ids:
  github:
    issue_id: "179"
    url: "https://github.com/chatterzhao/freely/issues/179"
primary_platform: github
created_at: "2026-05-03T09:01:00Z"
updated_at: "2026-05-03T09:17:00Z"
pre_tests_path: docs/epics/timezone-standardization/pre-tests.md
canonical_issue_path: docs/epics/timezone-standardization/issues/I-20260503T0901Z-timezone-standardize.md
---
# I-20260503T0901Z-timezone-standardize: Standardize timezone rendering across all 7 locations

- issue_id: `I-20260503T0901Z-timezone-standardize`
- title: `standardize timezone rendering across the entire system`
- status: `in_dev`
- priority: `P0`
- milestone: `M-timezone-standardization`
- phase_state: `in_dev`
- source_candidate: `docs/pre-brainstorms/20260503-0901--timezone-standardize/candidates.md`
- promoted_from: `raw-20260503-0901`
- verification_artifact_dir: `docs/epics/timezone-standardization/code-reviews`

## Summary

Standardize all timestamp rendering to UTC+Z (ISO 8601 with Z suffix). Seven locations need changes:

1. Issue keys: `raw-YYYYMMDD-HHMM` → `raw-YYYYMMDDThhmmZ`
2. Branch/worktree names: `feature/raw-YYYYMMDD-HHMM-slug` → `feature/raw-YYYYMMDDThhmmZ-slug`  
3. Logs: `acp-bridge.py` missing timezone suffix
4. Doc metadata: frontmatter `created_at`/`updated_at` format consistency
5. Tags: `YYYY.MM.DD-HHMM-stage` → `YYYY.MM.DD-HHMMZ-stage`
6. SQLite: `created_at` already correct (Z suffix present) — confirm only
7. Regex patterns: `\d{8}-\d{4}` → accept `\d{8}T\d{4,6}Z` with backward compat

## Per-location format

| Location | Old | New |
|----------|-----|-----|
| Issue keys | `raw-YYYYMMDD-HHMM` | `raw-YYYYMMDDThhmmZ` |
| Branch names | `raw-YYYYMMDD-HHMM` in path | `raw-YYYYMMDDThhmmZ` in path |
| Log timestamps | `YYYY-MM-DDThh:mm:ss` | `YYYY-MM-DDThh:mm:ssZ` |
| Doc frontmatter | various | `YYYY-MM-DDThh:mm:ssZ` (already correct in most places) |
| Tags | `YYYY.MM.DD-HHMM-stage` | `YYYY.MM.DD-HHMMZ-stage` |
| Regex | `\d{8}-\d{4}` | `\d{8}T\d{4,6}Z` + backward compat `\d{8}-\d{4}` |

## Files to change

- `docs/system/workspace/scripts/runtime/acp-bridge.py` (log ts)
- `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` (key extraction, regex)
- `docs/system/workspace/scripts/quality/governance-merge-gate` (branch validation, regex)
- `docs/system/workspace/scripts/worktree/wt-create` (issue key extraction)
- `docs/CONSTITUTION.md` (tag format)
- `docs/system/workspace/ibm-framework.md` (doc references)

## Backward compatibility

All regex must accept both old and new formats on read. Only NEW key generation uses the new format. Existing data (issue dirs, tags) with old format continue to work.
