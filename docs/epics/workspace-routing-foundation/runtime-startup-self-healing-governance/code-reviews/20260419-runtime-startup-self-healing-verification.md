# Verification: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- verification_date: `2026-04-19`
- branch: `feature/runtime-startup-self-healing-followthrough-20260419`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-startup-self-healing-followthrough`
- verifier: `codex`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`
3. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-launch-in-flight-state`
4. `bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-pid`
5. `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
6. `bash docs/system/workspace/scripts/tests/test-freely-prompt-build-failure-keeps-supervisor-alive`
7. `git diff --check`
8. `./bin/governance-check`
9. Protected-root replay:
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`
   - wait about 70 seconds
   - `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`

## Results

1. All focused regressions above passed in both the feature continuation worktree and the temporary `test-pre-merge-runtime-startup-self-healing-followthrough` assembly lane.
2. `test-monitor-ai-cli-pid` now proves launch-state writeback records `LAST_AI_STATE="up"` and `LAST_EXIT_REASON="ai_launch_in_flight"` as soon as the child pid is known, before any tool-specific exit timing can race status readers.
3. `test-freely-live-status-startup-self-heals-stale-launch-in-flight-state` proves stale `ai_launch_in_flight` state is self-healed only after the grace window, which keeps the logic tool-agnostic instead of pinning behavior to `codex`.
4. `test-freely-prompt-build-failure-keeps-supervisor-alive` proves `build_prompt` failure no longer kills the supervisor under `set -e`; the runtime records `prompt_build_failed`, keeps the supervisor alive, and `live-status` surfaces retryable truth instead of `startup_self_heal_no_runtime`.
5. The protected root initially still had the old failure signature in history: lifecycle trace reached `L020 prompt_build_begin` without `L021 prompt_build_complete`, and a later `live-status` misclassified the dead manager lane as `startup_self_heal_no_runtime`.
6. After the followthrough patch and replay on `2026-04-19 20:57-20:58 PDT`, protected-root startup no longer died at prompt build:
   - `runtime-events.log` recorded `supervisor_started supervisor_pid=69384`, `manager_continuity_startup_stub_materialized`, and `ai_launch_begin tool=codex`
   - protected-root `live-status` showed `desired_runtime_state: running`, `last_supervisor_state: up`, `last_ai_state: up`, `last_exit_reason: none`
   - active processes included authoritative `supervisor`, `interruption_dispatcher`, and `ai` pids, which means startup truth stayed aligned with real control-plane state
7. Feature-lane replay no longer self-healed to fake runtime-down state either; after one minute it surfaced `manager_worker_launch_verification_blocked`, which is an explicit governance stop reason rather than a startup-state lie.

## Verdict

`AT-001`, `AT-002`, and `AT-003` remain satisfied for this bounded owner, and the followthrough continuation closes the additional short-lived CLI race: startup now canonicalizes stale machine-owned truth, records launch-in-flight truth before AI exit can race readers, and keeps prompt-build failure in a retryable supervisor-owned state instead of collapsing it into fake runtime absence.

## Implementation Decision Note

- decision: `Keep startup self-heal scoped to machine-provable stale state, but make the startup truth contract robust for short-lived non-interactive CLI tools by recording launch-in-flight state and treating prompt-build failure as retryable supervisor truth.`
- why_this: `The protected-root replay showed the user-visible failure still occurred before manager-owned semantic recovery started: the supervisor could disappear during prompt build, and short-lived CLI exec tools can end fast enough that readers observe missing child pids unless launch state is written immediately. The narrowest correct fix is to harden runtime-owned startup truth rather than special-case codex or widening manager recovery.`
- alternatives_considered: `Special-case codex exec; suppress startup self-heal for one tool family only; rely on manager recovery after prompt-build loss; widen this owner into a broader lifecycle redesign.`
- boundary_non_goals: `This note still does not let startup repair semantic continuation, does not lock behavior to codex, and does not redesign generic post-failure recovery or manager routing.`
- residual_risk: `Downstream manager continuity or verification gates can still stop a lane, but those conditions now surface as explicit governance/runtime reasons like manager_worker_launch_verification_blocked or prompt_build_failed instead of fake runtime absence.`

## Remaining Closeout

1. Merge, push, and retire the dedicated feature worktree after recording the closeout commit on this lane.
