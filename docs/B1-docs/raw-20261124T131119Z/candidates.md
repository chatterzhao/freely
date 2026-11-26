---
candidate_id: C-20261124T131119Z-A
status: promoted
source_raw: raw-20261124T131119Z
created_at: 2026-11-26
milestone: M-20261124T131119Z-A
---

## C-20261124T131119Z-A: stale linked 孤儿副本关闭封装入口
- candidate_format_version: v2
- title: issue-sync close-orphans 按 local_id 关闭全部平台副本
- status: promoted
- promoted_issue_id: I-20261124T131119Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/issues/I-20261124T131119Z-A.md
- milestone: M-20261124T131119Z-A
- decision_reason: adapter 已有 close-local-id，缺的是 packaged 入口与可操作失败回执
- acceptance_criteria: 命令可达；委托 adapter close-local-id；rc 0/3/1 透传；失败打印重试命令；无调用方 adapter import
- promotion_gate: B0 判定为实现未完成
- open_questions: []
