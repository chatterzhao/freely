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
  - reproduce the exact false-positive path in an isolated worktree or focused test, not only on the current `develop` scene
  - identify the write path that rewrites `workcell-state.env` to `already_running_attach` after the last real cleanup
  - define whether the right repair belongs in attach detection, writeback semantics, or live-status downgrade/reconciliation
  - preserve the valid contract from `I-20260328-0745-A`: active real PIDs may still reconcile stale persisted `down` upward
- promotion_gate:
  - prove a minimal repro for the false-positive optimistic case
  - show why the earlier `live-status-current-runtime-state-reconciliation` fix does not already cover this regression
  - keep the blast radius narrow; do not merge broad status-surface redesign into the same repair
- open_questions:
  - does the root cause live in `ensure-manager` attach detection, stale supervisor PID reuse, or read-path trust of persisted attach state
  - should attach-only writes emit runtime events as observability anchors
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The symptom is real, but the trigger is still unproven. Evidence instrumentation is acceptable now; corrective behavior changes still need a focused repro.`
    verdict: `needs_more_research`
- priority: P1
- status: needs_research
- decision_reason: The symptom is real and current, but the exact root cause is not yet proven. The next lawful step is a focused repro and code-path audit, not a speculative fix.
- promoted_issue_path: `pending://issue-materialization`
- milestone: `pending://milestone-binding`
- next_action: Build a minimal repro lane for false `already_running_attach` and pin the precise write/read mismatch.
- revisit_trigger: Promote once a repro shows the exact attach path that writes optimistic `up/up` without a surviving project-owned supervisor or AI.
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`
