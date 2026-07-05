---
candidate_id: C-20260625T131154Z-A
status: promoted
source_raw: raw-20260625T131154Z54Z
created_at: 2026-06-25
milestone: M-20260625T131154Z-A
---

## C-20260625T131154Z-A: legacy issue

- candidate_format_version: v2
- title: pr-create-guarded Step 3 用 rebase 替代 merge
- status: promoted
- decision_reason: merge commit 跨 scope 触发 checkpoint-guard 拦截，rebase 逐个重放避免此问题
- next_action: 合并到 develop → 关闭 #3503
- revisit_trigger: N/A
- acceptance_criteria:
  - pr-create-guarded Step 3: git pull --rebase 替代 git merge
  - push: --force-with-lease 支持 rebase 后的历史重写
  - 冲突错误信息：更新为 rebase 术语
- promotion_gate: 修改完成且语法无误
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: inline
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260625T131154Z-A/issue.md
- milestone: M-20260625T131154Z-A
- session_refs: []
