---
candidate_id: C-20260707T025106Z-A
status: absorbed
source_raw: raw-20260707T025106Z
created_at: 2026-07-07
milestone: M-20260707T025106Z-A
---

## C-20260707T025106Z-A: pr-review-guarded 工位清洁检查 + pr-merge-guarded 兜底

- candidate_format_version: v2
- title: fix — pr-review-guarded 增加审查前+后工位清洁检查，pr-merge-guarded 增加兜底检查
- status: absorbed
- decision_reason: Option B — pr-review-guarded 审查前入口闸门 + 审查后出口闸门 + pr-merge-guarded 最后防线，三个检查点形成完整覆盖
- next_action: B2_IBM 物化 I-* issue → dev 实现 2 个文件的清洁检查逻辑
- revisit_trigger: 未来新增流程阶段命令时也需考虑清洁检查
- acceptance_criteria:
  - pr-review-guarded 审查前检查：dirty 时阻塞，列出 dirty 文件，给出 3 种修复方案（commit/stash/gitignore）
  - pr-review-guarded 审查后检查：review 产生新文件/修改时阻塞，要求 git add + git commit
  - pr-merge-guarded 合并前兜底检查：dirty 时阻塞，提示可能遗漏了 review 修改
  - 错误消息必须正向引导：说清问题 + 列出具体文件 + 给出修复命令 + 不包含丢弃操作建议
  - 检查逻辑与 pr-create-guarded Step 0a 一致（git status --porcelain + git ls-files --others）
- promotion_gate: 2 个文件修改完成，错误消息符合设计原则
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260707T025106Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260707T025106Z/issues/I-20260707T025106Z-A.md
- milestone: M-20260707T025106Z-A
- session_refs: []
