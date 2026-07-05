# Brainstorms

## Topic
Manager continuation handoff consumption after interruption triage.

## Problem
Freely 已经能把 broad supervisor chat 正确分类为：
- `classification=control` 或 `continuation`
- `ownership=manager`
- `absorption_target=handoff://continuation`

但 delegated manager continuation 在 runtime 里的后续消费仍不够可靠，导致：
- interruption resolution 已存在
- intake 已 delegated
- handoff 可能已经写入下一轮 prompt
- 但在 `context_compacted -> fresh_with_handoff`、本地 preemption、或 `auth_failure` 停机边界上，用户仍看不到稳定的“这条 handoff 是否已被主循环消费”的证据

## Observed Dogfood Evidence
- `freely chat` on develop manager worktree created intake `20260322-004126-develop-worktree-live-status-fle`
- interruption resolved it to manager-owned continuation
- follow-up intake `20260322-004411-handoff-live-status-fleet-status` also resolved to manager continuation
- first delegated manager continuation was injected into the next prompt as `Delegated continuation handoff`
- second manager continuation triggered local preemption
- the next runtime path then hit `context_compacted`, rotated to `fresh_with_handoff`, and finally stopped on `auth_failure`
- runtime therefore lacks a stable generated-vs-consumed evidence surface for manager continuation handoffs

## Why Existing Capability Is Insufficient
Existing capability from `manager-chat-reentry-and-cleanup-misrouting-governance` fixes the earlier bug:
- broad supervisor chat should not be swallowed by `cleanup://merged-worktree-followthrough`
- it should return to `handoff://continuation`

But current runtime still lacks the next step:
- after delegated manager continuation exists, runtime must preserve a durable record of:
  - handoff generated
  - handoff injected into a later prompt
  - handoff still pending or superseded
- the `fresh_with_handoff` path must not lose this trail
- auth/rate-limit stoppage must leave enough evidence for the next manager re-entry to continue correctly

## Correct Target
Do not create a parallel manager skill.
This should extend current truth sources:
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- runtime handoff / restart logic in `docs/system/workspace/scripts/runtime/freely`
- and the live observability surface in `freely live-status`

## Boundary
This is not about:
- fixing prompt wording
- changing user chat semantics
- adding a new fourth loop
- manually forcing manager output in develop
- replacing the current non-interactive tool model with TUI injection

This is about:
- ensuring delegated manager continuation has an auditable lifecycle:
  - generated
  - consumed into prompt
  - still pending / lost due to failure boundary
- preserving non-interactive autonomous operation
- keeping human role as out-of-band interruption only

## Questions To Settle
1. Should manager continuation consumption happen by:
   - graceful preemption of current manager AI round, or
   - next-cycle queueing after current round exits, or
   - a policy split depending on whether current round has already moved beyond notice/claim?
2. What exact artifact proves handoff consumption succeeded?
   - new prompt file referencing the delegated intake
   - new session-state field recording consumed intake ids
   - new live-status field recording pending vs consumed handoff ids
   - optional later supervision output
3. Should `live-status` expose a dedicated field for:
   - pending manager continuation handoff not yet consumed
   - manager continuation currently being consumed
4. Should `write_session_handoff` treat inline markdown backticks as shell-dangerous and avoid command substitution bugs during `fresh_with_handoff` generation?

## Expected Shape
CLI-first observability remains the main frontend. The minimum product shape is:
- runtime tracks manager continuation handoff generation and consumption explicitly
- `live-status` exposes that state
- `fresh_with_handoff` handoff writing is shell-safe
