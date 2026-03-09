# Cleanup Lifecycle

## Preconditions

- 清理前执行 `./bin/wt-status-all`，结果必须全 `CLEAN`
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
