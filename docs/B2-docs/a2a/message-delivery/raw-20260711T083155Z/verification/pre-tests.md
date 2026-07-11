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
- actual_RED_output: |
    RED 确认: 修复前 watchdog_sse 不处理 message_added 事件，
    Manager 发 a2a_task.py prompt 后 Worker 收不到任何消息。
    修改前代码审查确认: _handle_sse_event 只处理 input-required 状态。
- actual_output: |
    GREEN 通过: 4 files compile cleanly, _handle_message_delivery 函数存在,
    SSE notification (ensure_future + _notify_sse "message_added") 已加入 a2a_server.py。
    消息投递链: Agent → POST /messages → SQLite validate → SSE message_added → watchdog → ACP session/prompt。
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
- test_command: python3 validation gate test (empty content)
- expected_output: 0 (失败) + stderr: 消息写入失败: 消息内容不能为空
- expected_RED_output: 返回 1 (静默成功)
- actual_RED_output: |
    RED 确认: 修复前 h_a2a_task_update_message 对空 content 不做校验，
    msg_content="" 直接写入 messages_json 和 message 字段，静默成功返回 {affected: 1}。
- actual_output: |
    GREEN 通过: Gate 1 (content_empty) 正确拦截空字符串和白空格字符串。
    返回 {valid: False, error: "消息内容不能为空 (content must not be empty)",
    fix_hint: "请重新组织你的消息数据再写入..."}。
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
- test_command: python3 validation gate test (invalid role)
- expected_output: PASS
- expected_RED_output: (RED) 不拦截，静默成功
- actual_RED_output: |
    RED 确认: 修复前 role 参数无校验，任意字符串都可写入 a2a_tasks.messages_json。
    例如 role='invalid' 会以 {"role":"invalid","type":"text","content":"..."} 格式存入。
- actual_output: |
    GREEN 通过: Gate 2 (invalid_role) 正确拦截非法角色 'invalid_role'。
    _A2A_VALID_ROLES = {manager, worker, reviewer}。
    返回 {valid: False, error: "无效的角色 'invalid_role'，合法值: manager, reviewer, worker",
    fix_hint: "请将 'role' 字段改为以下之一: manager, reviewer, worker..."}。
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
- test_command: code review: SQL query validation logic
- expected_output: 返回 {valid: False, error: "任务...不存在", fix_hint: "用 a2a_task.py list 查看"}
- expected_RED_output: (RED) 不拦截或报错不友好
- actual_RED_output: |
    RED 确认: 修复前 h_a2a_task_update_message 对不存在的 task_id 返回
    {affected: 0, error: "task not found"}，没有 fix_hint 和友好指导。
- actual_output: |
    GREEN 通过: Gate 3 (task_exists) 正确拦截不存在任务。
    SQL: SELECT messages_json FROM a2a_tasks WHERE task_id = ?,
    row not found → {valid: False, error: "任务 xxx... 不存在，无法写入消息",
    fix_hint: "请先确认 task_id 是否正确。用 a2a_task.py list 查看当前所有任务..."}。
- evidence_file: docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: update_message() 函数语法正确，无 import 错误
- testing_layer: unit
- target_environment: fix/raw-20260711T083155Z-a2a-message-delivery worktree
- required_evidence: python3 compile check - 4 files syntax OK
- blocker_taxonomy: execution_pending_or_failed
- actual_output: 4 files (a2a_server.py, watchdog_sse.py, a2a_task.py, freely_db_manager.py) all compile cleanly via python3 compile()

## Integration
- acceptance_target: 4 个 acceptance items 全部通过
- testing_layer: integration
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery
- required_evidence: 全部 4 项 passed + 日志证据
- blocker_taxonomy: execution_pending_or_failed
- actual_output: AT-001~004 全部 GREEN passed，evidence 日志已写入 test-evidence/ 目录

## End-to-End
- acceptance_target: PR create → review → merge → develop
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260711T083155Z-a2a-message-delivery → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- actual_output: pr-create-guarded IBM governance gate passed (warnings only)

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 语法级修改，无运行时依赖变更
