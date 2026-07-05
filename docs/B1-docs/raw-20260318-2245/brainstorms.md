# Brainstorms

## Problem

- `freely baseline-status --project <worktree>` 目前会优先读取该 worktree 自己 `.freely/run/supervisor.pid`。
- 如果该 pid 文件是旧值，但对应 pid 还活着且实际属于另一个 worktree，状态就会把别人工位的 supervisor 错认成当前工位。
- 这会直接破坏多 worktree supervision 的可信度，主管层会误判某个工位仍在自治执行。

## Constraints

- 必须保持 CLI first。
- 不能只依赖 pid 文件存在。
- 不能为了状态查询去修改进程或写入运行态。

## Candidate Direction

- `status` / `fleet-status` / `stop` 统一增加 pid 归属校验：
  - pid 是否仍存活
  - `ps` 命令行是否包含当前 `--project <abs_path>`
- 只有两项都成立，才把 pid 视为当前 worktree 的真实 supervisor。
- 若 pid 文件失真，应在展示层降级为 `none`，并允许 `discover_supervisor_pid` 继续走命令行发现。

## Expected Outcome

- 单工位 `freely baseline-status` 不再错误显示其他 worktree 的 supervisor pid。
- 项目级 `fleet-status` 不再把 stale pid 当成活跃 supervisor。
- `stop --project` 不会误杀另一个 worktree 的 supervisor。
