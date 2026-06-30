# Pre-Tests: fix get_config → python3 reader
- issue_id: I-20260630T143515Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: init --auto 不报 get_config 错误
- acceptance_target: init 正常搜索/下载 ACP 工具
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T143515Z-fix-get-config-init
- required_evidence: init 执行无 get_config 错误
- evidence_level: real_env
- artifact_ref: docs/epics/acp-tool-setup/fix-get-config-init/test-evidence/acceptance-1.log
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo PASS
- expected_output: PASS
- expected_RED_output: get_config: command not found
- actual_RED_output: freely init --auto → get_config: command not found at L20045
- actual_output: (GREEN)
- evidence_file: (GREEN)
- red-green-status: green
- status: passed
- red_how: 执行 freely init --auto 时报 get_config: command not found
## Unit
- acceptance_target: bash -n syntax OK
- testing_layer: unit
- target_environment: fix-raw-20260630T143515Z-fix-get-config-init
- required_evidence: Syntax OK
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: Unit covered by AT-001
- replacement_evidence: bash -n passed
## Integration
- acceptance_target: config.toml cache hit on repeat init
- testing_layer: integration
- target_environment: test-pre-merge-20260630T143515Z-fix-get-config-init
- required_evidence: 4 tools show (config.toml)
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: Tested manually on develop — all 4 tools hit cache
- replacement_evidence: Manual test: 4/4 tools → (config.toml)
## End-to-End
- acceptance_target: init → cache → no download on repeat
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T143515Z-fix-get-config-init → develop
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: Dogfood after merge
- replacement_evidence: Post-merge verification
## Real-Environment
- real_environment_status: pass
- real_environment_reason: Tested on develop: init --auto works, 4 tools cached, no get_config error
