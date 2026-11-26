# Pre-Tests: wt-close 职责边界与 schema 对齐
- issue_id: I-20261125T065112Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 三份文档写实；batch 提示 scoped；touched linked schema 硬门禁
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261125T065112Z-wt-close-boundary
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/wt-close-boundary/raw-20261125T065112Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-wt-close-boundary.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 9 failed
- actual_RED_output: "SUMMARY: 1 ok, 9 failed（develop 基线）"
- actual_output: "SUMMARY: 10 ok, 0 failed（strict/bullet/untouched 三态）"
- evidence_file: docs/B2-docs/worktree-lifecycle/wt-close-boundary/raw-20261125T065112Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT，文档旧措辞与缺失 validator 必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 文档结构断言 + 从 gate 抽取纯函数做 strict/bullet/untouched 三态断言
## Unit
- test_tasks:
  1. 三份文档 write-free 与单入口表述。
  2. batch 提示 scoped。
  3. validator 三态。
