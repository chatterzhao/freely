# Candidates - 20260426-0001--ai-tool-alias-support

- Source brainstorm: `docs/pre-brainstorms/20260426-0001--ai-tool-alias-support/brainstorms.md`

### C-20260426-0001-A

- title: `AI_TOOL alias resolution and AI_TOOL_EXTRA_ARGS support`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- candidate_status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- problem: `Freely hardcodes tool binaries. Users need to use shell aliases (ccds, ccglm) that bundle provider/model/settings config.`
- why_now:
  - codex API balance exhausted; user switching to ccds (Claude Code + deepseek)
  - minimal change: alias resolution + extra args injection, no new subsystem
  - AI_TOOL_EXTRA_ARGS gives users a config-only way to customize tool launch
- proposed_scope:
  - alias resolution in tool-launchers.sh (zsh alias → binary + extra args)
  - AI_TOOL_EXTRA_ARGS injection in all tool exec lines
  - AI_TOOL_FAMILY override for custom tool family detection
- non_goals:
  - session pattern auto-detection
  - removing existing tool family cases
  - full generic launcher (keeps backward compat)
- absorbed_by_issue: `I-20260426-0000-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md`
- absorbed_by_issue_path: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md`
- absorption_reason: `Alias resolution is part of the same tool launcher enhancement as opencode integration. Absorbed into the new canonical issue I-20260426-0000-A.`
- decision_reason: `This candidate covers the AI_TOOL alias resolution change. Since it is implemented in the same files as the opencode launcher, it shares the same canonical owner issue I-20260426-0000-A.`
- session_refs:
  - {tool: ccds, session_id: "20260426-alias-support", jsonl_path: "unavailable://manual", role: "author"}
