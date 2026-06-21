---
local_id: I-20260621T043842Z-A
kind: linked
phase_state: completed
source_candidate: docs/pre-brainstorms/20260621T043842Z--session-parent-project-export/candidates.md#C-20260621T043842Z-A
platform_ids: {}
primary_platform: github
canonical_issue_path: docs/pre-brainstorms/20260621T043842Z--session-parent-project-export/candidates.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-21T04:38:42Z'
updated_at: '2026-06-21T04:50:00Z'
intake_id: ''
author: claude
channel: claude
session_refs: []
source_raw: raw-20260621T043842Z
candidate_id: C-20260621T043842Z-A
milestone_id: M-20260621T043842Z-A
---

# I-20260621T043842Z-A: Worker Fork A2A Socket + JSON Parse + Scan Filter Fix

## Map

### PRD

Fix three compounding root causes of worker duplication observed during freely runtime:

1. **#3201 (A2A socket)**: Export `SESSION_PARENT_PROJECT` to worker fork env, have `_resolve_project()` check it
2. **#3200 (JSON parse)**: Fix 8 inline `json.load(sys.stdin)` sites that treated `{"rows": [...]}` as bare `[...]`
3. **#3202 (scan filter)**: Include `submitted`/`launched` states in active-worker check

### Pre-tests

- [ ] `worktree_has_active_worker` returns true when worker exists
- [ ] `manager_exit_contract_kind` returns `delegate_workers` only with real pending workers
- [ ] Worker fork session can call `a2a-exit` successfully
- [ ] Scan does not re-list raw_keys with existing submitted/launched workers
- [ ] `freely daemon start` completes without JSON parse error noise

### Tasks

- [x] `a2a_task.py` L32: `_resolve_project()` checks `SESSION_PARENT_PROJECT` env
- [x] `freely` L12498: export `SESSION_PARENT_PROJECT` in worker fork env
- [x] `freely` L12757-12769: `worktree_has_active_worker` - add `has-active-worker` fast path + fix JSON parse
- [x] `freely` L12279: `manager_record_worker_pid_for_launch` - fix JSON parse
- [x] `freely` L14654: `manager_exit_contract_kind` - fix JSON parse
- [x] `freely` L14731: `validate_manager_exit_contract_for_project` - fix JSON parse
- [x] `freely` L12946: `active-workers` - fix JSON parse
- [x] `freely` L12953: completed_count - fix JSON parse
- [x] `freely` L2171: `_db_exit_contract_field` worker path - fix JSON parse
- [x] `freely` L14615: `parse_a2a_task_json_reply` worker path - fix JSON parse
- [x] `freely` L14877: `worker_exit_contract_kind` - fix JSON parse
- [x] `freely` L16450: scan filter - add `submitted`/`launched` to active check

### Code Review

- issue_id: I-20260621T043842Z-A
- reviewer: claude
- verdict: pass
- summary: |
  All changes are straightforward bug fixes: JSON parse corrections (dict→list),
  env var export, and state check expansion. No new dependencies, no API changes.
  All fixes are backward compatible and site-local.
