# Issue: codex-real-exec-switch-and-after-failure-recovery-governance

- issue_id: `I-20260410-1835-B`
- title: Codex real exec switch and after-failure recovery governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `codex-real-exec-switch-and-after-failure-recovery-governance`
- issue-name: `codex-real-exec-switch-and-after-failure-recovery-governance`
- priority: `P1`
- source_candidate: `docs/B1-docs/raw-20260410T143000Z/candidates.md#c-20260410-1835-b`
- source_brainstorm: `docs/B1-docs/raw-20260410T143000Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-codex-real-exec-switch-and-after-failure-recovery-governance.md`
- verification_artifact_dir: `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/code-reviews`
- follow_on_to: `I-20260407-0023-A`
- created_at: `2026-04-10`
- session_refs: []

## Why

Dogfooding exposed two coupled regressions in the Codex auth surface:

1. automatic recovery after a real failure was still entangled with manual full-sweep semantics
2. real command-surface verification was not frozen as owner evidence even though `freely start`, `bin/ai switch codex`, and `status codex` were touching live auth state and live runtime recovery

That left the runtime able to mis-handle the failed current slot, over-probe in the wrong situations, and rely on non-exec inventory truth in places where only real `codex exec` should decide.

## Scope

1. Make real `codex exec` the primary truth for Codex slot availability in `freely start`, watchdog recovery, and manual switch paths.
2. Keep manual `bin/ai switch codex` semantics distinct from after-failure recovery:
   - manual switch may full-sweep saved slots
   - after-failure recovery must skip the failed current slot and stop at the first usable later slot
3. Treat slot-local network/certificate failures during slot testing as fast-fail signals that kill the current test child and advance immediately.
4. Verify the real command surface by executing the relevant `bin/ai xx` commands and restoring auth afterward.

## Non-Goals

1. Do not reopen the broader testing-governance line handled by `I-20260410-1835-A`.
2. Do not reintroduce URL/OAuth inventory refresh as the primary truth for runtime recovery.
3. Do not add background periodic Codex probing as a default runtime behavior.

## Acceptance

1. `freely start` uses the current slot directly and only triggers automatic switch after a real failure.
2. Automatic recovery skips the failed current slot, probes later saved slots one by one with real `codex exec`, and stops at the first usable slot.
3. Manual `bin/ai switch codex` keeps its full-sweep semantics and does not silently skip the current slot.
4. Network/certificate failures during slot testing kill the current test child promptly so recovery can continue to the next candidate.
5. Real `bin/ai xx` validation is executed, restored, and recorded as owner evidence.

## Verification

- `docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/code-reviews/20260410-codex-real-exec-switch-and-after-failure-recovery-verification.md`

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/ai-cli`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- `docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-uses-recovery-probe-reason`
- `docs/system/workspace/scripts/tests/test-watchdog-codex-after-failure-skips-current-slot`
- `docs/system/workspace/scripts/tests/test-watchdog-codex-exec-truth-stops-at-first-usable-slot`
- `docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-codex-on-network-failure`
- `docs/system/workspace/scripts/tests/test-freely-worker-runtime-slot-local-failure-self-recovers-next-slot`
- `docs/system/workspace/scripts/tests/test-freely-active-runtime-reconnect-stays-network-local`

## Next

- Completed in the dedicated feature worktree. Promote through `test-pre-merge-20260410-codex-switch-real-env` and guarded merge to `develop`.
