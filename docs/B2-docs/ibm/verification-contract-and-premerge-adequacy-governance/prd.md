# PRD: verification-contract-and-premerge-adequacy-governance

## Goal

把 Freely 的 verification contract 从“文档里已经写了测试理念”收紧为“manager/worker handoff 与 `test-pre-merge-* -> develop` merge gate 都会强消费 issue-bound `pre-tests.md`，并能诊断测试缺口落在哪一层”。

## Why Now

当前暴露的问题不是完全没有测试设计，而是设计没有闭环：

- `pre-tests.md` 有 contract
- `test-lane` 有 lane
- `pretests-gate` 有 completion enforcement
- `governance-merge-gate` 有 develop owner enforcement

但 promote 时仍不能稳定回答：

1. `pre-tests.md` 是否写了这次修改真正需要的测试任务
2. 是否从这些任务派生了测试用例 / acceptance items
3. 是否真的执行了这些测试
4. 是否把完成状态、证据、`not_applicable` 理由回写到真源

## Product Surface

- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/agents/worker-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/pretests-gate`
- `docs/system/workspace/scripts/quality/governance-merge-gate`
- `docs/system/workspace/hooks/pre-merge-commit.sh`
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`

## Non-Goals

- 自动生成全部测试命令
- 用 changed paths 或关键词猜该跑哪些测试
- 用 merge gate 替代测试设计和 worker judgment
- 强制重写所有历史 `pre-tests.md`

## Non-Negotiables

- `pre-tests.md` 继续是唯一 canonical verification truth
- `pre-tests.md` 必须始终包含 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四个章节
- `Unit`、`Integration`、`End-to-End` 三章不适用时必须使用有限 `not_applicable_reason` 枚举并补一句解释
- `Real-Environment` 固定为最终审查结论章，只写 `real_environment_status` 与 `real_environment_reason`
- handoff 不能只传调度信息，不传测试义务
- gate 必须是 issue-bound，而不是扫全仓
- gate 失败必须给出可执行提示，而不是抽象口号
- post-merge integration / real-environment / dogfood 不得被压扁成一个 smoke-only 面

## Context Pack

- `docs/LAWS.md` 已要求 `develop` merge 前优先看 issue-bound `pre-tests.md`
- `doc-ibm-execution` 已要求 `pre-tests.md` 默认覆盖 integration / real-environment / dogfood
- `pretests-gate` 只卡 `phase_state=completed`
- `pre-merge-commit` 当前只调用 `governance-merge-gate` / `governance-promotion-gate`
- runtime 当前只消费 `Worktree`、`Branch`、`dispatch_priority`、`parallel_safe`、`write_scope`、`intent_kind`、`intent_target`

## Decomposition Tree

1. 冻结 handoff verification metadata
2. 冻结 `pre-tests.md` 的四章骨架与 adequacy item schema
3. 冻结 fallback gate diagnostic taxonomy
4. 冻结 `test-pre-merge-* -> develop` 的 owner-bound consumption path

## Prototype Path

最小原型不是自动化整个测试编排，而是：

1. prompt 能明确告诉 worker 必测哪些 acceptance items
2. gate 在 promote 出口能区分：
   - `pre_tests_missing`
   - `testcase_derivation_missing`
   - `execution_missing`
   - `verification_state_missing`
3. 提示补哪一层，而不是只说 verification fail

## Eval Plan

成功：

- manager / worker 真源明确新增最小 verification metadata
- `doc-ibm-execution` / checklist / quality bar 明确强制 `Unit`、`Integration`、`End-to-End`、`Real-Environment` 四章
- 前三章不适用时只能使用有限 reason type，而不是直接省略
- `Real-Environment` 不再扩成第二套任务表，而是给出 pass/fail + reason 的最终审查结论
- `pre-tests.md` item-level schema 能 machine-readably 表达任务引用、测试用例设计、lane、environment、promotion requirement
- merge gate 设计明确只消费 owner issue 绑定的 `pre-tests.md`
- gate 设计明确能区分“没写任务”“没设计用例”“没测”“没标状态/证据”

失败：

- `pre-tests.md` 仍能通过缺章、跳章或自由发挥不适用理由混过去
- 仍需要靠口头解释才知道该跑哪些测试
- gate 仍只能报一个笼统的 “testing inadequate”
- 系统仍靠 path guessing 决定本次修改相关测试
- prompt 仍只告诉 worker “做验证”，但不告诉它验哪些 item

## Execution Slices

1. prompt / runtime header contract
2. `pre-tests.md` schema contract
3. adequacy gate contract
4. focused regression and verification evidence

## Revisit Triggers

- 如果实现阶段证明 prompt contract 与 gate contract 完全不同步，才拆成两个独立 owner
- 如果未来要做统一 test orchestration DSL，再开新 owner

## Dev-Loop Handoff

本 issue 的第一阶段交付是 contract freeze，不是一次性完成所有脚本实现。进入 dev-loop 时，优先落 handoff metadata 与 gate diagnosis 的最小可执行闭环。
