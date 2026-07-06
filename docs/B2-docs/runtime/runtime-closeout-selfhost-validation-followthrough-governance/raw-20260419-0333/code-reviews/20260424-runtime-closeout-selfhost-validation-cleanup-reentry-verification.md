# Verification: runtime-closeout-selfhost-validation-cleanup-reentry

- issue_id: `I-20260419-0333-A`
- issue_path: `docs/B2-docs/runtime/runtime-closeout-selfhost-validation-followthrough-governance/issues/runtime-closeout-selfhost-validation-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`

## Scope Verdict

- `PASS`: canonical retained-cleanup replay proved runtime-owned worker launch was still correct; the remaining seam was that `worker_exit_contract_repair` handoff weakened the original cleanup prompt into “write any valid exit contract,” which allowed a repair-only `worker_done`.
- `PASS`: `write_worker_exit_contract_repair_handoff()` now carries forward the authoritative cleanup prompt metadata and explicitly restates the bounded cleanup reentry contract, including the four allowed cleanup classifications.
- `PASS`: `worker_runtime_handle_exit_contract_after_ai_cycle()` now rejects a repair-only cleanup `worker_done` when the round is still a cleanup repair resume and its evidence is limited to runtime repair artifacts.
- `PASS`: ordinary worker completion still stops the lane, so this hardening does not regress the normal `worker_done` path outside cleanup repair reentry.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-handoff-rebinds-cleanup-closeout`
2. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-only-done-forces-resume`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
4. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
5. `bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
6. `./bin/governance-check`
7. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-handoff-rebinds-cleanup-closeout`
8. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-repair-only-done-forces-resume`
9. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-forces-resume`
10. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
11. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: bash docs/system/workspace/scripts/tests/test-freely-worker-repair-prompt-prioritizes-exit-contract`
12. `test-pre-merge-20260424-worker-exit-contract-repair-closeout-boundary: ./bin/governance-check`

## Real Replay Evidence

- Canonical root runtime events at `2026-04-24T09:29:44Z` recorded `worker_auto_recovered`, proving runtime, not manager AI, still owned worker startup for the retained cleanup lane.
- Retained worker replay at `2026-04-24T09:30:42Z` wrote `event=worker_exit_contract_done` with summary `Repaired the missing worker exit contract ... no additional cleanup work was performed`, and its `EVIDENCE_PATHS_CSV` contained only `session-handoff.txt` plus `worker-exit-contract.env`.
- The failure therefore came from contract design, not launch ownership drift: the resumed cleanup worker was satisfying the minimal repair shape without re-entering the real cleanup closeout boundary.

## Implementation Decision Note

- decision: `Rebind cleanup repair rounds to the authoritative worker prompt metadata and reject repair-only cleanup completion receipts at runtime.`
- why_this: `The canonical bug was not that runtime failed to restart the lane; it was that the repair contract dropped the original cleanup gate. Restoring that gate in the handoff and hardening acceptance at runtime closes the escape hatch without moving worker launch into manager artifacts.`
- alternatives_considered: `Rely on prompt wording alone; move cleanup outcome classification into manager post-processing; silently accept repair-only receipts and hope later patrol reopens the lane.`
- boundary_non_goals: `This change does not classify the retained dirty residue itself, merge or retire the retained cleanup worktree, or change scan-json task selection policy.`
- residual_risk: `Protected-lane replay after merge is still required to prove the retained cleanup worker now lands on a bounded blocker or retirement outcome and that manager patrol then advances to the next scan-selected task.`
