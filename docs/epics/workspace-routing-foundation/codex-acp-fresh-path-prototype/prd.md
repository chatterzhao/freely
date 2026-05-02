# PRD: codex-acp-fresh-path-prototype

## Goal

把 `codex` 作为 Freely 的第一条真实 ACP adapter prototype target，验证 `adapter=acp` 是否能在不破坏现有 direct continuity contract 的前提下跑通最小 fresh path。

## Why Now

当前这条链已经具备：

- ACP boundary truth
- runtime adapter axis
- policy truth
- supported-adapter status surface

再继续停留在 adapter 抽象层，不会产生更高置信度。必须选一个真实工具落第一刀原型。

## Why Codex

1. current canonical tool
2. strongest direct implementation
3. no nested capability shape
4. ACP 生态里已有 Codex CLI adapter 现实

## Why Fresh-Path Only

Freely 当前对 `codex` 的 strongest value 在 explicit resume evidence。第一刀 prototype 若把 `resume` 也强塞进 ACP，会把“验证 ACP fresh path”与“重做 Codex continuity contract”混成一件事，风险过高。

因此第一刀只验证：

- `codex + adapter=acp + fresh`
- `codex + adapter=acp + fresh_with_handoff`

`resume` 继续由 `direct` 承担 strongest contract，直到 ACP path 真正证明 parity。

## Product Surface

- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/monitor-ai-cli.sh`
- focused tests for `codex` adapter routing and launch-kind restrictions

## Non-Negotiables

- `direct` remains first-class for `codex`
- direct resume semantics must not regress
- ACP path must not silently fake resume parity
- no second continuity truth surface

## Contract Frame

本轮最小新增 contract：

1. per-tool support
   - `codex` supports `direct,acp`
2. per-adapter launch-kind contract
   - `direct`: existing launch kinds remain
   - `acp`: first round limited to `fresh` / `fresh_with_handoff`
3. runtime fallback rule
   - if `adapter=acp` and `launch_kind=resume`, runtime must fail fast or reroute intentionally
4. evidence contract
   - ACP path still writes into existing Freely launch/status/evidence surfaces

## Eval Plan

成功：

- `codex + adapter=acp` becomes a real launch path
- `codex + adapter=direct` keeps existing continuity strength
- prototype tells us whether ACP bridge work is worth continuing for current canonical tools

失败：

- ACP path only exists in config/status but not real launch code
- resume semantics are silently weakened
- ACP path forks continuity surfaces

## Execution Slices

1. metadata and policy restrictions
2. codex ACP launcher path
3. continuity-safe writeback and blocked resume semantics
4. focused regressions
5. one real-environment fresh-path sample
