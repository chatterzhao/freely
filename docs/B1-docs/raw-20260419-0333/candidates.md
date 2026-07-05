# Candidates - 20260419-0333--runtime-closeout-selfhost-validation-followthrough

## Context
- Source brainstorm: `docs/B1-docs/raw-20260419-0333/brainstorms.md`
- Status: `promoted`
- Route: `materialize-bounded-runtime-closeout-selfhost-followthrough-owner`

## Candidates

### C-20260419-0333-A
- candidate_format_version: `v2`
- title: `Runtime closeout selfhost validation followthrough`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- promoted_issue_id: `I-20260419-0333-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/progress/workspace-routing-foundation/p-runtime-lifecycle-receipt-followthrough-governance.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `docs/system/workspace/scripts/runtime/interruption-manager-handler`
- problem: The post-merge checkpoint branch preserves real follow-on behavior changes for daemon attach reuse, ambiguous start-lock cleanup, and interruption closeout/continuation routing, but none of those changes are yet bound to a dedicated issue/progress chain.
- why_now:
  - current non-main worktree review shows this checkpoint is carrying active code rather than a retire-only snapshot
  - closeout/self-host validation surfaced concrete runtime and routing follow-ons after the receipt-ledger lane had already narrowed itself to governance-only scope
  - focused regressions already exist in-tree and can decide whether this should promote as one bounded owner or split
- acceptance_criteria:
  - the checkpoint diff is validated with focused regressions for daemon reuse, ambiguous start-lock cleanup, launch-failure lock release, and interruption-manager routing
  - the resulting owner shape is explicit as one bounded issue with concrete issue/progress/pre-tests/review truth
  - no receipt-ledger-only owner is silently reused to carry these runtime/routing changes
- promotion_gate:
  - keep scope bounded to the checkpoint diff preserved on `feature/checkpoint-runtime-closeout-selfhost-validation-20260419`
  - require concrete test evidence before guarded merge decisions
  - keep interruption closeout/self-host routing coupled only to this preserved follow-on seam
- open_questions:
  - is a new real-repo/self-host replay needed beyond the focused shell regressions already preserved in this checkpoint
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The checkpoint diff has focused green evidence and a shared closeout/self-host trigger surface, so it should promote as one bounded owner instead of drifting as an undocumented checkpoint.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260419-0333-A` is now the canonical owner for the preserved runtime closeout/selfhost follow-on.
- revisit_trigger: Re-open only if canonical develop later proves the daemon attach/start-lock half and interruption closeout routing half are actually independent seams requiring separate owners.
- decision_reason: `The receipt-only followthrough owner is too narrow, while the preserved checkpoint regressions show one stable bounded seam across runtime closeout and self-host routing behavior.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
