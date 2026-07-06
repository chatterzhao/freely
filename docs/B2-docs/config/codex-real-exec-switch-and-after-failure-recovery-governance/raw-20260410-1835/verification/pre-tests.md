# Pre-Tests: codex-real-exec-switch-and-after-failure-recovery-governance

## Unit
- acceptance target: `Focused recovery helpers preserve after-failure skip-current semantics and stop at the first usable later slot`
- testing layer: `unit`
- target environment: `feature/codex-real-switch-e2e-and-pretests-gap-20260410-170500`
- required evidence: `targeted regression pass receipts`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-skips-current-slot`.
2. Run `bash docs/system/workspace/scripts/tests/test-watchdog-codex-exec-truth-stops-at-first-usable-slot`.

## Integration
- acceptance target: `Runtime and slot-test helpers classify slot-local failures correctly and keep recovery on the exec-only path`
- testing layer: `integration`
- target environment: `feature/codex-real-switch-e2e-and-pretests-gap-20260410-170500`
- required evidence: `runtime helper regressions plus monitor fast-fail regression`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-uses-recovery-probe-reason`.
2. Run `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-network-failure`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`.

## End-to-End
- acceptance target: `A real limited slot can trigger freely start recovery, which skips the failed current slot and hands off on the first later usable slot`
- testing layer: `end_to_end`
- target environment: `feature/codex-real-switch-e2e-and-pretests-gap-20260410-170500`
- required evidence: `real bad-slot start, live-status/log observation, and restored runtime state`
- blocker taxonomy: `execution_pending_or_failed`
1. Switch Codex to the real limited slot `account-worahe1001@outlook-com-1`.
2. Run `freely start`, observe runtime logs for the first failure and ordered recovery probes, then stop after the first usable slot is adopted.
3. Verify the recovered slot is a later saved slot and that `freely stop` leaves no lingering supervisor/monitor/codex child.

## Real-Environment
- acceptance target: `The full live Codex command surface is executed and restored, and manual switch semantics stay distinct from after-failure runtime recovery`
- testing layer: `real_environment`
- target environment: `feature/codex-real-switch-e2e-and-pretests-gap-20260410-170500`
- required evidence: `real bin-ai command execution receipts plus final auth restore confirmation`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/ai init`.
2. Run `./bin/ai list`.
3. Run `./bin/ai whoami codex`.
4. Run `./bin/ai status codex`.
5. Run `./bin/ai switch codex`.
6. Run `./bin/ai switch codex <slot>`.
7. Run `./bin/ai login codex apikey`.
8. Run `./bin/ai save codex`.
9. Run `./bin/ai delete codex <slot>`.
10. Restore the original Codex auth and verify it with `./bin/ai --quiet --format json whoami codex`.

## Acceptance Items

### Recovery skips the failed current slot
- id: `AT-001`
- requirement: `After a real failure, automatic recovery skips the failed current slot and probes later saved slots with real exec truth.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/raw-20260410-1835/code-reviews/20260410-codex-real-exec-switch-and-after-failure-recovery-verification.md`

### Slot-local network failures fast-fail and continue
- id: `AT-002`
- requirement: `Slot-local network or certificate failures kill the current test child promptly so the next saved slot can be tried.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/raw-20260410-1835/code-reviews/20260410-codex-real-exec-switch-and-after-failure-recovery-verification.md`

### Manual switch keeps full-sweep semantics
- id: `AT-003`
- requirement: `Manual bin-ai switch codex sweeps saved slots and does not blindly skip the current slot.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/raw-20260410-1835/code-reviews/20260410-codex-real-exec-switch-and-after-failure-recovery-verification.md`

### Real command surface is restored after testing
- id: `AT-004`
- requirement: `Real bin-ai command validation restores the original live auth and leaves no residual temporary slots or lingering runtime children.`
- evidence_level: `real_env`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/raw-20260410-1835/code-reviews/20260410-codex-real-exec-switch-and-after-failure-recovery-verification.md`
