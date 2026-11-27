---
candidate_id: C-20261127T110239Z-A
status: promoted
source_raw: raw-20261127T110239Z
created_at: 2026-11-27
milestone: M-20261127T110239Z-A
---

## C-20261127T110239Z-A: 可操作的评论失败诊断
- candidate_format_version: v2
- title: closed-issue 评论跳过与 401 语义翻译
- status: promoted
- promoted_issue_id: I-20261127T110239Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T110239Z/issues/I-20261127T110239Z-A.md
- milestone: M-20261127T110239Z-A
- decision_reason: 裸 HTTP 401 无法区分鉴权/路径/平台状态，且重跑制造重复评论
- acceptance_criteria: closed Gitee issue 不 POST 且打印原因；401 翻译含 issue_comment 与修复命令；promote-finalize 重跑不重复
- promotion_gate: B0 判定为实现不完整
- open_questions: []
