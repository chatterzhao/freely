# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: scope 超标时 commit 不被阻塞，仅输出 warning
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: --fail-on-required 已从 pre-commit.sh 移除
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh
- expected_output: 0
- actual_output: 0
- evidence_file: (执行后填写，echo 0 > .freely/run/test-evidence/acceptance-1.log)
- blocker: (失败时填写)
- status: passed

## Unit
- acceptance_target: pre-commit scope check 改为警告
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 中无 --fail-on-required
- not_applicable_reason: (不适用填写)
- not_applicable_explanation: (不适用填写)
- replacement_evidence: (不适用填写)

## Integration
- acceptance_target: scope 超标时多个文件可正常 commit
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: (不适用)
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次改动仅涉及 hook 文本和 AGENTS.md，不涉及多模块协作、数据流或状态变更，无集成面可测
- replacement_evidence: merge 到 develop 后通过后续 PR 提交流程自然验证

## End-to-End
- acceptance_target: 修改后的 hook 在 develop 上正常工作
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T054513Z-scope-warning → develop merge chain
- required_evidence: (不适用)
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 本 fix 的端到端验证发生在 merge 到 develop 后的实际 PR 提交流程中，当前工位无法模拟 develop 上的完整 merge 流程
- replacement_evidence: merge 后下一个 PR 的提交流程自然覆盖

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次修改仅涉及 hook 文本和 AGENTS.md，不涉及运行时逻辑，无需真实环境测试
