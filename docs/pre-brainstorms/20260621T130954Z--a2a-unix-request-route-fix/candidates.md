# c-20260621T130954Z-A

- candidate_id: C-20260621T130954Z-A
- title: Fix a2a_task.py _unix_request route stripping — _request → _rest_request for latest_manager/pending_delivery/launched_pids
- status: absorbed
- absorbed_into: `I-20260621T130954Z-A`
- promoted_issue_path: `docs/issues/I-20260621T130954Z-A/issue.md`
- decision_reason: Trivial fix (3 lines, 1 file) — same pattern as list()/create()/update(). Absorbed into I-20260621T130954Z-A for direct merge.
- next_action: Merge to develop and verify daemon worker launch
---

# Candidate: a2a_task.py _unix_request Route Stripping Fix

## Problem
`a2a_task.py` `_unix_request` method (L155) strips specific REST path segments like `/latest-manager`, `/pending-delivery`, `/launched-pids` before `_rpc_map` lookup, making dedicated entries dead code.

## Solution
Change 3 methods from `_request` to `_rest_request`.
