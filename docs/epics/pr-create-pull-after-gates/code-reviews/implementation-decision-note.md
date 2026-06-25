---
issue_id: I-20260625T050000Z-A
---

# Implementation Decision Note

- decision: Move git pull origin develop from Step 1 to Step 3 in pr-create-guarded
- why_this: Gates are all local-only checks; only push needs up-to-date remote state. Moving pull to just before push eliminates redundant network round-trips on every gate failure retry without changing semantics.
- alternatives_considered:
  1. Keep pull at Step 1 (status quo) — wastes network on retries
  2. Remove pull entirely and require manual pull — breaks automation
  3. Add a gate-skip flag for the pull — over-engineered for this change
- boundary_non_goals: This change does not add new gates, alter existing gate behavior, change the push command, or modify any other script.
- residual_risk: If someone uses FREELY_SKIP_IBM_GATE=1 and remote has diverged, the pull at Step 3 could introduce merge conflicts. Same risk as pull-at-Step-1, just manifested later.
