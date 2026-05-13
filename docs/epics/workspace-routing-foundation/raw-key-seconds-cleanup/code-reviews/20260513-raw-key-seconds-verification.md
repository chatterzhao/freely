# Code Review / Verification: raw key seconds cleanup

- issue_id: I-20260513T010343Z-A
- reviewer: AI
- reviewed_at: 2026-05-13

## Changes Verified

1. `freely` L9667, L12069, L13584, L13631: `[0-9]{6}` → `[0-9]{4,6}` — regex accepts both 4-digit (minute) and 6-digit (second) precision
2. `wt-create` L11, L37, L40, L188, L189, L191: help/error messages updated to `YYYYMMDDTHHMM[SS]Z`
3. 10+ doc files: format text updated to reflect seconds precision

## Implementation Decision Note

- decision: All YYYYMMDDTHHMMZ → YYYYMMDDTHHMM[SS]Z, regex `[0-9]{6}` → `[0-9]{4,6}`
- why_this: I-20260507T143545Z-A 的 timestamp-seconds-upgrade 未完成，遗留 14 处
- alternatives_considered: 不改 docs（拒绝：docs 与代码不一致会导致混淆）
- boundary_non_goals: 不改变 raw key 整体格式规范，仅修复遗漏
- residual_risk: 无——只是提升 regex 兼容性 + 修正文档描述
