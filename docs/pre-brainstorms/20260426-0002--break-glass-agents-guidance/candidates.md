# Candidates - 20260426-0002--break-glass-agents-guidance

- Source brainstorm: `docs/pre-brainstorms/20260426-0002--break-glass-agents-guidance/brainstorms.md`

### C-20260426-0002-A

- title: `Harden AGENTS.md break-glass guidance`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- candidate_status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- problem: `AGENTS.md break-glass guidance was too soft, enabling AI to rationalize bypass during dogfooding.`
- why_now:
  - two break-glass merges occurred during dogfooding that should have been documentation fixes
  - the soft guidance was a contributing factor
- proposed_scope:
  - rewrite AGENTS.md line 114 to list forbidden bypass patterns
  - narrow verified_false_negative to factual errors only
- non_goals:
  - changing LAWS.md §2D (AGENTS.md is guidance, laws are canonical)
  - modifying hook behavior
- absorbed_by_issue: `I-20260426-0000-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/tool-alias-and-opencode-launcher-governance/issues/tool-alias-and-opencode-launcher-governance.md`
- decision_reason: `AGENTS.md is a governance document maintained alongside the tool launcher governance work. This is the developer-facing fix for the break-glass abuse discovered during I-20260426-0000-A dogfooding.`
- session_refs:
  - {tool: ccds, session_id: "20260426-agents-fix", jsonl_path: "unavailable://manual", role: "author"}
