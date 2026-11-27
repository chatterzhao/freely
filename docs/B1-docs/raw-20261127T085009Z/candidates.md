---
candidate_id: C-20261127T085009Z-A
status: promoted
source_raw: raw-20261127T085009Z
created_at: 2026-11-27
milestone: M-20261127T085009Z-A
---

## C-20261127T085009Z-A: 单平台 legacy raw 物化互锁
- candidate_format_version: v2
- title: wt-create 显式 source-platform 补齐副本
- status: promoted
- promoted_issue_id: I-20261127T085009Z-A
- promoted_issue_path: docs/B2-docs/worktree-lifecycle/worktree-seed/raw-20261127T085009Z/issues/I-20261127T085009Z-A.md
- milestone: M-20261127T085009Z-A
- decision_reason: 参数已存在却未接入判据，形成工位与副本互锁
- acceptance_criteria: 显式来源跳过前置校验且审计可见；物化后 issue-sync create 补齐；失败非零
- promotion_gate: B0 判定为实现未完成
- open_questions: []
