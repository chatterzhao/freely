# Brainstorm: pr-create dirty check + pr-merge develop check
## Discovery
pr-create Step 0a uses git diff --quiet which misses untracked files. pr-merge has no develop check.
## Decision
Two small fixes: git status --porcelain for pr-create, develop check for pr-merge.
