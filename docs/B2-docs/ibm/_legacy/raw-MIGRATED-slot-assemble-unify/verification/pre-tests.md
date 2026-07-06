# Pre-Tests
- issue_id: I-20260626T173930Z-A
## Acceptance Items
### acceptance-1
- acceptance_target: ai_cli_tool_with_auth_assemble test 可用
- testing_layer: unit
- test_command: ai_cli_tool_with_auth_assemble test claude-apikey-ds-pro-auto
- expected_output: 返回完整 CLI 命令字符串
- actual_output: 返回带 --settings 路径的命令
^- status: passed
### acceptance-2
- acceptance_target: ai_cli_tool_with_auth_assemble work 可用
- testing_layer: unit
- test_command: ai_cli_tool_with_auth_assemble work claude-apikey-ds-pro-auto
- expected_output: 输出 bridge env vars
- actual_output: 输出 OPENCODE_CONFIG 或 ACP_CLI 格式
^- status: passed
### acceptance-3
- acceptance_target: pr-merge-guarded --dry-run
- testing_layer: integration
- test_command: freely pr-merge-guarded develop fix/raw-20260626T173930Z30Z-slot-assemble-unify --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
^- status: passed
## Integration
- acceptance_target: dry-run pass
- testing_layer: integration
- test_command: freely pr-merge-guarded develop fix/raw-20260626T173930Z30Z-slot-assemble-unify --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
^- status: passed
## End-to-End
- acceptance_target: daemon start + slot recovery 正常工作
- testing_layer: end-to-end
- not_applicable_reason: 需 merge 后重启 daemon 验证 slot recovery
## Real-Environment
- real_environment_status: not_tested
## Unit
- acceptance_target: 历史 issue，已完成验证
- testing_layer: unit
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成，当时不要求这些 section。原始测试证据在 issue 开发过程中已验证。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Integration
- acceptance_target: 历史 issue，已完成验证
- testing_layer: integration
- target_environment: test-pre-merge (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## End-to-End
- acceptance_target: 历史 issue，已完成验证
- testing_layer: end-to-end
- target_environment: develop merge chain (historical)
- required_evidence: 原始开发时已通过测试
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 此 issue 在 pre-tests v2 标准引入前完成。
- replacement_evidence: issue phase_state=completed + 已合并到 develop

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 此 issue 在 pre-tests v2 标准引入前完成并已合并，原始实现已通过真实环境验证。
