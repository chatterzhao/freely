# Candidates: worker session_id not written to agent_working

candidate_id: C-20260716T031047Z-A
status: promoted
source_raw: raw-20260716T031047Z
milestone: M-20260716T031047Z-A
---
## C-20260716T031047Z-A: Add raw_key extraction to capture_worker_session_id_and_store
- candidate_format_version: v2
- title: Extract raw_key from target_project path and use it for agent_working writes
- status: promoted
- decision_reason: Single function change, no call-site changes needed — simplest and least risky
- milestone: M-20260716T031047Z-A
- promoted_issue_id: I-20260716T031047Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260716T031047Z/issues/I-20260716T031047Z-A.md

### Changes
1. In `capture_worker_session_id_and_store()`: extract raw_key from `$target_project` via `grep -oE '[0-9]{8}T[0-9]{6}Z'`
2. Replace `'${agent_id}'` with `'${_raw_key}'` in `acp_session_register` call (L13082)
3. In pre-launch `agent_assign` (L13275): extract raw_key from `$target_project` and use instead of "develop"
