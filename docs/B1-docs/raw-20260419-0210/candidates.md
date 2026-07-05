# Candidates - 20260419-0210--protected-branch-ref-only-entrypoint-gap

- Source brainstorm: `docs/B1-docs/20260419-0210--protected-branch-ref-only-entrypoint-gap/brainstorms.md`

### C-20260419-0210-A

- candidate_format_version: `v2`
- title: `Protected-branch ref-only entrypoint enforcement`
- problem: `Protected branches still allow ref-only local advances such as git merge --ff-only to bypass the canonical guarded merge entrypoint because pre-merge-commit only runs when Git actually creates a merge commit.`
- why_now:
  - `2026-04-19` protected-root replay proved canonical `develop` could be fast-forwarded directly to a feature commit before push-time governance ran
  - this contradicts the declared contract that `freely pr-merge-guarded` is the canonical protected-merge entrypoint
  - leaving the gap open means protected-root local truth can diverge from the legal merge path even when later push-time governance still exists
- acceptance_criteria:
  - protected-branch ref-only advances to non-receipted commits fail before the branch ref is updated
  - receipt-bearing protected merge commits remain valid on `main`, `develop`, and `test-pre-merge-*`
  - focused regressions reproduce the blocked `git merge --ff-only` case and the allowed receipt-bearing merge case
  - the repair remains a narrow follow-on to entrypoint enforcement rather than a generic receipt or server-side governance rewrite
- promotion_gate:
  - do not reopen `I-20260405-0425-A`
  - do not widen into server-side enforcement or push policy redesign
  - keep the implementation at the protected-branch ref-transaction boundary
- open_questions:
  - whether future follow-ons should consume the same ref gate for additional protected-branch rewrite cases beyond the observed `ff-only` seam
  - whether hook documentation should explicitly distinguish merge-commit gating from ref-transaction gating for future owners
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: `This is a real follow-on gap because the prior owner only guarded merge-commit entry, while the observed failure moved the protected ref without creating a merge commit.`
- decision_reason:
  - the observed misuse is not hypothetical and it already escaped the completed merge-commit-only owner boundary
  - `reference-transaction` is the narrowest Git hook that can actually intercept the protected ref advance before it lands
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260419-0210-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/issues/protected-branch-ref-only-entrypoint-enforcement-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - materialize the narrow follow-on owner
  - wire protected-branch ref updates through `reference-transaction`
  - add focused regression proof for blocked `ff-only` and allowed receipt-bearing merge commit
- revisit_trigger:
  - protected-root local `develop` again advances to a non-receipted commit
  - the new ref gate blocks canonical receipt-bearing merge commits
