---
candidate_id: C-20260705T010030Z-A
status: promoted
source_raw: raw-20260705T010030Z
created_at: 2026-07-05
milestone: M-20260705T010030Z-A
---

## C-20260705T010030Z-A: wt-close --raw-key 唯一入口重构

- candidate_format_version: v2
- title: wt-close 重构 — --raw-key 唯一必填参数，自动发现双工位
- status: promoted
- decision_reason: |
  消除 --branch 入口和 test-pre-merge disposable 路径，
  统一为 --raw-key 唯一入口，命令自动发现两个工位。
- next_action: B2 设计 → dev 实现 → merge
- revisit_trigger: N/A（已 promote）
- acceptance_criteria:
  - wt-close 只有 --raw-key 一个入口参数
  - _extract_issue_id 函数已删除
  - test-pre-merge disposable 路径已删除
  - usage 和所有错误提示指向 --raw-key
  - bash -n 语法通过
- promotion_gate: 语法通过 + 静态审查通过
- open_questions: []
- acceptance_reviews:
  - reviewer: claude
  - mode: plan-subagent
  - summary: 审查 wt-close 重构是否符合设计意图
  - verdict: pass
- promoted_issue_id: I-20260705T010030Z-A
- promoted_issue_path: docs/epics/worktree-close/rawkey-unify/raw-20260705T010030Z/issues/I-20260705T010030Z-A.md
- milestone: M-20260705T010030Z-A
- session_refs: []
