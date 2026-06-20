---
local_id: I-20260620T083454Z-A
kind: fix
phase_state: dev_done
milestone: ""
source_candidate: docs/pre-brainstorms/20260620T083454Z--lifecycle-scan-phase-state/candidates.md#C-20260620T083454Z-A
canonical_issue_path: docs/issues/I-20260620T083454Z-A/issue.md
title: "fix: task-source-scan check phase_state before reporting incomplete"
created_at: "2026-06-20T09:50:00Z"
author: manager
parent_raw: raw-20260620T083454Z
implemented_in:
  branch: fix/raw-20260620T083454Z-scan-fix
  commits:
  - d7f3433e4
  - 2adaf04e5
  - c72a42683
verified_in:
  test_branch: test-pre-merge-20260620T083454Z-scan-fix
---

## Summary

Fix the lifecycle task-source-scan to check `phase_state` frontmatter before reporting items as incomplete.

## Changes

In `docs/system/workspace/scripts/runtime/task-lifecycle-scan.py`:
- Before reporting an item as `dev_worktree_missing`, `b1_brainstorm_missing`, etc.
- Check if `issue.md` frontmatter exists
- If yes, read `phase_state` field
- If `phase_state` is `absorbed/dropped/completed`, skip reporting as incomplete

## Verification

- [x] Code change committed on fix/raw-20260620T083454Z-scan-fix
- [ ] PR review needed
- [ ] merge to develop via PR
