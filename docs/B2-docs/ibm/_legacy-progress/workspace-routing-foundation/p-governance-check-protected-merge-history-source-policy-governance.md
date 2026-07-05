# Progress: governance-check-protected-merge-history-source-policy-governance

- issue_id: `I-20260406-0045-A`
- issue_path: `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- title: `Governance-check protected-merge history source policy governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/governance-check-protected-merge-history-20260406-0045`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0045-feature-governance-check-protected-merge-history`
- updated_at: `2026-04-06`
- closure_status: `merged-and-verified`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- A valid `feature/* -> test-pre-merge-* -> develop` promotion had left canonical `develop` red because `governance-check` revalidated the batch-internal merge commit under develop-only source rules.
- This owner repaired protected-branch receipt auditing so it filters merge history by effective target branch, keeping direct invalid source-policy rejection intact.
- Canonical `develop` absorbed the fix through `test-pre-merge-20260406-0045-governance-check-history-source-policy` and guarded merge `f58cf65`, then passed post-merge governance replay.

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `./bin/governance-check`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0045-test-pre-merge-governance-check-history-source-policy --issue docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`

## Closure Evidence

- feature commits `ef79bda`, `bc2be26`, and `c0d6bb4`
- premerge merge `9d72147`
- develop merge `f58cf65`
- `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-implementation-decision.md`
- `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-verification.md`
- `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/code-reviews/20260406-governance-check-protected-merge-history-source-policy-canonical-closeout-verification.md`

## Next Action

- No further action in this owner unless canonical `develop` again lets inherited protected-branch merge ancestry poison source-policy auditing.
