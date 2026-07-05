# Candidates - 20260426-0002--break-glass-agents-guidance

- Source brainstorm: `docs/B1-docs/20260426-0002--break-glass-agents-guidance/brainstorms.md`

### C-20260426-0002-A

- title: `Harden AGENTS.md break-glass guidance`
- source_class: `discovery`
- route_kind: `pre_brainstorm`
- phase_state: `done_pre_brainstorm`
- status: `proposed`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P1`
- promoted_issue_path: ""
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



- next_action: `If the guidance change proves sufficient during continued dogfooding, promote to a formal issue. Otherwise revisit and strengthen.`
- session_refs:
  - {tool: ccds, session_id: "20260426-agents-fix", jsonl_path: "unavailable://manual", role: "author"}
