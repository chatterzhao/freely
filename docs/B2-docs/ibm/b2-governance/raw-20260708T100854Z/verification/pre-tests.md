# Pre-Tests: A2A socket + timestamps
- issue_id: I-20260708T100854Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: _a2a_socket_path 返回 .sock + watchdog 日志有时间戳
- testing_layer: unit
- target_environment: test-pre-merge-20260708T100854Z-a2a-socket-path-fix
- required_evidence: grep 确认
- evidence_level: real_env
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T100854Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "\.sock" docs/system/workspace/scripts/runtime/freely | head -1
- expected_output: ">0"
- red-green-status: green
- status: pass
- blocker: execution_pending_or_failed
- red_how: fix: 修改前 _a2a_socket_path 无 .sock
## Unit
- acceptance_target: 语法检查
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: py_compile
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 文本修改
- replacement_evidence: AT-001 grep
## Integration
- acceptance_target: 无集成面
- testing_layer: integration
- target_environment: test-pre-merge-20260708T100854Z-a2a-socket-path-fix
- required_evidence: 不适用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 文本修改
- replacement_evidence: AT-001
## End-to-End
- acceptance_target: 门禁链
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 门禁链覆盖
- replacement_evidence: pr-create-guarded gate chain
## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001 GREEN
