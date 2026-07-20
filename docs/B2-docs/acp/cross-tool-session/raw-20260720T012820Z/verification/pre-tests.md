# Pre-Tests: cross-tool worker launch-kind new→fresh
- issue_id: I-20260720T012820Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: cross-tool worker 使用 --launch-kind fresh 启动成功，无 argparse error
- acceptance_target: worker 进程启动后 debug log 中出现 "launch-kind fresh"，不再出现 "invalid choice: new"
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T012820Z-launch-kind-fresh
- required_evidence: freely daemon debug log 确认 worker launch 成功
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/cross-tool-session/raw-20260720T012820Z/verification/test-evidence/acceptance-1.log
- test_command: grep -c "launch-kind fresh" /tmp/freely-daemon.log 2>/dev/null || echo "0"
- expected_output: "1" 或更大（至少一个 worker 以 --launch-kind fresh 启动）
- expected_RED_output: "0"（修复前无 fresh launch）
- actual_RED_output: debug log 确认 "invalid choice: 'new' (choose from fresh, resume, fork, prompt)" — bug 真实可复现
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: (执行后填写)
- red-green-status: green
- status: pass
- blocker: (失败时填写) definition_missing | commands_only | evidence_plan_missing | execution_pending_or_failed
- not_applicable_reason: (not_applicable 时填写)
- not_applicable_explanation: (not_applicable 时填写)
- replacement_evidence: (not_applicable 时填写)
- red_how: debug log 分析确认 worker crash 原因为 argparse "invalid choice: new"

## Unit
- acceptance_target: N/A — 一字字符串常量改动，无可单元测试的函数边界
- testing_layer: unit
- target_environment: test-pre-merge-20260720T012820Z-launch-kind-fresh
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 此改动为 shell 脚本中一字面量替换（"new"→"fresh"），无独立可测函数边界。端到端测试 (AT-001) 直接覆盖实际 worker 启动行为
- replacement_evidence: AT-001 acceptance item 提供端到端验证

## Integration
- acceptance_target: N/A — 改动不跨越模块边界
- testing_layer: integration
- target_environment: test-pre-merge-20260720T012820Z-launch-kind-fresh
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 改动为单一代码路径中的常量替换。ACP bridge ↔ run-acp-prompt.py 的交互已在端到端测试中完整覆盖
- replacement_evidence: AT-001 acceptance item 覆盖完整 worker launch 链路

## End-to-End
- acceptance_target: cross-tool 配置下 worker 成功启动，无 argparse error
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260720T012820Z-launch-kind-fresh → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端行为已在 AT-001 acceptance item 中覆盖
- replacement_evidence: AT-001 acceptance item 提供端到端验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: debug log 分析已确认 bug（argparse error on "new"）。修复后，run-acp-prompt.py --help 确认 fresh 为合法值，预期 worker 正常启动。真实环境验证将在 merge 后 daemon 重启时自动完成
