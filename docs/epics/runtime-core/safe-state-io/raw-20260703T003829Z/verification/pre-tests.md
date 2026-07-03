# Pre-Tests: write_workcell_state safe source

- issue_id: I-20260703T003829Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: daemon 启动不再因 workcell-state.env 的多词值而执行意外命令
- acceptance_target: daemon start 成功，无 pr-create-guarded 被意外调用
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source
- required_evidence: daemon 启动日志显示 supervisor 正常运行
- evidence_level: real_env
- artifact_ref: docs/epics/runtime-core/safe-state-io/raw-20260703T003829Z/verification/test-evidence/acceptance-1.log
- test_command: ./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/test-pre-merge-20260703T003829Z-safe-env-source --task-mode auto
- expected_output: daemon_status: running, supervisor_pid 非空
- expected_RED_output: daemon 启动失败，日志中出现 pr-create-guarded 被意外执行
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: (不适用时填写)
- not_applicable_explanation: (不适用时填写)
- replacement_evidence: (不适用时填写)
- red_how: fix: 构造含未引号多词值的 workcell-state.env，启动 daemon，确认 source 触发 pr-create-guarded 导致启动失败

### acceptance-2
- id: AT-002
- requirement: workcell-state.env 文件内容正确，多词值有引号
- acceptance_target: write_workcell_state 生成的文件中所有值都有引号包裹
- testing_layer: unit
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source
- required_evidence: 生成的 env 文件所有行格式为 KEY="value"
- evidence_level: integration
- artifact_ref: docs/epics/runtime-core/safe-state-io/raw-20260703T003829Z/verification/test-evidence/acceptance-2.log
- test_command: grep -c '=' .freely/run/workcell-state.env && ! grep -E '^[A-Z_]+=[^"].* .*[^"]$' .freely/run/workcell-state.env
- expected_output: 所有行都有 KEY="value" 格式，无未引号多词值
- expected_RED_output: LAST_WORKER_CLOSEOUT_GATE_COMMAND=freely pr-create-guarded 存在未引号多词值
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: (不适用时填写)
- not_applicable_explanation: (不适用时填写)
- replacement_evidence: (不适用时填写)
- red_how: fix: 执行 write_workcell_state 前，手动放置含未引号多词值的旧 env 文件，确认生成的文件正确带引号

### acceptance-3
- id: AT-003
- requirement: .freely/run/workcell-state.env 不在 git 跟踪中
- acceptance_target: git ls-files 不包含该文件
- testing_layer: unit
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source
- required_evidence: git ls-files .freely/run/workcell-state.env 返回空
- evidence_level: integration
- artifact_ref: docs/epics/runtime-core/safe-state-io/raw-20260703T003829Z/verification/test-evidence/acceptance-3.log
- test_command: git ls-files .freely/run/workcell-state.env | grep -c . || echo "not tracked - PASS"
- expected_output: not tracked - PASS
- expected_RED_output: .freely/run/workcell-state.env（文件在 git 跟踪中）
- actual_RED_output: (RED 阶段执行后填写)
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: pending
- status: pending
- blocker: (失败时填写)
- not_applicable_reason: (不适用时填写)
- not_applicable_explanation: (不适用时填写)
- replacement_evidence: (不适用时填写)
- red_how: fix: 修复前 git ls-files 能找到该文件

## Unit
- acceptance_target: meta_env_value 正确提取 LAST_ENTRYPOINT_MODE
- testing_layer: unit
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source
- required_evidence: 函数返回正确值
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 端到端测试已覆盖；meta_env_value 是已有函数，本项目不新增单元测试基础设施
- replacement_evidence: AT-001 端到端结果

## Integration
- acceptance_target: daemon 启动后 write_workcell_state 正确写入 state 文件
- testing_layer: integration
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source
- required_evidence: daemon 启动后 state 文件内容符合预期格式
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 + AT-002 组合已覆盖集成场景
- replacement_evidence: AT-001 + AT-002 组合结果

## End-to-End
- acceptance_target: daemon 在 task-mode auto 下正常启动并运行 AI 循环
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260703T003829Z-safe-env-source → develop merge chain
- required_evidence: daemon supervisor 运行，AI 正常启动
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 就是端到端测试
- replacement_evidence: AT-001 端到端结果

## Real-Environment
- real_environment_status: pass
- real_environment_reason: develop 分支 daemon 已在修复后成功启动运行，验证通过
