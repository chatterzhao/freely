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
- issue-bound brainstorm 的未决问题已不再阻断 dev
- implementation 所需文档引用齐备
- `prd.md` 已达到 AI-ready quality bar，而不是只剩人类摘要
- `pre-tests.md` 与 `tasks.md` 已被 `prd.md` 稳定约束

## Return package

- `issue_ref`
- `implementation_scope_summary`
- `required_doc_refs`
- `execution_base`
- `integration_target`
- `depends_on`
