---
b1_id: B1-20260619T045626Z
phase_state: completed
source_raw: raw-20260619T045626Z26Z
source_url: https://github.com/chatterzhao/freely/issues/3031
produced_candidate: C-20260619T045626Z-A
created_at: 2026-06-19
---

# B1_IBM: pr-merge-guarded 并发安全

## Problem
merge 中途失败留下 MERGE_HEAD，阻塞后续 merge。

## Decision: flock + trap cleanup
