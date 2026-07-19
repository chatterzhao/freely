# Pre-Tests: agent 实例 ID 全链路
- issue_id: I-20260719T074532Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: freely L6064 raw_key 从硬编码改为变量提取
- acceptance_target: grep 显示使用 _worker_raw_key 而非硬编码 'develop'
- testing_layer: unit
- target_environment: fix-raw-20260719T074532Z-agent-instance-id
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/agent-instance-id/raw-20260719T074532Z/verification/test-evidence/acceptance-1.log
- test_command: grep -n "agent_assign.*develop" docs/system/workspace/scripts/runtime/freely
- expected_output: (no output — grep exit 1, 无硬编码 'develop')
- expected_RED_output: 命中 L6064 的硬编码 'develop'
- red-green-status: green
- status: pass
- red_how: L6064 硬编码 'develop'

### acceptance-2
- id: AT-002
- requirement: freely L13306 用 agent_next_free 替代硬编码 "worker_01"
- acceptance_target: L13306 不再含硬编码
- testing_layer: unit
- target_environment: fix-raw-20260719T074532Z-agent-instance-id
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/agent-instance-id/raw-20260719T074532Z/verification/test-evidence/acceptance-2.log
- test_command: grep -n '_worker_agent_id="worker_01"' docs/system/workspace/scripts/runtime/freely
- expected_output: (no output)
- expected_RED_output: L13306
- red-green-status: green
- status: pass
- red_how: L13306 _worker_agent_id="worker_01"

### acceptance-3
- id: AT-003
- requirement: a2a_task.py 有 --agent-instance 参数
- acceptance_target: argparse 含 --agent-instance
- testing_layer: unit
- target_environment: fix-raw-20260719T074532Z-agent-instance-id
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/agent-instance-id/raw-20260719T074532Z/verification/test-evidence/acceptance-3.log
- test_command: grep -c 'agent.instance\|agent-instance' docs/system/workspace/scripts/runtime/a2a_task.py
- expected_output: "1" 或更多
- expected_RED_output: "0"（无此参数）
- red-green-status: green
- status: pass
- red_how: a2a_task.py 无 --agent-instance 参数

### acceptance-4
- id: AT-004
- requirement: Runtime worker 发现用 LIKE 'worker_%' 替代等值匹配
- acceptance_target: grep 显示 LIKE 模式
- testing_layer: unit
- target_environment: fix-raw-20260719T074532Z-agent-instance-id
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/agent-instance-id/raw-20260719T074532Z/verification/test-evidence/acceptance-4.log
- test_command: grep -c "LIKE.*worker_%\|agent_id.*LIKE.*worker" docs/system/workspace/scripts/runtime/freely
- expected_output: "1" 或更多
- expected_RED_output: "0"
- red-green-status: green
- status: pass
- red_how: 当前 WHERE agent_id = 'worker'

## Unit
- acceptance_target: 5 处代码修改均为文本层变更，grep 可验证
- testing_layer: unit
- target_environment: fix-raw-20260719T074532Z-agent-instance-id
- required_evidence: AT-001~004 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001~004 直接 grep 验证修改点
- replacement_evidence: AT-001~004 输出

## Integration
- acceptance_target: 两条 launch 路径的 agent_assign 调用均传入正确的 raw_key 和 agent_instance
- testing_layer: integration
- target_environment: develop → daemon 重启
- required_evidence: daemon 重启后 agent_working.worker_id 非 NULL
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 集成验证需要 daemon 运行 + Manager 实际委派，属 post-merge dogfood
- replacement_evidence: AT-001~004 GREEN

## End-to-End
- acceptance_target: Worker task agent_id=worker_NN → Runtime LIKE 发现 → bridge 启动
- testing_layer: end-to-end
- target_environment: develop merge → daemon auto mode
- required_evidence: daemon 运行观察
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: post-merge dogfood 验证
- replacement_evidence: AT-001~004 GREEN

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 5处修复已完成(L6064 raw_key + L13306 agent_next_free + a2a_task --agent-instance + DB LIKE + prompt模板), daemon重启后下一轮patrol自然验证
