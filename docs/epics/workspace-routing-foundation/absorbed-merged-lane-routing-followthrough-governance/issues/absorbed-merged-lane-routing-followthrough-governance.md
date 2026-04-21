# Issue: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- title: `Absorbed merged lane routing followthrough governance`
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `absorbed-merged-lane-routing-followthrough-governance`
- issue-name: `absorbed-merged-lane-routing-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/pre-brainstorms/20260421-1330--absorbed-merged-lane-routing-followthrough/candidates.md#c-20260421-1330-a`
- source_brainstorm: `docs/pre-brainstorms/20260421-1330--absorbed-merged-lane-routing-followthrough/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- reopen_reason: `canonical develop self-host replay proved absorbed merged blocker lanes were no longer auto-recovered, but scan/fleet patrol still routed them as if they were launchable worker execution targets`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-absorbed-merged-lane-routing-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- created_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The previous runtime repairs already blocked automatic relaunch of merged worker lanes. The remaining failure was subtler: manager patrol still looked at absorbed merged lanes and treated them like current execution capacity.

Two bounded surfaces caused that drift:

1. `wt-fleet-status` preserved `LAST_ROLE_HINT=worker` even when the branch tip was already absorbed into `develop`.
2. `task-source-scan` kept routing linked progress items back to `verification` because it did not consult the linked branch/worktree absorption state.

This owner exists to downgrade those absorbed lanes to cleanup-followthrough visibility without hiding them from scan, so Freely keeps autonomy while choosing real launchable tasks next.

## Scope

1. Downgrade absorbed merged lanes in fleet status from `worker` to cleanup-like role visibility.
2. Route absorbed merged progress items to `cleanup` instead of `verification`, while keeping them visible as unfinished followthrough.
3. Add focused regressions for both downgraded surfaces plus nearby scan/fleet coverage.
4. Replay the guarded feature -> test-pre-merge -> develop chain.
5. Re-run canonical `develop` self-host acceptance so Freely must pick a real task, complete it to the current-project success standard, close the worktree, and continue.

## Non-Goals

1. Do not redesign scan, live-status, or manager continuity architecture.
2. Do not add a durable prompt lifecycle index.
3. Do not weaken Freely's ability to self-select work from scan.
4. Do not reopen the broader daemon self-loop implementation owner.

## Acceptance

1. Absorbed merged lanes no longer render as `worker` in fleet status.
2. Task-source scan routes absorbed merged progress owners to cleanup-style followthrough instead of verification execution.
3. Focused regressions and existing nearby scan/fleet regressions pass.
4. Guarded replay into `develop` succeeds lawfully.
5. On canonical `develop`, `./bin/freely daemon start` selects a real launchable task, completes it to the current-project success standard, closes the corresponding temporary worktree, and proceeds to another task.

## Verification

- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
- `./bin/governance-check`
- canonical `develop` self-host replay: `./bin/freely daemon start`

## Completion

- `docs/pre-brainstorms/20260421-1330--absorbed-merged-lane-routing-followthrough/brainstorms.md`
- `docs/pre-brainstorms/20260421-1330--absorbed-merged-lane-routing-followthrough/candidates.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-absorbed-merged-lane-routing-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`
- `docs/system/workspace/scripts/runtime/task-source-scan.py`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
- `docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
