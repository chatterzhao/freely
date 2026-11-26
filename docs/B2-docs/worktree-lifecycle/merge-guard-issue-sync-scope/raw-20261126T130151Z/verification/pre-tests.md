# Pre-Tests: pr-merge followthrough 证据沿袭
- issue_id: I-20261126T130151Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: helper 存在且在 test merge 后调用；attest 参数/回执/fail-closed
- acceptance_target: 目标 1-3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261126T130151Z-merge-followthrough-evidence
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-merge-followthrough-evidence.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 2 ok, 10 failed — develop 无 helper
- actual_RED_output: "SUMMARY: 2 ok, 10 failed（develop 基线 a63624e2）"
- actual_output: "SUMMARY: 12 ok, 0 failed（stub 全路径）"
- evidence_file: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261126T130151Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- red_how: 对 develop（--source-dir）跑同一 AT，helper 不存在必然失败。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 结构断言 + stub python3/git 捕获调用参数与回执
## Unit
- test_tasks:
  1. helper 与调用点存在。
  2. 参数、成功回执、失败指引断言。
