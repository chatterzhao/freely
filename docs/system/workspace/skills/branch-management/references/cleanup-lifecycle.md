# Cleanup Lifecycle

## Preconditions

- 清理前确认 target worktree 自身安全：
  - merged
  - inactive
  - target clean
- 若存在 unrelated dirty 或 busy worktree，不作为全局阻断；必须在 cleanup evidence 中显式记录为 retained / skipped
- 合并后不要立即删除分支/worktree

## State progression

- `active`
- `merged-pending-verify`
- `verified-retirable`
- `retired`

## Retire only when

- 合并完成
- 测试和语义回归为绿色
- 无待处理回滚项

## Required evidence

- 清理的分支名与 worktree 路径
- 本地/远程删除结果
- 若保留分支，记录原因与预计清理时机
