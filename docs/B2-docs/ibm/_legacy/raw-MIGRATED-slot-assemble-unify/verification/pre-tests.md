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
- test_command: freely pr-merge-guarded develop fix/raw-20260626T173930Z-slot-assemble-unify --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
^- status: passed
## Integration
- acceptance_target: dry-run pass
- testing_layer: integration
- test_command: freely pr-merge-guarded develop fix/raw-20260626T173930Z-slot-assemble-unify --dry-run
- expected_output: --dry-run complete
- actual_output: --dry-run complete
^- status: passed
## End-to-End
- acceptance_target: daemon start + slot recovery 正常工作
- testing_layer: end-to-end
- not_applicable_reason: 需 merge 后重启 daemon 验证 slot recovery
## Real-Environment
- real_environment_status: not_tested
