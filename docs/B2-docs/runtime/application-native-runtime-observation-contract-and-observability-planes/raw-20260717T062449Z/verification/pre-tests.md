# Pre-Tests: trace 打点拆相
- issue_id: I-20260717T062449Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: L041 实时化 + L042 OUT 单值（AC1/AC2）
- acceptance_target: auto 周期中 launch_observed 与 launch_begin 时差 ≤10s；最新 L042 OUT to 为单值
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T062449Z-trace-gaps-l041-l042-l090
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/harness/at001-auto-cycle-trace.sh
- expected_output: "AT-001 PASS"
- expected_RED_output: "AT-001 FAIL（l041_delta 数十秒级或缺失; l042_out 含候选集竖线）"
- actual_RED_output: observed: l041_delta=269s l042_out='to=A-L020|A-L090|...' → AT-001 FAIL（时差 269s + 候选集实抓）
- actual_output: observed: l041_delta=1s l042_out='to=A-L020' → AT-001 PASS（对照 RED: 269s/候选集）
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现状 L041 于 post-cycle 发出(2026-07-16 实测晚 94s)、L042 expected_next 为候选集,真实 auto 周期即复现

### acceptance-2
- id: AT-002
- requirement: cleanup 链出口声明（AC3）
- acceptance_target: stop 场景 L090/L092 OUT ok=1 且 to 单值
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T062449Z-trace-gaps-l041-l042-l090
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/harness/at002-cleanup-chain.sh
- expected_output: "AT-002 PASS"
- expected_RED_output: "AT-002 FAIL（to=UNSET ok=0）"
- actual_RED_output: L090/L092 OUT 均 to=UNSET ok=0（stop 场景实抓 seq=6/8）→ AT-002 FAIL
- actual_output: L090 OUT to=A-L092 ok=1；L092 OUT to=TERM ok=1 → AT-002 PASS（对照 RED: 双 UNSET）
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现状 cleanup 链恒 to=UNSET ok=0（今日 trace 全量可证）,stop 场景即复现

### acceptance-3
- id: AT-003
- requirement: 契约 §12 同步（AC4）
- acceptance_target: §12 中 L041/L042/L090 三条目标记 resolved 且含 L042 接力语义修订
- testing_layer: unit
- target_environment: fix/raw-20260717T062449Z-trace-gaps-l041-l042-l090
- required_evidence: 文本断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-3.log
- test_command: |
  D=docs/system/workspace/three-loop-trace-contract.md
  R=$(grep -c "resolved (raw-20260717T062449Z" "$D" || true)
  S=$(grep -c "接力型下游由.*fr=L042\|fr=A-L042 的 IN" "$D" || true)
  echo "resolved_entries=$R semantics_note=$S"
  if [ "$R" -ge 3 ] && [ "$S" -ge 1 ]; then echo "AT-003 PASS"; else echo "AT-003 FAIL"; fi
- expected_output: "AT-003 PASS"
- expected_RED_output: "AT-003 FAIL（resolved_entries=0）"
- actual_RED_output: resolved_entries=0 semantics_note=0 → AT-003 FAIL
- actual_output: resolved_entries=3 semantics_note=1 → AT-003 PASS
- evidence_file: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — §12 现三条目均 open,断言必 FAIL

## Unit
- acceptance_target: 契约文本断言
- testing_layer: unit
- target_environment: fix/raw-20260717T062449Z-trace-gaps-l041-l042-l090
- required_evidence: AT-003 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Integration
- acceptance_target: 打点行为由 E2E 全链覆盖
- testing_layer: integration
- target_environment: test-pre-merge-20260717T062449Z-trace-gaps-l041-l042-l090
- required_evidence: AT-001/002 的 trace 行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 打点正确性只能在真实 supervisor 生命周期中判定,E2E 即最小真实面
- replacement_evidence: AT-001/AT-002 observed 行

## End-to-End
- acceptance_target: auto 周期与 stop 场景双面
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T062449Z-trace-gaps-l041-l042-l090 → develop merge chain
- required_evidence: AT-001/AT-002 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-001
2. AT-002

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 真实 auto 周期(l041_delta=1s,to=A-L020)与真实 stop 场景(L090→L092→TERM ok=1)双面通过
