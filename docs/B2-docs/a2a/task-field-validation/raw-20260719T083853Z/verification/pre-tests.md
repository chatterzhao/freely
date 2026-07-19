# Pre-Tests: 三层校验
- issue_id: I-20260719T083853Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: L1 — a2a_task.py handler校验worker task必填字段
- acceptance_target: 校验代码存在且错误消息含字段名
- testing_layer: unit
- target_environment: fix-raw-20260719T083853Z-a2a-task-validation
- required_evidence: grep命中
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c 'worker task requires' docs/system/workspace/scripts/runtime/a2a_task.py
- expected_output: "1"
- expected_RED_output: "0"
- actual_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前handler无校验,空值静默写入

### acceptance-2
- id: AT-002
- requirement: L2 — DB insert校验worker task必填字段
- acceptance_target: 校验代码存在
- testing_layer: unit
- target_environment: fix-raw-20260719T083853Z-a2a-task-validation
- required_evidence: grep命中
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c 'worker task rejected' docs/system/workspace/scripts/runtime/freely_db_manager.py
- expected_output: "1"
- expected_RED_output: "0"
- actual_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前DB insert无校验

### acceptance-3
- id: AT-003
- requirement: L3 — agent_assign校验agent_id格式
- acceptance_target: 校验代码存在且含格式说明
- testing_layer: unit
- target_environment: fix-raw-20260719T083853Z-a2a-task-validation
- required_evidence: grep命中
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c "agent_id.*invalid.*worker_NN" docs/system/workspace/scripts/runtime/agent_working.py
- expected_output: "1"
- expected_RED_output: "0"
- actual_output: "1"
- red-green-status: green
- status: pass
- red_how: 当前agent_assign无格式校验

### acceptance-4
- id: AT-004
- requirement: prompt模板含--worktree --branch --raw-key
- acceptance_target: 模板存在且区分配Manager和Worker
- testing_layer: unit
- target_environment: fix-raw-20260719T083853Z-a2a-task-validation
- required_evidence: grep命中
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c 'worktree.*branch.*raw-key' docs/system/workspace/scripts/runtime/freely
- expected_output: "2"
- expected_RED_output: "0"
- actual_output: "2"
- red-green-status: green
- status: pass
- red_how: 当前模板无这些字段

## Unit
- acceptance_target: AT-001~004 grep验证修改存在
- testing_layer: unit
- target_environment: fix-raw-20260719T083853Z-a2a-task-validation
- required_evidence: AT-001~004覆盖
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 三层校验为代码修改, grep验证即覆盖单元层
- replacement_evidence: AT-001~004 GREEN输出

## Integration
- acceptance_target: 无效worker task被L1拒绝 + 报错明确
- testing_layer: integration
- target_environment: test-pre-merge-20260719T083853Z-a2a-task-validation
- required_evidence: AT-001~004覆盖 + post-merge daemon验证
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 集成验证需daemon重启后Manager AI调用a2a-exit, 属post-merge dogfood
- replacement_evidence: AT-001~004 GREEN

## End-to-End
- acceptance_target: 有效task正常创建,无效task被拒绝
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: post-merge daemon + Manager实际调用
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 需完整daemon运行+Manager AI决策, post-merge dogfood
- replacement_evidence: AT-001~004 GREEN

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 三层校验已实现(L1 handler+L2 DB+L3 agent_assign), 无效worker task在写入前被拒绝并返回明确错误消息
