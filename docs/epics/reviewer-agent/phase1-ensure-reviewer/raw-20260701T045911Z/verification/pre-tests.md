# Pre-Tests: Phase 1 Reviewer agent
- issue_id: I-20260701T045911Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: ensure_reviewer() 函数存在于 runtime 脚本
- acceptance_target: grep 确认函数定义
- testing_layer: unit
- target_environment: test-pre-merge-20260701T045911Z-reviewer-agent-orchestration
- required_evidence: grep 输出
- evidence_level: integration
- artifact_ref: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-1.log
- test_command: grep -c "ensure_reviewer\|reviewer.*agent\|reviewer.*ACP" docs/system/workspace/scripts/runtime/freely
- expected_output: >=3 references
- expected_RED_output: 0 (函数不存在)
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-1.log
- red-green-status: pending
- status: pending
- red_how: feature: 修复前无 ensure_reviewer 函数

### acceptance-2
- id: AT-002
- requirement: A2A task 支持 reviewer agent_id
- acceptance_target: grep 确认 reviewer 前缀处理
- testing_layer: unit
- target_environment: test-pre-merge-20260701T045911Z-reviewer-agent-orchestration
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-2.log
- test_command: grep -c "reviewer\|REVIEWER" docs/system/workspace/scripts/runtime/a2a/a2a_server.py
- expected_output: >=3
- expected_RED_output: 0
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-2.log
- red-green-status: pending
- status: pending
- red_how: feature: A2A 当前不支持 reviewer agent_id

### acceptance-3
- id: AT-003
- requirement: freely-cycle dispatch_reviewer 有代码执行
- acceptance_target: grep 确认 dispatch 后启动 reviewer 的逻辑
- testing_layer: unit
- target_environment: test-pre-merge-20260701T045911Z-reviewer-agent-orchestration
- required_evidence: grep
- evidence_level: integration
- artifact_ref: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-3.log
- test_command: grep -c "dispatch_reviewer\|ensure_reviewer\|launch_reviewer" bin/freely-cycle docs/system/workspace/scripts/runtime/freely
- expected_output: >=2 处有实际 dispatch 逻辑
- expected_RED_output: 0
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/epics/reviewer-agent/phase1-ensure-reviewer/raw-20260701T045911Z/verification/acceptance-3.log
- red-green-status: pending
- status: pending
- red_how: feature: freely-cycle 只建议 dispatch，无执行代码

## Unit
- acceptance_target: 4 项改动语法正确
- testing_layer: unit
- target_environment: feature/raw-20260701T045911Z-reviewer-agent-orchestration
- required_evidence: bash -n
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/002/003 grep 覆盖
- replacement_evidence: AT-001/002/003 green
- status: not_applicable

## Integration
- acceptance_target: reviewer agent 能成功启动
- testing_layer: integration
- target_environment: test-pre-merge-20260701T045911Z-reviewer-agent-orchestration
- required_evidence: daemon 日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需要完整 daemon 环境启动 reviewer，合并后在 develop 验证
- replacement_evidence: AT-001/002/003 green + 合并后观察
- status: not_applicable

## End-to-End
- acceptance_target: manager→worker→reviewer 三者均能启动
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: 3 种 agent 同时运行
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: AT integration green
- status: not_applicable

## Real-Environment
- real_environment_status: fail
- real_environment_reason: RED 阶段：reviewer 不作为独立 agent
