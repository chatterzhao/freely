# Verification Blocker: runtime-lifecycle-receipt guarded replay stale batch cannot consume dirty source truth

- issue_id: `I-20260418-1900-A`
- issue_path: `docs/B2-docs/runtime/runtime-lifecycle-receipt-followthrough-governance/issues/runtime-lifecycle-receipt-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- route_judgment: `blocked`
- target_batch_branch: `test-pre-merge-runtime-lifecycle-followthrough-20260424`
- source_owner_branch: `feature/runtime-lifecycle-receipt-closeout-reconcile-20260424`
- source_owner_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-lifecycle-receipt-closeout-reconcile`

## Scope Verdict

- `BLOCKED`: `freely pr-merge-guarded test-pre-merge-runtime-lifecycle-followthrough-20260424 feature/runtime-lifecycle-receipt-closeout-reconcile-20260424` returned `Already up to date.` followed by `[MERGE-GUARD] blocked: no merge in progress.`
- `BLOCKED`: the stale batch already carried the committed source owner ancestor, while the newer bounded owner truth still existed only as dirty, uncommitted source-worktree changes.
- `PASS`: the failure proved the remaining blocker was lifecycle sequencing, not missing issue/progress/review fields in the bounded owner scope.
- `REQUIRED`: retire `test-pre-merge-runtime-lifecycle-followthrough-20260424`, checkpoint the owner truth on `feature/runtime-lifecycle-receipt-closeout-reconcile-20260424`, and replay that checkpoint through a fresh disposable `test-pre-merge-*` batch created from current `develop`.

## Commands

1. `freely pr-merge-guarded test-pre-merge-runtime-lifecycle-followthrough-20260424 feature/runtime-lifecycle-receipt-closeout-reconcile-20260424`
2. `git status --short`
3. `git rev-list --left-right --count test-pre-merge-runtime-lifecycle-followthrough-20260424...feature/runtime-lifecycle-receipt-closeout-reconcile-20260424`
4. `git diff --name-only develop...test-pre-merge-runtime-lifecycle-followthrough-20260424`

## Command Results

1. `freely pr-merge-guarded ...`
   - Exit `1`
   - Output: `[MERGE-GUARD] allowed: feature/runtime-lifecycle-receipt-closeout-reconcile-20260424 -> test-pre-merge-runtime-lifecycle-followthrough-20260424`, then `Already up to date.` and `[MERGE-GUARD] blocked: no merge in progress.`
2. `git status --short`
   - Exit `0`
   - The source owner lane still held dirty owner-truth files when this replay attempt happened.
3. `git rev-list --left-right --count ...`
   - Exit `0`
   - Output: `6 0`, confirming the source branch ref was already an ancestor of the stale batch.
4. `git diff --name-only develop...test-pre-merge-runtime-lifecycle-followthrough-20260424`
   - Exit `0`
   - Output included unrelated runtime-target-worker-role files, proving the stale batch was no longer a bounded replay surface for this owner.

## Manager Follow-Up

1. Preserve this blocker as successor-owner evidence.
2. Checkpoint the bounded owner truth on `feature/runtime-lifecycle-receipt-closeout-reconcile-20260424`.
3. Retire `test-pre-merge-runtime-lifecycle-followthrough-20260424`; do not reuse it.
4. Create a fresh disposable `test-pre-merge-*` batch from current `develop`.
5. Replay `feature/runtime-lifecycle-receipt-closeout-reconcile-20260424` into that fresh batch with `freely pr-merge-guarded`.
