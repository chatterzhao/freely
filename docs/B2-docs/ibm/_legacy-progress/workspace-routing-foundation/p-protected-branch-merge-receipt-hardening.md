# Progress: protected-branch-merge-receipt-hardening

- issue_id: `I-20260402-1912-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- title: `Protected-branch merge receipt hardening`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/protected-branch-merge-receipt-hardening-closeout-20260402-2345`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-2345-feature-protected-branch-merge-receipt-hardening-closeout`
- updated_at: `2026-04-02`
- closure_status: `closed`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner narrows the residual protected-branch merge hardening that remained after the completed break-glass governance owner.
- The immediate job is to separate root staged signal from regression: merge receipt hardening is in scope, watchdog revert is not.
- The first dev-loop slice is `receipt_ledger_parity_audit`, with explicit `legacy_backfill` grandfathering for historical ledger-only receipts.
- The parity slice is now implemented: `governance-check` scans from an explicit day-floor, enforces trailer/ledger field parity for `trailer_parity`, and only allows ledger-only grandfathering when the receipt is explicitly marked `legacy_backfill`.
- The guarded completion slice is now implemented too: `pr-merge-guarded` writes git-dir scoped handshake state and protected-branch hooks reject env-only spoofed completion attempts.
- The staged merge-gate boundary remains covered by the existing canonical regression suite; no runtime change was required after rechecking `test-governance-merge-gate`.

## Verification Evidence

1. `git diff --check`
2. `./bin/governance-check`
3. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
4. `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
5. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
6. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
7. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
8. `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
9. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
10. `docs/B1-docs/raw-20260402-1912/brainstorms.md`
11. `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/brainstorms/b-protected-branch-merge-receipt-hardening.md`
12. `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/code-reviews/20260402-protected-branch-merge-receipt-hardening-verification.md`

## Next Action

1. Owner is complete on canonical `develop`.
2. Keep watchdog revert out of scope, and reopen only if a later narrow follow-on is needed beyond receipt parity, guarded completion handshake hardening, and the frozen staged merge-gate boundary.

## Closure Evidence

- closure_status: `completed-on-develop`
- closure_evidence:
  - `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/code-reviews/20260402-protected-branch-merge-receipt-hardening-verification.md`
  - `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-breakglass-hook-completion`
  - `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
  - `./bin/governance-check`
  - `develop` guarded merge absorption
