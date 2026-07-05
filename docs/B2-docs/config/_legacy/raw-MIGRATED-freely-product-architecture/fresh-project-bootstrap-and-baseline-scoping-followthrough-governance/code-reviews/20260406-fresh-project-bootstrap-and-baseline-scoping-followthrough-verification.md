# Verification: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

- issue_id: `I-20260405-2358-A`
- title: `Fresh-project bootstrap and baseline scoping followthrough governance`
- branch: `feature/fresh-project-bootstrap-baseline-scoping-followthrough-20260406-1905`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260406-1905-feature-fresh-project-bootstrap-baseline-scoping-followthrough`

## Findings

- `PASS`: `sync-tooling` now rewrites copied config truth to the target project, rematerializes `.githooks`, and keeps baseline/status baseline pinned to the requested target through a real fresh-project replay.
- `PASS`: existing worktree-oriented sync behavior still passes after the narrower retargeting change.
- `PASS`: adjacent baseline/status regressions still pass, so the repair did not break the canonical status surface.

## Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-fresh-project-bootstrap`
2. `bash docs/system/workspace/scripts/tests/test-freely-sync-tooling-into-worktree`
3. `bash docs/system/workspace/scripts/tests/test-freely-baseline-status`
4. `bash docs/system/workspace/scripts/tests/test-freely-status-family`
5. `./bin/governance-check`
6. `git diff --check`
7. Real CLI replay on a fresh git project confirmed:
   - `baseline_project=<fresh-project>`
   - `status_baseline_project=<fresh-project>`
   - `has_githooks=yes`

## Residual Risk

- This slice assumes the canonical docs layout (`docs/PROJECT_INTENT.md`, `docs/CONSTITUTION.md`) for the target project. If future sync consumers deliberately point config at non-standard absolute doc paths, the retargeting helper must preserve those paths correctly.
