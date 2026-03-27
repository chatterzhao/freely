# Pre-tests: pre-test-merge-responsibility-usage-and-lifecycle-governance

## Compatibility Note

- 历史 pre-tests/path 保留 `pre-test-merge` 命名，当前 canonical 语义按 `test-pre-merge-*` 测试批次前缀族解释。

## Pre-merge acceptance

1. `CONSTITUTION.md` 明确 `pre-test-merge` 是临时预集成验证批次，而不是长期开发父分支。
2. `LAWS.md` 明确：
   - `pre-test-merge` 只承担验证路径
   - stale / retire / replay 相关判断具有最小治理语义
3. `pre-test-merge-flow.md`、`cleanup-lifecycle.md`、`manager-reactivation-patrol.md` 对以下判断保持一致：
   - 何时当前批次仍有效
   - 何时当前批次必须 stale / retire
   - 何时 promotion 默认应回到来源 feature replay
4. 若某个 story 的 `pre-tests.md` 本身未通过 story-level 质量 gate，则不得把 `pre-test-merge` 批次上的测试执行误记为充分 acceptance：
   - 至少要能区分 `definition_missing`
   - `commands_only`
   - `evidence_plan_missing`
   - `execution_pending_or_failed`
5. `docs/milestones.md` 与本 issue 的下一跳一致：本 issue 只收敛职责定义，不直接承担能力实现。

## Non-goals

1. 不要求本 issue 直接产出 runtime/status 新字段。
2. 不要求本 issue 直接修复某个具体 `pre-test-merge` 批次。
3. 不要求在本 issue 中关闭后续 capability lifecycle。
