---
candidate_id: C-20260619T045626Z-A
status: promoted
source_raw: raw-20260619T045626Z26Z
created_at: 2026-06-19
milestone: M-20260619T045626Z-A
---

## C-20260619T045626Z-A: legacy issue

- candidate_format_version: v2
- status: promoted
- decision_reason: 行业对比(GitHub/GitLab/Mergify都是server-side queue)，Freely缺少并发保护
- next_action: 实现flock + MERGE_HEAD cleanup
- acceptance_criteria:
  - do_initial_merge 前 acquire_merge_lock
  - trap EXIT 清理 MERGE_HEAD
- promotion_gate: 代码修改完成
- promoted_issue_path: docs/issues/I-20260619T045626Z-A/issue.md
- milestone: M-20260619T045626Z-A
