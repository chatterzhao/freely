# Implementation Decision: worktree-tool-boundary-bootstrap-governance

- issue_id: `I-20260403-2041-A`
- issue_path: `docs/epics/freely-product-architecture/worktree-tool-boundary-bootstrap-governance/issues/worktree-tool-boundary-bootstrap-governance.md`
- branch: `feature/tool-sandbox-worktree-bootstrap-20260403-204147`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260403-204147-feature-tool-sandbox-worktree-bootstrap`

## decision

Introduce `freely sync-tooling` as the canonical sibling-worktree rematerialization primitive, then make managed worktree entrypoints and tool launchers consume that primitive instead of assuming ignored tool-local files or raw project-root launch semantics will be enough.

## why_this

The actual failure was not “one tool needs another flag”. The failure was that Freely had a managed boundary contract in the project root but no canonical way to reproduce it inside sibling worktrees. Without one rematerialization primitive, every entrypoint and every tool surface would drift independently and protected-root editing would remain an easy fallback.

## alternatives_considered

1. Keep tool bootstrap only in the project root and rely on Git copying local config directories into new worktrees.
   - Rejected because ignored or untracked local tool surfaces are not guaranteed to copy, and the user can change `.gitignore`.
2. Invent project-local config formats for every tool.
   - Rejected because several tools do not have a verified project-local writable-root surface; wrapper plus launch-time extension is the honest contract today.
3. Forbid project-root use entirely and force all commands to start inside sibling worktrees.
   - Rejected because project root still has a real integration/merge/bootstrap role and the product already depends on that distinction.

## boundary_non_goals

- Do not reopen the completed autonomy/materialization umbrella.
- Do not redefine project root as an invalid merge surface.
- Do not redesign manager/runtime orchestration outside the boundary bootstrap contract.

## residual_risk

Some external tools may later expose stable project-local config surfaces. If that happens, the current wrapper-only or launch-flag strategy should be upgraded in a new narrow follow-on rather than retroactively pretending the surface existed now.
