---
b1_id: B1-20260625T044836Z
phase_state: completed
source_raw: raw-20260625T044836Z36Z
source_url: https://github.com/chatterzhao/freely/issues/3477
produced_candidate: C-20260625T044836Z-A
created_at: 2026-06-25
---

# B1_IBM: issue-sync filter — skip closed issues

## Input
- source: raw-20260625T044836Z36Z

## Problem
- batch 遍历全部 ~200 issues，大部分已同步
- 只需检查不一致的

## Decision: filter by platform_state
- platform_state=closed → skip
- 减少到 ~10-20 不一致的 issue
- scan 速度从分钟级降到秒级

## Candidate
- candidate_id: C-20260625T044836Z-A
- status: promoted
- milestone: M-20260625T044836Z-A
