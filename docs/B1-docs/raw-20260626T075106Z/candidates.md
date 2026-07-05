---
candidate_id: C-20260626T075106Z-A
status: promoted
source_raw: raw-20260626T075106Z06Z
milestone: M-20260626T075106Z-A
---

## C-20260626T075106Z-A: legacy issue

- candidate_format_version: v2
- title: Registry-driven tool family, per-agent slots, agent-id.env lifecycle, reviewer agent
- status: absorbed
- absorbed_into: I-20260626T075106Z-A
- decision_reason: Hardcoded tool family case statements block new tool additions; agent-id.env lacks cleanup; reviewer agent missing
- next_action: Implement and merge
- revisit_trigger: N/A
- acceptance_criteria:
  - _resolve_tool_family and related functions fully registry-driven
  - AGENT_AI_TOOL per-agent slot variable with fallback
  - agent-id.env cleanup on wt-close and before Manager delegation
  - reviewer-agent.md created with fork-Manager constraint
- promotion_gate: Code implemented + subagent review passed
- open_questions: []
- promoted_issue_path: docs/issues/I-20260626T075106Z-A/issue.md
- milestone: M-20260626T075106Z-A
