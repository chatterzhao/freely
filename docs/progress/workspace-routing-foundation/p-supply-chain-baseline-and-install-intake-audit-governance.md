# Progress: supply-chain-baseline-and-install-intake-audit-governance

- issue_id: `I-20260401-0115-A`
- issue_path: `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/issues/supply-chain-baseline-and-install-intake-audit-governance.md`
- title: `Supply-chain baseline and install-intake audit governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/security-baseline-followthrough-and-closeout-20260401-0035`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260401-0035-feature-security-baseline-followthrough-and-closeout`
- updated_at: `2026-04-01`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Materialized the next real residual security capability slice instead of leaving it implied under the earlier baseline umbrella.
- Added a canonical supply-chain audit for lockfile presence, direct dependency intake, explicit lifecycle allowlist enforcement, and mutable GitHub Action refs.
- Wired the same audit into `freely doctor`.
- Taught `freely init` to seed the repo-scoped lifecycle allowlist file so new repos satisfy the baseline contract without manual file creation.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-check-supply-chain-baseline`
2. `bash docs/system/workspace/scripts/tests/test-freely-doctor-supply-chain-gate`
3. `bash docs/system/workspace/scripts/tests/test-freely-doctor-execution-boundary-audit`
4. `bash docs/system/workspace/scripts/tests/test-freely-hook-gate`
5. `bash docs/system/workspace/scripts/tests/test-freely-chat-and-tui`
6. `docs/epics/workspace-routing-foundation/supply-chain-baseline-and-install-intake-audit-governance/code-reviews/20260401-supply-chain-baseline-and-install-intake-audit-verification.md`
7. `./bin/governance-check`

## Next Action

1. Sync with latest `develop` before final merge if upstream has advanced.
2. Merge this owner to `develop`.
3. Write back canonical closeout evidence and move the milestone entry to `completed_issues`.
