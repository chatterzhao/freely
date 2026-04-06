# Progress: governance-check-protected-merge-history-source-policy-governance

- issue_id: `I-20260406-0045-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- title: `Governance-check protected-merge history source policy governance`
- phase_state: `in_dev`
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

## Active Plan

1. Fix the protected-branch audit history traversal.
2. Pass the focused regression and replay `./bin/governance-check` on canonical `develop`.
