# Brainstorm: codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance

## Source Boundary

- canonical source candidate: `docs/pre-brainstorms/20260406-0901--codex-reconnect-probe-fast-fail/candidates.md#c-20260406-0901-a`
- absorbed sibling: `docs/pre-brainstorms/20260406-0715--codex-live-auth-identity-and-probe-lock-boundary/candidates.md#c-20260406-0715-a`

## Framing

本 owner 只收敛 reconnect fast-fail 与 runtime network classification alignment，不重开以下边界：

- stale slot pointer / unsaved live auth identity reconciliation
- Codex slot bundle shape / provider cleanup
- standalone `ai-switch-cli` extraction timing

## Design Notes

1. Probe status vocabulary 继续保持窄口径，只新增 `network_failure`。
2. `network_failure` 表示“当前 live auth 暂时不可用”，不是 slot invalidation。
3. fast-fail 必须保留 artifact，避免只留下一个更快但不可诊断的空状态。
4. runtime log matcher 只扩充 vocabulary，不增加第二套 recovery state machine。

## Residual Risk

- 纯字符串匹配可能跟 upstream Codex 日志文案变化耦合。
- 如果上游 later 提供 machine-readable connectivity signal，应允许 future owner 收窄 matcher。
