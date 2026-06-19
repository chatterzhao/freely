---
b1_id: B1-20260619T045410Z
phase_state: completed
source_raw: raw-20260619T045410Z
source_url: https://github.com/chatterzhao/freely/issues/3030
produced_candidate: C-20260619T045410Z-A
created_at: 2026-06-19
---
# B1_IBM: pr-merge-guarded PR close timing fix
## Problem: gh pr close before merge causes lost PR on hook failure
## Decision: move close to after MERGE_HEAD cleared
## Candidate: C-20260619T045410Z-A status=promoted
