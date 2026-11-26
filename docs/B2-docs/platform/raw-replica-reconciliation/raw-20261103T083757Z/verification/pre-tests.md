# Pre-Tests: Gitee delete-branch 端点纠正
- issue_id: I-20261103T083757Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: canonical 分支端点、DELETE 方法、鉴权与回执保持
- acceptance_target: 目标 1-2
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261103T083757Z-gitee-delete-branch-path
- required_evidence: develop RED、工位 GREEN，逐断言与 SUMMARY
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T083757Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-gitee-delete-branch-path.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 4 ok, 4 failed
- actual_RED_output: "SUMMARY: 4 ok, 4 failed（develop 基线）"
- actual_output: "SUMMARY: 8 ok, 0 failed（canonical 端点）"
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T083757Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 对 develop 跑同一 AT，git-ref 路径必然命中。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge
- task_refs: T1-T2
- case_design: 纯函数路径断言 + stub api_request 的方法/路径/鉴权/回执断言
## Unit
- test_tasks:
  1. 无 git-ref 路径残留。
  2. repo_path_branch 返回 canonical 路径。
  3. cmd_delete_branch 方法/鉴权/回执保持。
