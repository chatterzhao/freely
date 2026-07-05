# PRD: story-level-pre-tests-quality-gate-governance

## Goal

把 story-level `pre-tests.md` 的最低质量门禁写进 Freely 真源，使其能够稳定恢复 acceptance contract，而不是只列命令。

## Why Now

Freely 最近多次暴露出同类问题：

- issue 有 `pre-tests.md`
- 也有一些脚本级或局部验证
- 但真实 acceptance target、环境和证据边界仍然要靠口头解释恢复

这说明当前缺的不是“再跑几条测试”，而是 `pre-tests.md` 本身还不够硬。

## Product Surface

- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/ibm-completion-gate.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/issue-materialization-checklist.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/epics/workspace-routing-foundation/pre-test-merge-responsibility-usage-and-lifecycle-governance/pre-tests.md`
- `docs/LAWS.md`

## Non-Goals

- 完整 testing evidence ladder
- 新测试执行框架
- 完整 real-environment harness 系统

## Non-Negotiables

- 不把 `pre-tests.md` 退化成 commands list
- 不把 artifact plane canonical evidence truth 搬到 status surface
- 不让质量失败与执行失败混成一种 blocker

## Context Pack

- `integration-acceptance-first-verification-governance` 已冻结 `pre-tests.md` 的 issue-level acceptance control surface 角色。
- `application-native-runtime-observation-contract-and-observability-planes` 已冻结 artifact plane 是 canonical acceptance evidence truth。
- 当前缺的是 story-level `pre-tests.md` 质量门禁本身。

## Decomposition Tree

1. 明确 story-level `pre-tests.md` 的最低字段和能力边界
2. 冻结 blocker taxonomy 的最小枚举：`definition_missing` / `commands_only` / `evidence_plan_missing` / `execution_pending_or_failed`
3. 明确不合格 `pre-tests.md` 的判定条件
4. 明确质量失败与执行失败的 blocker 区分
4. 把这些规则写回 IBM / lifecycle 真源

## Prototype Path

最小原型是让 Freely 真源能够一致拒绝下面这些退化情况：

- 只有命令，没有 acceptance target
- 有测试名，没有 target environment
- 有 environment，没有 required evidence
- blocker 没有区分 `definition_missing` / `commands_only` / `evidence_plan_missing` / `execution_pending_or_failed`

## Eval Plan

成功：

- 读者能仅凭 `pre-tests.md` 恢复 story acceptance contract
- 真源明确拒绝 commands-only `pre-tests.md`
- 真源明确给出最小 blocker taxonomy，后续 issue 不必再靠口头命名 blocker
- doc-loop / verification 不再需要大量口头补充来解释怎么测、测什么、缺什么

失败：

- `pre-tests.md` 仍可只列命令
- 仍无法区分质量失败与执行失败
- 仍需要 issue author 在聊天里额外解释 acceptance target

## Execution Slices

1. `doc-ibm-execution` skill 与 references truth update
2. `pre-test-merge` / post-merge lifecycle truth update
3. `three-loop-capability-lifecycle` 与 `LAWS.md` truth update
4. issue / milestone writeback

## Revisit Triggers

- 当 story-level quality gate 已冻结后，进入 broader testing evidence ladder materialization
- 当 Freely 开始标准化 real-environment harness contract

## Dev-Loop Handoff

本 issue 的 dev-loop 以文档真源收敛为主，不要求先写新的测试 runner。
