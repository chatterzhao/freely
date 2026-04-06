# Candidates - 20260406-0055--governance-check-nested-test-pre-merge-receipt-audit

## C-20260406-0055-A

- candidate_format_version: `v2`
- title: Governance-check nested test-pre-merge ancestry receipt audit false positive
- status: `proposed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `pending://issue-materialization`
- promoted_issue_id: `pending://issue-materialization`
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
  - should audit ignore nested internal merges after validating the outer protected merge, or should it validate them against their own effective target branch rules
  - can the effective target/source pair be recovered from existing receipt fields and merge subjects, or is a narrower ancestry manifest needed
- acceptance_reviews:
  - reviewer: `codex-self-review`
    verdict: `supports`
    note: the failure is a post-merge ancestry-audit false positive introduced by the now-canonical premerge promotion topology, so it needs a narrow governance follow-on instead of widening the just-completed CLI packaging owner.
- priority: `P1`
- next_action: compare “ignore nested internal merges” versus “audit them against their effective target branch” using the concrete failing ancestry `ab7a9b8 -> 8e0985b`, then materialize a narrow owner.
- revisit_trigger: any later canonical `test-pre-merge-* -> develop` promotion still causes `./bin/governance-check` to reject an internal feature merge as if it were a direct merge into `develop`.
