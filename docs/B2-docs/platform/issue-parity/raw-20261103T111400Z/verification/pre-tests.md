# Pre-Tests: open raw 文档物化与历史 platform_ids 回填
- issue_id: I-20261103T111400Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 每个 open raw key 有本地文档且双平台编号与平台实际编号一致
- acceptance_target: parity --require-local-docs 通过
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261103T111400Z-raw-doc-materialization
- required_evidence: parity GREEN 日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/verification/test-evidence/AT-001-parity-GREEN.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py --require-local-docs
- expected_output: OK: github/gitee open raw-key sets equal
- expected_RED_output: FAIL: ... missing local docs/B1-docs/raw-<key>/issue.md（13 个 open key）
- actual_RED_output: develop 上 FAIL，列出 13 个 open key 缺本地 raw 文档（20260714T012901Z…20261103T083757Z）
- actual_output: OK（README 见 evidence 日志）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/verification/test-evidence/AT-001-parity-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 实时平台 API + 本地文档交叉校验集合与编号。

### acceptance-2
- id: AT-002
- requirement: 历史本地文档平台编号按唯一证据回填
- acceptance_target: 回填后编号与平台一致
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261103T111400Z-raw-doc-materialization
- required_evidence: 回填清单 + parity 校验
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/verification/test-evidence/AT-002-backfill.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py --require-local-docs
- expected_output: 13 个历史文档回填成功，parity 通过
- expected_RED_output: 历史文档 platform_ids 缺失
- actual_RED_output: develop 上 13 个历史文档缺平台编号
- actual_output: 回填 13 个文档后 parity 通过（见 evidence）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261103T111400Z/verification/test-evidence/AT-002-backfill.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T2
- case_design: 对每个本地文档按标题前缀唯一匹配平台副本，不唯一则跳过。

## Unit
- acceptance_target: 无代码变更，不适用单元测试
- testing_layer: unit
- target_environment: fix/raw-20261103T111400Z-raw-doc-materialization
- required_evidence: 无
- blocker_taxonomy: not_applicable_scope
- not_applicable_reason: change_not_touching_this_layer
- not_applicable_explanation: 本 issue 仅改治理文档，无产品代码。
- replacement_evidence: AT-001/AT-002 parity 校验。

## Integration
- acceptance_target: 本地文档与平台编号一致
- testing_layer: integration
- target_environment: fix/raw-20261103T111400Z-raw-doc-materialization
- required_evidence: AT-001 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 parity --require-local-docs。

## End-to-End
- acceptance_target: 真实平台 + 本地文档
- testing_layer: end-to-end
- target_environment: fix/raw-20261103T111400Z-raw-doc-materialization
- required_evidence: AT-001
- blocker_taxonomy: not_applicable_scope
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已是真实平台校验。
- replacement_evidence: AT-001。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: parity 测试直接调用真实 GitHub/Gitee API。
