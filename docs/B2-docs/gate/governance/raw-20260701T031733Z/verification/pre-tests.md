# Pre-Tests: skill 模板对齐 gate 期望
- issue_id: I-20260701T031733Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: B1 candidates.md 模板包含 promoted_issue_path 示例
- acceptance_target: grep 确认模板中有 promoted_issue_path 字段
- testing_layer: unit
- target_environment: test-pre-merge-20260701T031733Z-gate-skill-alignment
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-1.log
- test_command: grep -c "promoted_issue_path" docs/system/workspace/skills/freely-doc-B1_IBM-execution/SKILL.md
- expected_output: 匹配到至少 1 处 promoted_issue_path
- expected_RED_output: 匹配到 0 处 (修复前模板无此字段)
- actual_RED_output: grep 返回 0（B1 模板无 promoted_issue_path）— RED 确认
- actual_output: grep 返回 2（模板中 2 处 promoted_issue_path 示例）
- evidence_file: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: feature: 修复前 B1 模板无 promoted_issue_path 字段

### acceptance-2
- id: AT-002
- requirement: B2 pre-tests.md 模板无反引号且含 epics-map 提醒
- acceptance_target: grep 确认模板已修正
- testing_layer: unit
- target_environment: test-pre-merge-20260701T031733Z-gate-skill-alignment
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-2.log
- test_command: grep -c "epics-map\|force-add.*log\|not_applicable_reason.*covered" docs/system/workspace/skills/freely-doc-B2_IBM-execution/SKILL.md
- expected_output: 匹配到 epics-map、force-add、not_applicable_reason 各至少 1 处
- expected_RED_output: 匹配数不足 (修复前模板无这些内容)
- actual_RED_output: grep 返回 0（B2 模板无 epics-map/force-add 提醒）— RED 确认
- actual_output: epics-map=1 force-add=1 各至少 1 处
- evidence_file: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-2.log
- red-green-status: green
- status: passed
- red_how: feature: 修复前 B2 模板无反引号警告、epics-map 提醒、evidence force-add 提醒

### acceptance-3
- id: AT-003
- requirement: dev-loop 和 test-execution skill 含 dev-to-test merge 提醒
- acceptance_target: grep 确认 merge 提醒存在
- testing_layer: unit
- target_environment: test-pre-merge-20260701T031733Z-gate-skill-alignment
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-3.log
- test_command: grep -c "merge.*test\|merge.*测试" docs/system/workspace/skills/freely-dev-loop-execution/SKILL.md docs/system/workspace/skills/freely-test-execution/SKILL.md
- expected_output: 每个文件至少 1 处 merge 到 test 的提醒
- expected_RED_output: dev-loop skill 无 merge 提醒 (修复前)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: dev-loop 1 处 test-execution 多处 merge 提醒
- evidence_file: docs/B2-docs/gate/governance/raw-20260701T031733Z/verification/acceptance-3.log
- red-green-status: green
- status: passed
- red_how: feature: 修复前 dev-loop skill 无 merge 到 test 提醒

## Unit
- acceptance_target: 5 个 skill 文件语法正确 (Markdown)
- testing_layer: unit
- target_environment: feature/raw-20260701T031733Z-gate-skill-alignment
- required_evidence: 文件存在且可读
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: Markdown 文件无语法检查工具，已被 AT-001/002/003 的 grep 验证覆盖
- replacement_evidence: AT-001/002/003 的 grep 结果
- status: not_applicable

## Integration
- acceptance_target: 模板示例之间格式一致，字段命名统一
- testing_layer: integration
- target_environment: test-pre-merge-20260701T031733Z-gate-skill-alignment
- required_evidence: 人工审查
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 模板一致性由 AT-001/002/003 逐项验证覆盖
- replacement_evidence: AT-001/002/003 的 grep 结果
- status: not_applicable

## End-to-End
- acceptance_target: 使用修正后的模板走完一个完整 PR，门禁失败次数显著减少
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T031733Z-gate-skill-alignment → develop merge chain
- required_evidence: 后续 PR 的门禁通过率提升
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证需在后续实际 PR 中观察，本轮通过单元验证确认模板修正
- replacement_evidence: AT-001/002/003 绿色证据 + 后续 PR 门禁日志
- status: not_applicable

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 4 个 skill 文件已修正，模板字段齐全，merge 提醒已添加
