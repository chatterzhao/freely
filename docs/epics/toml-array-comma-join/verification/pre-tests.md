# Pre-Tests: TOML array comma-join + feedback validation + bash 3.2 guard
- issue_id: I-20260626T150328Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: tool-registry-query.py adapters.supported 返回逗号分隔值
- testing_layer: unit
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: 输出 `direct,acp` 而非 `direct acp`
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude adapters.supported
- expected_output: direct,acp
- actual_output: (由 skill:freely-test-execution 执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-1.log)
- blocker: (失败时填写)
- status: pending

### acceptance-2
- acceptance_target: tool-registry-query.py aliases 返回逗号分隔值
- testing_layer: unit
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: 输出 `cc,cc-use-codex-cli,kiro-cli,iflow,claude-code`（逗号分隔）
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude aliases
- expected_output: cc,cc-use-codex-cli,kiro-cli,iflow,claude-code
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-2.log)
- blocker: (失败时填写)
- status: pending

### acceptance-3
- acceptance_target: cmd_feedback 拒绝无类型前缀的标题
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "title must start with a type prefix"
- test_command: ./bin/freely feedback --title "bad title without prefix" --body "## test body with enough characters to satisfy the fifty character minimum requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*title must start with a type prefix.*exit:1
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-3.log)
- blocker: (失败时填写)
- status: pending

### acceptance-4
- acceptance_target: cmd_feedback 拒绝过长标题
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "title too long"
- test_command: ./bin/freely feedback --title "fix: $(python3 -c "print('x'*80)")" --body "## test body with enough characters to satisfy the fifty character minimum requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*title too long.*exit:1
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-4.log)
- blocker: (失败时填写)
- status: pending

### acceptance-5
- acceptance_target: cmd_feedback 拒绝过短 body
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "body too short"
- test_command: ./bin/freely feedback --title "fix: test" --body "short" 2>&1; echo "exit:$?"
- expected_output: ERROR.*body too short.*exit:1
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-5.log)
- blocker: (失败时填写)
- status: pending

### acceptance-6
- acceptance_target: cmd_feedback 拒绝无 ## section 的 body
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "body must contain at least one ##"
- test_command: ./bin/freely feedback --title "fix: test" --body "this body has no section heading just plain text that meets the minimum character count requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*body must contain at least one ##.*exit:1
- actual_output: (执行后填写)
- evidence_file: (执行后填写，指向 .freely/run/test-evidence/acceptance-6.log)
- blocker: (失败时填写)
- status: pending

## Unit
- acceptance_target: Python comma-join 和 bash alias loop 的单元验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: acceptance-1 + acceptance-2 均 passed

## Integration
- acceptance_target: cmd_feedback 4 项格式校验全部正确拦截
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: acceptance-3 ~ acceptance-6 均 passed

## End-to-End
- acceptance_target: Freely daemon start 后 ACP bridge 正常启动，不再出现 unsupported adapter 错误
- testing_layer: end-to-end
- target_environment: develop（合并后）
- required_evidence: daemon start → supervisor up → ai cycle 正常 launch

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 需要重启 Freely daemon 进行端到端验证，在当前 PR 合并后执行
