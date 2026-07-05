---
local_id: I-20260621T130954Z-A
kind: I
phase_state: completed
source_candidate: `docs/B1-docs/raw-20260621T130954Z/candidates.md#c-20260621T130954Z-A`
verification_artifact_dir: docs/B1-docs/raw-20260621T130954Z
raw_refs:
  - raw-20260621T130954Z
candidate_refs:
  - C-20260621T130954Z-A
created_at: '2026-06-21T13:10:12Z'
updated_at: '2026-06-21T13:10:12Z'
---

# I-20260621T130954Z-A: Fix a2a_task.py _unix_request Route Stripping

## Summary

`a2a_task.py` `_unix_request` method strips specific REST path segments before `_rpc_map` lookup, causing `latest_manager()`, `pending_delivery()`, and `launched_pids()` to return empty results.

Fix: Use `_rest_request` instead of `_request` for these 3 methods.

## Acceptance Criteria

- `a2a_task.py latest-manager` returns dict with `task_id`
- `a2a_task.py list-pending-delivery` returns tasks list
- `a2a_task.py launched-pids` returns rows
- Worker launch pipeline functional after daemon restart
