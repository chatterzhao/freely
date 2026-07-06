# Pre-Tests: hook 提示 + 命令速查
- issue_id: I-20260706T114314Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: pre-commit 拦截消息含完整流程
- testing_layer: unit
- target_environment: test-pre-merge-20260706T114314Z-hook-messages-and-cmd-docs
- required_evidence: grep 验证消息内容
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T114314Z/verification/test-evidence/acceptance-1.log
- test_command: grep -q 'freely feedback' .githooks/pre-commit.sh && echo "PASS" || echo "FAIL"
- expected_output: PASS
- red-green-status: pending
- status: pending

### acceptance-2
- id: AT-002
- requirement: AGENTS.md 含命令速查表
- testing_layer: unit
- target_environment: test-pre-merge-20260706T114314Z-hook-messages-and-cmd-docs
- required_evidence: grep 验证
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T114314Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'freely pr-create-guarded.*gh pr create' AGENTS.md && echo "PASS" || echo "FAIL"
- expected_output: PASS
- red-green-status: pending
- status: pending

## Unit
- acceptance_target: 文本内容验证
- testing_layer: unit
- target_environment: test-pre-merge-20260706T114314Z-hook-messages-and-cmd-docs
- required_evidence: AT-001 + AT-002
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: n/a (纯文本修改)
- testing_layer: integration
- target_environment: test-pre-merge-20260706T114314Z-hook-messages-and-cmd-docs
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文本修改，无运行时行为
- replacement_evidence: AT-001 + AT-002 grep 验证

## End-to-End
- acceptance_target: n/a
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯文本修改
- replacement_evidence: pr-create-guarded 全部门禁通过

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯文档修改
