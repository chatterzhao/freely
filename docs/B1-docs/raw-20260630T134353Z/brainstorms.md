---
b1_id: B1-20260630T134353Z
phase_state: completed
source_raw: raw-20260630T134353Z
produced_candidate: C-20260630T134353Z-A
---
# B1: freely init --auto + config.toml cache
## Problem
Init re-searches system every time. No --auto for AI/CI.
## Decision
Add --auto flag + config.toml cache check.
