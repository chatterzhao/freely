# Candidates - 20260330-2318--live-status-already-running-attach-regression

## Context

- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260330-2318-A
- candidate_format_version: v2
- title: Live-status false already-running-attach regression
- problem: `develop` can reach a state where `fleet-status` correctly reports `sup=none ai=none`, but `workcell-state.env` is later rewritten to `running/up/up/already_running_attach`, causing `live-status` to present stale optimistic runtime truth with no current project-owned supervisor or AI PID.
- why_now: This is a current dogfood regression on the protected manager worktree. It distorts the top-level operator entrypoint and can cause manager patrol to reason from a fake healthy runtime.
- acceptance_criteria:
  - prove the exact false-positive path that rewrites `workcell-state.env` to `already_running_attach` after the last real cleanup
  - show that the bad attach reuse is specifically the manager path reusing a live supervisor while `ai_pid_state!=confirmed_running`
  - narrow the repair to attach detection / optimistic write semantics without redesigning the broader status surface
  - preserve the valid contract from `I-20260328-0745-A`: active real PIDs may still reconcile stale persisted `down` upward
- promotion_gate:
  - confirm real production evidence for the manager attach false-positive and bind it to a focused regression
  - show why the earlier `live-status-current-runtime-state-reconciliation` fix does not already cover this regression
  - keep the blast radius narrow; do not merge broad status-surface redesign into the same repair
- open_questions:
  - does the root cause live in `ensure-manager` attach detection, stale supervisor PID reuse, or read-path trust of persisted attach state
  - should attach-only writes emit runtime events as observability anchors
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The trigger is now proven by live evidence: manager attach reuse can report already_running_attach while ai_pid_state=missing immediately after a valid fallback selection. The remaining work is a narrow attach-gating repair with regression coverage.`
    verdict: `promote_when_regression_green`
- priority: P1
- status: promoted
- decision_reason: Live evidence on `develop` proved the exact bad attach path: manager-role attach reuse accepted a live supervisor while `ai_pid_state=missing`, then rewrote workcell state to `already_running_attach`. The repair can now stay narrow and test-backed.
- promoted_issue_path: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- next_action: Owner `I-20260330-2318-A` is complete on `develop`. Keep this candidate only as provenance unless false optimistic attach truth reappears and proves the write-side repair insufficient.
- revisit_trigger: Reopen broader status-surface discussion only if false optimistic `already_running_attach` truth still appears after the manager-only attach gate repair.
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`
