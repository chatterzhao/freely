---
b1_id: B1-20260710T043521Z
phase_state: completed
source_raw: raw-20260710T043521Z
---
# B1: scan skip closed items
## Problem: 641 items flagged as mismatch despite platform_state=closed
## Decision: Skip when platform_state starts with "closed" and no platform_ids
