---
candidate_id: C-20260629T164530Z-A
status: promoted
source_raw: raw-20260629T164530Z
created_at: 2026-06-29
milestone: M-20260629T164530Z-A
---

## C-20260629T164530Z-A: legacy issue

- candidate_format_version: v2
- title: wt-close --raw-key flag 重构
- status: promoted
- decision_reason: 上版 PR positional 参数与 flag 模式冲突，重构为正交 flag 设计
- next_action: 实现 → RED → GREEN → PR → merge
- revisit_trigger: N/A
- acceptance_criteria:
  - --raw-key 支持 raw-{key}、fix/raw-{key}-{slug}、feature/raw-{key}-{slug} 三种输入
  - --branch 保留原有行为
  - --raw-key + --platform-only 不走分支解析
  - 修复 + 前缀和 unbound variable
- promotion_gate: 实现 + 测试通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260629T164530Z-A/issue.md
- milestone: M-20260629T164530Z-A
- session_refs: []
