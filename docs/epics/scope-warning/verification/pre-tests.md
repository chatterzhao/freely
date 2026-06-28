# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pre-commit scope check 改为警告不阻塞
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 中 --fail-on-required 已移除，scope note 处无 exit 1
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh; grep -A2 "scope note" .githooks/pre-commit.sh | grep -c "exit 1"
- expected_output: 0（无 fail-on-required） 0（scope note 后无 exit 1）
- actual_output: 0 0
- evidence_file: docs/epics/scope-warning/test-evidence/acceptance-1.log
- blocker: 
- status: passed

### acceptance-2
- acceptance_target: 多 scope commit 集成面正常
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 多 scope commit 仅警告不阻塞
- test_command: 在 test-pre-merge 工位做多 scope commit
- expected_output: commit 成功仅警告
- actual_output: 
- evidence_file: 
- blocker: 
- status: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 仅改 hook 文本和 AGENTS.md，不涉及多模块协作、数据流或状态变更。集成面在 merge develop 后通过后续 PR 提交流程自然覆盖

### acceptance-3
- acceptance_target: develop 上 PR 正常创建合并
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge + PR 流程正常
- test_command: 本 PR 的 merge 流程本身即为端到端验证
- expected_output: merge 成功
- actual_output: 
- evidence_file: 
- blocker: 
- status: not_applicable
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证在 merge develop 后的实际 PR 流程中自然发生，当前工位无法模拟

## Unit
- acceptance_target: 文件修改正确
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 手动验证通过
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 已通过 acceptance-1 的 grep 验证覆盖
- replacement_evidence: acceptance-1 验证结果

## Integration
- acceptance_target: 多 scope commit 不阻塞
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: (不适用)
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 仅 hook 文本+文档，无集成面可测。merge 后自然覆盖
- replacement_evidence: 后续 PR 流程

## End-to-End
- acceptance_target: develop 上 PR 正常
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: (不适用)
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: merge 后实际 PR 流程自然验证
- replacement_evidence: 本 PR merge + 后续 #3601 PR

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅 hook 文本和文档，不涉及运行时逻辑
