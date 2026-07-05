# Issue: live-status-current-runtime-state-reconciliation-governance

- issue_id: `I-20260328-0745-A`
- title: Live-status current runtime state reconciliation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `live-status-current-runtime-state-reconciliation-governance`
- issue-name: `live-status-current-runtime-state-reconciliation-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260328-0745/candidates.md#c-20260328-0745-a`
- source_brainstorm: `docs/B1-docs/raw-20260328-0745/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
- pre_tests_path: `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/code-reviews`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

`live-status` is the current-state entrypoint, but it could surface an internally contradictory answer:

- `activity_state: ai_active`
- `last_ai_state: down`
- `last_exit_reason: starting`

The contradiction came from reading current runtime PID truth and persisted `workcell-state.env` independently without any reconciliation step.

## Scope

1. Reconcile `last_supervisor_state` toward `up` when a live project-owned supervisor PID is confirmed.
2. Reconcile `last_ai_state` toward `up` when a live project-owned AI PID is confirmed.
3. Collapse `last_exit_reason: starting` to `none` only when the AI PID is already confirmed live.
4. Keep the change read-only in `live-status`; do not rewrite persisted runtime state files.
5. Extend focused regression coverage for the active-AI case.

## Acceptance

- `live-status` no longer reports `activity_state: ai_active` while still showing `last_ai_state: down`.
- The reconciliation is one-way toward confirmed `up` and only happens when PID ownership is positively confirmed for the current project.
- Missing PIDs do not fabricate new failure states.
- Watchdog-only and manager-recovery focused tests continue to pass.

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/progress/workspace-routing-foundation/p-live-status-current-runtime-state-reconciliation-governance.md`
- `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status-watchdog-survival`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`

## Closure Evidence

- `develop` 已包含 merge `2ebf39e Merge branch 'feature/fix-last-ai-state-down-20260328-0745' into develop`
- canonical verification artifact 已存在：`docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/code-reviews/20260328-live-status-current-runtime-state-reconciliation-verification.md`
- 原始 feature worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260328-0745-feature-fix-last-ai-state-down` 已退休，不再需要额外 salvage

## Next

- This lifecycle is closed on canonical `develop`.
- Broader status-family evolution such as JSON/watch/scoring remains a separate lifecycle.
