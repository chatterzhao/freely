---
issue_id: I-20260710T142858Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260710T142858Z-A
## IDN
- decision: Add A2A task query path before continuity fallback in worker launch
- why_this: A2A Phase 3 (Runtime) never connected; tasks stuck at submitted
- alternatives_considered: Replace continuity entirely — risk of breaking handoff/context rotation
- boundary_non_goals: Don't remove continuity system; don't modify A2A Server
- residual_risk: Low — new path only activates when submitted tasks exist; falls through to continuity otherwise
