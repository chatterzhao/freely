# PRD: integration-acceptance-first-verification-governance

## Goal

把 Freely 的 IBM 与 verification 收敛成“integration / acceptance first”的 AI-native 验收模型。

## Why Now

Freely 已经进入真正用 Freely 开发 Freely 的阶段。当前最容易复发的退化不是“没有测试”，而是：
- `pre-tests.md` 被写成附属清单
- verification 先退回到代码阅读
- merge 后才临时发现需要真正的 integration acceptance

## Product Surface

- `doc-ibm-execution`
- IBM references
- three-loop truth source
- `LAWS.md` 验收优先级口径

## Non-Goals

- 新测试 runner
- 新 review 模板系统
- 重写所有历史 issue 的 `pre-tests.md`

## Non-Negotiables

- 不把代码评审移除，只调整其默认优先级
- 不破坏 candidate-level acceptance 与 issue-level acceptance 的分层
- 不把历史已完成 issue 重写成当前真源

## Context Pack

- `doc-ibm-execution` 已要求 `prd.md -> pre-tests.md -> tasks.md`
- `prd-quality-bar` 已要求 `pre-tests.md` 能从 `prd.md` 自然派生
- `LAWS.md` 已要求 develop 合并前 `TEST`（含集成验收）通过
- 当前缺的是统一口径：默认先看 integration / acceptance evidence

## Decomposition Tree

1. IBM 层明确 `pre-tests.md` 的主控制面角色
2. IBM reference 明确 `pre-merge` / `post-merge` acceptance 表达
3. three-loop 明确 verification 优先级
4. `LAWS` 明确合并 gate 不以“代码已读完”替代 integration / acceptance evidence

## Prototype Path

最小原型就是把上述真源改成一致口径，并通过治理检查。

## Eval Plan

成功：
- IBM / loop / laws 三处口径一致
- 读者不再容易误解成“review-first”

失败：
- 仍能从真源里读出“先读代码，再决定要不要跑验收”
- `pre-tests.md` 仍像附属注释，而不是 acceptance 控制面

## Execution Slices

1. `doc-ibm-execution` 与 references
2. `three-loop-capability-lifecycle`
3. `LAWS`
4. lifecycle writeback

## Revisit Triggers

- 当 Freely 开始引入结构化 verification review 模板
- 当 GUI/TUI 接入更强的 acceptance runner
- 当 post-merge acceptance 成为更多 issue 的常态

## Dev-Loop Handoff

本 issue 的实现就是文档真源收敛本身，不需要额外代码开发。
