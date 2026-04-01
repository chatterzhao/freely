# Pre-Tests: multi-tool-auto-switch-v1-codex-fallback-governance

## Acceptance Contract

1. 新项目 config 默认写出 `AUTO_SWITCH_SLOT=false`、`AUTO_SWITCH_TOOL=false`、`AI_FALLBACK_TOOLS=""`，并保持 `AI_TOOL` 仍是单一 active tool pointer。
2. `ensure-manager` 会重新读取 project config，不依赖旧进程启动时缓存的 `AI_TOOL`。
3. 当 manager 项目上次退出原因是 `kiro_monthly_request_limit` 或 `kiro_subscription_status_service_error`，且 `AUTO_SWITCH_TOOL=true` 时，control plane 会把 active tool 切到 `codex`，再执行既有 Codex readiness gate。
4. 这次跨工具 fallback 必须显式记录 `launch_kind=fresh_with_handoff`，不得冒充 resume。
5. 若 Codex readiness 失败，`ensure-manager` 仍保持 no-launch；不得因为切换到 fallback tool 就跳过 readiness guard。
6. 当 auto-switch 未开启时，Kiro availability failure 仍应保持“本地 stop + defer control plane”的旧 contract。

## Focused Tests

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
   - 锁住 `kiro-cli tool-local failure -> config active tool switches to codex -> codex readiness -> manager launch`
   - 同时要求 event log 写出 `previous_tool`、`active_tool`、`reason`
2. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
   - 锁住 auto-switch 未开启时，Kiro availability failure 仍只 stop/defer，不在本地 blind relaunch
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
   - 锁住 fallback 目标仍受 Codex no-account-ready guard 约束

## Regression Risks

1. `ensure-manager` 如果不 reload config，watchdog 进程会继续持有旧的 `AI_TOOL=kiro-cli`，导致 config 改了也不生效。
2. 如果把 `tools.md` 优先级直接当成 fallback order，routing truth 与 runtime availability truth 会再次混淆。
3. 如果 cross-tool fallback 没有强制 `fresh_with_handoff`，会把不同 continuity class 的工具误当成可 resume 等价物。
