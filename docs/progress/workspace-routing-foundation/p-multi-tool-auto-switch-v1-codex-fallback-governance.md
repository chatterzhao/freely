# Progress: multi-tool-auto-switch-v1-codex-fallback-governance

- issue_id: `I-20260331-1840-A`
- title: Multi-tool auto-switch v1 codex fallback governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`

## Current Slice

- 冻结 v1 runtime-owned fallback config：`AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS`
- 保持 same-tool automatic slot recovery 只由 Codex watchdog family 承担
- 允许 manager control plane 在 `kiro-cli` tool-local failure 后切到 `codex`
- cross-tool fallback 一律降级为 `fresh_with_handoff`

## Evidence

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- `docs/epics/workspace-routing-foundation/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`
- live repro on `develop`: `kiro-cli` exits with `kiro_monthly_request_limit`, then launcher persistence keeps control-plane watchdogs alive for post-exit fallback work instead of losing the runtime-owned recovery path at supervisor teardown

## Remaining

- merge absorption into `develop`
- post-merge live validation on protected manager runtime with local `kiro-cli` unavailable / `codex` available
