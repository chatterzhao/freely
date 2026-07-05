---
candidate_id: C-20260627T084551Z-A
status: promoted
source_raw: raw-20260627T084551Z
created_at: 2026-06-27
milestone: M-20260627T084551Z-A
---

## C-20260627T084551Z-A: run-acp-prompt.py fork 改用 session/fork

- candidate_format_version: v2
- title: run-acp-prompt.py fork 改用 session/fork
- status: promoted
- decision_reason: session/fork 是 ACP 官方规范，Claude+OpenCode 已支持
- next_action: B2_IBM → dev → pr-merge
- revisit_trigger: N/A
- acceptance_criteria:
  - fork 路径 try session/fork，失败降级 session/new
  - ensure-codex-acp 读 tool-registry.toml
- promotion_gate: Claude+OpenCode worker fork 成功缓存命中
- open_questions: []
- acceptance_reviews:
  - reviewer: claude; mode: subagent; verdict: pass
- promoted_issue_path: docs/issues/I-20260627T084551Z-A/issue.md
- milestone: M-20260627T084551Z-A
- session_refs: []
