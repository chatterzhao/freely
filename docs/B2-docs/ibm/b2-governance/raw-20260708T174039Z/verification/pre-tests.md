# Pre-Tests: tool-launchers socket path fix
- issue_id: I-20260708T174039Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: _bridge_socket 调用传入 base_tool 参数
- acceptance_target: tool_run_acp_from_prompt_file 中 _bridge_socket 调用格式为 _bridge_socket "$project" "$tool"
- testing_layer: integration
- target_environment: test-pre-merge-20260708T174039Z-tool-launchers-socket-path
- required_evidence: grep 确认代码行格式正确
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T174039Z/verification/test-evidence/acceptance-1.log
- test_command: grep -n '_bridge_socket "\$project" "\$tool"' docs/system/workspace/scripts/runtime/tool-launchers.sh
- expected_output: 第 823 行匹配
- expected_RED_output: 无匹配 — 当前代码无 "$tool" 参数
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前第 823 行只有 _bridge_socket "$project" 无 $tool

### acceptance-2
- id: AT-002
- requirement: socket 路径计算正确
- acceptance_target: 修改后 _bridge_socket 返回带 base_tool 后缀的路径
- testing_layer: unit
- target_environment: fix/raw-20260708T174039Z-tool-launchers-socket-path
- required_evidence: socket 路径以 -claude.sock 结尾
- evidence_level: integration
- artifact_ref: docs/B2-docs/ibm/b2-governance/raw-20260708T174039Z/verification/test-evidence/acceptance-2.log
- test_command: bash -c 'source docs/system/workspace/scripts/runtime/monitor-ai-acp.sh 2>/dev/null; result=$(_bridge_socket /Users/zhaoyu/Downloads/code/my-freely/freely claude); echo "$result"; echo "$result" | grep -q -- "-claude.sock" && echo "PASS" || echo "FAIL"'
- expected_output: path 以 -claude.sock 结尾 → PASS
- expected_RED_output: 修改前传空 base_tool → 路径无 -claude → FAIL
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- red_how: fix — 修改前路径为 /tmp/freely-acp-<hash>.sock，缺少 -claude

## Unit
- acceptance_target: _bridge_socket 函数在有/无 base_tool 参数时行为正确
- testing_layer: unit
- target_environment: fix/raw-20260708T174039Z-tool-launchers-socket-path
- required_evidence: 两种调用方式的差异验证
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 修改后 daemon AI session 能正常产出 cycle log
- testing_layer: integration
- target_environment: test-pre-merge-20260708T174039Z-tool-launchers-socket-path
- required_evidence: cycle log 文件非空，含 session UUID
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: develop → fix worktree → freely daemon start → AI session produces output
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260708T174039Z-tool-launchers-socket-path → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 手动测试验证：相同 claude-agent-acp + DeepSeek + 完整 prompt → AI 正常产出 526 chunks
