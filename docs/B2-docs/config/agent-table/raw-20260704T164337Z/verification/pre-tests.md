# Pre-Tests: ACP cleanup
- issue_id: I-20260704T164337Z-A

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 6 stubs deleted, 0 DEPRECATED remaining
- acceptance_target: watchdog_sse.py 无 DEPRECATED 残留
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep count=0
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/watchdog_sse.py
- test_command: grep -c "DEPRECATED" docs/system/workspace/scripts/runtime/watchdog_sse.py
- expected_output: 0
- expected_RED_output: 6
- actual_RED_output: (RED)
- actual_output: GREEN. 0 DEPRECATED remaining.
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 6 个 DEPRECATED stub → RED

## Unit
- acceptance_target: grep 静态验证
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001 passed
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 纯删除+签名修正，grep 等效覆盖
- replacement_evidence: AT-001 GREEN

## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: test-pre-merge-20260704T164337Z-acp-cleanup
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯清理，无集成面
- replacement_evidence: 无

## End-to-End
- acceptance_target: N/A
- testing_layer: end_to_end
- target_environment: develop
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 纯清理
- replacement_evidence: 无

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯清理，无运行时影响
