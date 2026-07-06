# Implementation Decision Note: test-lane-routing-and-enforcement-governance

- issue_id: `I-20260405-1914-A`
- issue_path: `docs/B2-docs/gate/test-lane-routing-and-enforcement-governance/raw-20260405-1914issues/test-lane-routing-and-enforcement-governance.md`
- decision_date: `2026-04-05`
- author: `codex`

## Implementation Decision Note

- decision: `Make test-lane an explicit branch-to-lane contract instead of a permissive wrapper: feature-local is limited to dedicated feature/release/hotfix/premerge worktrees, premerge-integration is limited to test-pre-merge-* batches, and post-merge-followthrough is limited to protected targets.`
- why_this: `The observed pain was false confidence from commands that could run on the wrong branch but still “work”. That makes it too easy to test on develop, or on an ad hoc writable branch, and believe the right lane was covered.`
- alternatives_considered: `Considered keeping feature-local as “any non-protected branch”, and considered making the wrapper infer a lane automatically from the current branch. The first preserves misuse; the second hides policy decisions and makes failures harder to reason about in hooks and tests.`
- boundary_non_goals: `This owner does not implement lane inference, test catalog discovery, batch auto-creation, or lifecycle management for test-pre-merge batches.`
- residual_risk: `As long as some teams call raw test commands directly, they can still avoid the explicit lane contract; follow-on governance may need wrapper adoption checks or hook integration if that becomes a repeated escape path.`
