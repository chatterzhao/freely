---
issue_id: I-20260624T151020Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260624T151020Z-A
- issue_path: docs/issues/I-20260624T151020Z-A/issue.md
## Implementation Decision Note
- decision: 修复 wt-close 调用 pretests-retirement-gate 时传递 --project + --worktree-path
- why_this: gate 从第一天就要求这些标志，wt-close 传参一直错
- alternatives_considered: 改 gate 接受位置参数（不如修调用方）
- boundary_non_goals: gate 本身不改
- residual_risk: 无
