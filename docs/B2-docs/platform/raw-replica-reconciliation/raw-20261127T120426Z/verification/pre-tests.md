# Pre-Tests: 封装 comment-delete
- issue_id: I-20261127T120426Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: 显式参数、映射校验、失败透传、无调用方直连
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261127T120426Z-comment-delete-command
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T120426Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-comment-delete-command.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 1 ok, 14 failed
- actual_RED_output: "SUMMARY: 1 ok, 14 failed（develop 基线）"
- actual_output: "SUMMARY: 15 ok, 0 failed（stub handler）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T120426Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: develop 无 adapter 函数与封装命令，必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T3
- case_design: 结构断言 + stub handler 的映射校验/错误透传
## Unit
- test_tasks:
  1. 两平台 handler 与 adapter 校验函数存在。
  2. Gitee CLI 子命令存在。
