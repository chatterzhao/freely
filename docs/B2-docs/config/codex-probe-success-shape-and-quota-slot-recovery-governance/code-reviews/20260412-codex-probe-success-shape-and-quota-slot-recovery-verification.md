# Verification: codex-probe-success-shape-and-quota-slot-recovery-governance

- issue_id: `I-20260412-0907-A`
- issue_path: `docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md`
- verification_date: `2026-04-12`
- verifier: `codex`

## Implementation Decision Note

- decision: `Treat the Codex hi probe as success only when the transcript shape is exactly the canonical user/assistant exchange, and prioritize explicit 403/quota evidence over reconnect noise so bad slots advance immediately to the next usable slot.`
- why_this: `The real failure was not generic network instability; it was false-positive slot usability and misclassified quota/auth failures. Tightening the probe contract and making quota/auth evidence win over reconnect text is the smallest bounded change that restores forward progress without widening the whole execution-network policy.`
- alternatives_considered: `Keep rc=0 as the probe truth and only broaden quota regexes later; or collapse all reconnect failures into unconditional slot rotation. The first leaves false-positive usable slots alive, and the second would erase the intentional bounded retry policy for genuine network-only failures.`
- boundary_non_goals: `This owner does not redesign cross-tool fallback, remove execution_network taxonomy, or promise that every Codex CLI output variation forever matches the current transcript parser without future follow-on work.`
- residual_risk: `If the Codex CLI transcript format changes again, the stricter probe may fail closed and require a fresh owner to re-freeze the success contract. Likewise, any new quota/auth wording not covered by the current detection set would need another bounded follow-on.`

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
5. `freely start --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`
6. `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`
7. `tail -n 80 .freely/logs/runtime-events.log`
8. `cat ~/.codex/active-slot`
9. `freely stop --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-slot-recovery-network-failure`

## Real-Environment Notes

1. `account-worahe1001@outlook-com-1` reproduced the bad current-slot path.
2. The first failing cycle recorded `slot_switch_reason=primary_rate_limit_exhausted` instead of `execution_network_transient`.
3. Recovery then selected `account-worahe1000@outlook-com-1` as the next usable slot and resumed launching from there.

## Residual Risk

- The fixed success transcript is based on the current Codex CLI output contract. If Codex changes the role-marker/output layout later, this owner should reopen as a fresh probe-contract follow-on instead of silently weakening success detection again.
