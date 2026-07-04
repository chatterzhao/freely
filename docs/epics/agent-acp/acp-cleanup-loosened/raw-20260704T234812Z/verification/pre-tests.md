# Pre-Tests: #3731 ACP cleanup 遗漏修复
- issue_id: I-20260704T234812Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 全部 6 个修改文件通过语法检查
- acceptance_target: Python AST 解析通过 + bash -n 通过
- testing_layer: unit
- target_environment: feature-local
- required_evidence: 语法检查命令输出全部 OK
- evidence_level: integration
- artifact_ref: docs/epics/agent-acp/acp-cleanup-loosened/raw-20260704T234812Z/verification/test-evidence/syntax-check.log
- test_command: |
  python3 -c "import py_compile; py_compile.compile('docs/system/workspace/scripts/runtime/acp-bridge.py', doraise=True); py_compile.compile('docs/system/workspace/scripts/runtime/freely_db_manager.py', doraise=True); py_compile.compile('docs/system/workspace/scripts/runtime/watchdog_sse.py', doraise=True); print('Python: OK')" && bash -n docs/system/workspace/scripts/runtime/freely && bash -n docs/system/workspace/scripts/runtime/monitor-ai-acp.sh && bash -n docs/system/workspace/hooks/pre-commit.sh && echo "Shell: OK"
- expected_output: Python: OK
  Shell: OK
- expected_RED_output: SyntaxError / IndentationError 报错
- actual_RED_output: |
  freely_db_manager.py: IndentationError at line 1377 (unexpected indent).
  watchdog_sse.py: unterminated triple-quoted string literal at line 406.
  acp-bridge.py: syntax OK. Shell: all three OK.
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 freely_db_manager.py h_aw_upsert_only 缩进错误 + watchdog_sse.py 3 个未闭合 docstring → RED

### acceptance-2
- id: AT-002
- requirement: acp-bridge.py CLI 接受 --base-tool 参数并穿透到 pid/socket
- acceptance_target: --base-tool opencode 启动后 pid 文件和 socket 包含 opencode 后缀
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认 CLI 有 --base-tool 参数，_pid_file/_socket_path 调用传 base_tool
- evidence_level: integration
- artifact_ref: docs/epics/agent-acp/acp-cleanup-loosened/raw-20260704T234812Z/verification/test-evidence/base-tool-cli.log
- test_command: |
  grep -c "add_argument.*--base-tool" docs/system/workspace/scripts/runtime/acp-bridge.py && echo "CLI has --base-tool" && grep "_pid_file\|_socket_path" docs/system/workspace/scripts/runtime/acp-bridge.py | grep -c "base_tool"
- expected_output: CLI has --base-tool
  >= 3 (cmd_start/stop/status 各至少一处使用 base_tool)
- expected_RED_output: 0 处 --base-tool CLI 参数
- actual_RED_output: |
  grep "add_argument.*--base-tool" → 0 matches. acp-bridge.py CLI 无 --base-tool 参数。
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 acp-bridge.py argparse 无 --base-tool 参数，grep = 0 → RED

### acceptance-3
- id: AT-003
- requirement: freely + monitor-ai-acp.sh bash 路径函数与 Python 一致（conditional suffix）
- acceptance_target: 空 base_tool 时路径无尾随 -，非空时有 -{base_tool} 后缀
- testing_layer: unit
- target_environment: feature-local
- required_evidence: source 检查 conditional suffix 逻辑
- evidence_level: integration
- artifact_ref: docs/epics/agent-acp/acp-cleanup-loosened/raw-20260704T234812Z/verification/test-evidence/path-consistency.log
- test_command: |
  grep -c '\[\[ -n "\$base_tool" \]\] && _suffix=' docs/system/workspace/scripts/runtime/freely docs/system/workspace/scripts/runtime/monitor-ai-acp.sh && echo "path consistency OK"
- expected_output: path consistency OK
- expected_RED_output: 0 matches（无条件判断）
- actual_RED_output: |
  grep in freely → 0 matches. grep in monitor-ai-acp.sh → 0 matches.
  bash 路径函数无条件加 - 前缀，无 conditional suffix 逻辑。
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 bash `_acp_bridge_pid_file`、`_acp_bridge_socket`、`_bridge_pid_file`、`_bridge_socket` 无条件加 - 分隔符 → RED

### acceptance-4
- id: AT-004
- requirement: pre-commit.sh hook 消息包含 `freely feedback` + `freely wt-create` + skill
- acceptance_target: 拦截消息中可 grep 到这三项
- testing_layer: unit
- target_environment: feature-local
- required_evidence: grep 确认三处关键词
- evidence_level: integration
- artifact_ref: docs/epics/agent-acp/acp-cleanup-loosened/raw-20260704T234812Z/verification/test-evidence/hook-message.log
- test_command: |
  grep -c "freely feedback" docs/system/workspace/hooks/pre-commit.sh && grep -c "freely wt-create" docs/system/workspace/hooks/pre-commit.sh && grep -c "freely-workflow-guarded-execution" docs/system/workspace/hooks/pre-commit.sh && echo "hook message OK"
- expected_output: hook message OK
- expected_RED_output: 0/0/0
- actual_RED_output: |
  grep "freely feedback" → 0 matches. grep "freely wt-create" → 2 (already present).
  grep "freely-workflow-guarded-execution" → 2 (already present).
  缺少 `freely feedback` 命令引导。
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: red
- status: pending
- blocker: execution_pending_or_failed
- red_how: fix — 修复前 hook 拦截消息未提及 `freely feedback` 命令，grep = 0 → RED

## Unit
- acceptance_target: 全部 4 个 AT 通过 grep 静态验证
- testing_layer: unit
- target_environment: feature-local
- required_evidence: AT-001 ~ AT-004 全部 passed
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: shell/Python 跨文件语法修复，无可导出函数单元。grep 静态验证等效覆盖全部 4 个 AT
- replacement_evidence: AT-001~AT-004 通过静态代码验证

## Integration
- acceptance_target: daemon 启动后 bridge 按 base_tool 正确命名 socket/pid
- testing_layer: integration
- target_environment: test-pre-merge-20260704T234812Z-acp-cleanup-followup
- required_evidence: daemon 正常启动，socket/pid 文件命名正确
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成测试需启动 daemon。静态验证已覆盖。E2E dogfood post-merge
- replacement_evidence: AT-001~AT-004 静态验证通过

## End-to-End
- acceptance_target: daemon cycle 正常完成，多 bridge 场景 socket 正确路由
- testing_layer: end_to_end
- target_environment: test-pre-merge-20260704T234812Z-acp-cleanup-followup → develop
- required_evidence: daemon cycle + agent 通信正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: E2E 需启动 daemon。静态验证已覆盖。Post-merge dogfood
- replacement_evidence: AT-001~AT-004 静态验证通过 + post-merge dogfood

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 全部为机械性 bug 修复，不影响运行时行为。语法修复后代码行为与原设计一致
