# Pre-Tests: 监督面观测真源对齐
- issue_id: I-20260717T004752Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: trace §11 覆盖全部实际打点（AC1）
- acceptance_target: runtime append_lifecycle_trace 打出的每个 L 编号都能在 trace-contract 查到
- testing_layer: integration
- target_environment: fix/raw-20260717T004752Z-supervision-docs-truth-align
- required_evidence: 提取对照脚本输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/harness/at001-trace-registry-diff.sh
- expected_output: "AT-001 PASS"
- expected_RED_output: "AT-001 FAIL: 未注册 checkpoint: L090 L091 L092 L201 L202 ..."
- actual_RED_output: AT-001 FAIL: 未注册 checkpoint: L091 L092 L202 L211 L212 L225 L231 L232 L332 L333 L334 L335 L336
- actual_output: AT-001 PASS: 全部 29 个 checkpoint 已注册
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — §11 现只注册 9 个 checkpoint，脚本对照必列出缺失清单

### acceptance-2
- id: AT-002
- requirement: heartbeat/bridge/task_mode/storm 文档锚点在位（AC2/3/4）
- acceptance_target: capability-lifecycle 与 watchdog SKILL 含关键机制锚点
- testing_layer: unit
- target_environment: fix/raw-20260717T004752Z-supervision-docs-truth-align
- required_evidence: 锚点 grep 组输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-2.log
- test_command: |
  CL=docs/system/workspace/three-loop-capability-lifecycle.md
  SK=docs/system/workspace/skills/freely-watchdog-control-plane/SKILL.md
  M=0
  grep -q "SUPERVISOR_HEARTBEAT_TIMEOUT_SECS" "$CL" || { echo "miss: heartbeat@CL"; M=1; }
  grep -q "SUPERVISOR_STARTUP_HEARTBEAT_GRACE_SECS" "$CL" || { echo "miss: 新生宽限@CL"; M=1; }
  grep -q "ACP_BRIDGE_WARMUP_GRACE_SECS" "$CL" || { echo "miss: warmup@CL"; M=1; }
  grep -qE "wait.*sleep.*continue|wait 模式.*跳过 prompt" "$CL" || { echo "miss: task_mode wait 语义@CL"; M=1; }
  grep -q "AI_MODE" "$CL" || { echo "miss: AI_MODE 区分@CL"; M=1; }
  grep -q "RESTART_STORM_WINDOW_SECS" "$SK" || { echo "miss: storm 阈值@SKILL"; M=1; }
  grep -q "supervisor-heartbeat" "$SK" || { echo "miss: heartbeat@SKILL"; M=1; }
  grep -q "LOOP_GUARD_L0" "$CL" || { echo "miss: Loop Guard@CL"; M=1; }
  [ "$M" -eq 0 ] && echo "AT-002 PASS: 全部锚点在位" || echo "AT-002 FAIL"
- expected_output: "AT-002 PASS: 全部锚点在位"
- expected_RED_output: "miss: heartbeat@CL ... AT-002 FAIL"
- actual_RED_output: 8 项锚点全缺(heartbeat/新生宽限/warmup/task_mode wait/AI_MODE/storm@SKILL/heartbeat@SKILL/LoopGuard) → AT-002 FAIL
- actual_output: AT-002 PASS: 全部锚点在位
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 审计确认全部锚点缺失，grep 组必 FAIL

### acceptance-3
- id: AT-003
- requirement: L240 缺口闭合（AC5）
- acceptance_target: 真实 daemon 启动的 trace 中 A-L240 OUT 带 to=A-L010 ok=1
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004752Z-supervision-docs-truth-align
- required_evidence: 真实 lifecycle-trace 行
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/harness/at003-l240-out.sh
- expected_output: "AT-003 PASS"
- expected_RED_output: "AT-003 FAIL: to/ok 仍为 UNSET/0"
- actual_RED_output: L240_OUT: seq=22 ph=OUT me=A-L240 to=UNSET ok=0 ...（kill -9 猝死触发 watchdog 重拉,实抓）→ AT-003 FAIL
- actual_output: L240_OUT: seq=28 ph=OUT me=A-L240 to=A-L010 ok=1 ...（kill -9 猝死→watchdog 重拉路径实抓）→ AT-003 PASS
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — L240 仅在 watchdog 重拉路径打点；harness 以 kill -9 猝死 supervisor 触发 ensure-manager 重拉复现（今日主仓 trace 中全部 L240 OUT 均 to=UNSET ok=0）

### acceptance-4
- id: AT-004
- requirement: AGENTS.md 幽灵命令纠错（AC6）
- acceptance_target: AGENTS.md 不再引用不存在的 pre-init-runtime；替代指引含 agent-table.toml
- testing_layer: unit
- target_environment: fix/raw-20260717T004752Z-supervision-docs-truth-align
- required_evidence: 断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-4.log
- test_command: |
  G=$(grep -c "pre-init-runtime" AGENTS.md || true)
  A=$(grep -c "agent-table.toml" AGENTS.md || true)
  echo "ghost_refs=$G agent_table_refs=$A"
  if [ "$G" -eq 0 ] && [ "$A" -ge 1 ]; then echo "AT-004 PASS"; else echo "AT-004 FAIL: ghost=$G table=$A"; fi
- expected_output: "AT-004 PASS"
- expected_RED_output: "AT-004 FAIL: ghost>=1"
- actual_RED_output: ghost_refs=1 agent_table_refs=0 → AT-004 FAIL
- actual_output: ghost_refs=0 agent_table_refs=1 → AT-004 PASS
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — AGENTS.md L98 现引用该幽灵命令（2026-07-16 test 工位实测 unknown command）

## Unit
- acceptance_target: 文档锚点与 AGENTS 断言
- testing_layer: unit
- target_environment: fix/raw-20260717T004752Z-supervision-docs-truth-align
- required_evidence: AT-002/AT-004 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002
2. AT-004

## Integration
- acceptance_target: trace 注册表与实际打点对照
- testing_layer: integration
- target_environment: fix/raw-20260717T004752Z-supervision-docs-truth-align
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## End-to-End
- acceptance_target: 真实 trace 中 L240 缺口闭合
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004752Z-supervision-docs-truth-align → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-003 在 test-pre-merge 真实 daemon 以 kill -9 猝死触发 watchdog 重拉,实抓 L240 OUT to=A-L010 ok=1
