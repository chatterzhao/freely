# Pre-Tests: watchdog_sse 路由死定义搬移
- issue_id: I-20260717T084757Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: main 后无被引用 def + 日志时间戳（AC1）
- acceptance_target: AST 断言 referenced_dead 为空且 timestamped=True
- testing_layer: unit
- target_environment: fix/raw-20260717T084757Z-sse-routing-dead-def
- required_evidence: harness 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/harness/at001-ast-order.sh
- expected_output: "AT-001 PASS"
- expected_RED_output: "referenced_dead=['_get_agent_slot'] → AT-001 FAIL"
- actual_RED_output: defs_after_main=['_get_agent_slot'] referenced_dead=['_get_agent_slot'] timestamped=False → AT-001 FAIL
- actual_output: defs_after_main=[] referenced_dead=[] timestamped=True → AT-001 PASS
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现状 def 在 main 后且无时间戳,AST 必列 referenced_dead

### acceptance-2
- id: AT-002
- requirement: 阻塞点前定义（AC2）
- acceptance_target: __main__ 语义逐节点执行,watchdog_run 阻塞前 _get_agent_slot 已在命名空间
- testing_layer: integration
- target_environment: fix/raw-20260717T084757Z-sse-routing-dead-def
- required_evidence: harness 输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/harness/at002-exec-order.sh
- expected_output: "AT-002 PASS"
- expected_RED_output: "defined_before_block=False → AT-002 FAIL"
- actual_RED_output: defined_before_block=False → AT-002 FAIL（忠实模拟阻塞点,def 不可达）
- actual_output: defined_before_block=True → AT-002 PASS
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 忠实模拟 watchdog_run 永不返回,现状 def 不可达必 FAIL

### acceptance-3
- id: AT-003
- requirement: E2E 路由无 NameError（AC3）
- acceptance_target: 真实 daemon + chat 注入触发路由,watchdog 日志 0 NameError 且有 routing 行
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T084757Z-sse-routing-dead-def
- required_evidence: harness observed 行
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/harness/at003-e2e-route.sh
- expected_output: "AT-003 PASS"
- expected_RED_output: "nameerror>=1（生产 2026-07-17 实抓同款）"
- actual_RED_output: observed: nameerror=1 routes_logged=1 → AT-003 FAIL（A2A input-required 注入确定性触发,与生产同款 NameError 实抓）
- actual_output: observed: nameerror=0 routes_logged=1 → AT-003 PASS（对照 RED: nameerror=1）
- evidence_file: docs/B2-docs/runtime/sse-watchdog/raw-20260717T084757Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — chat 注入确定性触发 manager 路由,现状必 NameError（生产日志已实抓同款）

## Unit
- acceptance_target: AST 断言
- testing_layer: unit
- target_environment: fix/raw-20260717T084757Z-sse-routing-dead-def
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## Integration
- acceptance_target: __main__ 语义沙箱
- testing_layer: integration
- target_environment: fix/raw-20260717T084757Z-sse-routing-dead-def
- required_evidence: AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002

## End-to-End
- acceptance_target: 真实路由触发
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T084757Z-sse-routing-dead-def → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 真实 daemon + A2A input-required 注入:路由完成零 NameError（RED 同法 nameerror=1 对照）
