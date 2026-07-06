---
b1_id: B1-20260704T052343Z
phase_state: completed
source_raw: raw-20260704T052343Z
produced_candidate: C-20260704T052343Z-A
---
# B1: wt-close --force 警告区分

## Problem
pre-commit.sh 和 git-worktree-guard 中 --force 警告不区分收口与废弃。

## Decision
两处修改：明确 --force = 永久丢弃，区分正常 wt-close 收口。
## Candidate
- candidate_id: C-20260704T052343Z-A
- status: promoted
- milestone: M-20260704T052343Z-A
