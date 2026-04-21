# Issue: runtime-daemon-self-loop-followthrough-governance

- issue_id: `I-20260421-1200-A`
- title: `Runtime daemon self-loop followthrough governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-daemon-self-loop-followthrough-governance`
- issue-name: `runtime-daemon-self-loop-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/candidates.md#c-20260421-1200-a`
- source_brainstorm: `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- reopen_reason: `real self-host dogfooding on 2026-04-21 showed one remaining daemon self-loop blocker after the broader runtime lifecycle owner landed: unexpected daemon TERM could be recorded as operator_stop, and orphan dispatcher/watchdog residue could block lawful restart`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- created_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The blocker here is narrower than the surrounding scan/live-status architecture debate. Freely already knows how to patrol, choose a task source, and write continuity, but the runtime could not reliably remain in autonomous looping on canonical `develop`.

Two concrete causes were verified in real execution:

1. user-facing start precheck could treat orphaned dispatcher/watchdog residue as authoritative runtime truth even when no valid supervisor existed,
2. daemon supervisor could record an unexpected external `TERM` as `operator_stop`, which breaks autonomous looping after one patrol round.

This owner exists to carry the narrow fix through a lawful protected-branch path and then prove the final acceptance surface on `develop`, not just feature-local green tests.

## Scope

1. Keep `project_has_authoritative_runtime_processes_for_user_precheck()` authoritative-supervisor-only for user-facing repeated-start refusal.
2. Make daemon-mode supervisor ignore unexpected `INT`/`TERM` when no `stop.marker` exists, while preserving explicit stop semantics.
3. Keep current manager continuity formats runtime-consumable by parsing `## Worker Delegation` handoffs into concrete worker prompt launches.
4. Route `merged-clean` / `retire-ready` worker lanes to cleanup followthrough retirement instead of runtime recovery, and let cleanup reclaim stale recorded ownership for those lanes.
5. Add focused regressions for orphan precheck residue, unexpected daemon `TERM`, worker-delegation continuity consumption, and retire-ready merged-worker retirement routing.
6. Replay the guarded promotion path with concrete owner evidence.
7. Prove on canonical `develop` that Freely self-starts, selects a task, completes it to the current-project success standard, closes the temporary worktree, and continues to another task.

## Non-Goals

1. Do not redesign scan architecture or live-status semantics in this owner.
2. Do not weaken Freely's freedom of action or task autonomy.
3. Do not reopen unrelated runtime/watchdog architecture owners.
4. Do not stop at "daemon process stayed alive once"; the final acceptance remains autonomous end-to-end self-work on `develop`.

## Acceptance

1. Focused regressions cover the orphaned precheck residue and unexpected daemon `TERM` seams.
2. Focused regressions also prove runtime consumes current `## Worker Delegation` continuity and retires merged-clean blocker worktrees instead of re-recovering them.
3. `./bin/pretests-gate` and `./bin/governance-check` pass for this owner.
4. Guarded replay from `feature/runtime-daemon-self-loop-blocker-20260421` through `test-pre-merge-20260421-runtime-self-loop-blocker` into `develop` succeeds lawfully.
5. On canonical `develop`, `freely daemon start` selects at least one task, completes it to the current-project success standard, closes the corresponding temporary worktree, and proceeds to another task.
6. The temporary blocker worktree and disposable test-pre-merge branch are retired after canonical `develop` absorbs the fix.

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `bash docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `./bin/governance-check`
- canonical `develop` self-host replay: `./bin/freely daemon start`
- `git worktree list`

## Completion

- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/candidates.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-runtime-daemon-self-loop-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/code-reviews/20260421-runtime-daemon-self-loop-followthrough-verification.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-worker-delegation-format`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-retire-ready-merged-worker`
- `docs/system/workspace/scripts/tests/test-freely-manager-supervision-alert-retire-ready-merged-worker`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-followthrough-intent-retain`
- `docs/system/workspace/scripts/tests/test-pretests-retirement-gate`
- `docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `docs/system/workspace/scripts/tests/test-freely-daemon-runtime-ignores-unexpected-term-without-stop-marker`
