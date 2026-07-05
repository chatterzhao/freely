# Verification: guarded-merge-followthrough-gap-closeout

- issue_id: `I-20260408-1205-A`
- issue_path: `docs/B2-docs/ibm/verification-contract-and-premerge-adequacy-governance/issues/verification-contract-and-premerge-adequacy-governance.md`
- verification_date: `2026-04-10`
- verifier: `codex`

## Scope Verdict

- `PASS`: the guarded `develop` merge completion path now executes the same downstream governance gate that `pre-merge-commit` owns, so `git merge --continue` can no longer bypass develop materialization checks.
- `PASS`: the new `completed` candidate provenance exemption stays narrow; it only applies to governance-only diffs whose candidate already points at a canonical owner issue and milestone closeout line.
- `PASS`: the metadata repairs for historical candidate provenance now align legacy candidate ids with the canonical owner issues that already closed them out.
- `PASS`: follow-on candidate `C-20260411-1417-B` remains absorbed by `I-20260408-1205-A`, and the canonical owner chain is now explicitly restated so stale-truth reconcile batches can carry lawful absorbed provenance in the same develop-bound diff.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
2. `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
3. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
4. `./bin/governance-check`
5. `git diff --check`

## Implementation Decision Note

- decision: `Have pre-commit delegate guarded develop merge completion into pre-merge-commit, and only exempt completed provenance repairs when the canonical owner line is already present.`
- why_this: `The actual bypass came from hook coverage, not from an intentionally relaxed policy. Guarded completion used pre-commit, but merge continuation did not reliably execute pre-merge-commit, so develop governance checks were silently skipped on the path that mattered.`
- alternatives_considered: `Treat the miss as historical-only and just patch metadata; broaden governance-only exemptions for all completed candidates; add a second standalone hook with duplicated develop gate logic.`
- boundary_non_goals: `This closeout does not make every governance edit auto-pass, and it does not relax owner-bound develop merges that still lack a canonical candidate -> issue -> milestone chain.`
- residual_risk: `If future protected-branch completion paths bypass both hooks entirely, this owner will not detect them without another runtime or git-entrypoint audit.`
