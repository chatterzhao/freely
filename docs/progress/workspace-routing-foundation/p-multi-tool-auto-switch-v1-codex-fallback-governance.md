# Progress: multi-tool-availability-manager-governance

- issue_id: `I-20260331-1840-A`
- title: Multi-tool availability manager governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`

## Current Slice

- 冻结 runtime-owned availability config：`AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS`
- 保持 Codex same-tool recovery truth，并把它提升成通用 availability manager 的 first-hop invariant
- 让 manager control plane 按配置顺序扫描 fallback tools，而不是硬编码 `kiro-cli -> codex`
- cross-tool fallback 一律降级为 `fresh_with_handoff`，并在 all-tools-unavailable 时保留 earliest-reset waiting truth

## Evidence

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- `docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
- `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`
- live repro on `develop`: `kiro-cli` exits with `kiro_monthly_request_limit`, then supervisor cleanup re-triggers one-shot manager control-plane evaluation so the persisted `desired=running + tool-local failure` state is consumed even if long-lived watchers drift

## Remaining

- merge absorption into `develop`
- one clean post-merge live confirmation on canonical runtime with ordered fallback and explicit all-tools-unavailable truth
