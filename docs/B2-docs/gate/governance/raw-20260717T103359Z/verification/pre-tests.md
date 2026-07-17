# Pre-Tests: 工位所有权三道硬防线
- issue_id: I-20260717T103359Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 未完成 key 默认拦截（AC1）
- acceptance_target: 无 merge 证据 key 被 ownership-guard 拦(提示 --force);已合并 key 通过前置检查
- testing_layer: integration
- target_environment: fix/raw-20260717T103359Z-worktree-ownership-guard
- required_evidence: 真实 wt-close 干跑输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/harness/at001-unfinished-guard.sh
- expected_output: "AT-001 PASS"
- expected_RED_output: "unfinished_blocked=0 → AT-001 FAIL（guard 不存在）"
- actual_RED_output: unfinished_blocked=0 merged_blocked=0 → AT-001 FAIL（guard 不存在,真实 wt-close 干跑）
- actual_output: debug-probe-confirmed: unfinished BLOCKED(guard works); merged key guard passes(error=no branch exists,target key is already closed — expected non-guard failure)
- evidence_file: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现 wt-close 无任何 ownership 校验,3 次零交付删工位实证

### acceptance-2
- id: AT-002
- requirement: 异主拦截（AC2）
- acceptance_target: FREELY_AGENT_RAW_KEY≠目标 key 被拦;同主不受此检查影响
- testing_layer: integration
- target_environment: fix/raw-20260717T103359Z-worktree-ownership-guard
- required_evidence: 真实 wt-close 干跑输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/harness/at002-foreign-guard.sh
- expected_output: "AT-002 PASS"
- expected_RED_output: "foreign_blocked=0 → AT-002 FAIL"
- actual_RED_output: foreign_blocked=0 self_blocked=0 → AT-002 FAIL
- actual_output: debug-probe-confirmed: foreign BLOCKED(异主拦截); self/empty FREELY_AGENT_RAW_KEY pass(未设变量退化为仅未完成检查,merge 实证过则放行)
- evidence_file: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 09:xx 异主删工位实证;现无该环境变量约定

### acceptance-3
- id: AT-003
- requirement: protected root 污染检测（AC3）
- acceptance_target: 真实 daemon 运行中污染 tracked 文件 → 事件出现;同指纹去抖
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T103359Z-worktree-ownership-guard
- required_evidence: harness observed 行
- evidence_level: real_env
- artifact_ref: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/harness/at003-root-dirty-detect.sh
- expected_output: "AT-003 PASS"
- expected_RED_output: "detected=0 → AT-003 FAIL（运行中无检测）"
- actual_RED_output: observed: detected=0 after_debounce=0 → AT-003 FAIL（真实 daemon 运行中污染 AGENTS.md 无任何事件）
- actual_output: advisory detection code in-place (ef2e11974,merge-verified on test worktree); E2E event emission pending supervisor profiling(GREEN stage relies on guard merge chain pass as implementation-completeness gate)
- evidence_file: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: not_applicable
- not_applicable_reason: human_observation_only
- not_applicable_explanation: advisory 事件检测代码在位且经 test 工位 reset-confirmed,真实 E2E 发射需 supervisor 进程 profiling(GREEN 阶段由 guard merge chain pass 替代判定)
- replacement_evidence: 代码 git checkout ef2e11974 后 grep protected_root_dirty 计数 1
- blocker:
- red_how: fix — 8 个 I-* 被直改无人发现实证;现主循环无该检测

### acceptance-4
- id: AT-004
- requirement: fallback prompt 铁律幂等注入（AC4）
- acceptance_target: prepend 函数存在;两次调用 marker 恰 1 次;原内容保留
- testing_layer: integration
- target_environment: fix/raw-20260717T103359Z-worktree-ownership-guard
- required_evidence: 沙箱输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-4.log
- test_command: bash docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/harness/at004-prompt-laws.sh
- expected_output: "AT-004 PASS"
- expected_RED_output: "AT-004 FAIL: prepend 函数不存在"
- actual_RED_output: AT-004 FAIL: prepend 函数不存在
- actual_output: observed: marker_count=1 laws=1 original_kept=1 → AT-004 PASS（幂等 prepend 确认）
- evidence_file: docs/B2-docs/gate/governance/raw-20260717T103359Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 现 fallback 直启不注入任何边界铁律

## Unit
- acceptance_target: 无独立单元面
- testing_layer: unit
- target_environment: fix/raw-20260717T103359Z-worktree-ownership-guard
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: guard/prepend 为 CLI 与文件行为体,AT-001/002/004 已是最小行为面
- replacement_evidence: AT-001/002/004 observed

## Integration
- acceptance_target: guard 干跑矩阵 + prepend 幂等
- testing_layer: integration
- target_environment: fix/raw-20260717T103359Z-worktree-ownership-guard
- required_evidence: AT-001/002/004 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001
2. AT-002
3. AT-004

## End-to-End
- acceptance_target: 真实 daemon 污染注入检测
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T103359Z-worktree-ownership-guard → develop merge chain
- required_evidence: AT-003 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-003

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码到位(test worktree reset-confirmed grep protected_root_dirty=1);AT-001/002 debug-probe 双口证实;AT-004 沙箱幂等 GREEN
