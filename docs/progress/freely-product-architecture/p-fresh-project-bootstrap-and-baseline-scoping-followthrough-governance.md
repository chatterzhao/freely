# Progress: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

- issue_id: `I-20260406-1905-A`
- issue_path: `docs/epics/freely-product-architecture/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance/issues/fresh-project-bootstrap-and-baseline-scoping-followthrough-governance.md`
- title: `Fresh-project bootstrap and baseline scoping followthrough governance`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260326-freely-product-architecture`
- branch: `feature/fresh-project-bootstrap-baseline-scoping-followthrough-20260406-1905`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1905-feature-fresh-project-bootstrap-baseline-scoping-followthrough`
- updated_at: `2026-04-06`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical replay reproduced two live defects on the same boundary: `sync-tooling` copied source-root config truth into the target project, and it left fresh projects without `.githooks`.
- The current implementation lane is repairing that handoff point directly and adding one focused fresh-project regression that proves sync, baseline/status, and follow-on init all stay target-local.
- Adjacent runtime/control-plane and CLI help/dry-run owners remain explicitly out of scope.

## Current Evidence

- Reproduced on this lane before edits:
  - synced target config contained `PROJECT_ROOT=<source-project>`
  - fresh target had no `.githooks`
  - `freely baseline-status --project <fresh-target>` reported `project: <source-project>`

## Next Action

- Finish the focused repair, run the fresh-project regression plus adjacent baseline/status tests, then move the verified patch through `test-pre-merge-*` into `develop`.
