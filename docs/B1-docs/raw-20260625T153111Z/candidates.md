---
candidate_id: C-20260625T153111Z-A
status: promoted
source_raw: raw-20260625T153111Z
created_at: 2026-06-25
milestone: M-20260625T153111Z-A
---

## C-20260625T153111Z-A: legacy issue

- candidate_format_version: v2
- title: .freely/agent-table.toml — agent 池声明 + 解析器 + wt-create 集成
- status: promoted
- decision_reason: 独立文件职责清晰，pool 模式支持扩容，{role}_slot 对应终端 alias
- next_action: 实现解析器 → 集成 wt-create → Manager 巡逻集成
- revisit_trigger: N/A
- acceptance_criteria:
  - agent-table.toml 格式规范（[[agents]] + [[agent_pools]]）
  - Python 解析器：支持按 worker_id 查 slot、按 role 列实例、查空闲
  - wt-create 集成：读表分配空闲 worker_id，写对应 slot 到工位 config.toml
  - Manager patrol 集成：读表查空闲 worker
- promotion_gate: 解析器可用 + wt-create 正确分配 slot
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T153111Z-A/issue.md
- milestone: M-20260625T153111Z-A
- session_refs: []
