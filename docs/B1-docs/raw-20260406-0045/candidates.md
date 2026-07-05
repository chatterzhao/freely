# Candidates

### C-20260406-0045-A
- candidate_format_version: v2
- title: Governance-check protected-merge history source policy
- status: promoted
- milestone: `M-20260306-workspace-routing-foundation`
- source_brainstorm: `docs/B1-docs/raw-20260406-0045/brainstorms.md`
- problem: `./bin/governance-check` currently audits all reachable protected merge commits on `develop`, so a valid `feature/* -> test-pre-merge-*` merge inside batch ancestry gets revalidated under develop-only source rules and causes a false negative on canonical post-merge followthrough.
- why_now:
  - canonical `develop` is currently red after a valid guarded merge
  - the break is caused by the new test-pre-merge promotion model and therefore must be absorbed as a governance follow-on, not left as local operator trivia
- acceptance_criteria:
  - `governance-check` audits protected merge receipts from each branch's first-parent history instead of all reachable merge ancestry
  - a direct invalid `feature/* -> develop` merge still fails
  - a valid `feature/* -> test-pre-merge-* -> develop` chain passes on `develop`
- promotion_gate:
  - materialize a narrow owner, land the history-scan fix plus focused regression, and rerun `./bin/governance-check` on canonical `develop`
- open_questions:
  - whether the same first-parent restriction should remain shared between ordinary receipt and break-glass receipt audits
- acceptance_reviews:
  - reviewer: `governance-audit-review`
    verdict: `supports`
    note: `Develop should audit its own canonical merge chain, not nested batch-internal merges.`
  - reviewer: `regression-replay-review`
    verdict: `supports`
    note: `A fresh repo replay of feature -> test-pre-merge -> develop is the right minimal regression for this failure.`
- decision_reason:
  - canonical `develop` is currently red after a valid guarded promotion
  - the fix boundary is narrow and entirely within protected merge receipt auditing
  - changing audit traversal is safer than rewriting receipt trailers for valid batch merges
- promoted_issue_id: `I-20260406-0045-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action: Materialize the owner and fix the protected-merge ancestry audit before any further closeout relies on `./bin/governance-check` being green.
- revisit_trigger: Re-open only if protected-branch receipt auditing still misattributes nested merge ancestry after first-parent scanning lands.
