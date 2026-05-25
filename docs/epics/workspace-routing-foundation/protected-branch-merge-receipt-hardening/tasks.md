# Tasks: protected-branch-merge-receipt-hardening

## Slice 1: IBM contract freeze

- [x] Materialize a focused owner instead of reusing the stale broad break-glass candidate.
- [x] Freeze the root staged patch classification and explicitly exclude watchdog revert.
- [x] Freeze the `merge_completion_only` boundary for break-glass.
- [x] Freeze the receipt trailer / ledger parity audit contract.
- [x] Freeze staged-view and sibling-context regression boundaries for `governance-merge-gate`.

## Slice 2: First implementation slice selection

- [x] Decide whether `receipt_ledger_parity_audit` is the first dev-loop slice.
- [x] If parity goes first, specify the exact audit fields and failure output.
- [x] Record why handshake hardening does not go first: parity audit is narrower, does not widen break-glass surface, and can harden canonical audit truth before touching runtime merge completion state.

## Slice 3: Dev-loop implementation

- [x] Implement the first focused repair without deleting current canonical regression tests.
- [x] Add or update regression coverage for whichever hook-point is changed.
- [x] Re-run `git diff --check` and `./bin/governance-check`.

## Slice 4: Guarded completion handshake hardening

- [x] Require protected-branch guarded completion to carry git-dir scoped handshake state, not just `FREELY_*` env.
- [x] Make `pre-commit` and `pre-merge-commit` validate target/source parity between guarded state and `MERGE_HEAD`.
- [x] Reject env-only break-glass spoof attempts in regression coverage.
- [x] Keep `merge_completion_only` semantics intact while tightening the handshake.

## Exit

- [x] IBM artifacts are sufficient to keep this owner in `in_ibm`.
- [x] Dev-loop may start only after the first implementation slice is unambiguous.
- [x] Residual protected-branch merge receipt hardening is implemented without reopening break-glass whitelist policy.

## Chosen First Slice

- first_slice: `receipt_ledger_parity_audit`
- scope_notes:
  - compare break-glass trailer fields to ledger truth for trailer-bearing merges
  - support explicit `legacy_backfill` receipts only for grandfathered history without canonical trailers
  - do not reopen handshake or staged-view changes in the same patch

## Verification Notes

- `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
- `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
- `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
- `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
- `git diff --check`
- `./bin/governance-check`
