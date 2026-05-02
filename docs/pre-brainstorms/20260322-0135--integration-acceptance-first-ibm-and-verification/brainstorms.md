# Brainstorm: integration-acceptance-first-ibm-and-verification

- brainstorm_id: `20260322-0135--integration-acceptance-first-ibm-and-verification`
- created_at: `2026-03-22`
- status: `active`
- related_signals:
  - 在 Freely 狗粮过程中，很多缺口不是先通过“读代码审查”暴露，而是通过 `freely start/chat/tui` 的集成行为暴露。
  - 现有 `doc-ibm-execution`、`prd-quality-bar`、`LAWS` 已要求 `prd.md -> pre-tests.md -> tasks.md` 的 AI-ready 验收链，但没有把“集成/验收优先”明确收成主导性验证策略。
  - 目前 code review 仍常被默认理解成逐行代码评审，而不是以行为验证、验收标准、集成测试为主。

## Problem

Freely 正在用 Freely 开发 Freely。AI-native 能力的缺口，往往首先表现在：
- 端到端行为不符合预期
- handoff / runtime / continuity / worktree 治理链断线
- `chat/tui/live-status/fleet-status` 等入口行为与真源设计不一致

这些问题如果继续主要依赖“读代码找问题”，会出现两个退化：
- 验收晚于实现，直到 merge 前才发现问题
- review 关注局部代码形状，而不是系统行为与 acceptance boundary

## Desired Outcome

把以下口径明确化：
- IBM 阶段产出的 `pre-tests.md` 不是附属文件，而是后续 dev-loop 和 verification 的主导验收面。
- AI 时代的默认验证顺序应优先是：
  1. 行为/集成测试
  2. 验收标准满足性
  3. 再到定向代码评审
- code review 仍存在，但应服务于风险定位、回归判断、验收缺口解释，而不是默认替代集成验证。

## Tensions

- 不能把“集成测试优先”误写成“永远不需要代码评审”。
- 不能只在 `LAWS` 补一句口号；必须让 `IBM / PRD / pre-tests / verification review` 的关系更明确。
- 不能破坏现有 `candidate acceptance review` 与 issue-level acceptance 的分层。

## Likely Landing Zones

优先扩展现有真源，而不是新增平行 skill：
- `docs/system/workspace/skills/doc-ibm-execution/SKILL.md`
- `docs/system/workspace/skills/doc-ibm-execution/references/prd-quality-bar.md`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- 视情况补 `LAWS.md` 的验证/验收口径

## Working Hypothesis

应新增一条能力：
- `integration-acceptance-first verification governance`

其核心不是“新增测试框架”，而是收敛 AI-native 的验收优先级：
- `pre-tests.md` 成为 issue-level acceptance 的主控制面
- verification 先回答“行为是否满足验收标准”
- code review 退居风险定位与缺口解释的二级角色

## Open Questions

1. `pre-tests.md` 是否应显式区分：
- smoke / integration / regression / non-goals
2. verification review 模板是否应先给出：
- 已通过的集成行为
- 未满足的 acceptance
- 只有在必要时再给代码层 findings
3. `LAWS` 是否需要明确：
- develop 合并 gate 默认优先看 integration / acceptance evidence，而不是代码阅读完成度
