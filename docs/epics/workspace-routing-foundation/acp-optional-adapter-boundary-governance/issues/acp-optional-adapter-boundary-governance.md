# Issue: acp-optional-adapter-boundary-governance

- issue_id: `I-20260401-1545-A`
- title: ACP optional adapter boundary governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `acp-optional-adapter-boundary-governance`
- issue-name: `acp-optional-adapter-boundary-governance`
- priority: P1
- source_candidate: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/candidates.md#c-20260401-1545-a`
- source_brainstorm: `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/pre-tests.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/all-tools-unified-slot-contract-governance/issues/all-tools-unified-slot-contract-governance.md`
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
  - `docs/epics/control-surface-runtime-convergence/backend-service-contract-and-adapter-taxonomy/issues/backend-service-contract-and-adapter-taxonomy.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经形成了多工具 runtime、continuity、slot-first recovery、auto approval 与 external code agent orchestration，但外部 agent 的接入面仍主要依赖 per-tool launcher/profile。

ACP 预研现在已经有稳定边界：

- ACP 不替代 Freely 的三 loop、recovery、continuity 或治理真源
- ACP 只适合作为 optional adapter layer
- `direct` 必须继续保持 first-class path
- 每个工具都应能独立选择 `direct`、`acp` 或 `prefer_acp_fallback_direct`
- 真正的端到端双路径验证应落在后续 prototype owner，而不是继续停留在 pre-brainstorm

因此当前要做的不是再泛化讨论 ACP，而是把这套边界 materialize 成正式 issue 真源，直接指导下一阶段实现。

## Scope

1. 冻结 Freely 最小 adapter contract，明确哪些字段属于 adapter，哪些继续属于 Freely runtime/governance。
2. 冻结双轨 adapter 架构：
   - `adapter=direct`
   - `adapter=acp`
   - `adapter=prefer_acp_fallback_direct`
3. 明确 ACP 只吸收：
   - session lifecycle
   - update streaming
   - tool call reporting
   - permission message transport
   - optional terminal/file callback experiments
4. 明确以下面继续留在 Freely：
   - continuity / recovery truth
   - branch / worktree governance
   - fresh-with-handoff
   - context / token / rate-limit rotation
   - manager / worker dispatch
   - future risk-aware approval council
5. 冻结 future prototype 的 issue-level acceptance 形状：
   - 至少一个现有工具验证 `direct -> acp`
   - 至少一个新增工具验证 `direct` 或 `acp`
   - 两条路径继续写回同一套 continuity / recovery / lifecycle evidence
6. 明确 prototype 前置条件：runtime 必须先具备独立 `adapter axis`，不能继续只靠 `tool -> launcher case`。
7. 区分：
   - 当前宪法已承诺工具面
   - 当前仓库实验性实现 reality
   - future speculative tool pool

## Non-Goals

1. 不把 ACP 升格成 Freely 的治理平面。
2. 不要求现有工具批量迁移到 ACP。
3. 不在本 issue 中直接完成某个具体工具的 ACP bridge 或真实双路径验证。
4. 不把 `cc` / `cc-use-codex-cli` 的实验性当前实现写成宪法承诺工具面。

## Acceptance

1. issue / PRD / pre-tests / tasks / issue-bound brainstorm 之间对以下结论口径一致：
   - `ACP = optional adapter layer`
   - `direct = first-class path`
   - `per-tool adapter selection`
2. issue-bound truth 明确区分 ACP 可吸收的 communication concerns 与 Freely 必须保留的 governance concerns。
3. issue-bound truth 明确 prototype 前置条件包含独立 `adapter axis`。
4. issue-bound truth 明确 future prototype 的 issue-level acceptance，不再把真实工具双路径验证写回 candidate-level acceptance。
5. issue-bound truth 明确 current-repo candidate pool 与 future speculative tool pool 的不同角色，可直接指导 follow-on implementation owner。

## Ready For Dev

后续实现建议按四个 slice 推进：

1. 先从 runtime 中抽出独立 `adapter axis`
2. 再定义 ACP adapter contract 只覆盖 communication plane
3. 选择一个 current-repo tool 做第一刀 prototype
4. 用真实工具执行 issue-level dual-path acceptance

当前实现落点应优先围绕这三处真源展开：

- `docs/system/workspace/tools.md`
  - 继续定义 tool contract、resume strength、canonical promised surface 与 experimental reality
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
  - 当前仍是 `tool -> launcher case` 的主要承载面，是抽出 `adapter axis` 的第一落点
- `docs/system/workspace/scripts/runtime/freely`
  - 当前负责 launch metadata、resume target、cycle evidence、session writeback，与 future adapter selection 必须保持一致

第一刀 prototype 应优先选择：

- 单层 session
- resume 语义相对清晰
- 没有 nested capability
- 不会把 experimental tool reality 误当 canonical contract

## Implementation References

- `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/brainstorms.md`
- `docs/pre-brainstorms/20260401-1545--acp-client-agent-protocol-runtime-adoption/candidates.md`
- `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/brainstorms/b-acp-optional-adapter-boundary-governance.md`
- `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/prd.md`
- `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/tasks.md`
- `docs/system/workspace/tools.md`
- `docs/system/workspace/scripts/runtime/tool-launchers.sh`
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- `docs/PROJECT_INTENT.md`
- `docs/LAWS.md`

## Verification

- `./bin/governance-check`
- review that candidate-level acceptance remains research-boundary only
- review that issue-level acceptance now owns real-tool dual-path validation
- review that `cc` remains experimental current implementation reality in ACP comparisons

## Next

- `2026-04-01 21:26 PDT` completion: `develop` merge `a0f9a48` absorbed the ACP boundary governance line, so `ACP = optional adapter layer` and `direct = first-class path` are now canonical truth rather than branch-local research.
- `I-20260401-1703-A` and `I-20260401-1545-A-01` completed the same lifecycle line by materializing the runtime adapter axis and the first Codex ACP fresh-path prototype on top of this boundary.
- Re-open only if future ACP rollout pressures this boundary to absorb governance concerns that should remain in Freely runtime/lifecycle truth.
