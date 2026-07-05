# Verification: governance-check-protected-merge-history-source-policy-governance canonical closeout

- issue_path: `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- verified_in_branch: `develop`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely`
- verified_at: `2026-04-06`
- verifier: `codex`

## Scope

验证当前 owner 已通过 `test-pre-merge-* -> develop` canonical promote 路径吸收到主线，并且 canonical `develop` 上的治理审计不再被 nested pre-merge ancestry 污染。

## Evidence

1. Guarded promote path
   - `PASS`: `feature/governance-check-protected-merge-history-20260406-0045` merged into `test-pre-merge-20260406-0045-governance-check-history-source-policy` as `9d72147`, then that batch merged into `develop` as `f58cf65`.
2. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
   - `PASS`: canonical regression suite covers both direct invalid protected-branch receipts and the inherited-target nested merge scenario.
3. `./bin/governance-check`
   - `PASS`: canonical `develop` no longer revalidates internal batch merge `ab7a9b8` as if it landed directly on `develop`.

## Verdict

- The owner is complete on canonical `develop`: protected-branch receipt auditing now honors the effective merge target instead of all reachable merge ancestry.
- The focused regression and live governance audit both pass on canonical `develop`, so this owner can close without widening into unrelated merge-helper behavior.
