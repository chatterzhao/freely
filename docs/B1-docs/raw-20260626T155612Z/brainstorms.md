---
b1_id: B1-20260626T155612Z
phase_state: completed
source_raw: raw-20260626T155612Z
source_url: https://github.com/chatterzhao/freely/issues/3565
produced_candidate: C-20260626T155612Z-A
created_at: 2026-06-26
---

# B1_IBM: pr-merge-guarded issue-sync after merge dirties source worktree

## Input
- source_raw: raw-20260626T155612Z
- source_url: https://github.com/chatterzhao/freely/issues/3565
- discovered during: wt-close blocked after PR #3564 merge

## Problem
pr-merge-guarded runs issue-sync AFTER merging to develop, writing phase_state changes (platform_state: closed) to the fix|feature worktree. This leaves uncommitted modifications that block wt-close. The fix worktree is about to be deleted — writing to it after merge is wasted work.

Contrast with pr-review-guarded: review → commit → push → merge → clean worktree.

## Brainstorm
### Option A: issue-sync writes to develop instead of source worktree
Would keep source worktree clean, but develop is a protected branch — can't commit directly.

### Option B: wt-close --force ignores dirty state
Paper over the symptom, doesn't fix the root cause.

### Option C: Move issue-sync before merge, auto-commit + push
Mirrors pr-review-guarded pattern. Issue-sync writes to source worktree → commit → push → merge. Worktree stays clean.

## Decision: Option C
- why_this: Consistent with pr-review-guarded. Source worktree stays clean for wt-close. Works for fix/feature/feat/hotfix equally.
- alternatives_considered: A (violates protected branch), B (paper over symptom)
- residual_risk: Diff comparison changed from post-merge (HEAD vs HEAD^) to pre-merge (source vs target). Must verify this correctly identifies changed issues.

## Candidate
- candidate_id: C-20260626T155612Z-A
- status: promoted
- milestone: M-20260626T155612Z-A
