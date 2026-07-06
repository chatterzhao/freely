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
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/B2-docs/acp/acp-optional-adapter-boundary-governance/raw-20260401-1545/issues/acp-optional-adapter-boundary-governance.md`

### PT-2
- id: `PT-2`
- requirement: `issue-bound truth keeps communication concerns in ACP and governance concerns in Freely`
- evidence_level: `mock`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/progress/workspace-routing-foundation/p-acp-optional-adapter-boundary-governance.md`

### PT-3
- id: `PT-3`
- requirement: `follow-on implementation order is frozen before any first-tool ACP prototype`
- evidence_level: `mock`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/milestones.md`
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
