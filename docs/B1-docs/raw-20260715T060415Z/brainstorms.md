---
b1_id: B1-20260715T060415Z
phase_state: completed
source_raw: raw-20260715T060415Z
created_at: 2026-07-15
---
# B1: scan prompt injection field name mismatch
## Problem
task-lifecycle-scan.py outputs `summary.total`, `summary.by_station`, `item.station`.
Injection Python reads `summary.total_incomplete`, `summary.by_stage`, `item.stage`.
## Decision
Align field names with backward compat fallback.
## Candidate
C-20260715T060415Z-A promoted M-20260715T060415Z-A
