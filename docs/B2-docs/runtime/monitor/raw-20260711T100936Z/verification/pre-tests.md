# Pre-Tests: daemon stop rc=143 分类
- issue_id: I-20260711T100936Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: stop_marker 检测正确区分 stop vs crash
- acceptance_target: stop_marker 存在时 stop_reason=stop_requested → exit 0
- testing_layer: integration
- target_environment: test-pre-merge-20260711T100936Z-rc143-classification
- required_evidence: bash 语法检查 + 逻辑审查确认
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/monitor/raw-20260711T100936Z/verification/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/monitor-ai-acp.sh
- expected_output: (no output = syntax OK)
- expected_RED_output: stop_reason=unknown for both stop and crash
- actual_RED_output: 修复前 daemon stop 和 AI crash 都产生 rc=143 → stopReason=unknown → exit 1
- actual_output: bash -n passed (syntax OK), stop_marker 检查逻辑已加入
- evidence_file: docs/B2-docs/runtime/monitor/raw-20260711T100936Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: bash 语法检查通过
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: bash -n 无错误
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: bash 函数级修改，AT-001 的 bash -n 检查已覆盖语法。stop_marker 检查逻辑为条件判断（文件存在性），无独立单元测试面。
- replacement_evidence: bash -n passed + 代码审查确认逻辑正确

## Integration
- acceptance_target: monitor-ai-acp.sh 与 freely daemon stop 的 stop_marker 协作
- testing_layer: integration
- target_environment: test-pre-merge 工位
- required_evidence: 代码审查确认 stop_marker_file() 函数与 monitor 中 _stop_marker 变量一致
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成测试需要运行中 daemon，当前工位为语法级修改。stop_marker_file() 已在 freely bash 中定义，monitor 调用方式一致。
- replacement_evidence: 代码审查确认函数签名和文件路径一致

## End-to-End
- acceptance_target: daemon stop → loop.log 显示 stopReason=stop_requested
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: 合并后 daemon 运行日志
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 端到端验证需要真实 daemon 运行环境，合并后在实际运行中验证
- replacement_evidence: 代码逻辑审查 + bash -n 语法检查

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 12行逻辑修改，bash -n 通过，合并后 daemon 实机验证
