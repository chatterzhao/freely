---
candidate_id: C-20260708T122837Z-A
status: absorbed
source_raw: raw-20260708T122837Z
milestone: M-20260708T122837Z-A
---
## C-20260708T122837Z-A: scan stage + batch
- status: absorbed
- absorbed_into: `I-20260708T122837Z-A`
- milestone: `M-20260708T122837Z-A`
- decision_reason: 增量改造——保留新 scan 改进，恢复旧 scan 的 stage 分级 + batch 聚合 + derive_action
- promoted_issue_id: I-20260708T122837Z-A
- promoted_issue_path: docs/B2-docs/ibm/b2-governance/raw-20260708T122837Z/issues/I-20260708T122837Z-A.md
- promotion_gate: scan 输出每条 item 含 stage + next_action + platform_sync_batch 聚合
- acceptance_criteria:
  - 每条 item 有 stage 字段
  - 每条 item 有具体 next_action
  - platform_sync_batch 聚合 sync 类 item
  - _derive_action 根据 stage 推导操作
