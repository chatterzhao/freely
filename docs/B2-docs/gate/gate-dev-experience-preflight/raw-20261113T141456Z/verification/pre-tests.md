# Pre-Tests: governance-only lane 接线
- issue_id: I-20261113T141456Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 白名单单源、GATE 1 给指引、batch 显式范围
- acceptance_target: 目标 1-3
- testing_layer: integration
- target_environment: test-pre-merge-20261113T141456Z-governance-only-lane
- required_evidence: develop RED 3/5 → 工位 GREEN 8/0
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-governance-only-lane.py
- expected_output: SUMMARY: 8 ok, 0 failed
- expected_RED_output: SUMMARY: 3 ok, 5 failed
- actual_RED_output: "SUMMARY: 3 ok, 5 failed（develop 基线）"
- actual_output: "SUMMARY: 8 ok, 0 failed"
- evidence_file: docs/B2-docs/gate/gate-dev-experience-preflight/raw-20261113T141456Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 基线存在双白名单、GATE 1 无 lane 指引、batch 无 --raw-key。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

## Unit
- acceptance_target: 单源白名单与 lane 边界
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: t-governance-only-lane-01.sh 全绿
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: AT-001 + 全量 CI
- testing_layer: integration
- target_environment: test-pre-merge-20261113T141456Z-governance-only-lane
- required_evidence: test-all --ci 0 failed
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: guarded merge 放行边界不降级
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: config 白名单单源生效；bin/ 与未配置路径均拒绝。
