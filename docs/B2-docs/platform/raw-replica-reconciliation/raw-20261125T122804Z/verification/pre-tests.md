# Pre-Tests: 生成型 updated 行不参与副本内容判定
- issue_id: I-20261125T122804Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: updated-only 漂移 reconcile ok；真实正文/生命周期行差异仍 block
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T122804Z-updated-at-body-drift
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T122804Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-updated-row-reconciliation.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 3 failed — develop 无生成型行归一化
- actual_RED_output: "SUMMARY: 4 ok, 3 failed（develop 基线）"
- actual_output: "SUMMARY: 7 ok, 0 failed（归一化后）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T122804Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT（--source-dir develop），updated-only 差异必然 content_diverged。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 纯函数指纹断言 + reconcile 正反用例（updated-only ok / 正文差异 block / phase_state 差异 block）
## Unit
- test_tasks:
  1. `_body()` 归一化 `| updated |` 值但保留行。
  2. `canonical_projection` 对 updated-only 差异产生相同指纹。
  3. 人类正文与生命周期表格行差异仍产生不同指纹。
  4. `reconcile()` 正反用例。
