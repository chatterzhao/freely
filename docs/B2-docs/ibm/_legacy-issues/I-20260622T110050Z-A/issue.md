---
local_id: I-20260622T110050Z-A
kind: I
phase_state: completed
source_candidate: docs/B1-docs/raw-20260622T110050Z50Z/candidates.md#C-20260622T110050Z-A
verification_artifact_dir: docs/B2-docs/I-20260622T110050Z-A/code-reviews
raw_refs:
  - raw-20260622T110050Z50Z
candidate_refs:
  - C-20260622T110050Z-A
created_at: '2026-06-22T11:00:50Z'
updated_at: '2026-06-22T11:00:50Z'
---

# I-20260622T110050Z-A: wt-close Error Messages Guide Instead of Push --force

## Summary
wt-close 的 phase_state 和 pretests-retirement-gate 错误提示改为三路引导：
1. 实现完但状态忘更新 → 更新重试
2. 没做完 → 继续工作
3. 放弃了 → --force + --reason

## Changes
- `docs/system/workspace/scripts/worktree/wt-close`: Phase 1 Checks 错误提示

## Acceptance Criteria
- [x] phase_state 不匹配时显示三路引导
- [x] pretests-retirement-gate 失败时显示三路引导
- [x] 不再直接说 "Use --force to skip"
