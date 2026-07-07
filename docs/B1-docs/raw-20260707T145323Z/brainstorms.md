---
b1_id: B1-20260707T145323Z
phase_state: completed
source_raw: raw-20260707T145323Z
produced_candidate: C-20260707T145323Z-A
---
# B1: issue-sync 幂等性修复 + platform-adapter bug 修复 + review 指南强化

## Discovery

### value_check: P0 阻塞
1. pr-merge-guarded 死循环——issue-sync close 每次写 updated_at 导致无限 commit
2. #3808 重构引入 search_raw_issue isinstance 反了导致 wt-create 全局阻塞
3. GitHub get_assignees 用 gh api 而非 gh issue view，404 被当 assignee 名

### scope_check
- bin/issue-sync: 删除 1 行
- platform-adapter.py: 修 isinstance + get_assignees → gh issue view
- review-guidelines: 强化行为测试要求

## Decision: 最小改动修复
## Candidate: C-20260707T145323Z-A, promoted
