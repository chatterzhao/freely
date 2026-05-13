# Code Review / Verification: raw key seconds cleanup

- issue: I-20260513T010343Z-A
- reviewer: AI
- reviewed_at: 2026-05-13

## Changes Verified

1. `freely` L9667, L12069, L13584, L13631: `[0-9]{6}` → `[0-9]{4,6}` — regex accepts both 4-digit (minute) and 6-digit (second) precision
2. `wt-create` L11, L37, L40, L188, L189, L191: help/error messages updated to `YYYYMMDDTHHMM[SS]Z`
3. 10+ doc files: format text updated to reflect seconds precision

## Implementation Decision

- decision: All YYYYMMDDTHHMMZ → YYYYMMDDTHHMM[SS]Z, regex `[0-9]{6}` → `[0-9]{4,6}`
- residual_risk: None — only regex compatibility + doc alignment
