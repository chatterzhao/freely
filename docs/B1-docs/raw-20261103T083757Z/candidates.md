---
candidate_id: C-20261103T083757Z-A
status: promoted
source_raw: raw-20261103T083757Z
created_at: 2026-11-26
milestone: M-20261103T083757Z-A
---

## C-20261103T083757Z-A: Gitee delete-branch 端点纠正
- candidate_format_version: v2
- title: 用 Gitee API v5 canonical 分支端点删除远程分支
- status: promoted
- promoted_issue_id: I-20261103T083757Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T083757Z/issues/I-20261103T083757Z-A.md
- milestone: M-20261103T083757Z-A
- decision_reason: GitHub ref 路径在 Gitee 恒 404，fallback 掩盖真实失败
- acceptance_criteria: repo_path_branch 返回 /branches/；delete-branch DELETE + 鉴权 + 回执不变
- promotion_gate: B0 判定为实现偏差
- open_questions: []
