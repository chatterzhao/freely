---
candidate_id: C-20260630T021946Z-A
status: promoted
source_raw: raw-20260630T021946Z
created_at: 2026-06-30
milestone: M-20260630T021946Z-A
---

## C-20260630T021946Z-A: a2a_tasks 状态对齐 Google A2A 标准

- candidate_format_version: v2
- title: a2a_tasks 状态对齐 Google A2A 标准 — input-required + canceled
- status: promoted
- decision_reason: `blocked` 是非标准状态名，Google A2A 对应态是 `input-required`。缺少 `canceled` 终止态。修改范围明确（a2a_task.py State class + SQLite CHECK + 3 个 A2A 文档 + wt-close 注释），不动 exit kind 映射层
- next_action: 进入 B2_IBM → 物化 I-* issue → pre-tests → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - a2a_task.py: State 常量使用标准名 `INPUT_REQUIRED = "input-required"`，新增 `CANCELED = "canceled"`
  - SQLite CHECK constraint 更新
  - A2A 文档中的状态引用更新
  - wt-close 注释更新
  - exit kind `worker_blocked` 保留不变
  - worker agent prompt 中状态指令更新为 `input-required`
- promotion_gate: all tests GREEN + merge
- open_questions:
  - 历史 DB 中 `state=blocked` 的行是否需要迁移？（决定：不迁移，新 task 用新 state，旧 task 已完成）
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - verdict: pass
- promoted_issue_path: docs/epics/a2a-state-standard/state-rename/raw-20260630T021946Z/issues/I-20260630T021946Z-A.md
- milestone: M-20260630T021946Z-A
- session_refs: []
