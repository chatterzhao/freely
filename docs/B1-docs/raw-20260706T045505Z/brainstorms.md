---
b1_id: B1-20260706T045505Z
phase_state: completed
source_raw: raw-20260706T045505Z
produced_candidate: C-20260706T045505Z-A
---
# B1: wt-create 内置 reopen
## Problem
issue 已 absorbed 后 wt-create 拒绝创建工位，要求手动改 develop 上的 phase_state
## Fix
wt-create 检测到 closed state → 自动改为 proposed（在工位分支，不碰 develop）
## Candidate
- candidate_id: C-20260706T045505Z-A
- status: promoted
