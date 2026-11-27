# Pre-Tests: 可操作评论诊断
- issue_id: I-20261127T110239Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: closed issue 不 POST、401 翻译可操作、promote-finalize 重跑幂等
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261127T110239Z-actionable-comment-error
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-actionable-comment-error.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 9 failed
- actual_RED_output: "SUMMARY: 2 ok, 9 failed（develop 基线）"
- actual_output: "SUMMARY: 11 ok, 0 failed（stub API + 重跑）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 无状态检查/翻译/幂等守卫，必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: stub HTTP 401 + fixture 双跑 promote-finalize
## Unit
- test_tasks:
  1. 三处契约静态断言。
  2. 401 语义翻译文本。
  3. 重跑只推一次评论。
