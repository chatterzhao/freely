# Verification: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- verification_date: `2026-04-20`
- branch: `feature/runtime-manager-startup-blocker-rootcause-20260419`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-manager-startup-blocker-rootcause`
- verifier: `codex`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-detach-contract`
3. `bash docs/system/workspace/scripts/tests/test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path`
4. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
5. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-launch-in-flight-state`
6. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
7. `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
8. `bash docs/system/workspace/scripts/tests/test-freely-prompt-build-failure-keeps-supervisor-alive`
9. `bash docs/system/workspace/scripts/tests/test-freely-live-status`
10. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`
11. `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`
12. `git diff --check`
13. `./bin/governance-check`
14. Protected-root replay:
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - wait about 70 seconds
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Results

1. All focused regressions above passed in both the feature continuation worktree and the temporary `test-pre-merge-runtime-startup-self-healing-followthrough` assembly lane.
2. `test-monitor-ai-cli-pid` now proves launch-state writeback records `LAST_AI_STATE="up"` and `LAST_EXIT_REASON="ai_launch_in_flight"` as soon as the child pid is known, before any tool-specific exit timing can race status readers.
3. `test-freely-live-status-startup-self-heals-stale-launch-in-flight-state` proves stale `ai_launch_in_flight` state is self-healed only after the grace window, which keeps the logic tool-agnostic instead of pinning behavior to `codex`.
4. `test-freely-prompt-build-failure-keeps-supervisor-alive` proves `build_prompt` failure no longer kills the supervisor under `set -e`; the runtime records `prompt_build_failed`, keeps the supervisor alive, and `live-status` surfaces retryable truth instead of `startup_self_heal_no_runtime`.
5. `test-freely-daemon-start-detach-contract` keeps the launcher requirement explicit: `daemon start` must spawn `daemon-run` in a new session rather than fall back to shell-owned `nohup ... &`, because short-lived non-interactive callers can otherwise tear the control plane down after startup returns.
6. `test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path` proves `live-status` no longer self-heals a live daemon runtime down when the recorded project root and the inspected project root differ only by path spelling that still resolves to the same on-disk directory.
7. `test-freely-live-status` still passes after the path-equivalence hardening, so the runtime surface and prompt/deep-ref output remain intact.
8. `test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite` still passes in the fresh `2026-04-20` session, so status refresh keeps persisting corrected continuity and prompt anchors even when worker-slot counts do not change.
9. `test-freely-stale-manager-continuity-filter` still passes in the same session, so stale continuity that points at missing worktrees keeps getting filtered instead of being revived into status truth.
10. The protected root initially still had the old failure signature in history: lifecycle trace reached `L020 prompt_build_begin` without `L021 prompt_build_complete`, and a later `live-status` misclassified the dead manager lane as `startup_self_heal_no_runtime`.
11. After the detached-launch followthrough patch, a fresh feature-worktree cold start replay on `2026-04-20` no longer died after the `daemon start` caller exited:
   - `runtime-events.log` recorded normal startup progression through supervisor start, continuity stub materialization, and AI launch begin
   - after `daemon start` returned and a fresh shell waited about 75 seconds, `live-status` still showed `activity_state: ai_active`, `desired_runtime_state: running`, `last_supervisor_state: up`, `last_ai_state: up`, `pending_delegated_continuation_ids: none`, and the delegated continuation listed under `last_consumed_delegated_continuation_ids`
   - `ps` showed the supervisor reparented to pid `1`, confirming the control plane was truly session-detached instead of surviving only while the original non-interactive caller session remained alive
12. That same feature-lane replay therefore no longer self-healed to fake runtime-down state after one minute; it preserved a live control-plane and consumed the queued delegated continuation instead of collapsing to `startup_self_heal_no_runtime`.
13. Fresh-session demand-pool reentry on `2026-04-20` did not surface a higher-priority blocker in milestones, progress/recovery truth, review/test evidence, session handoff evidence, GitHub-like repo issue surfaces, or `docs/PROJECT_INTENT.md`; the delegated continuation therefore stays absorbed as a sidecar closeout action, and `docs/PROJECT_INTENT.md` now ends with `<!-- runtime-lifecycle-validation -->`.

## Verdict

`AT-001`, `AT-002`, and `AT-003` remain satisfied for this bounded owner, and the current continuation closes one more ownership edge without widening scope: startup now canonicalizes stale machine-owned truth, records launch-in-flight truth before AI exit can race readers, keeps prompt-build failure in a retryable supervisor-owned state, and preserves a live daemon when project-root spelling differs but the directory identity is the same.

## Implementation Decision Note

- decision: `Keep startup self-heal scoped to machine-provable stale state, but make the startup truth contract robust for short-lived non-interactive CLI tools by recording launch-in-flight state and treating prompt-build failure as retryable supervisor truth.`
- why_this: `The protected-root replay showed the user-visible failure still occurred before manager-owned semantic recovery started: the supervisor could disappear during prompt build, and short-lived CLI exec tools can end fast enough that readers observe missing child pids unless launch state is written immediately. The narrowest correct fix is to harden runtime-owned startup truth rather than special-case codex or widening manager recovery.`
- alternatives_considered: `Special-case codex exec; suppress startup self-heal for one tool family only; rely on manager recovery after prompt-build loss; widen this owner into a broader lifecycle redesign.`
- boundary_non_goals: `This note still does not let startup repair semantic continuation, does not lock behavior to codex, and does not redesign generic post-failure recovery or manager routing.`
- residual_risk: `Downstream manager continuity or verification gates can still stop a lane, but those conditions now surface as explicit governance/runtime reasons like manager_worker_launch_verification_blocked or prompt_build_failed instead of fake runtime absence. This worktree also still carries unrelated dirty tests for session-rotation/delegated-continuation/readiness resilience, so guarded promote should split or reroute those files before treating the lane as a clean startup-self-heal closeout.`

## Remaining Closeout

1. Split or reroute unrelated dirty tests (`test-freely-session-rotation`, `test-freely-delegated-continuation-ids-empty-success`, `test-freely-delegated-continuation-prompt-contract`, `test-freely-interruption-dispatcher-ready-loop-tolerates-empty-probe-failure`, `test-freely-post-cycle-helper-failure-does-not-kill-supervisor`) before guarded promote so this owner's acceptance surface stays narrow.
2. Merge, push, and retire the dedicated feature worktree after recording the closeout commit for the current continuation on this lane.
3. Keep the `docs/PROJECT_INTENT.md` marker as delegated continuity evidence only; do not widen this owner or substitute the marker for the remaining guarded promote duties.
