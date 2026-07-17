# Pre-Tests: acp_bridge pid 族 per-tool 收口
- issue_id: I-20260717T060903Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 逐文件枚举清死不伤活（AC1/AC2）
- acceptance_target: 沙箱一死一活两组文件,self-heal 后死组 4 文件全清、活组 4 文件完好
- testing_layer: integration
- target_environment: fix/raw-20260717T060903Z-bridge-pidfamily-pertool
- required_evidence: harness observed 行 + PASS
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/harness/at001-pertool-selfheal.sh
- expected_output: "AT-001 PASS: 清死不伤活"
- expected_RED_output: "AT-001 FAIL: per-tool self-heal 函数不存在"
- actual_RED_output: AT-001 FAIL: per-tool self-heal 函数不存在
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 现无逐文件枚举函数,harness 必 FAIL

### acceptance-2
- id: AT-002
- requirement: 真实 daemon 下 self-heal 生效且免伤（AC3）
- acceptance_target: dead 别名文件被清、活 claude bridge 文件/进程完好、无重生 spawn
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T060903Z-bridge-pidfamily-pertool
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/harness/at002-live-daemon-selfheal.sh
- expected_output: "AT-002 PASS: 清死不伤活且无重生"
- expected_RED_output: "AT-002 FAIL: dead_left>=1（glob 多行展开使 self-heal 静默失效,dead 文件残留）"
- actual_RED_output: observed: dead_left=2 live_ok=1 respawns=0 → AT-002 FAIL（dead pid+sock 残留=self-heal 静默失效实证；活 bridge 未受伤系缺陷1使广播分支未达）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T060903Z/verification/test-evidence/acceptance-2.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 现状 runtime_pid_file_for_role 对多文件 glob 展开多行,self-heal cat/rm 静默失败,dead 文件必残留

## Unit
- acceptance_target: 无独立单元面（函数行为面由 AT-001 沙箱覆盖）
- testing_layer: unit
- target_environment: fix/raw-20260717T060903Z-bridge-pidfamily-pertool
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 新函数为 IO 行为体,AT-001 沙箱即最小行为面
- replacement_evidence: AT-001 observed 输出

## Integration
- acceptance_target: 沙箱一死一活矩阵
- testing_layer: integration
- target_environment: fix/raw-20260717T060903Z-bridge-pidfamily-pertool
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## End-to-End
- acceptance_target: 真实 daemon self-heal 免伤
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T060903Z-bridge-pidfamily-pertool → develop merge chain
- required_evidence: AT-002 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-002

## Real-Environment
- real_environment_status: fail
- real_environment_reason: pending — GREEN 阶段执行 AT-002 后更新
