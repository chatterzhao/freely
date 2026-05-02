# Pre-Tests - runtime-worker-launch-linkage-and-stall-recovery-governance

## Pre-merge acceptance

1. Manager handoff -> worker launch linkage
- setup:
  - 在 manager continuity 中提供至少一个稳定的 worker prompt path 与 target worktree
  - target worker worktree 初始 `DESIRED_RUNTIME_STATE=stopped`
- expect:
  - runtime 将 handoff 转成 target worker intake / expected-running state
  - manager watchdog 或 runtime 能拉起该 worker supervisor

2. Stalled AI recovery
- setup:
  - 当前 workcell 有活跃 ai pid
  - 当前 cycle log 超过阈值不更新
  - 新 delegated continuation 或 intake 已进入
- expect:
  - runtime 触发 graceful recovery
  - 必要时记录 hard-kill fallback
  - 下一轮 prompt 能消费该新 handoff

## Post-merge acceptance

1. 在 `develop` 上真实用 `freely chat` 再次要求 manager 巡检剩余 worktree
- expect:
  - 若 manager continuity 已给出 stable worker launch order，则 Freely 不只写 prompt 文件，而会真正把目标 worker 拉起或明确写出 runtime blocker
