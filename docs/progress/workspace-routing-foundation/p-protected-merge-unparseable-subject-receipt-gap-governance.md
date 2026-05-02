# Progress: protected-merge-unparseable-subject-receipt-gap-governance

- issue_id: `I-20260411-0217-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- title: `Protected-merge unparseable-subject receipt-gap governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/protected-merge-unparseable-subject-gap-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-protected-merge-unparseable-subject-gap`
- updated_at: `2026-04-11`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner exists to define a stronger canonical contract for generic-subject protected-ancestry receipt gaps.
- The old subject-matched receipt-gap contract remains intentionally narrow and unchanged.
- Implementation is complete in the feature worktree: the ordinary receipt-gap ledger now has an explicit `unparseable_subject_ancestry` validation mode, `governance-check` validates it against absorbing protected merge truth, and the April 10 preferred-auth ancestry gaps are now registered canonically.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
2. `./bin/governance-check`
3. `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/code-reviews/20260411-protected-merge-unparseable-subject-receipt-gap-verification.md`
4. `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/code-reviews/20260411-protected-merge-unparseable-subject-receipt-gap-canonical-closeout-verification.md`
5. `git worktree list --porcelain`

## Next Action

1. `completed`
