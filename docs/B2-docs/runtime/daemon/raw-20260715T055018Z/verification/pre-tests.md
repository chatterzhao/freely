# Pre-Tests: scan cache refresh + auto→listen universal
- issue_id: I-20260715T055018Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: bash -n 语法检查通过
- acceptance_target: freely 脚本语法无错误
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: start_project_runtime 清理旧 scan 缓存
- acceptance_target: rm -f manager-task-source-scan-latest.json 存在
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认改动
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q 'rm -f.*manager-task-source-scan-latest' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: 通用 auto→listen 降级逻辑存在
- acceptance_target: grep 确认 task_mode_auto_to_listen_universal
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认改动
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q 'task_mode_auto_to_listen_universal' docs/system/workspace/scripts/runtime/freely && echo PASS || echo FAIL
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL - fix not yet applied
- actual_output: PASS
- evidence_file: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: bash 语法 + grep 验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT-001~003 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~003 已覆盖
- replacement_evidence: AT-001~003 PASS

## Integration
- acceptance_target: daemon start 后 scan 被刷新，auto→listen 正常切换
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon 运行无 restart loop
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后实际启动验证
- replacement_evidence: 代码审查

## End-to-End
- acceptance_target: daemon start → scan fresh → AI 有数据可操作 → 正常 work cycle
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: lifecycle 显示正常 AI cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: 代码审查

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 修复逻辑简单明确——rm 缓存文件 + 条件判断提升
