---
name: auto-loop-orchestrator
description: Orchestrate A:auto-loop(ADD) from issue discovery through routing to doc-loop or dev-loop and back to discovery. Use when AI runs autonomous continuous delivery cycles.
---

# skill:auto-loop-orchestrator

## Workflow
1. Discover candidates from configured sources.
2. Route candidate by readiness:
   - unresolved -> `skill:doc-loop-execution`
   - ready/in-progress -> `skill:dev-loop-execution`
3. Update candidate route/status records.
4. Repeat loop until stop condition.

## Done
- Discovery, routing, and closure states remain traceable.
