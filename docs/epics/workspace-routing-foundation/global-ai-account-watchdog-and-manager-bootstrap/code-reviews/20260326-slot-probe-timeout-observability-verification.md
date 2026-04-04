# Code Review: global-ai-account-watchdog-and-manager-bootstrap
- issue_id: `I-20260318-1630`

- date: `2026-03-26`
- reviewer: `codex`
- branch: `feature/watchdog-switch-stability-and-probe-freeze-20260326`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260326-feature-watchdog-switch-stability-and-probe-freeze`
- scope: `slot probe timeout observability`

## Findings

1. `codex_probe_current_slot_now()` 之前在 timeout 时只返回 `timeout`，不会保留 partial output，导致现场无法区分网络/代理慢、CLI 卡住，还是 `402 deactivated_workspace` 已经返回但被 timeout 截断。当前已补 `.freely/run/codex-probe-artifacts/` artifact writeback。
2. timeout 分支中的 `wait "$pid"` 在 `set -e` 下会把整个 probe 函数打断。当前已改成 `wait "$pid" 2>/dev/null || true`，保证 timeout artifact 一定能落盘。

## Verification

- `bash -n docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `./bin/governance-check`

## Residual Risk

- `test-freely-ensure-manager` 在该旧 feature 工位上仍有既有漂移，当前没有证据表明由本次 timeout observability 改动引入；本轮未把它计入通过证据。
