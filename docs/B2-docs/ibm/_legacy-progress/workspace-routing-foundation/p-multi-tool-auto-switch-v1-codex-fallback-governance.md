# Progress: multi-tool-availability-manager-governance

- issue_id: `I-20260331-1840-A`
- title: Multi-tool availability manager governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`

## Current Slice

- 冻结 runtime-owned availability config：`AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS`
- 保持 Codex same-tool recovery truth，并把它提升成通用 availability manager 的 first-hop invariant
- 让 manager control plane 按配置顺序扫描 fallback tools，而不是硬编码 `kiro-cli -> codex`
- cross-tool fallback 一旦开始，总是从 `AI_FALLBACK_TOOLS` 最左侧重新扫描；`AI_TOOL` / `LAST_ACTIVE_SLOT` 继续只承担 current tool/current slot 真相
- cross-tool fallback 一律降级为 `fresh_with_handoff`，并在 all-tools-unavailable 时保留 earliest-reset waiting truth
- 把 cleanup-time one-shot recheck 变成 teardown-aware：state 已写成 down/down 时，先等旧 supervisor 真的退出，再做 fallback / relaunch

## Evidence

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-waits-for-supervisor-teardown-before-fallback`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-cross-tool-restarts-from-leftmost-priority`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- `docs/system/workspace/scripts/tests/test-tool-launchers-kiro-default-model`
- `docs/B2-docs/ibm/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`
- live repro on `develop` surfaced a narrow race: cleanup could write `desired=running + down/down + kiro_monthly_request_limit`, but an immediate one-shot recheck could still see the exiting supervisor pid and bail out as `already running`; this slice now adds teardown-aware waiting before fallback selection

- closure_status: `merged-and-verified`
- closure_evidence:
  - `merge_commits: 7252ed8, f5addf3, 795fe8d, 12a56bc`
  - `tests: bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-priority-list-fallback && bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-codex-slot-first-then-cross-tool && bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-all-tools-unavailable-earliest-reset`
  - `review: docs/B2-docs/ibm/multi-tool-auto-switch-v1-codex-fallback-governance/code-reviews/20260331-multi-tool-auto-switch-v1-codex-fallback-verification.md`
  - `live_validation: canonical develop runtime confirmed ordered fallback selection and teardown-aware recovery`
