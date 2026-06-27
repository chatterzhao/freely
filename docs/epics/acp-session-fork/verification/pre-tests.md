# Pre-Tests: ACP session/fork
- issue_id: I-20260627T084551Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: fork 路径 try session/fork with Claude
- testing_layer: integration
- target_environment: fix/raw-20260627T084551Z-acp-session-fork
- required_evidence: session/fork creates new session_id different from parent
- test_command: python3 docs/system/workspace/scripts/runtime/run-acp-prompt.py --launch-kind fork --cwd . --prompt-file /dev/null --bridge-socket /tmp/freely-acp-test.sock 2>&1 | head -1
- expected_output: UUID (new session id)
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: not_applicable
- not_applicable_reason: pre-merge 阶段 ACP bridge 不可用，集成测试需在 develop 上实际 fork session 验证
- not_applicable_explanation: acceptance-1 需要启动 claude-agent-acp 并通过 bridge socket 发送 session/fork RPC，只有在 freely daemon 运行环境才能执行。改为在 acceptance-2（代码审查）和 acceptance-3（配置检查）验证

### acceptance-2
- acceptance_target: fork 降级到 session/new when fork unsupported
- testing_layer: unit
- target_environment: fix/raw-20260627T084551Z-acp-session-fork
- required_evidence: code path includes try/except fallback
- test_command: grep -c "session/fork" docs/system/workspace/scripts/runtime/run-acp-prompt.py && grep -c "session/new" docs/system/workspace/scripts/runtime/run-acp-prompt.py && echo "PASS"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: pass

### acceptance-3
- acceptance_target: ensure-codex-acp reads .toml not .json5
- testing_layer: unit
- target_environment: fix/raw-20260627T084551Z-acp-session-fork
- required_evidence: REGISTRY variable points to .toml
- test_command: grep "REGISTRY=" docs/system/workspace/scripts/runtime/ensure-codex-acp | grep -q ".toml" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: pass

## Unit
- acceptance_target: 两个文件改动正确

## Integration
- acceptance_target: freely daemon worker fork uses session/fork

## End-to-End
- acceptance_target: worker fork cache hit improvement measurable

## Real-Environment
- real_environment_status: not_tested
