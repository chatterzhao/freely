# Verification: runtime-closeout-selfhost-validation-worker-recovery-sync

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`

## Scope Verdict

- `PASS`: canonical replay after `develop` absorbed the cleanup reentry fix still showed repeated repair-only `worker_done` receipts on the retained cleanup lane, but the retained worktree handoff format proved the worker was still running stale local runtime code rather than the newly merged canonical tooling.
- `PASS`: `start_workcell_supervisor_async()` now performs a `sync-tooling --source-project <canonical> --project <target>` preflight before launching the target worktree supervisor.
- `PASS`: both manager worker-prompt launch and expected-running worker recovery now pass the manager project as the canonical sync source, so retained worker restarts consume freshly merged runtime changes without manual sync.
- `PASS`: the focused launch-order regression and an existing manager recovery regression both pass, so the new preflight does not suppress ordinary recovery behavior.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-syncs-tooling-before-launch`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-only-done-forces-resume`

## Real Replay Evidence

- After `develop` reached merge commit `1541cd7c`, canonical daemon replay at `2026-04-24 02:48:22 PDT` still auto-recovered the retained cleanup worktree, but the retained handoff remained in the old three-bullet repair format and the retained worker continued writing `worker_exit_contract_done` with the repair-only summary.
- A direct comparison showed canonical runtime `docs/system/workspace/scripts/runtime/freely` and the retained worktree copy had diverged, confirming the recovery path was launching stale worktree tooling instead of the newly merged runtime.
- The remaining seam was therefore launch provenance, not task ownership: runtime still chose and started the worker, but it started the wrong copy of Freely.

## Implementation Decision Note

- decision: `Sync canonical tooling into retained worker worktrees immediately before supervisor launch.`
- why_this: `The bug was caused by stale local control-plane code inside old worktrees. Syncing through the existing tooling contract preserves runtime-owned launch responsibility while making retained worker recovery consume the current canonical runtime.`
- alternatives_considered: `Manually resync dirty worktrees after every merge; move worker launch to canonical root only; accept stale worktree runtime and keep layering prompt-only fixes on top.`
- boundary_non_goals: `This change does not classify retained cleanup residue, rewrite scan-json selection, or change manager-vs-runtime launch ownership.`
- residual_risk: `A fresh canonical replay is still required to prove the retained cleanup lane now runs the synced runtime and produces a bounded blocker or retirement outcome instead of the stale repair-only receipt.`
