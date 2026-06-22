---
local_id: I-20260622T113847Z-A
kind: I
phase_state: completed
source_candidate: docs/pre-brainstorms/20260622T113847Z--platform-only/candidates.md#C-20260622T113847Z-A
verification_artifact_dir: docs/epics/I-20260622T113847Z-A/code-reviews
raw_refs:
  - raw-20260622T113847Z
candidate_refs:
  - C-20260622T113847Z-A
created_at: '2026-06-22T11:38:47Z'
updated_at: '2026-06-22T11:38:47Z'
---

# I-20260622T113847Z-A: wt-close --platform-only

## Summary
新增 wt-close --platform-only 参数，用于孤儿工位的平台 issue 收口。
纯 API close，不改 develop 本地文件。

## Changes
- wt-close: --platform-only 参数、GATE 门禁、Phase 2 逻辑
- --skip-platform 文档：明确唯一合法场景

## Acceptance Criteria
- [x] --platform-only 关闭 raw issue 和 absorbed I-* issue 的平台 issue
- [x] 不改动 develop 上任何文件
- [x] 必须 --reason
