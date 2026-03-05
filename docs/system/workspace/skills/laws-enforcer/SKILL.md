---
name: laws-enforcer
description: Execute and verify law-level workflows and acceptance criteria. Use when AI needs to transform constitutional constraints into operational checks for doc-loop, dev-loop, auto-loop outputs and completion evidence.
---

# skill:laws-enforcer

## Workflow
1. Identify applicable law section for current task.
2. Select required execution skill routes.
3. For merge/promotion/release/cleanup gates, run `./bin/wt-status-all` and require all worktrees `CLEAN`.
4. Verify required artifacts and statuses.
5. Block completion if law acceptance evidence is missing.
6. Emit completion summary linked to artifacts.

## Done
- Law-defined artifacts and statuses are present and consistent.
