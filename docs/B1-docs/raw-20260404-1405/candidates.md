# Candidates - 20260404-1405--manager-bootstrap-prompt-publication-without-continuity-materialization

## C-20260404-1405-A

- candidate_format_version: `v2`
- title: Manager bootstrap prompt publication without continuity materialization governance
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md`
- promoted_issue_id: `I-20260404-1405-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: Canonical `develop` can generate a fresh manager prompt during `freely start`, but the runtime drops back to `stalled_without_runtime` before it materializes new manager continuity or worker prompt consumption, leaving `operator_stop` and `stopped` semantics ambiguous.
- why_now:
  - `develop` push followthrough is now unblocked, so the runtime bootstrap gap is the remaining P0 blocker for real supervision recovery
  - the failure is reproducible on current canonical `develop`
  - no active owner lawfully absorbs this control-plane gap
- acceptance_criteria:
  - reproduce and freeze the failing startup path from dispatcher-ready through prompt publication, continuity materialization, and post-start steady state
  - distinguish explicit human/operator stop from internal recovery/early-exit paths in manager bootstrap truth
  - restore a lawful startup contract where fresh manager prompt publication results in durable continuity or an explicit bounded failure artifact
  - ensure `live-status` and runtime events expose the real failure boundary instead of collapsing it into ambiguous `operator_stop`
- promotion_gate:
  - do not reopen completed runtime owners unless the new evidence proves their canonical contract false
  - do not paper over the problem by forcing `desired_runtime_state=stopped` without explaining the bootstrap exit
  - keep the lane focused on manager bootstrap, prompt publication, continuity materialization, and stop semantics
- open_questions:
  - is the real failure a premature bootstrap exit, a prompt-to-continuity publication contract break, or a false recovery stop?
  - should prompt publication itself become a stronger durability boundary, or should failure only be recorded after continuity generation is attempted?
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: Current evidence is concrete enough to materialize a focused owner instead of leaving the runtime stall as an unowned observation.
- next_action: Materialize the runtime/control-plane owner on `workspace-routing-foundation`, record the exact bootstrap evidence in canonical issue/progress truth, and then repair the failing path in a dedicated implementation lane.
- revisit_trigger: Reopen only if canonical `develop` can again generate manager prompt publication without durable continuity materialization after this owner is completed.
