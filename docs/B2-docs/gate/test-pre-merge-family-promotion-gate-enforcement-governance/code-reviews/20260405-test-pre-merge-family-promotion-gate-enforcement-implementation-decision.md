# Implementation Decision Note: test-pre-merge-family-promotion-gate-enforcement-governance

- issue_id: `I-20260405-1805-A`
- issue_path: `docs/epics/workspace-routing-foundation/test-pre-merge-family-promotion-gate-enforcement-governance/issues/test-pre-merge-family-promotion-gate-enforcement-governance.md`
- decision_date: `2026-04-05`
- author: `codex`

## Implementation Decision Note

- decision: `Bind the new promote model to both merge-time and audit-time enforcement by teaching pr-merge-guarded and governance-check that develop normally accepts only test-pre-merge-* and hotfix/* sources, while preserving the historical effective-date boundary for older ancestry.`
- why_this: `The observed failure mode was dual truth: docs were moving toward test-pre-merge promotion, but guarded merges and ancestry audit still encoded the older feature -> develop path. Closing only one side would leave either a bypassable gate or a permanently failing audit.`
- alternatives_considered: `Considered updating only pr-merge-guarded, only governance-check, or rewriting historical merge receipts to fit the new model. Single-surface changes leave contradictions in the other surface, while history rewrite is outside the lawful closeout path and unnecessary because an effective-date boundary already exists.`
- boundary_non_goals: `This owner does not automate stale-batch retirement, manifest generation, paired create/delete flows, or runtime visualization of test-pre-merge family state.`
- residual_risk: `If future branch families are added without updating both merge-time and audit-time contracts together, the repo can regress into split policy again; any such change must reopen this owner or a direct descendant.`
