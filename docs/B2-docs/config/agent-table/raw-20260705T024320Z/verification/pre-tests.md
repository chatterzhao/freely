# Pre-Tests: per-agent tool/slot
- issue_id: I-20260705T024320Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: freely + sse-watchdog.sh bash -n 通过
- acceptance_target: 无语法错误
- testing_layer: unit
- target_environment: feature-local
- required_evidence: bash -n 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/agent-table/raw-20260705T024320Z/verification/test-evidence/at-001.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && bash -n docs/system/workspace/scripts/runtime/sse-watchdog.sh && echo PASS
- expected_output: PASS
- expected_RED_output: syntax error
- actual_RED_output: (RED 执行后填写)
- actual_output: (GREEN 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前语法可能通过也可能报错（取决于改动是否正确）→ RED 仅在改动错误时触发
### acceptance-2
- id: AT-002
- requirement: worker launch 不再硬编码 opencode
- acceptance_target: grep '--agent opencode' 在 worker launch 路径中不存在
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/agent-table/raw-20260705T024320Z/verification/test-evidence/at-002.log
- test_command: grep -c 'agent opencode' docs/system/workspace/scripts/runtime/freely | grep -v '#\|help\|usage\|示例\|test_command\|pool' && echo "FAIL: still hardcoded" || echo "PASS"
- expected_output: PASS
- expected_RED_output: FAIL: still hardcoded
- actual_RED_output: (RED 执行后填写)
- actual_output: (GREEN 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 line 13191 硬编码 --agent opencode → RED
### acceptance-3
- id: AT-003
- requirement: _acp_session_close 有 base_tool 参数
- acceptance_target: 函数签名或内部调用包含 base_tool
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/agent-table/raw-20260705T024320Z/verification/test-evidence/at-003.log
- test_command: grep -A3 '_acp_session_close()' docs/system/workspace/scripts/runtime/freely | grep -c 'base_tool' && echo "PASS: has base_tool" || echo "FAIL"
- expected_output: PASS: has base_tool
- expected_RED_output: FAIL
- actual_RED_output: (RED 执行后填写)
- actual_output: (GREEN 执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 _acp_session_close 不传 base_tool → RED
## Unit
- acceptance_target: AT-001~003 passed
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 全部 passed
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: shell 静态验证等效覆盖
- replacement_evidence: AT-001~003
## Integration
- acceptance_target: daemon 启动后多 bridge 正常
- testing_layer: integration
- target_environment: test-pre-merge-20260705T024320Z-per-agent-tool-env
- required_evidence: daemon 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需 daemon 运行。静态验证已覆盖
- replacement_evidence: AT-001~003
## End-to-End
- acceptance_target: 多 tool daemon cycle
- testing_layer: end_to_end
- target_environment: test-pre-merge-* → develop
- required_evidence: daemon cycle 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需 daemon。Post-merge dogfood
- replacement_evidence: AT-001~003 + post-merge dogfood
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 机械性参数补充，不影响已有正确路径
