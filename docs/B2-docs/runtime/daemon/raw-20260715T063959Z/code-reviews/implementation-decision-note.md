- issue_id: I-20260715T063959Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260715T063959Z/issues/I-20260715T063959Z-A.md

## Implementation Decision Note

- decision: Revert 6 ${AI_MODE:-wait} → ${AI_MODE:-auto}. Keep 3 ${AI_MODE:-none} guards.

- why_this: AI_MODE controls Claude interaction posture (auto=autonomous, step=interactive). wait is not a valid Claude mode — start-lead-agent.sh rejects it. The original auto default was correct.

- alternatives_considered: None. This is a straight revert of a mistaken change in aimode-hotfix2.

- boundary_non_goals: NOT changing task_mode default (remains wait). NOT changing AI_MODE:-none guards (correct for log lines).

- residual_risk: None — reverting to the original correct value.
