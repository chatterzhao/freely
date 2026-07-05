- issue_id: I-20260626T075106Z-A
- kind: fix
- phase_state: completed
- source_candidate: docs/pre-brainstorms/20260626T075106Z--family-registry-driven/candidates.md#C-20260626T075106Z-A
- source_raw: raw-20260626T075106Z
- canonical_issue_path: docs/issues/I-20260626T075106Z-A/issue.md
- pre_tests_path: docs/epics/family-registry-driven/verification/pre-tests.md
- verification_artifact_dir: docs/epics/family-registry-driven/verification
- title: Registry-driven tool family + AGENT_AI_TOOL + agent-id.env cleanup + reviewer-agent

# I-20260626T075106Z-A: tool family de-hardcode + AGENT_AI_TOOL + agent-id.env + reviewer

- source_candidate: docs/pre-brainstorms/20260626T075106Z--family-registry-driven/candidates.md#C-20260626T075106Z-A

## 实现

- _resolve_tool_family: registry-driven loop over _tool_registry_tools
- _tool_session_dir: session.directory_template from registry
- tool_uses_claude_session_id: session.id_format == "uuid"
- tool_prefers_explicit_resume_target: session.supports_resume
- AGENT_AI_TOOL: per-agent slot with fallback chain
- wt-close: agent-id.env cleanup by raw-key
- manager_reconcile_agent_id_env: zombie reaper
- reviewer-agent.md: new agent doc
