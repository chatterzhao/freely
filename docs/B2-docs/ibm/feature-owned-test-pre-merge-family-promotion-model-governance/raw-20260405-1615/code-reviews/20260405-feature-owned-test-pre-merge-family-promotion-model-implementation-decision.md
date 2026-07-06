# Implementation Decision Note: feature-owned-test-pre-merge-family-promotion-model-governance

- issue_id: `I-20260405-1615-A`
- issue_path: `docs/B2-docs/ibm/feature-owned-test-pre-merge-family-promotion-model-governance/issues/feature-owned-test-pre-merge-family-promotion-model-governance.md`
- decision_date: `2026-04-05`
- author: `codex`

## Implementation Decision Note

- decision: `Freeze a single canonical test-pre-merge family that serves both single-feature and explicit multi-bundle develop promotion, and require follow-on enforcement owners to consume that model rather than invent new prefixes or direct feature -> develop shortcuts.`
- why_this: `The pain point is branch pollution and blocked integration throughput when develop becomes the first real test surface. A single protected premerge family gives each feature or bundle an isolated develop-like integration lane without reintroducing a second naming family or leaving room for direct feature -> develop escape hatches.`
- alternatives_considered: `Considered keeping test-pre-merge as replay-only evidence while feature branches remained the actual promote unit, and considered inventing a dedicated test-pre-multi-merge prefix. The first preserves the exact bypass path that caused the current governance gap, while the second splits one branch responsibility into two partially overlapping families and would force hooks, tests, and runtime surfaces to branch again.`
- boundary_non_goals: `This owner does not decide lifecycle automation, paired create/delete UX, manifest file formats, or the exact hook/script entrypoints that enforce the frozen model.`
- residual_risk: `Until every active execution surface consumes the frozen model, old wording or stale scripts can drift back toward replay-only semantics; that is why this owner immediately hands off to explicit gate-enforcement and lane-enforcement follow-ons.`
