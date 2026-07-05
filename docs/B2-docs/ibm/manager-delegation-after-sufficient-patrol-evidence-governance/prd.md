# PRD: manager-delegation-after-sufficient-patrol-evidence-governance

## Problem

Freely 当前的主管已经可以完成高质量 patrol，但还缺少一个明确的 delegation threshold。结果是主管可能在 evidence 已足够时仍然继续只读巡检，而不进入 worker execution。

## Goal

让主管在 evidence sufficient 时，稳定地从 patrol 切换到具体 worker delegation。

## Non-goals

- 不实现新的 runtime watchdog 机制
- 不新增平行 skill
- 不解决所有 worker launch 细节

## Required Outcome

1. `manager-agent` 定义 patrol completion gate。
2. `auto-loop-orchestrator` 定义 patrol 完成后必须进入 concrete execution routing。
3. `multi-worktree-supervision` 定义 stable disposition 的标准下一跳。

## Eval Plan

- Truth-source review:
  - 主管职责是否明确包含“证据充分后必须 delegate”
  - 是否明确禁止无 blocker 时继续 manager-only patrol
- Dogfood acceptance:
  - 本次真实 `freely chat` 巡检案例作为 acceptance evidence，说明为什么这条规则是必要的
