# Progress: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- issue_path: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- title: `Codex probe success shape and quota slot recovery governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-slot-recovery-network-failure`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`
- updated_at: `2026-04-12`
- follow_on_to: `I-20260410-1835-B`

## Summary

This bounded follow-on closes the remaining dogfood gap in the Codex recovery family: the `hi` probe now has one strict success shape, and reconnect-plus-403/quota failures now move forward to the next slot instead of stalling on the failed current slot.

## Implementation

- tightened the watchdog `codex exec "hi"` probe to a single structural success transcript
- expanded runtime quota/auth detection to include reconnect-plus-403 precharge/balance failures
- kept pure reconnect/TLS evidence on the execution-network retry path
- added focused regressions for both the probe contract and the mixed reconnect-plus-quota classification

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-requires-expected-success-shape`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`
- real bad-account `freely start` replay from `account-worahe1001@outlook-com-1` with observed auto-switch to `account-worahe1000@outlook-com-1`
- Git commit `8f49bef8` on the feature branch

## Next Action

Merge to `develop` through `test-pre-merge-runtime-slot-recovery-20260412-1004`.
