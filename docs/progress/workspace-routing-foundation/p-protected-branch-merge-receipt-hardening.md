# Progress: protected-branch-merge-receipt-hardening

- issue_id: `I-20260402-1912-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/issues/protected-branch-merge-receipt-hardening.md`
- title: `Protected-branch merge receipt hardening`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/protected-branch-merge-receipt-hardening-20260402-1912`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260402-1912-feature-protected-branch-merge-receipt-hardening`
- updated_at: `2026-04-02`
- closure_status: `open`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner narrows the residual protected-branch merge hardening that remained after the completed break-glass governance owner.
- The immediate job is to separate root staged signal from regression: merge receipt hardening is in scope, watchdog revert is not.
- The first dev-loop slice is `receipt_ledger_parity_audit`, with explicit `legacy_backfill` grandfathering for historical ledger-only receipts.
- The parity slice is now implemented: `governance-check` scans from an explicit day-floor, enforces trailer/ledger field parity for `trailer_parity`, and only allows ledger-only grandfathering when the receipt is explicitly marked `legacy_backfill`.
- The guarded completion slice is now implemented too: `merge-guarded` writes git-dir scoped handshake state and protected-branch hooks reject env-only spoofed completion attempts.
- The staged merge-gate boundary remains covered by the existing canonical regression suite; no runtime change was required after rechecking `test-governance-merge-gate`.

## Verification Evidence

1. `git diff --check`
2. `./bin/governance-check`
3. `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
4. `bash docs/system/workspace/scripts/tests/test-pre-commit-hook`
5. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
6. `bash docs/system/workspace/scripts/tests/test-merge-guarded`
7. `bash docs/system/workspace/scripts/tests/test-merge-guarded-breakglass-hook-completion`
8. `bash docs/system/workspace/scripts/tests/test-merge-guarded-hooked-initial-merge-receipt`
9. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
10. `docs/pre-brainstorms/20260402-1912--protected-branch-merge-receipt-hardening/brainstorms.md`
11. `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/brainstorms/b-protected-branch-merge-receipt-hardening.md`
12. `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-hardening/code-reviews/20260402-protected-branch-merge-receipt-hardening-verification.md`

## Next Action

1. Guardedly absorb this parity-and-handshake slice into `develop`.
2. Keep watchdog revert out of scope, and reopen only if a fresh residual gap appears beyond the now-landed parity and guarded-handshake hardening.
