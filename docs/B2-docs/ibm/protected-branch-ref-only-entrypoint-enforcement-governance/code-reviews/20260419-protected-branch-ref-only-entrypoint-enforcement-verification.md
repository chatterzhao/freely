# Verification: protected-branch-ref-only-entrypoint-enforcement-governance

- issue_id: `I-20260419-0210-A`
- issue_path: `docs/B2-docs/ibm/protected-branch-ref-only-entrypoint-enforcement-governance/issues/protected-branch-ref-only-entrypoint-enforcement-governance.md`
- verification_date: `2026-04-19`
- verifier: `codex`

## Commands

1. `bash docs/system/workspace/scripts/tests/test-reference-transaction-hook`
2. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
3. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
4. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
5. `git diff --check`
6. `./bin/governance-check`

## Results

1. `reference-transaction` blocked `git merge --ff-only` from advancing `develop` to a non-receipted feature commit before the protected ref moved.
2. The same hook still allowed a receipt-bearing protected merge commit to update a protected branch.
3. Existing guarded merge regressions remained green after the new ref gate was added.
4. Repository governance checks remained green after the new hook, regression, and owner writeback.

## Verdict

`AT-001`, `AT-002`, and `AT-003` are satisfied: protected-branch ref-only entrypoint drift is now blocked locally without breaking canonical receipt-bearing protected merge commits.

## Implementation Decision Note

- decision: `Close the protected-branch ff-only gap at the reference-transaction boundary instead of trying to stretch pre-merge-commit beyond merge-commit creation.`
- why_this: `The reproduced failure moved the protected ref without creating a merge commit, so merge-commit hooks were the wrong enforcement surface. reference-transaction is the narrowest local gate that can fail the ref update before it lands.`
- alternatives_considered: `Rely on pre-push only; add post-merge rollback logic; reopen the earlier merge-commit owner and pretend the bug was already covered; widen into a server-side enforcement redesign.`
- boundary_non_goals: `This owner does not redesign push governance, receipt policy, or server-side protection. It only closes ref-only protected-branch entrypoint drift.`
- residual_risk: `A user with lower-level Git escape hatches could still mutate local repository state outside the normal hook path, but the ordinary protected-root ff-only misuse that escaped the prior owner is now fail-closed.`
