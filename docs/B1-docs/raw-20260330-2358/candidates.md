# Candidates - 20260330-2358--network-failure-recovery-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: active

## Candidates

### C-20260330-2358-A: legacy issue
- candidate_format_version: v2
- title: Introduce explicit network-failure taxonomy and bounded recovery contracts in Freely runtime
- problem: Freely already distinguishes `auth_failure`, rate-limit exhaustion, and `oauth_unreachable` during account inventory refresh, but it still lacks a canonical classification for generic in-flight network and proxy failures inside running `codex exec` workcells. As a result, transient or persistent execution-time network faults can collapse into generic `ai_exit_rc_*` handling and depend on coarse restart-storm protection rather than an explicit retry, cooldown, or circuit-breaker contract.
- why_now: Recent dogfood analysis showed that users naturally conflate proxy outage, OAuth reachability, quota exhaustion, and `402` workspace failures because Freely only models some of these states explicitly. The current behavior is partially correct at preflight time but still underspecified during execution, which risks blind relaunch loops, incorrect account switching, and unclear observability when the network path is the real dependency failure.
- acceptance_criteria:
  - Freely defines separate canonical states for proxy configuration errors, OAuth inventory reachability failures, transient execution-time network failures, and persistent execution-time network failures
  - each network state has an explicit recovery contract covering retry eligibility, retry budget, backoff behavior, cooldown or circuit-open behavior, and escalation surface
  - execution-time network failures no longer rely solely on generic `ai_exit_rc_*` plus restart-storm fallback
  - account switching remains excluded from the default recovery path for network failures unless independent slot-specific evidence exists
  - focused regressions can prove the intended behavior for preflight and execution-time network fault families
- promotion_gate:
  - prove the current runtime really lacks an execution-time network-failure taxonomy, rather than merely missing one log string
  - freeze the taxonomy and ownership boundaries before changing classifier code
  - keep the first issue scoped to runtime recovery semantics, not a broad redesign of proxy configuration UX
- open_questions:
  - should `execution_network_transient` prefer in-place `resume` when valid resume evidence exists, or always launch fresh with handoff after a bounded number of failures
  - should persistent network failures be surfaced as a project-local cooldown only, or also feed a global control-plane availability signal
  - should proxy endpoint health be actively probed, or is failure-window inference from tool exits sufficient for the first issue
  - which network error signatures are safe to classify as transient across supported tools without overfitting to Codex-specific wording
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The repo already models oauth_unreachable but not generic in-flight network failure. A safe next step is to freeze a network-failure taxonomy and recovery contract before any classifier or supervisor patch is attempted.`
    verdict: `needs_more_research`
- priority: P1
- status: promoted
- decision_reason: The taxonomy is now narrow enough to materialize: runtime classifies execution-time network failures and explicit proxy-config-invalid signals into a bounded in-place retry/cooldown contract, while keeping slot/tool fallback out of the default path.
- promoted_issue_path: `docs/B2-docs/runtime/runtime-network-failure-taxonomy-and-bounded-recovery-governance/issues/runtime-network-failure-taxonomy-and-bounded-recovery-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- next_action: Keep `I-20260330-2358-A` in verification until the bounded runtime recovery owner, focused regressions, and truth-source updates merge into `develop`.
- revisit_trigger: Revisit if execution-time network failures still trigger slot/tool fallback, if proxy-config-invalid is routed into auth/account switching, or if persistent dependency outages still spin through generic `ai_exit_rc_*` churn.
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
