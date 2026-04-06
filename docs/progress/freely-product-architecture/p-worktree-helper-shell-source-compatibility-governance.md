# Progress: worktree-helper-shell-source-compatibility-governance

- issue_id: `I-20260405-2302-A`
- issue_path: `docs/epics/freely-product-architecture/worktree-helper-shell-source-compatibility-governance/issues/worktree-helper-shell-source-compatibility-governance.md`
- title: `Worktree helper shell source compatibility governance`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/worktree-helper-shell-source-compatibility-20260405-2302`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260405-2302-feature-worktree-helper-shell-source-compatibility`
- updated_at: `2026-04-05`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Materialized a new narrow follow-on owner after reproducing that documented `wt-add` / `wt-enter` wrapper commands fail in default `zsh` before helper semantics run.
- The lane is scoped to wrapper source-safety and wrapper-path regressions only.

## Current Evidence

- `zsh -lc 'source ./bin/wt-add -- README.md'`
- `zsh -lc 'source ./bin/wt-enter develop'`
- `bash -lc 'source ./bin/wt-add -- README.md'`
- `bash -lc 'source ./bin/wt-enter develop'`

## Next Action

- Implement the narrow wrapper fix and bind the regression suite to the documented `bin/` helper path.
