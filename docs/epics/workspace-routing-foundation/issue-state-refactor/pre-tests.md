# Pre-Tests — scan 常量对齐 IBM Framework §89

- issue_id: I-20260505T1210Z-A

## Unit

- acceptance target: scan 常量和 raw phase_state 读取逻辑变更——不涉及可执行单元测试边界
- testing layer: unit
- target environment: feature worktree (local)
- required evidence: grep verification of constant values
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 常量定义变更（3 行）和 frontmatter 字段回退逻辑，不涉及可执行单元测试
- replacement_evidence: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md

## Integration

- acceptance target: scan 对新旧 phase_state 值的正确分类（absorbed→终端，completed→终端）
- testing layer: integration
- target environment: feature worktree with develop baseline
- required evidence: 20260502-1028 不再误报，现有 completed issue 不受影响
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: scan 是只读分析工具，正确性通过手工对比 scan 输出确认
- replacement_evidence: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md

## End-to-End

- acceptance target: 完整 merge 链路 feature→test-pre-merge→develop gate 全部通过
- testing layer: end_to_end
- target environment: test-pre-merge worktree
- required evidence: pr-merge-guarded gate passed
- blocker taxonomy: definition_missing
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 端到端验证面是 gate 链路本身
- replacement_evidence: pr-merge-guarded 执行日志

## Real-Environment

- real_environment_status: pass
- real_environment_reason: 常量定义和前端解析逻辑变更，不影响运行时行为，不需要真实环境测试

## Acceptance Items

### A1 - Constants match IBM Framework §89

- id: A1
- requirement: TERMINAL_RAW={absorbed,dropped}, DONE_STATES={done_b2_ibm,completed}, ACTIVE_B2={in_b2_ibm,done_b2_ibm,in_dev,blocked_dev}
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 常量值通过 code-review 验证，不产生可执行测试产物
- replacement_evidence: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md

### A2 - No regression on existing completed items

- id: A2
- requirement: phase_state=completed 的 I-* issue 行为不变——completed ∈ DONE_STATES 不变
- evidence_level: integration
- status: not_applicable
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: completed 仍在 DONE_STATES 中，code-review 确认无退化
- replacement_evidence: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md

### A3 - Absorbed raw no longer false-positive

- id: A3
- requirement: phase_state=absorbed 的 raw 不再出现在 scan 非终端项中
- evidence_level: integration
- status: not_applicable
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 20260502-1028 从 scan 排除即验证通过
- replacement_evidence: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review.md

### B1 - issue-sync close preserves raw phase_state

- id: B1
- requirement: issue-sync close raw-xxx 后 raw phase_state 不变（保持 absorbed）
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review-B.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### B2 - issue-sync create sets platform_state

- id: B2
- requirement: issue-sync create 后 platform_state=open
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review-B.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### C1 - G1 blocks completed+open

- id: C1
- requirement: phase_state=completed 且 platform_state=open → gate block
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review-C.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### C2 - S3 blocks illegal phase_state

- id: C2
- requirement: phase_state 不在合法值集合中 → gate block
- evidence_level: integration
- status: pass
- artifact_ref: docs/epics/workspace-routing-foundation/issue-state-refactor/code-reviews/review-C.md
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

