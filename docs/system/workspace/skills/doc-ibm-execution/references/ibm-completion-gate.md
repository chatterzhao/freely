# IBM Completion Gate

## While still in IBM

补齐缺失项：

- issue-bound brainstorm
- `prd.md`
- `pre-tests.md`
- `tasks.md`
- 治理一致性修复

并验证：

- `prd.md` 满足 [prd-quality-bar.md](prd-quality-bar.md)
- `pre-tests.md` 来自 `prd.md` 的 eval / acceptance 结构
- `pre-tests.md` 默认以 executable integration / acceptance 为主，而不是只列代码检查点或 wording review 清单
- `pre-tests.md` 至少明确 acceptance target、testing layer、target environment、required evidence 与 blocker taxonomy
- `pre-tests.md` 能恢复关键 acceptance 面的 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
- `tasks.md` 来自 `prd.md` 的 decomposition / execution slices

并保持：

- `phase_state=in_ibm`
- 不为纯 IBM 工作伪造 `progress`
- 若依赖未合并父分支，保留 `execution_base`、`integration_target`、`depends_on`
- candidate-level acceptance 已在 issue-bound artifacts 中被继续深化

## Ready for dev

满足以下条件时进入 `done_ibm`：

- 文档已足够驱动实现
- issue scope 与 acceptance 稳定
- `pre-tests.md` 与 `tasks.md` 已体现 issue-level acceptance
- `pre-tests.md` 没有把 wording review 当成主验收面
- `pre-tests.md` 已能区分最小 blocker taxonomy：`definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`
- 若存在 merge 后才能验证的关键路径，`pre-tests.md` 已显式区分 `pre-merge` 与 `post-merge`
- 对 Freely 自治能力，`pre-tests.md` 默认已覆盖：
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
  - 若其中某类不适用，已显式写明理由与替代证据
- `post-merge acceptance` 已写明目标环境是 `develop` 还是某个 `test-pre-merge-*` 批次
- `post-merge acceptance` 已写明：在 protected branch worktree 中只做验证，不直接修实现
- 若目标环境是 `test-pre-merge-*`，语义已写明这是主线前临时验证批次，完成后走 replay 来源 feature + retire batch，而不是提升该批次本身
- 若目标环境是 `develop`，语义已写明这是主线后的 completion verification，而不是在 `develop` 上先预测试
- issue-bound brainstorm 的未决问题已不再阻断 dev
- implementation 所需文档引用齐备
- `prd.md` 已达到 AI-ready quality bar，而不是只剩人类摘要
- `pre-tests.md` 与 `tasks.md` 已被 `prd.md` 稳定约束
- issue 不再需要额外口头补充来区分 acceptance 定义失败与测试执行失败

## Return package

- `issue_ref`
- `implementation_scope_summary`
- `required_doc_refs`
- `execution_base`
- `integration_target`
- `depends_on`
