# Code Review: oauth-slot-inventory-sweep-and-launch-time-confirmation-governance
- issue_id: `I-20260327-1115`

- verdict: pass
- date: `2026-03-27`

## Why

这条 follow-on issue 的完成条件不是“有一个 OAuth 预研分支”，而是把 inventory truth、cooldown ledger、status surface 与 manager launch-time confirmation 都收束到同一套运行时真源，并证明它们已经能替代旧的全量串行真实 probe 主路径。

## Checks

- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager`
- `bash docs/system/workspace/scripts/tests/test-freely-rate-limit-defers-to-watchdog`
- `bash docs/system/workspace/scripts/tests/test-ai-cli-switch-default-tool`
- `./bin/governance-check`

## Findings

1. `availability-watchdog.sh` 现在提供统一的 OAuth inventory truth 入口，支持 cache freshness、full sweep overwrite 与 launch-time confirmation，而不是让 `switch auto`、`status`、`ensure-manager` 各写一套 slot 判定。
2. `freely ai status` 在 cache 缺失或过期时会优先刷新 OAuth inventory，不再要求全量真实 probe 才能看到 inventory 概览。
3. `ensure-manager` 会先消费 OAuth inventory 结果，再只对最终 candidate slot 做真实确认；`deactivated_workspace` 与 `rate_limited` 不会被误当作可直接切换目标。
4. focused regressions 覆盖了“不改活跃 auth”“cooldown overwrite”“status stale refresh”“watchdog sweep -> launch-time confirmation”四条新 contract，当前均通过。

## Conclusion

OAuth slot inventory sweep and launch-time confirmation governance 已达到 merge-ready。完成 closeout 只剩 canonical develop merge 与 worktree retirement，不再存在实现层 blocker。
