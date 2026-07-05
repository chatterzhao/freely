# Candidates - 20260403-2041--worktree-tool-boundary-bootstrap

## C-20260403-2041-A

- title: Worktree tool boundary bootstrap governance
- problem: Freely's completed tool-materialization family still leaves a real sibling-worktree gap: managed tool boundaries materialize in the project root, but new worktrees do not automatically regain the same local tool surfaces and launch-time writable-root extensions, which leaves a path back to protected-root implementation drift.
- why_now:
  - the failure mode is already concrete in dogfood use: tool writes can be blocked in sibling worktrees while `develop` remains writable on disk
  - the remaining code and doc surface is narrow and directly testable
  - completed owners already froze the product/tool contract, so this must land as a follow-on rather than a silent umbrella reopen
- acceptance_criteria:
  - standard worktree entrypoints rematerialize managed local tool boundaries into new sibling worktrees
  - tool boundary truth explicitly keeps project root as the integration / merge surface and `{project}-worktrees` as the owner-development extension boundary
  - supported launchers inject the sibling worktrees root as an allowed boundary where the tool requires an explicit flag
  - docs / hooks / skills stop teaching raw `git worktree add` as the default managed path
- promotion_gate:
  - keep the owner attached to the existing tool-materialization family, not workspace-routing umbrella redesign
  - prove the change closes a real sibling-worktree boundary gap rather than only renaming docs
  - verify at least explicit `sync-tooling`, `wt-create`, and protected-branch `post-checkout` auto-worktree paths
- decision_reason:
  - this is the smallest lawful owner that can absorb the already-written runtime, hook, and test changes
  - leaving the change undocumented would keep a hidden path back to protected-root edits
  - reopening `I-20260401-1303-A-2` would blur a completed contract back into an umbrella
- priority: `P0`
- status: `promoted`
- milestone: `M-20260326-freely-product-architecture`
- promoted_issue_path: `docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md`
- promoted_issue_path_role: `primary-owner`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- next_action:
  - owner completed on canonical `develop`
  - reopen only if sibling-worktree boundary rematerialization or managed entrypoint guidance regresses
- revisit_trigger:
  - reopen only if canonical `develop` still shows an unowned tool-boundary drift after this worktree-bootstrap slice lands
