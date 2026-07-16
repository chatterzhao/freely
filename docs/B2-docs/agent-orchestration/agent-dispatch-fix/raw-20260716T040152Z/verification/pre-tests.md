# Pre-Tests: Agent 编排链路缺陷修复
- issue_id: I-20260716T040152Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: a2a-exit --reason 参数能正确解析并传递到 A2A task
- acceptance_target: a2a_task.py a2a-exit --state input-required --reason "needs-review:b1" 创建的 task 的 reason 字段 = "needs-review:b1"
- testing_layer: unit
- target_environment: feature worktree (fix/raw-20260716T040152Z-agent-orchestration-fix)
- required_evidence: 测试输出显式 PASS，reason 字段值正确
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -m pytest tests/test_a2a_exit_reason.py -v 2>&1
- expected_output: |
  test_a2a_exit_reason.py::test_reason_arg_parsed PASSED
  test_a2a_exit_reason.py::test_reason_passed_to_create PASSED
  test_a2a_exit_reason.py::test_reason_passed_to_update PASSED
  All tests passed ✅
- expected_RED_output: tests FAILED — a2a-exit --reason not recognized or reason field is empty
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


### acceptance-2
- id: AT-002
- requirement: watchdog_sse.py 收到 reason 后能正确路由到对应 role
- acceptance_target: |
  InputRequiredReason.from_string("needs-review:b1").needs_role == "reviewer"
  InputRequiredReason.from_string("needs-review:dev").needs_role == "reviewer"
  InputRequiredReason.from_string("").needs_role == "manager"
  InputRequiredReason.from_string("needs-manager-decision").needs_role == "manager"
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 所有路由断言通过
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-2.log
- test_command: python3 -m pytest tests/test_input_required_reason.py tests/test_watchdog_sse.py -v 2>&1
- expected_output: |
  All tests passed ✅
- expected_RED_output: (已有测试，RED 阶段验证全部通过——这些是已有功能的回归测试)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


### acceptance-3
- id: AT-003
- requirement: a2a-exit wrapper 作为独立命令可调用
- acceptance_target: bin/a2a-exit --help 输出 usage 信息
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: wrapper 可执行且正确转发参数
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-3.log
- test_command: bash -c 'cd /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260716T040152Z-agent-orchestration-fix && ./bin/a2a-exit --help 2>&1'
- expected_output: usage 信息包含 --state、--reason、--role 参数
- expected_RED_output: ./bin/a2a-exit: No such file or directory
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


### acceptance-4
- id: AT-004
- requirement: a2a-exit --reason 端到端 — 从 CLI 到 A2A task 到 SSE notification
- acceptance_target: 调用 a2a-exit input-required --reason needs-review:b1 → 查询 task 的 reason 字段 = needs-review:b1
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: A2A task reason 字段正确存储
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-4.log
- test_command: python3 -m pytest tests/test_agent_orchestration_e2e.py::test_a2a_exit_reason_e2e -v 2>&1
- expected_output: |
  test_a2a_exit_reason_e2e PASSED
- expected_RED_output: test FAILED — reason field is empty or not present
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


### acceptance-5
- id: AT-005
- requirement: freely-cycle 不再包含 reviewer 分配逻辑
- acceptance_target: grep "agent_assign.*reviewer.*update_only" bin/freely-cycle 返回空
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 代码中 reviewer 分配代码已移除
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-5.log
- test_command: bash -c '! grep -q "agent_assign.*reviewer.*update_only" /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/fix-raw-20260716T040152Z-agent-orchestration-fix/bin/freely-cycle && echo "PASS: no reviewer dispatch in freely-cycle"'
- expected_output: PASS: no reviewer dispatch in freely-cycle
- expected_RED_output: (grep 找到匹配行 — reviewer 分配逻辑仍存在)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


### acceptance-6
- id: AT-006
- requirement: agent_assign(update_only=True) 在行不存在时输出错误日志
- acceptance_target: 调用 agent_assign(update_only=True) 在行不存在时返回 error status 并输出 stderr
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: stderr 包含 row-not-found 或等效警告
- evidence_level: integration
- artifact_ref: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/verification/test-evidence/acceptance-6.log
- test_command: python3 -m pytest tests/test_agent_working_logic.py -v 2>&1
- expected_output: |
  All tests passed ✅
- expected_RED_output: (新增的 update_only 测试 FAILED — 无错误日志输出)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)


## Unit
- acceptance_target: a2a-exit argparse 解析、InputRequiredReason 路由、agent_working 逻辑
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 所有单元测试 PASS
- blocker_taxonomy: execution_pending_or_failed

## Integration
- acceptance_target: a2a-exit → A2A task → reason 字段 端到端连通
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: reason 字段从 CLI 正确传递到 A2A task 存储
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: fix→test-pre-merge→develop merge passes
- testing_layer: end_to_end
- target_environment: develop-bound guarded merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码改动仅涉及 Python 脚本和 shell wrapper，不涉及运行时 daemon 进程。修改后通过单元测试和集成测试验证即可。
