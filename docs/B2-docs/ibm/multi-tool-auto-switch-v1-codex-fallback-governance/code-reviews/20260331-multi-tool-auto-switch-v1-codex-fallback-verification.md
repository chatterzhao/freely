# Verification: multi-tool-availability-manager-governance

- issue_id: `I-20260331-1840-A`
- reviewer: `codex`
- verdict: `pass`

## Verified

1. `ensure-manager` 每轮开始都会重新 `load_config "$project"`，所以 control plane 消费的是最新 active tool 与 `AI_FALLBACK_TOOLS` truth，而不是旧进程缓存。
2. 当前工具若具备 canonical same-tool recovery truth，control plane 会先走同工具恢复；Codex 继续受既有 watchdog readiness / no-launch contract 约束，same-tool 穷尽前不会直接跨工具切换。
3. 当 same-tool recovery 已穷尽或出现允许 cross-tool recovery 的 tool-local failure，`ensure-manager` 会按 `AI_FALLBACK_TOOLS` 的顺序扫描可用工具，而不是把 `codex` 写死成唯一 target。
4. cross-tool fallback 不会把 current tool 隐式插回列表最前；same-tool recovery 已失败后，下一轮跨工具选择总是从 `AI_FALLBACK_TOOLS` 最左侧重新开始，只把 current tool 当作 active pointer / de-dup truth。
5. 当所有已配置工具都不可用时，manager launch 保持 blocked，并写出 `tool_auto_switch_waiting_for_recovery` 与 earliest-reset hint，而不是盲目 relaunch 或伪装健康。
6. 兼容性合同仍保持：
   - `kiro_monthly_request_limit` / `kiro_subscription_status_service_error` 在 `AUTO_SWITCH_TOOL=true` 时仍可通过 ordered fallback 选到 Codex
   - auto-switch 未开启时，Kiro availability failure 继续 stop/defer
   - fallback 目标若是 Codex，仍必须通过既有 no-account-ready guard
7. live follow-up surfaced a separate Kiro launch blocker inside the same owner: when `AI_MODEL` is empty, the launcher had still been defaulting to stale `claude-opus-4.6`, causing `ai_exit_rc_1` before availability classification. The runtime now falls back to Kiro `model=auto`, so live repro returns to canonical `kiro_monthly_request_limit` instead of looping on invalid-model failure.
8. live follow-up also surfaced a control-plane race: cleanup-time one-shot `ensure-manager` recheck could still see the exiting supervisor pid and return `manager supervisor already running`, so fallback selection never started. The runtime now waits for a `desired=running + down/down` teardown window to clear before entering cross-tool recovery.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
2. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
4. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
5. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
7. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
8. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
9. `bash docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
10. `./bin/governance-check`

## Residual Risk

1. 只有 Codex 目前具备成熟的 same-tool watchdog truth；`kiro-cli` / `iflow` / `cc` 参与 cross-tool fallback 时仍使用较弱 readiness contract，后续需要单独冻结各自 capability surface。
2. earliest-reset hint 当前主要来自 Codex availability state；其他工具若还没有结构化 reset truth，只能作为无 hint 的 unavailable target 参与排序。
3. 这份 review 仍缺一条 post-merge live confirmation，用 canonical `develop` 验证 current-tool slot-first、随后从左到右的 ordered fallback、teardown-aware recheck 与 all-tools-unavailable waiting truth 在真实 manager runtime 上都可见。

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
