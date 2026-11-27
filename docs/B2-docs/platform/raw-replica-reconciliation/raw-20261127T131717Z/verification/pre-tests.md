# Pre-Tests: 标题身份唯一判据
- issue_id: I-20261127T131717Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 规范前缀匹配、body 提及排除、多副本仍 ambiguous
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261127T131717Z-title-only-identity
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-title-only-identity.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 10 failed
- actual_RED_output: "SUMMARY: 1 ok, 10 failed（develop 基线）"
- actual_output: "SUMMARY: 11 ok, 0 failed（stub gh candidates）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T131717Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 无 is_identity_title 且按 body 搜索，必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 纯函数边界断言 + stub gh 候选过滤
## Unit
- test_tasks:
  1. 唯一身份 helper。
  2. title-only 查询。
  3. 无 body 判据。
