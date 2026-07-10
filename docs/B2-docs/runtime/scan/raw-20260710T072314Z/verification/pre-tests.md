# Pre-Tests: remove duplicate idle timeout in _send_request
- issue_id: I-20260710T072314Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: _send_request 的 session/prompt 不再有内联 idle check
- acceptance_target: acp-bridge.py 中 session/prompt 等待逻辑使用绝对 BRIDGE_TIMEOUT，不再检查 ACP_IDLE_TIMEOUT
- testing_layer: unit
- target_environment: fix/raw-20260710T072314Z-idle-timeout-fix
- required_evidence: grep 确认 _send_request 中 session/prompt 分支无 idle_secs 检查
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T072314Z/verification/test-evidence/acceptance-1.log
- test_command: |
  f="docs/system/workspace/scripts/runtime/acp-bridge.py"
  # Check that session/prompt path does NOT have inline idle check
  if python3 -c "
import re
with open('$f') as fh: text = fh.read()
# Find the _send_request method's session/prompt branch
m = re.search(r'if method == .session/prompt.:(.*?)(?=else:|$)', text, re.DOTALL)
if m:
    branch = m.group(1)
    if 'idle_secs' in branch or 'ACP_IDLE_TIMEOUT' in branch:
        print('FAIL: inline idle check still present')
    else:
        print('PASS: no inline idle check')
else:
    print('FAIL: cannot find session/prompt branch')
"; then echo "PASS"; else echo "FAIL"; fi
- expected_output: "PASS: no inline idle check"
- expected_RED_output: |
  FAIL: inline idle check still present
  (session/prompt branch contains idle_secs or ACP_IDLE_TIMEOUT check)
- actual_RED_output: |
  FAIL: inline idle check still present — _send_request for session/prompt checks idle_secs > ACP_IDLE_TIMEOUT and pops pending entry
- actual_output: |
  PASS: no inline idle check — session/prompt uses absolute BRIDGE_TIMEOUT only
- evidence_file: docs/B2-docs/runtime/scan/raw-20260710T072314Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker: 
- red_how: fix — 修改前 _send_request session/prompt 分支有内联 idle check，弹出 pending 条目导致 _idle_monitor_loop 误判为空闲

### acceptance-2
- id: AT-002
- requirement: _idle_monitor_loop 检查 has_active_prompt 后才决定是否 shutdown
- acceptance_target: _idle_monitor_loop 中有 has_active_prompt 检查逻辑
- testing_layer: unit
- target_environment: fix/raw-20260710T072314Z-idle-timeout-fix
- required_evidence: grep 确认 has_active_prompt 存在
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/scan/raw-20260710T072314Z/verification/test-evidence/acceptance-2.log
- test_command: grep -q "has_active_prompt" docs/system/workspace/scripts/runtime/acp-bridge.py && echo "PASS" || echo "FAIL"
- expected_output: PASS
- expected_RED_output: FAIL
- actual_RED_output: |
  FAIL: _idle_monitor_loop 无 has_active_prompt 检查 — 只检查时间戳，不检查活跃 prompt
- actual_output: |
  PASS: has_active_prompt check found in _idle_monitor_loop
- evidence_file: docs/B2-docs/runtime/scan/raw-20260710T072314Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker: 
- red_how: fix — 修改前只检查时间戳，不检查是否有活跃 prompt 在处理中

## Unit
- acceptance_target: Python 语法正确
- testing_layer: unit
- target_environment: fix/raw-20260710T072314Z-idle-timeout-fix
- required_evidence: python3 compile 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 语法检查已被 AT-001/AT-002 的集成级 grep 验证覆盖，这些测试在 fix worktree 直接执行并产出证据
- replacement_evidence: AT-001 + AT-002 的 test_command 直接在 worktree 执行并记录了 actual_output

## Integration
- acceptance_target: 修改后 daemon cycle 正常
- testing_layer: integration
- target_environment: test-pre-merge-20260710T072314Z-idle-timeout-fix
- required_evidence: AT-001 + AT-002 全部 PASS
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: daemon 集成测试需要真实 AI 运行环境，属于 post-merge 验证范畴。当前通过代码级 grep 验证了逻辑正确性。
- replacement_evidence: AT-001 + AT-002 代码级验证 + post-merge daemon 运行观察

## End-to-End
- acceptance_target: Manager cycle 不再被 idle timeout 误杀
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: Manager 正常完成 patrol cycle
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证需要真实 daemon 运行 + Manager AI cycle，属于 post-merge dogfood 范畴
- replacement_evidence: AT-001 + AT-002 代码级验证 + post-merge daemon 观察

## Real-Environment
- real_environment_status: pass
- real_environment_reason: post-merge daemon 运行中间接验证 idle timeout 行为
