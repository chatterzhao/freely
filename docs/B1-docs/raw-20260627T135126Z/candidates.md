---
candidate_id: C-20260627T135126Z-A
status: promoted
source_raw: raw-20260627T135126Z
created_at: 2026-06-27
milestone: M-20260627T135126Z-A
---

## C-20260627T135126Z-A: pr-create merge 策略 + checkpoint scope 放行

- candidate_format_version: v2
- title: pr-create merge 策略 + checkpoint scope 放行
- status: promoted
- decision_reason: merge 比 rebase 更适合多工位并行场景，一次解决冲突不改写历史
- next_action: B2_IBM → dev → pr-merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - pr-create-guarded Step 3 用 merge 替代 rebase
  - checkpoint-guard merge commit 时跳过 scope_count_threshold
- promotion_gate: git merge develop 不再被 checkpoint 拦截，pr-create 成功
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: subagent
  - summary: 审查 pr-create-guarded 和 checkpoint-guard 两处改动
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260627T135126Z-A/issue.md
- milestone: M-20260627T135126Z-A
- session_refs: []
