# Candidates: context-window-aware-session-rotation

- candidate_id: `C-20260316-1839`
- title: 将 Codex context window 占用阈值接入 session rotation 与 continuity 提醒
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
- acceptance_hint:
  - runtime 能从 Codex session jsonl 解析最近 `total_tokens / model_context_window`
  - `warn` 阈值触发下一轮 continuity 提醒
  - `rotate` 阈值触发 `fresh_with_handoff`
  - handoff/status 能显示 `jsonl_path` 与 `context_ratio`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}
