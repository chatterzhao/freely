# Pre-Tests: bridge 生命周期三点收口
- issue_id: I-20260717T004654Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 孤儿回收 + 暖机宽限在位（AC1/AC2）
- acceptance_target: reuse fall-through 重生前 terminate 存活旧 pid；健康检查失败分支含 ACP_BRIDGE_WARMUP_GRACE_SECS 暖机复用
- testing_layer: unit
- target_environment: fix/raw-20260717T004654Z-bridge-orphan-leak
- required_evidence: 源码断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-1.log
- test_command: |
  BODY=$(awk '/^_ensure_acp_bridge_running\(\)/,/^  # ── Config.toml binary path lookup ──/' docs/system/workspace/scripts/runtime/freely)
  T1=0; printf '%s' "$BODY" | grep -q 'terminate_pid_with_graceful_wait "$pid"' && T1=1
  T2=0; printf '%s' "$BODY" | grep -q 'ACP_BRIDGE_WARMUP_GRACE_SECS' && T2=1
  echo "orphan_reap=$T1 warmup_grace=$T2"
  if [ "$T1" -eq 1 ] && [ "$T2" -eq 1 ]; then echo "PASS: 回收+暖机在位"; else echo "FAIL: reap=$T1 warmup=$T2"; fi
- expected_output: "PASS: 回收+暖机在位"
- expected_RED_output: "FAIL: reap=0 warmup=0"
- actual_RED_output: orphan_reap=0 warmup_grace=0 → FAIL
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 当前 fall-through 只 rm 文件不杀进程、无暖机宽限，断言必 FAIL

### acceptance-2
- id: AT-002
- requirement: lazy 守卫在位（AC3）
- acceptance_target: 主循环 per-cycle ensure 对非 manager 且无 pid 文件的工具 continue
- testing_layer: unit
- target_environment: fix/raw-20260717T004654Z-bridge-orphan-leak
- required_evidence: 源码断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-2.log
- test_command: |
  BLK=$(awk '/_cycle_tools=\(\)/,/^      done$/' docs/system/workspace/scripts/runtime/freely | head -40)
  G=0; printf '%s' "$BLK" | grep -q "lazy-start guard" && G=1
  echo "lazy_guard=$G"
  if [ "$G" -eq 1 ]; then echo "PASS: lazy 守卫在位"; else echo "FAIL: 无守卫,非 manager 工具被无条件 ensure"; fi
- expected_output: "PASS: lazy 守卫在位"
- expected_RED_output: "FAIL: 无守卫,非 manager 工具被无条件 ensure"
- actual_RED_output: lazy_guard=0 → FAIL: 无守卫
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-2.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 当前 cycle ensure 块无条件遍历三工具，断言必 FAIL

### acceptance-3
- id: AT-003
- requirement: E2E lazy + 无泄漏（AC4）
- acceptance_target: wait 模式 100s：acp_bridge_started ≤1、存活 bridge ≤1、opencode/cline 进程 0
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004654Z-bridge-orphan-leak
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/harness/at003-lazy-nolek-e2e.sh
- expected_output: "AT-003 PASS: lazy-start 生效且无泄漏"
- expected_RED_output: "AT-003 FAIL: spawns>=3（三工具 eager 启动，2026-07-17 每次启动实测 3-4 次 spawn 事件）"
- actual_RED_output: observed: bridge_spawn_events=19 live_bridges=19 opencode=6 cline=6 → AT-003 FAIL（单 supervisor 下 100s 泄漏 19 个 bridge,eager 启动 opencode/cline 各 6 个）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260717T004654Z/verification/test-evidence/acceptance-3.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 今日所有启动周期均实测 3-4 个 acp_bridge_started（claude+opencode+cline eager），真实 daemon 启动即复现

## Unit
- acceptance_target: 源码断言
- testing_layer: unit
- target_environment: fix/raw-20260717T004654Z-bridge-orphan-leak
- required_evidence: AT-001/AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001
2. AT-002

## Integration
- acceptance_target: 暖机/回收行为经 E2E 窗口整体验证（bridge 数有界即证明回收与宽限协同生效）
- testing_layer: integration
- target_environment: test-pre-merge-20260717T004654Z-bridge-orphan-leak
- required_evidence: AT-003 的 live_bridges/opencode/cline 计数
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 三点修复的集成效果（回收×宽限×守卫）在 AT-003 真实 daemon E2E 中以进程计数整体判定，单独集成沙箱需重造 registry/auth 依赖且真实度更低
- replacement_evidence: AT-003 harness 的 live_bridges/opencode/cline 观测值

## End-to-End
- acceptance_target: wait 模式真实 daemon 无 eager 启动无泄漏
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004654Z-bridge-orphan-leak → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Real-Environment
- real_environment_status: fail
- real_environment_reason: pending — GREEN 阶段执行 AT-003 后更新
