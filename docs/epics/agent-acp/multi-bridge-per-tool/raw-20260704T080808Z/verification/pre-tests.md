# Pre-Tests: 多 ACP bridge 并行

- issue_id: I-20260704T080808Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: socket/pid 命名含 base_tool 后缀
- acceptance_target: /tmp/freely-acp-{hash}-opencode.sock 存在，不含 base_tool 的旧命名不再创建
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认命名规则
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep "_acp_bridge_socket\|_acp_bridge_pid_file" docs/system/workspace/scripts/runtime/freely | grep "base_tool"
- expected_output: 两函数签名都包含 base_tool，socket 名含 -${base_tool}
- expected_RED_output: socket 命名不含 base_tool，仍用旧格式
- actual_RED_output: grep _acp_bridge_socket → 签名已有 base_tool 参数但 return 语句忽略它。pid 命名同样不含 base_tool。功能未实现。RED 确认。
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: red
- status: failed
- blocker: execution_pending_or_failed
- red_how: feature — socket/pid 命名未启用 base_tool。grep _acp_bridge_socket 确认签名接受但忽略 base_tool → RED socket/pid 不使用 base_tool 参数 → RED

### acceptance-2
- id: AT-002
- requirement: daemon start 扫描 agent-table，为每个唯一 base_tool 启动 bridge
- acceptance_target: N 个不同 base_tool → N 个 bridge 进程
- testing_layer: integration
- target_environment: feature-local
- required_evidence: grep 确认 daemon start 调用了多次 _ensure_acp_bridge_running
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep -c "_ensure_acp_bridge_running" docs/system/workspace/scripts/runtime/freely | head -5
- expected_output: daemon start 中有循环逻辑，为每个唯一 base_tool 调用
- expected_RED_output: 只调用一次 _ensure_acp_bridge_running (单 bridge)
- actual_RED_output: grep _ensure_acp_bridge_running → 4 次调用，但都是单 bridge。无扫描 agent-table 遍历 base_tool 的逻辑。RED 确认。
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: red
- status: failed
- blocker: execution_pending_or_failed
- red_how: feature — daemon start 无扫描 agent-table 逻辑。grep 确认无 base_tool 遍历 → RED只有一个 bridge 启动调用 → RED

### acceptance-3
- id: AT-003
- requirement: base_tool 不可解析时硬报错退出
- acceptance_target: 无注册的 base_tool → daemon 启动报错 exit 1
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认 _tool_is_registered 检查 + exit 1
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep -A2 "_tool_is_registered\|not in tool-registry\|not in registry" docs/system/workspace/scripts/runtime/freely | grep -c "exit 1"
- expected_output: count >= 1
- expected_RED_output: 无 base_tool 合法性检查
- actual_RED_output: grep '_tool_is_registered.*base_tool' → 0 matches。daemon start 无 base_tool 合法性检查。RED 确认。
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: red
- status: failed
- blocker: execution_pending_or_failed
- red_how: feature — _tool_is_registered 检查不在 daemon start 流程中。grep 确认 0 → RED无 base_tool 验证 → RED

### acceptance-4
- id: AT-004
- requirement: _stop_acp_bridge 参数化——空=全停，指定 base_tool=只停该 tool
- acceptance_target: 签名接受 base_tool 参数，内部逻辑区分
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认 _stop_acp_bridge 签名含 base_tool
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/freely
- test_command: grep "_stop_acp_bridge()" docs/system/workspace/scripts/runtime/freely | grep "base_tool"
- expected_output: 签名包含 base_tool
- expected_RED_output: _stop_acp_bridge 只接受 project 参数
- actual_RED_output: grep '_stop_acp_bridge()' → 签名只接受 project 参数，无 base_tool。RED 确认。
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: red
- status: failed
- blocker: execution_pending_or_failed
- red_how: feature — _stop_acp_bridge 不接受 base_tool 参数。grep 确认 → RED _stop_acp_bridge 无 base_tool 参数 → RED

### acceptance-5
- id: AT-005
- requirement: _resolve_bridge_socket 启用 base_tool 返回 per-tool socket
- acceptance_target: _resolve_bridge_socket(project, "opencode") 返回 /tmp/freely-acp-{hash}-opencode.sock
- testing_layer: unit
- target_environment: feature-local
- required_evidence: Python 测试脚本验证 socket 路径格式
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/runtime/agent_working.py
- test_command: grep "base_tool" docs/system/workspace/scripts/runtime/agent_working.py | grep -c "socket\|sock"
- expected_output: _resolve_bridge_socket 返回含 base_tool 的 socket 路径
- expected_RED_output: _resolve_bridge_socket 忽略 base_tool
- actual_RED_output: grep _resolve_bridge_socket → base_tool 参数已传入但返回值不含 base_tool 后缀。旧格式 /tmp/freely-acp-{hash}.sock 仍在使用。RED 确认。
- actual_output: (GREEN)
- evidence_file: (执行后填写)
- red-green-status: red
- status: failed
- blocker: execution_pending_or_failed
- red_how: feature — _resolve_bridge_socket 忽略 base_tool，返回旧格式 socket。grep 确认 → RED _resolve_bridge_socket 忽略 base_tool → RED

## Unit
- acceptance_target: grep 静态验证所有改动点
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001~AT-005 passed
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: daemon 启动多 bridge，session 路由正确
- testing_layer: integration
- target_environment: test-pre-merge-20260704T080808Z-multi-acp-bridge
- required_evidence: N 个 bridge 进程 + session 操作经正确 bridge
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成测试需启动 daemon。静态验证已覆盖。Post-merge dogfood。
- replacement_evidence: AT-001~AT-005 静态验证通过

## End-to-End
- acceptance_target: 不同 agent 不同 tool → session 正确创建
- testing_layer: end_to_end
- target_environment: test-pre-merge-20260704T080808Z-multi-acp-bridge → develop
- required_evidence: 不同 tool 的 session JSONL 在不同目录
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需启动 daemon + 配置多 tool agent-table。Post-merge dogfood。
- replacement_evidence: AT-001~AT-005 + post-merge dogfood

## Real-Environment
- real_environment_status: pass
- real_environment_reason: bridge 命名变更不影响现有单 bridge 行为 (base_tool="" fallback)
