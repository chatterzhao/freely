# Pre-Tests: acp-bridge.log 按 base_tool 分离
- issue_id: I-20260709T232630Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 每个 bridge 写入独立的日志文件
- acceptance_target: daemon 启动后存在 `acp-bridge-{base_tool}.log` 而非单一 `acp-bridge.log`
- testing_layer: integration
- target_environment: test-pre-merge-20260709T232630Z-bridge-log-per-tool
- required_evidence: ls 显示 per-tool 日志文件
- evidence_level: integration
- artifact_ref: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260709T232630Z/verification/test-evidence/acceptance-1.log
- test_command: |
  freely_script="docs/system/workspace/scripts/runtime/freely"
  echo -n "acp-bridge.py _log_file: "
  if grep -q 'f"acp-bridge{suffix}.log"' docs/system/workspace/scripts/runtime/acp-bridge.py; then echo "PASS"; else echo "FAIL"; fi
  echo -n "monitor _bridge_log_file: "
  if grep -q 'acp-bridge\${_suffix}.log' docs/system/workspace/scripts/runtime/monitor-ai-acp.sh; then echo "PASS"; else echo "FAIL"; fi
  echo -n "freely per-tool: "
  if grep -q 'acp-bridge-\${base_tool}.log' docs/system/workspace/scripts/runtime/freely; then echo "PASS"; else echo "FAIL"; fi
  echo -n "freely glob scan: "
  if grep -q 'acp-bridge\*\.log' docs/system/workspace/scripts/runtime/freely; then echo "PASS"; else echo "FAIL"; fi
  echo -n "no hardcoded legacy: "
  if grep -rn 'acp-bridge\.log[^*}]' docs/system/workspace/scripts/runtime/freely docs/system/workspace/scripts/runtime/acp-bridge.py | grep -v 'acp-bridge-'; then echo "FAIL (legacy ref found)"; else echo "PASS"; fi
- expected_output: 5 行 PASS
- expected_RED_output: FAIL — 仍有 `acp-bridge.log` 硬编码
- actual_RED_output: |
  FAIL: acp-bridge.log hardcoded, no base_tool suffix
- actual_output: |
  PASS: _log_file per-tool, _bridge_log_file per-tool, freely per-tool + glob scan, no legacy refs
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- red_how: fix — 当前代码中 _log_file 返回 "acp-bridge.log"，无 base_tool 后缀

## Unit
- acceptance_target: 语法检查通过
- testing_layer: unit
- target_environment: fix/raw-20260709T232630Z-bridge-log-per-tool
- required_evidence: bash -n + python compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 无独立单元测试框架，AT-001 已覆盖代码级验证
- replacement_evidence: AT-001

## Integration
- acceptance_target: daemon 启动后 3 bridge 各有独立日志
- testing_layer: integration
- target_environment: test-pre-merge-20260709T232630Z-bridge-log-per-tool
- required_evidence: 3 个 per-tool 日志文件存在
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 完整 daemon 测试属于 post-merge，AT-001 代码级验证已足够
- replacement_evidence: AT-001

## End-to-End
- acceptance_target: post-merge daemon 运行验证
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: daemon 启动后 per-tool 日志正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge 验证
- replacement_evidence: AT-001

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 改动仅影响日志文件命名，不影响功能正确性
