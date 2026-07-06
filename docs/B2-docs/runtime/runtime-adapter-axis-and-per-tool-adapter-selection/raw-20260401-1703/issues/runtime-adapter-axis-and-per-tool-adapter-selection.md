# Issue: runtime-adapter-axis-and-per-tool-adapter-selection

- issue_id: `I-20260401-1703-A`
- title: Runtime adapter axis and per-tool adapter selection
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-adapter-axis-and-per-tool-adapter-selection`
- issue-name: `runtime-adapter-axis-and-per-tool-adapter-selection`
- priority: P1
- source_candidate: `docs/B1-docs/raw-20260401T224500Z/candidates.md#c-20260401-1703-a`
- source_brainstorm: `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/raw-20260401-1703/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/raw-20260401-1703/code-reviews
- depends_on:
  - `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/raw-20260401-1545issues/acp-optional-adapter-boundary-governance.md`
  - `docs/B2-docs/ibm/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
  - `docs/B2-docs/ibm/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

ACP boundary 已经收口，但 runtime 现在还没有 first-class `adapter axis`。

当前真实形态仍然是：

- config 主要以 `AI_TOOL` 为中心
- `tool-launchers.sh` 主要以 `tool -> launcher case` 分派
- `freely` 自己持有 continuity / status / launch metadata / session writeback

如果不先把 adapter selection 从 tool selection 中抽出来，后续无论要不要接 ACP，都会把 communication plane、tool-specific launch glue、continuity truth 一起拖进同一次改造。

因此这条 owner 的职责不是接 ACP，而是先把 runtime 切出一个安全的 adapter boundary。

## Scope

1. 在 runtime config 中引入 first-class adapter truth，例如 `AI_TOOL_ADAPTER`。
2. 在不实现 ACP bridge 的前提下，引入与当前 adapter 解耦的 policy truth，例如 `AI_TOOL_ADAPTER_POLICY`。
3. 明确 current tools 的默认 adapter policy 仍然是 `direct`。
4. 让 launch dispatch 先按 adapter 路由，再进入 tool-specific direct implementation。
5. 保持 continuity / recovery / session evidence writeback 继续走现有 canonical surfaces，不因 adapter extraction 旁路。
6. 让 status / introspection surface 能暴露当前 adapter、policy 与当前工具的 supported-adapter matrix。
7. 对未实现 adapter，例如 `acp`，提供 fail-fast contract，而不是静默回退。
8. 提供最小受管 mutation command，让 tool + adapter truth 不必依赖手改 config。

## Non-Goals

1. 不在本 issue 中实现 ACP bridge。
2. 不在本 issue 中完成 first-tool ACP prototype。
3. 不改变 current tool continuity 强弱分层。
4. 不把 `cc` / `cc-use-codex-cli` 的实验性 reality 升格成 promised surface。

## Acceptance

1. `freely` config truth 能显式持久化 `AI_TOOL_ADAPTER` 与 `AI_TOOL_ADAPTER_POLICY`，且当前工具默认 policy 保持 `direct`。
2. runtime launch path 先经过 adapter dispatch，再进入 direct implementation；不再只有裸 `tool -> launcher case`。
3. 当前 canonical tools 在 `adapter=direct` 下保持现有行为与 continuity writeback，不出现回归。
4. `freely status` 或等价 introspection surface 能显示当前 adapter truth、policy truth 与当前工具的 supported-adapter matrix。
5. 若配置到未实现 adapter，例如 `acp`，runtime 会给出显式 unsupported/blocked 信号，而不是静默回退为 `direct`。
6. `freely init --tool-adapter <adapter> [--tool-adapter-policy <policy>]` 与 `freely set-tool --tool <tool> [--tool-adapter <adapter>] [--tool-adapter-policy <policy>]` 能通过受管命令面持久化 adapter truth。
7. same-tool reselection 保留当前 adapter/policy truth；cross-tool selection 才回落到目标工具默认 policy，除非显式给出 adapter 或 policy override。
8. same-tool mutation 不会把当前 `AI_MODEL` / `AI_REASONING_EFFORT` 静默重置回工具默认值。
9. issue / PRD / pre-tests / tasks 对上述实现顺序与非目标口径一致，可直接进入 dev-loop。

## Ready For Dev

实现建议按四个 slice 推进：

1. config surface
   - 新增 `AI_TOOL_ADAPTER`
   - 新增 `AI_TOOL_ADAPTER_POLICY`
   - 写入 init/defaults/persist path
   - 暴露最小受管 mutation command
2. tool metadata surface
   - 为当前工具冻结 default adapter 与 supported adapter truth
3. runtime dispatch surface
   - 让 launch path 从 `tool -> launcher` 调整为 `adapter -> tool implementation`
4. status / tests
   - 暴露 adapter truth
   - 锁住 direct no-regression 和 unsupported-adapter fail-fast

## Implementation References

- `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/raw-20260401-1545issues/acp-optional-adapter-boundary-governance.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/prd.md`
- `docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/pre-tests.md`
- `docs/B2-docs/runtime/runtime-adapter-axis-and-per-tool-adapter-selection/tasks.md`

## Verification

- `./bin/governance-check`
- focused runtime tests for config persistence, adapter-aware dispatch, and unsupported-adapter fail-fast
- review that current direct path evidence surfaces remain canonical

## Next

- `2026-04-01 21:26 PDT` completion: `develop` merge `a0f9a48` absorbed the runtime adapter axis, so `AI_TOOL_ADAPTER` / `AI_TOOL_ADAPTER_POLICY`, adapter-aware dispatch, managed mutation, and per-tool support truth are now canonical develop behavior.
- `I-20260401-1545-A-01` consumed this contract to land the first real `codex + adapter=acp` fresh-path prototype without weakening direct-path resume truth.
- Re-open only if future adapter work requires a broader runtime redesign beyond the now-canonical adapter axis surface.
