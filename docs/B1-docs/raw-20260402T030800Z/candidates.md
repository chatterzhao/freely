# 候选：runtime-status-time-display-audit

- id: `C-20260402T030800Z-A`
- candidate_format_version: `v2`
- title: Materialize host-local rendering for human-readable runtime status time surfaces
- source_brainstorm: `docs/B1-docs/raw-20260402-0308/brainstorms.md`
- problem: Freely already moved Probe Recent Activity plus `freely ai` and watchdog cooldown helper output onto host-local display time with timezone labels, but core runtime status surfaces still echo raw ISO/UTC truth for humans. That leaves the same product with split display semantics and no dedicated owner for the runtime slice.
- why_now:
  - the broader time-boundary research is already merged and should not remain half-absorbed under a frontend owner
  - `freely live-status`, `baseline-status`, `develop-push status`, and intake status are user-facing surfaces, not raw machine truth
  - the current feature branch already contains the narrow runtime/test implementation and only lacks canonical lifecycle materialization
- acceptance_criteria:
  - `freely live-status` renders `last_state_updated_at`, `activation_consent_recorded_at`, intake `created_at`, and develop-push defer timestamps in host local time with timezone label
  - `freely baseline-status` renders `activation_consent_recorded_at` in host local time with timezone label
  - `freely develop-push status` renders `develop_push_followthrough_defer_updated_at` in host local time with timezone label
  - `freely ai status` exposes both raw cache refresh truth and a host-local `refreshed_at_human` display field
  - watchdog cooldown human-readable fields continue to render host-local time with timezone label
  - no persistent timestamp truth, backup naming, or RFC3339/epoch storage fields are rewritten
- promotion_gate:
  - keep the slice strictly on human-readable display surfaces
  - do not rewrite `.bak` or governance naming timestamps away from UTC
  - do not change stored `created_at`, `occurredAt`, `reset_at`, or RFC3339/epoch machine truth
  - do not reopen `frontend-probe-v0`; that owner keeps only the Probe display slice
- open_questions:
  - whether future TUI/GUI surfaces should share a common formatter module across shell and frontend stacks
  - whether user-selectable timezone preferences should become a later product capability rather than host-local default only
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The runtime/status slice is real, already partially implemented, and should be owned explicitly instead of remaining hidden under frontend continuation.`
    verdict: `ready_for_ibm`
- priority: `P1`
- status: `promoted`
- decision_reason:
  - the real product rule is layered: UTC naming truth, RFC3339/epoch storage truth, host-local display truth
  - frontend absorbed only one surface; runtime/status surfaces need their own owner and verification
  - this owner legitimizes already-landed `ai-cli` and watchdog display changes while extending the same contract into `freely` status outputs
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-human-readable-time-display-governance/issues/runtime-human-readable-time-display-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - `I-20260402T030800Z-A` now owns the runtime/status slice: `freely` status displays, `freely ai status` human-readable refresh surfaces, watchdog cooldown human text, and verification that machine truth stays unchanged.
- revisit_trigger:
  - materialize a new follow-on if Freely adds user-selectable timezone preferences or needs a shared formatter across future TUI/GUI/runtime surfaces.
