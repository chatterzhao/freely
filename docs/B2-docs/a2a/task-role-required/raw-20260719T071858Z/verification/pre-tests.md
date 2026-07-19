# Pre-Tests: Manager prompt 模板补 --role worker
- issue_id: I-20260719T071858Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: Manager prompt 模板中 a2a-exit 委派 Worker 示例含 --role worker
- acceptance_target: grep 命中 "示例 — 委派 Worker" 后的 --role worker
- testing_layer: unit
- target_environment: fix-raw-20260719T071858Z-a2a-exit-role-worker
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-role-required/raw-20260719T071858Z/verification/test-evidence/acceptance-1.log
- test_command: grep -A2 "示例.*委派 Worker" docs/system/workspace/scripts/runtime/freely | grep -c '\--role worker'
- expected_output: "1"
- expected_RED_output: "0"（模板中没有 --role worker）
- red-green-status: pending
- status: pending
- red_how: 当前模板中委派 Worker 示例没有 --role worker（确认 RED）

### acceptance-2
- id: AT-002
- requirement: a2a_task.py --role 参数无默认值（required）
- acceptance_target: grep "--role" 相关行显示 required=True 而非 default="manager"
- testing_layer: unit
- target_environment: fix-raw-20260719T071858Z-a2a-exit-role-worker
- required_evidence: grep 输出
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-role-required/raw-20260719T071858Z/verification/test-evidence/acceptance-2.log
- test_command: grep 'p_exit.add_argument.*--role' docs/system/workspace/scripts/runtime/a2a_task.py
- expected_output: required=True（无 default="manager"）
- expected_RED_output: default="manager"（当前默认值）
- red-green-status: pending
- status: pending
- red_how: 当前 --role 有 default="manager"

### acceptance-3
- id: AT-003
- requirement: 全仓所有 a2a-exit 调用点均已显式传 --role
- acceptance_target: 所有 a2a-exit 调用（非帮助文档）含 --role
- testing_layer: unit
- target_environment: fix-raw-20260719T071858Z-a2a-exit-role-worker
- required_evidence: 无遗漏调用点
- evidence_level: real_env
- artifact_ref: docs/B2-docs/a2a/task-role-required/raw-20260719T071858Z/verification/test-evidence/acceptance-3.log
- test_command: grep -rn 'a2a-exit' docs/system/workspace/scripts/runtime/freely | grep -v '#\|示例\|--role' | grep -c 'a2a-exit'
- expected_output: "0"（所有调用点都含 --role）
- expected_RED_output: "> 0"（存在不含 --role 的调用点）
- red-green-status: pending
- status: pending
- red_how: 当前 prompt 模板中的 a2a-exit 调用不含 --role worker

## Unit
- acceptance_target: 模板字符串和 Python argparse 参数均为文本修改，单元层直接验证
- testing_layer: unit
- target_environment: fix-raw-20260719T071858Z-a2a-exit-role-worker
- required_evidence: AT-001/AT-002/AT-003 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 纯文本改动，AT-001~003 的 grep 验证即覆盖
- replacement_evidence: AT-001/AT-002/AT-003 输出

## Integration
- acceptance_target: Manager 重启后用新 prompt 模板运行，委派 Worker 时 agent_id=worker
- testing_layer: integration
- target_environment: develop → freely daemon 重启
- required_evidence: 新轮次 A2A DB 中 worker task agent_id=worker
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: E2E 验证（需要完整 daemon 运行 + Manager AI 决策）
- not_applicable_explanation: 集成层 = 模板被正确注入 prompt → Manager AI 使用新模板。此验证等价于 daemon 重启后下一轮 patrol 的结果，属于 post-merge dogfood
- replacement_evidence: AT-001~003 GREEN + post-merge daemon 观察

## End-to-End
- acceptance_target: Worker task agent_id=worker → Runtime 发现 → Worker bridge 启动 → Worker 执行任务
- testing_layer: end-to-end
- target_environment: develop merge chain → freely daemon auto mode
- required_evidence: A2A DB worker task agent_id=worker + bridge 启动日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: 需要完整 daemon 运行 + Manager AI 实际决策 + 有效 scan items
- not_applicable_explanation: 模板修改为纯文本，影响面是 AI 行为而非代码逻辑。E2E 验证在 post-merge 的 daemon 运行中自然完成
- replacement_evidence: AT-001~003 GREEN

## Real-Environment
- real_environment_status: fail
- real_environment_reason: 当前 A2A DB 中 worker task agent_id=manager，Worker 永远不启动
