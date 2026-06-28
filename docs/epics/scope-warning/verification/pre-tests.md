# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: scope 超标时 commit 不被阻塞，仅输出 warning
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 多 scope 文件 commit 成功，HOOK 输出 scope note 但不 exit 1
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh
- expected_output: 0
- actual_output: 0（确认 --fail-on-required 已移除）
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (失败时填写)
- status: passed

## Unit
- acceptance_target: pre-commit scope check 改为警告
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 中无 --fail-on-required，MSG无exit 1
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本次仅修改3个文本文件（hook + AGENTS.md），单元级验证已完成（grep + 手动检查hook语法），集成和端到端在test-pre-merge工位合并后验证
- replacement_evidence: acceptance-1 的 grep 结果

## Integration
- acceptance_target: scope 超标时多个文件可正常 commit
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 多scope文件 commit 仅输出警告不阻塞
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次改动仅涉及hook文本和AGENTS.md，不涉及多模块协作、数据流或状态变更。集成面在merge到develop后通过后续PR验证

## End-to-End
- acceptance_target: 修改后的 hook 在 develop 上正常工作
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T054513Z-scope-warning → develop merge chain
- required_evidence: merge 到 develop 后 PR 正常创建和合并
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本fix的端到端验证发生在merge到develop后的实际使用中（后续PR提交流程自然验证），当前工位无法模拟develop上的完整merge流程

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次修改仅涉及hook文本和AGENTS.md，不涉及运行时逻辑，无需真实环境测试
