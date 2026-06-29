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
- actual_output: direct,acp
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: none
^- status: passed

### acceptance-2
- acceptance_target: tool-registry-query.py aliases 返回逗号分隔值
- testing_layer: unit
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: 输出 `cc,cc-use-codex-cli,kiro-cli,iflow,claude-code`（逗号分隔）
- test_command: python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml claude aliases
- expected_output: cc,cc-use-codex-cli,kiro-cli,iflow,claude-code
- actual_output: cc,cc-use-codex-cli,kiro-cli,iflow,claude-code
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: none
^- status: passed

### acceptance-3
- acceptance_target: cmd_feedback 拒绝无类型前缀的标题
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "title must start with a type prefix"
- test_command: ./bin/freely feedback --title "bad title without prefix" --body "## test body with enough characters to satisfy the fifty character minimum requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*title must start with a type prefix.*exit:1
- actual_output: "[ERROR] title must start with a type prefix: fix, feat, docs, refactor, chore, test, build, ci, perf, style" / exit:1
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: none
^- status: passed

### acceptance-4
- acceptance_target: cmd_feedback 拒绝过长标题
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "title too long"
- test_command: ./bin/freely feedback --title "fix: $(python3 -c "print('x'*80)")" --body "## test body with enough characters to satisfy the fifty character minimum requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*title too long.*exit:1
- actual_output: "[ERROR] title too long: 113 chars (max 100 including [RAW-{key}] prefix)" / exit:1
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker: none
^- status: passed

### acceptance-5
- acceptance_target: cmd_feedback 拒绝过短 body
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "body too short"
- test_command: ./bin/freely feedback --title "fix: test" --body "short" 2>&1; echo "exit:$?"
- expected_output: ERROR.*body too short.*exit:1
- actual_output: "[ERROR] body too short (5 non-ws chars, need ≥ 50)" / exit:1
- evidence_file: .freely/run/test-evidence/acceptance-5.log
- blocker: none
^- status: passed

### acceptance-6
- acceptance_target: cmd_feedback 拒绝无 ## section 的 body
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: exit code 1，stderr 含 "body must contain at least one ##"
- test_command: ./bin/freely feedback --title "fix: test" --body "this body has no section heading just plain text that meets the minimum character count requirement" 2>&1; echo "exit:$?"
- expected_output: ERROR.*body must contain at least one ##.*exit:1
- actual_output: "[ERROR] body must contain at least one ## section heading" / exit:1
- evidence_file: .freely/run/test-evidence/acceptance-6.log
- blocker: none
^- status: passed

## Unit
- acceptance_target: Python comma-join 和 bash alias loop 的单元验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: acceptance-1 + acceptance-2 均 passed

## Integration
- acceptance_target: cmd_feedback 4 项格式校验全部正确拦截
- testing_layer: integration
- target_environment: test-pre-merge-20260626T150328Z-toml-array-comma-join
- required_evidence: acceptance-3 ~ acceptance-6 均 pass
- test_command: echo "verified by acceptance-3 through acceptance-6 in Acceptance Items section"
- expected_output: All 4 feedback format validations return exit 1 with correct error messages

## End-to-End
- acceptance_target: Freely daemon start 后 ACP bridge 正常启动，不再出现 unsupported adapter 错误
- testing_layer: end-to-end
- target_environment: develop（合并后）
- required_evidence: daemon start → supervisor up → ai cycle 正常 launch
- not_applicable_reason: Freely daemon requires clean develop tree and cannot be started from fix worktree; E2E verification deferred to post-merge real-environment check. All code-level behaviors are covered by acceptance-1 through acceptance-6 above.
- not_applicable_explanation: 当前 fix worktree 无法启动完整的 Freely daemon 端到端测试（daemon start 要求 clean develop），改为合并后通过 Real-Environment 验证。代码级正确性已由 acceptance-1 ~ acceptance-6 充分覆盖。

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: Freely daemon 端到端验证需合并到 develop 后重启执行
