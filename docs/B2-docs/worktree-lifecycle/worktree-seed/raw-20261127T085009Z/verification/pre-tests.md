# Pre-Tests: 单平台 raw 物化
- issue_id: I-20261127T085009Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 显式来源跳过前置校验、审计可见、issue-sync 补副本、失败非零
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261127T085009Z-single-platform-materialize
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-single-platform-materialize.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 5 ok, 5 failed
- actual_RED_output: "SUMMARY: 5 ok, 5 failed（develop 基线）"
- actual_output: "SUMMARY: 10 ok, 0 failed（stub rc 0/1）"
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT，source_platform 未接入判据必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 结构断言 + stub issue-sync 的 0/1 退出码断言
## Unit
- test_tasks:
  1. 判据尊重显式 source-platform。
  2. 审计与命令文档同步。
  3. issue-sync 失败非零且打印拒绝。
