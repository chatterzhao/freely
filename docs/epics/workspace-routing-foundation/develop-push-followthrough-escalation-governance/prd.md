# PRD: develop-push-followthrough-escalation-governance

## Goal

把 Freely 的 protected-branch followthrough 从“只暴露 push debt”收紧为“merge 后默认及时 push，并在必要时要求活跃 worktree 先 resync 最新 `develop` 再继续做治理判断”。

## Why Now

当前 repo 已经证明：

- lawful merge 之后，`develop` 可以长期只在本地领先 remote
- stale worktree 会继续基于旧上游做 owner / blocker / absorption 判断
- AI / runtime 中断会放大这个窗口

这说明 visibility 不是终点；下一层缺的是 sequencing contract。

## Product Surface

- `docs/LAWS.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/start-lead-agent.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/quality/governance-check`
- `docs/system/workspace/skills/worktree-maintenance-governance/SKILL.md`

## Non-Goals

- auto-push
- hidden network side effects
- replacing operator judgment with hook-only transport logic
- a generic git sync daemon

## Non-Negotiables

- merge 后若无 lawful defer，timely push 是默认 followthrough
- local-only canonical truth 不能静默长期悬空
- defer 必须有有限白名单与恢复点
- stale active worktree 若继续做依赖最新 protected truth 的判断，必须先 resync
- 第一阶段不引入 auto-push

## Context Pack

- 当前 repo 现场存在 `develop` ahead of remote 的 push debt
- 已完成 owner 只冻结了 `push_pending` / `push_deferred` 可见性
- 多工位治理已证明 stale upstream 会污染 owner judgment

## Decomposition Tree

1. timely push default
2. lawful defer taxonomy
3. `resync_required` trigger
4. status / patrol surfacing

## Prototype Path

最小原型不是自动推送，而是：

1. manager 能看见哪个 `push_pending` 已经该立即处理
2. status / patrol 能标记哪些树必须先 resync
3. defer 有限且可审，不再是开放式借口

## Eval Plan

成功：

- 真源明确“能 push 就应尽快 push”的默认语义
- defer reason 只有有限白名单
- `resync_required` 的触发条件明确绑定到 owner judgment / verification / cleanup 场景
- status / patrol 有明确的 followthrough next action

失败：

- push debt 仍只被当作可见但可长期悬挂的状态
- stale worktree 仍可继续做最新 `develop` 敏感判断
- defer 仍是开放式自由发挥文本

## Execution Slices

1. laws / manager truth
2. status / patrol wording
3. runtime / governance checks if needed

## Revisit Triggers

- 如果实现阶段证明 push urgency 与 resync trigger 完全不同步，再拆 owner
- 如果未来要做 auto-push 或 remote retry，再单开 follow-on

## Dev-Loop Handoff

本 issue 第一阶段是治理 contract 冻结。dev-loop 优先让 manager/status surfaces 能给出明确 followthrough judgment，而不是先做 transport automation。
