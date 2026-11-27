# Pre-Tests: 全角标点变量边界
- issue_id: I-20261127T100325Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 无全角标点邻接变量，失败回执可操作
- acceptance_target: 目标 1-2
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261127T100325Z-fullwidth-colon-shell
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-fullwidth-variable-boundary.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 2 failed
- actual_RED_output: "SUMMARY: 4 ok, 2 failed（develop 基线）"
- actual_output: "SUMMARY: 6 ok, 0 failed（显式边界）"
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T100325Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 中回执仍用 \$raw_key：，必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 静态扫描 + set -u 下 stub rc=1 的 stderr 断言
## Unit
- test_tasks:
  1. 扫描全角标点邻接变量。
  2. stub 失败回执可操作。
