# Verification: protected-merge-unparseable-subject-receipt-gap-governance

- issue_id: `I-20260411-0217-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-merge-unparseable-subject-receipt-gap-governance/issues/protected-merge-unparseable-subject-receipt-gap-governance.md`
- verification_date: `2026-04-11`
- verifier: `codex`

## Scope Verdict

- `PASS`: `governance-check` now supports a distinct stronger-evidence path for generic-subject protected-ancestry receipt gaps.
- `PASS`: existing parseable-subject receipt-gap regressions still pass under the expanded test matrix.
- `PASS`: malformed generic-subject entries still fail closed when the absorbing merge or bounded evidence contract is wrong or incomplete.
- `PASS`: canonical `develop` ancestry gaps from the April 10 preferred-auth batch are now represented by explicit unparseable-subject entries instead of a hash-only bypass.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
2. `./bin/governance-check`

## Implementation Decision Note

- decision: `Add validation_mode unparseable_subject_ancestry to the existing ordinary receipt-gap ledger, and validate it against the absorbing protected merge plus bounded owner evidence.`
- why_this: `It preserves one canonical audit surface while keeping the old subject-matched semantics intact and fail-closed.`
- alternatives_considered: `A separate ledger for generic-subject ancestry gaps, and a hash-only exception path inside the existing ledger.`
- boundary_non_goals: `No weakening of future trailer requirements, no topology-only truth recovery, and no reopening of preferred-auth implementation scope.`
- residual_risk: `Future generic-subject ancestry gaps still require explicit bounded evidence and absorbing merge truth; this owner does not generalize to arbitrary malformed merge history.`
