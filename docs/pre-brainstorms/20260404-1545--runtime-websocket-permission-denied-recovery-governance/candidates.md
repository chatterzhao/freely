# Candidates - 20260404-1545--runtime-websocket-permission-denied-recovery-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260404-1545-A
- candidate_format_version: v2
- title: Bound runtime supervision when websocket permission-denied failures block manager continuity and intake claim
- problem: On canonical root `develop`, Freely can durably ingest human chat interruptions and inject them into fresh manager prompts, but repeated websocket `Operation not permitted` failures prevent the manager from writing new continuity or claiming intake items. The system therefore presents a false-active state: prompts keep refreshing while `intake/*.meta.env` remains `STATUS="new"` and no new continuity is materialized.
- why_now: This was observed immediately after `develop` was pushed on 2026-04-04. The runtime already distinguishes restart-storm and execution-time network failures, but the supervision loop still degrades into prompt-only churn instead of exposing a bounded blocked state for intake/continuity followthrough.
- acceptance_criteria:
  - websocket permission-denied execution failures are classified into an explicit runtime-owned recovery path rather than collapsing into generic prompt churn
  - when manager runtime cannot consume intake, intake truth no longer remains indefinitely at `STATUS="new"` without a blocked or claimed state transition
  - manager continuity or an equivalent blocked handoff artifact records why supervision could not proceed and what recovery gate is now active
  - restart-storm pause does not keep re-emitting fresh prompts indefinitely without a new continuity or blocked-state artifact
  - the contract explicitly states that GitHub issue create/sync capability is still pre-brainstorm-only and must not be assumed by runtime supervision
- promotion_gate:
  - prove the observed failure is a real supervision contract gap, not just a local environment one-off
  - freeze whether this belongs to an existing network/runtime family or needs a new narrow follow-on owner
  - define the minimum truth surface for blocked intake consumption before editing runtime code
- open_questions:
  - should websocket `Operation not permitted` map to `execution_network_persistent`, a new local-permission reason, or an environment-boundary fatal state
  - should blocked intake be represented as a new intake status, a claimed reaction, or only via manager continuity/handoff artifact
  - what exact signal should stop prompt regeneration when continuity has not advanced
  - can the existing `runtime-network-failure-taxonomy-and-bounded-recovery-governance` family absorb this as a narrow follow-on, or is a supervision-specific owner required
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The failure is narrower than generic network taxonomy. The visible gap is that supervision truth does not converge once manager websocket startup is denied, so a bounded blocked-state contract should be frozen before changing runtime behavior.`
    verdict: `needs_more_research`
- priority: P1
- status: proposed
- next_action: Decide whether to promote this as a follow-on to runtime network failure governance or as a new supervision-owned lifecycle for blocked intake/continuity truth.
- revisit_trigger: Revisit if a fresh root runtime can successfully claim the pending intake and write a new continuity despite websocket permission-denied churn, or if existing owner docs are updated to absorb this exact blocked-state contract.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
