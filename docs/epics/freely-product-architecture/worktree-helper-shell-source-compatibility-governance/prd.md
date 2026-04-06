# PRD: worktree-helper-shell-source-compatibility-governance

## Problem

Freely is CLI-first, but a documented helper path is currently broken in the default shell context. Operators following the documented commands hit wrapper-level failure before the helper logic or protection semantics even run.

## Product Requirement

1. Documented sourced helper commands must remain callable from the default shell context used in dogfood.
2. Wrapper behavior must stay truthful to the existing helper semantics.
3. Regression coverage must bind to the real user-facing command path.

## Required Outcomes

1. `wt-add` wrapper resolves and sources its real script path without assuming `bash`.
2. `wt-enter` wrapper does the same.
3. Focused tests prove both the wrapper path and the underlying helper semantics.

## Non-Goals

1. No shell abstraction framework.
2. No broader worktree UX redesign.
3. No change to protected branch policies or helper semantics beyond preserving current truth through the wrapper path.
