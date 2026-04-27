# Candidates - 20260426-0000--opencode-direct-launcher-integration

- Source brainstorm: `docs/pre-brainstorms/20260426-0000--opencode-direct-launcher-integration/brainstorms.md`

### C-20260426-0000-A

- title: `Add opencode direct launcher integration`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- candidate_status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- problem: `Freely runtime recognizes opencode as a valid tool name but has no launch implementation. The user needs to switch from codex to opencode due to API balance constraints.`
- why_now:
  - codex API balance is exhausted (INSUFFICIENT_BALANCE on vikeyai.com)
  - opencode is installed (v1.14.26) and has deepseek-v4-pro configured
  - minimal change: only add launch case + session extraction + tool validation
  - no new architecture or subsystem
- proposed_scope:
  - add `opencode` case to `tool_run_direct_from_prompt_file` in tool-launchers.sh
  - add `opencode` session ID extraction pattern in monitor-ai-cli.sh
  - add `opencode` to tool classification functions (accepts_explicit_resume_target, prefers_explicit_resume_target)
  - add `opencode` to tool validation lists in freely and start-lead-agent.sh
- non_goals:
  - full opencode probe/watchdog parity with codex
  - opencode slot/account switching support
  - opencode ACP adapter support
  - opencode --add-dir boundary support
- promoted_issue_id: `I-20260426-0001-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md`
- next_action: `Promoted to I-20260426-0001-A. Complete pre-tests and guarded develop merge.`
- next_action: `Absorbed into I-20260401-0840-A. No independent issue needed.`
- session_refs:
  - {tool: opencode, session_id: "20260426-opencode-integration", jsonl_path: "unavailable://manual", role: "author"}
