# Progress: protected-branch-ref-only-entrypoint-enforcement-governance

- issue_id: `I-20260419-0210-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/issues/protected-branch-ref-only-entrypoint-enforcement-governance.md`
- phase_state: `in_verification`
- runtime_state: `unavailable`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/protected-branch-ff-only-gate-20260419`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-protected-branch-ff-only-gate`
- updated_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The completed develop entrypoint owner only guarded merge-commit paths.
- A real protected-root replay showed `git merge --ff-only` still moved `develop` locally because no merge commit was created and `pre-merge-commit` never ran.
- The current repair adds a protected-branch `reference-transaction` gate so ref-only advances fail unless the new head is already a receipt-bearing protected merge commit.

## Current Evidence

1. `bash docs/system/workspace/scripts/tests/test-reference-transaction-hook` passes and reproduces the exact blocked `ff-only` path plus the allowed receipt-bearing merge case.
2. The new gate lives at `.githooks/reference-transaction` and `docs/system/workspace/hooks/reference-transaction.sh`.
3. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`, `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`, `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`, `git diff --check`, and `./bin/governance-check` all pass after the ref gate lands.
4. Hook documentation now records ref-only protected-branch enforcement separately from merge-commit gating.

## Next Action

1. Re-run the older guarded merge regressions plus `./bin/governance-check`.
2. Merge to `develop`, push, and retire the lane.
