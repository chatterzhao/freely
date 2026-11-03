# Pre-Tests: 双平台 open issue 对齐
- issue_id: I-20261103T091157Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: Gitee 搜索分页可命中第 2 页的 raw issue
- acceptance_target: search_raw_issue 不再单页截断
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-adapter-gitee-search.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-adapter-gitee-search.py
- expected_output: OK
- expected_RED_output: AssertionError: 0 != 1 : expected one match, got []
- actual_RED_output: AssertionError: 0 != 1 : expected one match, got []（修复前只请求 per-page 50 的第一页）
- actual_output: OK（分页到第 2 页命中 IK1ATI）
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/verification/test-evidence/AT-001-gitee-search-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: fake _run 返回 130 条 issue（目标在第 2 页），断言命中且发生分页。

### acceptance-2
- id: AT-002
- requirement: 两平台 open raw key 集合相等，且每个 open 均有本地文档与双平台编号
- acceptance_target: parity 实时校验通过
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity
- required_evidence: parity 测试通过日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/verification/test-evidence/AT-002-parity-GREEN.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py
- expected_output: OK: github/gitee open raw-key sets equal
- expected_RED_output: FAIL: open key sets differ ... 4 gitee-only；13 个 open 缺本地文档
- actual_RED_output: FAIL：gitee-only=['20260715T131531Z','20260718T035754Z','20260719T054212Z','20260720T032133Z']，并列出缺本地文档/编号不一致项
- actual_output: OK: github/gitee open raw-key sets equal (14 keys); all have local docs with both platform ids
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/verification/test-evidence/AT-002-parity-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T3,T4
- case_design: 实时读取两平台 open issue 与本地文档，断言集合相等、编号一致。

### acceptance-3
- id: AT-003
- requirement: 4 个 Gitee-only 漂移镜像已关闭且理由记录
- acceptance_target: 关闭状态 + 评论理由
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity
- required_evidence: Gitee issue 状态 closed + 关闭评论
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/verification/test-evidence/AT-003-drift-closed.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-open-parity.py（其 open 集合已不含这 4 个 key，可作为关闭证据）
- expected_output: 4 个 key 不再出现在任何平台 open 集合
- expected_RED_output: 4 个 key 出现在 gitee open 集合
- actual_RED_output: 4 个 key 出现在 gitee open 集合（parity RED 日志）
- actual_output: 4 个 key 均不在两平台 open 集合；Gitee 对应 issue 已 closed 且带关闭理由
- evidence_file: docs/B2-docs/platform/issue-parity/raw-20261103T091157Z/verification/test-evidence/AT-003-drift-closed.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T4
- case_design: 通过 parity 测试的动态 open 集合验证关闭结果，并抽查 issue 状态。

## Unit
- acceptance_target: Gitee search 分页
- testing_layer: unit
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity
- required_evidence: AT-001 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-adapter-gitee-search.py。

## Integration
- acceptance_target: 双平台 open 对齐与本地可追溯
- testing_layer: integration
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity
- required_evidence: AT-002 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-open-parity.py。

## End-to-End
- acceptance_target: 真实双平台 API 对齐
- testing_layer: end-to-end
- target_environment: fix/raw-20261103T091157Z-platform-issue-parity → develop merge chain
- required_evidence: parity 测试 + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-002 已是真实平台 API 的端到端校验；PR 链路由 guarded receipts 覆盖。
- replacement_evidence: AT-002 + pr-create/pr-merge receipts。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: parity 测试与 4 个漂移关闭均直接调用真实 GitHub/Gitee API。
