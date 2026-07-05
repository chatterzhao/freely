# Implementation Decision: codex-current-live-apikey-bootstrap-without-saved-slot-governance

- issue_id: `I-20260406-1829-A`
- issue_path: `docs/B2-docs/config/codex-current-live-apikey-bootstrap-without-saved-slot-governance/issues/codex-current-live-apikey-bootstrap-without-saved-slot-governance.md`
- decided_in_branch: `feature/codex-current-live-apikey-bootstrap-dev-20260406-1904`
- decided_in_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1904-feature-codex-current-live-apikey-bootstrap-dev`
- decided_at: `2026-04-06`
- decision_maker: `codex`

- decision: `Treat a usable current live Codex API-key auth as a bounded bootstrap identity even when saved-slot inventory is empty, and keep that identity explicit as current-live instead of synthesizing a fake slot.`
- why_this: `The old residual tree proved bootstrap recovery and ai switch acceptance both need the same contract: usable live auth can be real even when there is no saved-slot inventory yet. Preserving slot=null/current-live avoids inventing state, keeps recovery truthful, and absorbs the remaining residual watchdog slice into a narrow owner.`
- alternatives_considered: `Rejected replaying the old residual ai-cli patch verbatim because the execution lane already had a stronger current-live switch path in base. Rejected manufacturing a synthetic saved slot because that would blur live-auth truth with inventory truth and create follow-on cleanup debt.`
- boundary_non_goals: `This owner does not reopen reconnect fast-fail, does not widen into interactive login UX, and does not generalize the no-saved-slot bootstrap contract to other providers.`
- residual_risk: `The current-live bootstrap path remains Codex-specific. If another provider later needs equivalent semantics, it should land in a separate owner after proving the same boundary is stable.`
