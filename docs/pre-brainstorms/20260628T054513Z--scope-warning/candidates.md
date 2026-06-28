---
candidate_id: C-20260628T054513Z-A
status: promoted
source_raw: raw-20260628T054513Z
created_at: 2026-06-28
milestone: M-20260628T054513Z-A
---

## C-20260628T054513Z-A: scope 硬阻塞 → 警告

- candidate_format_version: v2
- title: checkpoint-guard 从硬阻塞改为建议警告
- status: promoted
- decision_reason: 文件数不等于 scope 爆炸，硬阻塞逼迫拆分同一问题的修改
- next_action: B2_IBM → pr-create → merge
- revisit_trigger: N/A
- acceptance_criteria:
  - pre-commit hook 移除 --fail-on-required
  - scope 超标时输出警告不阻塞
  - AGENTS.md.example 写入提交规范
- promotion_gate: commit 不被 scope 阻塞即可
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: plan
  - summary: 验证 scope 硬阻塞→警告，pre-commit 不再 exit 1
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260628T054513Z-A/issue.md
- milestone: M-20260628T054513Z-A
- session_refs: []
