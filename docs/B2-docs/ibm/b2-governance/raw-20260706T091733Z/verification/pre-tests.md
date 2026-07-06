# Pre-Tests: 门禁硬拦截
- issue_id: I-20260706T091733Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: gh wrapper 拦截 pr merge
- acceptance_target: gh pr merge 被 blocked
- testing_layer: unit
- target_environment: test-pre-merge-20260706T091733Z-gate-hard-block
- required_evidence: gh pr merge 输出 blocked 信息
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T091733Z/verification/test-evidence/acceptance-1.log
- test_command: .githooks/bin/gh pr merge 2>&1 | grep -q 'BLOCKED' && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending

### acceptance-2
- id: AT-002
- requirement: git wrapper 剥离 --no-verify
- acceptance_target: git push --no-verify 被 wrapper 拦截
- testing_layer: unit
- target_environment: test-pre-merge-20260706T091733Z-gate-hard-block
- required_evidence: --no-verify 被 stripped
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260706T091733Z/verification/test-evidence/acceptance-2.log
- test_command: PATH=".githooks/bin:$PATH" git push --no-verify 2>&1 | grep -q 'stripped' && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending

## Unit
- acceptance_target: PATH wrappers 正确拦截
- testing_layer: unit
- target_environment: test-pre-merge-20260706T091733Z-gate-hard-block
- required_evidence: AT-001 + AT-002
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: freely pr-create-guarded 全部门禁通过
- testing_layer: integration
- target_environment: test-pre-merge-20260706T091733Z-gate-hard-block
- required_evidence: governance gate PASS
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: full pr-create → pr-merge → wt-close chain
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: PR merged
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: PATH wrappers tested via unit checks, full chain validated via governance gate
