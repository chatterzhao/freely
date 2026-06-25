---
b1_id: B1-20260625T152446Z
phase_state: completed
source_raw: raw-20260625T152446Z
source_url: https://github.com/chatterzhao/freely/issues/3507
produced_candidate: C-20260625T152446Z-A
created_at: 2026-06-25
---

# B1_IBM: pr-review-guarded ACP TDD Reviewer

## Input
- source: raw-20260625T152446Z

## Problem
- pr-review-guarded 是 bash 自审，同一 agent 没有独立性
- 需要独立 Reviewer agent 做 TDD 四问评审

## Decision: ACP session + TDD reviewer
- pr-review-guarded 调用 ACP 启动独立 Reviewer session
- Round 1: session/new, Round 2+: session/prompt
- >3 rounds escalate to Manager
- 保留 --verdict override 作为紧急旁路

## Candidate
- candidate_id: C-20260625T152446Z-A
- status: promoted
- milestone: M-20260625T152446Z-A
