---
name: constitution-guard
description: Enforce constitutional hard constraints before and after autonomous execution. Use when AI plans or completes development, merge, release, or recovery actions and must guarantee branch/worktree, architecture, and governance boundaries remain compliant.
---

# skill:constitution-guard

## Workflow
1. Run constitutional preflight before execution.
2. Validate hard constraints using `references/constitutional-gates.md`.
3. Block any action that violates hard constraints.
4. Re-run gate after merge/promotion/release actions.
5. Record pass/fail with evidence.

## Done
- Hard constraints pass, or action is blocked with explicit reason.
