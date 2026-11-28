# Pre-Tests: 批次① sync+skills 投影化
- issue_id: I-20261113T110656Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 三条实现迁到 scripts 真源，bin 变薄投影，registry 删除条目
- acceptance_target: 目标 1-3
- testing_layer: integration
- target_environment: test-pre-merge-20261113T110656Z-implementation-in-bin-migration
- required_evidence: develop RED 2/12 → 工位 GREEN 17/0
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-implementation-in-bin-batch1.py
- expected_output: SUMMARY: 17 ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 12 failed
- actual_RED_output: "SUMMARY: 2 ok, 12 failed（develop 基线）"
- actual_output: "SUMMARY: 17 ok, 0 failed"
- evidence_file: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 基线三条实现仍在 bin/，registry 仍有条目，真源不存在。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### acceptance-2
- id: AT-002
- requirement: 行为回归（raw-issue-pull parity 与 deploy-skills 语义）
- acceptance_target: 目标 2
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: t-implementation-in-bin-batch1-01.sh 与 parity 测试全绿
- evidence_level: integration
- artifact_ref: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/system/workspace/scripts/tests/unit/t-implementation-in-bin-batch1-01.sh
- expected_output: SUMMARY: 0 failed
- expected_RED_output: regression-only
- actual_RED_output: regression-only
- actual_output: "unit 全绿；parity 全绿；check-bin-projection 全绿"
- evidence_file: docs/B2-docs/command-wrapper/implementation-projection/raw-20261113T110656Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 行为逐字迁移，本项为回归保护。
- replacement_evidence: AT-001 的 parity 断言与全量 CI
- red_how: 基线 parity 已绿；RED 以 AT-001 为准。
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge

## Unit
- acceptance_target: bin 投影形态与 exec 真源
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 全绿
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: AT-001 + check-bin-projection + CI
- testing_layer: integration
- target_environment: test-pre-merge-20261113T110656Z-implementation-in-bin-migration
- required_evidence: 全绿
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 投影入口行为与 develop 基线一致
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 三条入口逐字迁移，parity 与 check-bin-projection 全绿。
