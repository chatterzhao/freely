# Progress: protected-merge-unparseable-subject-receipt-gap-governance

- issue_id: `I-20260411-0217-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- title: `Protected-merge unparseable-subject receipt-gap governance`
- phase_state: `done_ibm`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/protected-merge-unparseable-subject-gap-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-protected-merge-unparseable-subject-gap`
- updated_at: `2026-04-11`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner exists to define a stronger canonical contract for generic-subject protected-ancestry receipt gaps.
- The old subject-matched receipt-gap contract remains intentionally narrow and unchanged.
- Implementation has not started yet; IBM materialization is now complete and the next step is focused regression expansion.

## Verification Evidence

1. `./bin/governance-check` currently fails on six generic-subject ancestry merges under `test-pre-merge-20260410-preferred-auth-fix`.
2. `docs/pre-brainstorms/20260411-0217--protected-merge-unparseable-subject-receipt-gap/brainstorms.md`
3. `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/pre-tests.md`

## Next Action

1. Add focused regression coverage for the new validation mode before changing `docs/system/workspace/scripts/quality/governance-check`.
