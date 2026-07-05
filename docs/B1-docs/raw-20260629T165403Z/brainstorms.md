---
b1_id: B1-20260629T165403Z
phase_state: completed
source_raw: raw-20260629T165403Z03Z
produced_candidate: C-20260629T165403Z-A
---

# B1_IBM: wt-close args unbound + test-pre-merge -D

## Problem
1. `set -- "${args[@]}"` 在 args 为空时触发 unbound variable
2. Phase 6b test-pre-merge 删除用 -d（正常路径），但分支有未合并 commit，-d 拒绝

## Decision
两个 one-liner fix，无替代方案。

## Candidate
- candidate_id: C-20260629T165403Z-A
- status: promoted
- milestone: M-20260629T165403Z-A
