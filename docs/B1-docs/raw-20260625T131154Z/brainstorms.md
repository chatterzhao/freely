---
b1_id: B1-20260625T131154Z
phase_state: completed
source_raw: raw-20260625T131154Z54Z
source_url: https://github.com/chatterzhao/freely/issues/3503
produced_candidate: C-20260625T131154Z-A
created_at: 2026-06-25
---

# B1_IBM: pr-create-guarded rebase 替代 merge

## Input
- source: raw-20260625T131154Z54Z (GitHub #3503)

## Problem
- pr-create Step 3 使用 `git merge develop`，多工位并行时 merge commit 跨 scope 被 checkpoint-guard 拦截

## Decision: rebase 替代 merge
- `git pull --rebase` + `--force-with-lease` push
- 每个 commit scope 保持原样，不触发预算超限

## Candidate
- candidate_id: C-20260625T131154Z-A
- status: promoted
- milestone: M-20260625T131154Z-A
