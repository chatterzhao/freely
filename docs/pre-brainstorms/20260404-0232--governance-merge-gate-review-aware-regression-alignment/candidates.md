# Candidates - 20260404-0232--governance-merge-gate-review-aware-regression-alignment

## Context

- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260404-0232-A

- candidate_format_version: `v2`
- title: Governance merge gate review-aware regression alignment
- source_brainstorm: `docs/pre-brainstorms/20260404-0232--governance-merge-gate-review-aware-regression-alignment/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/implementation-decision-notes-in-issue-review-artifacts-governance/issues/implementation-decision-notes-in-issue-review-artifacts-governance.md`
- reopen_reason: `post-merge acceptance proved test-governance-merge-gate still uses a pre-review-gate fixture for a mixed unresolved-candidate implementation case, so the regression now fails on missing staged review evidence before it reaches the current allowed path`
- problem: `test-governance-merge-gate` case `2d` omits the staged review artifact now required by the canonical gate, and the same post-merge inspection also exposed a file-scope bypass that lets same-file `promoted` / `absorbed` candidates borrow an unrelated owner.
- why_now:
  - canonical `develop` post-merge acceptance must leave merge-gate regression coverage green before push
  - the gate behavior is already correct, so keeping the stale fixture only creates false red acceptance noise
  - the smallest compliant fix is a narrow gate-and-test realignment: stage valid review evidence for the allowed unresolved-candidate case, and remove the same-file owner-binding bypass that contradicts existing pre-tests
- acceptance_criteria:
  - the reopened owner remains limited to review-aware regression alignment in `test-governance-merge-gate`
  - the mixed unresolved-candidate implementation case stages a complete owner review artifact before asserting pass
  - same-file `promoted` / `absorbed` candidates cannot borrow an unrelated owner issue/progress/review just because they share a `candidates.md` file with the true owner candidate
  - `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` passes without changing merge-gate semantics
  - `./bin/governance-check` passes
- promotion_gate:
  - do not widen this lane into a general merge-gate wording audit or policy rewrite
  - do not relax the implementation decision note contract
  - keep the fix limited to the narrow borrowed-owner bypass repair, regression fixtures, and the minimum lifecycle evidence
- open_questions:
  - none; the failing fixture, the current allowed path, and the same-file bypass are all reproduced
- acceptance_reviews:
  - reviewer: `codex`
    verdict: `accepted`
    note: `The gate contract is already mostly correct, but the current lane must both refresh the unresolved-candidate fixture and remove the same-file borrowed-owner bypass to match the documented pre-tests.`
- decision_reason:
  - this failure sits on the residual-risk line explicitly left by `I-20260401-2354-A` and re-exposes the owner-binding boundary from `develop-merge-issue-binding-and-cmi-governance`
  - reopening as a narrow follow-on preserves the canonical landing surface and keeps post-merge acceptance truthful
- priority: `P1`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260404-0232-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-merge-gate-review-aware-regression-alignment-governance/issues/governance-merge-gate-review-aware-regression-alignment-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialized into a dedicated issue on branch `feature/governance-merge-gate-diagnostic-alignment-20260404-023234`
  - refresh the mixed unresolved-candidate implementation fixture so it stages a complete review artifact before asserting pass
  - remove the same-file borrowed-owner bypass so `promoted` / `absorbed` regressions continue to fail lawfully
- revisit_trigger:
  - reopen only if future merge-gate contract changes again make this mixed unresolved-candidate implementation regression fail on an earlier guard, or if same-file borrowed-owner regressions start passing again
