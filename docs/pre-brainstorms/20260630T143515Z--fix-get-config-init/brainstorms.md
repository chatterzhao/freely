---
b1_id: B1-20260630T143515Z
phase_state: completed
source_raw: raw-20260630T143515Z
produced_candidate: C-20260630T143515Z-A
---
# B1: get_config→python3 reader + PROJECT_ROOT→project
## Problem: get_config nonexistent, grep+sed broken on macOS
## Decision: python3 reader for config.toml values, $project instead of $PROJECT_ROOT
