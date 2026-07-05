---
b1_id: B1-20260625T211802Z
phase_state: completed
source_raw: raw-20260625T211802Z
produced_candidate: C-20260625T211802Z-A
created_at: 2026-06-26
---

# B1_IBM: agent-table slot 全链路

## Problem
- agent-table.toml 已定义池但未完整消费
- Manager/Worker/Reviewer 都用同一 AI_TOOL，无法独立

## Decision
1. agent-table-query --next-free: 扫工位 .freely/worker-id.env 找出 busy，返回空闲
2. sync_tooling: 写 worker-id.env + slot
3. pr-review-guarded: 读 worker-id.env → reviewer_slot
4. Manager: agent-table-query --get manager_01 → manager_slot
5. manager_max_parallel_workers: 读 pool count

## Candidate
- candidate_id: C-20260625T211802Z-A
- status: promoted
- milestone: M-20260625T211802Z-A
