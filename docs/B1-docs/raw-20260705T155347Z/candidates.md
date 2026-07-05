---
candidate_id: C-20260705T155347Z-A
status: promoted
source_raw: raw-20260705T155347Z
milestone: M-20260705T155347Z-A
---

## C-20260705T155347Z-A: legacy issue

- candidate_format_version: v2
- title: B1/B2 目录结构重构 + 8 epic 收敛 + 全量 skill/门禁路径更新
- status: promoted
- decision_reason: |
    B1 flat raw-{key}/ 目录统一标识符；
    B2 {epic}/{story}/raw-{key}/ 8 层分层；
    skill/代码路径引用全部更新为新结构；
    历史文件只搬不修内部引用。
- next_action: 进入 B2 设计阶段，产出 prd + pre-tests + tasks
- revisit_trigger: skill 更新后发现新 issue 仍写入旧路径
- acceptance_criteria:
  - B1 skill 中 brainstorms/candidates 写入路径改为 `docs/B1-docs/raw-{key}/`
  - B2 skill 中全部产物路径改为 `docs/B2-docs/{epic}/{story}/raw-{key}/`
  - pr-review-guarded 中 `find docs/epics` → `find docs/B2-docs`
  - check-epics-map 改为扫描 `docs/B2-docs/`
  - epics-map.svg 删除重建，对应 8 epic 结构
  - 历史文件迁移到新目录，旧目录清理
  - milestones.md 路径引用更新
- promotion_gate: 所有 P0 文件已修改 + bash -n 通过 + epics-map 对齐
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260705T155347Z-A
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260705T155347Z-A/issue.md
- milestone: M-20260705T155347Z-A
- session_refs: []
