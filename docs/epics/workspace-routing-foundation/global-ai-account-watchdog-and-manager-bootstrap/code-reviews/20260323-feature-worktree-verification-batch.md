# Code Review: global-ai-account-watchdog-and-manager-bootstrap

## Result

- feature worktree verification passed

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-watchdog-control-plane-skills`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-earliest-reset-wait-revive`
- `./bin/governance-check`
- direct CLI verification:
  - `./bin/freely ensure-manager --project <tmp-project>`
  - `./bin/freely start --project <tmp-project>`

## What Changed

1. `freely ai switch codex` 继续使用主动 probe 结果决定切到可用账号，或在全部限流时切到最早恢复账号。
2. availability watchdog 扩展了 probe 结果分类与时间解析，覆盖 time-only `try again at 1:42 AM`、subscription / unauthorized / timeout / generic error。
3. 自动切号命令输出改成更直接的 operator-facing switched status，同时保留 JSON 路径给脚本消费。
4. 直接 `freely` 命令验证确认：
   - `ensure-manager` 仍由 watchdog 先恢复账号，再 bootstrap manager
   - `start` 仍会把 rate-limit 理由写入 session state，交给 watchdog / manager control plane 接管
5. earliest-reset wait continuation 现在补上了 runtime 常驻性与 wakeup 契约：
   - wait 采用 `reset_at + buffer`
   - wait 期间会周期性真实 probe saved accounts，任一账号变得可工作即可提前醒来
   - wait 结束后会重新 probe/select，再决定 relaunch manager
   - watchdog 不会因为单轮 readiness pass 失败而退出，也会覆盖 stale `ensure-manager.pid`

## Notes

- 本批次是单个 dedicated feature worktree 上的 verification，不需要为了测试引入 `pre-test-merge`。
- 当前 gate 是 feature worktree 内的 verification 与 writeback；`post-merge acceptance` 只在真正并入 `develop` 后才成立。
- `test-freely-rate-limit-defers-to-watchdog` 首次运行曾出现一次 3 秒边界失败；随后单独复现与连续重跑通过，当前判断为时间阈值边界上的 flaky，而不是稳定回归。

## Remaining Acceptance

- 暂存并提交当前 verification batch。
- 若决定 promote，再按 `develop` gate 判断是否需要 merge 后验收。
