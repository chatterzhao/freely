# Brainstorm: wt-close Phase 3 'local' regression

## Discovery
Commit a80b3072 introduced `local _current_phase` at script top level. Bash rejects this. wt-close --force crashes.

## Decision
Remove `local` keyword. One-word fix, zero risk.
