# Implementation Decision: freely-db-cli + AGENTS.md + hook fix

## Decision
Three independent single-line/doc fixes, all low risk, no logic changes.

## Implementation

### 1. freely-db-cli (_task_update_params)
**Change**: Add missing `for k in (` prefix at line 282.
**Before**: Bare tuple `"worktree", "branch", ...` causing IndentationError
**After**: `for k in ("worktree", "branch", ...):`
**Risk**: Zero. This is restoring accidentally deleted syntax. All worktree copies of this file have the same bug.

### 2. AGENTS.md §核心开发流程
**Change**: Replace flat 11-stage list with branching entry + 9-stage flow.
**Before**: `feedback` buried as sub-option in stage 2
**After**: `feedback` / `scan` as OR-branch entry points, then wt-create → ... → wt-close
**Risk**: Zero. Documentation-only, aligns with existing skill definitions.

### 3. pre-commit.sh hook message
**Change**: Replace mechanical git commands with skill routing + anti-bypass warning.
**Before**: "Use wt-create feature/<name> --base develop"
**After**: "Invoke skill:freely-fix-execution or skill:freely-feat-execution. Do NOT work around this hook."
**Risk**: Zero. Only changes the text of an error message.

## Why This
All three bugs have the same root cause pattern: missing or insufficient guidance for AI agents.
- Bug 1: Missing syntax → AI can't self-diagnose (IndentationError has no useful context)
- Bug 2: Missing entry point → AI skips feedback step, starts from wrong place
- Bug 3: Missing skill routing → AI treats hook as obstacle, not as signpost

The fixes close these guidance gaps at three levels: code (syntax), documentation (workflow), and runtime (hook messages).

## Alternatives Considered
- **Rewrite _task_update_params**: Overkill for a 1-line fix
- **Add linting check for syntax errors in Python scripts**: Future enhancement, out of scope
- **Auto-invoke skill on hook block**: Technically infeasible from bash hook

## Boundary / Non-Goals
- Not adding automated syntax checking (separate concern)
- Not restructuring the full AGENTS.md (scope creep)
- Not changing hook behavior beyond message text

## Residual Risk
None. All changes are additive (restoring deleted code) or documentation-only.
