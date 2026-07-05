# Issue: runtime-start-stop-lifecycle-and-process-leak-governance

- issue_id: `I-20260417-0445-A`
- title: `Runtime start/stop lifecycle and process leak governance`
- phase_state: `completed`
- completed_at: `2026-04-28`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-start-stop-lifecycle-and-process-leak-governance`
- issue-name: `runtime-start-stop-lifecycle-and-process-leak-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260417-0445--runtime-start-stop-process-lifecycle-and-leak-contract/candidates.md#c-20260417-0445-a`
- source_brainstorm: `docs/pre-brainstorms/20260417-0445--runtime-start-stop-process-lifecycle-and-leak-contract/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-runtime-start-stop-lifecycle-and-process-leak-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- created_at: `2026-04-18`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Live process inspection showed the runtime leak was not one isolated leftover pid. The bounded defect was that user-facing start semantics, startup lock truth, same-project watcher discovery, and AI failure cleanup were still loose enough to let repeated starts rebuild or relaunch partial runtime state after users thought the runtime had stopped.

This owner captures the first implementation slice that closes that seam without reopening broader runtime architecture work: reject repeated user starts, keep `--force` explicit, make start-lock handling lawful, converge stop on discovered same-project runtime processes, classify local `.iflow` state failures as runtime failures, and preserve enough lifecycle trace truth to debug the bounded path.

## Scope

1. Reject repeated `freely start --project <project>` and `freely daemon start --project <project>` when the same-project runtime is already active.
2. Keep `--force` semantics as explicit stop-then-start rather than implicit attach.
3. Publish, ignore, and clean same-project start-lock truth lawfully for self-owned locks, orphaned AI pid hints, stale active locks, and launch-failure cleanup.
4. Discover and terminate same-project watchdog and interruption-dispatcher processes during stop followthrough.
5. Classify local `.iflow` permission or state failures as runtime failures and terminate the full AI descendant tree on failure.
6. Preserve bounded lifecycle-trace and interruption-manager verification that directly supports this start/stop leak contract.

## Non-Goals

1. Do not redesign manager continuity or manager handoff semantics in this owner.
2. Do not widen into generic slot switching, auth recovery, or unrelated runtime failure taxonomy work.
3. Do not change protected-branch development rules; implementation still lands through guarded `test-pre-merge-* -> develop` replay.
4. Do not treat lifecycle tracing as a new standalone observability program beyond this bounded runtime leak seam.

## Acceptance

1. Repeated `freely start` rejects while runtime is already running and does not spawn an extra runtime chain.
2. Repeated `freely daemon start` rejects under the same contract and does not launch a duplicate daemon/runtime chain.
3. Same-project start-lock handling tolerates lawful self-owned and orphaned hints, cleans stale active owners, and releases the lock on startup failure.
4. `freely stop --project <project>` terminates discovered same-project watchdog and interruption-dispatcher processes instead of leaving relaunch-capable remnants alive.
5. Local `.iflow` state failures are materialized as runtime failures and the full AI descendant tree is terminated.
6. Focused interruption-manager fast-path and lifecycle-trace evidence remain green as bounded regressions for this contract.
7. The owner carries explicit issue/progress/pre-tests/review truth plus `premerge-integration` adequacy for guarded promotion to `develop`.

## Verification

- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-precheck-ignores-self-owned-start-lock`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-rejects-when-runtime-already-running`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-interruption-manager-fast-path-control-validation`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-lifecycle-trace-log`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-stalled-active-owner`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-self-owned-start-lock`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-rejects-when-runtime-already-running`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-releases-start-lock-when-startup-fails`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-discovered-watchers-and-dispatchers`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-codex-session-permission-failure`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-iflow-local-state-failure`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-iflow-descendants-on-runtime-failure`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`
- `git diff --check`

## Closeout

1. Carry the implementation and bounded lifecycle writeback through `feature/runtime-process-leak-20260417 -> test-pre-merge-runtime-lifecycle-20260417 -> develop`.
2. After guarded promote, run one short canonical `develop` followthrough replay to confirm Freely still starts and reports runtime status normally under the new contract.
3. Retire the disposable `test-pre-merge-*` worktree immediately after followthrough passes.
