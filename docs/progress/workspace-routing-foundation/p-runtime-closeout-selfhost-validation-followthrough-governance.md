# Progress: runtime-closeout-selfhost-validation-followthrough-governance

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- title: `Runtime closeout selfhost validation followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/checkpoint-runtime-closeout-selfhost-validation-20260419`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260418-feature-runtime-closeout-selfhost-validation`
- updated_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner materializes the real follow-on behavior preserved on the runtime closeout/self-host checkpoint branch instead of letting it drift as undocumented branch-local truth.
- The bounded seam is one shared closeout/self-host validation surface: lawful daemon reuse, safe ambiguous start-lock cleanup, and interruption-manager fast paths for the prompts that repeatedly arise during worktree retirement and continuation routing.
- Focused feature-local regressions are green in the current worktree, including the missing `.freely/run` start-lock parent fix and a worker startup-truth attach regression that preserves healthy in-flight runtimes before `ai.pid` lands.
- Real self-host replay in this worktree no longer relaunches a second supervisor on repeated `./bin/freely daemon start`; after the first successful start (`supervisor_pid=93757`), a second start is rejected as `already running` instead of spawning another control-plane.
- A second guarded replay with a longer delay kept the same result after the runtime progressed past bootstrap: first start returned `supervisor_pid=98716`, `ai_launch_begin` landed in runtime events, `live-status` reached `last_ai_state=up`, and a second `daemon start` 12 seconds later still stopped at `user_start_rejected_already_running`.
- `./bin/pretests-gate` now accepts the owner contract in this worktree, so the issue-bound pre-tests truth is no longer blocked on stale `pending` metadata.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-ambiguous-missing-state`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-acquires-with-missing-run-dir`
3. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
5. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
6. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
7. Real replay on `2026-04-19`: first `./bin/freely daemon start --project <worktree>` returned `supervisor_pid: 93757`; second `daemon start` was rejected with `daemon start refused: project runtime is already running`
8. Guarded long-delay replay on `2026-04-19`: first `daemon start` returned `supervisor_pid: 98716`; runtime events recorded `ai_launch_begin`; second `daemon start` 12 seconds later returned exit code `2` with `daemon start refused: project runtime is already running`
9. `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
10. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260419-runtime-closeout-selfhost-validation-followthrough-verification.md`

## Current Batch Risks

1. The local self-host evidence now covers both early bootstrap and post-`ai_launch_begin` timing windows, but protected-lane promotion still depends on carrying this through the repo's normal merge/verification path.
2. The bounded interruption routing changes must stay coupled only to closeout/self-host prompts; future widening would need a separate owner.
3. The older integration and checkpoint worktrees should not be retired until this new owner is either merged or explicitly dropped.

## Next Action

1. Keep this owner in verification and prepare the normal promotion path with the new long-delay replay plus `pretests-gate` evidence attached.
2. Keep the other non-main worktrees in cleanup-candidate state rather than pushing new code there.
3. Leave `git diff --check` and `./bin/governance-check` recorded as green for this round.
