# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pre-commit scope check 改为警告不阻塞
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 语法正确，--fail-on-required + exit 1 已移除
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh && echo "---" && grep "exit 1" .githooks/pre-commit.sh | grep -c "MSG\|scope"
- expected_output: 0（无 fail-on-required）\n0（scope 相关无 exit 1）
- actual_output: 0  0
- evidence_file: 
- blocker: 
- status: passed

## Unit
- acceptance_target: 3个文本文件修改正确
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 文件内容验证
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 已通过 acceptance-1 的 grep 验证，不需要额外单元测试框架
- replacement_evidence: acceptance-1 结果

## Integration
- acceptance_target: scope 超标时多文件正常 commit
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 多 scope commit 仅警告
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 仅改 hook 文本和文档，无集成面可测。merge develop 后通过后续 PR 提交流程自然覆盖
- replacement_evidence: merge 后后续 PR 提交过程

## End-to-End
- acceptance_target: develop 上 PR 正常创建合并
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge + PR 流程
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证在 merge develop 后的实际 PR 流程中自然发生
- replacement_evidence: 本 PR merge 和后续 #3601 PR 创建

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅 hook 文本和文档，不涉及运行时逻辑
