---
b1_id: B1-20260624T151020Z
phase_state: completed
source_raw: raw-20260624T151020Z20Z
source_url: https://github.com/chatterzhao/freely/issues/3440
produced_candidate: C-20260624T151020Z-A
created_at: 2026-06-24
---

# B1_IBM: wt-close pretests-retirement-gate 传参修复

## Problem
wt-close 调用 pretests-retirement-gate 时传参格式错误，gate 从引入至今从未正确调用。

## Brainstorm
### Option A: 修复 wt-close 传参 ✅
改为 --project + --worktree-path 标志。
### Option B: 改 gate 接受位置参数
不如修调用方。

## Decision: Option A
一行修改，gate 本身不需要改。
## Candidate
- candidate_id: C-20260624T151020Z-A
- status: promoted
