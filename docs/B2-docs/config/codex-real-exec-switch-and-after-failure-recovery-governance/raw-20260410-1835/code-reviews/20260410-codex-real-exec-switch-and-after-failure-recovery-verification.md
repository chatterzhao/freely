# Verification: codex-real-exec-switch-and-after-failure-recovery-governance

- issue_id: `I-20260410-1835-B`
- issue_path: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/issues/codex-real-exec-switch-and-after-failure-recovery-governance.md`
- verification_date: `2026-04-10`
- verifier: `codex`

## Scope Verdict

- `PASS`: runtime recovery now treats real `codex exec` as the primary availability truth for after-failure slot recovery
- `PASS`: automatic recovery skips the failed current slot and stops at the first later usable saved slot
- `PASS`: manual `bin/ai switch codex` still performs a full saved-slot sweep and does not blindly skip the current slot
- `PASS`: slot-local network/certificate failures kill the current test child quickly instead of stalling recovery
- `PASS`: the real `bin/ai xx` command surface was executed and the original live auth was restored afterward

## Commands

1. `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-uses-recovery-probe-reason`
2. `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-skips-current-slot`
3. `bash docs/system/workspace/scripts/tests/test-watchdog-codex-exec-truth-stops-at-first-usable-slot`
4. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-network-failure`
5. `bash docs/system/workspace/scripts/tests/test-freely-worker-runtime-slot-local-failure-self-recovers-next-slot`
6. `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`
7. `./bin/ai init`
8. `./bin/ai list`
9. `./bin/ai whoami codex`
10. `./bin/ai status codex`
11. `./bin/ai switch codex`
12. `./bin/ai switch codex <slot>`
13. `./bin/ai login codex apikey`
14. `./bin/ai save codex`
15. `./bin/ai delete codex <slot>`
16. `freely start`
17. `freely live-status`
18. `freely stop`
19. `./bin/ai --quiet --format json whoami codex`

## Real-Environment Notes

1. The bad-slot replay used `account-worahe1001@outlook-com-1` as the intentionally limited current slot.
2. The first active-runtime failure classified to `primary_rate_limit_exhausted`, then recovery probed later saved slots in order.
3. Recovery stopped on the first usable saved slot, `apikey-codex-a1002-1`, instead of sweeping the full inventory.
4. Manual `switch codex` remained a full sweep and explicitly included the current slot.
5. Temporary auth mutations created during `login/save/delete` validation were cleaned up, and final auth was restored to `apikey-codex-a1006-1`.
6. After `freely stop`, no lingering supervisor, monitor, or Codex child remained.

## Implementation Decision Note

- decision: `Make real `codex exec` the primary runtime truth, split manual sweep from after-failure recovery semantics, and fast-fail slot-local network errors so recovery can keep moving.`
- why_this: `The regressions came from mixing inventory truth with runtime truth and from reusing full-sweep helpers where the runtime only needed ordered after-failure recovery.`
- alternatives_considered: `Keep URL/OAuth inventory as the primary signal; make automatic recovery full-sweep all slots; preserve long-running reconnect retries on slot-local failures; keep real command-surface validation outside owner evidence.`
- boundary_non_goals: `No new periodic background probing, no reopening of the testing-governance root-cause owner, and no broader ACP architecture redesign.`
- residual_risk: `Live account/network behavior can still vary by environment, so canonical post-merge followthrough remains necessary even though feature-lane real-env validation now exists.`
