---
b1_id: B1-20260720T055358Z
phase_state: completed
source_raw: raw-20260720T055358Z
source_url: https://github.com/chatterzhao/freely/issues/4056
produced_candidate: C-20260720T055358Z-A
created_at: 2026-07-20
---

# B1_IBM: Prevent wt-create silent exit when issue.md lacks phase_state

## Input
- Source: patrol discovery — chain_trace merged_develop items with no phase_state
- Raw issue: raw-20260720T055358Z

## Problem
Line 311 of `docs/system/workspace/scripts/worktree/wt-create`:
```
_phase=$(grep 'phase_state:' "$_issue_file" 2>/dev/null | head -1 | sed 's/.*: *//' | tr -d "'\"")
```
When issue.md has no `phase_state:` field, `grep` returns exit code 1. With `set -euo pipefail`, this propagates through the pipeline and causes the entire script to exit silently — no error message, no worktree created.

## Brainstorm
### Option A: Add `|| true` after grep pipeline
Absorb grep's exit code 1 so `_phase` becomes empty string, case statement falls through safely.

### Option B: Check file existence separately before grep
Add an explicit check for phase_state before using it. More robust but adds more code.

## Decision: Option A
- Minimal change (one character in effect — `|| true`)
- No behavioral change when phase_state IS present
- Safe for all callers
- Fix was already applied by patrol on 2026-07-20

## Candidate
- candidate_id: C-20260720T055358Z-A
- status: promoted
- milestone: M-20260720T055358Z-A
