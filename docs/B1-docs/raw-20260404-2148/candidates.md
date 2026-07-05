# Candidates - 20260404-2148--slot-switch-lock-startup-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260404-2148-A
- candidate_format_version: v2
- title: Bound startup governance for stale or ambiguous codex slot-switch lock
- problem: Freely has already seen a real startup failure where a stale shared `~/.codex/slot-switch.lock` blocked runtime launch until the operator manually deleted it. The current root failure on 2026-04-04 is no longer a live lock, but startup governance still lacks a clear preflight and truth surface for stale, active, or ambiguous shared lock states.
- why_now: Dogfooding on canonical root `develop` showed two different truths on the same day: a stale shared lock was able to block startup earlier, while the latest repeated failure now exits with `auth_failure` and no current lock. That combination proves operators currently have to infer too much from logs and manual filesystem inspection.
- acceptance_criteria:
  - `freely start` can distinguish `active lock`, `stale lock`, `idle`, and `ambiguous lock` before launch
  - stale lock is auto-cleaned only when `owner_pid` is missing or dead
  - live shared lock never gets project-local force removal; startup instead waits, defers, or fails with explicit lock reason
  - `state.env` missing, unreadable, or malformed no longer leaks raw `sed` or equivalent race noise as the only operator signal
  - `doctor`, `live-status`, or an equivalent status surface exposes structured current slot-switch lock truth
- promotion_gate:
  - freeze whether the minimum truth surface is `start + doctor + live-status` or must also include `baseline-status`
  - confirm this owner stays separate from blocked-intake websocket supervision governance
  - define the narrow operator contract for stale cleanup, bounded wait, and ambiguous lock escalation
- open_questions:
  - should `baseline-status` be part of the minimum truth surface, or is `doctor + live-status` enough for first materialization
  - when `state.env` is missing but `owner_pid` still appears live, should startup classify that as `active_ambiguous` or a separate degraded state
  - should the preflight live in `cmd_start`, `start_project_runtime`, or a shared helper consumed by both `start` and status commands
  - what is the exact timeout / escalation contract for an active shared lock during startup
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The latest startup failure is not caused by a current lock, but the historical stale lock blocker is real and still lacks a governed preflight surface. This should be a narrow startup follow-on instead of being mixed back into blocked-intake supervision or reopened completed owners.`
    verdict: `needs_more_research`
- priority: P1
- status: promoted
- milestone: `M-20260306-workspace-routing-foundation`
- decision_reason: The boundary is now narrow enough to materialize cleanly. This owner stays separate from blocked-intake websocket supervision and from completed shared-slot owners, and it converts the startup/doctor/status contract into a dedicated runtime lifecycle.
- promoted_issue_id: `I-20260404-2148-A`
- promoted_issue_path: `docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- next_action: Implement the startup preflight plus minimal doctor/status lock truth on the dedicated `2148` feature lane and verify with focused runtime regressions.
- revisit_trigger: Re-open only if future evidence proves this startup/status lock contract was fully absorbed elsewhere or if a broader shared-slot redesign is explicitly opened.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
