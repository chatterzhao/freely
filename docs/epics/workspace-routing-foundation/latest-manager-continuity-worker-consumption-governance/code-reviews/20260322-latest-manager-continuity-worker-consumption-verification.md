# Code Review: latest-manager-continuity-worker-consumption-governance

## Result

- pre-merge verification passed
- 2026-03-23 worker continuation reran the same verification suite and kept the issue in `in_verification`; only protected-environment post-merge acceptance remains.
- 2026-03-23 first-hop closure rechecked `lead-agent -> constitution-guard -> laws-enforcer -> context-source-skill`, confirmed this intake is still a `continuation` routed to `dev-loop-execution`, and found no new implementation gap beyond the existing post-merge acceptance requirement.
- 2026-03-23 second-hop dev-loop continuation revalidated the runtime/test truth source for delegated continuation active-prompt visibility and reran the full targeted suite; all checks remained green, so this lane still needs only post-merge `develop` acceptance.
- 2026-03-23 direct runtime inspection confirmed why the visibility regression is closed: `freely` persists consumed delegated ids immediately after prompt build, filters those ids out of active pending snapshots while the same prompt is running, and exposes them again after AI exit.
- 2026-03-24 the latest fresh session still stayed on `continuation -> dev_loop -> codex`, reran the targeted verification suite, and a read-only sidecar runtime/test audit again found no remaining implementation gap inside the declared worker write scope. The worktree remains doc-only dirty, and the only remaining gap is one real post-merge `develop` acceptance.
- 2026-03-24 active-worker launch-state followthrough reproduced the reported drift only as an earlier manager continuity snapshot on `develop`, not as a new repo regression. The current truth surface has already advanced again: `live-status` and `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env` now align on continuity `20260324-033747`, keep the same worker prompt `20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt`, and show that prompt as generated+queued with `active_running_worker_count=2` while the same-family worker is still running. The only extra running lane left in `fleet-status` is the stale-batch dirty worker, which remains runtime-owned outside this issue family.
- 2026-03-24 a later canonical recheck on `develop` tightened that same finding: by `2026-03-24T12:15:17Z`, `live-status` and `manager-worker-launch-state.env` had advanced again to continuity `20260324-034106`, both generated and consumed truth pointed to the same `20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt` prompt, `queued_worker_prompts` was `none`, and `active_running_worker_count=1`. That confirms the earlier mismatch was temporal protected-surface churn, not an unhandled repo-side branch in the runtime implementation.
- Canonical review disposition: this tree is `merge-ready` for verification-only closeout, but not `delete-ready` until one real post-merge `develop` acceptance is recorded via `freely chat` in the application-native real environment.

## Evidence

- 2026-03-24 reran `test-freely-manager-worker-launch-linkage`, `test-freely-worker-active-reentry-from-manager-launch`, `test-freely-latest-manager-continuity-worker-consumption`, `test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`, `test-freely-delegated-continuation-active-prompt-visibility`, and `./bin/governance-check`
- 2026-03-24 sidecar runtime/test audit rechecked `docs/system/workspace/scripts/runtime/freely` and `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`, confirmed the acceptance remains implemented, and found no remaining implementation gap inside the declared runtime/test scope
- 2026-03-24 reran `bash docs/system/workspace/scripts/tests/test-freely-live-status`, `./bin/governance-check`, and a direct truth-surface comparison across `bash /Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`, `bash /Users/zhaoyu/Downloads/code/my-freely/freely/bin/freely fleet-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`, and `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env`; the later `20260324-033747` surface remained internally aligned and showed the same-family prompt still queued while its worker was in flight
- 2026-03-24 final worker-side recheck confirmed the newest canonical `develop` surface at `2026-03-24T12:15:17Z`: `live-status` and `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-worker-launch-state.env` aligned on continuity `20260324-034106`, both generated and consumed truth pointed to the same `20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt` prompt, and `fleet-status` showed only one same-family active worker lane while the stale-batch followthrough remained separately owned
- 2026-03-24 `git diff --name-only` still only listed the same four issue-owned continuity docs, so the dirty state remained doc-only during this rerun
- absorbed delegated continuation intake ids `20260323-224831`, `20260323-224818`, and `20260323-224244` into the current `I-20260322-0445` worker continuation before re-running verification
- `lead-agent -> constitution-guard -> laws-enforcer -> context-source-skill` first-hop closure in the current worker session
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `./bin/governance-check`
- runtime truth-source checkpoints in `docs/system/workspace/scripts/runtime/freely`:
  - `LAST_DELEGATED_CONTINUATION_CONSUMED_IDS` / `..._AT` persistence
  - `active_prompt_consumed_delegation_ids_for_project`
  - `delegated_continuation_snapshot_for_project`
  - `delegated_continuation_ids_for_project`

## What Changed

1. `ensure_manager_once` now invokes worker latest-continuity consumption even when the manager supervisor is already running.
2. `manager-worker-launch-state.env` now records:
   - latest continuity generated
   - latest continuity consumed
   - latest worker prompts generated
   - latest worker prompts consumed
3. baseline/live status now expose the generated/consumed launch-state truth.
4. stale continuity snapshots are reset when a newer continuity file becomes canonical.
5. delegated continuation ids are now treated as consumed as soon as they are absorbed into the active prompt, so live status hides them from pending until the active AI exits.
6. the active-prompt visibility contract remained stable under repeated worker continuation reruns; no new implementation delta was needed in this lane.

## Remaining Acceptance

- run one real post-merge acceptance on `develop` via `freely chat`, confirming workers consume the newest manager continuity round in a live dogfooding loop.
- keep this feature worktree scoped to verification writeback only until that `develop` acceptance is recorded.
- treat the branch as merge-ready, but not delete-ready, until that native post-merge acceptance is written back.
