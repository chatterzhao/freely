# Pre-Tests: Worker slot ACP 协议兼容修复
- issue_id: I-20260718T043147Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: agent-table.toml worker_slot 已改为 claude-apikey-ds-pro-auto
- acceptance_target: agent-table.toml 的 worker_slot = claude-apikey-ds-pro-auto
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: grep 输出显示 claude-apikey-ds-pro-auto
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/acp-config-reader/raw-20260718T043147Z/verification/test-evidence/acceptance-1.log
- test_command: grep "worker_slot" /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/agent-table.toml
- expected_output: worker_slot = "claude-apikey-ds-pro-auto"
- expected_RED_output: worker_slot = "opencode-apikey-ds-flash-auto"
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: grep agent-table.toml 确认当前值为 opencode-apikey-ds-flash-auto（错误配置，RED）

### acceptance-2
- id: AT-002
- requirement: daemon 重启后 worker ACP bridge initialize 无超时错误
- acceptance_target: worker 日志中出现 initialize 成功，无 ACP timeout
- testing_layer: integration
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: freely live-status 无 acp_initialize_timeout 错误；worker 日志显示 initialize 完成
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/acp-config-reader/raw-20260718T043147Z/verification/test-evidence/acceptance-2.log
- test_command: cd /Users/zhaoyu/Downloads/code/my-freely/freely && freely live-status 2>&1 | grep -E "worker|acp|timeout|initialize"
- expected_output: 无 acp_timeout / acp_initialize_timeout 相关错误行
- expected_RED_output: manager_worker_launch_verification_blocked 或 acp timeout 相关错误
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 当前 daemon 运行时 live-status 显示 last_exit_reason=manager_worker_launch_after_ai_cycle，worker 日志含 ACP initialize timeout

### acceptance-3
- id: AT-003
- requirement: Manager 成功委派 Worker，任务状态从 submitted 进入 working
- acceptance_target: worker task 能从 submitted → working（不卡在 submitted）
- testing_layer: end-to-end
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: freely fleet-status 或 freely live-status 显示至少一个 worker 处于 working 状态
- evidence_level: real_env
- artifact_ref: docs/B2-docs/acp/acp-config-reader/raw-20260718T043147Z/verification/test-evidence/acceptance-3.log
- test_command: cd /Users/zhaoyu/Downloads/code/my-freely/freely && freely fleet-status 2>&1 | grep -E "worker|working|submitted"
- expected_output: 至少一个 worker 显示 working 或 activity_state=ai_active
- expected_RED_output: 所有 worker 处于 submitted 状态，无任何 working
- actual_RED_output:
- actual_output:
- evidence_file:
- red-green-status: pending
- status: pending
- blocker:
- red_how: 当前所有 worker task 永远停在 submitted，无法进入 working

## Unit
- acceptance_target: agent-table.toml 配置格式合法（TOML 语法正确，字段值非空）
- testing_layer: unit
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-001 grep 覆盖此层
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 直接通过 grep 验证配置值，已覆盖单元层验证需求
- replacement_evidence: AT-001 grep 输出

## Integration
- acceptance_target: worker bridge 与 claude-agent-acp 完成 stdio JSON-RPC initialize handshake
- testing_layer: integration
- target_environment: fix-raw-20260718T043147Z-worker-acp-bridge-timeout
- required_evidence: AT-002 live-status 无 ACP timeout 错误覆盖此层
- blocker_taxonomy: execution_pending_or_failed

## End-to-End
- acceptance_target: 完整 Manager→Worker 委派链路可用（task 从 submitted → working）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260718T043147Z-worker-acp-bridge-timeout → develop merge chain
- required_evidence: AT-003 fleet-status 显示 worker working 状态
- blocker_taxonomy: execution_pending_or_failed

## Real-Environment
- real_environment_status: fail
- real_environment_reason: 当前生产 agent-table.toml 使用 opencode-apikey-ds-flash-auto，所有 worker 无法启动（此 fix 的 RED 状态）
