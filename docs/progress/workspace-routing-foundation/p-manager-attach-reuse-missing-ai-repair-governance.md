# Progress: manager-attach-reuse-missing-ai-repair-governance

- issue_id: `I-20260330-2318-A`
- issue_path: `docs/epics/workspace-routing-foundation/manager-attach-reuse-missing-ai-repair-governance/issues/manager-attach-reuse-missing-ai-repair-governance.md`
- phase_state: `in_dev`
- summary: `The false live-status attach regression is now proven to be a manager-only attach gate bug. The patch requires a confirmed running AI PID before manager attach reuse succeeds, while preserving worker attach reuse.`
- current_focus:
  - `land the manager-only attach gate repair in runtime/freely`
  - `keep test-freely-project-command-semantics green with explicit manager-missing-ai coverage`
  - `rerun one protected develop live validation after merge`
- evidence:
  - `real_trigger: 2026-04-01 develop live run emitted tool_auto_switch_selected followed by supervisor_attach_reuse with ai_pid_state=missing role_hint=manager`
  - `tests: bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
