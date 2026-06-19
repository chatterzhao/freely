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
- `pre-tests.md` 至少固定 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四个章节
- `Unit`、`Integration`、`End-to-End` 三章若不适用，`pre-tests.md` 已写 `not_applicable_reason`、`not_applicable_explanation` 与必要的 `replacement_evidence`
- `Real-Environment` 章节固定写 `real_environment_status` 与 `real_environment_reason`，作为“本次实现是否需要真实环境测试、以及是否已达标”的最终审查结论
- 若当前 issue 是 follow-on owner，且 scope 触达 `auth switch / account switch / slot recovery / startup recovery / watchdog / freely start / bin/ai / codex exec` family，`Real-Environment` 不能只填结论就过；至少要保留一条 artifact-backed 的 `real_env` 或 `post_merge_dogfood` acceptance item
- `Unit`、`Integration`、`End-to-End` 三章至少明确 acceptance target、testing layer、target environment、required evidence 与 blocker taxonomy
- `pre-tests.md` 能恢复关键 acceptance 面的 `environment`、`evidence`、`failure signal`、`failure handling / replay expectation`
- issue 已显式声明 `pre_tests_path` 与 `verification_artifact_dir`
- `pre-tests.md` 已包含 completion gate 可消费的 machine-readable acceptance items：`id` / `requirement` / `evidence_level` / `status` / `artifact_ref`
- 对新写或正在升级 adequacy 的 owner，`Acceptance Items` 默认同步写 v2 adequacy 字段：`surface_kind` / `target_lane` / `promotion_gate`
- 对 `develop` promote 相关 item，优先把 lane/gate 写成 `target_lane: premerge-integration` 与 `promotion_gate: develop_merge`
- `task_refs` 与 `case_design` 默认作为强建议字段补齐，避免只有标题式测试项
- `tasks.md` 来自 `prd.md` 的 decomposition / execution slices

并保持：

- `phase_state=in_b2_ibm`
- 不为纯 IBM 工作伪造 `progress`
- 若依赖未合并父分支，保留 `execution_base`、`integration_target`、`depends_on`
- candidate-level acceptance 已在 issue-bound artifacts 中被继续深化

## Ready for dev

满足以下条件时进入 `done_b2_ibm`：

- 文档已足够驱动实现
- issue scope 与 acceptance 稳定
- `pre-tests.md` 与 `tasks.md` 已体现 issue-level acceptance
- `pre-tests.md` 没有把 wording review 当成主验收面
- `pre-tests.md` 没有缺失 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 中的任一章节
- `pre-tests.md` 已能区分最小 blocker taxonomy：`definition_missing`、`commands_only`、`evidence_plan_missing`、`execution_pending_or_failed`
- 对 auth/switch/startup-recovery/watchdog follow-on owner，`pre-tests.md` 没有把 `Real-Environment` 写成 `pass` 却又缺失 artifact-backed 的 live-evidence acceptance item
- 若存在 merge 后才能验证的关键路径，`pre-tests.md` 已显式区分 `pre-merge` 与 `post-merge`
- 对 Freely 自治能力，`pre-tests.md` 默认已覆盖：
  - post-merge integration acceptance
  - post-merge application-native real-environment acceptance
  - post-merge end-to-end dogfood acceptance
  - 若其中某类不适用，已显式写明理由与替代证据
- `post-merge acceptance` 已写明目标环境是 `develop` 还是某个 `test-pre-merge-*` 批次
- `post-merge acceptance` 已写明：在 protected branch worktree 中只做验证，不直接修实现
- 若目标环境是 `test-pre-merge-*`，语义已写明这是主线前临时验证批次，完成后回到来源 `feature/*` / `fix/*` 走 guarded PR/merge 进入 `develop`，并 retire 该批次
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

## Evidence Level Integration

This gate consumes the five-level testing evidence ladder by reference — do not redefine levels locally.

Refer to `docs/epics/testing-evidence-ladder/testing-evidence-ladder-and-gate-mapping/prd.md` for:

- **Five evidence levels**: script regression, integration, end-to-end scenario, application-native real-environment, protected-env post-merge acceptance. Each level has a defined default purpose, promotion trigger, what it can prove, and what it cannot replace.
- **Completion gate minimum evidence**: per issue class, the minimum `evidence_level` required before `phase_state: completed` may be set.
- **Retirement gate minimum evidence**: per issue class, the minimum `evidence_level` required before a worktree may be retired.
- **Blocker taxonomy**: `evidence_gap` (level not met) vs `execution_pending` (tests defined but not yet run).

Acceptance items in `pre-tests.md` MUST set `evidence_level` to one of the five ladder levels. A lower level passing does NOT satisfy a gate that requires a higher level.
