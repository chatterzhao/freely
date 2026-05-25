# Verification: protected-branch-merge-receipt-hardening

- issue_id: `I-20260402-1912-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- branch: `feature/protected-branch-merge-receipt-hardening-20260402-1912`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-1912-feature-protected-branch-merge-receipt-hardening`
- verification_date: `2026-04-02`
- verifier: `codex`
- verdict: `pass_for_verification`

## Scope Verdict

- `PASS`: this owner stays inside the narrow residual hardening slice and does not reopen break-glass whitelist policy or unrelated watchdog behavior.
- `PASS`: `governance-check` now enforces protected-branch break-glass trailer/ledger parity for trailer-bearing merges and rejects misuse of `legacy_backfill`.
- `PASS`: the break-glass ledger now distinguishes grandfathered ledger-only receipts from current trailer-bearing merges through explicit `source_branch` and `receipt_mode` truth.
- `PASS`: protected-branch completion can no longer be spoofed by setting `FREELY_*` env alone; hooks now require git-dir scoped guarded state aligned with `MERGE_HEAD`.
- `PASS`: the focused regressions preserve the current completion-only, initial-receipt, and staged merge-gate boundaries instead of deleting them to make the audit easier to satisfy.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
2. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
3. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
4. `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
5. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
6. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
7. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
8. `git diff --check`
9. `./bin/governance-check`

## Implementation Decision Note

- decision: `Close the residual protected-branch gap by pairing trailer/ledger parity audit with a harder guarded completion handshake, while leaving staged merge-gate coverage on its canonical regression rails.`
- why_this: `The remaining risk was not policy definition but two narrow runtime truths: audit parity and env-only completion spoofing. Tightening those closes the real gap without widening break-glass semantics or deleting existing guardrails.`
- alternatives_considered: `Considered stopping after parity alone and leaving handshake as future work, and considered restaging merge-gate runtime changes in the same patch. The former would leave a known spoof surface open; the latter would widen scope without new evidence because canonical staged/sibling regressions already pass.`
- boundary_non_goals: `This slice does not rewrite break-glass whitelist policy, does not relax merge_completion_only scope, does not absorb the unrelated watchdog revert, and does not change staged merge-gate runtime behavior without failing regression evidence.`
- residual_risk: `A future follow-on may still be needed only if new evidence shows a receipt gap beyond trailer parity, guarded completion handshake state, and the already-frozen staged merge-gate regression boundary.`

## Develop Absorption

- canonical_merge_commit: `see develop history`
- canonical_merge_target: `develop`
- post_merge_replay:
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
