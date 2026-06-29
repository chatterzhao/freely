# Progress: runtime-closeout-selfhost-validation-followthrough-governance

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- title: `Runtime closeout selfhost validation followthrough governance`
- phase_state: `completed`
- runtime_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/worker-recovery-sync-tooling-before-launch-20260424`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-worker-recovery-sync-tooling-before-launch`
- updated_at: `2026-04-24`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- This owner materializes the real follow-on behavior preserved on the runtime closeout/self-host checkpoint branch instead of letting it drift as undocumented branch-local truth.
- The bounded seam is one shared closeout/self-host validation surface: lawful daemon reuse, safe ambiguous start-lock cleanup, and interruption-manager fast paths for the prompts that repeatedly arise during worktree retirement and continuation routing.
- Focused feature-local regressions are green in the current worktree, including the missing `.freely/run` start-lock parent fix and a worker startup-truth attach regression that preserves healthy in-flight runtimes before `ai.pid` lands.
- Real self-host replay in this worktree no longer relaunches a second supervisor on repeated `freely daemon start`; after the first successful start (`supervisor_pid=93757`), a second start is rejected as `already running` instead of spawning another control-plane.
- A second guarded replay with a longer delay kept the same result after the runtime progressed past bootstrap: first start returned `supervisor_pid=98716`, `ai_launch_begin` landed in runtime events, `live-status` reached `last_ai_state=up`, and a second `daemon start` 12 seconds later still stopped at `user_start_rejected_already_running`.
- `./bin/pretests-gate` now accepts the owner contract in this worktree, so the issue-bound pre-tests truth is no longer blocked on stale `pending` metadata.
- Canonical `develop` self-host replay on `2026-04-24` exposed a new repair seam inside the same closeout/self-host owner: when runtime resumed a retained cleanup worker for `worker_exit_contract_invalid`, the broad lead-agent preamble stayed ahead of the repair contract, so the worker kept writing a minimal `worker_done` receipt instead of the bounded blocker contract needed for lawful cleanup followthrough.
- The runtime prompt builder now prepends an explicit repair-first override for both worker and manager exit-contract repair handoffs, keeping the existing runtime-owned launch boundary intact while forcing the resumed lane to repair the missing contract before any broad patrol or delegation logic.
- Focused regressions now prove the repair-first override renders before the lead-agent body, that worker prompts still include the exit-contract directive, and that invalid worker exit contracts still force precise resume repair.
- Canonical replay evidence after that first repair narrowed the remaining root cause further: runtime was already relaunching the retained cleanup worker correctly, but the generated `session-handoff.txt` only required “produce a valid worker exit contract,” so the resumed lane could legally short-circuit into a repair-only `worker_done` backed only by runtime repair artifacts.
- Runtime now rebinds worker exit-contract repair handoffs to the authoritative cleanup prompt metadata when that worker carries verification/closeout state, and cleanup repair rounds now reject a repair-only `worker_done` that cites only the handoff plus the rewritten exit contract instead of bounded cleanup evidence.
- New regressions prove the repair handoff preserves the original cleanup closeout contract and that a retained cleanup lane in `worker_exit_contract_repair` cannot stop itself with a no-op repair receipt while ordinary `worker_done` still stops a normal worker lane.
- Post-merge canonical replay exposed one more runtime-owned seam on the same owner: manager recovery was correctly deciding to restart the retained cleanup worker, but it launched that worktree through the worktree's own stale `bin/freely`, so the recovered lane still ran old runtime code and never consumed the new cleanup reentry hardening from `develop`.
- `start_workcell_supervisor_async()` now syncs tooling from the canonical source project into the target worktree before launching its supervisor, and both worker-prompt launches plus expected-running recovery paths now pass the manager project as that canonical source.
- A focused regression proves the launch order is now `sync-tooling` first, then worker supervisor start, so retained worker recovery can actually pick up newly merged runtime fixes without manual intervention.
- Canonical replay after those repairs moved the same owner one step further: manager now fresh-patrolled back onto the retained cleanup lane and launched a new worker, but valid `resume_manager` still rewrote its next handoff as `manager_exit_contract_repair`, and the retained worker still kept an older `worker_exit_contract_repair` handoff in `.freely/run/session-handoff.txt`.
- Runtime now distinguishes those two boundaries correctly: valid `resume_manager` writes a continuation handoff, and authoritative manager worker launch clears stale worker repair handoffs before the next worker round so the relaunched cleanup lane follows the fresh cleanup prompt instead of the old repair-only contract.
- Focused feature-local and protected-lane regressions both pass for the new seam, keeping the existing repair-first worker prompt behavior, invalid-contract resume repair, and cleanup followthrough resume behavior intact while removing the stale repair poisoning.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-ambiguous-missing-state`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-lock-acquires-with-missing-run-dir`
3. `bash docs/system/workspace/scripts/tests/test-freely-start-attaches-worker-runtime-when-startup-truth-is-ready`
4. `bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
5. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
6. `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler-cc`
7. Real replay on `2026-04-19`: first `freely daemon start --project <worktree>` returned `supervisor_pid: 93757`; second `daemon start` was rejected with `daemon start refused: project runtime is already running`
8. Guarded long-delay replay on `2026-04-19`: first `daemon start` returned `supervisor_pid: 98716`; runtime events recorded `ai_launch_begin`; second `daemon start` 12 seconds later returned exit code `2` with `daemon start refused: project runtime is already running`
9. `./bin/pretests-gate --project <worktree> --issue docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
10. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260419-runtime-closeout-selfhost-validation-followthrough-verification.md`
11. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
12. `bash docs/system/workspace/scripts/tests/test-freely-worker-prompt-includes-exit-contract-directive`
13. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
14. `./bin/governance-check`
15. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-exit-contract-repair-focus-verification.md`
16. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-handoff-rebinds-cleanup-closeout`
17. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-only-done-forces-resume`
18. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
19. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-cleanup-reentry-verification.md`
20. `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-syncs-tooling-before-launch`
21. `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
22. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-worker-recovery-sync-verification.md`
23. `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-resume-writes-continuation-handoff`
24. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-clears-stale-worker-repair-handoff`
25. Protected replay on `test-pre-merge-20260424-retained-cleanup-owner-rebind-followthrough`: reran `test-freely-manager-exit-contract-resume-writes-continuation-handoff`, `test-freely-manager-worker-launch-clears-stale-worker-repair-handoff`, `test-freely-worker-repair-prompt-prioritizes-exit-contract`, `test-freely-manager-exit-contract-resume-triggers-cleanup-followthrough`, and `test-freely-worker-exit-contract-invalid-forces-resume`
26. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-manager-resume-and-stale-worker-handoff-verification.md`
27. `docs/epics/workspace-routing-foundation/runtime-closeout-selfhost-validation-followthrough-governance/code-reviews/20260424-runtime-closeout-selfhost-validation-manager-resume-and-stale-worker-handoff-premerge-verification.md`

## Current Batch Risks

1. Runtime must keep syncing worker tooling from the canonical source project only as a launch preflight; it must not silently mutate unrelated worktree content outside the existing sync-tooling contract.
2. Canonical success still depends on protected-lane absorption plus a real daemon replay that proves the retained cleanup worker now runs the merged runtime code and emits a bounded blocker or retirement contract instead of a no-op `worker_done`.
3. The retained cleanup worktree remains mixed-scope dirty and must still be handled by cleanup governance rather than silently absorbed by this runtime launch fix.
4. The canonical daemon still needs one more replay after `develop` absorbs this batch to prove the retained cleanup worker settles lawfully and that manager then advances back to scan-selected next-task routing instead of staying pinned on the same cleanup lane.

## Next Action

1. Promote this runtime-launch fix through a fresh `test-pre-merge-*` replay into `develop`.
2. Restart canonical `freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely` and verify retained cleanup replay now stays on continuation truth, clears stale repair handoff on the relaunched worker, and produces bounded cleanup truth instead of repair-only receipts.
3. Only after that retained cleanup lane settles lawfully should manager move on to the next scan-selected task; until then, keep all other dirty retained-lane residue frozen.

## Closeout

- completed_at: `2026-04-28`
- merge_evidence: `merged via 903537ad`
