# Pre-Tests: sse pid 校验参数顺序修复
- issue_id: I-20260717T004721Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 函数签名对齐家族约定（AC1）
- acceptance_target: valid_sse_watchdog_pid_for_project 声明行为 local project="$1" pid="$2"
- testing_layer: unit
- target_environment: fix/raw-20260717T004721Z-sse-pid-arg-order
- required_evidence: 源码断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-1.log
- test_command: |
  BODY=$(awk '/^valid_sse_watchdog_pid_for_project\(\)/,/^}/' docs/system/workspace/scripts/runtime/freely)
  if printf '%s' "$BODY" | grep -q 'local project="\$1" pid="\$2"'; then echo "PASS: 签名已对齐"; else echo "FAIL: 签名仍反转"; fi
- expected_output: "PASS: 签名已对齐"
- expected_RED_output: "FAIL: 签名仍反转"
- actual_RED_output: FAIL: 签名仍反转
- actual_output: PASS: 签名已对齐
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前 L3570 为 local pid="$1" project="$2"，断言必 FAIL

### acceptance-2
- id: AT-002
- requirement: 活 sse-watchdog 判定 valid（AC2）
- acceptance_target: 对 argv 伪装的活装饰进程，valid_sse_watchdog_pid_for_project(project,pid) 返回 0
- testing_layer: integration
- target_environment: fix/raw-20260717T004721Z-sse-pid-arg-order
- required_evidence: 沙箱行为断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/harness/at002-valid-check-behavior.sh
- expected_output: "AT-002 PASS: 活 sse-watchdog 判定 valid"
- expected_RED_output: "AT-002 FAIL: 活 sse-watchdog 判定 invalid（参数反转）"
- actual_RED_output: AT-002 FAIL: 活 sse-watchdog 判定 invalid（参数反转）
- actual_output: AT-002 PASS: 活 sse-watchdog 判定 valid
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 反转签名下 kill -0 <项目路径> 恒失败，判定必 invalid

### acceptance-3
- id: AT-003
- requirement: 真实启动无 sse 误清（AC3）
- acceptance_target: daemon 启动 45s 窗口内 0 次 startup_self_heal_stale_pid_cleared role=sse_watchdog
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004721Z-sse-pid-arg-order
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/harness/at003-no-false-clear-e2e.sh
- expected_output: "AT-003 PASS: 无 sse 误清事件"
- expected_RED_output: "AT-003 FAIL: clears>=1（2026-07-17T02:23:45/47Z 生产复现同款事件）"
- actual_RED_output: 初版计数断言 clears=1（含合法死 pid 清除,断言精化为仅判活 pid）；精化后用修复前二进制重放：live_sse_pid=74868 false_clears=1 still_alive=1 → FAIL（活 pid 被误清,evidence: test-evidence/acceptance-3-red-replay.log）
- actual_output: observed: live_sse_pid=80970 false_clears=0 still_alive=1 pidfile_intact=1 → AT-003 PASS: 活 sse-watchdog 未被误清
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T004721Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前每个启动周期必现（lane A GREEN 运行日志中 02:23:45/47 仍各有一次），真实 daemon 启动即可复现

## Unit
- acceptance_target: 声明行源码断言
- testing_layer: unit
- target_environment: fix/raw-20260717T004721Z-sse-pid-arg-order
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001 签名断言

## Integration
- acceptance_target: 提取函数 + 活装饰进程行为验证
- testing_layer: integration
- target_environment: fix/raw-20260717T004721Z-sse-pid-arg-order
- required_evidence: AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002 行为断言

## End-to-End
- acceptance_target: 真实 daemon 启动周期无误清
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004721Z-sse-pid-arg-order → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003 E2E

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-003 在 test-pre-merge 工位真实 daemon 执行：修复前二进制重放活 pid 被误清（74868）,修复后活 pid（80970）经 live-status self-heal 触发无误清
