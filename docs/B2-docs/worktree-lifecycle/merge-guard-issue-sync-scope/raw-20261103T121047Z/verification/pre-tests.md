# Pre-Tests: merge-guard issue-sync scope + Gitee reopen
- issue_id: I-20261103T121047Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: merge 时只同步本 lane raw key 的 issue
- acceptance_target: filter_issue_ids 行为
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T121047Z-merge-guard-issue-sync-scope
- required_evidence: 单测 GREEN
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-merge-guard-issue-sync-scope.py
- test_command: python3 docs/system/workspace/scripts/tests/test-merge-guard-issue-sync-scope.py
- expected_output: OK
- expected_RED_output: ModuleNotFoundError: issue-sync-scope.py / filter_issue_ids missing
- actual_RED_output: ERROR ModuleNotFoundError（helper 不存在）
- actual_output: OK（3 tests）
- evidence_file: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261103T121047Z/verification/test-evidence/AT-001-scope-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 多 raw 文档 diff + 指定 key → 只保留匹配；无 key → 原样；CLI stdin 验证。

### acceptance-2
- id: AT-002
- requirement: gitee-issue.py reopen 使用与 close 一致的可工作形态
- acceptance_target: reopen_request 路径与 body
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T121047Z-merge-guard-issue-sync-scope
- required_evidence: 单测 GREEN
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-gitee-issue-reopen-path.py
- test_command: python3 docs/system/workspace/scripts/tests/test-gitee-issue-reopen-path.py
- expected_output: OK
- expected_RED_output: missing reopen_request helper
- actual_RED_output: AssertionError missing reopen_request helper
- actual_output: OK（2 tests）
- evidence_file: docs/B2-docs/worktree-lifecycle/merge-guard-issue-sync-scope/raw-20261103T121047Z/verification/test-evidence/AT-002-reopen-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T3
- case_design: 断言 path=/repos/zhaoquan/issues/IKSN3S、body={"repo":"freely","state":"open"}。

## Unit
- acceptance_target: 两个纯函数
- testing_layer: unit
- target_environment: fix/raw-20261103T121047Z-merge-guard-issue-sync-scope
- required_evidence: AT-001/AT-002
- blocker_taxonomy: execution_pending_or_failed
1. 运行两个单测。

## Integration
- acceptance_target: 真实 merge 流程只收口本 lane
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: 单测 + 代码审查
- blocker_taxonomy: covered_by_more_realistic_required_surface
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 真实 merge 场景复现需要生产级工位；本修复由 scope 纯函数单测 + merge 代码路径审查覆盖。
- replacement_evidence: AT-001 + code review。

## End-to-End
- acceptance_target: 真实 merge 不误关
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge receipt
- blocker_taxonomy: covered_by_more_realistic_required_surface
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 修复本身作用于 merge 路径，由下一次正常 lane merge 作为回归观察；事故复盘已在 B1/IDN 记录。
- replacement_evidence: merge receipt + post-merge open parity 检查。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 单元测试覆盖过滤与请求构造；merge 路径为真实执行面。
