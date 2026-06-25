---
issue_id: I-20260625T030147Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260625T030147Z-A
## Implementation Decision Note
- decision: freely start/daemon start auto-detect platforms from git remotes
- why_this: single source of truth; commands read FREELY_REPO_PLATFORMS not re-detect
- alternatives_considered: per-command detection (rejected - redundant)
- boundary_non_goals: pr-create _platform_configs to be cleaned up separately
- residual_risk: none
