# Pre-tests: acp-optional-adapter-boundary-governance

## Acceptance Structure

### Pre-merge focused regression / smoke

1. `boundary-freeze` 明确：
   - ACP 被定义为 optional adapter layer
   - `direct` 被定义为 first-class path
   - `per-tool adapter selection` 被定义为 canonical direction
2. `concern-split` 明确：
   - ACP 只吸收 communication plane
   - Freely 继续保留 governance / continuity / recovery truth
3. `prototype-preconditions` 明确：
   - future prototype 先抽 `adapter axis`
   - 不把“接一条 ACP bridge”误写成完整原型前提

### Post-merge integration acceptance

1. 后续 implementation owner 必须能直接从 issue / PRD / tasks 看出实现顺序：
   - extract adapter axis
   - add ACP adapter path
   - pick first-tool prototype
   - execute real-tool dual-path validation
2. 后续 implementation owner 必须能直接识别第一批代码落点：
   - `docs/system/workspace/tools.md`
   - `docs/system/workspace/scripts/runtime/tool-launchers.sh`
   - `docs/system/workspace/scripts/runtime/freely`
3. candidate / milestone / issue 三处口径必须一致，不再出现：
   - candidate 继续标 `needs_research`
   - milestone 仍停在 `pending://issue-materialization`
   - issue 却已 materialized 的生命周期冲突

### Post-merge application-native real-environment acceptance

1. future prototype owner 的 acceptance 必须要求真实工具验证，而不是只做 schema review：
   - 至少一个现有工具可验证 `direct -> acp`
   - 至少一个新增工具可选择 `direct` 或 `acp`
2. issue-bound truth 必须明确两条路径都写回同一套 continuity / recovery evidence。

### Post-merge end-to-end dogfood acceptance

1. Freely 后续自举开发新增工具接入时，必须能按每工具配置选择：
   - `adapter=direct`
   - `adapter=acp`
   - `adapter=prefer_acp_fallback_direct`
2. experimental current implementation reality 不得在 dogfood 过程中冒充 canonical promised contract。

### Non-Goals

1. 本轮不执行具体 ACP bridge。
2. 本轮不要求真实工具端到端测试已经跑通。
3. 本轮不要求决定最终 first-tool prototype 一定是谁。

## Acceptance Items

### PT-1
- id: `PT-1`
- requirement: `ACP boundary freezes ACP as optional adapter layer and direct as first-class path`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/acp-optional-adapter-boundary-governance/issues/acp-optional-adapter-boundary-governance.md`

### PT-2
- id: `PT-2`
- requirement: `issue-bound truth keeps communication concerns in ACP and governance concerns in Freely`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/progress/workspace-routing-foundation/p-acp-optional-adapter-boundary-governance.md`

### PT-3
- id: `PT-3`
- requirement: `follow-on implementation order is frozen before any first-tool ACP prototype`
- evidence_level: `mock`
- status: `pass`
- artifact_ref: `docs/milestones.md`
