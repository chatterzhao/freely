# Progress: runtime-closeout-selfhost-validation-followthrough-governance

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- title: `Runtime closeout selfhost validation followthrough governance`
- phase_state: `in_verification`
- runtime_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/worker-exit-contract-repair-focus-20260424`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-worker-exit-contract-repair-focus`
- updated_at: `2026-04-24`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner materializes the real follow-on behavior preserved on the runtime closeout/self-host checkpoint branch instead of letting it drift as undocumented branch-local truth.
- The bounded seam is one shared closeout/self-host validation surface: lawful daemon reuse, safe ambiguous start-lock cleanup, and interruption-manager fast paths for the prompts that repeatedly arise during worktree retirement and continuation routing.
- Focused feature-local regressions are green in the current worktree, including the missing `.freely/run` start-lock parent fix and a worker startup-truth attach regression that preserves healthy in-flight runtimes before `ai.pid` lands.
- Real self-host replay in this worktree no longer relaunches a second supervisor on repeated `./bin/freely daemon start`; after the first successful start (`supervisor_pid=93757`), a second start is rejected as `already running` instead of spawning another control-plane.
- A second guarded replay with a longer delay kept the same result after the runtime progressed past bootstrap: first start returned `supervisor_pid=98716`, `ai_launch_begin` landed in runtime events, `live-status` reached `last_ai_state=up`, and a second `daemon start` 12 seconds later still stopped at `user_start_rejected_already_running`.
- `./bin/pretests-gate` now accepts the owner contract in this worktree, so the issue-bound pre-tests truth is no longer blocked on stale `pending` metadata.
- Canonical `develop` self-host replay on `2026-04-24` exposed a new repair seam inside the same closeout/self-host owner: when runtime resumed a retained cleanup worker for `worker_exit_contract_invalid`, the broad lead-agent preamble stayed ahead of the repair contract, so the worker kept writing a minimal `worker_done` receipt instead of the bounded blocker contract needed for lawful cleanup followthrough.
- The runtime prompt builder now prepends an explicit repair-first override for both worker and manager exit-contract repair handoffs, keeping the existing runtime-owned launch boundary intact while forcing the resumed lane to repair the missing contract before any broad patrol or delegation logic.
- Focused regressions now prove the repair-first override renders before the lead-agent body, that worker prompts still include the exit-contract directive, and that invalid worker exit contracts still force precise resume repair.

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
11. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
12. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
13. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
14. `./bin/governance-check`
15. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-exit-contract-repair-focus-verification.md`

## Current Batch Risks

1. The repair-first override is intentionally narrow; it must not regress ordinary `resume` or `fresh_with_handoff` prompt construction outside exit-contract repair lanes.
2. Canonical success still depends on protected-lane absorption plus a real daemon replay that proves the retained cleanup worker now emits a bounded blocker or retirement contract instead of a no-op `worker_done`.
3. The retained cleanup worktree remains mixed-scope dirty and must still be handled by cleanup governance rather than silently absorbed by this repair-only lane.

## Next Action

1. Promote this repair through `test-pre-merge-20260424-worker-exit-contract-repair-focus` into `develop`.
2. Restart canonical `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` and verify retained cleanup replay now writes a bounded blocker/retirement contract instead of `worker_done`.
3. Keep all other dirty retained-lane residue frozen until runtime either retires that worktree cleanly or hands back a precise split/freeze decision.
