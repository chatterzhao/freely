---
b1_id: B1-20260703T234313Z
phase_state: completed
source_raw: raw-20260703T234313Z
produced_candidate: C-20260703T234313Z-A
---

# B1: IBM gate legacy loophole

## Problem
governance-merge-gate:1633 treats phase_state=completed + capability changes
as WARNING. This allows bypassing proper IBM workflow.

## Fix
1. Change WARNING to ERROR → block merge
2. Update workflow skill: mandatory full workflow for ALL changes
3. Update error message to explain correct phase_state progression

## Candidate
- candidate_id: C-20260703T234313Z-A
- status: promoted
- milestone: M-20260703T234313Z-A
