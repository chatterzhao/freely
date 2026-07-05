# 预研：dirty worktree governance redesign

## Context

- 触发：Freely 已经进入多 worktree、多 AI 进程、subagent 并行工作的形态。
- 现象：`./bin/wt-status-all` 只要出现任一 `DIRTY`，当前 runtime 的 `cleanup-followthrough` 就直接整体报 `fleet_not_clean`，连安全可删的 merged worktree 也一并保留。
- 本轮 dogfooding 里，用户明确提出：脏的那个暂时不管，因为它正在工作；重点应是理解 dirty gate 原本预防什么，以及在多工位并行时如何重新设计。

## Problem

过去把 `dirty fleet` 当成全局阻断，主要是在防三件事：

1. 误清理仍在工作的工位
2. 把 unrelated dirty 改动带进 merge / promote / release
3. 在项目级看错 ownership，把正在工作的脏树误当作可收口对象

但现在这条规则的粒度太粗：

- `merge / promote / release` 的确需要强门禁
- `audit / merge-prep / retirement-handoff` 本质上是分析，不应被 unrelated dirty 全局阻断
- `cleanup-followthrough` 若只是删除已 merged、inactive、target clean 的工位，也不该因为另一个 worktree 正在工作就整体停摆

## Design Shift

不再把 dirty 只建模成一个二元的 `fleet_clean=true/false`。

应拆成三个独立判断面：

1. `target_clean`
- 当前要 merge / retire / cleanup 的目标树自己是否干净

2. `fleet_busy`
- 其他 worktree 是否有 active runtime、明确 ownership、checkpoint 中工作

3. `fleet_dirty_unrelated`
- 其他 worktree 是否 dirty，但与当前要处理的目标无关

## Revised Rules

### 仍维持强阻断的动作

- merge into protected branch
- promotion / completion 宣告
- release / tag / hotfix
- 删除 target 本身不安全的 branch/worktree

这些动作仍要求强安全边界，不建议引入通用 `allow-dirty`。

### 应允许 finer-grained handling 的动作

- `audit`
- `merge_prep`
- `retirement_handoff`
- 项目级监督 / status / routing
- `cleanup-followthrough`

这类动作应：

- 如实报告 busy / dirty
- 跳过不安全对象
- 继续处理安全对象

而不是被 unrelated dirty 全局阻断。

## Bypass Shape

如果后续要增加显式命令开关，方向应是细粒度而非总开关：

- `--allow-dirty-unrelated`
- `--skip-busy-worktree`
- `--scope <target-worktree|branch>`

不建议：

- 对 merge / release 生效的通用 `--allow-dirty`

## Current Increment

本轮先落最小修复：

- `cleanup-followthrough` 不再因为 unrelated dirty tree 直接 `fleet_not_clean`
- 它只跳过真正不安全的 target：
  - dirty
  - runtime-active
  - remove-failed

更广的治理重写，再从这一条 pre-brainstorm 继续 materialize。
