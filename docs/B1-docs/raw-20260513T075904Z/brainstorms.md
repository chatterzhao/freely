# Brainstorm: pr-merge-guarded post-merge sync phase_state fix

## Issue

`pr-merge-guarded:235` reads `fm.get('status')` but I-* issues use `phase_state`.
`linked/completed` case never matches. GitHub issues never auto-closed post-merge.

## Fix

Read `fm.get('phase_state', fm.get('status', ''))`.
