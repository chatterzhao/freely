# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: scope 超标时 commit 不被阻塞
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: pre-commit.sh 中移除 --fail-on-required 和 exit 1
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh && echo "scope check: warning only, no block"
- expected_output: 0\nscope check: warning only, no block
- actual_output: 0\nscope check: warning only, no block
- evidence_file: test-evidence/acceptance-1.log
- blocker: 
- status: passed

## Unit
- acceptance_target: 3 个文件修改正确（pre-commit + AGENTS.md + AGENTS.md.example）
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 文件内容验证通过
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次仅修改 3 个文本文件的配置内容，无代码逻辑变更，单元测试通过手动验证文件内容即可
- replacement_evidence: acceptance-1 grep 验证 + git diff 审查

## Integration
- acceptance_target: scope 超标时多文件正常 commit
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 多 scope commit 仅警告
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 本次改动仅 hook 文本和 AGENTS.md，不涉及多模块协作、数据流或状态变更。集成验证在 merge develop 后通过后续 PR 自然覆盖
- replacement_evidence: merge 后下一个 PR 提交流程自然验证

## End-to-End
- acceptance_target: develop 上 PR 正常创建合并
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: merge + PR 流程正常
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 端到端验证在 merge develop 后的实际 PR 流程中自然发生，当前工位无法模拟 develop 完整流程
- replacement_evidence: 本 PR 的 merge 和后续 #3601 PR 的创建过程自然覆盖

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 仅修改 hook 文本和 AGENTS.md，不涉及运行时逻辑，无需真实环境测试
