# 预研：remote branch retirement governance

## Context

- 日期：2026-03-21
- 触发：本轮 worktree fleet 已完成本地 worktree / 本地分支收口，但在最终 promote 后仍需额外判断远程 feature 分支是否应删除。
- 当前仓库的规则已经要求 cleanup 结果包含远程删除留痕，但现有 runtime `cleanup-followthrough` 只处理本地 worktree 和本地 branch。

## Problem

当前存在一个治理不闭环：

1. 本地 worktree 可以清理干净
2. `develop` 可以已吸收对应 feature
3. 但远程仍可能残留同名 branch

这会导致：

- worktree 治理从本地看似结束，但远程协作面仍未退休
- 主管在下一轮 fleet 巡检时，仍会看到“好像还有活跃 feature”
- cleanup evidence 不能完整回答 `local deleted / remote deleted / retained with reason`

## Constraints

- 不应新造平行 skill；应扩展既有：
  - `skill:worktree-maintenance-governance`
  - `skill:branch-management`
- 远程分支不能一刀切删除：
  - 已完全被 `develop` 吸收：删除
  - 仍有独立未合并提交：保留并写明原因
  - 远程不可达/删除失败：保留并写明 blocker
- 本轮能力应先落在 cleanup runtime 和治理文档，而不是先做复杂 UI/控制面。

## Proposed Direction

1. 在 `worktree-maintenance-governance` 中，把 remote branch disposition 纳入 retirement / fleet closure 的必查面。
2. 在 `branch-management` 的 cleanup lifecycle 中，把：
   - remote exists check
   - remote merged check
   - remote delete result / retained reason
   写成明确步骤。
3. 在 `freely` 的 `cleanup-followthrough` 中补远程分支处理：
   - remote not configured -> 允许只做本地 cleanup
   - remote branch absent -> 允许本地 cleanup
   - remote branch present and merged -> 删除 remote，再删除本地
   - remote branch present but not merged / delete failed -> 保留本地并写明原因
4. 增加脚本级回归，锁定：
   - 远程分支被删除
   - dirty worktree 仍保留
   - resolution.md 能看出 remote disposition

## Expected Result

- Freely 的 worktree 收口不再只清本地，而能明确完成远程 retirement check。
- 主管以后做 worktree 治理时，`cleanup complete` 的语义变成：
  - local worktree deleted
  - local branch deleted
  - remote branch deleted，或 retained with reason
- 若远程未闭环，主管会继续看到它，而不是被“本地已删”误导。
