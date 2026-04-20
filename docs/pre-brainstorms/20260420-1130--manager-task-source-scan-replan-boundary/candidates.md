# Candidates - 20260420-1130--manager-task-source-scan-replan-boundary

- Source brainstorm: `docs/pre-brainstorms/20260420-1130--manager-task-source-scan-replan-boundary/brainstorms.md`

### C-20260420-1130-A

- candidate_format_version: `v2`
- title: `Manager task-source scan idle/replan boundary governance`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `in_pre_brainstorm`
- candidate_status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- problem: `Freely manager needs a structured way to find work after startup and after closeout, but the current patrol layer lacks a runtime-owned trigger contract. Without it, stale delegated continuation can hijack the lane, while broad patrol can also re-scan too often and derail in-flight worker continuity.`
- why_now:
  - recent self-host replay shows manager can miss valid follow-on work when stale delegated handoff stays active
  - once milestone patrol seeds are exposed, runtime still needs a clear answer for when scan should regenerate versus when existing continuity should remain primary
  - the user explicitly requires both capabilities at once: startup autonomous patrol and interruption-driven task completion
- proposed_scope:
  - freeze task-source scan as an idle/replan step rather than an every-cycle step
  - define the first bounded trigger set for regeneration and suppression
  - materialize a machine-readable scan json and scan-state artifact for manager patrol
  - keep raw durable family naming (`human interruption`, `external issue`) separate from standing surfaces (`milestone`, `pre-brainstorm`, `progress`, `recovery`, `delegated continuation`)
- non_goals:
  - shipping full GitHub/Gitee provider automation in this owner
  - collapsing all standing surfaces into a new raw-source family schema
  - broad runtime/fleet redesign outside the manager patrol trigger seam
- acceptance_criteria:
  - a new pre-brainstorm freezes the idle/replan trigger boundary and the distrust-stale-state rule
  - runtime regenerates `manager-task-source-scan-latest.json` only on bounded idle/replan triggers
  - prompt-time broad patrol is suppressed while active workers are stably running
  - prompt-time patrol seed remains available for idle manager rounds, using existing scan json when no new regeneration is needed
  - scan json records trigger reason plus per-surface reconcile/trust hints for milestone / pre-brainstorm / progress patrol seeds
  - focused tests prove startup generation, active-worker suppression, idle-after-continuity regeneration, stale delegated intake filtering, and unresolved pre-brainstorm/progress surfacing
- promotion_gate:
  - keep the first patrol surface set bounded to `human interruption`, delegated continuation, active milestone queue, active pre-brainstorm queue, and active progress queue
  - do not widen this owner into external issue provider automation, generic watchdog redesign, or project-wide fleet closure
  - prove the runtime slice with focused startup/prompt/launch regressions before considering IBM materialization
- open_questions:
  - whether `recovery` should join the machine-readable patrol snapshot or stay ad hoc until a narrower owner absorbs it
  - whether the same stale-pid protection should be frozen as an explicit cross-watcher contract for `ensure-interruption-dispatch`, rather than only traveling as a mirrored bootstrap guard in the current runtime patch
- acceptance_reviews:
  - reviewer: `codex-first-hop-audit`
    verdict: `still_pre_brainstorm`
    note: `Current repo truth keeps the lane inside candidate-owned boundary freeze. The runtime/script/test batch now proves the idle/replan scan seam, launch-time prompt consumption, and the narrow stale-pid bootstrap guard needed for startup re-entry, but the owner is still not IBM-ready because its patrol contract and provider/follow-on boundaries remain candidate-level only.`
- depends_on:
  - `docs/pre-brainstorms/20260407-0817--source-ledger-routing-and-manager-audit-boundary/candidates.md#c-20260407-0817-a`
  - `docs/epics/workspace-routing-foundation/manager-owner-stance-and-source-patrol-governance/issues/manager-owner-stance-and-source-patrol-governance.md`
- promoted_issue_path: `pending://issue-materialization`
- next_action: `Checkpoint the current bounded runtime/doc/test slice now that focused patrol-seam regressions pass, keep the bootstrap stale-pid guard as a narrow startup adjunct inside this owner, and revisit IBM only after the patrol contract is stable enough to freeze provider/follow-on boundaries.`
- revisit_trigger: `Revisit when external issue provider scan/writeback is ready to join the same patrol transaction, or when progress/recovery surfaces need to be promoted into the scan json rather than read ad hoc.`
- session_refs:
  - {tool: `codex`, session_id: `current-thread`, jsonl_path: `unavailable://codex-thread-only`, role: `author`}
- next_recommended_route: `doc-pre-brainstorm-execution`
- restart_point: `continuation`
- ownership: `worker-canonical-pre-brainstorm-writeback`
- checkpoint_decision: `checkpoint-after-focused-tests`
