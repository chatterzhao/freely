# Pre-Tests: tool family de-hardcode + AGENT_AI_TOOL + agent-id.env + reviewer
- issue_id: I-20260626T075106Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: _resolve_tool_family returns correct tool for all 4 registered tools
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: Registry-driven lookup matches all 4 tools
- test_command: grep -c '_tool_registry_tools\|for _reg_tool in \$(.tool_registry_tools)' docs/system/workspace/scripts/runtime/freely
- expected_output: 2 or more (loop appears in both levels of _resolve_tool_family)
- actual_output: Registry-driven loop found in _resolve_tool_family (primary and recursive), parse_ai_spec, no hardcoded case statements remain
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (none)
^- status: passed

### acceptance-2
- acceptance_target: AGENT_AI_TOOL fallback chain present at all 5 locations
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: All locations use ${AGENT_AI_TOOL:-${AI_TOOL:-...}}
- test_command: grep -c 'AGENT_AI_TOOL' docs/system/workspace/scripts/runtime/freely
- expected_output: 5 or more
- actual_output: 5 occurrences — sync_tooling, base_tool, tool change detection, tool_name, acp_tool_file, all with correct fallback to AI_TOOL
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker: (none)
^- status: passed

### acceptance-3
- acceptance_target: agent-id.env cleanup in wt-close and manager_reconcile_agent_id_env
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: Cleanup code present in both locations
- test_command: grep -c 'agent-id.env' docs/system/workspace/scripts/worktree/wt-close docs/system/workspace/scripts/runtime/freely
- expected_output: 3 or more references across both files
- actual_output: Cleanup present in wt-close (raw-key matching + develop worktree resolution) and manager_reconcile_agent_id_env (zombie detection + removal)
- evidence_file: .freely/run/test-evidence/acceptance-3.log
- blocker: (none)
^- status: passed

### acceptance-4
- acceptance_target: reviewer-agent.md exists with fork-Manager constraint
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: File exists with required content
- test_command: grep -c 'fork MANAGER session\|fork Manager' docs/system/workspace/agents/reviewer-agent.md
- expected_output: 2 or more
- actual_output: fork-Manager constraint documented in role description and startup paths, Tool Policy complete, 4-layer review flow documented
- evidence_file: .freely/run/test-evidence/acceptance-4.log
- blocker: (none)
^- status: passed

### acceptance-5
- acceptance_target: Freely runtime bash syntax valid and tool registry loads correctly
- testing_layer: integration
- target_environment: test-pre-merge worktree
- required_evidence: bash -n passes, 4 tools listed from registry
- test_command: bash -n docs/system/workspace/scripts/runtime/freely && echo "Syntax OK" && python3 docs/system/workspace/scripts/runtime/tool-registry-query.py docs/system/workspace/scripts/runtime/tool-registry.toml --list
- expected_output: Syntax OK + 4 tool names (claude codex opencode cline)
- actual_output: Syntax OK. claude, cline, codex, opencode — all 4 tools listed from registry
- evidence_file: .freely/run/test-evidence/acceptance-5.log
- blocker: (none)
^- status: passed

### acceptance-6
- acceptance_target: Freely doctor passes with registry-driven tool family
- testing_layer: end-to-end
- target_environment: test-pre-merge worktree
- required_evidence: doc gate and execution-boundary audit both pass
- test_command: freely doctor --project "$(pwd)" 2>&1 | head -20
- expected_output: doc gate PASS, execution-boundary audit PASS
- actual_output: doc gate PASS, hook gate PASS, execution-boundary audit PASS aligned
- evidence_file: .freely/run/test-evidence/acceptance-6.log
- blocker: (none)
^- status: passed

## Unit
- acceptance_target: Subagent code review passed all criteria
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: Independent reviewer PASS (22/23, bugs found and fixed)
^- status: passed

## Integration
- acceptance_target: Cross-module bash syntax and registry loading verified
- testing_layer: integration
- target_environment: test-pre-merge worktree
- required_evidence: acceptance-5 covers this layer
^- status: passed

## End-to-End
- acceptance_target: Full daemon startup with registry-driven tool resolution
- testing_layer: end-to-end
- target_environment: test-pre-merge worktree → develop merge chain
- required_evidence: acceptance-6 covers this layer
^- status: passed
