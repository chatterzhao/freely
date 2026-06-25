---
b1_id: B1-20260625T235348Z
phase_state: completed
source_raw: raw-20260625T235348Z
produced_candidate: C-20260625T235348Z-A
created_at: 2026-06-25
---

# B1_IBM: wt-close consistency check

## Problem
- CWD in worktree → git branch -d fatal
- No dev↔test sync check → test results lost
- Remote ops before local → irreversible on failure

## Decision
- cd PROJECT_ROOT first
- Check both worktrees clean, check sync both ways
- Local before remote: delete worktree → delete branch → delete remote → close issue
- Add feature/* case

## Candidate
- candidate_id: C-20260625T235348Z-A
- status: promoted
- milestone: M-20260625T235348Z-A
