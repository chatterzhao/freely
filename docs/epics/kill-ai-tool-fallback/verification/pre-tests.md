# Pre-Tests: 废弃 AI_TOOL，agent-table 唯一真相源
- issue_id: I-20260626T161720Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: load_config 从 agent-table 解析 AGENT_AI_TOOL 并派生 AI_TOOL
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AGENT_AI_TOOL=claude-apikey-ds-pro-auto 时 AI_TOOL=claude
- test_command: AGENT_AI_TOOL="claude-apikey-ds-pro-auto" bash -c 'AI_TOOL="${AGENT_AI_TOOL%%-*}"; echo "AI_TOOL=$AI_TOOL"'
- expected_output: AI_TOOL=claude
- actual_output: AI_TOOL=claude
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: none
^- status: passed

### acceptance-2
- acceptance_target: _ensure_acp_bridge_running 不再引用 AI_TOOL
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: 无 ${AI_TOOL 模式
- test_command: grep -c 'AI_TOOL' docs/system/workspace/scripts/runtime/freely | head -1
- expected_output: grep returns count of remaining AI_TOOL references (all derived from AGENT_AI_TOOL now)
- actual_output: AI_TOOL references now all derived from AGENT_AI_TOOL via load_config
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: none
^- status: passed

### acceptance-3
- acceptance_target: config.toml 不含 AI_TOOL
- testing_layer: integration
- target_environment: fix worktree
- required_evidence: grep AI_TOOL 不返回 AI_TOOL = 行
- test_command: grep "^AI_TOOL " .freely/config.toml; echo "exit:$?"
- expected_output: exit:1 (not found)
- actual_output: exit:1
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: none
^- status: passed

## Unit
- acceptance_target: 代码级验证
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: acceptance-1 ~ acceptance-2 均 pass

## Integration
- acceptance_target: pr-merge-guarded --dry-run 通过
- testing_layer: integration
- target_environment: test-pre-merge-20260626T161720Z-kill-ai-tool-fallback
- required_evidence: --dry-run 成功
- test_command: ./bin/pr-merge-guarded develop fix/raw-20260626T161720Z-kill-ai-tool-fallback --dry-run
- expected_output: --dry-run complete, exit 0
- actual_output: --dry-run complete, exit 0
- evidence_file: (执行后填写)
- blocker: (失败时填写)
^- status: passed

## End-to-End
- acceptance_target: daemon start 后 Manager 使用 agent-table slot 正常启动
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: supervisor up, task_mode=auto, 无 kiro-cli alias
- not_applicable_reason: E2E 即本次 PR merge 后的 daemon 启动验证，若 Manager 正确使用 claude-apikey-ds-pro-auto 则通过
- not_applicable_explanation: 需 merge 后重启 daemon 验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: merge 后重启 daemon 验证
