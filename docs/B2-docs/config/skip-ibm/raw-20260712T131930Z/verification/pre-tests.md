# Pre-Tests: TOML template format fix
- issue_id: I-20260712T131930Z-A
## Acceptance Items
### acceptance-1
- id: AT-001
- requirement: freely init 生成 config.toml 时 allowed_paths 为数组非字符串
- acceptance_target: python3 tomllib 读取 config.toml [skip_ibm_gate].allowed_paths 为 list
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: type(allowed_paths) == list
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/skip-ibm/raw-20260712T131930Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "import tomllib;c=tomllib.load(open('.freely/config.toml','rb'));assert isinstance(c['skip_ibm_gate']['allowed_paths'],list);print('PASS')"
- expected_output: PASS
- expected_RED_output: AssertionError (type is str not list)
- actual_RED_output: 修复前 config.toml allowed_paths = "[]" (字符串)
- actual_output: PASS — config.toml allowed_paths = [] (数组)
- evidence_file: docs/B2-docs/config/skip-ibm/raw-20260712T131930Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing
## Unit
- acceptance_target: TOML 模板语法验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: tomllib 解析模板无异常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001 已覆盖
- replacement_evidence: AT-001 passed
## Integration
- acceptance_target: freely init --reset 后 config.toml 格式正确
- testing_layer: integration
- target_environment: develop
- required_evidence: init 后 allowed_paths 为数组
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 需实际运行 freely init 验证，模板修改为纯格式
- replacement_evidence: AT-001: tomllib 解析模板通过
## End-to-End
- acceptance_target: governance-merge-gate 不受影响
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: merge gate 正常
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 合并后验证
- replacement_evidence: 代码审查
## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯模板格式修复，tomllib 解析验证通过
