---
candidate_id: C-20260626T161720Z-A
status: promoted
source_raw: raw-20260626T161720Z
created_at: 2026-06-26
milestone: M-20260626T161720Z-A
---

## C-20260626T161720Z-A: legacy issue

- candidate_format_version: v2
- title: 废弃 AI_TOOL，agent-table 唯一真相源
- status: promoted
- decision_reason: AI_TOOL alias残留导致 Manager 无法启动。agent-table 是正确定义 per-agent slot 的地方，应成为唯一源。
- next_action: B2_IBM → pr-create → pr-merge → wt-close
- revisit_trigger: N/A
- acceptance_criteria:
  - load_config 从 agent-table 解析 AGENT_AI_TOOL，自动派生 AI_TOOL
  - _ensure_acp_bridge_running 不再降级到 AI_TOOL
  - sync_tooling 不写 AGENT_AI_TOOL 到 config
  - freely-review/pr-review-guarded 使用 AGENT_AI_TOOL
  - freely init 生成 agent-table.toml 模板
  - config.toml 移除 AI_TOOL 键
- promotion_gate: 所有修改完成并提交
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent-review
  - summary: 子代理 review 确认改动正确，发现并修复 pr-review-guarded worker-id.env 不一致问题
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260626T161720Z-A/issue.md
- milestone: M-20260626T161720Z-A
- session_refs: []
