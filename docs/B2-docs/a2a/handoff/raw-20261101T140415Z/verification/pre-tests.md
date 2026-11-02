# Pre-Tests: 交接运行时 P0 修复
- issue_id: I-20261101T140415Z-A
> B2 写入时 `red-green-status: pending`；RED 后改 `red`；GREEN 后改 `green`。

## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: acp_session_connect 在 _do_new 路径（跨工具/无 manager 会话）于 session/new 后送达首条 handoff 消息
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature worktree + stubbed ACP bridge
- required_evidence: unittest 输出
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-handoff-runtime.py
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py
- expected_output: test_new_session_prompts_first_message OK；调用序列含 session/new 后 session/prompt，prompt 含 [role:worker] 与原文
- expected_RED_output: NameError: name 'message' is not defined
- actual_RED_output: NameError: name 'message' is not defined
- actual_output: OK (unittest)；session/new 后紧跟 session/prompt，prompt 含 [role:worker] 与原文
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T140415Z/verification/test-evidence/test-handoff-runtime.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

### acceptance-2
- id: AT-002
- requirement: 存活判定三态：ping 有 result=alive；session error=dead；bridge 不可达=unknown
- surface_kind: unit
- target_lane: feature-local
- promotion_gate: develop_merge
- testing_layer: unit
- target_environment: feature worktree + stubbed ACP RPC
- required_evidence: unittest 输出
- evidence_level: mock
- artifact_ref: docs/system/workspace/scripts/tests/test-handoff-runtime.py
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py
- expected_output: test_session_state_alive_dead_unknown OK，三态分别为 alive/dead/unknown
- expected_RED_output: AttributeError: module 'watchdog_sse' has no attribute '_session_state'
- actual_RED_output: AttributeError: module 'watchdog_sse' has no attribute '_session_state'
- actual_output: OK；alive / dead / unknown 三态断言通过
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T140415Z/verification/test-evidence/test-handoff-runtime.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

### acceptance-3
- id: AT-003
- requirement: _check_agent_liveness 在 alive 时不清绑定；在 dead 时清绑定
- surface_kind: integration
- target_lane: premerge-integration
- promotion_gate: develop_merge
- testing_layer: integration
- target_environment: test-pre-merge worktree + stubbed DB/ACP
- required_evidence: unittest 输出 + 断言 upsert 调用
- evidence_level: integration
- artifact_ref: docs/system/workspace/scripts/tests/test-handoff-runtime.py
- test_command: python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py
- expected_output: test_liveness_keeps_alive_binding OK；alive 时无清绑定 upsert，dead 时一次
- expected_RED_output: pgrep 误判使 alive 行被清绑定
- actual_RED_output: AssertionError: alive session must not be cleared；upsert val=worker_01
- actual_output: OK；alive 无清绑定 upsert，dead 恰好一次
- evidence_file: docs/B2-docs/a2a/handoff/raw-20261101T140415Z/verification/test-evidence/test-handoff-runtime.log
- red-green-status: green
- status: passed
- blocker: execution_pending_or_failed

## Unit
- acceptance_target: _do_new 首条消息与 _session_state 三态
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: AT-001 + AT-002
- blocker_taxonomy: execution_pending_or_failed
1. 运行 `python3 docs/system/workspace/scripts/tests/test-handoff-runtime.py`，断言 AT-001/AT-002。

## Integration
- acceptance_target: _check_agent_liveness 与 DB upsert 的交互
- testing_layer: integration
- target_environment: test-pre-merge worktree
- required_evidence: AT-003
- blocker_taxonomy: execution_pending_or_failed
1. 在同一测试文件中运行 liveness 用例，断言 alive 不清绑定、dead 清一次。

## End-to-End
- acceptance_target: n/a
- testing_layer: end-to-end
- target_environment: n/a
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 真实交接需要活的 ACP bridge 与 harness 会话；本切片只改模块内路径，端到端由 AT-003 的集成断言替代。
- replacement_evidence: AT-003 + 既有 test-acp-handoff.py 回归

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 在 test-pre-merge 工位以真实仓库文件跑 unittest；不依赖外部服务或凭据。
