# Tasks: A2A→SSE→ACP 消息投递链 + SQLite 友好校验
- issue_id: I-20260711T083155Z-A

## 子任务

### T1: freely_db_manager.py — SQLite 三层校验 gate ✅
- 状态: completed
- 内容: h_a2a_task_update_message 增加 content 非空 / role 合法 / task 存在 三层校验
- 产物: freely_db_manager.py (+50/-8)

### T2: a2a_server.py — SSE emit + 友好错误响应 ✅
- 状态: completed
- 内容: messages handler 检查 result.valid，失败返回 422，成功 emit SSE message_added
- 产物: a2a_server.py (+20/-5)

### T3: watchdog_sse.py — ACP 消息投递 ✅
- 状态: completed
- 内容: _handle_message_delivery() 实现 task → agent_working → ACP session/prompt 投递
- 产物: watchdog_sse.py (+75/-0)

### T4: a2a_task.py — CLI 友好错误输出 ✅
- 状态: completed
- 内容: update_message() 失败时打印 error + fix_hint + example 到 stderr
- 产物: a2a_task.py (+18/-1)

### T5: B1/B2 文档 ✅
- 状态: completed
- 内容: brainstorms.md, candidates.md, milestones.md, B2 brainstorms, I-* issue, prd.md, pre-tests.md
- 产物: docs/B1-docs/raw-20260711T083155Z/*.md, docs/B2-docs/a2a/message-delivery/raw-20260711T083155Z/*

### T6: PR + merge
- 状态: pending
- 内容: pr-create-guarded → pr-merge-guarded
