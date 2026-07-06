# Verification: governance-check-protected-merge-history-source-policy-governance

- issue_path: `docs/B2-docs/gate/governance-check-protected-merge-history-source-policy-governance/raw-20260406-0045/issues/governance-check-protected-merge-history-source-policy-governance.md`
- verified_in_branch: `feature/governance-check-protected-merge-history-20260406-0045`
- verified_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-0045-feature-governance-check-protected-merge-history`
- verified_at: `2026-04-06`
- verifier: `codex`

## Scope

- prove nested `test-pre-merge-*` ancestry no longer fails `develop` source-policy auditing
- keep direct invalid `feature/* -> develop` rejection intact

## Evidence

1. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
   - 结果：通过
   - 说明：新增两个回归场景，分别覆盖 `develop` 不应误判 batch 内部 merge，以及当前 `test-pre-merge-*` 不应重新审计继承自 `develop` 的旧 promote merge。
2. `./bin/governance-check`
   - 结果：通过
   - 说明：当前 feature worktree 已不再复现 `develop` 对 merge commit `ab7a9b8` 的误报。
3. `git diff --check`
   - 结果：通过

## Verdict

- 当前修复已经证明 ordinary receipt 与 break-glass receipt 审计都会按 first-parent protected merge history 工作。
- canonical `develop` followthrough replay 仍需在 guarded merge 后再跑一轮，然后才能关闭本 owner。
