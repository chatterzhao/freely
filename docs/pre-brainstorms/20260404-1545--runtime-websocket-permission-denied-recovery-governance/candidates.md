# Candidates - 20260404-1545--runtime-websocket-permission-denied-recovery-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260404-1545-A
- candidate_format_version: v2
- title: Bound runtime supervision when websocket permission-denied failures block manager continuity and intake claim
- problem: On canonical root `develop`, Freely can durably ingest human chat interruptions and inject them into fresh manager prompts, but repeated websocket `Operation not permitted` failures prevent the manager from writing new continuity or claiming intake items. The system therefore presents a false-active state: prompts keep refreshing while `intake/*.meta.env` remains `STATUS="new"` and no new continuity is materialized.
- why_now: This was observed immediately after `develop` was pushed on 2026-04-04. Continued supervision showed that root runtime can again inject fresh human interruptions into manager prompts, but the loop still degrades before claim/continuity writeback. New evidence also adds `codex slot switch is already in progress` and repo-local `fork: Resource temporarily unavailable` churn to the same blocked supervision surface.
- acceptance_criteria:
  - websocket permission-denied execution failures are classified into an explicit runtime-owned recovery path rather than collapsing into generic prompt churn
  - when manager runtime cannot consume intake, intake truth no longer remains indefinitely at `STATUS="new"` without a blocked or claimed state transition
  - manager continuity or an equivalent blocked handoff artifact records why supervision could not proceed and what recovery gate is now active
  - restart-storm pause does not keep re-emitting fresh prompts indefinitely without a new continuity or blocked-state artifact
  - if prompt assembly succeeds but claim/continuity writeback does not, runtime exposes that narrower blocked state instead of presenting a false-active manager loop
  - the contract explicitly states that GitHub issue create/sync capability is still pre-brainstorm-only and must not be assumed by runtime supervision
- promotion_gate:
  - prove the observed failure is a real supervision contract gap, not just a local environment one-off
  - freeze whether this belongs to an existing network/runtime family or needs a new narrow follow-on owner
  - define the minimum truth surface for blocked intake consumption before editing runtime code
- open_questions:
  - should websocket `Operation not permitted` map to `execution_network_persistent`, a new local-permission reason, or an environment-boundary fatal state
  - should `slot switch already in progress` and repo-local fork exhaustion share the same blocked-intake recovery contract or stay separate
  - should blocked intake be represented as a new intake status, a claimed reaction, or only via manager continuity/handoff artifact
  - what exact signal should stop prompt regeneration when continuity has not advanced
  - can the existing `runtime-network-failure-taxonomy-and-bounded-recovery-governance` family absorb this as a narrow follow-on, or is a supervision-specific owner required
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The failure is narrower than generic network taxonomy. Fresh evidence shows prompt assembly can recover while claim/continuity truth still does not converge, so the blocked-state contract must cover websocket denial, slot-switch busy, and local process exhaustion before runtime behavior is changed.`
    verdict: `promote_to_issue`
- priority: P1
- status: promoted
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-blocked-intake-and-continuity-truth-governance/issues/runtime-blocked-intake-and-continuity-truth-governance.md`
- next_action: Candidate mirror only. `I-20260405-2136-A` is now the canonical owner for prompt-visible-but-unclaimed runtime supervision; continue all follow-on implementation and verification from the issue-bound package instead of this pre-brainstorm candidate.
- revisit_trigger: Revisit only if canonical `develop` proves the blocked supervision family actually belongs inside an existing owner, or if the prompt-visible-but-unclaimed surface disappears without needing a dedicated lifecycle.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
  - tool: codex
  - session_id: current-thread-followthrough
  - jsonl_path: unavailable://codex-thread-only
  - role: supervision-followthrough
