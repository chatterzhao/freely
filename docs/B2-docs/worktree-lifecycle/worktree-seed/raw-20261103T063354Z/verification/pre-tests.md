# Pre-Tests: PR 收尾平台名对齐
- issue_id: I-20261103T063354Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 收尾循环使用配置平台名，不再把 git remote 名传给 adapter
- acceptance_target: 目标 1-3
- testing_layer: integration
- target_environment: test-pre-merge-20261103T063354Z-pr-merge-platform-name
- required_evidence: develop RED + 工位 GREEN 逐断言；函数级单测
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-pr-merge-platform-name.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: 至少 1 failed（仍按 git remote 循环 / 无 configured-platforms 动作）
- actual_RED_output: "SUMMARY: 4 ok, 7 failed（S2/S3/S4/S6/S7/S8/B3 failed）"
- actual_output: (GREEN 阶段填写)
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- red_how: develop 基线 `_sync_prs_across_platforms` 遍历 `git remote` 并传 origin 给 close-pr；AT 必然失败。
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge

### acceptance-2
- id: AT-002
- requirement: 既有 pr-merge 行为不回归
- acceptance_target: 目标 3
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261103T063354Z-pr-merge-platform-name
- required_evidence: test-pr-merge-push-receipt.py 与 test-all --ci 全绿
- evidence_level: integration
- artifact_ref: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/verification/test-evidence/acceptance-2.log
- test_command: python3 docs/system/workspace/scripts/tests/test-pr-merge-push-receipt.py
- expected_output: SUMMARY: 0 failed
- expected_RED_output: regression-only
- actual_RED_output: regression-only
- actual_output: (GREEN 阶段填写)
- evidence_file: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261103T063354Z/verification/test-evidence/acceptance-2.log
- red-green-status: not_applicable
- status: not_applicable
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本轮改收尾循环而非 push helper；作为回归保护。
- replacement_evidence: AT-001 与全量 CI
- red_how: 基线已绿；RED 以 AT-001 为准。
- surface_kind: end_to_end
- target_lane: premerge-integration
- promotion_gate: develop_merge

## Unit
- acceptance_target: adapter CLI 与收尾循环的静态契约
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: t-pr-merge-platform-name-01.sh 全绿
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: AT-001 + AT-002
- testing_layer: integration
- target_environment: test-pre-merge-20261103T063354Z-pr-merge-platform-name
- required_evidence: 两条 AT 全绿且 test-all --ci 0 failed
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: guarded merge 回执不再出现 unknown: origin
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge 回执与本 PR 的回执证据
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pending
- real_environment_reason: 待 GREEN 阶段填写
