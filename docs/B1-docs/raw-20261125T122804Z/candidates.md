---
candidate_id: C-20261125T122804Z-A
status: promoted
source_raw: raw-20261125T122804Z
created_at: 2026-11-26
milestone: M-20261125T122804Z-A
---

## C-20261125T122804Z-A: 生成型 updated 行不参与副本内容判定
- candidate_format_version: v2
- title: raw-reconciliation 归一化 `| updated |` 行，消除结构性漂移
- status: promoted
- promoted_issue_id: I-20261125T122804Z-A
- promoted_issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T122804Z/issues/I-20261125T122804Z-A.md
- milestone: M-20261125T122804Z-A
- decision_reason: 正文 `| updated |` 是从 frontmatter 派生的生成型元数据，有 4 个合法写入者；把它当内容比较会产生无意义且无法根治的 content_diverged。
- acceptance_criteria:
  - `| updated |` 值不同但其余一致 → reconcile ok
  - 人类正文不同 → 仍 content_diverged
  - 不新增平台写通道，不改 `platform_body()` 其他字段
- promotion_gate: B0 判定为设计不完整，AT 红线可复现
- open_questions: []
