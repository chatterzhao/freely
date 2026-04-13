# Implementation Decision: runtime-forensic-time-alignment-and-stall-recovery-observability-governance

- issue_id: `I-20260412-1845-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-forensic-time-alignment-and-stall-recovery-observability-governance/issues/runtime-forensic-time-alignment-and-stall-recovery-observability-governance.md`
- branch: `feature/fix-manager-continuity-gap-20260412`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260412-feature-fix-manager-continuity-gap`
- decision_date: `2026-04-12`
- author: `codex`

## Implementation Decision Note

- decision: `Treat the 2026-04-12 incident as a runtime forensic-alignment and stall-observability owner, and repair it by emitting explicit stall-recovery runtime events plus a bounded stop-time continuity fallback.`
- why_this: `The human-readable time-display boundary was already correct. The actual product failure was that one run looked like multiple runs until UTC/local evidence was aligned, and the canonical runtime event plane still hid the recovery that actually occurred.`
- alternatives_considered: `Reopen the runtime time-display owner; declare the incident resolved by manual analyst discipline only; widen this owner into generic restart orchestration; leave continuity fallback unowned and rely on future manual reconstruction from state files.`
- boundary_non_goals: `No filename timestamp changes, no stored RFC3339/epoch rewrites, no dual-surface UTC/local output redesign, and no generic restart-policy expansion.`
- residual_risk: `Cross-plane correlation still depends on operators aligning UTC event timestamps with local file mtimes manually; this owner only makes the bounded recovery event explicit and records the need for a later observability follow-on if broader correlation anchors become necessary.`
