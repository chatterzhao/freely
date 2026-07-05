# Pre-tests: checkpoint-commit-and-multi-worktree-supervision-governance

1. clean repo 上 `./bin/checkpoint-guard` 返回 `checkpoint_required: no`
2. control-plane 与 product-plane 混合改动时 `./bin/checkpoint-guard` 返回 required
3. `./bin/checkpoint-guard --staged-only --fail-on-required` 对混 scope staged commit 返回非零
4. `./bin/wt-fleet-status` 能列出多个 worktree，并显示 runtime/dirty/checkpoint 列
5. `freely baseline-status --project <worktree>` 显示 `checkpoint_required` / `checkpoint_reasons`
