---
schema_version: '1'
local_id: raw-20260807T114900Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260807T114900Z-A
platform_ids:
  github:
    issue_id: '4107'
    url: https://github.com/chatterzhao/freely/issues/4107
    synced_at: ''
  gitee:
    issue_id: IK787N
    url: https://gitee.com/zhaoquan/freely/issues/IK787N
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-08-07T11:49:00Z'
updated_at: '2026-11-03T06:11:46Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
promoted_children: []
source_candidate: ''
completed_at: '2026-11-03T06:12:00Z'
closeout_note: ''
---
# fix: scan platform_adapter import broken, #3380 phantom-closed


workflow_kind: fix

## Symptom
`freely task-source-scan --project . --json` reports `platform_health: degraded`, reason `No module named 'platform_adapter'`, total=0. The discovery loop is blind: **87 open platform issues** (50 gitee + 37 github) are invisible to scan.

## Root cause
`docs/system/workspace/scripts/runtime/task-lifecycle-scan.py` uses direct import:
- line 451 (`_detect_platforms`): `from platform_adapter import configured_platforms`
- line 502 (`get_platform_open_issues`): `from platform_adapter import list_open_issue_records`
- line 548 (`get_all_platform_issue_states`): `from platform_adapter import _handlers, _safe`

But the file is named `platform-adapter.py` (hyphen), so Python import fails. `_detect_platforms` falls back to git remotes, but `get_platform_open_issues` returns `{"__degraded__": ...}` → scan degrades.

## History — governance chain break
- raw-20260623T022909Z (github #3380) covered this exact bug, marked `phase_state: absorbed` → `I-20260623T022909Z-A` `phase_state: completed`, platform issue closed.
- The ACTUAL code fix commit `2b2f4c77f` (replace direct imports with importlib `_get_pa()` loader) is **orphaned — never merged to develop** (`git merge-base --is-ancestor 2b2f4c77f develop` = false).
- A docs-only commit `3d67e39a1` (materialized issue docs, `Closes #3380`) IS in develop but does NOT touch task-lifecycle-scan.py. Issue closed without code fix → phantom closure.

## Expected fix
Reimplement the importlib loader against the CURRENT scan structure (file has been refactored since the June fix):
- Add `import importlib.util` + cached `_get_pa()` helper using `spec_from_file_location('platform_adapter', <sync>/platform-adapter.py)`.
- Replace the 3 direct imports (lines 451/502/548) with `_get_pa().<symbol>`.
- Prior art: orphaned commit `2b2f4c77f` + `e9962ba30` (may be recoverable via reflog/git fsck).

## Verification
- `freely task-source-scan --project /Users/zhaoyu/Downloads/code/my-freely/freely --json` → `platform_health` not degraded, `total > 0`, categories populated.
- Full dev workflow: B1→B2→dev(RED-GREEN)→test→pr-create-guarded→pr-merge-guarded→wt-close.
