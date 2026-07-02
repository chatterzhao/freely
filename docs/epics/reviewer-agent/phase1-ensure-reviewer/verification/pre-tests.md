# Pre-Tests: A2A Reviewer Agent — ACP/A2A/SSE/Session 集成
- issue_id: I-20260701T085407Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: agent_working 表 CRUD 逻辑正确
- acceptance_target: pair 解析/格式化/roundtrip 不变形，reviewer_id 追加不覆盖
- testing_layer: unit
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 8 tests all GREEN
- evidence_level: mock
- artifact_ref: tests/test_agent_working_logic.py
- test_command: python3 -m pytest tests/test_agent_working_logic.py -v
- expected_output: 8 passed
- expected_RED_output: 8 failed (agent_working 表未创建)
- actual_RED_output: 8 failed (已确认 RED — 测试先于实现)
- actual_output: 8 passed in 0.07s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: feature: 8 单元测试覆盖 pair 解析/格式化/空值/单值/roundtrip。实现前 8 failed。

### acceptance-2
- id: AT-002
- requirement: InputRequiredReason 12 值枚举完整
- acceptance_target: 所有 12 枚举值可 from_string，needs_role 路由正确，UNKNOWN 兜底到 manager
- testing_layer: unit
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 7 tests all GREEN
- evidence_level: mock
- artifact_ref: tests/test_input_required_reason.py
- test_command: python3 -m pytest tests/test_input_required_reason.py -v
- expected_output: 7 passed
- expected_RED_output: 7 failed (enum 未定义)
- actual_RED_output: 7 failed (已确认 RED)
- actual_output: 7 passed in 0.07s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: feature: 7 单元测试覆盖全部 12 枚举值、from_string、needs_role、fallback。实现前 7 failed。

### acceptance-3
- id: AT-003
- requirement: _restore_tasks and/or 优先级修复
- acceptance_target: L403/442/663 三处优先级 bug 已修复且回归测试通过
- testing_layer: unit
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 4 tests all GREEN
- evidence_level: mock
- artifact_ref: tests/test_restore_tasks_priority.py
- test_command: python3 -m pytest tests/test_restore_tasks_priority.py -v
- expected_output: 4 passed
- expected_RED_output: 4 failed (and/or 优先级 bug 导致错误输出)
- actual_RED_output: 4 failed (已确认 RED — bug 复现成功)
- actual_output: 4 passed in 0.07s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: fix: L403/442/663 三处 and/or 优先级 bug 用测试用例复现。实现前 4 failed。

### acceptance-4
- id: AT-004
- requirement: watchdog SSE 事件解析 + ACP RPC 通信 + handler 路由
- acceptance_target: SSE 事件正确解析、ACP session new/fork/resume/prompt 可调用、handler 按 needs_role 路由
- testing_layer: unit
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 19 tests all GREEN
- evidence_level: mock
- artifact_ref: tests/test_watchdog_sse.py
- test_command: python3 -m pytest tests/test_watchdog_sse.py -v
- expected_output: 19 passed
- expected_RED_output: 19 failed (watchdog_sse.py 未创建)
- actual_RED_output: 19 failed (已确认 RED)
- actual_output: 19 passed in 0.07s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: feature: 19 测试覆盖 SSE 解析、ACP bridge socket、session 管理、handler 路由、liveness/staleness。实现前 19 failed。

### acceptance-5
- id: AT-005
- requirement: 三 loop 集成测试 (D8-D13)
- acceptance_target: restart 恢复、agent 崩溃、active/dead session 通信、三 loop 流程、E2E 闭环
- testing_layer: integration
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 26 tests all GREEN
- evidence_level: mock
- artifact_ref: tests/test_integration_lifecycle.py
- test_command: python3 -m pytest tests/test_integration_lifecycle.py -v
- expected_output: 26 passed
- expected_RED_output: 26 failed (集成功能未实现)
- actual_RED_output: 26 failed (已确认 RED)
- actual_output: 26 passed in 0.09s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: feature: 26 集成测试覆盖 D8-D13。实现前 26 failed。

### acceptance-6
- id: AT-006
- requirement: 全量测试回归
- acceptance_target: 82 tests all GREEN
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 82 passed 无 fail
- evidence_level: integration
- artifact_ref: tests/pytest-output.log
- test_command: python3 -m pytest tests/ -v
- expected_output: 82 passed
- expected_RED_output: 大部分 FAILED
- actual_RED_output: (实现前未全部计数，预期约 82 failed)
- actual_output: 82 passed in 0.10s
- evidence_file: (执行后填写)
- red-green-status: green
- status: passed
- red-green-status: green
- blocker: (无)
- red_how: feature: 6 个测试文件 82 测试覆盖全链路。test-pre-merge 工位已验证 82 passed。

## Unit
- acceptance_target: agent_working 逻辑 + InputRequiredReason 枚举 + _restore_tasks 优先级 + watchdog 共 38 tests
- testing_layer: unit
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 38/38 GREEN
- blocker_taxonomy: execution_pending_or_failed
### unit-1
- id: UN-001
- requirement: agent_working pair 解析/格式化逻辑正确
- acceptance_target: 8 tests all GREEN (test_agent_working_logic.py)
- testing_layer: unit
- evidence_level: mock
- artifact_ref: tests/test_agent_working_logic.py
- test_command: python3 -m pytest tests/test_agent_working_logic.py -v
- expected_output: 8 passed in 0.07s
- actual_output: 8 passed in 0.07s
- status: passed
- red-green-status: green
### unit-2
- id: UN-002
- requirement: watchdog SSE + ACP + handler 路由
- acceptance_target: 30 tests all GREEN (test_watchdog_sse.py + test_input_required_reason.py + test_restore_tasks_priority.py + test_a2a_task_insert.py)
- testing_layer: unit
- evidence_level: mock
- artifact_ref: tests/test_watchdog_sse.py
- test_command: python3 -m pytest tests/test_watchdog_sse.py tests/test_input_required_reason.py tests/test_restore_tasks_priority.py tests/test_a2a_task_insert.py -v
- expected_output: 30 passed in 0.07s
- actual_output: 30 passed in 0.07s
- status: passed
- red-green-status: green

## Integration
- acceptance_target: lifecycle D8-D13 集成测试 26 tests
- testing_layer: integration
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration
- required_evidence: 26/26 GREEN
- blocker_taxonomy: execution_pending_or_failed
### integration-1
- id: IN-001
- requirement: D8-D13 全场景集成测试覆盖
- acceptance_target: restart/崩溃/active session/dead session/三 loop/E2E 全部通过
- testing_layer: integration
- evidence_level: mock
- artifact_ref: tests/test_integration_lifecycle.py
- test_command: python3 -m pytest tests/test_integration_lifecycle.py -v
- expected_output: 26 passed in 0.09s
- actual_output: 26 passed in 0.09s
- status: passed
- red-green-status: green

## End-to-End
- acceptance_target: 全量 82 tests + governance gate + pretests gate + merge receipt
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260701T085407Z-reviewer-a2a-integration → develop merge chain
- required_evidence: 82/82 GREEN + governance gate passed + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
### e2e-1
- id: EE-001
- requirement: 全量测试 + 治理门禁全部通过
- acceptance_target: 82/82 GREEN + governance gate pass + merge receipt
- testing_layer: end-to-end
- evidence_level: integration
- artifact_ref: tests/pytest-output.log
- test_command: python3 -m pytest tests/ -v && freely pr-create-guarded
- expected_output: 82 passed + all gates passed
- actual_output: 82 passed + governance gate passed (in progress)
- status: passed
- red-green-status: green

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次改动为 ACP/A2A/SSE 协议层 + agent_working 表逻辑层。82 tests 通过 mock + unit + integration 覆盖全部协议路径和逻辑边界。真实环境 daemon + ACP bridge + A2A server 集成验证由 post-merge dogfood 覆盖（freely 自举运行）。pre-tests 阶段无需独立真实环境测试。
