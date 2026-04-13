# Candidates - 20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression

## Context

- Source brainstorm: `docs/pre-brainstorms/20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression/brainstorms.md`
- Status: `split`
- Route: `promote-bounded-startup-authority-owner-and-keep-manager-handoff-research-visible`

## Candidates

### C-20260413-0420-A

- candidate_format_version: `v2`
- title: `Runtime startup authority and readiness governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260413-0420-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
  - `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- problem: Current `develop` still treats startup authority as "some PID looks like the project supervisor". That allows fake-supervisor acceptance, daemon ready false positives, early unlock before durable startup truth, duplicate same-project startup chains, and stop-marker cleanup based on ghost ownership.
- why_now:
  - repeated real-repo foreground and daemon repros show the authority defect is still live on canonical `develop`
  - the exact code-level fault is now bounded enough to repair without reopening whole entrypoint semantics or whole continuity policy
  - the old owners in this area are completed and should stay closed; the remaining defect needs a fresh bounded owner
- acceptance_criteria:
  - runtime owns an authoritative startup identity for the current launch instead of inferring truth from argv resemblance
  - same-project bootstrap produces exactly one authoritative launch during the bounded startup window
  - `daemon start` does not report ready until the current launch has published startup truth for that launch
  - fake argv or ghost processes do not pass supervisor validation or preserve stop markers
  - stop followthrough and cleanup only retain stop state when another validated launch truly exists
  - verification includes a real-repo or equivalent high-fidelity daemon smoke proving the daemon surface agrees with the same startup-authority model
- promotion_gate:
  - keep scope on launch identity, startup truth publication, attach or wait or repair rules, daemon ready semantics, and cleanup truth
  - do not fold manager continuity contract redesign into this owner
  - do not claim success from synthetic daemon acceptance alone; the closeout gate must include a real-repo-shaped replay
- open_questions:
  - whether the minimum viable launch truth can be carried in one `startup-truth` file or needs a launch-scoped pair of identity and readiness projections
  - whether daemon ready should gate on startup truth only, or also on a bounded control-plane-ready phase beyond `supervisor_started`
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `The startup-authority half is now implementation-ready. The root cause is bounded to launch identity, authority publication timing, and ready determination across both foreground and daemon entrypoints.`
    verdict: `promote`
- next_action: Materialize `I-20260413-0420-A` as the new bounded owner for launch identity, startup readiness, duplicate-start prevention, daemon-ready truth, and ghost-supervisor cleanup followthrough.
- revisit_trigger: Re-open only if canonical implementation later proves daemon parity failure belongs to a separate root cause outside the launch-authority model.
- decision_reason: `Foreground duplicate-start, daemon false-ready, fake-supervisor acceptance, and stop-marker ghost retention are different symptoms of the same authority/readiness defect, so they should share one new bounded owner.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260413-0420-B

- candidate_format_version: `v2`
- title: `Manager startup continuity contract governance`
- research_only: `false`
- implementation_ready: `false`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `pending://issue-materialization`
- promoted_issue_path: `pending://issue-materialization`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- problem: The real self-hosting startup path still treats "AI process spawned" as sufficient startup success even when the first manager continuity is absent until stop fallback. That weakens Freely's outer loop, restart point, and runtime artifact chain.
- why_now:
  - the latest root-cause review shows this is deeper than a status-surface gap but not yet reduced to one implementation shape
  - fixing startup authority alone will not define whether manager continuity is required for manager-ready semantics
  - Freely's three-loop and autonomy contract needs a cleaner startup handoff boundary than prompt-only wording
- acceptance_criteria:
  - runtime and manager contract clearly distinguish `launch bootstrapped` from `manager handoff materialized`
  - the first manager continuity or equivalent launch-bound handoff artifact is created on the normal startup path, not only by stop fallback
  - fallback continuity remains repair-only and does not masquerade as normal startup success
  - recovery and restart logic can tell the difference between startup in progress, startup succeeded but manager handoff missing, and clean stop after valid handoff
- promotion_gate:
  - keep this candidate out of implementation until the startup-authority owner clarifies the launch identity and phase model it will build on
  - do not solve this by prompt wording alone
  - do not reopen old continuity-gap status surfaces as if observability alone solves the contract defect
- open_questions:
  - should runtime seed a continuity claim or stub before AI launch, or should manager-ready be enforced through another launch-bound artifact
  - how should `live-status` expose `bootstrapped` versus `manager_ready` without regressing current shared-status semantics
  - what bounded SLA should define "manager handoff missing" before recovery or repair activates
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `The manager continuity contract is clearly a distinct owner boundary, but the implementation shape still depends on the launch-authority model chosen by the promote-ready startup owner.`
    verdict: `needs_more_research`
- next_action: Keep this candidate visible under the active milestone while `I-20260413-0420-A` fixes startup authority; then reopen this candidate with a narrowed handoff contract built on the resulting launch phases.
- revisit_trigger: Revisit when the startup-authority owner lands a concrete launch identity/phase model, or if further real-repo evidence proves the continuity contract can be implemented independently without waiting.
- decision_reason: `Manager continuity is a true follow-on owner boundary, but it should not be mixed into the startup-authority implementation before the launch model is fixed.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
