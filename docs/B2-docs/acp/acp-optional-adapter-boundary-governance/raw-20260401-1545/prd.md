# PRD: acp-optional-adapter-boundary-governance

## Goal

把 ACP 在 Freely 中的角色冻结为一个可执行的 adapter-boundary contract，使后续实现能在不破坏自治治理的前提下，为外部 code agents 提供 `direct` 与 `acp` 双轨接入能力。

## Why Now

Freely 的 runtime/governance 已经足够成熟，真正开始暴露出 adapter heterogeneity 的成本：

- 外部 tools 的 session/resume 能力不一致
- permission 和 update streaming 语义不一致
- launcher/profile glue 正在按工具复制
- 但 Freely 又不能为了统一接线层而牺牲 continuity、recovery 与工作流真源

如果 ACP 有价值，它应先以 narrow adapter boundary 的方式进入，而不是作为 runtime rewrite 的理由。

## Product Surface

- `docs/B1-docs/raw-20260401T224500Z/brainstorms.md`
- `docs/B1-docs/raw-20260401T224500Z/candidates.md`
- `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/raw-20260401-1545/issues/acp-optional-adapter-boundary-governance.md`
- `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/raw-20260401-1545/verification/pre-tests.md`
- `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/tasks.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`

## Non-Goals

- 直接实现某个工具的 ACP bridge
- 强制现有工具迁移到 ACP
- 用 ACP 替代 Freely 的 recovery / continuity / governance surfaces
- 在本轮解决 future risk-aware approval council

## Non-Negotiables

- `direct` 必须继续是 first-class path
- ACP 只能是 optional adapter layer
- 每个工具都必须允许独立 adapter 选择，而不是全局单开关
- experimental current implementation reality 不能冒充 canonical promised tool surface
- real-tool dual-path validation 是 future issue-level acceptance，不是本轮 candidate acceptance

## Context Pack

- 当前宪法已承诺工具面是 `codex`、`kiro-cli`、`iflow`
- `cc` / `cc-use-codex-cli` 属于当前仓库中的实验性实现 reality
- Freely 的长期记忆与恢复真相在 candidate / issue / progress / recovery / milestones，而不在单一 agent session
- ACP 最适合吸收 communication plane，不适合接管 control plane

## Canonical Contract Frame

Freely 未来的 tool integration contract 应至少分为两层：

1. `tool contract`
   - tool identity
   - capabilities
   - current resume strength / session semantics
   - whether it supports `direct`, `acp`, or both
2. `adapter contract`
   - session create/load/list
   - update streaming
   - tool call reporting
   - permission message transport
   - optional terminal/file callbacks

以下面不进入 adapter contract：

- continuity truth
- recovery truth
- branch/worktree lifecycle
- fresh-with-handoff
- context/token/rate-limit rotation
- manager/worker dispatch metadata

## Current Runtime Touchpoints

后续实现不能凭空添加一层 adapter 概念，而要从当前真源中拆出来：

1. `docs/system/workspace/tools.md`
   - 已经定义 tool inventory、resume strength、canonical vs weak continuity contract
   - future adapter policy 应从这里可见，但不能让它覆盖 runtime truth
2. `docs/system/workspace/scripts/runtime/tool-launchers.sh`
   - 当前 `tool_run_from_prompt_file()` 仍主要按 `tool` 分支
   - `codex`、`iflow`、`kiro-cli`、`cc`、`cc-use-codex-cli` 的 launch semantics 直接写死在这里
   - first implementation slice 应先把这里从 `tool-specific launcher` 收敛成 `tool contract + adapter contract`
3. `docs/system/workspace/scripts/runtime/freely`
   - 当前在 launch 前后写入 `tool_session_id`、`tool_resume_target`、`jsonl_path`、`cycle_log`、`context_ratio`、nested Codex MCP evidence
   - future ACP path 必须兼容这些 continuity writeback，不得旁路生成第二套真相

## Prototype Path

最小 prototype 不应该从“给某个工具硬接 ACP”开始，而应该按顺序推进：

1. 先从 runtime 中抽出 `adapter axis`
2. 再让一个 current-repo tool 能声明 `direct` 与 `acp`
3. 再增加至少一个新增工具的接入选择
4. 最后用真实工具做双路径 acceptance

当前代码层的最小触点应是：

1. 在 `tools.md` 为每工具引入 adapter policy 可见性
2. 在 `tool-launchers.sh` 把 launch decision 从“只看 tool”提升到“tool + adapter”
3. 在 `freely` 保持现有 session/evidence writeback，不因 ACP path 旁路 continuity surfaces

## Eval Plan

成功：

- IBM 真源统一承认双轨 adapter 架构
- follow-on implementation owner 不会再把 ACP 写成治理替代品
- follow-on implementation owner 能明确知道先抽 `adapter axis`
- future prototype acceptance 已经锁定真实工具双路径验证

失败：

- issue-bound truth 仍然把 ACP 写成主架构替代
- `direct` 被弱化成临时兼容层
- candidate 与 issue 的 acceptance 再次混层
- prototype 仍被描述成“直接对接一个 ACP bridge 就够了”

## Execution Slices

1. 冻结 `optional adapter layer` 边界
2. 冻结 `direct / acp / prefer_acp_fallback_direct`
3. 冻结 prototype preconditions
4. 冻结 current-repo vs speculative target pools
5. 生命周期回写与后续 implementation handoff

## Revisit Triggers

- 当某个 current-repo tool 已出现可信 ACP path
- 当新增工具的接入成本继续因 per-tool glue 上升
- 当 ACP schema 本身出现会影响 adapter boundary 的变化
- 当 Freely 后续实现出 risk-aware approval council，需要重新确认 approval transport 与 policy ownership 边界

## Dev-Loop Handoff

本 issue 的完成物是边界与验收控制面本身。真正的代码实现应另起 follow-on owner，先改 runtime adapter axis，再做 first-tool prototype。
