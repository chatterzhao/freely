---
candidate_id: C-20260630T021946Z-A
status: promoted
source_raw: raw-20260630T021946Z
created_at: 2026-06-30
milestone: M-20260630T021946Z-A
---

## C-20260630T021946Z-A: legacy issue

- candidate_format_version: v2
- title: a2a_tasks 状态对齐 Google A2A 标准 — input-required + canceled
- status: promoted
- decision_reason: `blocked` 是非标准状态名，Google A2A 对应态是 `input-required`。缺少 `canceled` 终止态。修改范围明确（a2a_task.py State class + SQLite CHECK + 3 个 A2A 文档 + wt-close 注释），不动 exit kind 映射层
- next_action: 进入 B2_IBM → 物化 I-* issue → pre-tests → RED → dev → GREEN → PR
- revisit_trigger: N/A
- acceptance_criteria:
  - a2a_task.py: State 常量全标准名；`--kind` → `--state`，值直接用 A2A state
  - 删除 exit kind 映射层（`'worker_blocked'→'input-required'` 等），`--state` 值直接写 DB
  - 所有 `--kind worker_blocked` 调用处改为 `--state input-required`
  - A2A 文档全部更新
  - wt-close + agent prompt 模板更新
- promotion_gate: all tests GREEN + merge
- open_questions:
  - 历史 DB 中 `state=blocked` 的行是否需要迁移？（决定：不迁移，新 task 用新 state，旧 task 已完成）
- acceptance_reviews:
  - reviewer: claude
  - mode: in-session
  - verdict: pass
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260630T021946Z-A/issue.md
- milestone: M-20260630T021946Z-A
- session_refs: []
