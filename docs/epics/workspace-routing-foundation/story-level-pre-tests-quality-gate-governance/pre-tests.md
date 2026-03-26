# Pre-tests: story-level-pre-tests-quality-gate-governance

## Acceptance Structure

### Pre-merge acceptance

1. Freely 真源明确：story-level `pre-tests.md` 至少必须表达
   - acceptance target
   - testing layer
   - target environment
   - required evidence
   - blocker taxonomy
2. Freely 真源明确：commands-only `pre-tests.md` 不合格。
3. Freely 真源明确：最小 blocker taxonomy 至少包括
   - `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
4. Freely 真源明确：`pre-tests.md` 质量失败与测试执行失败是两类不同 blocker。
5. 相关 truth sources 与既有 `integration-acceptance-first`、artifact-plane acceptance evidence、`pre-test-merge` / post-merge verification 口径一致。

### Post-merge acceptance

1. 本 issue 不要求单独的 post-merge acceptance 环境。
2. 若后续 follow-on 把 testing ladder 扩到 protected/post-merge acceptance，必须复用本 issue 冻结的质量 gate，而不是绕过它。

### Non-goals

1. 不要求在本 issue 中统一所有 story 模板格式。
2. 不要求在本 issue 中引入新的真实环境测试 harness。
