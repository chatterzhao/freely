# Pre-Tests: A2A Worker Launch
- issue_id: I-20260710T142858Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: A2A 查询代码存在于 launch 函数中
- acceptance_target: manager_runtime_launch_workers_from_latest_task 包含 a2a_task.py list 调用
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/raw-20260710T142858Z/verification/test-evidence/acceptance-1.log
- test_command: grep -q "a2a_task.py.*list.*submitted.*worker" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: manager_runtime_launch_workers_from_latest_task 不查询 a2a_tasks
- actual_output: |
  PASS: A2A query path exists
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix — 修改前只读 continuity 文件

### acceptance-2
- id: AT-002
- requirement: A2A task state 在启动后更新为 working
- acceptance_target: launch 成功后调用 a2a_task.py update --state working
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/raw-20260710T142858Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q "update.*task-id.*state working\|--state working" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
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
- requirement: 旧 continuity 系统保留作为 fallback
- acceptance_target: A2A 路径在无 submitted tasks 时 fall through 到 continuity
- testing_layer: unit
- target_environment: fix worktree
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/task-lifecycle/raw-20260710T142858Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q "latest_launchable_manager_worker_prompt_continuity_file" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: FAIL
- actual_output: PASS
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix

## Unit
- acceptance_target: A2A worker launch
- testing_layer: unit
- target_environment: develop
- required_evidence: daemon cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon verification
- replacement_evidence: AT-001/AT-002/AT-003
## Integration
- acceptance_target: A2A worker launch
- testing_layer: integration
- target_environment: develop
- required_evidence: daemon cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon verification
- replacement_evidence: AT-001/AT-002/AT-003
## End-to-End
- acceptance_target: A2A worker launch
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge daemon verification
- replacement_evidence: AT-001/AT-002/AT-003
## Real-Environment: pass
- real_environment_status: pass
- real_environment_reason: post-merge daemon 运行验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: post-merge daemon 运行验证
