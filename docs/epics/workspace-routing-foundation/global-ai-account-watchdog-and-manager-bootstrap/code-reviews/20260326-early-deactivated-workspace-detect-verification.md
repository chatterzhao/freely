# Code Review: early-deactivated-workspace-detect verification

- issue_id: `I-20260318-1630`
- branch: `feature/watchdog-probe-early-deactivated-workspace-detect-20260326`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260326-feature-watchdog-probe-early-deactivated-workspace-detect`
- status: `pass`

## What changed

- `codex_probe_current_slot_now()` 不再把“timeout 窗口内已经明确出现的 `402/deactivated_workspace`”继续拖成 generic timeout。
- probe 轮询期一旦看到 `402 Payment Required` 或 `deactivated_workspace`，会立即：
  - 杀掉 probe 进程
  - 落 `.freely/run/codex-probe-artifacts/*-deactivated-workspace.log`
  - 返回 `deactivated_workspace`
- timeout 分支仍保留原有 partial-output artifact，用于纯 timeout/黑盒卡住场景。

## Why this matters

- live artifact 已证明当前不少 “timeout” 其实在 15 秒内早就拿到了 `deactivated_workspace`，只是被 Codex CLI 的 websocket/https fallback 重试拖到了 timeout。
- 若不提前收敛，slot sweep 会对已知坏 slot 额外浪费一整个 timeout 周期，放大切换抖动。

## Verification

- `bash -n docs/system/workspace/skills/watchdog-control-plane/scripts/availability-watchdog.sh`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-timeout-artifact`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-detects-deactivated-workspace-before-timeout`
- `bash docs/system/workspace/scripts/tests/test-freely-codex-probe-defers-during-account-switch`
- `bash docs/system/workspace/scripts/tests/test-freely-ai-account-switch`
- `./bin/governance-check`

## Residual risk

- 当前修复只把 `deactivated_workspace/402` 从 generic timeout 中剥离出来；还没有进一步细分其他 timeout 根因，例如纯网络慢、代理慢或 CLI 本体卡死。
