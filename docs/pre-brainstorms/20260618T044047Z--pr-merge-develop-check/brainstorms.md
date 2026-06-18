# Brainstorm: pr-merge explicit cd + develop check
## Discovery
pr-merge uses $PWD without cd. Missing develop cleanliness check.
## Decision
Add cd to PROJECT_ROOT + git status --porcelain check.
