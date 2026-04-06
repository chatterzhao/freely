# Progress: governance-check-protected-merge-history-source-policy-governance

- issue_id: `I-20260406-0045-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- title: `Governance-check protected-merge history source policy governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/governance-check-protected-merge-history-20260406-0045`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0045-feature-governance-check-protected-merge-history`
- updated_at: `2026-04-06`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- A valid `feature/* -> test-pre-merge-* -> develop` promotion left canonical `develop` red because `governance-check` revalidated the batch-internal merge commit under develop-only source rules.
- This lane is narrowing the repair to first-parent protected merge history selection plus a focused regression.
- The code path and focused regression now pass in this feature worktree; the remaining step is canonical guarded promotion and develop followthrough replay.

## Active Plan

1. Guarded-merge this owner through a fresh `test-pre-merge-*` batch.
2. Replay `./bin/governance-check` on canonical `develop`.
