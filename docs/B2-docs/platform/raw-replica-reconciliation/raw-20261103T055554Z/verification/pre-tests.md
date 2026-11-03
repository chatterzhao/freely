# Pre-Tests: raw replica 身份解析按标题前缀
- issue_id: I-20261103T055554Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 标题前缀唯一命中优先于 body 交叉引用
- acceptance_target: 给定一条真实身份 + 一条 body 引用匹配时，_resolve_raw_identity 选中真实身份
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T055554Z-replica-search-prefix
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity.py
- expected_output: OK
- expected_RED_output: AttributeError: module 'platform_adapter' has no attribute '_resolve_raw_identity'
- actual_RED_output: AttributeError: module 'platform_adapter' has no attribute '_resolve_raw_identity'
- actual_output: OK（4 个用例全过）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/verification/test-evidence/AT-001-RED.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 用 fake match 列表构造"标题前缀真实身份 + 其它 issue 标题"两元素，断言选中真实身份。

### acceptance-2
- id: AT-002
- requirement: 真机 discover 对交叉引用 key 不再 ambiguous
- acceptance_target: discover_raw_replicas('20260807T114900Z') 两个平台均 status=ok 且 title 为该 key
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: test-pre-merge-20261103T055554Z-replica-search-prefix
- required_evidence: 真机调用日志
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/verification/test-evidence/AT-002-live-discover.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity-live.py 20260807T114900Z
- expected_output: github=ok gitee=ok
- expected_RED_output: github=ambiguous gitee=ambiguous
- actual_RED_output: github=ambiguous gitee=ambiguous（修复前从 main repo 观测）
- actual_output: github=ok gitee=ok（test 工位真机执行）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/verification/test-evidence/AT-002-live-discover.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T2,T3
- case_design: 用真实平台凭据调用 discover_raw_replicas，断言两个配置平台都返回 status=ok 且不是 ambiguous。

### acceptance-3
- id: AT-003
- requirement: 多真实身份仍 ambiguous / 无标题命中保留单条兜底
- acceptance_target: 两条标题前缀命中 -> ambiguous；无标题命中且仅一条 body 命中 -> 采用；空集合 -> not found
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261103T055554Z-replica-search-prefix
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-adapter-raw-identity.py
- expected_output: OK
- expected_RED_output: AttributeError（helper 未实现）
- actual_RED_output: AttributeError（helper 未实现）
- actual_output: OK（同一套 unit 用例 4/4）
- evidence_file: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/verification/test-evidence/AT-003-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 用 fake match 列表分别构造多条前缀命中、单条兜底、空集合三种输入，断言返回值与错误语义。

## Unit
- acceptance_target: _resolve_raw_identity 的四种分支
- testing_layer: unit
- target_environment: fix/raw-20261103T055554Z-replica-search-prefix
- required_evidence: AT-001/AT-003 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-adapter-raw-identity.py 覆盖标题优先、多身份 ambiguous、兜底、no match。

## Integration
- acceptance_target: 真机 discover 身份解析
- testing_layer: integration
- target_environment: test-pre-merge-20261103T055554Z-replica-search-prefix
- required_evidence: AT-002 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-adapter-raw-identity-live.py 20260807T114900Z。

## End-to-End
- acceptance_target: PR gate 的 raw-reconciliation-gate 不再因 body 引用被 block
- testing_layer: end_to_end
- target_environment: test-pre-merge-20261103T055554Z-replica-search-prefix -> develop merge chain
- required_evidence: pr-create-guarded / pr-merge-guarded 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端面就是本分支自身经过 pr-create/pr-merge 的 guarded 链路；单独 e2e 脚本无法比真实 gate 链路更真实。
- replacement_evidence: 本分支 PR 的 guarded merge receipts。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 真机 discover 调用（AT-002）直接使用配置的 GitHub/Gitee 凭据读取真实 issue，属于真实环境验证。
