---
b1_id: B1-20260703T054629Z
phase_state: completed
source_raw: raw-20260703T054629Z
produced_candidate: C-20260703T054629Z-A
---

# B1_IBM: wt-close pretests gate passes wrong worktree path

## Problem
wt-close calls pretests-retirement-gate with `--worktree-path "$wt_path"` where `$wt_path` is the fix worktree. test-gate.env only exists in test-pre-merge worktrees. Gate always fails because fix worktree has no test evidence.

Same bug as pr-create-guarded (fixed in raw-20260703T003829Z).

## Decision
Find companion test-pre-merge by raw key timestamp, pass that path to gate. Block if test worktree not found.

## Candidate
- candidate_id: C-20260703T054629Z-A
- status: promoted
- milestone: M-20260703T054629Z-A
