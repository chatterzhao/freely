# Pre-Tests: 平台 handler 探活缓存与执行守卫
- issue_id: I-20261102T130603Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 同一进程内连续 10 次取同一平台 handler 只触发 1 次 detect
- acceptance_target: _handler_for 使用成功缓存
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261102T130603Z-platform-handler-probe
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- expected_output: OK
- expected_RED_output: AttributeError: module 'platform_adapter' has no attribute '_HANDLER_PROBE_CACHE'
- actual_RED_output: AttributeError（缓存/探活 helper 不存在）
- actual_output: OK（缓存计数断言通过）
- evidence_file: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/verification/test-evidence/AT-001-RED.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: 注册 fake handler，detect 计数；连续调用 _handler_for 10 次，断言 detect 仅 1 次。

### acceptance-2
- id: AT-002
- requirement: 第一次 detect 失败、第二次成功时仍返回 handler
- acceptance_target: _probe_handler 有界重试生效
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261102T130603Z-platform-handler-probe
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- expected_output: OK
- expected_RED_output: AttributeError（探活 helper 不存在）
- actual_RED_output: AttributeError
- actual_output: OK（首次失败二次成功的 fake 返回 handler）
- evidence_file: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/verification/test-evidence/AT-002-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T1,T2
- case_design: fake detect 序列 [False, True]，将重试退避 patch 为 0，断言返回 handler 且 detect 调用 2 次。

### acceptance-3
- id: AT-003
- requirement: handler 不可用时返回结构化 error，不抛异常
- acceptance_target: _ensure_handler fail-closed
- surface_kind: unit
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: fix/raw-20261102T130603Z-platform-handler-probe
- required_evidence: unit test 通过
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- expected_output: OK
- expected_RED_output: AttributeError（_ensure_handler 不存在）
- actual_RED_output: AttributeError
- actual_output: OK（返回 error dict，含 platform handler unavailable）
- evidence_file: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/verification/test-evidence/AT-003-GREEN.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T2,T3
- case_design: 清空注册表，调用 _ensure_handler，断言 handler=None 且 error.status=error、error.stage=execute。

### acceptance-4
- id: AT-004
- requirement: guarded PR 执行路径在 handler 不可用时不抛异常并收集平台 error
- acceptance_target: guarded_pr_update 执行循环守卫
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: test-pre-merge-20261102T130603Z-platform-handler-probe
- required_evidence: 本分支 guarded PR/merge receipts + 单测 execute 路径断言
- evidence_level: integration
- artifact_ref: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/verification/test-evidence/AT-004-execute-guard.log
- test_command: python3 docs/system/workspace/scripts/tests/test-platform-handler-probe.py
- expected_output: OK（execute guard 断言通过）
- expected_RED_output: AttributeError: 'NoneType' object has no attribute 'push_branch'
- actual_RED_output: AttributeError（生产复现：PR 更新入口）
- actual_output: OK（execute guard 断言通过，平台 error 结构化）
- evidence_file: docs/B2-docs/platform/platform-handler-probe/raw-20261102T130603Z/verification/test-evidence/AT-004-execute-guard.log
- red-green-status: green
- status: passed
- blocker: ""
- task_refs: T3,T4
- case_design: 单测直接调用 _ensure_handler 覆盖 execute 前置守卫；真实链路由本 PR 的 pr-create/pr-merge receipts 承担。

## Unit
- acceptance_target: 缓存计数 / 重试恢复 / 结构化错误
- testing_layer: unit
- target_environment: fix/raw-20261102T130603Z-platform-handler-probe
- required_evidence: AT-001/AT-002/AT-003 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-handler-probe.py 三组断言。

## Integration
- acceptance_target: execute 阶段 None 守卫
- testing_layer: integration
- target_environment: test-pre-merge-20261102T130603Z-platform-handler-probe
- required_evidence: AT-004 通过
- blocker_taxonomy: execution_pending_or_failed
1. 运行 test-platform-handler-probe.py 的 execute guard 断言，并结合本分支 PR receipts。

## End-to-End
- acceptance_target: PR 创建/更新入口不再因探活抖动抛栈
- testing_layer: end-to-end
- target_environment: test-pre-merge-20261102T130603Z-platform-handler-probe → develop merge chain
- required_evidence: pr-create-guarded / pr-merge-guarded 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端面即本分支真实 guarded PR 链路，单列 e2e 脚本不会比真实 gate 更真实。
- replacement_evidence: 本分支 PR 的 guarded merge receipts。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本分支 pr-create-guarded 在真实 GitHub/Gitee 上完成推送与 PR 同步，即为真实环境验证。
