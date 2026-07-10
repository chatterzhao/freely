# Pre-Tests: Manager agent collaboration fix
- issue_id: I-20260710T061534Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: idle monitor 不误杀工作中的 bridge
- acceptance_target: _idle_monitor_loop 检查 self.pending 中活跃 session/prompt
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T061534Z/verification/test-evidence/acceptance-1.log
- test_command: grep -q "has_active_prompt" docs/system/workspace/scripts/runtime/acp-bridge.py && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: 无 has_active_prompt 检查 — idle monitor 只看时间戳，不检查活跃 prompt
- actual_output: |
  PASS: has_active_prompt check exists in _idle_monitor_loop
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: fix — idle monitor 只看时间戳，误杀工作中的 AI

### acceptance-2
- id: AT-002
- requirement: hygiene 硬编码注入已移除
- acceptance_target: build_prompt 不调用 append_manager_hygiene_alert_if_needed
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T061534Z/verification/test-evidence/acceptance-2.log
- test_command: |
  if grep "append_manager_hygiene_alert_if_needed" docs/system/workspace/scripts/runtime/freely | grep -v "^#"; then echo "FAIL"; else echo "PASS"; fi
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: build_prompt calls append_manager_hygiene_alert_if_needed
- actual_output: |
  PASS: no append_manager_hygiene_alert_if_needed in build_prompt
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: fix — build_prompt 硬编码注入 hygiene alert

### acceptance-3
- id: AT-003
- requirement: 委派指令包含 workflow skill 引用
- acceptance_target: [worker] lines 包含 workflow 指导
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T061534Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q "freely-workflow-guarded-execution" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: scan next_action 不含 workflow skill 引用
- actual_output: |
  PASS: workflow skill referenced in scan templates
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- red_how: fix — 委派指令未引用 workflow skill

## Unit
- acceptance_target: 语法检查
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: python compile + bash -n
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~AT-003 已覆盖
- replacement_evidence: AT-001/AT-002/AT-003

## Integration
- acceptance_target: daemon cycle 中 Manager 不再被超时误杀
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: Manager cycle 正常完成
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon 运行验证
- replacement_evidence: AT-001/AT-002/AT-003

## End-to-End
- acceptance_target: Manager 正常巡逻 + 委派 Worker
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon cycle 正常 + Worker 被委派
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon 验证
- replacement_evidence: AT-001/AT-002/AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 运行时间接验证
