# Issue: multi-tool-auto-switch-v1-codex-fallback-governance

- issue_id: `I-20260331-1840-A`
- title: Multi-tool auto-switch v1 codex fallback governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `multi-tool-auto-switch-v1-codex-fallback-governance`
- issue-name: `multi-tool-auto-switch-v1-codex-fallback-governance`
- source_candidate: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md#c-20260331-1840-a`
- source_brainstorm: `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 现在已经有两条不对称的真相：

- `codex` 已有 canonical slot sweep / no-launch watchdog contract
- `kiro-cli` 已能把月度限额与订阅校验失败分类成 tool-local availability failure

但当前 manager control plane 仍只认单一 `AI_TOOL`，所以 `kiro-cli` 故障后只会停下，不会在开启 auto-switch 时切到可用的 `codex`。v1 要补的是这条最窄、最安全的桥，而不是一口气做泛化的多工具编排。

## Scope

1. 冻结 runtime-owned fallback config：`AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS`。
2. 保持 `AI_TOOL` 仍是单一 active tool pointer；v1 不改成完整 tool-group state machine。
3. 保持 same-tool automatic slot recovery 只对已存在 canonical truth 的 `codex` 生效。
4. 让 `ensure-manager` 在以下条件下把 protected manager 项目从 `kiro-cli` 切到 `codex`：
   - 项目仍 `desired=running`
   - 当前没有活着的 manager supervisor / AI
   - `AUTO_SWITCH_TOOL=true`
   - 上次退出是 `kiro_monthly_request_limit` 或 `kiro_subscription_status_service_error`
   - Codex readiness 成功
5. 冻结 cross-tool continuity downgrade：v1 一律强制 `fresh_with_handoff`，不保留 resume 语义。

## Non-Goals

1. 不把 `tools.md` 的任务路由优先级直接复用成 runtime fallback order。
2. 不让 `cc`、`cc-use-codex-cli`、`iflow` 进入自动 fallback v1。
3. 不把 host/network-global failures 误当成 cross-tool fallback 触发器。
4. 不把 worker lane、多工具 generic slot family、或完整 tool-group persisted state 一起塞进本 owner。

## Acceptance

1. `write_config()` 为新项目写出 `AUTO_SWITCH_SLOT`、`AUTO_SWITCH_TOOL`、`AI_FALLBACK_TOOLS` 默认字段。
2. `ensure-manager` 每轮都重新读取项目 config，因此 control plane 可以消费最新 active tool truth。
3. 当 manager 项目上次因 `kiro_monthly_request_limit` 或 `kiro_subscription_status_service_error` 退出，且 `AUTO_SWITCH_TOOL=true` 时，`ensure-manager` 会把 config 中的 active tool 切到 `codex`，再走既有 Codex readiness gate。
4. 上述 fallback 会写出 machine-readable runtime event，包含 `previous_tool`、`active_tool`、`reason` 与 `launch_kind=fresh_with_handoff`。
5. 现有 Kiro defer contract 不回退：当 auto-switch 未开启时，runtime 仍在本地 stop 并 defer 给 control plane。
6. 现有 Codex no-account-ready guard 不回退：Codex readiness 失败时，`ensure-manager` 仍跳过 launch。
7. manager supervisor 在 `desired=running` 下退出后，必须重新触发一次 control-plane recheck；不能把 `kiro_monthly_request_limit` 留在已写入 state 但无人消费的中间态。

## Completion

- `docs/pre-brainstorms/20260331-1840--multi-tool-group-auto-switch-governance/candidates.md`
- `docs/milestones.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
- `docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
- `docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- live validation on `develop` with local `kiro-cli` unavailable and `AUTO_SWITCH_TOOL=true`

## Verification

- Focused regressions:
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-kiro-to-codex-fallback`
  - `bash docs/system/workspace/scripts/tests/test-freely-kiro-availability-failures-defer-to-control-plane`
  - `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-skips-launch-when-no-account-ready`
- Governance:
  - `./bin/governance-check`
- Live repro:
  - Start on `develop`, confirm `kiro_monthly_request_limit`, then verify the manager watchdog survives supervisor exit long enough to rewrite `AI_TOOL=codex` and emit `tool_auto_switch_selected`

## Next

- 若 v1 合并后继续验证稳定，再决定是否把 `AI_FALLBACK_TOOLS` 扩到 `cc` / `iflow` 或完整 tool-group persisted state。
- 若要支持跨工具保留 resume 语义，必须先新开 lifecycle 冻结 continuity equivalence contract；本 owner 不预支这条能力。
