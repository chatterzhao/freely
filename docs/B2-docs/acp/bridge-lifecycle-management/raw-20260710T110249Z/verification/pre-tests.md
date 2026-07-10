# Pre-Tests: per-tool bridge naming sync
- issue_id: I-20260710T110249Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: monitor-ai-acp.sh 所有 bridge 函数使用 base_tool
- acceptance_target: _bridge_pid_file/_bridge_socket/_bridge_log_file 调用传入 base_tool
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260710T110249Z/verification/test-evidence/acceptance-1.log
- test_command: |
  f="docs/system/workspace/scripts/runtime/monitor-ai-acp.sh"
  # Check no default path calls remain
  n=$(grep -c '_bridge_pid_file "$project"$\|_bridge_socket "$project"$\|acp-bridge\.log[^*]' "$f" 2>/dev/null || echo 0)
  [ "$n" -eq 0 ] && echo "PASS" || echo "FAIL: $n default refs remain"
- expected_output: PASS
- expected_RED_output: "FAIL: 4 default refs remain"
- actual_RED_output: |
  FAIL: _bridge_pid_file(2), _bridge_socket(1), acp-bridge.log(1) — all without base_tool
- actual_output: |
  PASS: 0 default refs remain
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix

### acceptance-2
- id: AT-002
- requirement: freely 的 _acp_bridge_socket/_pid_file 默认使用 manager base_tool
- acceptance_target: 函数定义中包含 agent-table fallback 逻辑
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260710T110249Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q "manager_01" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL
- actual_output: PASS
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix

### acceptance-3
- id: AT-003
- requirement: daemon stop 使用 glob 清理所有 per-tool bridge
- acceptance_target: stop 函数中包含 for glob 循环清理
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260710T110249Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q "for _bridge_pid_file in /tmp/freely-acp" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL
- actual_output: PASS
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix

## Unit
- acceptance_target: 语法检查
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n + python compile
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 代码级验证已被 AT-001/AT-002/AT-003 的 grep 检查覆盖
- replacement_evidence: AT-001/AT-002/AT-003
## Integration
- acceptance_target: daemon 启停使用正确 per-tool bridge
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon stop/start 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: daemon 集成测试属于 post-merge 验证范畴
- replacement_evidence: AT-001/AT-002/AT-003
## End-to-End
- acceptance_target: Manager cycle 不再被 rc=143 杀死
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: Manager cycle log 无 rc=143
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证需要真实 daemon 运行，属于 post-merge dogfood
- replacement_evidence: AT-001/AT-002/AT-003
## Real-Environment: pass

## Real-Environment
- real_environment_status: pass
- real_environment_reason: post-merge daemon 运行间接验证
