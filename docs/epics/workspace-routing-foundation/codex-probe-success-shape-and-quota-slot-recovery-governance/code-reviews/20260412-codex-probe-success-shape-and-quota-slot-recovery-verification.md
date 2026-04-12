# Verification: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- issue_path: `docs/epics/workspace-routing-foundation/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- verification_date: `2026-04-12`
- verifier: `codex`

## Scope Verdict

- `PASS`: the Codex `hi` probe now only accepts the fixed success transcript shape
- `PASS`: reconnect-plus-403 quota failures now classify to slot-local exhaustion instead of `execution_network_*`
- `PASS`: pure reconnect/TLS evidence still stays network-local
- `PASS`: real bad-account startup replay auto-switched to the next usable account slot

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-requires-expected-success-shape`
2. `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-log-defers-to-watchdog`
3. `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`
4. `./bin/ai switch codex account-worahe1001@outlook-com-1 --yes`
5. `./bin/freely start --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`
6. `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`
7. `tail -n 80 .freely/logs/runtime-events.log`
8. `cat ~/.codex/active-slot`
9. `./bin/freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`

## Real-Environment Notes

1. `account-worahe1001@outlook-com-1` reproduced the bad current-slot path.
2. The first failing cycle recorded `slot_switch_reason=primary_rate_limit_exhausted` instead of `execution_network_transient`.
3. Recovery then selected `account-worahe1000@outlook-com-1` as the next usable slot and resumed launching from there.

## Residual Risk

- The fixed success transcript is based on the current Codex CLI output contract. If Codex changes the role-marker/output layout later, this owner should reopen as a fresh probe-contract follow-on instead of silently weakening success detection again.
