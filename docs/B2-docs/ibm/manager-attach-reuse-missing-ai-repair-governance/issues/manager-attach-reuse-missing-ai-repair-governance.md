# Issue: manager-attach-reuse-missing-ai-repair-governance

- issue_id: `I-20260330-2318-A`
- title: Manager attach reuse missing-AI repair governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-attach-reuse-missing-ai-repair-governance`
- issue-name: `manager-attach-reuse-missing-ai-repair-governance`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260330/candidates.md#c-20260330-2318-a`
- source_brainstorm: `docs/B1-docs/raw-20260330/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/issues/multi-tool-auto-switch-v1-codex-fallback-governance.md`
  - `docs/epics/workspace-routing-foundation/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`develop` live validation finally proved the false `already_running_attach` path. After a correct `tool_auto_switch_selected previous_tool=kiro-cli active_tool=codex`, the manager bootstrap immediately emitted `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager` and rewrote workcell state to `running/up/up/already_running_attach`.

That means the defect is narrower than a general `live-status` redesign:

1. manager attach reuse can accept a live supervisor without a confirmed live project AI child,
2. `start_project_runtime()` then writes optimistic `up/up` attach state, and
3. `live-status` later reports fake healthy truth because the bad write already happened.

The smallest correct owner is therefore a manager-only attach gate repair, not a broader status-surface rewrite.

## Scope

1. Refuse manager attach reuse unless `ai_pid_state=confirmed_running`.
2. Fall back to project-local repair/restart when manager sees `missing` or stale AI state.
3. Preserve valid worker attach reuse and other healthy attach contracts.
4. Lock the repair with focused regression coverage.
5. Re-run one protected `develop` live validation against the earlier `kiro_monthly_request_limit -> codex` recovery path.

## Non-Goals

1. Do not redesign `live-status` downgrade/reconciliation in this slice.
2. Do not change non-manager attach semantics beyond preserving the healthy existing contract.
3. Do not widen this fix into generic runtime-event redesign.
4. Do not reopen the broader multi-tool availability owner unless this narrow repair proves insufficient.

## Acceptance

1. `ensure_no_active_supervisor_conflict()` must refuse attach reuse for manager projects when `ai_pid_state!=confirmed_running`.
2. The manager `missing ai.pid` path must fall back to project-local repair and remove stale control-plane state instead of returning attach success.
3. Valid worker attach reuse with missing AI state must remain intact.
4. Focused regression coverage must lock the manager-only repair path.
5. One `develop` live validation must confirm the post-`kiro_monthly_request_limit` recovery no longer lands in false `already_running_attach`.

## Completion

- `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/pre-tests.md`
- `docs/progress/workspace-routing-foundation/p-manager-attach-reuse-missing-ai-repair-governance.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `./bin/governance-check`
- `develop` live validation: `kiro-cli` monthly-limit recovery reaches `tool_auto_switch_selected ... active_tool=codex` and `ai_launch_begin ... tool=codex` without `supervisor_attach_reuse ... ai_pid_state=missing role_hint=manager`

## Next

- `2026-04-01 01:14 PDT` completion: `develop` merge `9b89fb3` absorbed the narrow manager attach gate repair, focused regression stayed green, and protected live validation confirmed the old false-attach path is gone on the `kiro_monthly_request_limit -> codex` recovery chain.
- Re-open only if false optimistic `already_running_attach` truth still appears after this write-side repair, which would justify a broader `live-status` reconciliation lifecycle.
