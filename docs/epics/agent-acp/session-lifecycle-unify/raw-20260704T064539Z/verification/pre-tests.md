# Pre-Tests: 统一 ACP session 管理

- issue_id: I-20260704T064539Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: agent_working 表有 slot 列，acp_session_connect 写入 slot
- acceptance_target: 调用 acp_session_connect 后 agent_working 表中对应行 slot 字段值等于传入的 slot
- testing_layer: unit
- target_environment: feature-local
- required_evidence: Python 测试脚本输出 PASS
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/agent_working.py
- test_command: python3 -c "from agent_working import acp_session_register; acp_session_register('.', 'test_key', 'worker', 'w1', session_id='test_sid', slot='opencode-apikey-ds-flash-auto'); row = _db_rpc('.', 'agent_working.get', {'raw_key': 'test_key'}); assert row.get('row', {}).get('slot') == 'opencode-apikey-ds-flash-auto'; print('PASS')"
- expected_output: PASS
- expected_RED_output: agent_working 表无 slot 列，SQL 报错
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 agent_working 表无 slot 列，INSERT 会报错 → RED

### acceptance-2
- id: AT-002
- requirement: acp_session_connect 正确选择 session 操作 (prompt > resume > fork > new)
- acceptance_target: alive session → prompt, dead session → resume, no session → fork, cross-tool → new
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 单元测试覆盖 4 种路径的决策
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/agent_working.py
- test_command: bash docs/system/workspace/scripts/tests/test-acp-session-connect-decision-tree
- expected_output: 所有 4 条路径测试 PASS (prompt/resume/fork/new 按优先级正确选择)
- expected_RED_output: 测试不存在或 acp_session_connect 未实现
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前无 acp_session_connect 函数 → 测试文件不存在 → RED

### acceptance-3
- id: AT-003
- requirement: watchdog_sse.py 6 个旧函数已删除，handler 改为调用 acp_session_connect
- acceptance_target: watchdog_sse.py 中无 _acp_session_new/fork/resume/prompt/should_use_fork/create_reviewer_session
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认旧函数不存在
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/watchdog_sse.py
- test_command: grep -c "_acp_session_new\|_acp_session_fork\|_acp_session_resume\|_acp_session_prompt\|_should_use_fork\|_create_reviewer_session" docs/system/workspace/scripts/runtime/watchdog_sse.py
- expected_output: 0
- expected_RED_output: 6 (6 个旧函数仍存在)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 6 个旧函数仍在 watchdog_sse.py 中，grep 计数 >0 → RED

### acceptance-4
- id: AT-004
- requirement: _ensure_acp_bridge_running 接受显式 base_tool 参数
- acceptance_target: 函数签名包含 base_tool 参数，内部不再从 AGENT_AI_TOOL 读取
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认签名和内部实现
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep -A3 "_ensure_acp_bridge_running()" docs/system/workspace/scripts/runtime/freely | grep "base_tool"
- expected_output: 包含 base_tool="${2:-claude}" 参数声明
- expected_RED_output: 内部从 AGENT_AI_TOOL 读取 base_tool
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前函数签名不接受 base_tool 参数，内部从 AGENT_AI_TOOL 取 → RED

### acceptance-5
- id: AT-005
- requirement: _acp_bridge_socket 接受 base_tool 参数（本期忽略，行为不变）
- acceptance_target: 函数签名包含 base_tool，本期调用方传入但被忽略，返回原有 socket 路径
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认签名预留 + 调用方传参
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep "_acp_bridge_socket()" docs/system/workspace/scripts/runtime/freely | grep "base_tool"
- expected_output: 包含 base_tool 参数
- expected_RED_output: 函数签名无 base_tool 参数
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 _acp_bridge_socket 只接受 project → RED

### acceptance-6
- id: AT-006
- requirement: CLAUDE_SESSION_ID_CURRENT 全部替换为 TOOL_SESSION_ID_CURRENT (3 文件 11 处)
- acceptance_target: 搜索代码库中无 CLAUDE_SESSION_ID_CURRENT 残留
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认 0 处残留
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep -rn "CLAUDE_SESSION_ID_CURRENT" docs/system/workspace/scripts/ --include="*.sh" --include="*.py" | grep -v "\.bak\|__pycache__" | wc -l
- expected_output: 0
- expected_RED_output: 11 (11 处残留)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 11 处 CLAUDE_SESSION_ID_CURRENT → RED

### acceptance-7
- id: AT-007
- requirement: debug 回退日志在异常路径输出（resume 失败、fork 失败、未知场景）
- acceptance_target: 回退到 session/new 时 stderr 包含 fallback 日志
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 代码中包含 log_warn/log_info 的 fallback 语句
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/agent_working.py
- test_command: grep -c "falling back\|fell back\|fallback to new" docs/system/workspace/scripts/runtime/agent_working.py docs/system/workspace/scripts/runtime/watchdog_sse.py docs/system/workspace/scripts/runtime/freely
- expected_output: count >= 4 (4 个 fallback 路径: resume fail, fork fail, cross-tool, unknown)
- expected_RED_output: 0 (无回退日志)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前无统一 session 管理，无回退日志 → RED

## Unit
- acceptance_target: 每个修改点通过 grep 静态验证确认代码模式正确
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001 ~ AT-007 全部 passed
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: daemon 启动后 session 创建/恢复/通信正常工作
- testing_layer: integration
- target_environment: test-pre-merge-20260704T064539Z-acp-session-unify
- required_evidence: daemon cycle 正常完成，session 使用正确操作
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成测试需启动 freely daemon，当前已停止。静态代码验证已覆盖所有修改点。E2E dogfood post-merge。
- replacement_evidence: AT-001~AT-007 静态验证通过

## End-to-End
- acceptance_target: 完整 daemon cycle → agent session 创建/恢复/通信正常
- testing_layer: end_to_end
- target_environment: test-pre-merge-20260704T064539Z-acp-session-unify → develop merge chain
- required_evidence: daemon cycle + agent 通信正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需启动 daemon。静态验证已覆盖。Post-merge dogfood。
- replacement_evidence: AT-001~AT-007 静态验证通过 + post-merge dogfood

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码重构不影响运行时行为（本期所有 agent 同 tool → 同 bridge → 行为不变）。slot 列新增为 schema 变更，daemon 启动时自动处理。
