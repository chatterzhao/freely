# Tasks: story-level-pre-tests-quality-gate-governance

1. 更新 IBM / reference 真源，明确 story-level `pre-tests.md` 最低质量线。
2. 在 IBM / reference 真源中冻结最小 blocker taxonomy：`definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`。
3. 更新 `pre-test-merge` / post-merge verification 相关真源，确保它们消费同一套质量 gate，而不是平行定义。
4. 更新 lifecycle / verification 真源，明确 `pre-tests.md` 质量失败与执行失败的 blocker 区分。
5. 明确 commands-only `pre-tests.md` 不构成 acceptance control surface。
6. 保持与 artifact-plane acceptance evidence / status-surface mirror contract 一致。
7. 回写 issue / milestone / umbrella candidate。
