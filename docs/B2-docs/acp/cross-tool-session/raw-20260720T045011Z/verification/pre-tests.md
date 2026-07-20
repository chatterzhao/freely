# Pre-Tests: session ID capture ses_ 格式
- issue_id: I-20260720T045011Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: capture_worker_session_id_and_store 接受 ses_ 格式 session ID
- acceptance_target: opencode Worker 的 ses_ session ID 正确写入 agent_working
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T045011Z-session-id-capture-ses-format
- required_evidence: agent_working 表 worker_id 列包含 session_id
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260720T045011Z/verification/test-evidence/acceptance-1.log
- test_command: sqlite3 .freely/freely.db "SELECT worker_id FROM agent_working WHERE worker_id LIKE '%ses_%' LIMIT 1"
- expected_output: 返回包含 ses_ 的 worker_id
- expected_RED_output: 空结果（修复前 session_id 从未被捕获）
- actual_RED_output: 所有 capture 超时 30s，agent_working 无 session_id
- actual_output: (GREEN阶段填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: daemon log 显示 8/8 worker capture 全部 30s 超时
## Unit
- acceptance_target: N/A
- testing_layer: unit
- target_environment: test-pre-merge-20260720T045011Z-session-id-capture-ses-format
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 一行 regex 替换，无可单元测试函数边界
- replacement_evidence: AT-001 覆盖
## Integration
- acceptance_target: N/A
- testing_layer: integration
- target_environment: test-pre-merge-20260720T045011Z-session-id-capture-ses-format
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: Worker 正常启动后 agent_working 正确记录 session_id
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T045011Z-session-id-capture-ses-format → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 覆盖
- replacement_evidence: AT-001
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 一行改动。real env 验证将在 merge 后 daemon 重启自动完成
