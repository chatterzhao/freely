---
b1_id: B1-20260627T234054Z
phase_state: completed
source_raw: raw-20260627T234054Z
produced_candidate: C-20260627T234054Z-A
---
# B1: wt-create assignee check
## Problem
多人可同时 pull 同一个 issue 创建工位
## Fix
pull_raw_issue 前检查平台 assignee: 已分配→拒绝, 未分配→自动认领
## Candidate
C-20260627T234054Z-A, promoted
