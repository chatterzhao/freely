# Implementation Decision Note: develop-push-triage-merge-receipt-gap-followthrough

- issue_id: `I-20260404-0640-A`
- issue_path: `docs/epics/workspace-routing-foundation/protected-branch-merge-receipt-gap-followthrough/issues/protected-branch-merge-receipt-gap-followthrough.md`
- decision_date: `2026-04-04`
- author: `codex`

## Implementation Decision Note

- decision: `Keep the ordinary protected-merge receipt-gap owner narrow, but teach governance-check to validate trailerless ancestry merges against their actual merge subject so develop -> feature/* merges that later enter protected ancestry can use the canonical backfill ledger.`
- why_this: `The failing gap 70ef97d is already reachable from develop ancestry, yet its historical merge subject targets a feature branch rather than develop itself. Matching ledger entries against the subject target/source pair preserves auditability without pretending the merge originally targeted a protected branch.`
- alternatives_considered: `Considered deleting the 70ef97d ledger entry and treating the ancestry merge as out of scope, and considered widening the ledger schema into a generic ancestry exception list. The first keeps governance-check red on canonical develop, while the second loses the narrow protected-merge repair semantics this owner is supposed to preserve.`
- boundary_non_goals: `This slice does not weaken canonical trailer requirements for future protected merges, does not rewrite history, and does not create a general exemption path for arbitrary non-protected merges.`
- residual_risk: `Any future ancestry gap with an unparseable merge subject will still fail closed and require a narrower follow-up instead of silently passing audit.`
