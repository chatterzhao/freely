---
b1_id: B1-20260624T155212Z
phase_state: completed
source_raw: raw-20260624T155212Z
source_url: https://github.com/chatterzhao/freely/issues/3446
produced_candidate: C-20260624T155212Z-A
created_at: 2026-06-24
---

# B1_IBM: pretests-retirement-gate fallback for missing workcell-state.env

## Input
- raw issue: `docs/B1-docs/raw-20260624T155212Z/issue.md`
- GitHub issue #3446: pretests-retirement-gate fails immediately when workcell-state.env doesn't exist
- Worktree: fix/raw-20260624T155212Z-pretests-retirement-gate-fallback

## Problem
The `pretests-retirement-gate` script at `docs/system/workspace/scripts/quality/pretests-retirement-gate` exits with code 1 (line ~103) when `workcell-state.env` does not exist in the worktree being retired.

This `.freely/run/workcell-state.env` file is only created by the Worker execution framework. Manually-executed worktrees (without a Worker) never have this file. This means every manually-executed worktree must use `--force` to close, which bypasses the pre-tests validation entirely.

## Brainstorm

### Option A: Remove the check entirely
- Simply delete the state_file existence check
- Problem: then the downstream code references owner_issue and recorded_pre_tests from an empty env dict, causing cascading failures at lines 106-114

### Option B: Skip state-dependent checks when state_file missing
- Wrap lines 106-142 in `if state_file.exists():` block
- When state_file missing, proceed directly to scanning
- Problem: still needs to find the right issue and pre-tests to validate

### Option C: Fallback scan of worktree pre-tests.md (chosen)
- When state_file missing, scan `$WORKTREE_PATH/docs/epics/` for `**/pre-tests.md` files
- For each pre-tests.md, find the owning issue by matching `pre_tests_path` field in issue files
- Run `pretests-gate --project $WORKTREE_PATH --issue $issue_path` for each
- This directly validates the pre-tests without needing Worker metadata

## Decision: Option C — Fallback scan

**Rationale:**
1. Preserves the original validation path when Worker metadata exists (backward compatible)
2. Adds equivalent validation for the manual-execution path
3. Eliminates the `--force` requirement for manually-executed worktrees
4. No silent degradation — the fallback prints diagnostic messages and still fails if pre-tests are incomplete
5. The pretests-gate already handles all validation logic; the fallback just feeds it the right inputs from the worktree

## Implementation

Change in `docs/system/workspace/scripts/quality/pretests-retirement-gate`:

Replace the `if not state_file.exists(): sys.exit(1)` block (lines 103-105) with a fallback that:
1. Scans `$WORKTREE_PATH/docs/epics/**/pre-tests.md` for pre-tests files
2. For each, resolves the owning issue by matching the `pre_tests_path` field in issue files
3. Runs `pretests-gate --project $WORKTREE_PATH --issue <issue_path>` for each found issue
4. Exits 0 if all pass, 1 if any fail

## Candidate

- candidate_id: C-20260624T155212Z-A
- status: promoted
- milestone: M-20260624T155212Z-A
