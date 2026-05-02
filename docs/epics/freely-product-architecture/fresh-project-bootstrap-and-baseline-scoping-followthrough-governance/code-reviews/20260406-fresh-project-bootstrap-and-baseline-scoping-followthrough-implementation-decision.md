# Code Review: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

- issue_id: `I-20260405-2358-A`
- title: `Fresh-project bootstrap and baseline scoping followthrough governance`
- branch: `feature/fresh-project-bootstrap-baseline-scoping-followthrough-20260406-1905`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1905-feature-fresh-project-bootstrap-baseline-scoping-followthrough`

- decision: `Keep the repair at the sync-tooling handoff: rewrite target-local config paths after copying managed config, rematerialize .githooks from the authoritative source project, and prove the whole boundary with one real fresh-project regression.`
- why_this: `Both live defects happen at the same first-hop boundary. Fixing only baseline-status would leave init blocked on missing hooks; fixing only hooks would still let status drift back to the source repo.`
- alternatives_considered: `Considered teaching baseline-status/status to ignore copied config drift, but that would hide wrong bootstrap truth instead of fixing it. Considered synthesizing new hook assets during init only, but that would still leave sync-tooling unable to hand off a target-local baseline surface.`
- boundary_non_goals: `This lane does not reopen runtime restart/chat semantics, ai switch/help ergonomics, or the higher-level authorization/bootstrap architecture owner.`
- residual_risk: `If future target projects intentionally place intent/constitution outside the canonical docs paths, the simple retargeting logic must still preserve explicit source-config absolute paths. This slice only guarantees the currently observed canonical fresh-project path.`
