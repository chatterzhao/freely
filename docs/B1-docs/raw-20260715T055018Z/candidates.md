---
candidate_id: C-20260715T055018Z-A
status: promoted
source_raw: raw-20260715T055018Z
created_at: 2026-07-15
milestone: M-20260715T055018Z-A
---

## C-20260715T055018Z-A: scan cache refresh + auto→listen universal

- candidate_format_version: v2
- title: fix scan cache stale on daemon start + auto→listen for all exit kinds
- status: promoted
- decision_reason: 两处小改——删除旧 scan 缓存(1行) + 将 auto→listen 从 stop_ai 专属提升到通用(10行重构)
- next_action: B2→dev 实现
- revisit_trigger: N/A
- acceptance_criteria:
  - daemon start 后首次 build_prompt 触发 scan 刷新
  - tool_unproductive 时 auto→listen 正常切换
  - listen 模式启动后 300s 内刷新 scan 并自动回 auto（如有任务）
- promotion_gate: bash -n + 代码审查
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: manual
  - summary: 审查两处修改的语义正确性
  - verdict: pass
- promoted_issue_id: I-20260715T055018Z-A
- promoted_issue_path: docs/B2-docs/runtime/daemon/raw-20260715T055018Z/issues/I-20260715T055018Z-A.md
- milestone: M-20260715T055018Z-A
- session_refs: []
