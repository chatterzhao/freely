# Candidates - 20260413-1640--tasks-closeout-completion-and-adequacy-gate

## Context

- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260413-1640-A: legacy issue

- candidate_format_version: `v2`
- title: Tasks closeout completion and adequacy gate governance
- source_brainstorm: `docs/B1-docs/raw-20260413-1640/brainstorms.md`
- reopen_of_issue: `docs/B2-docs/ibm/structured-closeout-gate-context-and-review-evidence-governance/issues/structured-closeout-gate-context-and-review-evidence-governance.md`
- reopen_reason: `a real owner audit and guarded develop replay proved closeout contract hardening still omitted tasks.md, allowing completed lifecycle truth to drift from unchecked execution closeout boxes`
- problem: `pretests-gate` bound completion and guarded adequacy to issue `pre-tests.md` but did not also require sibling `tasks.md` closeout completeness, so owners could be recorded as completed while leaving unchecked execution tasks behind.
- why_now:
  - real completed owners `I-20260413-0420-B` and `I-20260413-0420-C` exposed the drift on canonical repo truth
  - the correct enforcement surface is already live in `pretests-gate`, so the smallest lawful fix is a narrow owner that adds `tasks.md` closeout scanning there rather than widening merge orchestration
  - the current feature lane cannot merge upstream until this implementation is attached to a candidate-driven lifecycle and review artifact
- acceptance_criteria:
  - `pretests-gate` rejects `phase_state=completed` owners when bound `tasks.md` is missing or still contains unchecked tasks
  - `pretests-gate --require-adequacy` applies the same `tasks.md` closeout check during guarded promote
  - `governance-merge-gate` inherits the behavior by delegation without adding a second `tasks.md` parser
  - `bash docs/system/workspace/scripts/tests/test-pretests-gate` passes
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` passes
  - `./bin/governance-check` passes
- promotion_gate:
  - do not demote `pre-tests.md` from its canonical verification-truth role
  - do not create a new tests ledger or merge-only copy of `tasks.md` parsing
  - keep the code change limited to bound tasks closeout validation and its focused regressions
- open_questions:
  - none; the gap, the desired enforcement surface, and the owner-bound fix were all reproduced directly in repo state
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `accepted`
    note: `The gap is a narrow contract omission: completion and guarded adequacy must read sibling tasks closeout truth from the same owner line without widening merge-gate policy.`
- decision_reason:
  - reopening the closeout-contract line keeps the repair on the same governance family that already hardened structured closeout fields and fresh review evidence
  - binding `tasks.md` in `pretests-gate` is the smallest defensible fix because that gate already owns completion and adequacy truth
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260413-1640-A`
- promoted_issue_path: `docs/B2-docs/ibm/tasks-closeout-completion-and-adequacy-gate-governance/issues/tasks-closeout-completion-and-adequacy-gate-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialized into a dedicated issue on branch `feature/tasks-closeout-gate-20260413`
  - keep enforcement in `pretests-gate`, derive sibling `tasks.md` from the owner contract, and fail closed on missing or unchecked task closeout
  - prove the delegated `governance-merge-gate` path stays aligned through focused regressions
- revisit_trigger:
  - reopen only if future closeout policy needs a broader multi-ledger contract than `pre-tests.md` plus owner-bound `tasks.md`, or if guarded promote starts requiring a different execution-completeness source
