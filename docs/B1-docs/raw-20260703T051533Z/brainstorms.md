---
b1_id: B1-20260703T051533Z
phase_state: completed
source_raw: raw-20260703T051533Z
produced_candidate: C-20260703T051533Z-A
---

# B1_IBM: __pycache__ .pyc files tracked by git block daemon

## Problem
.gitignore has `__pycache__/` but 6 .pyc files were force-added to git.
Python recompiles on import → dirty tree → daemon refuses to start.

## Decision
`git rm --cached` all tracked .pyc files. .gitignore already covers them.

## Candidate
- candidate_id: C-20260703T051533Z-A
- status: promoted
- milestone: M-20260703T051533Z-A
