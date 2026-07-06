# Verification: test-pre-merge-family-promotion-gate-enforcement-governance

- issue_id: `I-20260405-1805-A`
- issue_path: `docs/B2-docs/gate/test-pre-merge-family-promotion-gate-enforcement-governance/raw-20260405-1805issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- branch: `feature/testing-lane-guidance-20260405-1545`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-1545-feature-testing-lane-guidance`
- verification_date: `2026-04-05`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: active governance truth sources now agree that `develop` normally promotes from `test-pre-merge-*` and `hotfix/*`, not directly from `feature/*`.
- `PASS`: merge-time enforcement and ancestry audit both consume the same source-branch policy, so the repo no longer keeps two normal develop-entry paths alive.
- `PASS`: the change remains narrow to promotion-gate enforcement and does not claim lifecycle automation or batch UX landed.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
2. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
3. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
4. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
5. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
6. `./bin/governance-check`
7. `git diff --check`

## Implementation Decision Note

- decision: `Update the guarded merge source policy and the protected-ancestry receipt audit in the same transaction, with the same effective-date compatibility boundary.`
- why_this: `The underlying bug was policy drift between what merges were allowed now and what merge history was audited against. Treating them as one owner is the only way to keep protected-branch behavior coherent.`
- alternatives_considered: `Considered leaving governance-check permissive for compatibility and relying only on pr-merge-guarded going forward. That would allow old-style direct feature merges to remain silently acceptable in later protected ancestry, which defeats the user’s requirement that develop accept only tested premerge batches as the normal path.`
- boundary_non_goals: `This verification does not assert paired worktree creation, stale visualization, or multi-bundle manifest tooling.`
- residual_risk: `Direct raw git merges that bypass the guarded entrypoint can still create drift until all local workflows consistently use the enforced wrappers and hooks.`
