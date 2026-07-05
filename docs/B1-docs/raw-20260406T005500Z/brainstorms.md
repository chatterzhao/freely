# Brainstorms - 20260406-0055--governance-check-nested-test-pre-merge-receipt-audit

## Context

Canonical promote now requires `feature/* -> test-pre-merge-* -> develop`, and the latest CLI packaging closeout followed that path:

- `ab7a9b8`: merge `feature/cli-command-audit-20260406-0015` into `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout`
- `8e0985b`: merge `test-pre-merge-20260406-0035-cli-wrapper-regression-closeout` into `develop`

Post-merge followthrough on `develop` then ran `./bin/governance-check` and got:

- `[FAIL] protected branch merge ab7a9b8... on develop has invalid Freely-Source-Branch 'feature/cli-command-audit-20260406-0015'.`

The failing commit is not a direct merge into `develop`; it is an internal merge inside the promoted `test-pre-merge-*` batch.

## Why This Is A New Follow-On

This is not the CLI packaging owner's scope. The repaired commands all behaved correctly on canonical `develop`.

It is also not the same as the older “missing trailer” receipt-gap family:

- `ab7a9b8` has a canonical guarded merge subject and belongs to the correct promote ancestry
- the failure is that ancestry audit is interpreting the nested merge in the wrong protected-branch context

So the new question is narrower:

1. When `develop` history contains a promoted `test-pre-merge-*` merge commit, how should ancestry audit treat internal feature -> `test-pre-merge-*` merges that are now ancestors of `develop` but were never direct merges into `develop`?

## Candidate Direction

Two plausible contract directions need comparison:

1. Only validate direct merges whose effective target branch is protected, and ignore nested internal merges whose effective target was another non-final batch branch.
2. Keep auditing nested merges, but recover the effective protected target/source pair from the merge receipt chain so `feature/* -> test-pre-merge-*` is validated against the `test-pre-merge-*` rules instead of the final `develop` rules.

## Non-Goals

- Do not reopen CLI wrapper packaging / auth wake scope.
- Do not rewrite merge history.
- Do not relax the canonical `test-pre-merge-* -> develop` promote model back to direct `feature/* -> develop`.
- Do not widen into generic merge-receipt ledger redesign unless this narrower audit decision proves impossible.

## Working Conclusion

This pre-brainstorm no longer needs an independent follow-on owner.

Canonical `develop` already absorbed and completed the fix under `I-20260406T004500Z-A`:

- protected-branch receipt auditing now follows first-parent protected merge history
- nested `feature/* -> test-pre-merge-*` merges are no longer revalidated against `develop`
- direct invalid `feature/* -> develop` receipts still fail

This entry remains as discovery provenance for the false positive on `ab7a9b8`, not as an active unresolved bug.
