# Candidates - 20260406-0055--governance-check-nested-test-pre-merge-receipt-audit

## C-20260406-0055-A

- candidate_format_version: `v2`
- title: Governance-check nested test-pre-merge ancestry receipt audit false positive
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`
- promoted_issue_id: `I-20260406-0045-A`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- problem: after a canonical `feature/* -> test-pre-merge-* -> develop` promotion, `./bin/governance-check` on `develop` rejects internal merge `ab7a9b8` because it validates `Freely-Source-Branch: feature/...` against `develop` rules, even though that merge actually targeted `test-pre-merge-*`. This turns a valid promoted ancestry into a false protected-branch failure.
- why_now:
  - this is a real failure on canonical `develop`, not a hypothetical edge case
  - the repo has already frozen `test-pre-merge-*` as the only normal develop-bound promote family, so ancestry audit must understand that topology
  - leaving the false positive unresolved would make every future canonical premerge promotion look governance-invalid during post-merge followthrough
- acceptance_criteria:
  - `./bin/governance-check` must stop treating nested feature -> `test-pre-merge-*` merges as if they landed directly on `develop`
  - ancestry audit must still reject genuinely invalid protected-branch merges and must not reopen direct `feature/* -> develop` as a normal path
  - focused regressions must cover at least one valid nested feature -> `test-pre-merge-*` merge inside a promoted batch and one genuinely invalid source/target combination
- promotion_gate:
  - keep the owner on ancestry-audit interpretation, not generic merge-receipt or lifecycle automation redesign
  - do not absorb CLI packaging, runtime control-plane, or unrelated protected-branch ledger work
  - preserve the canonical `test-pre-merge-* -> develop` promote model while fixing the audit blind spot
- open_questions:
  - none; the absorbed owner already proved first-parent protected merge history is the correct contract for this false-positive family
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports_absorb`
    note: the false positive was real, but canonical `develop` already closed it under `I-20260406-0045-A`; this candidate should remain only as absorbed provenance instead of reopening a parallel owner.
- priority: `P1`
- decision_reason: the exact false-positive family was already absorbed and completed by `I-20260406-0045-A`, which switched protected-branch receipt auditing to first-parent protected merge history and added the nested `test-pre-merge-*` regression that this candidate was asking for.
- next_action: treat this pre-brainstorm as provenance for why `I-20260406-0045-A` widened from a concrete post-merge failure; future ancestry-audit regressions should open a new follow-on only if canonical `develop` regresses beyond that completed owner.
- revisit_trigger: reopen only if canonical `develop` again causes `./bin/governance-check` to reject a valid nested `feature/* -> test-pre-merge-* -> develop` ancestry after the `I-20260406-0045-A` fix is already present.
