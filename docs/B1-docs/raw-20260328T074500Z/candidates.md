# Candidates - 20260328-0745--live-status-current-runtime-state-reconciliation

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260328T074500Z-A: legacy issue
- candidate_format_version: v2
- title: Live-status current runtime state reconciliation governance
- problem: `live-status` simultaneously exposed a current-state answer (`activity_state: ai_active`) and stale persisted state (`last_ai_state: down`, `last_exit_reason: starting`), which made the current-state surface internally inconsistent whenever supervisor start had already launched AI but `workcell-state.env` had not been refreshed again.
- why_now: This inconsistency was visible on canonical `develop` during active runtime patrol, so it risked misleading both human operators and manager-side supervision exactly where `live-status` is supposed to be the fast current-state entrypoint.
- acceptance_criteria:
  - `live-status` keeps `last_supervisor_state` and `last_ai_state` aligned with confirmed project-owned live PIDs
  - `last_exit_reason` stops showing `starting` once the project-owned AI PID is confirmed live
  - the reconciliation remains read-only and does not mutate `workcell-state.env` during status reads
  - absence of a PID does not invent a new failure state
  - focused regression tests cover the active-AI reconciliation case without regressing watchdog-only and manager-recovery paths
- promotion_gate:
  - narrow the repair to the `live-status` read path
  - keep recovery, operator-stop, auth-failure, and restart-storm persistence semantics unchanged
  - add test coverage for the active-AI case
  - attach concrete owner issue, progress, and verification evidence in the same merge
- open_questions:
  - none
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The safe fix is a one-way read-time reconciliation toward confirmed project-owned live PIDs. Changing supervisor write timing would widen blast radius and is unnecessary for the observed inconsistency.`
    verdict: `ready_for_ibm`
  - reviewer: `gpt-5.4-mini explorer`
    mode: `independent code review`
    summary: `No findings. The main residual tradeoff is that live-status becomes more explicitly current-state-oriented rather than a pure persisted snapshot, which matches the command's purpose.`
    verdict: `ready_for_ibm`
- priority: P1
- status: promoted
- decision_reason: This is not a new product surface and not a broad same-family reopen. It is a narrow current-state reconciliation bug inside `live-status`, so the right lifecycle is a small promoted repair issue with a fresh compliant key rather than mutating an older non-compliant issue family.
- promoted_issue_path: `docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/issues/live-status-current-runtime-state-reconciliation-governance.md`
- milestone: `docs/milestones.md#M-20260306-workspace-routing-foundation`
- next_action: Merge the narrow runtime/test repair, then leave any broader status-family evolution to separate lifecycles.
- revisit_trigger: If a future patrol shows `live-status` again mixing current runtime truth with stale persisted state, or if reconciliation starts hiding real degraded conditions without a live project-owned PID, reopen this family as a new focused regression issue.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
