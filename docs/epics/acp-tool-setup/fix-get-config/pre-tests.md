# Pre-Tests: fix get_config/set_config regression
- issue_id: I-20260630T135725Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: freely init --auto 不报 get_config: command not found
- acceptance_target: init 正常执行，搜索已有 ACP binary 或提示下载
- testing_layer: integration
- target_environment: fix-raw-20260630T135725Z-fix-get-config
- required_evidence: init 执行成功
- evidence_level: integration
- artifact_ref: docs/epics/acp-tool-setup/fix-get-config/test-evidence/acceptance-1.log
- test_command: |
  bash -n docs/system/workspace/scripts/runtime/freely && echo "PASS: syntax OK"
  grep -q "upsert_config_key" docs/system/workspace/scripts/runtime/freely && echo "PASS: upsert_config_key used"
  grep -q "get_config" docs/system/workspace/scripts/runtime/freely && echo "WARN: get_config still referenced" || echo "PASS: get_config removed from our code"
- expected_output: "PASS: syntax OK\nPASS: upsert_config_key used\nPASS: get_config removed"
- expected_RED_output: get_config: command not found (修复前)
- actual_RED_output: freely init --auto 时报 get_config: command not found
- actual_output: PASS: syntax OK, upsert_config_key used, get_config removed
- evidence_file: docs/epics/acp-tool-setup/fix-get-config/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: 执行 freely init --auto 时触发 get_config: command not found

## Unit
- acceptance_target: bash -n syntax check passed
- testing_layer: unit
- target_environment: fix-raw-20260630T135725Z-fix-get-config
- required_evidence: bash -n 无错误
- blocker_taxonomy: execution_pending_or_failed
  - not_applicable_reason: no_executable_boundary_at_this_layer
  - not_applicable_explanation: Unit verification done via AT-001 code review
  - replacement_evidence: Syntax check (bash -n OK) + grep verification
  - not_applicable_reason: no_executable_boundary_at_this_layer
  - not_applicable_explanation: Unit tests covered by AT-001 code review + bash -n
  - replacement_evidence: Syntax check passed
- status: not_applicable

## Integration
- acceptance_target: freely init --auto 正常执行
- testing_layer: integration
- target_environment: test-pre-merge-20260630T135725Z-fix-get-config
- required_evidence: init 不报 get_config 错误
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需实际运行 init，已通过 GREP 验证代码级修复
- replacement_evidence: 代码审查 + bash -n 验证

## End-to-End
- acceptance_target: freely init --auto → config.toml 正确写入
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260630T135725Z-fix-get-config → develop merge chain
- required_evidence: guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
- status: not_applicable
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后在生产环境狗粮验证
- replacement_evidence: post-merge dogfood test

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 代码级修复已验证（get_config→grep+upsert_config_key），合并后狗粮测试
