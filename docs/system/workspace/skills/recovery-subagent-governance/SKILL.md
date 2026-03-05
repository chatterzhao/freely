---
name: recovery-subagent-governance
description: Enforce recovery coupling and subagent governance constraints. Use when AI delegates tasks, resumes interrupted work, or needs to preserve branch/worktree context and ownership boundaries.
---

# skill:recovery-subagent-governance

## Workflow
1. Record active branch/worktree/session context.
2. When delegating, define ownership boundaries and expected outputs.
3. Track subagent completion/failure and merge implications.
4. On resume, verify continuity artifacts before continuing execution.
5. Block continuation if context ownership is ambiguous.

## Done
- Recovery and delegation state is complete and auditable.
