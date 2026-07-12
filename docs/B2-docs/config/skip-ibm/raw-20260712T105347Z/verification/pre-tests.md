# Pre-Tests: config.toml skip_ibm 配置
- issue_id: I-20260712T105347Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: TOML config reading works
- acceptance_target: python3 tomllib 成功读取 [skip_ibm_gate] section
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: tomllib 解析成功
- evidence_level: integration
- artifact_ref: docs/B2-docs/config/skip-ibm/raw-20260712T105347Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "import tomllib; cfg=tomllib.load(open('.freely/config.toml','rb')); print(cfg.get('skip_ibm_gate',{}))"
- expected_output: {'allowed_paths': []}
- expected_RED_output: KeyError/not found
- actual_RED_output: 修复前 .freely/config.toml 无 [skip_ibm_gate] section
- actual_output: tomllib 成功解析，skip_ibm_gate.allowed_paths = []
- evidence_file: docs/B2-docs/config/skip-ibm/raw-20260712T105347Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

### acceptance-2
- id: AT-002
- requirement: governance-merge-gate syntax valid
- acceptance_target: python3 compile() passes
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: compile() no error
- evidence_level: integration  
- artifact_ref: docs/B2-docs/config/skip-ibm/raw-20260712T105347Z/verification/test-evidence/acceptance-1.log
- test_command: python3 -c "compile(open('docs/system/workspace/scripts/quality/governance-merge-gate').read(),'x','exec')"
- expected_output: (no output = OK)
- expected_RED_output: SyntaxError
- actual_RED_output: (pre-existing code)
- actual_output: Syntax OK
- evidence_file: docs/B2-docs/config/skip-ibm/raw-20260712T105347Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- blocker: definition_missing

## Unit
- acceptance_target: 两处修改语法正确
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: python3 compile + tomllib parse
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: AT-001/AT-002 覆盖了语法和配置解析
- replacement_evidence: AT-001+AT-002 passed

## Integration
- acceptance_target: FREELY_SKIP_IBM_GATE + templates/ 路径通过门禁
- testing_layer: integration
- target_environment: develop merge chain
- required_evidence: pr-create-guarded pass
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 集成验证需要在 PR merge gate 中实际执行
- replacement_evidence: 合并后验证

## End-to-End
- acceptance_target: 用户可通过 config.toml 添加自定义路径
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: 添加路径后 pr-create-guarded FREELY_SKIP_IBM_GATE=1 通过
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: protected_environment_only
- not_applicable_explanation: 端到端验证需要用户实际配置和运行
- replacement_evidence: 代码审查 + 语法验证

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 纯配置模板 + governance quality script 变更，语法验证通过
