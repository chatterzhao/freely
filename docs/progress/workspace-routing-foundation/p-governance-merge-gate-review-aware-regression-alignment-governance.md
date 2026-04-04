# Progress: governance-merge-gate-review-aware-regression-alignment-governance

- issue_id: `I-20260404-0232-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md`
- title: `Governance merge gate review-aware regression alignment governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/governance-merge-gate-diagnostic-alignment-20260404-023234`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-023234-feature-governance-merge-gate-diagnostic-alignment`
- updated_at: `2026-04-04`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Post-merge acceptance on canonical `develop` showed the mixed unresolved-candidate implementation regression now fails on missing staged review evidence because the fixture predates the review-artifact requirement.
- Reproducing the current path confirmed that once review evidence is present, this case is intentionally allowed under the active unresolved-candidate repair contract.
- The same inspection exposed a same-file borrowed-owner bypass for `promoted` / `absorbed` candidates, so this owner refreshes the fixture and restores the documented owner-binding block in one narrow lane.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
2. `git diff --check`
3. `./bin/governance-check`
4. `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`

## Next Action

1. Replay this narrow review-aware regression alignment lane into canonical `develop`.
2. Resume post-merge acceptance and push once develop stays green.
