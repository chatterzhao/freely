---
timestamp: 2026-06-24T15:50:00Z
topic: pr-create-pretests-check
---

# Brainstorm: Add pretests evidence check to pr-create-guarded

## Starting Point

Issue #3442: pr-create-guarded currently only checks IBM governance docs but not pretests execution evidence. The pretests check only happens at wt-close, which is too late.

## Divergent Thinking

1. Add Step 2c to pr-create-guarded calling pretests-retirement-gate (same pattern as wt-close)
   - Pro: consistent, reuses existing gate
   - Con: introduces self-referential gate for PR itself

2. Add the check in a separate script that pr-create-guarded calls
   - Pro: modular
   - Con: unnecessary indirection for a single call

3. Add the check at Step 2b (merge with IBM governance gate)
   - Pro: single gate step
   - Con: conflates IBM governance with test evidence; harder to debug failures

## Converged Decision

Option 1: Add Step 2c as a separate call to pretests-retirement-gate, matching wt-close
pattern exactly. Clear separation of concerns between IBM governance (Step 2b) and
pretests evidence (Step 2c).
