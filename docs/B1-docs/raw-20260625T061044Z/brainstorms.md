---
b1_id: B1-20260625T061044Z
phase_state: completed
source_raw: raw-20260625T061044Z44Z
source_url: https://github.com/chatterzhao/freely/issues/3484
produced_candidate: C-20260625T061044Z-A
created_at: 2026-06-25
---

# B1_IBM: issue-sync batch before daemon scan

## Input
- source: raw-20260625T061044Z44Z

## Problem
- scan 发现的同步任务大部分是机械操作，全部交给 AI 浪费 token

## Decision: daemon start 时先跑 issue-sync batch
- 在 scan 前处理所有确定性同步
- AI 只需处理真正需要判断的 case

## Candidate
- candidate_id: C-20260625T061044Z-A
- status: promoted
- milestone: M-20260625T061044Z-A
