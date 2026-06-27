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
- status: pass

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
