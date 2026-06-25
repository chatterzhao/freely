---
b1_id: B1-20260625T222357Z
phase_state: completed
source_raw: raw-20260625T222357Z
source_url: https://github.com/chatterzhao/freely/issues/3516
produced_candidate: C-20260625T222357Z-A
created_at: 2026-06-25
---

# B1_IBM: Review agent in test-pre-merge with three-layer review

## Input
- source: raw-20260625T222357Z

## Problem
- Reviewer 在 fix 工位，只能看 pre-tests.md 字段，看不到 evidence 文件
- test-pre-merge 被丢弃后代码回不到 fix 工位
- 需要 dirty check + code sync check

## Decision
- Review agent 工作目录 = test-pre-merge
- 前置检查(bash): clean + sync + cherry-pick
- 三层: code quality / completeness / code safety
- pass/fail 两档

## Candidate
- candidate_id: C-20260625T222357Z-A
- status: promoted
- milestone: M-20260625T222357Z-A
