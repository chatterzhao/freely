---
candidate_id: C-20261127T120426Z-A
status: promoted
source_raw: raw-20261127T120426Z
created_at: 2026-11-27
milestone: M-20261127T120426Z-A
---

## C-20261127T120426Z-A: 封装 comment-delete
- candidate_format_version: v2
- title: 按 local_id 显式删除平台单条评论
- status: promoted
- promoted_issue_id: I-20261127T120426Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261127T120426Z/issues/I-20261127T120426Z-A.md
- milestone: M-20261127T120426Z-A
- decision_reason: 副本重复评论无法用封装命令清理，导致 raw-reconciliation 永久阻塞
- acceptance_criteria: 显式 platform/comment-id；映射校验；失败透传；无调用方 gh/curl
- promotion_gate: B0 判定为实现未完成
- open_questions: []
