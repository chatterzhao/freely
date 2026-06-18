# Brainstorm: merge semantic conflict detection

## Discovery
ef251886 receipt fix was silently overwritten by 15fa666c merge. Git auto-merged without conflict.

## Decision
Add post-merge receipt verification in pr-merge-guarded. Improve hook error message with actionable guidance.
