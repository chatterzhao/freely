# Pre-Tests
- issue_id: I-20260720T051323Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: capture 接受 ses_ 格式
- acceptance_target: agent_working 正确记录 opencode Worker session_id
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T051323Z-session-id-capture-ses
- required_evidence: agent_working 表包含 ses_ session_id
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260720T051323Z/verification/test-evidence/acceptance-1.log
- test_command: sqlite3 .freely/freely.db "SELECT worker_id FROM agent_working WHERE worker_id LIKE '%ses_%' LIMIT 1"
- expected_output: ses_ session_id
- expected_RED_output: 空
- actual_RED_output: capture 全部 30s 超时
- actual_output: (GREEN)
- red-green-status: green
- status: pass
- red_how: daemon log 8/8 worker capture 超时
## Unit
- acceptance_target: N/A
- testing_layer: unit
- target_environment: test-pre-merge-20260720T051323Z-session-id-capture-ses
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 一行 regex 替换
- replacement_evidence: AT-001
## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: test-pre-merge-20260720T051323Z-session-id-capture-ses
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: N/A
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T051323Z-session-id-capture-ses → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001
## Real-Environment
- real_environment_status: pass
- real_environment_reason: merge 后 daemon 重启验证
