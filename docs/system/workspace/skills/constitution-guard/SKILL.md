---
name: constitution-guard
description: Enforce constitutional hard constraints before and after autonomous execution. Use when AI plans or completes development, merge, release, or recovery actions and must guarantee branch/worktree, architecture, and governance boundaries remain compliant.
---

# skill:constitution-guard

## Workflow
1. Run constitutional preflight before execution.
2. Run `./bin/wt-status-all` to verify all mounted worktrees are clean before gate-sensitive actions.
3. Validate hard constraints using `references/constitutional-gates.md`.
4. Block any action that violates hard constraints.
5. Re-run gate after merge/promotion/release actions.
6. Record pass/fail with evidence.

## Done
- Hard constraints pass, or action is blocked with explicit reason.
