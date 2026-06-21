# c-20260621T130954Z-A

- candidate_id: C-20260621T130954Z-A
- title: Fix a2a_task.py _unix_request route stripping — _request → _rest_request for latest_manager/pending_delivery/launched_pids
- status: promoted
- promoted_issue_path: `docs/issues/I-20260621T130954Z-A/issue.md`
- decision_reason: _unix_request route stripping regex makes dedicated _rpc_map entries unreachable. Fix is trivial (3 lines, 1 file), same pattern as list()/create()/update().
- next_action: Merge to develop and verify daemon worker launch
---

# Candidate: a2a_task.py _unix_request Route Stripping Fix

## Problem
`a2a_task.py` `_unix_request` method (L155) strips specific REST path segments like `/latest-manager`, `/pending-delivery`, `/launched-pids` before `_rpc_map` lookup, making dedicated entries dead code. The generic `tasks/list` is called instead, returning wrong format.

This causes `latest_manager()` to return `{}`, breaking the worker launch pipeline.

## Solution
Change `latest_manager()`, `pending_delivery()`, and `launched_pids()` from `_request` (JSON-RPC) to `_rest_request` (raw HTTP), matching the pattern already used by `list()`, `create()`, `update()`.

## Verification
- `a2a_task.py latest-manager` returns dict with `task_id`
- Daemon starts → Manager exits → `worker_launch: enter` appears in log
- Workers transition from `submitted` to `working`
