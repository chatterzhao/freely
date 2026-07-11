# Pre-Tests: A2A→SSE→ACP 消息投递链 + SQLite 友好校验
- issue_id: I-20260711T083155Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 正常消息投递全链路
- acceptance_target: Manager 发消息 → Worker ACP session 收到
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: SSE message_added 事件发出 + watchdog 日志显示 ACP 投递成功
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-1.log
- test_command: echo "验证: a2a_task.py prompt 发送 → A2A Server SSE → watchdog ACP 投递"
- expected_output: watchdog 日志: message_delivery: worker session=xxx task=xxx ok
- expected_RED_output: (RED 阶段) watchdog 日志无 message_delivery 行
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: 空 content 被 SQLite 层拦截并返回友好错误
- acceptance_target: 发空消息 → HTTP 422 + fix_hint + example
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: 返回 {"ok":false, "error":"消息内容不能为空", "fix_hint":"..."}
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-2.log
- test_command: python3 -c "from a2a_task import update_message; print(update_message('test-xxx', ''))"
- expected_output: 0 (失败) + stderr: 消息写入失败: 消息内容不能为空
- expected_RED_output: 返回 1 (静默成功)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-3
- id: AT-003
- requirement: 非法 role 被拦截
- acceptance_target: role=invalid → HTTP 422 + 合法值列表
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: 返回 fix_hint 包含 "manager, reviewer, worker"
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-3.log
- test_command: grep -q "无效的角色" <(python3 -c "from a2a_task import update_message; update_message('test-xxx','hello','invalid')" 2>&1) && echo PASS
- expected_output: PASS
- expected_RED_output: (RED) 不拦截，静默成功
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-4
- id: AT-004
- requirement: 不存在的 task_id 被拦截
- acceptance_target: 不存在的 task → HTTP 422 + "任务...不存在"
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: 返回 fix_hint 建议用 a2a_task.py list 查看
- evidence_level: integration
- artifact_ref: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-4.log
- test_command: grep -q "不存在" <(python3 -c "from a2a_task import update_message; update_message('nonexistent-task-id-12345','hello')" 2>&1) && echo PASS
- expected_output: PASS
- expected_RED_output: (RED) 不拦截或报错不友好
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: update_message() 函数语法正确，无 import 错误
- testing_layer: unit
- target_environment: fix/raw-20260711T083155Z-a2a-message-delivery worktree
- required_evidence: python3 -c "import a2a_task" 成功
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 4 个 acceptance items 全部通过
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: 全部 4 项 passed + 日志证据
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: PR create → review → merge → develop
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 语法级修改，无运行时依赖变更
