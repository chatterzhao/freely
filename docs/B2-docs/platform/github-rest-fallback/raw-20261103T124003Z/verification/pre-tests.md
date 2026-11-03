# Pre-Tests: GitHub REST fallback
- issue_id: I-20261103T124003Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: GraphQL 504 时 list_open_issue_records 回退 REST 并返回 open issue
- acceptance_target: handler 回退逻辑
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T124003Z-github-handler-rest-fallback
- required_evidence: 单测 GREEN
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-adapter-github-rest-fallback.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-adapter-github-rest-fallback.py
- expected_output: OK
- expected_RED_output: AssertionError: {'4135','4136','4139'} != set()（回退前返回空）
- actual_RED_output: FAILED (failures=2)
- actual_output: OK（2 tests）
- evidence_file: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/verification/test-evidence/AT-001-rest-fallback-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: mock gh issue list 返回 504；mock gh api --paginate --slurp 返回两页（含一个 PR）→ 期望 3 条 issue。

### acceptance-2
- id: AT-002
- requirement: parity 测试在真实平台连续通过
- acceptance_target: parity 稳定性
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261103T124003Z-github-handler-rest-fallback
- required_evidence: parity 连续 3 次 OK
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/verification/test-evidence/AT-002-parity-stable.log
- test_command: for i in 1 2 3; do python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py; done
- expected_output: 3 次 OK
- expected_RED_output: FAIL gitee-only 13（GitHub 空列表误判）
- actual_RED_output: FAIL: open key sets differ ... gitee-only（真实 GraphQL 504 窗口）
- actual_output: 3 次 OK（14 keys）
- evidence_file: docs/B2-docs/platform/github-rest-fallback/raw-20261103T124003Z/verification/test-evidence/AT-002-parity-stable.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T3
- case_design: 真实 GitHub/Gitee API + 本地文档；连续 3 次。

## Unit
- acceptance_target: 回退逻辑
- testing_layer: unit
- target_environment: fix/raw-20261103T124003Z-github-handler-rest-fallback
- required_evidence: AT-001
- blocker_taxonomy: execution_pending_or_failed
1. 运行单测。

## Integration
- acceptance_target: 真实平台稳定性
- testing_layer: integration
- target_environment: fix/raw-20261103T124003Z-github-handler-rest-fallback
- required_evidence: AT-002
- blocker_taxonomy: execution_pending_or_failed
1. parity x3。

## End-to-End
- acceptance_target: scan/parity 生产路径
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: parity x3 + scan health
- blocker_taxonomy: covered_by_more_realistic_required_surface
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-002 已是真实平台端到端；scan 复用同一 handler。
- replacement_evidence: AT-002 + scan platform_health。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: parity 测试直接调用真实平台 API。
