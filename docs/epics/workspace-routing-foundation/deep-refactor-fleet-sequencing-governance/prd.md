# PRD: deep-refactor-fleet-sequencing-governance

## Goal

在 Freely 准备 broad/deep refactor 前，先用一条统一的 fleet sequencing gate 判断当前 worktree、runtime 与 upstream governance 的收口顺序，避免在 fleet 状态模糊时直接开始大改。

## Why Now

这次真实 fleet 已经暴露了 sequencing 缺口：

- canonical `develop` 仍挂 `desired=running`，但没有 runtime
- develop-facing merge-prep 工位仍然 dirty
- 多棵上游治理树已完成却尚未被统一吸收

如果没有统一 gate，下一轮深层重构仍会踩进同样的混乱。

## Product Surface

- `AGENTS.md`
- `docs/milestones.md`
- `docs/progress/workspace-routing-foundation/p-deep-refactor-fleet-sequencing-governance.md`

## Non-Goals

- 不改 Freely 运行期能力真源
- 不引入新的 runtime health detector
- 不把 merge-prep 工位直接等同于完成 merge / retire

## Non-Negotiables

- 这条规则属于开发 Freely 的治理输入，不得误写成 `docs/system/**` 能力 contract
- 大重构前必须先检查 dirty/running/owner 工位
- 要先判断哪些上游治理树会被后续工作直接消费

## Context Pack

- `AGENTS.md` 是开发 Freely 的入口，而不是产品能力真源
- `wt-fleet-status`、`freely live-status`、`milestones` 与 `progress` 必须一起看
- sequencing gate 要服务后续 refactor lane，而不是替代每条 issue 自己的 lifecycle

## Decomposition Tree

1. 固化 pre-refactor fleet audit 命令面
2. 固化高风险工位优先原则
3. 固化 upstream governance merge order judgment
4. 写回 lifecycle evidence

## Prototype Path

最小原型就是：

- `AGENTS.md` 有可执行的 audit gate
- fleet 实际状态已按该 gate 收束一次
- 文档证明这条 gate 足以指导下一轮 deep refactor 开始前的排序

## Eval Plan

成功：

- 新会话仅读 `AGENTS.md` 就知道 broad/deep refactor 前要先做 fleet sequencing audit
- fleet 实际状态已没有假 `desired=running` 与 dirty closeout owner 阻塞
- 上游治理 merge-prep 工位已准备好继续向 `develop` 吸收

失败：

- 仍然能跳过 fleet audit 直接开深层重构
- 仍然把 clean/stopped 非阻塞工位误当第一优先
- 仍然把这条规则说成 Freely 产品能力而不是开发治理

## Execution Slices

1. `AGENTS.md` gate
2. candidate -> issue materialization
3. progress / milestone writeback
4. verification review

## Revisit Triggers

- 若后续要把 sequencing gate 上升到更高等级的 `LAWS`
- 若后续要把 fleet sequencing judgement 自动化
- 若 broad/deep refactor 再次在 clean/stopped 与 dirty/running 工位排序上失焦

## Dev-Loop Handoff

这条 issue 的实现就是开发治理文档与 lifecycle writeback 本身。
