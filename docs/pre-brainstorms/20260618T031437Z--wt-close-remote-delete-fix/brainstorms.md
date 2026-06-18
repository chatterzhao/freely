# Brainstorm: wt-close remote branch deletion fix

## Discovery
9 remote branches on GitHub not deleted after local wt-close. Two bugs found.

## Decision
Fix SELF_ROOT→PROJECT_ROOT and replace silent failure with warnings.
