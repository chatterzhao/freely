# PRD: runtime-adapter-axis-and-per-tool-adapter-selection

## Goal

在不引入 ACP bridge 的前提下，把 Freely runtime 当前的 tool-specific launch glue 收敛成 first-class adapter-aware dispatch，为后续 `direct / acp / prefer_acp_fallback_direct` 双轨接入打下实现基础。

## Why Now

当前 runtime 已经具备：

- per-tool session continuity
- slot-first recovery
- status / evidence writeback
- tool capabilities / tool policy config surface

但 adapter 仍然没有成为独立维度。这意味着：

- 当前只能表达“选哪个 tool”
- 还不能安全表达“同一个 tool 用哪个 adapter”

ACP issue 已经明确这一步必须先做，因此这里的产品目标是 extraction，不是 bridge。

## Product Surface

- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/*adapter*`
- `docs/system/workspace/scripts/tests/*launch*`

## Non-Goals

- ACP transport implementation
- first-tool ACP prototype
- new external tool onboarding
- rewrite of continuity / recovery truth

## Non-Negotiables

- default path remains `direct`
- unsupported adapter must fail fast
- current direct path behavior must remain stable
- adapter extraction must not create a second continuity or status truth surface

## Context Pack

- `AI_TOOL_CAPABILITIES` / `AI_TOOL_POLICY` already exist in config and status surfaces
- current launch flow still passes through `tool_run_from_prompt_file`
- `freely status` already exposes tool-specific config and session/evidence state
- current tools have unequal continuity strength, and this issue must preserve that explicitness

## Canonical Contract Frame

最小新增 contract 应至少包含：

1. config truth
   - `AI_TOOL_ADAPTER_POLICY`
   - `AI_TOOL_ADAPTER`
   - 受管 mutation entrypoint，可更新 `tool + adapter/policy` selection
2. tool metadata truth
   - default adapter
   - supported adapters
3. dispatch truth
   - adapter route first
   - tool implementation second
4. status truth
   - current adapter, desired policy, and current supported-adapter matrix visible

本轮不新增 canonical truth：

- ACP session schema
- adapter-specific continuity state
- adapter-specific recovery truth

## Prototype Path

最小实现顺序：

1. 在 config 与 status 中引入 `AI_TOOL_ADAPTER_POLICY` 与 `AI_TOOL_ADAPTER`
2. 在 tool metadata 中冻结 current tools 的 default/supported adapters
3. 将 launch dispatch 改为 adapter-aware
4. 先只实现 `direct`
5. 对 `acp` 明确 unsupported contract

## Eval Plan

成功：

- runtime 已能明确知道当前是哪个 adapter
- runtime 已能明确区分“期望 policy”和“当前解析出的 adapter”
- direct path 保持不回归
- current tools 不需要立即迁移
- follow-on ACP owner 不必再重构 tool selection 本身
- 受管命令面已能更新 tool + adapter/policy truth，而不是要求手改 config
- same-tool mutation 不会把当前 tool-local model/reasoning truth 静默重置回默认值

失败：

- `AI_TOOL_ADAPTER` 只停留在配置，不影响实际 dispatch
- unsupported adapter 被静默回退到 `direct`
- continuity / status writeback 被分叉成两套
- 本轮又偷偷开始做 first-tool ACP bridge

## Execution Slices

1. config defaults, persistence, and managed mutation
2. tool metadata helpers
3. adapter-aware launch dispatch
4. status / introspection updates
5. focused regression tests

## Revisit Triggers

- 当 first-tool ACP prototype owner 启动
- 当新增工具需要非 direct 的 adapter path
- 当 current tools 需要把 `prefer_acp_fallback_direct` 接到真实 supported-adapter matrix

## Dev-Loop Handoff

这条 owner 应直接进入 runtime implementation。第一批改动优先集中在 `freely`、`tool-launchers.sh` 和 `tools.md`，不要先碰 ACP bridge。
