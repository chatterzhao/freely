# Implementation Decision: governance-check-protected-merge-history-source-policy-governance

- issue_id: `I-20260406-0045-A`
- issue_path: `docs/epics/workspace-routing-foundation/governance-check-protected-merge-history-source-policy-governance/issues/governance-check-protected-merge-history-source-policy-governance.md`

## Implementation Decision Note

- decision: `Audit protected merge receipts from each branch's first-parent merge history.`
- why_this: `The branch's canonical promote history lives on first-parent. Nested batch merges are valid on their own protected branch but are not direct merges into develop.`
- alternatives_considered: `Keeping all-reachable merge traversal would continue to misclassify nested test-pre-merge merges on develop; changing receipt trailers would distort the real source branch instead of fixing the audit target.`
- boundary_non_goals: `This owner does not redesign merge receipts or repair pr-merge-guarded's already-up-to-date exit path.`
- residual_risk: `If future policy wants to audit non-canonical merge ancestry separately, that should be a second explicit audit rather than silently sharing the develop source-policy check.`
