# Cleanup Lifecycle

## Preconditions

- 清理前确认 target worktree 自身安全：
  - merged
  - inactive
  - target clean
- `issue phase_state=completed` 只表示业务实现/验收已收口；若 cleanup / continuity / verification write-back 仍停留在该 feature worktree 的 dirty 改动中，则这条 branch lifecycle 仍未完成
- 若存在 unrelated dirty 或 busy worktree，不作为全局阻断；必须在 cleanup evidence 中显式记录为 retained / skipped
- 合并后不要立即删除分支/worktree
- 对 `pre-test-merge` 而言，`stale` 是“该批次不再权威”的治理信号，不是可长期保留的 active state；若同一能力仍要继续验证，先 retire 当前批次，再用来源 feature replay 出新的验证批次。

## State progression

- `active`
- `merged-pending-verify`
- `verified-retirable`
- `retired`

## Retire only when

- 合并完成
- 测试和语义回归为绿色
- 无待处理回滚项
- 若存在远程 branch，其 disposition 已明确：
  - merged and deleted
  - or retained with reason
- 对 `pre-test-merge` 的 retire / rebuild，cleanup evidence 还应记录 replay target，避免把 stale 批次误留成当前事实来源。

## Required evidence

- 清理的分支名与 worktree 路径
- 本地/远程删除结果
- 若保留分支，记录原因与预计清理时机

## Remote branch check

1. 若仓库没有配置 remote，可只做本地 cleanup，并在 evidence 中写明 `remote: not-configured`
2. 若存在 remote branch：
  - 先同步 remote refs
  - 确认远程分支是否已被当前 integration target 吸收
  - 已吸收：先删 remote，再删本地 worktree / branch
  - 未吸收或 remote delete 失败：保留本地并记录原因
