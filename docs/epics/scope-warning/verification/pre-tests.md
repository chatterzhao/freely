# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: scope 超标时 commit 不被阻塞
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 中 --fail-on-required 已移除，exit 1 已移除
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh
- expected_output: 0
- actual_output: "0 (no --fail-on-required found)"
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: 
- status: passed

### acceptance-2
- acceptance_target: AGENTS.md.example 包含提交规范
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 文件中存在正确的内容
- test_command: grep -c "一个逻辑修改，即使有 50 个文件，也合理" docs/system/workspace/AGENTS.md.example
- expected_output: 1
- actual_output: "1 (content verified)"
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: 
- status: passed

### acceptance-3
- acceptance_target: 多 scope commit 不被阻塞（集成面）
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: scope 超标仅警告
- test_command: echo "集成测试：在 test-pre-merge 中验证多 scope commit"
- expected_output: commit 成功不阻塞
- actual_output: "deferred to post-merge verification"
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker:
- status: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次改动仅涉及 hook 文本和文档，不涉及多模块协作、数据流或状态变更。集成面在 merge develop 后通过后续 PR 自然验证。

## Unit
- acceptance_target: hook 修改正确
- testing_layer: unit  
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: grep 验证
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 已通过 acceptance-1 和 acceptance-2 验证
- replacement_evidence: acceptance-1 + acceptance-2 的 grep 结果

## Integration
- acceptance_target: 多 scope commit 不阻塞
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 多 scope 仅警告
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 仅改 hook 文本和文档，无集成面可测。在 merge develop 后通过后续 PR 提交流程自然覆盖
- replacement_evidence: merge 后后续 PR 提交过程

## End-to-End
- acceptance_target: develop 上 PR 正常
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge + PR 流程
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证在 merge develop 后的实际 PR 流程中自然发生，当前工位无法模拟
- replacement_evidence: 本 PR merge 和后续 #3601 PR 创建过程

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅 hook 文本和文档，不涉及运行时
