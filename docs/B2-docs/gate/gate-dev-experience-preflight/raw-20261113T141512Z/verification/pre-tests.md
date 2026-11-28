# Pre-Tests: status 只读视图空表降级
- issue_id: I-20261113T141512Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: status 只读视图在 agent_working 空表时 rc=0 且输出状态段
- acceptance_target: 目标 1-3
- testing_layer: integration
- target_environment: test-pre-merge-20261113T141512Z-status-readonly-semantics
- required_evidence: develop RED rc=1 → 工位 GREEN rc=0，逐断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-status-readonly-empty-agent.py
- expected_output: SUMMARY: 6 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 4 failed
- actual_RED_output: "SUMMARY: 2 ok, 4 failed（develop 基线 status rc=1）"
- actual_output: "SUMMARY: 6 ok, 0 failed（四个只读视图 rc=0）"
- evidence_file: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 基线执行 status --view live 得 rc=1；fix 后同命令 rc=0 并输出 project/branch 段。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### acceptance-2
- id: AT-002
- requirement: 写入路径仍 fail-closed，runtime 行预算不变
- acceptance_target: 目标 2
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: t-status-readonly-01.sh 4/0 与 check-runtime-size rc=0
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/system/workspace/scripts/tests/unit/t-status-readonly-01.sh
- expected_output: SUMMARY: 4 ok, 0 failed
- expected_RED_output: 不适用（写入路径回归保护）
- actual_RED_output: regression-only
- actual_output: "SUMMARY: 4 ok, 0 failed；runtime 27166/27166"
- evidence_file: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141512Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 写入路径本轮未改，作为回归保护执行。
- replacement_evidence: AT-001 与全量 CI
- red_how: 基线已符合；回归以 AT-001 为准。
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge

## Unit
- acceptance_target: 只读标记仅出现在只读入口，写入路径未放宽
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 4 ok / 0 failed
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: 四个 status 视图全绿
- testing_layer: integration
- target_environment: test-pre-merge-20261113T141512Z-status-readonly-semantics
- required_evidence: AT-001 + test-all --ci 0 failed
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: guarded merge 后只读视图仍可用
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 四个只读视图在空 agent_working 下实测 rc=0 并输出状态段；runtime 行数 27166 不变。
