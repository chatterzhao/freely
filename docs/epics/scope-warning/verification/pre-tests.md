# Pre-Tests: scope hard block → advisory warning
- issue_id: I-20260628T054513Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: scope 超标时 commit 不被阻塞，仅输出 warning
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: 多 scope 文件 commit 成功，HOOK 输出 scope note 但不 exit 1
- test_command: echo "test" > /tmp/test-1 && git add /tmp/test-1 && git commit -m "test: scope check" 2>&1; echo "exit=$?"
- expected_output: 若 scope 超标则输出 [HOOK] scope note，commit 成功，exit=0
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

## Unit
- acceptance_target: pre-commit hook 不含 --fail-on-required
- testing_layer: unit
- target_environment: fix-raw-20260628T054513Z-scope-warning
- required_evidence: grep 确认
- test_command: grep -c "fail-on-required" .githooks/pre-commit.sh; echo "expected: 0"
- expected_output: 0
- actual_output: (执行后填写)
- evidence_file: (执行后填写)
- blocker: (失败时填写)
- status: pending

## Integration
- acceptance_target: scope 超标时多个文件可正常 commit
- testing_layer: integration
- target_environment: test-pre-merge-20260628T054513Z-scope-warning
- required_evidence: 5+ 文件 commit 成功

## End-to-End
- acceptance_target: 修改后的 hook 在 develop 上正常工作
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260628T054513Z-scope-warning → develop merge chain
- required_evidence: merge 到 develop 后 PR 正常创建和合并

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本次修改仅涉及 hook 文本和 AGENTS.md，不涉及运行时逻辑，无需真实环境测试
