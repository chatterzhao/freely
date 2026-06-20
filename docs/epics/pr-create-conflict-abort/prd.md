# PRD: pr-create-guarded conflict handling

## Problem
When git pull triggers merge conflicts, the error message is generic.
Users don't know which files are conflicted, and don't know they can abort.

## Fix
1. Run `git diff --name-only --diff-filter=U` to list conflicted files
2. Provide both resolution paths: manual resolve (A) or abort (B)
