# Brainstorms

## Topic
Manager continuation handoff consumption after interruption triage.

## Problem
Freely 已经能把 broad supervisor chat 正确分类为：
- `classification=control` 或 `continuation`
- `ownership=manager`
- `absorption_target=handoff://continuation`

但 supervisor 主循环没有稳定消费这条 handoff，导致：
- interruption resolution 已存在
- intake 已 delegated
- manager AI 仍停在旧 prompt/cycle
- 用户看不到真正的项目级 worktree 治理判断被产出

## Observed Dogfood Evidence
- `freely chat` on develop manager worktree created intake `20260322-004126-develop-worktree-live-status-fle`
- interruption resolved it to manager-owned continuation
- follow-up intake `20260322-004411-handoff-live-status-fleet-status` also resolved to manager continuation
- but loop log did not show a new cycle consuming the new handoff into fresh manager judgment output

## Why Existing Capability Is Insufficient
Existing capability from `manager-chat-reentry-and-cleanup-misrouting-governance` fixes the earlier bug:
- broad supervisor chat should not be swallowed by `cleanup://merged-worktree-followthrough`
- it should return to `handoff://continuation`

But current runtime still lacks the next step:
- after delegated manager continuation exists,
- supervisor / runtime must either preempt current stale manager round or schedule the next round to consume that handoff
- and produce explicit project-level supervision output

## Correct Target
Do not create a parallel manager skill.
This should extend current truth sources:
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- runtime handoff / restart logic in `docs/system/workspace/scripts/runtime/freely`
- likely the active issue line around manager chat reentry, or a tightly scoped sibling issue if lifecycle separation is required

## Boundary
This is not about:
- fixing prompt wording
- changing user chat semantics
- adding a new fourth loop
- manually forcing manager output in develop

This is about:
- ensuring delegated manager continuation is actually consumed by the next manager cycle
- preserving non-interactive autonomous operation
- keeping human role as out-of-band interruption only

## Questions To Settle
1. Should manager continuation consumption happen by:
   - graceful preemption of current manager AI round, or
   - next-cycle queueing after current round exits, or
   - a policy split depending on whether current round has already moved beyond notice/claim?
2. What exact artifact proves handoff consumption succeeded?
   - new prompt file referencing the delegated intake
   - new continuity writeback
   - new supervision resolution / worktree governance output
3. Should `live-status` expose a dedicated field for:
   - pending manager continuation handoff not yet consumed
   - manager continuation currently being consumed

## Expected Shape
CLI-first observability still remains the main frontend, but this issue is specifically about runtime/manager handoff consumption, not display polish.
