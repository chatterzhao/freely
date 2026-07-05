---
b1_id: B1-20260630T062010Z
phase_state: completed
source_raw: raw-20260630T062010Z10Z
produced_candidate: C-20260630T062010Z-A
---
# B1_IBM: wt-close remove Phase 3.6 + --force semantics

## Problem
1. Phase 3.6 copies raw issue to develop — not wt-close's job, and develop is protected
2. --force help didn't say: local+remote+platform all deleted
3. --force semantics unclear: users use it when they think work is merged

## Decision
1. Remove Phase 3.6 entirely
2. --force help: 永久丢弃, 本地+远程+平台同时删除
3. Block message: if you think merged → try without --force first
## Candidate: C-20260630T062010Z-A promoted
