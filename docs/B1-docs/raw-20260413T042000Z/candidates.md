# Candidates - 20260413-0420--real-repo-daemon-gap-and-foreground-double-start-regression

## Context

- Source brainstorm: `docs/B1-docs/raw-20260413-0420/brainstorms.md`
- Status: `split`
- Route: `promote-bounded-startup-authority-owner-and-keep-manager-handoff-research-visible`

## Candidates

### C-20260413T042000Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Manager startup continuity materialization governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260413T042000Z-D`
- promoted_issue_path: `docs/B2-docs/ibm/manager-startup-continuity-materialization-governance/issues/manager-startup-continuity-materialization-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/B2-docs/ibm/manager-startup-continuity-contract-governance/issues/manager-startup-continuity-contract-governance.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
- problem: Canonical `develop` now has authoritative startup identity and a frozen startup-handoff contract, but the normal startup path still does not materialize the first manager continuity artifact until stop fallback or later manager behavior. That leaves Freely's startup chain bootstrapped but not handoff-materialized on the success path.
- why_now:
  - startup authority is already canonical, so this lane no longer needs to solve launch identity or daemon-ready truth
  - the contract owner already froze the narrowest next seam: runtime-seeded continuity stub at the expected path plus machine-readable handoff state
  - real dogfooding still treats missing first continuity as a status surface or stop-repair symptom instead of a normal startup responsibility
- acceptance_criteria:
  - normal startup seeds a launch-bound manager continuity stub at the prompt-required continuity path before AI launch
  - the seeded startup artifact is distinguishable from stop-time repair fallback and from manager-materialized continuity
  - `live-status` and `fleet-status` expose machine-readable manager handoff state for `missing`, `seeded_stub`, `repair_fallback`, or `materialized`
  - stop fallback remains repair-only and is not redefined as normal startup success
  - focused regressions prove the new startup stub materialization and handoff-state surfaces without reopening daemon-ready semantics
- promotion_gate:
  - keep scope on startup stub materialization, handoff-state exposure, and repair-only fallback distinction
  - do not gate `daemon start` readiness on manager continuity in this first implementation pass
  - do not widen into generic worker continuity consumption, watchdog redesign, or a new artifact family
- open_questions:
  - whether later manager enrichment should preserve the runtime stub body or replace it wholesale once semantic continuity is written
  - whether a bounded SLA for `seeded_stub -> materialized` should become its own follow-on owner after this lane lands
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `The root cause is now narrow enough to implement directly: runtime must seed the first continuity artifact on the normal path and status must expose that handoff state separately from startup authority.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260413T042000Z-D` is now the canonical implementation owner for normal-path startup continuity stub materialization and manager handoff state surfacing.
- revisit_trigger: Re-open only if canonical implementation later proves the stub/state seam is wrong, or if manager handoff materialization still requires readiness-state coupling beyond this bounded owner.
- decision_reason: `This owner turns the frozen startup-handoff contract into the smallest runtime implementation slice that Freely can consume immediately: seed the expected continuity path on normal startup, surface what happened, and keep stop fallback visibly repair-only.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260413T042000Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Runtime startup root-cause packet governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260413T042000Z-C`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-startup-root-cause-packet-governance/issues/runtime-startup-root-cause-packet-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/gate/pretests-adequacy-item-schema-materialization-governance/issues/pretests-adequacy-item-schema-materialization-governance.md`
  - `docs/B2-docs/ibm/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- problem: The root-cause review is now strong enough to split into a promote-ready startup-authority lane and a still-research manager-handoff lane, but canonical `develop` cannot absorb candidate-only truth without a concrete owner package that records the split and its boundaries.
- why_now:
  - guarded develop replay already proved the current packet is blocked for lacking concrete owner truth rather than lacking more brainstorming
  - the split itself is bounded and documentation-only, so it should land now instead of keeping canonical routing behind a disposable feature branch
  - materializing this packet on `develop` keeps startup-authority implementation and manager-handoff follow-on cleanly separated before either dev-loop begins
- acceptance_criteria:
  - canonical `develop` records that `C-20260413T042000Z-A` is the promote-ready startup-authority owner boundary
  - canonical `develop` records that `C-20260413T042000Z-B` remains visible as follow-on research for the manager-handoff contract
  - the packet lands as a concrete issue/progress/review owner instead of candidate-only truth
  - the owner does not claim runtime authority/readiness or manager continuity implementation is already fixed
- promotion_gate:
  - keep scope on packet split, milestone routing, and guarded-promote sufficiency for this documentation-only owner
  - do not materialize `C-20260413T042000Z-A` into an implementation issue from this worktree
  - do not claim success for fake-supervisor, daemon-ready, or continuity behavior beyond documenting the root-cause split and next owner boundaries
- open_questions:
  - whether the future startup-authority implementation should carry daemon parity in the same owner or split again after launch-truth design freezes
  - whether the future manager-handoff owner should require a launch-bound stub artifact or another `manager_ready` truth surface
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `The pre-brainstorm analysis is mature enough that canonical develop should absorb the split itself now, but the actual runtime and continuity repairs still belong in later bounded owners.`
    verdict: `ready_for_issue_materialization`
- next_action: Materialize the packet as `I-20260413T042000Z-C`, run the bounded doc/governance verification path, guarded-promote the packet to `develop`, and then retire the temporary feature and premerge worktrees.
- revisit_trigger: Revisit only if guarded promote still says the packet lacks a concrete owner after issue/progress/review truth and develop-merge adequacy are present, or if a later implementation lane proves the split itself should be redrawn.
- decision_reason: `This owner exists only to canonically record the root-cause split and its routing. It intentionally stops before runtime implementation so startup authority and manager handoff can each reopen under their own bounded owners.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260413T042000Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Runtime startup authority and readiness governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260413T042000Z-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
  - `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
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
    summary: `The startup-authority half is implementation-ready as a bounded follow-on, but this research lane should stop at candidate split and milestone binding. The future owner package belongs in the dedicated implementation lane that will carry pre-tests, verification, and guarded promotion evidence.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260413T042000Z-A` is now the canonical owner for startup authority publication, daemon-ready truth, and authoritative supervisor cleanup.
- revisit_trigger: Re-open only if canonical implementation later regresses back toward pid/argv startup heuristics, or if daemon parity still proves to be a separate owner after authoritative startup truth is in place.
- decision_reason: `Foreground duplicate-start, daemon false-ready, fake-supervisor acceptance, and stop-marker ghost retention were promoted together into one bounded implementation owner because they all collapse onto the same startup authority/readiness defect.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`

### C-20260413T042000Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Manager startup continuity contract governance`
- research_only: `true`
- implementation_ready: `false`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260413T042000Z-B`
- promoted_issue_path: `docs/B2-docs/ibm/manager-startup-continuity-contract-governance/issues/manager-startup-continuity-contract-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-startup-authority-and-readiness-governance/issues/runtime-startup-authority-and-readiness-governance.md`
  - `docs/B2-docs/runtime/runtime-selfhost-continuity-gap-and-status-truth-governance/issues/runtime-selfhost-continuity-gap-and-status-truth-governance.md`
  - `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- problem: The real self-hosting startup path still treats "AI process spawned" as sufficient startup success even when the first manager continuity is absent until stop fallback. That weakens Freely's outer loop, restart point, and runtime artifact chain.
- why_now:
  - startup authority now landed on canonical `develop`, so the handoff lane no longer needs to wait for launch identity and bootstrapped truth
  - repeated review shows the remaining defect is a bounded startup-handoff contract, not a generic watchdog or status-family rewrite
  - Freely's three-loop and autonomy contract needs a first-handoff artifact on the normal path, not prompt-only wording plus stop fallback
- acceptance_criteria:
  - runtime and manager contract clearly distinguish `launch bootstrapped` from `manager handoff materialized`
  - the first manager continuity or equivalent launch-bound handoff artifact is created on the normal startup path, not only by stop fallback
  - fallback continuity remains repair-only and does not masquerade as normal startup success
  - recovery and restart logic can tell the difference between startup in progress, startup succeeded but manager handoff missing, and clean stop after valid handoff
- promotion_gate:
  - keep this owner on contract freeze and routing only; do not implement runtime stub writing or status fields from this worktree
  - do not solve this by prompt wording alone
  - do not reopen old continuity-gap status surfaces as if observability alone solves the contract defect
- open_questions:
  - what markdown/body shape should the first runtime-seeded continuity claim/stub use before manager enrichment
  - how should `live-status` expose `manager_handoff_state` without regressing current shared-status semantics
  - what bounded SLA should define "manager handoff missing" before recovery or repair activates
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `Startup authority is now canonical, and the remaining handoff defect is narrow enough to freeze as a dedicated contract owner without yet promising runtime implementation.`
    verdict: `ready_for_issue_materialization`
- next_action: Materialize the contract-freezing owner as `I-20260413T042000Z-B`, run the bounded doc/governance verification path, guarded-promote it to `develop`, and then let a later implementation owner add the normal-path stub and handoff-state runtime changes.
- revisit_trigger: Re-open only if later implementation proves the frozen contract is wrong, or if canonical runtime evidence shows the handoff seam must be widened beyond stub plus state exposure.
- decision_reason: `Manager continuity is now ready to materialize as a research-only contract owner: startup authority already froze the launch boundary, and the remaining task is to freeze the next implementation seam without mixing implementation into this packet.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
