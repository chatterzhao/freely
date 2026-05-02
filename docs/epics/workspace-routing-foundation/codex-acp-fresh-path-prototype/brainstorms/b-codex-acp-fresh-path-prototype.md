# Brainstorm: codex-acp-fresh-path-prototype

## Why Codex First

1. `codex` 属于当前宪法已承诺工具面，不是实验性 reality。
2. Freely 已经在 `codex` 上拥有最成熟的 direct path、resume evidence、context rotation 与 dogfooding 覆盖。
3. ACP 官方 agents / registry 当前明确列出了 Codex CLI 的 ACP adapter，因此它不是纯假设 target。
4. `codex` 没有 `cc-use-codex-cli` 那种 nested capability 复杂度，更适合第一刀收窄原型。

## Why Fresh-Path First

1. Freely 当前对 `codex` 的 strongest contract 是 explicit session-addressed resume。
2. 第一刀 ACP prototype 不应为了“走通 ACP”而削弱或伪造这条 resume contract。
3. 因此第一刀应限定为：
   - `codex + adapter=acp`
   - 先做 `fresh` / `fresh_with_handoff`
   - 不在首轮承诺 ACP path 的 resume parity
4. 若 ACP path 缺少 explicit resume target，runtime 必须继续：
   - 用 direct path 承担 strongest resume contract，或
   - 对 `resume` 显式 blocked / reroute，而不是 silently pretending parity

## Prototype Boundary

- 目标不是替代 `codex` 的 direct path
- 目标不是一开始就覆盖 `resume`
- 目标是验证：
  - Freely 能否在 `codex` 上真正落一条 `adapter=acp` 可运行 fresh path
  - continuity / status / evidence surfaces 是否继续统一
  - future per-tool ACP rollout 是否值得继续

## Prototype Success Signal

1. `codex` 能在同一 runtime 中同时支持：
   - `adapter=direct`
   - `adapter=acp`
2. 两条路径都走同一套 Freely config / status / lifecycle truth。
3. ACP path 在真实环境下至少能完成最小 fresh task。
4. direct path 的 explicit resume contract 不被回归。
