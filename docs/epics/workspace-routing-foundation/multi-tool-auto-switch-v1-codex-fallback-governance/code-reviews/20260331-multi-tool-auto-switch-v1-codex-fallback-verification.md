# Verification: multi-tool-auto-switch-v1-codex-fallback-governance

- issue: `I-20260331-1840-A`
- reviewer: `codex`
- verdict: `pass`

## Verified

1. `ensure-manager` 现在会在每轮开始时重新 `load_config "$project"`，不再把旧的 active tool 缓存在 watchdog 进程里。
2. 当项目配置启用 `AUTO_SWITCH_TOOL=true`、上次退出理由是 `kiro_monthly_request_limit` 时，control plane 会把 active tool 从 `kiro-cli` 改为 `codex`，记录 `tool_auto_switch_selected` event，并继续经过既有 Codex readiness gate 后再 launch manager。
3. 旧合同仍保持：
   - Kiro availability failure 在未启用 auto-switch 时继续 stop/defer
   - Codex readiness 失败时继续 no-launch

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
2. `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
3. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`

## Residual Risk

1. v1 仍只允许 `codex` 作为 automatic cross-tool fallback target；`cc` / `iflow` / generic tool groups 继续留在后续 lifecycle。
2. cross-tool fallback 当前只通过 runtime event 固化 `previous_tool` / `active_tool`；更完整的 persisted tool-switch handoff 仍可在 follow-on 中加强。
