# Brainstorm: candidate-acceptance-review-governance

- source_brainstorm: `docs/B1-docs/raw-20260320-0500/brainstorms.md`
- canonical_issue: `docs/epics/workspace-routing-foundation/candidate-acceptance-review-governance/issues/candidate-acceptance-review-governance.md`

## Key Decisions

- candidate-level acceptance boundary 需要显式化，而不是只保留 `next_action`。
- future candidate 默认进入 `candidate_format_version: v2`。
- promoted `v2` candidate 至少需要一次独立 `acceptance_reviews` 记录。
- IBM 需要把 candidate acceptance deepening 成 issue-level acceptance，而不是简单复制字段。
