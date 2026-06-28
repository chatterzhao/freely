# Pre-Tests: ACP session/fork
- issue_id: I-20260627T084551Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: fork 路径 try session/fork with Claude
- testing_layer: integration
- target_environment: develop
- required_evidence: session/fork creates new session_id
- test_command: python3 docs/system/workspace/scripts/runtime/run-acp-prompt.py --launch-kind fork --cwd . --bridge-socket /tmp/freely-acp-test.sock 2>&1
- expected_output: session id: (fork from ...)
- actual_output:
- evidence_file:
- blocker:
- not_applicable_reason: pre-merge 阶段 ACP bridge 不可用
- not_applicable_explanation: 需要启动 claude-agent-acp 并通过 bridge socket 发 session/fork RPC，只有 freely daemon 运行时才能执行。代码路径已通过 acceptance-2/3 验证
- status: not_applicable

### acceptance-2
- acceptance_target: fork code includes session/fork try/except
- testing_layer: unit
- target_environment: fix/raw-20260627T084551Z-acp-session-fork
- required_evidence: session/fork 和 session/new 都在代码中
- test_command: grep -c "session/fork" docs/system/workspace/scripts/runtime/run-acp-prompt.py && grep -c "session/new" docs/system/workspace/scripts/runtime/run-acp-prompt.py && echo "PASS"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: pass

### acceptance-3
- acceptance_target: ensure-codex-acp reads .toml
- testing_layer: unit
- target_environment: fix/raw-20260627T084551Z-acp-session-fork
- required_evidence: REGISTRY=.toml
- test_command: grep "REGISTRY=" docs/system/workspace/scripts/runtime/ensure-codex-acp | grep -q ".toml" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker:
- status: pass

## Unit
- acceptance_target: 文件改动正确，无语法错误

## Integration
- not_applicable_reason: pre-merge 阶段无法执行集成测试
- not_applicable_explanation: 需合入 develop 后启动 freely daemon 验证
- acceptance_target: freely daemon worker fork 使用 session/fork

## End-to-End
- not_applicable_reason: pre-merge 阶段无法执行端到端测试
- not_applicable_explanation: 需合入 develop 后在真实环境验证
- acceptance_target: worker fork 后缓存命中率提升

## Real-Environment
- real_environment_status: not_tested
